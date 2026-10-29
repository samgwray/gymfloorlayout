"""Loss-network evaluator against closed forms on hand-built route tables.

Single-route cases must reproduce Erlang carried load exactly. Overflow and two-type routes are
compared with the reduced-load fixed point solved independently here in scalar code, and
random tables check the bookkeeping identities that hold for any plan.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import fields
from typing import Any

import numpy as np
import pytest

from gymplanner.catalog.loader import Catalog
from gymplanner.catalog.schema import (
    Clearance,
    Dimensions,
    Equipment,
    Exercise,
    ExerciseOption,
    PriceTiers,
)
from gymplanner.domain import Demand, PeakEstimate
from gymplanner.queueing import carried_load, erlang_b
from gymplanner.selection.evaluator import (
    MAX_ROUTES_PER_EXERCISE,
    Evaluation,
    RouteTable,
    build_route_table,
    evaluate,
)

Route = tuple[float, Sequence[str]]
ExerciseSpec = tuple[str, float, Sequence[Route]]


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


def solve(table: RouteTable, units: Sequence[int] | np.ndarray) -> Evaluation:
    """Evaluate to a tight fixed-point tolerance so results can be held to closed forms."""
    return evaluate(table, np.asarray(units, dtype=np.int64), tolerance=1e-13, max_iterations=5_000)


def random_table(seed: int, n_types: int = 12, n_exercises: int = 25) -> RouteTable:
    """Mixed single- and two-type routes with falling quality, plus some unroutable demand."""
    rng = np.random.default_rng(seed)
    equipment = [(f"type{i}", int(rng.choice([1, 1, 1, 2, 4]))) for i in range(n_types)]
    exercises: list[ExerciseSpec] = []
    for e in range(n_exercises):
        routes: list[Route] = []
        quality = 1.0
        for _ in range(int(rng.integers(1, 4))):
            size = 2 if rng.random() < 0.25 else 1
            uses = [f"type{i}" for i in rng.choice(n_types, size=size, replace=False)]
            routes.append((quality, uses))
            quality = round(quality * rng.uniform(0.4, 0.9), 3)
        exercises.append((f"ex{e}", float(rng.uniform(0.05, 3.0)), routes))
    return make_table(equipment, exercises, unroutable_load=0.7)


def random_plans(table: RouteTable, seed: int, n_plans: int = 8) -> np.ndarray:
    return np.random.default_rng(seed).integers(0, 4, size=(n_plans, table.n_equipment))


def two_type_fixed_point(load: float, servers_a: int, servers_b: int) -> tuple[float, float]:
    """Reduced-load fixed point for one route through two types, solved independently.

    Each type is offered the route's load thinned by the chance the other type is busy.
    """
    block_a = block_b = 0.0
    for _ in range(100_000):
        new_a = erlang_b(servers_a, load * (1.0 - block_b))
        new_b = erlang_b(servers_b, load * (1.0 - block_a))
        if abs(new_a - block_a) + abs(new_b - block_b) < 1e-15:
            break
        block_a, block_b = 0.5 * (block_a + new_a), 0.5 * (block_b + new_b)
    return block_a, block_b


@pytest.mark.parametrize(
    ("units", "stations", "load"),
    [(1, 1, 1.0), (3, 1, 2.5), (2, 2, 7.0), (5, 1, 0.3), (1, 4, 40.0), (12, 1, 9.0)],
)
def test_single_exercise_single_type_is_erlang_carried_load(
    units: int, stations: int, load: float
) -> None:
    table = make_table([("rack", stations)], [("squat", load, [(1.0, ["rack"])])])
    result = evaluate(table, np.array([units]))
    servers = units * stations
    assert result.served[0] == pytest.approx(carried_load(servers, load), rel=1e-12)
    assert result.value[0] == pytest.approx(carried_load(servers, load), rel=1e-12)
    assert result.blocking[0, 0] == pytest.approx(erlang_b(servers, load), rel=1e-12)
    assert result.offered[0, 0] == pytest.approx(load, rel=1e-12)
    assert result.carried()[0, 0] == pytest.approx(carried_load(servers, load), rel=1e-12)


def test_no_units_serves_nothing() -> None:
    table = make_table([("rack", 1)], [("squat", 3.0, [(1.0, ["rack"])])])
    result = evaluate(table, np.array([0]))
    assert result.value[0] == 0.0
    assert result.served[0] == 0.0
    assert result.blocking[0, 0] == 0.0
    assert result.offered[0, 0] == 0.0


def test_value_weights_served_load_by_route_quality() -> None:
    table = make_table(
        [("smith", 1), ("leg_press", 1)],
        [("squat", 2.0, [(0.6, ["smith"])]), ("leg_press", 1.5, [(1.0, ["leg_press"])])],
    )
    result = evaluate(table, np.array([2, 1]))
    squat, press = carried_load(2, 2.0), carried_load(1, 1.5)
    assert result.served[0] == pytest.approx(squat + press, rel=1e-12)
    assert result.value[0] == pytest.approx(0.6 * squat + press, rel=1e-12)


RUN_ROUTES: list[Route] = [(1.0, ["treadmill"]), (0.5, ["elliptical"])]


def test_load_overflows_to_fallback_when_preferred_type_is_absent() -> None:
    table = make_table([("treadmill", 1), ("elliptical", 1)], [("run", 3.0, RUN_ROUTES)]) # Only half the runners (relative fit 0.5 / 1.0) are willing to use an elliptical instead.
    result = evaluate(table, np.array([0, 2]))
    assert result.route_carried[0, 0, 0] == 0.0
    assert result.offered[0, 0] == 0.0
    assert result.offered[0, 1] == pytest.approx(1.5, rel=1e-12)
    assert result.served[0] == pytest.approx(carried_load(2, 1.5), rel=1e-12)
    assert result.value[0] == pytest.approx(0.5 * carried_load(2, 1.5), rel=1e-12)


def test_blocked_load_overflows_to_fallback_when_preferred_type_is_saturated() -> None:
    load = 3.0
    table = make_table([("treadmill", 1), ("elliptical", 1)], [("run", load, RUN_ROUTES)])
    result = solve(table, [1, 2])

    first_blocking = erlang_b(1, load)
    overflow = 0.5 * load * first_blocking # half of the blocked runners accept the fallback
    second_blocking = erlang_b(2, overflow)
    first, second = load * (1 - first_blocking), overflow * (1 - second_blocking)
    np.testing.assert_allclose(result.route_carried[0, 0], [first, second], rtol=1e-9)
    np.testing.assert_allclose(result.offered[0], [load, overflow], rtol=1e-9)
    np.testing.assert_allclose(result.blocking[0], [first_blocking, second_blocking], rtol=1e-9)
    assert result.value[0] == pytest.approx(first + 0.5 * second, rel=1e-9)

    without_fallback = evaluate(table, np.array([1, 0]))
    assert result.value[0] > without_fallback.value[0] + 0.5 * second * 0.99


def test_poor_substitutes_absorb_little_demand_however_many_are_bought() -> None:
    table = make_table([("treadmill", 1), ("rower", 1)], [("run", 4.0, [(1.0, ["treadmill"]), (0.2, ["rower"])])]) # Runners accept a rower at quality 0.2: even unlimited rowers serve at most a fifth of them, so a missing treadmill cannot be papered over with cheap substitutes.
    plenty_of_rowers = solve(table, [0, 200])
    assert plenty_of_rowers.served[0] == pytest.approx(0.2 * 4.0, rel=1e-6)
    assert plenty_of_rowers.value[0] == pytest.approx(0.2 * 0.2 * 4.0, rel=1e-6)
    one_treadmill = solve(table, [1, 0])
    assert one_treadmill.value[0] > plenty_of_rowers.value[0]


def test_fallback_is_idle_when_preferred_type_has_ample_capacity() -> None:
    table = make_table([("treadmill", 1), ("elliptical", 1)], [("run", 3.0, RUN_ROUTES)])
    result = solve(table, [50, 2])
    assert result.route_carried[0, 0, 1] < 1e-12
    assert result.value[0] == pytest.approx(3.0, rel=1e-12)


PRESS_TYPES = [("bench", 1), ("dumbbells", 6)]


@pytest.mark.parametrize("units", [[3, 0], [0, 2]])
def test_two_type_route_needs_both_types(units: list[int]) -> None:
    table = make_table(PRESS_TYPES, [("db_press", 2.0, [(1.0, ["bench", "dumbbells"])])])
    result = evaluate(table, np.array(units))
    assert result.served[0] == 0.0
    assert result.value[0] == 0.0
    np.testing.assert_array_equal(result.offered[0], [0.0, 0.0])


@pytest.mark.parametrize(
    ("load", "benches", "dumbbell_sets", "dumbbell_stations"),
    [(2.0, 3, 2, 1), (2.0, 1, 1, 1), (5.0, 4, 1, 6), (9.0, 6, 2, 6), (0.4, 2, 1, 1)],
)
def test_two_type_route_matches_reduced_load_fixed_point(
    load: float, benches: int, dumbbell_sets: int, dumbbell_stations: int
) -> None:
    table = make_table(
        [("bench", 1), ("dumbbells", dumbbell_stations)],
        [("db_press", load, [(1.0, ["bench", "dumbbells"])])],
    )
    result = solve(table, [benches, dumbbell_sets])
    bench, dumbbells = two_type_fixed_point(load, benches, dumbbell_sets * dumbbell_stations)
    np.testing.assert_allclose(result.blocking[0], [bench, dumbbells], rtol=1e-8, atol=1e-12)
    np.testing.assert_allclose(result.offered[0], [load * (1 - dumbbells), load * (1 - bench)], rtol=1e-8)
    assert result.served[0] == pytest.approx(load * (1 - bench) * (1 - dumbbells), rel=1e-8)


def test_two_type_route_falls_back_to_single_type_route() -> None:
    table = make_table([*PRESS_TYPES, ("cable", 2)], [("fly", 2.0, [(1.0, ["bench", "dumbbells"]), (0.6, ["cable"])])])
    result = evaluate(table, np.array([0, 1, 1]))
    assert result.route_carried[0, 0, 0] == 0.0
    np.testing.assert_array_equal(result.offered[0, :2], [0.0, 0.0]) # A route that cannot exist must not tie up the dumbbells it would have used.
    willing = 0.6 * 2.0
    assert result.served[0] == pytest.approx(carried_load(2, willing), rel=1e-12)
    assert result.value[0] == pytest.approx(0.6 * carried_load(2, willing), rel=1e-12)


def test_fallback_sharing_a_busy_type_is_conditioned_on_the_first_failure() -> None:
    table = make_table( # Bench press with dumbbells, else dumbbells alone: both routes need the single dumbbell station, so together they can never carry more than that station's Erlang capacity.
        [("bench", 1), ("dumbbells", 1)],
        [("press", 1.0, [(1.0, ["bench", "dumbbells"]), (1.0, ["dumbbells"])])],
    )
    result = solve(table, [1, 1])
    assert result.served[0] == pytest.approx(carried_load(1, 1.0), rel=1e-6)
    assert result.offered[0, 1] == pytest.approx(1.0, rel=1e-6) # Each member is offered to the shared dumbbells exactly once.


def test_conditioned_fallback_matches_exact_state_enumeration() -> None:
    table = make_table([("a", 1), ("b", 1)], [("x", 1.0, [(1.0, ["a", "b"]), (1.0, ["b"])])]) # Two independent types with fixed blocking: route 0 needs both, route 1 needs only "b". Conditioned on route 0 failing, "b" is free only when "a" was the busy one.
    from gymplanner.selection.evaluator import _sweep

    blocking = np.array([[0.3, 0.4]])
    value, _, _, carried = _sweep(table, blocking, np.array([[True, True]]))
    p_both_free = 0.7 * 0.6
    p_only_b_free = 0.3 * 0.6 # a busy, b free
    assert carried[0, 0, 0] == pytest.approx(p_both_free)
    assert carried[0, 0, 1] == pytest.approx(p_only_b_free)
    assert value[0] == pytest.approx(0.6) # served whenever b is free


def test_unroutable_load_counts_toward_total_but_is_never_served() -> None:
    table = make_table([("bike", 1)], [("cycling", 2.0, [(1.0, ["bike"])])], unroutable_load=1.5)
    assert table.total_load == pytest.approx(3.5)
    result = evaluate(table, np.array([1_000]))
    assert result.served[0] == pytest.approx(2.0, rel=1e-12)
    assert result.served[0] / table.total_load == pytest.approx(2.0 / 3.5, rel=1e-12)


@pytest.mark.parametrize("seed", range(5))
def test_batch_evaluation_equals_one_by_one(seed: int) -> None:
    table = random_table(seed)
    plans = random_plans(table, seed)
    batch = evaluate(table, plans)
    for i, plan in enumerate(plans):
        single = evaluate(table, plan)
        assert batch.value[i] == pytest.approx(single.value[0], rel=1e-10, abs=1e-12)
        assert batch.served[i] == pytest.approx(single.served[0], rel=1e-10, abs=1e-12)
        np.testing.assert_allclose(batch.blocking[i], single.blocking[0], atol=1e-10)
        np.testing.assert_allclose(batch.offered[i], single.offered[0], rtol=1e-10, atol=1e-12)
        np.testing.assert_allclose(batch.route_carried[i], single.route_carried[0], rtol=1e-10, atol=1e-12)


@pytest.mark.parametrize("seed", range(4))
def test_warm_start_gives_the_same_answer_as_cold(seed: int) -> None:
    table = random_table(seed)
    plans = random_plans(table, seed)
    cold = evaluate(table, plans)
    rng = np.random.default_rng(seed)
    starts = {
        "other plans": cold.blocking[::-1].copy(),
        "all busy": np.ones(table.n_equipment),
        "random": rng.uniform(0.0, 1.0, table.n_equipment),
    }
    for label, warm in starts.items():
        result = evaluate(table, plans, warm_blocking=warm)
        np.testing.assert_allclose(result.value, cold.value, rtol=1e-4, err_msg=label)
        np.testing.assert_allclose(result.blocking, cold.blocking, atol=1e-4, err_msg=label)

    tight_cold = evaluate(table, plans, tolerance=1e-12, max_iterations=2_000)
    tight_warm = evaluate(table, plans, warm_blocking=starts["random"], tolerance=1e-12, max_iterations=2_000)
    np.testing.assert_allclose(tight_warm.value, tight_cold.value, rtol=1e-9)


def test_one_dimensional_units_are_a_batch_of_one() -> None:
    table = random_table(seed=1)
    units = random_plans(table, seed=1)[0]
    result = evaluate(table, units)
    n_exercises, n_routes, _ = table.route_res.shape
    assert result.value.shape == (1,)
    assert result.blocking.shape == (1, table.n_equipment)
    assert result.route_carried.shape == (1, n_exercises, n_routes)


@pytest.mark.parametrize("seed", range(6))
def test_flow_identities_hold_for_any_plan(seed: int) -> None:
    table = random_table(seed)
    plans = random_plans(table, seed + 50)
    result = evaluate(table, plans)
    servers = plans * table.stations

    assert np.all(result.value >= 0)
    assert np.all(result.value <= result.served + 1e-12)
    assert np.all(result.served <= table.load.sum() + 1e-9)
    np.testing.assert_allclose(result.served, result.route_carried.sum(axis=(1, 2)), rtol=1e-12)
    np.testing.assert_allclose(
        result.value, np.einsum("nek,ek->n", result.route_carried, table.route_quality), rtol=1e-12
    )
    through_type = np.einsum("nek,kuer->nr", result.route_carried, table.incidence) # A type carries exactly the demand served on routes through it, never beyond capacity.
    np.testing.assert_allclose(result.carried(), through_type, rtol=1e-9, atol=1e-12)
    assert np.all(result.carried() <= servers + 1e-6)
    assert np.all((result.blocking >= 0) & (result.blocking <= 1))
    assert np.all(result.blocking[servers == 0] == 0)


def test_relabelling_types_and_exercises_does_not_change_the_answer() -> None:
    table = random_table(seed=5)
    rng = np.random.default_rng(5)
    units = rng.integers(0, 4, size=table.n_equipment)
    type_perm = rng.permutation(table.n_equipment)
    ex_perm = rng.permutation(len(table.exercise_ids))
    new_index = np.argsort(type_perm)
    route_res = table.route_res[ex_perm]
    relabelled = RouteTable(
        equipment_ids=tuple(table.equipment_ids[i] for i in type_perm),
        stations=table.stations[type_perm],
        exercise_ids=tuple(table.exercise_ids[i] for i in ex_perm),
        load=table.load[ex_perm],
        route_res=np.where(route_res >= 0, new_index[np.maximum(route_res, 0)], -1),
        route_quality=table.route_quality[ex_perm],
        incidence=table.incidence[:, :, ex_perm][..., type_perm],
        unroutable_load=table.unroutable_load,
    )
    base = solve(table, units)
    moved = solve(relabelled, units[type_perm])
    assert moved.value[0] == pytest.approx(base.value[0], rel=1e-9)
    assert moved.served[0] == pytest.approx(base.served[0], rel=1e-9)
    np.testing.assert_allclose(moved.blocking[0], base.blocking[0][type_perm], atol=1e-9)


def _equipment(eid: str, stations: int = 1) -> Equipment:
    return Equipment(
        id=eid,
        name=eid,
        category="free_weights",
        zone="free_weights",
        description="fixture",
        footprint=Dimensions(length_in=48, width_in=24),
        clearance=Clearance(front_in=24, back_in=24, left_in=12, right_in=12),
        stations=stations,
        price_usd=PriceTiers(value=100, commercial=200, premium=300),
        sources=["fixture"],
    )


def _exercise(xid: str, options: Sequence[Route]) -> Exercise:
    return Exercise(
        id=xid,
        name=xid,
        modality="dumbbell",
        pattern="horizontal_push",
        popularity=1.0,
        block_minutes=10.0,
        options=[ExerciseOption(uses=list(uses), quality=q) for q, uses in options],
        sources=["fixture"],
    )


def _catalog(equipment: Sequence[Equipment], exercises: Sequence[Exercise]) -> Catalog:
    """Catalog with only the equipment and exercises sections, all build_route_table reads.

    The other sections stay empty so the fixture does not churn as the catalog grows.
    """
    sections: dict[str, Any] = {f.name: () for f in fields(Catalog) if f.name != "data_version"}
    sections.update(equipment=tuple(equipment), exercises=tuple(exercises))
    return Catalog(**sections)


def _demand(exercise_load: dict[str, float]) -> Demand:
    total = sum(exercise_load.values())
    peak = PeakEstimate(
        peak_users=total,
        method="density",
        members=None,
        area_users=total,
        member_users=None,
        capped_by_code=False,
    )
    return Demand(
        profile_id="general",
        peak=peak,
        active_users=total,
        modality_share={"dumbbell": 1.0},
        exercise_load=exercise_load,
    )


ROUTE_CATALOG = _catalog(
    [_equipment("bench"), _equipment("dumbbells", stations=6), _equipment("cable", stations=2), _equipment("treadmill")],
    [
        _exercise("db_press", [(0.6, ["cable"]), (1.0, ["bench", "dumbbells"]), (0.8, ["dumbbells"])]),
        _exercise("db_row", [(0.9, ["bench", "dumbbells"]), (0.9, ["dumbbells"])]),
        _exercise("run", [(1.0, ["treadmill"])]),
        _exercise("stretch", [(1.0, ["bench"])]),
    ],
)
ROUTE_LOADS = {"db_press": 2.0, "db_row": 1.2, "run": 0.9}


def test_build_route_table_sorts_routes_and_matches_hand_built_table() -> None:
    allowed = ["bench", "dumbbells", "cable"]
    table = build_route_table(ROUTE_CATALOG, _demand(ROUTE_LOADS), allowed)
    expected = make_table(
        [("bench", 1), ("dumbbells", 6), ("cable", 2)],
        [
            ("db_press", 2.0, [(1.0, ["bench", "dumbbells"]), (0.8, ["dumbbells"]), (0.6, ["cable"])]),
            ("db_row", 1.2, [(0.9, ["dumbbells"]), (0.9, ["bench", "dumbbells"])]), # Equal quality: the route that ties up fewer types is tried first.
        ],
        unroutable_load=0.9,
    )
    assert table.equipment_ids == expected.equipment_ids
    assert table.exercise_ids == expected.exercise_ids
    np.testing.assert_array_equal(table.stations, expected.stations)
    np.testing.assert_array_equal(table.load, expected.load)
    np.testing.assert_array_equal(table.route_res, expected.route_res)
    np.testing.assert_array_equal(table.route_quality, expected.route_quality)
    np.testing.assert_array_equal(table.incidence, expected.incidence)
    assert table.unroutable_load == pytest.approx(0.9) # "run" needs a type that is not allowed; "stretch" has no demand and is left out entirely.
    assert table.total_load == pytest.approx(2.0 + 1.2 + 0.9)


def test_build_route_table_drops_options_using_excluded_types() -> None:
    table = build_route_table(ROUTE_CATALOG, _demand(ROUTE_LOADS), ["bench", "cable"])
    assert table.exercise_ids == ("db_press",)
    np.testing.assert_array_equal(table.route_quality, [[0.6]])
    assert table.unroutable_load == pytest.approx(1.2 + 0.9)
    result = evaluate(table, np.array([5, 50]))
    assert result.served[0] == pytest.approx(2.0, rel=1e-6)


def test_build_route_table_keeps_the_best_routes_when_there_are_too_many() -> None:
    n_options = MAX_ROUTES_PER_EXERCISE + 3
    stations = [_equipment(f"station{i}") for i in range(n_options)]
    options = [(round(1.0 - 0.05 * i, 2), [f"station{i}"]) for i in range(n_options)]
    catalog = _catalog(stations, [_exercise("curl", options[::-1])])
    table = build_route_table(catalog, _demand({"curl": 1.0}), [s.id for s in stations])
    assert table.route_quality.shape == (1, MAX_ROUTES_PER_EXERCISE)
    np.testing.assert_allclose(table.route_quality[0], [q for q, _ in options][:8])
    np.testing.assert_array_equal(table.route_res[0, :, 0], np.arange(MAX_ROUTES_PER_EXERCISE))


def test_equipment_left_out_of_the_plan_still_sets_how_willing_members_are_to_settle() -> None:
    every = ["bench", "dumbbells", "cable"] # A missing bench does not promote the 0.8 dumbbell-only route to first choice: willingness stays at 80%.
    full = build_route_table(ROUTE_CATALOG, _demand(ROUTE_LOADS), every)
    no_bench = build_route_table(ROUTE_CATALOG, _demand(ROUTE_LOADS), ["dumbbells", "cable"], offered=every)
    np.testing.assert_allclose(no_bench.reference_quality, [1.0, 0.9])
    np.testing.assert_allclose(no_bench.sweep_plan.willing[0], [0.8, 0.6 / 0.8])
    for dumbbells, cables in [(0, 1), (1, 0), (1, 1), (2, 3)]:
        with_bench_slot = solve(full, [0, dumbbells, cables])
        without = solve(no_bench, [dumbbells, cables])
        assert without.value[0] == pytest.approx(with_bench_slot.value[0], rel=1e-9)
        assert without.served[0] == pytest.approx(with_bench_slot.served[0], rel=1e-9)
    alone = build_route_table(ROUTE_CATALOG, _demand(ROUTE_LOADS), ["dumbbells", "cable"]) # Leaving ``offered`` out keeps the table's own best route as the reference.
    np.testing.assert_allclose(alone.reference_quality, [0.8, 0.9])
    assert solve(alone, [1, 1]).served[0] > solve(no_bench, [1, 1]).served[0]
