"""Small and narrow floors on the real datasets: plans hold what fits, and say truthfully why
they stop.

These floors are where the optimizer's estimate of space is furthest from what the layout can
place: aisles take most of a 150-300 sq ft room, and a floor 10 ft wide leaves one row beside
its main aisle.
"""

from __future__ import annotations

from dataclasses import replace
from functools import cache

import numpy as np
import pytest

from gymplanner.api.schemas import PlanRequest, PlanResponse
from gymplanner.catalog import Catalog, load_catalog
from gymplanner.layout import plan_layout
from gymplanner.planning import create_plan
from gymplanner.planning.fitting import layout_items, layout_rules, selection_of
from gymplanner.planning.service import build_problem
from gymplanner.selection.evaluator import evaluate
from gymplanner.selection.explain import type_usage
from gymplanner.selection.optimizer import additions
from gymplanner.settings import get_settings

SMALL = [
    {"area_sqft": 150, "budget_usd": 5_000},
    {"area_sqft": 150, "budget_usd": 15_000, "profile": "amenity"},
    {"area_sqft": 150, "budget_usd": 5_000, "entrance": "left"},
    {"area_sqft": 200, "budget_usd": 15_000},
    {"area_sqft": 250, "budget_usd": 20_000},
    {"area_sqft": 300, "budget_usd": 5_000},
    {"area_sqft": 250, "budget_usd": 2_000, "profile": "amenity"},
    {"area_sqft": 1_000, "budget_usd": 40_000, "width_ft": 10, "depth_ft": 100},
]


@cache
def catalog() -> Catalog:
    return load_catalog(get_settings().data_dir)


@cache
def planned(key: str) -> PlanResponse:
    return create_plan(PlanRequest(**eval(key)), catalog(), seed=1)


def keys() -> list[str]:
    return [repr(request) for request in SMALL]


@pytest.mark.parametrize("key", keys())
def test_small_floors_get_a_plan_that_holds_what_fits(key: str) -> None:
    plan = planned(key)
    request = PlanRequest(**eval(key))
    problem = build_problem(request, catalog())
    table, cons, room = problem.table, problem.constraints, problem.room
    assert plan.metrics.unit_count > 0
    assert len(plan.layout.placements) == plan.metrics.unit_count
    assert not any(w.startswith("Left out") for w in plan.warnings)

    units = np.zeros(table.n_equipment, dtype=np.int64)
    for item in plan.items:
        units[table.index_of(item.equipment_id)] = item.units
    selection = selection_of(table, cons, units)
    rules = layout_rules(catalog())

    def fits(more: np.ndarray) -> bool:
        trial = selection_of(table, cons, more)
        usage = type_usage(catalog(), table, more, trial.evaluation)
        return not plan_layout(room, layout_items(catalog(), table, more, usage), rules).unplaced

    best_single = 0.0 # At least as good as the best single piece the budget buys and the floor holds.
    for r in range(table.n_equipment):
        if cons.requires[r] or cons.unit_cost[r] > cons.budget_usd:
            continue
        one = np.zeros_like(units)
        one[r] = 1
        if fits(one):
            best_single = max(best_single, float(evaluate(table, one).value[0]))
    assert selection.value >= best_single * (1 - 1e-6)

    left = cons.budget_usd - selection.cost # Nothing affordable and worth buying would still fit beside the plan.
    roomy = replace(cons, area_sqin=np.inf)
    for move in additions(table, roomy, selection):
        if move.cost <= left + 1e-6:
            more = units.copy()
            for r, n in move.added.items():
                more[r] += n
            assert not fits(more), {table.equipment_ids[r]: n for r, n in move.added.items()}


@pytest.mark.parametrize("key", keys())
def test_small_floors_never_claim_demand_is_met_when_it_is_not(key: str) -> None:
    plan = planned(key)
    text = " ".join([plan.upgrade_note, *plan.warnings])
    if plan.metrics.served_share < 0.9:
        assert "demand is already met" not in text
        assert "already serves" not in text


def test_a_ten_foot_floor_with_the_door_in_the_middle_is_not_empty() -> None:
    plan = planned(repr(SMALL[1])) # 150 sq ft with no sides given is 10 x 15 ft, the door in the middle of the short wall.
    assert plan.inputs.width_ft == pytest.approx(10)
    assert plan.metrics.unit_count >= 1
    deep = planned(repr(SMALL[-1]))
    assert deep.metrics.unit_count >= 8


@pytest.mark.parametrize("profile", ["amenity", "strength"])
def test_a_budget_too_small_for_the_next_piece_still_shows_what_it_would_buy(profile: str) -> None:
    plan = planned(repr({"area_sqft": 250, "budget_usd": 2_000, "profile": profile})) # At $2,000, useful upgrades exceed the remaining budget; strength upgrades also need room for dumbbells and a bench together.
    assert plan.next_upgrades
    assert plan.upgrade_note.startswith("What a bigger budget would add next")
    first = plan.next_upgrades[0]
    assert first.cost_usd > plan.costs.remaining_usd
    unallocated = [w for w in plan.warnings if "unallocated" in w]
    if plan.costs.remaining_usd > 0.15 * plan.costs.budget_usd: # when the plan says so at all
        (warning,) = unallocated
        assert "the next piece worth adding" in warning
        assert f"${first.cost_usd:,.0f}" in warning
