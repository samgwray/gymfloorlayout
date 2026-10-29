"""Plan orchestration: inputs -> room -> demand -> selection -> layout -> simulation -> response."""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from gymplanner.api import schemas as out
from gymplanner.catalog.loader import Catalog
from gymplanner.catalog.schema import MODALITIES, Category, ZoneId
from gymplanner.demand import build_demand
from gymplanner.domain import SQIN_PER_SQFT, Demand, PlanInputs, Room
from gymplanner.layout import LayoutResult, LayoutRules, Rect, fits_alone
from gymplanner.planning.fitting import (
    Fitted,
    Floor,
    bought_upgrades,
    fit_to_floor,
    layout_item,
    layout_rules,
    placed_units,
    selection_of,
    upgrades,
)
from gymplanner.planning.reasons import (
    RuledOut,
    nothing_to_plan,
    plan_limit,
    ruled_out_notes,
    unallocated_warning,
    upgrade_note,
)
from gymplanner.planning.room import (
    build_room,
    effective_area_sqin,
    envelope_area_sqin,
    fits_room,
)
from gymplanner.planning.shortfall import budget_note, budget_shortfall
from gymplanner.planning.wording import capitalized, feet_inches, list_of, people, the_units
from gymplanner.selection import (
    Constraints,
    RouteTable,
    Selection,
    build_route_table,
    optimize,
)
from gymplanner.selection.explain import (
    PatternCoverage,
    TypeUsage,
    coverage_share,
    pattern_coverage,
    type_usage,
)
from gymplanner.selection.optimizer import (
    COVERAGE_TOLERANCE,
    COVERAGE_TRIES,
    MIN_UNIT_USE,
    UNCAPPED,
    coverage_moves,
    held_addition,
    most_wanted_holds,
    serves_within_tolerance,
)
from gymplanner.simulation import SimulationConfig, SimulationResult, simulate_peak

LEFTOVER_WARNING_SHARE = 0.15

CATEGORY_LABELS: dict[Category, str] = {
    "cardio": "Cardio",
    "racks_barbells": "Racks & barbells",
    "free_weights": "Dumbbells & benches",
    "selectorized": "Selectorized machines",
    "plate_loaded": "Plate-loaded machines",
    "cables": "Cable stations",
    "functional": "Functional & turf",
    "mobility": "Mobility & stretching",
}

MODALITY_LABELS: dict[str, str] = {
    "cardio": "cardio",
    "barbell": "barbell",
    "dumbbell": "dumbbell",
    "machine": "machines",
    "cable": "cables",
    "bodyweight": "bodyweight",
    "functional": "functional",
    "mobility": "mobility",
}
"""Kinds of training as they read inside a sentence."""

MODALITY_ZONE: dict[str, ZoneId] = {
    "cardio": "cardio",
    "machine": "machines",
    "cable": "machines",
    "barbell": "free_weights",
    "dumbbell": "free_weights",
    "functional": "functional",
    "bodyweight": "stretching",
    "mobility": "stretching",
}


class PlanError(ValueError):
    """The request cannot produce a plan (e.g. the budget does not cover flooring)."""


@dataclass(frozen=True)
class _Problem:
    inputs: PlanInputs
    room: Room
    demand: Demand
    table: RouteTable
    constraints: Constraints
    flooring_usd: float
    flooring_rate: float
    ruled_out: RuledOut
    excluded_notes: list[str]


def resolve_inputs(request: out.PlanRequest, catalog: Catalog) -> PlanInputs:
    profile = request.profile or catalog.behavior.default_profile
    if profile not in catalog.profile_by_id:
        raise PlanError(f"unknown profile '{profile}'")
    grade = request.grade or catalog.costs.default_grade
    known = set(catalog.equipment_by_id) | set(CATEGORY_LABELS)
    unknown = [ref for ref in request.exclude if ref not in known]
    if unknown:
        raise PlanError(f"unknown equipment or category to exclude: {', '.join(unknown)}")
    return PlanInputs(
        area_sqft=_floor_area(request, catalog.space.aisles.main_aisle_in),
        budget_usd=request.budget_usd,
        profile_id=profile,
        grade_id=grade,
        width_ft=request.width_ft,
        depth_ft=request.depth_ft,
        ceiling_ft=request.ceiling_ft,
        members=request.members,
        include_flooring=request.include_flooring,
        include_installation=request.include_installation,
        entrance=request.entrance,
        excluded_equipment=tuple(request.exclude),
    )


def _floor_area(request: out.PlanRequest, main_aisle_in: float) -> float:
    """The training floor's area once its sides are known, held to the same limits as an area.

    Given sides replace the square footage; one given side makes the other the area over it.
    A side shorter than the main aisle leaves nothing to plan.
    """
    area, width, depth = request.area_sqft, request.width_ft, request.depth_ft
    if width and depth:
        area = width * depth
        if not out.AREA_MIN_SQFT <= area <= out.AREA_MAX_SQFT:
            raise PlanError(
                f"{width:,.4g} × {depth:,.4g} ft is {area:,.0f} sq ft; plans cover "
                f"{out.AREA_MIN_SQFT:,.0f} to {out.AREA_MAX_SQFT:,.0f} sq ft."
            )
    elif width:
        depth = area / width
    elif depth:
        width = area / depth
    else:
        return area
    side, short = ("wide", width) if width <= depth else ("deep", depth)
    if short * 12 < main_aisle_in:
        raise PlanError(
            f"A floor {feet_inches(short * 12)} {side} has no room for the "
            f"{feet_inches(main_aisle_in)} main aisle."
        )
    return area


def _flooring_rate(catalog: Catalog, demand: Demand) -> float:
    """Blended $/sq ft: each zone's flooring weighted by the time members spend there."""
    rates = {f.id: f.cost_per_sqft.typical for f in catalog.costs.flooring}
    zone_rate = {z.id: rates[z.flooring] for z in catalog.space.zones}
    fallback = sum(zone_rate.values()) / len(zone_rate)
    return sum(demand.modality_share[m] * zone_rate.get(MODALITY_ZONE[m], fallback) for m in MODALITIES)


def _allowed_equipment(
    catalog: Catalog, inputs: PlanInputs, room: Room, rules: LayoutRules
) -> tuple[list[str], RuledOut]:
    """The equipment the plan may buy, and what the ceiling and the floor rule out."""
    profile = catalog.profile_by_id[inputs.profile_id]
    excluded = set(profile.excluded_equipment)
    for ref in inputs.excluded_equipment:
        if ref in CATEGORY_LABELS:
            excluded |= {e.id for e in catalog.equipment if e.category == ref}
        else:
            excluded.add(ref)
    allowed: list[str] = []
    too_tall: list[str] = []
    too_big: list[str] = []
    for item in catalog.equipment:
        if item.id in excluded:
            continue
        if item.min_ceiling_in and item.min_ceiling_in > room.ceiling_in:
            too_tall.append(item.id)
        elif not fits_room(item, room):
            too_big.append(item.id)
        else:
            allowed.append(item.id)
    lone = [layout_item(catalog.equipment_by_id[eid], eid, 0.0) for eid in allowed] # The layout has the last word: a unit it cannot place on its own, aisles kept clear, is never placed, so the optimizer must not spend on it.
    alone = {item.equipment_id for item in fits_alone(room, lone, rules)}
    too_big += [eid for eid in allowed if eid not in alone]
    allowed = [eid for eid in allowed if eid in alone]
    changed = True # Drop items whose prerequisites were removed.
    while changed:
        changed = False
        for eid in list(allowed):
            if any(req not in allowed for req in catalog.equipment_by_id[eid].requires):
                allowed.remove(eid)
                changed = True
    ruled_out = RuledOut(excluded=bool(inputs.excluded_equipment), too_tall=tuple(too_tall), too_big=tuple(too_big))
    return allowed, ruled_out


def _first_choice_load(catalog: Catalog, demand: Demand, offered: set[str]) -> dict[str, float]:
    """Offered load of the exercises each type is in the best route of, over all the equipment
    the gym's format offers: what members would ask for."""
    load: dict[str, float] = defaultdict(float)
    for exercise in catalog.exercises:
        erlangs = demand.exercise_load.get(exercise.id, 0.0)
        options = [o for o in exercise.options if offered.issuperset(o.uses)]
        if erlangs <= 0 or not options:
            continue
        for eid in max(options, key=lambda o: (o.quality, -len(o.uses))).uses:
            load[eid] += erlangs
    return load


def build_problem(request: out.PlanRequest, catalog: Catalog) -> _Problem:
    inputs = resolve_inputs(request, catalog)
    room = build_room(inputs, catalog)
    demand = build_demand(catalog, inputs.profile_id, room.training_sqft, inputs.members)
    allowed, ruled_out = _allowed_equipment(catalog, inputs, room, layout_rules(catalog))
    format_excludes = set(catalog.profile_by_id[inputs.profile_id].excluded_equipment) # Members still measure what the plan has against equipment it leaves out or has no room for; only what the gym's format never offers is out of their minds.
    offered = {e.id for e in catalog.equipment if e.id not in format_excludes}
    table = build_route_table(catalog, demand, allowed, offered=offered)
    notes = ruled_out_notes(catalog, _first_choice_load(catalog, demand, offered), demand.total_load, ruled_out)

    flooring_rate = _flooring_rate(catalog, demand) if inputs.include_flooring else 0.0
    flooring_usd = flooring_rate * room.training_sqft
    install = catalog.costs.installation_rate if inputs.include_installation else 0.0
    unit_cost = np.array([catalog.unit_price(eid, inputs.grade_id) * (1 + install) for eid in allowed])
    unit_area = np.array([effective_area_sqin(catalog.equipment_by_id[eid]) for eid in allowed])
    index = {eid: i for i, eid in enumerate(allowed)}
    constraints = Constraints(
        budget_usd=max(0.0, inputs.budget_usd - flooring_usd),
        area_sqin=room.training_sqft * SQIN_PER_SQFT * catalog.space.packing_efficiency,
        unit_cost=unit_cost,
        unit_area=unit_area,
        max_units=np.array([catalog.equipment_by_id[eid].max_units or UNCAPPED for eid in allowed], dtype=np.int64),
        requires=tuple(tuple(index[req] for req in catalog.equipment_by_id[eid].requires) for eid in allowed),
    )
    return _Problem(
        inputs=inputs,
        room=room,
        demand=demand,
        table=table,
        constraints=constraints,
        flooring_usd=flooring_usd,
        flooring_rate=flooring_rate,
        ruled_out=ruled_out,
        excluded_notes=notes,
    )


def _fitted_plan(floor: Floor, cons: Constraints) -> Fitted:
    """The plan laid out: the optimizer's, or one that holds the most-wanted type when, once both
    are laid out, it serves within ``MOST_WANTED_TOLERANCE`` of it."""
    free = optimize(floor.table, cons)
    plain = fit_to_floor(floor, cons, free)
    for plan, held in most_wanted_holds(floor.table, cons, free):
        fitted = fit_to_floor(floor, held, plan)
        if serves_within_tolerance(fitted.selection.value, plain.selection.value):
            return fitted
    return plain


def _rounded_out(floor: Floor, cons: Constraints, fitted: Fitted) -> Fitted:
    """``fitted`` with stations added, one at a time and the one that gives the most demand a
    well-suited option first, while the plan as laid out serves within ``COVERAGE_TOLERANCE`` of
    ``fitted`` and gives more of its demand a well-suited option."""
    table = floor.table
    anchor = fitted.selection.value
    covered = coverage_share(table, fitted.selection.units)
    tried: set[frozenset[int]] = set()
    for _ in range(COVERAGE_TRIES):
        move = next(
            (
                m
                for m in coverage_moves(table, cons, fitted.selection.units)
                if frozenset(m.added) not in tried
            ),
            None,
        )
        if move is None:
            break
        tried.add(frozenset(move.added))
        found = held_addition(table, fitted.constraints, fitted.selection, move.added)
        if found is None:
            continue
        plan, held = found
        if not _well_used(held, plan, move.added): # Like any purchase, the station must see ``MIN_UNIT_USE``: in a gym with few members nobody would use it. Checked here to spare a layout, and again on the plan kept.
            continue
        if not serves_within_tolerance(plan.value, anchor, COVERAGE_TOLERANCE): # Fitting keeps at least what the first layout places, and laying out rarely raises a plan's value: a plan outside the tolerance before layout, or once laid out the first time, is not fitted.
            continue
        first = selection_of(table, held, placed_units(table, held, floor.lay_out(plan)))
        if not serves_within_tolerance(first.value, anchor, COVERAGE_TOLERANCE):
            continue
        trial = fit_to_floor(floor, held, plan)
        share = coverage_share(table, trial.selection.units)
        if (
            share > covered
            and _well_used(held, trial.selection, move.added)
            and serves_within_tolerance(trial.selection.value, anchor, COVERAGE_TOLERANCE)
        ):
            fitted, covered = trial, share
    return fitted


def _well_used(cons: Constraints, selection: Selection, added: dict[int, int]) -> bool:
    """Whether each type a coverage move adds for its own sake, not only as another's
    prerequisite, is in ``selection`` and in use at least ``MIN_UNIT_USE`` per unit."""
    prerequisites = {p for r in added for p in cons.requires[r]}
    own = [r for r in added if r not in prerequisites] or list(added)
    carried = selection.evaluation.carried()[0]
    return all(selection.units[r] > 0 and carried[r] / selection.units[r] >= MIN_UNIT_USE for r in own)


def _rationale(eid: str, use: TypeUsage, catalog: Catalog) -> str:
    """One plain sentence: what the equipment is for and how busy it gets at peak."""
    uses = [name.lower() for name in use.top_exercises[:2]]
    purpose = f"For {' and '.join(uses)}" if uses else "Rounds out the floor"
    busy = f"in use {use.utilization:.0%} of the time at peak"
    note = ""
    if use.blocking > 0.25 and use.next_unit_value > 0:
        note = "; another would cut the wait"
    elif catalog.equipment_by_id[eid].power == "dedicated_circuit":
        note = "; needs a dedicated circuit"
    return f"{purpose}, {busy}{note}."


def _simulate(
    catalog: Catalog, problem: _Problem, units: NDArray[np.int64], seed: int
) -> SimulationResult:
    session = catalog.behavior.session
    config = SimulationConfig(
        peak_users=problem.demand.peak.peak_users,
        mean_floor_minutes=session.mean_floor_minutes,
        floor_minutes_cv=session.cv,
        idle_share=session.idle_share,
        seed=seed,
    )
    block_minutes = {e.id: e.block_minutes for e in catalog.exercises}
    routed = set(problem.table.exercise_ids)
    unroutable = {
        exercise_id: load
        for exercise_id, load in problem.demand.exercise_load.items()
        if load > 0 and exercise_id not in routed
    }
    return simulate_peak(problem.table, units, block_minutes, config, unroutable=unroutable)


def _assumptions(catalog: Catalog, problem: _Problem) -> list[out.AssumptionOut]:
    """The figures behind the plan, worded for people rather than for a log."""
    behavior, space, costs = catalog.behavior, catalog.space, catalog.costs
    inputs = problem.inputs
    profile = catalog.profile_by_id[inputs.profile_id]
    peak = problem.demand.peak
    if peak.capped_by_code:
        occupancy = f"{people(peak.peak_users)}, the building-code limit"
    elif peak.method == "members" and inputs.members is not None:
        occupancy = f"{people(peak.peak_users)}, from {inputs.members:,} members"
    else:
        density = profile.peak_users_per_1000_sqft or behavior.occupancy.peak_users_per_1000_sqft
        occupancy = f"{people(peak.peak_users)}, {density:g} per 1,000 sq ft"
    mix = ", ".join(f"{MODALITY_LABELS[m]} {s:.0%}" for m, s in profile.modality_share.as_dict().items() if s)
    ceiling = feet_inches(problem.room.ceiling_in) # Without an entered height the room has the default ceiling (see ``build_room``).
    if not inputs.ceiling_ft:
        ceiling = f"{ceiling}, the default; enter yours under More options"
    return [
        out.AssumptionOut(label="Peak occupancy", value=occupancy, sources=list(behavior.occupancy.sources)),
        out.AssumptionOut(
            label="Visit length",
            value=(
                f"{behavior.session.mean_floor_minutes:.0f} minutes, "
                f"{behavior.session.idle_share:.0%} of it between stations"
            ),
            sources=list(behavior.session.sources),
        ),
        out.AssumptionOut(label="Training mix", value=capitalized(mix), sources=list(profile.sources)),
        out.AssumptionOut(
            label="Aisles",
            value=(
                f"{feet_inches(space.aisles.main_aisle_in)} main aisle, "
                f"{feet_inches(space.aisles.secondary_aisle_in)} between rows"
            ),
            sources=list(space.aisles.sources),
        ),
        out.AssumptionOut(label="Ceiling", value=ceiling, sources=list(space.sources)),
        out.AssumptionOut(
            label="Flooring",
            value=(
                f"${problem.flooring_rate:.2f} per sq ft on average"
                if inputs.include_flooring
                else "Not included"
            ),
            sources=sorted({s for f in costs.flooring for s in f.sources}),
        ),
        out.AssumptionOut(
            label="Freight & installation",
            value=(
                f"{costs.installation_rate:.0%} of the equipment price"
                if inputs.include_installation
                else "Not included"
            ),
            sources=list(costs.installation_sources),
        ),
    ]


def _circuit_note(items: list[out.LineItemOut]) -> str | None:
    """'The 3 treadmills each need a dedicated circuit.'"""
    needing = [i for i in items if i.power == "dedicated_circuit" and i.units > 0]
    if not needing:
        return None
    who = list_of([the_units(i.name, i.units) for i in needing])
    verb = "needs" if sum(i.units for i in needing) == 1 else "each need"
    return f"{capitalized(who)} {verb} a dedicated circuit."


def _nothing_to_plan(catalog: Catalog, problem: _Problem, allowed: bool) -> str:
    cons = problem.constraints
    return nothing_to_plan(
        catalog,
        problem.room.width_in,
        problem.room.depth_in,
        problem.ruled_out,
        allowed=allowed,
        equipment_budget=cons.budget_usd,
        cheapest=float(cons.unit_cost.min()) if len(cons.unit_cost) else None,
        demand=problem.demand,
    )


def create_plan(request: out.PlanRequest, catalog: Catalog, seed: int) -> out.PlanResponse:
    started = time.perf_counter()
    problem = build_problem(request, catalog)
    inputs, room, table = problem.inputs, problem.room, problem.table
    warnings = list(problem.excluded_notes)
    if inputs.include_flooring and problem.flooring_usd >= inputs.budget_usd:
        raise PlanError(
            f"The budget does not cover flooring for {room.training_sqft:,.0f} sq ft "
            f"(about ${problem.flooring_usd:,.0f}). Raise the budget or leave flooring out."
        )

    if not table.equipment_ids:
        raise PlanError(_nothing_to_plan(catalog, problem, allowed=False))
    floor = Floor(catalog, room, table, layout_rules(catalog))
    fitted = _rounded_out(floor, problem.constraints, _fitted_plan(floor, problem.constraints))
    if not fitted.selection.units.any():
        raise PlanError(_nothing_to_plan(catalog, problem, allowed=True))
    steps = upgrades(floor, fitted)
    bought = bought_upgrades(floor, fitted, steps)
    if bought is not None:
        fitted = bought
        steps = upgrades(floor, fitted)
    selection, layout = fitted.selection, fitted.layout
    warnings += fitted.warnings
    units = selection.units
    evaluation = selection.evaluation
    total_load = max(table.total_load, 1e-9)
    usage = type_usage(catalog, table, units, evaluation)

    install_rate = catalog.costs.installation_rate if inputs.include_installation else 0.0
    unit_price = {eid: catalog.unit_price(eid, inputs.grade_id) for eid in table.equipment_ids}

    items: list[out.LineItemOut] = []
    category_cost: dict[Category, float] = defaultdict(float)
    footprint_sqft = 0.0
    envelope_sqft = 0.0
    for r in np.flatnonzero(units):
        eid = table.equipment_ids[int(r)]
        equipment = catalog.equipment_by_id[eid]
        n = int(units[r])
        price = unit_price[eid]
        install = price * install_rate * n
        subtotal = price * n + install
        category_cost[equipment.category] += subtotal
        fp = equipment.footprint.length_in * equipment.footprint.width_in / SQIN_PER_SQFT
        env = envelope_area_sqin(equipment) / SQIN_PER_SQFT
        footprint_sqft += fp * n
        envelope_sqft += env * n
        use = usage[eid]
        items.append(
            out.LineItemOut(
                equipment_id=eid,
                name=equipment.name,
                category=equipment.category,
                zone=equipment.zone,
                units=n,
                stations=equipment.stations,
                unit_price_usd=round(price, 2),
                installation_usd=round(install, 2),
                subtotal_usd=round(subtotal, 2),
                footprint_sqft=round(fp, 2),
                envelope_sqft=round(env, 2),
                utilization=use.utilization,
                blocking=use.blocking,
                served_users=use.served_users,
                top_exercises=use.top_exercises,
                rationale=_rationale(eid, use, catalog),
                example_models=list(equipment.example_models),
                power=equipment.power,
            )
        )
    zone_rank = {z.id: z.order for z in catalog.space.zones}
    items.sort(key=lambda i: (zone_rank[i.zone], -i.subtotal_usd))

    equipment_usd = sum(unit_price[table.equipment_ids[int(r)]] * int(units[r]) for r in np.flatnonzero(units))
    installation_usd = equipment_usd * install_rate
    total_usd = equipment_usd + installation_usd + problem.flooring_usd
    remaining = inputs.budget_usd - total_usd
    served_share = float(evaluation.served[0]) / total_load
    limit = plan_limit(catalog, table, fitted.constraints, selection, steps)
    shortfall = budget_shortfall(floor, problem.constraints, selection, limit)
    why = (problem.demand, served_share, problem.ruled_out)
    if remaining > LEFTOVER_WARNING_SHARE * inputs.budget_usd:
        warnings.append(unallocated_warning(remaining, limit, *why))
    next_upgrades = [
        out.UpgradeOut(
            items=[
                out.UpgradeItemOut(
                    equipment_id=table.equipment_ids[r],
                    name=catalog.equipment_by_id[table.equipment_ids[r]].name,
                    units=n,
                )
                for r, n in step.added.items()
            ],
            cost_usd=round(step.cost, 2),
            gain_share=step.gain / total_load,
        )
        for step in steps
    ]
    simulation = _simulate(catalog, problem, units, seed)
    coverage = pattern_coverage(catalog, table, units)
    circuits = _circuit_note(items)
    if circuits:
        warnings.append(circuits)
    peak = problem.demand.peak
    if peak.capped_by_code:
        warnings.append("Occupancy was capped at the building-code occupant load for the floor.")
    if peak.member_users is not None and peak.member_users > peak.area_users * 1.05:
        warnings.append(
            f"Your membership implies about {peak.member_users:.0f} people on the floor at the "
            f"busiest hour, more than {room.training_sqft:,.0f} sq ft holds comfortably "
            f"(about {peak.area_users:.0f}). The plan is sized for {peak.peak_users:.0f}."
        )
    warnings += layout.warnings

    zone_area: dict[ZoneId, float] = defaultdict(float)
    for zone in layout.zones:
        zone_area[zone.zone] += zone.rect.area / SQIN_PER_SQFT
    training = room.training_sqft
    by_zone = [
        out.ZoneSpaceOut(
            zone=z.id,
            name=z.name,
            sqft=round(zone_area.get(z.id, 0.0), 1),
            share=zone_area.get(z.id, 0.0) / training if training else 0.0,
        )
        for z in sorted(catalog.space.zones, key=lambda z: z.order)
        if zone_area.get(z.id, 0.0) > 0
    ]

    profile = catalog.profile_by_id[inputs.profile_id]
    response = out.PlanResponse(
        inputs=out.ResolvedInputsOut(
            area_sqft=round(room.training_sqft, 1),
            budget_usd=inputs.budget_usd,
            profile=inputs.profile_id,
            grade=inputs.grade_id,
            width_ft=round(room.width_in / 12, 2),
            depth_ft=round(room.depth_in / 12, 2),
            ceiling_ft=round(room.ceiling_in / 12, 2),
            members=inputs.members,
            include_flooring=inputs.include_flooring,
            include_installation=inputs.include_installation,
            entrance=inputs.entrance,
            exclude=list(inputs.excluded_equipment),
        ),
        demand=out.DemandOut(
            profile_id=profile.id,
            profile_name=profile.name,
            peak_users=problem.demand.peak.peak_users,
            active_users=problem.demand.active_users,
            members_estimate=problem.demand.peak.members,
            method=problem.demand.peak.method,
            capped_by_code=problem.demand.peak.capped_by_code,
            modality_share=problem.demand.modality_share,
        ),
        metrics=out.MetricsOut(
            served_share=served_share,
            quality_served_share=float(evaluation.value[0]) / total_load,
            coverage_share=coverage_share(table, units),
            unit_count=int(units.sum()),
            type_count=int((units > 0).sum()),
        ),
        costs=out.CostsOut(
            budget_usd=inputs.budget_usd,
            equipment_usd=round(equipment_usd, 2),
            installation_usd=round(installation_usd, 2),
            flooring_usd=round(problem.flooring_usd, 2),
            total_usd=round(total_usd, 2),
            remaining_usd=round(remaining, 2),
            by_category=[
                out.CategoryCostOut(category=c, label=CATEGORY_LABELS[c], usd=round(v, 2))
                for c, v in sorted(category_cost.items(), key=lambda kv: -kv[1])
            ],
        ),
        space=out.SpaceOut(
            training_sqft=round(training, 1),
            equipment_footprint_sqft=round(footprint_sqft, 1),
            equipment_envelope_sqft=round(envelope_sqft, 1),
            by_zone=by_zone,
        ),
        items=items,
        layout=_layout_out(layout, catalog),
        coverage=[_coverage_out(c, catalog) for c in coverage],
        simulation=_simulation_out(simulation, catalog),
        next_upgrades=next_upgrades,
        upgrade_note=upgrade_note(bool(next_upgrades), limit, *why),
        budget_note=(
            budget_note(shortfall, inputs.budget_usd, problem.flooring_usd) if shortfall else None
        ),
        warnings=warnings,
        assumptions=_assumptions(catalog, problem),
        data_version=catalog.data_version,
        compute_ms=round((time.perf_counter() - started) * 1000, 1),
    )
    return response


def _rect(r: Rect) -> out.RectOut:
    return out.RectOut(x=round(r.x, 2), y=round(r.y, 2), w=round(r.w, 2), h=round(r.h, 2))


def _layout_out(layout: LayoutResult, catalog: Catalog) -> out.LayoutOut:
    return out.LayoutOut(
        width_in=round(layout.width_in, 2),
        depth_in=round(layout.depth_in, 2),
        entrance_x_in=round(layout.entrance_x_in, 2),
        zones=[
            out.ZoneOut(id=z.zone, name=catalog.zone_by_id[z.zone].name, rect=_rect(z.rect))
            for z in layout.zones
        ],
        aisles=[_rect(a) for a in layout.aisles],
        placements=[
            out.PlacementOut(
                uid=p.item.uid,
                equipment_id=p.item.equipment_id,
                name=p.item.name,
                zone=p.item.zone,
                rect=_rect(p.rect),
                envelope=_rect(p.envelope),
                rotation=p.rotation,
            )
            for p in layout.placements
        ],
        warnings=list(layout.warnings),
        notes=list(layout.notes),
    )


def _coverage_out(c: PatternCoverage, catalog: Catalog) -> out.PatternCoverageOut:
    return out.PatternCoverageOut(
        pattern=c.pattern,
        label=c.label,
        coverage=c.coverage,
        equipment=[catalog.equipment_by_id[eid].name for eid in c.equipment_ids],
    )


def _simulation_out(sim: SimulationResult, catalog: Catalog) -> out.SimulationOut:
    busiest = sorted(sim.utilization.items(), key=lambda kv: -kv[1])[:5]
    return out.SimulationOut(
        seed=sim.seed,
        simulated_minutes=sim.simulated_minutes,
        visits=sim.visits,
        exercise_blocks=sim.exercise_blocks,
        mean_wait_min=sim.mean_wait_min,
        p90_wait_min=sim.p90_wait_min,
        first_choice_share=sim.first_choice_share,
        substituted_share=sim.substituted_share,
        skipped_share=sim.skipped_share,
        peak_concurrent_users=sim.peak_concurrent_users,
        busiest=[
            out.BusyEquipmentOut(equipment_id=eid, name=catalog.equipment_by_id[eid].name, utilization=u)
            for eid, u in busiest
        ],
    )
