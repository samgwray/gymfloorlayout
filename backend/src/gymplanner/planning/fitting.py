"""Fit a selection to the floor: the layout, not the optimizer's area model, has the last word.

The optimizer budgets space with a packing-efficiency estimate of the floor. Aisles take more
of a small or narrow floor than that and less of a big open one, so:

1. ``fit_to_floor`` lays the selection out. While units are left out it re-plans on less area,
   halfway between the area the layout placed and the area it was asked to place, and keeps
   the most valuable plan that fits.
2. It then grows that plan with what the budget still buys, best value per dollar first and
   several moves per layout. The layout keeps the most valuable units that fit, and a type it
   leaves out is not offered again: it did not fit beside more valuable units, which stay.
   When the layout makes room for an offer by leaving out the plan's own units, the offer
   shrinks, down to one move.
3. ``upgrades`` lists what a bigger budget would add next on the same floor, each step checked
   the same way, so the list holds only what the layout places. Steps the money left already
   buys are bought (``bought_upgrades``).

Units used mostly with a wall run (benches with dumbbells, ``wall_partners``) are laid out
facing it.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, replace
from functools import cached_property

import numpy as np
from numpy.typing import NDArray

from gymplanner.catalog.loader import Catalog
from gymplanner.catalog.schema import Equipment
from gymplanner.domain import Room
from gymplanner.layout import LayoutItem, LayoutResult, LayoutRules, plan_layout
from gymplanner.selection import Constraints, RouteTable, Selection, greedy, improve
from gymplanner.selection.evaluator import evaluate
from gymplanner.selection.explain import TypeUsage, type_usage
from gymplanner.selection.optimizer import Addition, additions

MAX_FIT_ATTEMPTS = 5
FIT_LOSS_ACCEPTED = 0.005
"""A layout that keeps all but this share of the plan's value ends the re-planning; another
attempt costs a full layout pass and, measured on sample plans, gains less than this."""
SHRINK_AT_LEAST = 0.97
"""Each re-plan has at most this share of the area the attempt before it had."""
GROW_LAYOUTS = 12
"""Layouts the grow step may try (each takes up to about a tenth of a second on the largest
floors). Sample plans rarely need more than three; a crowded floor, where each offer can push
out the plan's own units and the offers shrink to one piece, can need all of them."""
GROW_MOVES = 6
"""Moves offered to one layout: the layout keeps the most valuable of them that fit."""
MAX_UPGRADES = 6
UPGRADE_LAYOUTS = 8
"""Layouts the upgrade list may try when its steps do not all fit at once."""
SMALL_PLAN_UNITS = 40
UPGRADE_LAYOUTS_SMALL = 30
"""Layouts it may try for a plan of at most ``SMALL_PLAN_UNITS`` units: there each takes a few
milliseconds, and on a cramped floor the best buys per dollar are often the ones without room."""
UPGRADE_BUDGET_FACTOR = 1.6
PARTNER_SHARE = 0.5
"""A unit stands facing a wall run when at least this share of its use is with that run."""


@dataclass(frozen=True)
class Floor:
    """What laying out a selection needs."""

    catalog: Catalog
    room: Room
    table: RouteTable
    rules: LayoutRules

    @cached_property
    def partners(self) -> dict[str, str]:
        return wall_partners(self.catalog, self.table)

    def lay_out(self, selection: Selection) -> LayoutResult:
        usage = type_usage(self.catalog, self.table, selection.units, selection.evaluation)
        items = layout_items(self.catalog, self.table, selection.units, usage, self.partners)
        return plan_layout(self.room, items, self.rules)


@dataclass(frozen=True)
class Fitted:
    selection: Selection
    layout: LayoutResult
    """The selection laid out, every unit placed."""
    constraints: Constraints
    """The constraints the plan was made under: area as the last re-plan left it, but never
    less than the plan's own."""
    blocked: frozenset[int]
    """Types the grow step offered that found no room beside the plan."""
    warnings: list[str]


@dataclass(frozen=True)
class Upgrade:
    added: dict[int, int]
    cost: float
    gain: float
    """Objective gained (Erlangs) on top of the plan and the upgrades before it."""


def layout_rules(catalog: Catalog) -> LayoutRules:
    zones = sorted(catalog.space.zones, key=lambda z: z.order)
    return LayoutRules(
        main_aisle_in=catalog.space.aisles.main_aisle_in,
        secondary_aisle_in=catalog.space.aisles.secondary_aisle_in,
        zone_order=tuple(z.id for z in zones),
    )


def wall_partners(catalog: Catalog, table: RouteTable) -> dict[str, str]:
    """Types used mostly together with wall units of their own zone (a bench with dumbbells:
    at least ``PARTNER_SHARE`` of the demand its routes serve), with those units' row group.
    The layout stands them facing that run."""
    total: dict[str, float] = defaultdict(float)
    paired: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for e, load in enumerate(table.load):
        for k, quality in enumerate(table.route_quality[e]):
            types = [
                catalog.equipment_by_id[table.equipment_ids[r]]
                for r in table.route_res[e, k]
                if r >= 0
            ]
            for item in types:
                total[item.id] += float(load * quality)
                for wall in types:
                    if (
                        wall.layout.against_wall
                        and not item.layout.against_wall
                        and wall.zone == item.zone
                    ):
                        paired[item.id][wall.layout.row_group or wall.id] += float(load * quality)
    partners: dict[str, str] = {}
    for eid, groups in paired.items():
        group, weight = max(groups.items(), key=lambda kv: kv[1])
        if weight >= PARTNER_SHARE * total[eid]:
            partners[eid] = group
    return partners


def layout_item(
    equipment: Equipment, uid: str, priority: float, pairs_with: str = ""
) -> LayoutItem:
    return LayoutItem(
        uid=uid,
        equipment_id=equipment.id,
        name=equipment.name,
        zone=equipment.zone,
        length_in=equipment.footprint.length_in,
        width_in=equipment.footprint.width_in,
        clearance=equipment.clearance,
        aisle_side=equipment.layout.aisle_side,
        against_wall=equipment.layout.against_wall,
        row_group=equipment.layout.row_group or equipment.id,
        flexible_length=equipment.layout.flexible_length,
        min_length_in=equipment.layout.min_length_in,
        priority=priority,
        pairs_with=pairs_with,
    )


def layout_items(
    catalog: Catalog,
    table: RouteTable,
    units: NDArray[np.int64],
    usage: dict[str, TypeUsage],
    partners: Mapping[str, str] | None = None,
) -> list[LayoutItem]:
    """One layout item per unit; ``partners`` (``wall_partners``) keeps benches by their
    dumbbells."""
    items: list[LayoutItem] = []
    for r in np.flatnonzero(units):
        eid = table.equipment_ids[int(r)]
        priority = usage[eid].last_unit_value if eid in usage else 0.0
        pairs = (partners or {}).get(eid, "")
        items += [ # Later units of a type matter less than the first one.
            layout_item(catalog.equipment_by_id[eid], f"{eid}-{k + 1}", priority / (k + 1), pairs)
            for k in range(int(units[r]))
        ]
    return items


def placed_units(table: RouteTable, cons: Constraints, layout: LayoutResult) -> NDArray[np.int64]:
    """Units the layout placed, less any whose prerequisite was left out."""
    placed = Counter(p.item.equipment_id for p in layout.placements)
    units = np.array([placed.get(eid, 0) for eid in table.equipment_ids], dtype=np.int64)
    for r in range(len(units)):
        if units[r] and any(units[p] == 0 for p in cons.requires[r]):
            units[r] = 0
    return units


def selection_of(table: RouteTable, cons: Constraints, units: NDArray[np.int64]) -> Selection:
    return Selection(
        units=units,
        evaluation=evaluate(table, units),
        cost=float(units @ cons.unit_cost),
        area=float(units @ cons.unit_area),
    )


def _laid_out_exactly(layout: LayoutResult, table: RouteTable, units: NDArray[np.int64]) -> bool:
    placed = Counter(p.item.equipment_id for p in layout.placements)
    return all(placed.get(eid, 0) == int(n) for eid, n in zip(table.equipment_ids, units, strict=True))


def fit_to_floor(floor: Floor, cons: Constraints, selection: Selection) -> Fitted:
    """The most valuable plan found that the layout places in full (see the module docstring)."""
    table = floor.table
    best: tuple[Selection, LayoutResult | None] | None = None
    for attempt in range(MAX_FIT_ATTEMPTS):
        layout = floor.lay_out(selection)
        if not layout.unplaced:
            if best is None or selection.value >= best[0].value:
                best = (selection, layout)
            break
        placed = placed_units(table, cons, layout)
        if cons.min_units is not None:
            cons = replace(cons, min_units=np.minimum(cons.min_units, placed)) # A unit held in the plan that the layout could not place is held no longer.
        fitted = selection_of(table, cons, placed)
        if best is None or fitted.value > best[0].value:
            kept = layout if _laid_out_exactly(layout, table, placed) else None
            best = (fitted, None if kept is None else replace(kept, unplaced=[]))
        if attempt == MAX_FIT_ATTEMPTS - 1 or fitted.value >= selection.value * (
            1 - FIT_LOSS_ACCEPTED
        ):
            break
        area = min((fitted.area + selection.area) / 2, cons.area_sqin * SHRINK_AT_LEAST) # The floor holds somewhere between what was placed and what was asked for.
        if area <= fitted.area:
            break
        cons = replace(cons, area_sqin=area)
        selection = improve(table, cons, greedy(table, cons, start=placed, record_steps=False))

    assert best is not None
    selection, final_layout = best
    cons = replace(cons, area_sqin=max(cons.area_sqin, selection.area)) # The kept plan may come from an attempt with more area than the last one.
    warnings: list[str] = []
    if final_layout is None:
        final_layout = floor.lay_out(selection)
        if final_layout.unplaced:
            dropped = Counter(item.name for item in final_layout.unplaced)
            warnings.append(
                "Left out because no clear floor space remained: "
                + ", ".join(f"{n} x{c}" if c > 1 else n for n, c in dropped.items())
                + "."
            )
            selection = selection_of(table, cons, placed_units(table, cons, final_layout))
            final_layout = replace(final_layout, unplaced=[])
    if cons.min_units is not None:
        cons = replace(cons, min_units=np.minimum(cons.min_units, selection.units)) # A held unit the final layout left out is held no longer.
    selection, final_layout, blocked = _grow(floor, cons, selection, final_layout)
    cons = replace(cons, area_sqin=max(cons.area_sqin, selection.area))
    return Fitted(selection, final_layout, cons, blocked, warnings)


def _offer(
    candidates: list[Addition],
    blocked: set[int],
    failed: set[frozenset[tuple[int, int]]],
    budget_left: float,
    limit: int,
) -> list[Addition]:
    """The best candidates that the money left buys together, one move per type, leaving out
    blocked types and moves that failed on their own."""
    offer: list[Addition] = []
    spent, taken = 0.0, set[int]()
    for move in candidates:
        if len(offer) == limit:
            break
        if taken.intersection(move.added) or blocked.intersection(move.added):
            continue
        if frozenset(move.added.items()) in failed or spent + move.cost > budget_left + 1e-6:
            continue
        offer.append(move)
        spent += move.cost
        taken.update(move.added)
    return offer


def _grow(
    floor: Floor, cons: Constraints, selection: Selection, layout: LayoutResult
) -> tuple[Selection, LayoutResult, frozenset[int]]:
    """Add what the budget still buys while the layout places it (step 2 of the module
    docstring).

    When the layout makes room for an offer by leaving out the plan's own units, which it does
    when the offered ones matter more, the next offer is half the size, down to one move; one
    move that does not fit on its own is not offered again, as in ``_upgrades_one_by_one``."""
    table = floor.table
    blocked: set[int] = set()
    failed: set[frozenset[tuple[int, int]]] = set()
    size = GROW_MOVES
    for _ in range(GROW_LAYOUTS):
        candidates = additions(table, cons, selection)
        offer = _offer(candidates, blocked, failed, cons.budget_usd - selection.cost, size)
        if not offer:
            break
        units = _plus(selection.units, [move.added for move in offer])
        trial = selection_of(table, cons, units)
        trial_layout = floor.lay_out(trial)
        if not trial_layout.unplaced:
            selection, layout = trial, trial_layout
            continue
        placed = placed_units(table, cons, trial_layout)
        blocked.update(r for move in offer for r in move.added if placed[r] < units[r])
        if len(offer) == 1:
            if len(offer[0].added) == 1:
                blocked.update(offer[0].added) # one more of it does not fit, so more never will
            else:
                failed.add(frozenset(offer[0].added.items()))
        kept = _kept_layout(floor, cons, selection, trial_layout, placed)
        if kept is not None:
            selection, layout = kept
            continue
        size = max(1, len(offer) // 2)
    return selection, layout, frozenset(blocked)


def _kept_layout(
    floor: Floor,
    cons: Constraints,
    selection: Selection,
    layout: LayoutResult,
    placed: NDArray[np.int64],
) -> tuple[Selection, LayoutResult] | None:
    """What a layout that left units out placed, when that is worth more than ``selection`` and
    keeps every unit the constraints hold; laid out again if the placements were not exact."""
    if cons.min_units is not None and (placed < cons.min_units).any():
        return None
    fitted = selection_of(floor.table, cons, placed)
    if fitted.value <= selection.value * (1 + 1e-9):
        return None
    if _laid_out_exactly(layout, floor.table, placed):
        return fitted, replace(layout, unplaced=[])
    relaid = floor.lay_out(fitted)
    return None if relaid.unplaced else (fitted, relaid)


def upgrades(floor: Floor, fitted: Fitted) -> list[Upgrade]:
    """What a bigger budget would add next on the same floor, in order, each step one the layout
    places beside the plan and the steps before it.

    Most often the greedy's next moves under a larger budget (``UPGRADE_BUDGET_FACTOR`` times
    the equipment budget, and never less than the ``MAX_UPGRADES`` cheapest pieces worth adding
    cost) all fit, one layout per step settling it (the layout does not always place a subset of
    what it places together). Otherwise the best move per dollar is offered to the layout one at
    a time, the next one chosen with the steps kept so far in the plan: a piece that did not fit
    is not offered again, nor is a pair that did not fit together."""
    table, cons, selection = floor.table, fitted.constraints, fitted.selection
    if not selection.units.any():
        return []
    worth = [
        m
        for m in additions(table, cons, selection, np.inf)
        if not fitted.blocked.intersection(m.added)
    ]
    if not worth:
        return []
    cheapest = sorted(m.cost for m in worth)[:MAX_UPGRADES]
    budget = max(UPGRADE_BUDGET_FACTOR * cons.budget_usd, selection.cost + sum(cheapest))
    caps = cons.max_units.copy()
    for r in fitted.blocked:
        caps[r] = selection.units[r] # no room for another
    roomy = replace(cons, budget_usd=budget, area_sqin=np.inf, max_units=caps)
    greedy_steps = greedy(table, roomy, start=selection.units, max_steps=MAX_UPGRADES).steps
    steps = [dict(step.added) for step in greedy_steps[:MAX_UPGRADES]]
    prefixes = (_plus(selection.units, steps[: k + 1]) for k in range(len(steps)))
    if steps and all(not floor.lay_out(selection_of(table, cons, units)).unplaced for units in prefixes):
        kept = steps
    else:
        kept = _upgrades_one_by_one(floor, cons, selection, fitted.blocked)
    if not kept:
        return []
    running = np.array([_plus(selection.units, kept[: k + 1]) for k in range(len(kept))]) # Gains as kept, each on top of the plan and the steps before it.
    values = evaluate(table, running).value
    gains = np.diff(np.concatenate([[selection.value], values]))
    return [
        Upgrade(added=added, cost=float(sum(cons.unit_cost[r] * n for r, n in added.items())), gain=float(gain))
        for added, gain in zip(kept, gains, strict=True)
    ]


def bought_upgrades(floor: Floor, fitted: Fitted, steps: list[Upgrade]) -> Fitted | None:
    """``fitted`` with the first upgrade steps that the money left already buys and that the
    greedy would buy on the plan as it stands; None when there are none.

    The grow step tries a limited number of layouts, and on a crowded floor each piece it offers
    can push out others, so it can stop short of a piece that fits. Every step was laid out
    beside the plan and the steps before it, so the layout places these."""
    table, cons = floor.table, fitted.constraints
    left = cons.budget_usd - fitted.selection.cost
    taken: list[dict[int, int]] = []
    for step in steps:
        if step.cost > left + 1e-6:
            break
        current = selection_of(table, cons, _plus(fitted.selection.units, taken))
        if not any(move.added == step.added for move in additions(table, cons, current)):
            break
        taken.append(step.added)
        left -= step.cost
    if not taken:
        return None
    grown = selection_of(table, cons, _plus(fitted.selection.units, taken))
    layout = floor.lay_out(grown)
    if layout.unplaced:
        return None
    area = replace(cons, area_sqin=max(cons.area_sqin, grown.area))
    return replace(fitted, selection=grown, layout=layout, constraints=area)


def _upgrades_one_by_one(
    floor: Floor, cons: Constraints, selection: Selection, blocked: frozenset[int]
) -> list[dict[int, int]]:
    table = floor.table
    kept: list[dict[int, int]] = []
    current = selection
    no_room = set(blocked)
    failed: set[frozenset[tuple[int, int]]] = set()
    small = selection.units.sum() <= SMALL_PLAN_UNITS
    for _ in range(UPGRADE_LAYOUTS_SMALL if small else UPGRADE_LAYOUTS):
        if len(kept) == MAX_UPGRADES:
            break
        offer = next(
            (
                move.added
                for move in additions(table, cons, current, np.inf)
                if not no_room.intersection(move.added)
                and frozenset(move.added.items()) not in failed
            ),
            None,
        )
        if offer is None:
            break
        units = _plus(current.units, [offer])
        if floor.lay_out(selection_of(table, cons, units)).unplaced:
            if len(offer) == 1:
                no_room.update(offer) # one more of it does not fit, so more never will
            else:
                failed.add(frozenset(offer.items()))
            continue
        kept.append(dict(offer))
        current = selection_of(table, cons, units)
    return kept


def _plus(units: NDArray[np.int64], added: list[dict[int, int]]) -> NDArray[np.int64]:
    out = units.copy()
    for step in added:
        for r, n in step.items():
            out[r] += n
    return out
