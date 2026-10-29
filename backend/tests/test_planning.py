"""End-to-end planning on a small fixture catalog: request in, consistent plan out."""

from __future__ import annotations

from dataclasses import replace
from functools import cache
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from gymplanner.api.schemas import PlanRequest, PlanResponse, RectOut
from gymplanner.catalog import Catalog, load_catalog
from gymplanner.domain import Room
from gymplanner.layout import LayoutItem, LayoutResult, LayoutRules, Placement, plan_layout
from gymplanner.planning import PlanError, create_plan, fitting, service
from gymplanner.planning.fitting import Floor, fit_to_floor, layout_rules, selection_of
from gymplanner.planning.service import build_problem
from gymplanner.selection import Constraints, Selection, evaluate, greedy, optimize
from gymplanner.selection import optimizer as optimize_module
from gymplanner.selection.optimizer import (
    COVERAGE_TOLERANCE,
    MIN_UNIT_USE,
    Addition,
    serves_within_tolerance,
)

FIXTURE_DATA = Path(__file__).parent / "fixtures" / "mini_data"


@cache
def catalog() -> Catalog:
    return load_catalog(FIXTURE_DATA)


@cache
def plan(area: float, budget: float, **options: object) -> PlanResponse:
    request = PlanRequest(area_sqft=area, budget_usd=budget, **options)
    return create_plan(request, catalog(), seed=11)


def overlaps(a: RectOut, b: RectOut, tolerance: float = 1e-6) -> bool:
    return (
        a.x < b.x + b.w - tolerance
        and b.x < a.x + a.w - tolerance
        and a.y < b.y + b.h - tolerance
        and b.y < a.y + a.h - tolerance
    )


SIZES = [(800, 15_000), (1_500, 40_000), (6_000, 180_000), (20_000, 900_000)]


@pytest.mark.parametrize(("area", "budget"), SIZES)
def test_plan_stays_within_budget_and_adds_up(area: float, budget: float) -> None:
    result = plan(area, budget)
    costs = result.costs
    assert costs.total_usd <= budget + 0.01
    assert costs.total_usd == pytest.approx(costs.equipment_usd + costs.installation_usd + costs.flooring_usd, abs=0.05)
    assert costs.remaining_usd == pytest.approx(budget - costs.total_usd, abs=0.05)
    assert sum(item.subtotal_usd for item in result.items) == pytest.approx(
        costs.equipment_usd + costs.installation_usd, abs=0.5
    )
    assert sum(c.usd for c in costs.by_category) == pytest.approx(costs.equipment_usd + costs.installation_usd, abs=0.5)


@pytest.mark.parametrize(("area", "budget"), SIZES)
def test_every_unit_is_placed_once_without_collisions(area: float, budget: float) -> None:
    result = plan(area, budget)
    layout = result.layout
    assert len(layout.placements) == result.metrics.unit_count
    for item in result.items:
        placed = [p for p in layout.placements if p.equipment_id == item.equipment_id]
        assert len(placed) == item.units
    floor = RectOut(x=0, y=0, w=layout.width_in, h=layout.depth_in)
    for p in layout.placements:
        assert overlaps(p.rect, floor)
        assert p.rect.x >= -1e-6 and p.rect.x + p.rect.w <= layout.width_in + 1e-6
        assert p.rect.y >= -1e-6 and p.rect.y + p.rect.h <= layout.depth_in + 1e-6
        for q in layout.placements:
            if q.uid != p.uid:
                assert not overlaps(p.rect, q.envelope), (p.uid, q.uid)


def test_metrics_are_shares_and_consistent() -> None:
    result = plan(6_000, 180_000)
    metrics = result.metrics
    assert 0 < metrics.quality_served_share <= metrics.served_share <= 1
    assert 0 <= metrics.coverage_share <= 1
    assert metrics.type_count == len(result.items)
    assert sum(item.units for item in result.items) == metrics.unit_count
    for item in result.items:
        assert 0 <= item.utilization <= 1
        assert 0 <= item.blocking <= 1
        assert item.rationale
    assert all(0 <= c.coverage <= 1 for c in result.coverage)


def test_bigger_gyms_get_more_redundancy() -> None:
    small = plan(1_500, 40_000)
    large = plan(20_000, 900_000)
    small_ratio = small.metrics.unit_count / small.metrics.type_count
    large_ratio = large.metrics.unit_count / large.metrics.type_count
    assert large_ratio > 2 * small_ratio
    assert large.metrics.quality_served_share > small.metrics.quality_served_share


def test_upgrade_note_explains_the_upgrade_list() -> None:
    for area, budget in SIZES:
        result = plan(area, budget)
        assert result.upgrade_note
        if result.next_upgrades:
            assert all(u.cost_usd > 0 and u.gain_share > 0 for u in result.next_upgrades)


def test_simulation_reports_plausible_peak() -> None:
    result = plan(6_000, 180_000)
    sim = result.simulation
    total = sim.first_choice_share + sim.substituted_share + sim.skipped_share
    assert total == pytest.approx(1.0, abs=1e-6)
    assert sim.mean_wait_min <= sim.p90_wait_min + 1e-9 or sim.mean_wait_min < 0.5
    assert sim.peak_concurrent_users > 0


def test_same_request_gives_the_same_plan() -> None:
    request = PlanRequest(area_sqft=3_000, budget_usd=90_000)
    first = create_plan(request, catalog(), seed=5)
    second = create_plan(request, catalog(), seed=5)
    assert first.model_dump(exclude={"compute_ms"}) == second.model_dump(exclude={"compute_ms"})


def test_excluding_a_category_removes_it_and_lowers_quality() -> None:
    base = plan(6_000, 180_000)
    without = plan(6_000, 180_000, exclude=("cardio",))
    assert not any(item.category == "cardio" for item in without.items)
    assert without.metrics.quality_served_share < base.metrics.quality_served_share


def test_profile_exclusions_and_dimensions_are_respected() -> None:
    result = plan(5_000, 150_000, profile="strength", width_ft=50, depth_ft=100)
    assert not any(item.equipment_id == "rower" for item in result.items)
    assert result.inputs.width_ft == pytest.approx(50)
    assert result.inputs.depth_ft == pytest.approx(100)
    assert result.layout.width_in == pytest.approx(600)


def test_members_cap_the_peak_below_the_area_estimate() -> None:
    by_area = plan(6_000, 180_000)
    few_members = plan(6_000, 180_000, members=300)
    assert few_members.demand.method == "members"
    assert few_members.demand.peak_users < by_area.demand.peak_users
    assert few_members.costs.total_usd <= by_area.costs.total_usd + 1


def test_budget_that_cannot_cover_flooring_is_rejected() -> None:
    with pytest.raises(PlanError, match="flooring"):
        create_plan(PlanRequest(area_sqft=10_000, budget_usd=2_000), catalog(), seed=1)


def test_low_ceiling_excludes_tall_equipment_with_a_note() -> None:
    result = plan(6_000, 180_000, ceiling_ft=8)
    assert not any(item.equipment_id in {"treadmill", "power_rack"} for item in result.items)
    assert any(warning.startswith("The ceiling is too low for") for warning in result.warnings)


def test_circuit_note_names_the_equipment_that_needs_one() -> None:
    result = plan(6_000, 180_000)
    treadmills = next(i.units for i in result.items if i.equipment_id == "treadmill")
    expected = (
        "The treadmill needs a dedicated circuit."
        if treadmills == 1
        else f"The {treadmills} treadmills each need a dedicated circuit."
    )
    assert expected in result.warnings


def test_assumptions_follow_the_inputs() -> None:
    default = {a.label: a.value for a in plan(6_000, 180_000).assumptions}
    assert default["Peak occupancy"].endswith("per 1,000 sq ft")
    assert "Reception and lockers" not in default
    assert default["Ceiling"] == "12′, the default; enter yours under More options"
    assert default["Flooring"].endswith("per sq ft on average")

    bare = plan(6_000, 180_000, members=300, ceiling_ft=9.5, include_flooring=False, include_installation=False)
    given = {a.label: a.value for a in bare.assumptions}
    assert given["Peak occupancy"].endswith("from 300 members")
    assert given["Ceiling"] == "9′ 6″"
    assert given["Flooring"] == "Not included"
    assert given["Freight & installation"] == "Not included"
    assert all(a.sources for a in bare.assumptions)


def _without(result: LayoutResult, lost: list[Placement]) -> LayoutResult:
    """The layout as if the lost placements had not fit."""
    kept = [p for p in result.placements if all(p is not q for q in lost)]
    return replace(result, placements=kept, unplaced=[*result.unplaced, *(p.item for p in lost)])


def _floor(area: float, budget: float) -> tuple[Floor, Constraints, Selection]:
    problem = build_problem(PlanRequest(area_sqft=area, budget_usd=budget), catalog())
    floor = Floor(catalog(), problem.room, problem.table, layout_rules(catalog()))
    return floor, problem.constraints, optimize(problem.table, problem.constraints)


def test_fit_loop_keeps_the_most_valuable_plan_that_fits(monkeypatch: pytest.MonkeyPatch) -> None:
    """A re-plan that fits worse than the first attempt's placed units must not replace them."""
    calls: list[int] = []

    def worse_on_the_second_try(
        room: Room, items: list[LayoutItem], rules: LayoutRules
    ) -> LayoutResult:
        result = plan_layout(room, items, rules)
        calls.append(len(items))
        if len(calls) == 1 and result.placements:
            return _without(result, [max(result.placements, key=lambda p: p.item.priority)]) # Losing the most-used unit is worth another try ...
        if len(calls) == 2 and result.placements:
            return _without(result, result.placements[1:]) # ... but the re-plan keeps only one unit.
        return result

    floor, cons, selection = _floor(6_000, 180_000)
    first_placed = selection.units.copy()
    monkeypatch.setattr("gymplanner.planning.fitting.plan_layout", worse_on_the_second_try)
    fitted = fit_to_floor(floor, cons, selection)
    assert len(calls) > 2
    assert fitted.selection.units.sum() >= first_placed.sum() - 1 # The first attempt's units less the lost one, grown with whatever else fits.
    assert fitted.selection.value >= selection.value * 0.9
    assert len(fitted.layout.placements) == fitted.selection.units.sum()
    assert not fitted.layout.unplaced
    assert not any(w.startswith("Left out") for w in fitted.warnings)


def test_fit_loop_stops_once_a_layout_keeps_nearly_all_the_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Within the accepted loss, the first attempt's placed units are the plan; no re-plan."""
    calls: list[int] = []

    def loses_the_least_used_unit(
        room: Room, items: list[LayoutItem], rules: LayoutRules
    ) -> LayoutResult:
        result = plan_layout(room, items, rules)
        calls.append(len(items))
        if len(calls) == 1 and result.placements:
            return _without(result, [min(result.placements, key=lambda p: p.item.priority)])
        return result

    replans: list[int] = []
    real_improve = optimize_module.improve

    def counted_improve(*args: Any, **kwargs: Any) -> Selection:
        replans.append(1)
        return real_improve(*args, **kwargs)

    floor, cons, selection = _floor(6_000, 180_000)
    monkeypatch.setattr("gymplanner.planning.fitting.plan_layout", loses_the_least_used_unit)
    monkeypatch.setattr("gymplanner.planning.fitting.improve", counted_improve)
    monkeypatch.setattr("gymplanner.planning.fitting.FIT_LOSS_ACCEPTED", 1.0)
    fitted = fit_to_floor(floor, cons, selection)
    assert replans == []
    assert fitted.selection.units.sum() >= selection.units.sum() - 1
    assert not any(w.startswith("Left out") for w in fitted.warnings)


def _with_money_left(area: float, budget: float) -> tuple[Floor, Constraints, Selection]:
    """The greedy's plan stopped six steps early: money left, and room for more."""
    floor, cons, full = _floor(area, budget)
    partial = greedy(floor.table, cons, max_steps=max(1, len(full.steps) - 6))
    assert not floor.lay_out(partial).unplaced
    return floor, cons, partial


def test_the_grow_step_offers_less_when_the_layout_pushes_out_the_plan(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """On a crowded floor an offer of several pieces can push out more of the plan than it adds.
    The grow step then offers fewer, down to one piece, rather than repeat the same offer."""
    floor, cons, partial = _with_money_left(6_000, 180_000)
    base = floor.lay_out(partial)
    own = {p.item.uid for p in base.placements}
    count = int(partial.units.sum())

    def crowded(room: Room, items: list[LayoutItem], rules: LayoutRules) -> LayoutResult:
        result = plan_layout(room, items, rules)
        if len(items) > count + 1:
            return _without(result, [p for p in result.placements if p.item.uid in own][1:]) # Two or more new pieces push out all but one of the plan's own units.
        return result

    sizes: list[int] = []
    real_offer = fitting._offer

    def recorded(*args: Any) -> list[Addition]:
        sizes.append(args[-1])
        offer: list[Addition] = real_offer(*args)
        return offer

    monkeypatch.setattr("gymplanner.planning.fitting.plan_layout", crowded)
    monkeypatch.setattr("gymplanner.planning.fitting._offer", recorded)
    grown, layout, _ = fitting._grow(floor, cons, partial, base)
    assert sizes[0] == fitting.GROW_MOVES
    assert 1 in sizes
    assert sizes == sorted(sizes, reverse=True)
    assert grown.units.sum() > count
    assert not layout.unplaced


def test_the_grow_step_never_trades_away_a_held_unit(monkeypatch: pytest.MonkeyPatch) -> None:
    """A layout that makes room for new pieces by leaving out a held unit is not kept, so the
    constraints never hold more than the plan has."""
    floor, cons, partial = _with_money_left(6_000, 180_000)
    present = np.flatnonzero(partial.units)
    cheapest = int(present[np.argmin(cons.unit_cost[present])])
    held = replace(cons, min_units=np.where(np.arange(len(partial.units)) == cheapest, 1, 0))
    count = int(partial.units.sum())

    def pushes_out_the_held(
        room: Room, items: list[LayoutItem], rules: LayoutRules
    ) -> LayoutResult:
        result = plan_layout(room, items, rules)
        if len(items) > count:
            gone = floor.table.equipment_ids[cheapest]
            return _without(result, [p for p in result.placements if p.item.equipment_id == gone])
        return result

    monkeypatch.setattr("gymplanner.planning.fitting.plan_layout", pushes_out_the_held)
    fitted = fit_to_floor(floor, held, partial)
    assert fitted.selection.units[cheapest] >= 1
    assert fitted.constraints.min_units is not None
    assert (fitted.constraints.min_units <= fitted.selection.units).all()


def test_upgrades_the_money_left_already_buys_are_bought() -> None:
    floor, cons, partial = _with_money_left(6_000, 180_000)
    fitted = fitting.Fitted(partial, floor.lay_out(partial), cons, frozenset(), [])
    steps = fitting.upgrades(floor, fitted)
    assert steps and steps[0].cost <= cons.budget_usd - partial.cost
    bought = fitting.bought_upgrades(floor, fitted, steps)
    assert bought is not None
    assert bought.selection.units.sum() > partial.units.sum()
    assert bought.selection.cost <= cons.budget_usd + 1e-6
    assert len(bought.layout.placements) == bought.selection.units.sum()
    assert not bought.layout.unplaced


@pytest.mark.parametrize("members", [1, 60])
def test_the_coverage_rule_adds_only_stations_that_see_use(
    members: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Every type the coverage rule brings in is in use at least ``MIN_UNIT_USE`` per unit at the
    peak, even in a gym with one member, and the plan serves within the rule's tolerance."""
    request = PlanRequest(area_sqft=3_000, budget_usd=200_000, members=members)
    rounded = create_plan(request, catalog(), seed=11)
    monkeypatch.setattr(service, "COVERAGE_TRIES", 0)
    plain = create_plan(request, catalog(), seed=11)
    before = {item.equipment_id for item in plain.items}
    for item in rounded.items:
        if item.equipment_id not in before:
            assert item.served_users / item.units >= MIN_UNIT_USE, item.equipment_id
    assert rounded.metrics.coverage_share >= plain.metrics.coverage_share
    assert serves_within_tolerance(
        rounded.metrics.quality_served_share,
        plain.metrics.quality_served_share,
        COVERAGE_TOLERANCE,
    )


def test_a_gym_with_few_members_says_more_equipment_would_see_little_use(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(service, "COVERAGE_TRIES", 0) # The coverage rule rounds this plan out past 90% served, where the note says demand is met; without it the plan stops where each further unit would see little use.
    result = create_plan(PlanRequest(area_sqft=3_000, budget_usd=200_000, members=5), catalog(), seed=11)
    assert result.costs.remaining_usd > 0.5 * result.costs.budget_usd
    reason = "with about 1 person on the floor at the busiest hour, more equipment would see"
    assert any(reason in w for w in result.warnings if "unallocated" in w)
    assert result.upgrade_note.startswith("With about 1 person on the floor")
    assert not result.next_upgrades
    assert result.budget_note is None


def test_a_floor_bound_plan_says_the_floor_is_full_not_that_demand_is_met() -> None:
    result = plan(400, 200_000)
    assert result.metrics.served_share < 0.9
    (unallocated,) = [w for w in result.warnings if "unallocated" in w]
    assert "nothing more that is worth buying fits on this floor" in unallocated
    assert result.upgrade_note.startswith("The floor is full")
    assert not any("demand is already met" in w for w in [result.upgrade_note, *result.warnings])
    assert result.budget_note is None


def test_every_upgrade_fits_beside_the_plan_and_the_upgrades_before_it() -> None:
    for area, budget in [(1_500, 40_000), (6_000, 180_000), (800, 15_000)]:
        result = plan(area, budget)
        problem = build_problem(PlanRequest(area_sqft=area, budget_usd=budget), catalog())
        table, cons = problem.table, problem.constraints
        units = np.zeros(table.n_equipment, dtype=np.int64)
        for item in result.items:
            units[table.index_of(item.equipment_id)] = item.units
        floor = Floor(catalog(), problem.room, table, layout_rules(catalog()))
        for upgrade in result.next_upgrades:
            for step in upgrade.items:
                units[table.index_of(step.equipment_id)] += step.units
            assert not floor.lay_out(selection_of(table, cons, units)).unplaced, (area, upgrade)
        if result.next_upgrades:
            assert result.upgrade_note.startswith("What a bigger budget would add next")


@pytest.mark.parametrize(
    ("options", "message"),
    [
        ({"exclude": list(service.CATEGORY_LABELS)}, "the exclusions leave out every piece"),
        ({"width_ft": 6, "depth_ft": 50}, "Nothing fits a 6′ × 50′ floor"),
        (
            { # The treadmill and the power rack are all that is left, and both need 9 ft.
                "ceiling_ft": 7,
                "exclude": [
                    *(c for c in service.CATEGORY_LABELS if c not in {"cardio", "racks_barbells"}),
                    "upright_bike",
                    "rower",
                ],
            },
            "needs a higher ceiling",
        ),
    ],
)
def test_a_request_that_leaves_nothing_to_plan_is_an_error_that_says_why(
    options: dict[str, object], message: str
) -> None:
    with pytest.raises(PlanError, match=message):
        create_plan(PlanRequest(area_sqft=3_000, budget_usd=100_000, **options), catalog(), seed=1)


def test_a_budget_that_only_just_covers_flooring_is_an_error_that_says_why() -> None:
    problem = build_problem(PlanRequest(area_sqft=2_000, budget_usd=100_000), catalog())
    cheapest = float(problem.constraints.unit_cost.min())
    budget = problem.flooring_usd + cheapest / 2
    with pytest.raises(PlanError, match="less than the cheapest piece"):
        create_plan(PlanRequest(area_sqft=2_000, budget_usd=budget), catalog(), seed=1)


def test_equipment_left_out_still_counts_as_what_members_want() -> None:
    without = plan(6_000, 180_000, exclude=("treadmill",)) # Without treadmills, runners settle for a bike only as willingly as they would if the treadmills were busy: the plan's served share is measured as if they were in the gym.
    problem = build_problem(PlanRequest(area_sqft=6_000, budget_usd=180_000), catalog())
    table = problem.table
    units = np.zeros(table.n_equipment, dtype=np.int64)
    for item in without.items:
        units[table.index_of(item.equipment_id)] = item.units
    with_treadmill_slot = evaluate(table, units)
    assert without.metrics.served_share == pytest.approx(
        float(with_treadmill_slot.served[0]) / table.total_load, rel=1e-6
    )


def test_the_most_wanted_rule_compares_the_plans_as_laid_out(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A held plan within tolerance before the layout but not after it gives way, and one the
    layout keeps within tolerance is chosen."""
    problem = build_problem(PlanRequest(area_sqft=6_000, budget_usd=180_000), catalog())
    floor = Floor(catalog(), problem.room, problem.table, layout_rules(catalog()))
    cons = problem.constraints
    free = optimize(problem.table, cons)
    held = replace(cons, min_units=free.units.copy())
    monkeypatch.setattr(service, "most_wanted_holds", lambda *_: iter([(free, held)]))
    real = fitting.fit_to_floor

    def held_plan_loses(share: float) -> Any:
        def fit(floor: Floor, cons: Constraints, selection: Selection) -> fitting.Fitted:
            fitted = real(floor, cons, selection)
            if cons.min_units is None:
                return fitted
            evaluation = replace(fitted.selection.evaluation, value=fitted.selection.evaluation.value * share)
            return replace(fitted, selection=replace(fitted.selection, evaluation=evaluation))

        return fit

    monkeypatch.setattr(service, "fit_to_floor", held_plan_loses(0.9))
    assert service._fitted_plan(floor, cons).constraints.min_units is None
    monkeypatch.setattr(service, "fit_to_floor", held_plan_loses(0.97))
    assert service._fitted_plan(floor, cons).constraints.min_units is not None
