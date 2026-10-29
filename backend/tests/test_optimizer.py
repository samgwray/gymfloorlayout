"""Greedy knapsack and swap search over a synthetic but realistic gym.

The fixture gym has 26 equipment types and 40 exercises with first-choice and substitute
routes, two-type routes (bench + dumbbells, rack + bench), prerequisites (racks need a barbell
set) and unit caps. Prices and envelope areas are typical commercial figures.
"""

from __future__ import annotations

import time
from collections.abc import Sequence
from dataclasses import replace
from functools import cache
from itertools import pairwise
from typing import NamedTuple

import numpy as np
import pytest

from gymplanner.domain import SQIN_PER_SQFT
from gymplanner.queueing import servers_for_blocking
from gymplanner.selection.evaluator import RouteTable, evaluate
from gymplanner.selection.optimizer import (
    COVERAGE_MIN_SHARE,
    COVERAGE_TOLERANCE,
    MIN_GAIN_FRACTION,
    MIN_RELATIVE_RETURN,
    MIN_UNIT_USE,
    MOST_WANTED_BLOCKING,
    MOST_WANTED_TOLERANCE,
    RETURN_BASIS_SHARE,
    UNCAPPED,
    Constraints,
    Selection,
    coverage_moves,
    greedy,
    held_addition,
    improve,
    most_wanted,
    most_wanted_holds,
    optimize,
    plan_worth,
    serves_within_tolerance,
    unlimited_plan,
    with_most_wanted,
)

Route = tuple[float, Sequence[str]]
ExerciseSpec = tuple[str, float, Sequence[Route]]

GREEDY_SECONDS = 10.0
"""Wall-clock guard for the 60-type table; it runs in about 1.5 s on a laptop."""


def make_table(
    equipment: Sequence[tuple[str, int]],
    exercises: Sequence[ExerciseSpec],
    unroutable_load: float = 0.0,
) -> RouteTable:
    """RouteTable from (id, stations) and (id, load, routes); route 0 is the first choice."""
    index = {eid: i for i, (eid, _) in enumerate(equipment)}
    n_routes = max((len(routes) for _, _, routes in exercises), default=1)
    n_slots = max((len(uses) for _, _, routes in exercises for _, uses in routes), default=1)
    route_res = np.full((len(exercises), n_routes, n_slots), -1, dtype=np.int64)
    route_quality = np.zeros((len(exercises), n_routes))
    incidence = np.zeros((n_routes, n_slots, len(exercises), len(equipment)))
    for e, (_, _, routes) in enumerate(exercises):
        for k, (quality, uses) in enumerate(routes):
            route_quality[e, k] = quality
            for u, eid in enumerate(uses):
                route_res[e, k, u] = index[eid]
                incidence[k, u, e, index[eid]] = 1.0
    return RouteTable(
        equipment_ids=tuple(eid for eid, _ in equipment),
        stations=np.array([stations for _, stations in equipment], dtype=np.int64),
        exercise_ids=tuple(xid for xid, _, _ in exercises),
        load=np.array([load for _, load, _ in exercises], dtype=np.float64),
        route_res=route_res,
        route_quality=route_quality,
        incidence=incidence,
        unroutable_load=unroutable_load,
    )


def simple_constraints(
    n_types: int,
    unit_cost: Sequence[float],
    budget_usd: float = 1e9,
    max_units: Sequence[int] | None = None,
    requires: tuple[tuple[int, ...], ...] | None = None,
) -> Constraints:
    """Constraints where space never binds; for tables built to probe one mechanism."""
    return Constraints(
        budget_usd=budget_usd,
        area_sqin=1e12,
        unit_cost=np.asarray(unit_cost, dtype=np.float64),
        unit_area=np.ones(n_types),
        max_units=np.asarray(max_units or [UNCAPPED] * n_types, dtype=np.int64),
        requires=requires or ((),) * n_types,
    )


class Kind(NamedTuple):
    id: str
    stations: int
    cost_usd: float
    sqft: float
    """Effective envelope area claimed on a packed floor."""
    max_units: int | None = None
    requires: tuple[str, ...] = ()


GYM_TYPES = (
    Kind("treadmill", 1, 9_000, 40),
    Kind("elliptical", 1, 6_000, 30),
    Kind("upright_bike", 1, 3_500, 18),
    Kind("rower", 1, 1_200, 30),
    Kind("stair_climber", 1, 7_000, 22),
    Kind("air_bike", 1, 1_100, 18),
    Kind("barbell_set", 1, 900, 8),
    Kind("power_rack", 1, 3_500, 70, requires=("barbell_set",)),
    Kind("bench_press_station", 1, 1_800, 45, requires=("barbell_set",)),
    Kind("dumbbells", 6, 6_000, 50, max_units=3),
    Kind("adjustable_bench", 1, 600, 25),
    Kind("flat_bench", 1, 350, 22),
    Kind("cable_crossover", 2, 6_500, 60),
    Kind("functional_trainer", 2, 4_500, 45),
    Kind("lat_pulldown", 1, 4_000, 30),
    Kind("seated_row", 1, 4_000, 35),
    Kind("leg_press", 1, 5_500, 50),
    Kind("leg_extension", 1, 4_200, 30),
    Kind("leg_curl", 1, 4_200, 30),
    Kind("chest_press", 1, 4_500, 30),
    Kind("shoulder_press", 1, 4_500, 30),
    Kind("smith_machine", 1, 4_000, 50),
    Kind("kettlebells", 6, 1_500, 20, max_units=2),
    Kind("turf_lane", 1, 3_500, 150, max_units=2),
    Kind("mat_area", 4, 400, 60),
    Kind("pullup_dip", 1, 900, 30),
)

GYM_EXERCISES: tuple[ExerciseSpec, ...] = ( # (exercise, share of active floor time, routes from first choice to last resort)
    ("treadmill_run", 0.12, [(1.0, ["treadmill"]), (0.6, ["elliptical"]), (0.4, ["upright_bike"])]),
    ("elliptical", 0.06, [(1.0, ["elliptical"]), (0.6, ["treadmill"]), (0.5, ["stair_climber"])]),
    ("cycling", 0.06, [(1.0, ["upright_bike"]), (0.7, ["air_bike"])]),
    ("rowing", 0.03, [(1.0, ["rower"]), (0.4, ["air_bike"])]),
    ("stairs", 0.04, [(1.0, ["stair_climber"]), (0.6, ["treadmill"])]),
    ("intervals", 0.02, [(1.0, ["air_bike"]), (0.8, ["rower"]), (0.6, ["upright_bike"])]),
    ("incline_walk", 0.02, [(1.0, ["treadmill"]), (0.7, ["stair_climber"])]),
    ("back_squat", 0.04, [(1.0, ["power_rack"]), (0.7, ["smith_machine"]), (0.5, ["leg_press"])]),
    (
        "bench_press",
        0.035,
        [
            (1.0, ["bench_press_station"]),
            (0.95, ["power_rack", "flat_bench"]),
            (0.7, ["smith_machine", "flat_bench"]),
            (0.5, ["chest_press"]),
        ],
    ),
    ("deadlift", 0.025, [(1.0, ["power_rack"]), (0.9, ["barbell_set"])]),
    ("overhead_press", 0.015, [(1.0, ["power_rack"]), (0.7, ["smith_machine"]), (0.5, ["shoulder_press"])]),
    ("barbell_row", 0.01, [(1.0, ["barbell_set"]), (0.6, ["seated_row"])]),
    ("hip_thrust", 0.015, [(1.0, ["flat_bench", "barbell_set"]), (0.7, ["smith_machine", "flat_bench"])]),
    ("barbell_curl", 0.01, [(1.0, ["barbell_set"]), (0.8, ["dumbbells"]), (0.6, ["cable_crossover"])]),
    (
        "db_bench_press",
        0.03,
        [(1.0, ["adjustable_bench", "dumbbells"]), (0.95, ["flat_bench", "dumbbells"]), (0.5, ["chest_press"])],
    ),
    ("db_shoulder_press", 0.02, [(1.0, ["adjustable_bench", "dumbbells"]), (0.6, ["shoulder_press"])]),
    (
        "db_row",
        0.015,
        [(1.0, ["flat_bench", "dumbbells"]), (1.0, ["adjustable_bench", "dumbbells"]), (0.6, ["seated_row"])],
    ),
    ("db_lunge", 0.015, [(1.0, ["dumbbells"]), (0.5, ["smith_machine"])]),
    ("db_curl", 0.02, [(1.0, ["dumbbells"]), (0.8, ["cable_crossover"])]),
    ("lateral_raise", 0.015, [(1.0, ["dumbbells"]), (0.9, ["cable_crossover"])]),
    ("goblet_squat", 0.01, [(1.0, ["dumbbells"]), (1.0, ["kettlebells"])]),
    ("incline_db_press", 0.015, [(1.0, ["adjustable_bench", "dumbbells"]), (0.4, ["chest_press"])]),
    ("leg_press", 0.03, [(1.0, ["leg_press"]), (0.5, ["smith_machine"])]),
    ("leg_extension", 0.02, [(1.0, ["leg_extension"]), (0.4, ["cable_crossover"])]),
    ("leg_curl", 0.02, [(1.0, ["leg_curl"]), (0.4, ["cable_crossover"])]),
    (
        "machine_chest_press",
        0.02,
        [(1.0, ["chest_press"]), (0.7, ["adjustable_bench", "dumbbells"]), (0.6, ["bench_press_station"])],
    ),
    ("machine_shoulder_press", 0.015, [(1.0, ["shoulder_press"]), (0.7, ["adjustable_bench", "dumbbells"])]),
    ("lat_pulldown", 0.025, [(1.0, ["lat_pulldown"]), (0.7, ["cable_crossover"]), (0.6, ["pullup_dip"])]),
    ("seated_row", 0.02, [(1.0, ["seated_row"]), (0.8, ["cable_crossover"]), (0.8, ["functional_trainer"])]),
    (
        "cable_fly",
        0.02,
        [(1.0, ["cable_crossover"]), (0.9, ["functional_trainer"]), (0.6, ["adjustable_bench", "dumbbells"])],
    ),
    ("triceps_pushdown", 0.025, [(1.0, ["cable_crossover"]), (1.0, ["functional_trainer"]), (0.6, ["lat_pulldown"])]),
    ("face_pull", 0.015, [(1.0, ["cable_crossover"]), (1.0, ["functional_trainer"])]),
    ("cable_crunch", 0.02, [(1.0, ["cable_crossover"]), (1.0, ["functional_trainer"]), (0.6, ["mat_area"])]),
    ("kb_swing", 0.02, [(1.0, ["kettlebells"]), (0.7, ["dumbbells"])]),
    ("sled_push", 0.025, [(1.0, ["turf_lane"])]),
    ("pullups", 0.015, [(1.0, ["pullup_dip"]), (0.6, ["lat_pulldown"])]),
    ("dips", 0.01, [(1.0, ["pullup_dip"]), (0.5, ["flat_bench"])]),
    ("planks", 0.015, [(1.0, ["mat_area"])]),
    ("stretching", 0.02, [(1.0, ["mat_area"])]),
    ("foam_rolling", 0.01, [(1.0, ["mat_area"])]),
)


def gym_table(active_users: float) -> RouteTable:
    """The synthetic gym with ``active_users`` Erlangs split across exercises by time share."""
    total = sum(share for _, share, _ in GYM_EXERCISES)
    return make_table(
        [(kind.id, kind.stations) for kind in GYM_TYPES],
        [(xid, active_users * share / total, routes) for xid, share, routes in GYM_EXERCISES],
    )


def gym_constraints(table: RouteTable, budget_usd: float, area_sqft: float) -> Constraints:
    index = {eid: i for i, eid in enumerate(table.equipment_ids)}
    return Constraints(
        budget_usd=budget_usd,
        area_sqin=area_sqft * SQIN_PER_SQFT,
        unit_cost=np.array([kind.cost_usd for kind in GYM_TYPES], dtype=np.float64),
        unit_area=np.array([kind.sqft * SQIN_PER_SQFT for kind in GYM_TYPES]),
        max_units=np.array([kind.max_units or UNCAPPED for kind in GYM_TYPES], dtype=np.int64),
        requires=tuple(tuple(index[req] for req in kind.requires) for kind in GYM_TYPES),
    )


@cache
def solved(
    users: float, budget_usd: float, area_sqft: float
) -> tuple[RouteTable, Constraints, Selection, Selection]:
    """(table, constraints, greedy pass, greedy + swap search), shared across tests."""
    table = gym_table(users)
    cons = gym_constraints(table, budget_usd, area_sqft)
    first = greedy(table, cons)
    return table, cons, first, improve(table, cons, first)


def types_and_units(selection: Selection) -> tuple[int, int]:
    return int(np.count_nonzero(selection.units)), int(selection.units.sum())


def assert_feasible(selection: Selection, cons: Constraints) -> None:
    units = selection.units
    assert np.all(units >= 0)
    assert selection.cost == pytest.approx(float(units @ cons.unit_cost), rel=1e-9, abs=1e-6)
    assert selection.area == pytest.approx(float(units @ cons.unit_area), rel=1e-9, abs=1e-6)
    assert selection.cost <= cons.budget_usd + 1e-3
    assert selection.area <= cons.area_sqin + 1e-3
    assert np.all(units <= cons.max_units)
    for r in np.flatnonzero(units):
        missing = [p for p in cons.requires[int(r)] if units[p] == 0]
        assert not missing, f"type {r} bought without its prerequisites {missing}"
    if cons.min_units is not None:
        assert np.all(units >= cons.min_units)


def worthwhile_additions(
    table: RouteTable, cons: Constraints, selection: Selection, slack: float = 2.0
) -> dict[str, float]:
    """Affordable one-unit additions (with prerequisites) that clear greedy's stopping rules.

    The rules are applied with ``slack`` so only clearly worthwhile misses are reported: the
    floors on gain (a share of demand, and use for the unit bought) and the minimum return
    relative to the plan's average per dollar (taken over at least part of the budget).
    """
    floor = slack * max(MIN_GAIN_FRACTION * table.total_load, MIN_UNIT_USE)
    basis = max(selection.cost, RETURN_BASIS_SHARE * cons.budget_usd)
    units = selection.units
    candidates: list[tuple[str, np.ndarray]] = []
    for r in range(table.n_equipment):
        delta, pending = {r: 1}, [r]
        while pending:
            for prereq in cons.requires[pending.pop()]:
                if units[prereq] == 0 and prereq not in delta:
                    delta[prereq] = 1
                    pending.append(prereq)
        plus = units.copy()
        for k, n in delta.items():
            plus[k] += n
        added = plus - units
        if np.any(plus > cons.max_units):
            continue
        if added @ cons.unit_cost > cons.budget_usd - selection.cost + 1e-6:
            continue
        if added @ cons.unit_area > cons.area_sqin - selection.area + 1e-6:
            continue
        candidates.append((table.equipment_ids[r], plus))
    if not candidates:
        return {}
    gains = evaluate(table, np.array([plus for _, plus in candidates])).value - selection.value
    costs = [float((plus - units) @ cons.unit_cost) for _, plus in candidates]
    return {
        eid: float(g)
        for (eid, _), g, cost in zip(candidates, gains, costs, strict=True)
        if g > floor and g * basis >= slack * MIN_RELATIVE_RETURN * selection.value * cost
    }


SCENARIOS = [ # (active users, budget, floor area): budget-bound, area-bound, mid-size, large, area-bound despite a huge budget, budget below most prices, and demand-saturated (neither binds).
    (3.0, 25_000.0, 800.0),
    (6.0, 60_000.0, 400.0),
    (15.0, 150_000.0, 3_000.0),
    (40.0, 400_000.0, 8_000.0),
    (12.0, 2_000_000.0, 2_500.0),
    (2.0, 900.0, 5_000.0),
    (4.0, 2_000_000.0, 50_000.0),
]


@pytest.mark.parametrize(("users", "budget_usd", "area_sqft"), SCENARIOS)
def test_selection_is_feasible(users: float, budget_usd: float, area_sqft: float) -> None:
    """Budget, space, unit caps and prerequisites hold after greedy and after the swap search."""
    _, cons, first, final = solved(users, budget_usd, area_sqft)
    assert_feasible(first, cons)
    assert_feasible(final, cons)


@pytest.mark.parametrize(("users", "budget_usd", "area_sqft"), SCENARIOS)
def test_improve_never_lowers_the_value(users: float, budget_usd: float, area_sqft: float) -> None:
    _, _, first, final = solved(users, budget_usd, area_sqft)
    assert final.value >= first.value


@pytest.mark.parametrize(("users", "budget_usd", "area_sqft"), SCENARIOS)
def test_nothing_affordable_and_worthwhile_is_left_out(
    users: float, budget_usd: float, area_sqft: float
) -> None:
    """Greedy stops only when no affordable addition would serve a meaningful share of demand."""
    table, cons, first, final = solved(users, budget_usd, area_sqft)
    assert worthwhile_additions(table, cons, first) == {}
    assert worthwhile_additions(table, cons, final) == {}


def test_prerequisite_is_bought_with_the_item_that_needs_it() -> None:
    """Plates serve no exercise on their own, so they only enter as a rack's prerequisite."""
    table = make_table([("plates", 1), ("rack", 1)], [("squat", 2.0, [(1.0, ["rack"])])])
    cons = simple_constraints(2, [300.0, 3_200.0], budget_usd=5_000.0, requires=((), (0,)))
    selection = optimize(table, cons)
    assert selection.units.tolist() == [1, 1]
    assert selection.steps[0].added == {0: 1, 1: 1}


def test_item_is_skipped_when_its_prerequisite_does_not_fit() -> None:
    table = make_table([("plates", 1), ("rack", 1)], [("squat", 2.0, [(1.0, ["rack"])])])
    cons = simple_constraints(2, [300.0, 3_200.0], budget_usd=3_400.0, requires=((), (0,)))
    assert optimize(table, cons).units.tolist() == [0, 0]


@pytest.mark.parametrize("cap", [1, 6, 11, 17])
def test_unit_cap_holds_even_when_a_coarse_step_would_overshoot(cap: int) -> None:
    """From six units a type grows by ~15% per step; near the cap it must fall back to one."""
    table = make_table([("treadmill", 1)], [("run", 50.0, [(1.0, ["treadmill"])])])
    cons = simple_constraints(1, [100.0], max_units=[cap])
    assert greedy(table, cons).units.tolist() == [cap]


def test_min_units_are_kept_through_the_swap_search() -> None:
    table = gym_table(15.0)
    floor = np.zeros(table.n_equipment, dtype=np.int64)
    floor[table.index_of("turf_lane")] = 2
    floor[table.index_of("kettlebells")] = 1
    cons = replace(gym_constraints(table, 150_000.0, 3_000.0), min_units=floor)
    selection = optimize(table, cons)
    assert_feasible(selection, cons)


@pytest.mark.parametrize(
    ("budget_usd", "area_sqft", "users"),
    [(0.0, 3_000.0, 15.0), (300.0, 3_000.0, 15.0), (150_000.0, 0.0, 15.0), (150_000.0, 3_000.0, 0.0)],
)
def test_nothing_is_bought_without_money_space_or_demand(
    budget_usd: float, area_sqft: float, users: float
) -> None:
    table = gym_table(users)
    selection = optimize(table, gym_constraints(table, budget_usd, area_sqft))
    assert selection.units.sum() == 0
    assert selection.cost == 0.0


@pytest.mark.parametrize(("users", "area_sqft"), [(4.0, 1_000.0), (15.0, 3_000.0)])
def test_value_does_not_fall_as_budget_grows(users: float, area_sqft: float) -> None:
    """Greedy is a heuristic, so allow a 0.5% dip below the best value at any smaller budget."""
    values = [solved(users, float(b), area_sqft)[3].value for b in np.geomspace(3e3, 3e5, 16)]
    best_so_far = np.maximum.accumulate(values)
    assert np.all(np.array(values) >= best_so_far * (1 - 5e-3))
    assert values[-1] > 3 * values[0]


def test_value_does_not_fall_as_floor_area_grows() -> None:
    values = [solved(15.0, 150_000.0, float(a))[3].value for a in np.geomspace(150, 6_000, 12)]
    best_so_far = np.maximum.accumulate(values)
    assert np.all(np.array(values) >= best_so_far * (1 - 5e-3))


def test_improve_repairs_a_poor_starting_plan() -> None:
    table, cons, _, _ = solved(15.0, 150_000.0, 3_000.0)
    units = np.zeros(table.n_equipment, dtype=np.int64)
    units[table.index_of("treadmill")] = 16 # the whole budget on one kind of machine
    poor = Selection(
        units=units,
        evaluation=evaluate(table, units),
        cost=float(units @ cons.unit_cost),
        area=float(units @ cons.unit_area),
    )
    better = improve(table, cons, poor)
    assert better.value > 1.5 * poor.value
    assert_feasible(better, cons)


def test_bundle_buys_a_bench_that_is_only_useful_with_dumbbells() -> None:
    """Neither type serves anything alone, so only a joint move can make progress."""
    table = make_table([("bench", 1), ("dumbbells", 6)], [("db_press", 2.0, [(1.0, ["bench", "dumbbells"])])])
    selection = greedy(table, simple_constraints(2, [600.0, 6_000.0], budget_usd=20_000.0))
    assert selection.steps[0].added == {0: 1, 1: 1}
    assert selection.units[0] > selection.units[1] >= 1 # One dumbbell set serves six people and a bench one, so benches end up outnumbering sets.
    assert selection.value > 1.9


def test_half_a_bundle_is_never_bought() -> None:
    table = make_table([("bench", 1), ("dumbbells", 6)], [("db_press", 2.0, [(1.0, ["bench", "dumbbells"])])])
    cons = simple_constraints(2, [600.0, 6_000.0], budget_usd=6_500.0)
    assert optimize(table, cons).units.tolist() == [0, 0]


def test_a_gym_with_few_members_stops_buying_what_they_would_barely_use() -> None:
    """One person at the peak: the relative stopping rules alone would spend the budget on
    variety nobody uses; every unit bought must see ``MIN_UNIT_USE`` at the peak."""
    _, cons, first, few = solved(0.75, 200_000.0, 3_000.0)
    _, _, _, many = solved(15.0, 200_000.0, 3_000.0)
    assert 0 < few.units.sum() < many.units.sum() / 3
    assert few.cost < 0.4 * cons.budget_usd
    assert all(step.gain >= MIN_UNIT_USE for step in first.steps)


def test_one_cheap_piece_does_not_make_the_rest_of_a_small_budget_look_poor_value() -> None:
    """A $100 mat serves as much as a $1,600 bike. Measured against the mat alone the bike would
    return under 4% as much per dollar; measured over half the budget it is well worth buying."""
    table = make_table(
        [("mat", 1), ("bike", 1)],
        [("stretch", 0.15, [(1.0, ["mat"])]), ("cycle", 0.15, [(1.0, ["bike"])])],
    )
    cons = simple_constraints(2, [100.0, 1_600.0], budget_usd=3_000.0, max_units=[1, 1])
    assert optimize(table, cons).units.tolist() == [1, 1]


@pytest.mark.parametrize(("budget_usd", "area_sqft"), [(60_000.0, 2_000.0), (150_000.0, 4_000.0)])
def test_units_per_type_grow_with_demand_at_a_fixed_budget(
    budget_usd: float, area_sqft: float
) -> None:
    """Light demand buys one of many things; heavy demand buys more of the busiest things."""
    mixes = [types_and_units(solved(u, budget_usd, area_sqft)[3]) for u in (1.5, 4, 10, 30, 80)]
    ratios = [units / types for types, units in mixes]
    assert all(later >= earlier for earlier, later in pairwise(ratios))
    assert ratios[-1] >= 2 * ratios[0]
    assert mixes[1][0] >= mixes[-1][0] # At 1.5 active users many types would see too little use to buy (``MIN_UNIT_USE``), so variety is compared from 4 users up.


def test_small_gym_spreads_out_and_large_gym_adds_depth() -> None:
    _, _, _, small = solved(2.0, 20_000.0, 400.0)
    table, _, _, large = solved(75.0, 750_000.0, 15_000.0)
    small_types, small_units = types_and_units(small)
    large_types, large_units = types_and_units(large)
    assert small_units / small_types <= 1.5
    assert large_units / large_types >= 3.0
    assert set(np.flatnonzero(small.units)) <= set(np.flatnonzero(large.units)) # Broad variety is kept as the gym grows: every small-gym type is still there.
    assert large_types >= 0.9 * table.n_equipment


def test_greedy_steps_record_the_build_up() -> None:
    table, cons, first, _ = solved(15.0, 150_000.0, 3_000.0)
    rebuilt = np.zeros(table.n_equipment, dtype=np.int64)
    previous_value = 0.0
    for step in first.steps:
        for r, n in step.added.items():
            rebuilt[r] += n
        assert step.gain > 0
        assert step.value >= previous_value - 1e-6
        assert step.total_cost == pytest.approx(float(rebuilt @ cons.unit_cost))
        assert step.total_area == pytest.approx(float(rebuilt @ cons.unit_area))
        previous_value = step.value
    np.testing.assert_array_equal(rebuilt, first.units)
    assert first.steps[-1].value == pytest.approx(first.value)


def test_greedy_extends_a_start_without_mutating_it() -> None:
    table, cons, _, _ = solved(15.0, 150_000.0, 3_000.0)
    start = np.zeros(table.n_equipment, dtype=np.int64)
    start[table.index_of("treadmill")] = 3
    before = start.copy()
    selection = greedy(table, cons, start=start)
    np.testing.assert_array_equal(start, before)
    assert np.all(selection.units >= start)
    assert_feasible(selection, cons)


def test_greedy_stops_once_the_plan_is_worth_what_was_asked() -> None:
    table, cons, first, _ = solved(15.0, 150_000.0, 3_000.0)
    half = 0.5 * first.value
    early = greedy(table, cons, until_value=half)
    assert early.value >= half
    assert early.cost < first.cost
    assert early.steps == first.steps[: len(early.steps)]


def test_with_no_budget_limit_the_greedy_buys_past_the_budget_within_the_floor() -> None:
    table = gym_table(15.0)
    cons = gym_constraints(table, 40_000.0, 3_000.0)
    unlimited = unlimited_plan(table, cons)
    assert unlimited.cost > 2 * cons.budget_usd
    assert unlimited.area <= cons.area_sqin + 1e-6
    assert unlimited.value > 1.5 * greedy(table, cons).value


def test_plan_worth_reaches_the_value_for_what_its_units_cost() -> None:
    table = gym_table(15.0)
    cons = gym_constraints(table, 40_000.0, 3_000.0)
    unlimited = unlimited_plan(table, cons)
    goal = 0.8 * unlimited.value
    found = plan_worth(table, cons, goal, unlimited.cost)
    assert found is not None
    units, cost = found
    assert cost == pytest.approx(float(units @ cons.unit_cost))
    assert cost < unlimited.cost
    assert evaluate(table, units).value[0] == pytest.approx(goal, rel=0.02) # The value at a step inside a greedy step is a running estimate; re-solved, it is close.
    assert plan_worth(table, cons, table.total_load, unlimited.cost) is None


def test_optimize_is_deterministic() -> None:
    table = gym_table(15.0)
    cons = gym_constraints(table, 150_000.0, 3_000.0)
    np.testing.assert_array_equal(optimize(table, cons).units, optimize(table, cons).units)


def complement_found_late() -> tuple[RouteTable, Constraints]:
    """Twenty cheap single-purpose stations, then dumbbells, then a bench that needs both.

    The stations have the best value per dollar, the dumbbells the worst, so the dumbbells are
    the last purchase. Only then does a bench serve anyone, but its last score was taken while
    the dumbbells were missing.
    """
    stations = [f"station{i}" for i in range(20)]
    table = make_table(
        [(eid, 1) for eid in stations] + [("dumbbells", 1), ("bench", 1)],
        [(f"drill{i}", 0.06, [(1.0, [eid])]) for i, eid in enumerate(stations)] # Each drill is used just enough to be worth a station (``MIN_UNIT_USE``).
        + [("db_curl", 1.0, [(1.0, ["dumbbells"])]), ("db_press", 0.5, [(1.0, ["bench", "dumbbells"])])],
    )
    cons = simple_constraints(
        table.n_equipment,
        [100.0] * 20 + [10_000.0, 5_000.0],
        budget_usd=1_000_000.0,
        max_units=[UNCAPPED] * 20 + [1, UNCAPPED],
    )
    return table, cons


def test_greedy_rescores_stale_moves_before_stopping() -> None:
    table, cons = complement_found_late()
    selection = greedy(table, cons)
    assert worthwhile_additions(table, cons, selection) == {}


def test_swap_search_recovers_the_complement_greedy_left_out() -> None:
    table, cons = complement_found_late()
    selection = optimize(table, cons)
    assert selection.units[table.index_of("bench")] >= 1
    assert worthwhile_additions(table, cons, selection) == {}


def lumpy_item() -> tuple[RouteTable, Constraints]:
    """One expensive station with the best value, and two half-price ones that fill the budget.

    The middle station has the best value per dollar, so the greedy buys it first; the expensive
    one no longer fits, and the cheap one takes the rest. Dropping a single unit never frees
    enough for the expensive one, which is worth more than the other two together.
    """
    table = make_table(
        [("big", 1), ("mid", 1), ("small", 1)],
        [("a", 1.0, [(1.0, ["big"])]), ("b", 0.43, [(1.0, ["mid"])]), ("c", 0.176, [(1.0, ["small"])])],
    )
    cons = simple_constraints(table.n_equipment, [10_000.0, 5_000.0, 5_000.0], budget_usd=10_000.0, max_units=[1, 1, 1])
    return table, cons


def test_swap_search_makes_room_for_an_expensive_unit_the_greedy_reached_too_late() -> None:
    table, cons = lumpy_item()
    first = greedy(table, cons)
    assert list(first.units) == [0, 1, 1]
    best = improve(table, cons, first)
    assert list(best.units) == [1, 0, 0]
    assert best.value > 1.05 * first.value
    assert_feasible(best, cons)


def test_most_wanted_is_first_choice_for_the_most_demand() -> None:
    table = make_table( # Two-type routes count for both types: the dumbbells are first choice for 0.25 + 0.3.
        [("treadmill", 1), ("bike", 1), ("bench", 1), ("dumbbells", 1)],
        [
            ("run", 0.5, [(1.0, ["treadmill"]), (0.4, ["bike"])]),
            ("cycle", 0.3, [(1.0, ["bike"])]),
            ("press", 0.25, [(1.0, ["dumbbells", "bench"])]),
            ("curl", 0.3, [(1.0, ["dumbbells"])]),
        ],
    )
    top = most_wanted(table)
    assert top is not None
    assert table.equipment_ids[top] == "dumbbells"


def favourite(budget_usd: float, own_loads: tuple[float, float]) -> tuple[RouteTable, Constraints]:
    """A $10,000 favourite for the largest exercise, and two $5,000 pieces with their own."""
    table = make_table(
        [("favourite", 1), ("alternative", 1), ("other", 1)],
        [
            ("a", 0.6, [(1.0, ["favourite"]), (0.8, ["alternative"])]),
            ("b", own_loads[0], [(1.0, ["alternative"])]),
            ("c", own_loads[1], [(1.0, ["other"])]),
        ],
    )
    cons = simple_constraints(3, [10_000.0, 5_000.0, 5_000.0], budget_usd=budget_usd, max_units=[1, 1, 1])
    return table, cons


def plan_of(table: RouteTable, cons: Constraints, units: list[int]) -> Selection:
    chosen = np.array(units, dtype=np.int64)
    return Selection(
        units=chosen,
        evaluation=evaluate(table, chosen),
        cost=float(chosen @ cons.unit_cost),
        area=float(chosen @ cons.unit_area),
    )


def test_the_most_wanted_type_replaces_a_plan_that_serves_about_the_same() -> None:
    table, cons = favourite(15_000.0, (0.2, 0.4))
    without = plan_of(table, cons, [0, 1, 1])
    chosen, held = with_most_wanted(table, cons, without)
    assert chosen.units[0] == 1
    assert chosen.value >= without.value * (1 - MOST_WANTED_TOLERANCE)
    assert held.min_units is not None and held.min_units[0] == 1
    assert_feasible(chosen, cons)


def test_the_most_wanted_type_gives_way_when_it_would_take_the_whole_budget() -> None:
    table, cons = favourite(10_000.0, (0.2, 0.3))
    without = optimize(table, cons)
    assert without.units.tolist() == [0, 1, 1]
    chosen, held = with_most_wanted(table, cons, without)
    assert chosen is without
    assert held is cons


def test_the_most_wanted_type_is_held_at_the_units_its_own_demand_needs() -> None:
    """Runners settle for an elliptical at 0.55: a budget plan buys cheaper ellipticals in place
    of treadmills, and most runners find every treadmill busy."""
    table = make_table(
        [("treadmill", 1), ("elliptical", 1)],
        [
            ("run", 4.0, [(1.0, ["treadmill"]), (0.55, ["elliptical"])]),
            ("glide", 1.5, [(1.0, ["elliptical"]), (0.5, ["treadmill"])]),
        ],
    )
    cons = simple_constraints(2, [9_000.0, 4_000.0], budget_usd=60_000.0)
    free = optimize(table, cons)
    wanted = servers_for_blocking(4.0, MOST_WANTED_BLOCKING)
    assert free.units[0] < wanted
    holds = list(most_wanted_holds(table, cons, free))
    plan, held = holds[0]
    assert plan.units[0] == wanted
    assert held.min_units is not None and held.min_units[0] == wanted
    assert_feasible(plan, held)
    chosen, _ = with_most_wanted(table, cons, free)
    assert chosen.units[0] >= wanted
    assert serves_within_tolerance(chosen.value, free.value)


def test_most_wanted_tolerance_is_measured_on_the_plan_that_holds_it() -> None:
    assert serves_within_tolerance(100.0, 100.0 * (1 + MOST_WANTED_TOLERANCE)) # "Unless leaving it out serves more than 5% more": 105 against 100 is within, 105.1 not.
    assert not serves_within_tolerance(100.0, 100.0 * (1 + MOST_WANTED_TOLERANCE) + 0.1)
    assert serves_within_tolerance(100.0, 100.0 * (1 + COVERAGE_TOLERANCE), COVERAGE_TOLERANCE)
    assert not serves_within_tolerance(100.0, 101.0 + 100.0 * COVERAGE_TOLERANCE, 0.01)


def rounded_gym() -> tuple[RouteTable, Constraints]:
    """Dumbbells and a bench cover curls; squats, presses and rows only make do with them."""
    table = make_table(
        [("dumbbells", 1), ("bench", 1), ("barbell", 1), ("rack", 1), ("cable", 1), ("landmine", 1), ("calf_raise", 1)],
        [
            ("squat", 0.5, [(1.0, ["rack"]), (0.6, ["dumbbells"])]),
            ("bench_press", 0.4, [(1.0, ["rack", "bench"]), (0.7, ["dumbbells", "bench"])]),
            ("curl", 0.3, [(1.0, ["dumbbells"]), (0.8, ["cable"])]),
            ("row", 0.2, [(1.0, ["cable"]), (0.7, ["dumbbells"])]),
            ("landmine_press", 0.15, [(1.0, ["landmine", "barbell"])]),
            ("calf_raise", 0.005, [(1.0, ["calf_raise"])]),
        ],
    )
    rack = 3
    requires: tuple[tuple[int, ...], ...] = tuple((2,) if r == rack else () for r in range(7))
    cons = simple_constraints(7, [5_000.0, 500.0, 900.0, 3_000.0, 4_000.0, 300.0, 2_000.0], requires=requires)
    return table, cons


def test_coverage_moves_rank_stations_by_the_demand_they_newly_serve_well() -> None:
    """The rack (with the barbell it needs) gives squats and bench presses a well-suited route;
    the cable gives rows one; the landmine needs the barbell too, so they come as a pair. Calf
    raises are under ``COVERAGE_MIN_SHARE`` of all demand."""
    table, cons = rounded_gym()
    units = np.array([1, 1, 0, 0, 0, 0, 0], dtype=np.int64)
    moves = coverage_moves(table, cons, units)
    assert [sorted(table.equipment_ids[r] for r in m.added) for m in moves] == [
        ["barbell", "rack"],
        ["cable"],
        ["barbell", "landmine"],
    ]
    assert [m.covered for m in moves] == pytest.approx([0.9, 0.2, 0.15])
    assert COVERAGE_MIN_SHARE * table.total_load > 0.005


def test_coverage_moves_are_empty_once_everything_has_a_well_suited_route() -> None:
    table, cons = rounded_gym()
    assert coverage_moves(table, cons, np.ones(7, dtype=np.int64)) == []


def test_held_addition_keeps_the_station_and_its_prerequisites_within_the_budget() -> None:
    table, base = rounded_gym()
    cons = replace(base, budget_usd=9_000.0)
    selection = plan_of(table, cons, [1, 1, 0, 0, 1, 0, 0])
    found = held_addition(table, cons, selection, {3: 1, 2: 1})
    assert found is not None
    plan, held = found
    assert plan.units[3] >= 1 and plan.units[2] >= 1
    assert held.min_units is not None and held.min_units[[2, 3]].tolist() == [1, 1]
    assert_feasible(plan, held)
    assert held_addition(table, replace(base, budget_usd=3_000.0), selection, {3: 1, 2: 1}) is None # The rack and barbell alone cost $3,900: on $3,000 nothing can hold them.


def random_instance(
    seed: int, n_types: int = 60, n_exercises: int = 100
) -> tuple[RouteTable, Constraints]:
    rng = np.random.default_rng(seed)
    equipment = [(f"type{i}", int(rng.choice([1, 1, 1, 1, 2, 4]))) for i in range(n_types)]
    exercises: list[ExerciseSpec] = []
    for e in range(n_exercises):
        routes: list[Route] = []
        quality = 1.0
        for _ in range(int(rng.integers(2, 6))):
            size = 2 if rng.random() < 0.2 else 1
            routes.append((quality, [f"type{i}" for i in rng.choice(n_types, size, replace=False)]))
            quality = round(quality * rng.uniform(0.5, 0.95), 3)
        exercises.append((f"ex{e}", float(rng.gamma(1.5, 0.6)), routes))
    table = make_table(equipment, exercises)
    cons = Constraints(
        budget_usd=2_000_000.0,
        area_sqin=12_000 * SQIN_PER_SQFT,
        unit_cost=rng.uniform(300, 9_000, n_types),
        unit_area=rng.uniform(15, 80, n_types) * SQIN_PER_SQFT,
        max_units=np.full(n_types, UNCAPPED, dtype=np.int64),
        requires=((),) * n_types,
    )
    return table, cons


def test_greedy_is_fast_on_a_large_catalog() -> None:
    table, cons = random_instance(seed=0)
    started = time.perf_counter()
    selection = greedy(table, cons)
    elapsed = time.perf_counter() - started
    assert elapsed < GREEDY_SECONDS, f"greedy took {elapsed:.1f}s"
    assert len(selection.steps) > 100
    assert selection.evaluation.served[0] > 0.9 * table.total_load
    assert_feasible(selection, cons)


@pytest.mark.parametrize("seed", [3, 7])
def test_taking_independent_moves_together_matches_one_at_a_time(
    seed: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Runners-up that share no exercise with the step's best move do not change its value."""
    import gymplanner.selection.optimizer as optimizer_module

    table, cons = random_instance(seed, n_types=30, n_exercises=50)
    together = greedy(table, cons)
    monkeypatch.setattr(optimizer_module, "MAX_MOVES_PER_STEP", 1)
    one_by_one = greedy(table, cons)
    assert together.value == pytest.approx(one_by_one.value, rel=0.01)
    assert_feasible(together, cons)
    rebuilt = np.zeros(table.n_equipment, dtype=np.int64)
    for step in together.steps:
        for r, n in step.added.items():
            rebuilt[r] += n
    np.testing.assert_array_equal(rebuilt, together.units)
    assert together.steps[-1].value == pytest.approx(together.value)
