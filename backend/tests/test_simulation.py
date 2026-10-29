"""Design-hour simulation: queueing theory where it is exact, bookkeeping everywhere else.

With patience 0 a single station type is an Erlang loss system, so the skipped share must
match Erlang B; with unlimited patience it is a delay system, so waits must match
Pollaczek-Khinchine and Erlang C. Scripted runs (members arriving at set minutes, constant
block lengths) pin the rules the averages cannot: who gets freed stations, what a patience
timeout does and records, and which blocks and station-minutes fall inside the measured
window. Beyond that the tests pin the member model's calibration (offered Erlangs and floor
population match the demand model), the route semantics, reproducibility, and the run time
the planner depends on.
"""

from __future__ import annotations

import math
import time
from dataclasses import replace
from itertools import repeat
from typing import Any

import numpy as np
import pytest
from numpy.typing import NDArray

from gymplanner.queueing import erlang_b
from gymplanner.selection.evaluator import RouteTable
from gymplanner.simulation import SimulationConfig, SimulationResult, simulate_peak
from gymplanner.simulation.behavior import ExerciseMix, no_repeat_weights
from gymplanner.simulation.engine import _IDLE, _build_floor, _peak_concurrency, _Run

RouteSpec = tuple[float, list[str]]
ExerciseSpec = tuple[str, float, list[RouteSpec]]

ONE_BLOCK_VISIT_MIN = 1e-3
"""A planned stay far shorter than any block: every member trains exactly one block."""


def route_table(
    stations: dict[str, int], exercises: list[ExerciseSpec], unroutable_load: float = 0.0
) -> RouteTable:
    """Hand-built RouteTable; routes are listed best first, as build_route_table orders them."""
    equipment_ids = tuple(stations)
    index = {eid: i for i, eid in enumerate(equipment_ids)}
    n_routes = max((len(routes) for _, _, routes in exercises), default=1)
    n_slots = max((len(uses) for _, _, routes in exercises for _, uses in routes), default=1)
    shape = (len(exercises), n_routes, n_slots)
    route_res = np.full(shape, -1, dtype=np.int64)
    route_quality = np.zeros(shape[:2])
    incidence = np.zeros((n_routes, n_slots, len(exercises), len(equipment_ids)))
    for e, (_, _, routes) in enumerate(exercises):
        for k, (quality, uses) in enumerate(routes):
            route_quality[e, k] = quality
            for u, eid in enumerate(uses):
                route_res[e, k, u] = index[eid]
                incidence[k, u, e, index[eid]] = 1.0
    return RouteTable(
        equipment_ids=equipment_ids,
        stations=np.array([stations[eid] for eid in equipment_ids], dtype=np.int64),
        exercise_ids=tuple(exercise_id for exercise_id, _, _ in exercises),
        load=np.array([load for _, load, _ in exercises], dtype=np.float64),
        route_res=route_res,
        route_quality=route_quality,
        incidence=incidence,
        unroutable_load=unroutable_load,
    )


def config(**overrides: Any) -> SimulationConfig:
    base = SimulationConfig(peak_users=40.0, mean_floor_minutes=60.0, floor_minutes_cv=0.4, idle_share=0.25, seed=7)
    return replace(base, **overrides)


def one_block_visits(arrivals_per_min: float, **overrides: Any) -> SimulationConfig:
    """Poisson arrivals that each train one block and leave: a textbook M/G/c/c system."""
    settings: dict[str, Any] = {
        "peak_users": arrivals_per_min * ONE_BLOCK_VISIT_MIN,
        "mean_floor_minutes": ONE_BLOCK_VISIT_MIN,
        "idle_share": 0.0,
        "patience_min": 0.0,
        "warmup_min": 20.0,
    }
    return config(**(settings | overrides))


def scripted(**overrides: Any) -> SimulationConfig:
    """Settings for staged runs: constant block lengths, no idle gaps, no warm-up."""
    settings: dict[str, Any] = {"block_minutes_cv": 0.0, "idle_share": 0.0, "warmup_min": 0.0}
    return config(**(settings | overrides))


def staged_run(
    table: RouteTable,
    units: list[int],
    blocks: dict[str, float],
    settings: SimulationConfig,
    attempts: list[float],
) -> _Run:
    """A run with scripted members instead of random arrivals.

    Member ``i`` arrives at ``attempts[i]``, makes one attempt and leaves when that block
    ends. Call ``_advance()`` to play the events, then ``_result()``.
    """
    run = _Run(_build_floor(table, np.array(units), blocks, settings), settings)
    times = np.array(attempts, dtype=np.float64)
    run._add_members(times, times, times, np.ones(times.size, dtype=bool))
    return run


def single_station_table(load: float) -> RouteTable:
    return route_table({"rack": 1}, [("squat", load, [(1.0, ["rack"])])])


def served_blocks(result: SimulationResult) -> float:
    return result.exercise_blocks * (result.first_choice_share + result.substituted_share)


def erlang_c(servers: int, load: float) -> float:
    """Probability that an arrival to an M/M/c queue has to wait."""
    blocking = erlang_b(servers, load)
    return servers * blocking / (servers - load * (1.0 - blocking))


def design_scale_plan(
    seed: int, capacity: float
) -> tuple[RouteTable, NDArray[np.int64], dict[str, float]]:
    """60 equipment types, 100 exercises with 1-4 routes of 1-2 types, 400 users at peak.

    ``capacity`` scales stations relative to the load on each type's best routes, and about a
    tenth of the types get no units, so routes fall back and some exercises cannot be done.
    """
    rng = np.random.default_rng(seed)
    n_types, n_exercises, active_users = 60, 100, 400 * 0.75
    stations = {f"type{r}": int(rng.integers(1, 3)) for r in range(n_types)}
    share = rng.dirichlet(np.full(n_exercises, 0.8))
    exercises: list[ExerciseSpec] = []
    for e in range(n_exercises):
        n_routes = int(rng.integers(1, 5))
        qualities = np.sort(rng.uniform(0.4, 1.0, n_routes))[::-1]
        routes: list[RouteSpec] = []
        for quality in qualities:
            uses = rng.choice(n_types, size=int(rng.integers(1, 3)), replace=False)
            routes.append((float(quality), [f"type{u}" for u in uses]))
        exercises.append((f"exercise{e}", active_users * float(share[e]), routes))
    table = route_table(stations, exercises)
    best_route_load = np.zeros(n_types)
    for e in range(n_exercises):
        for r in table.route_res[e, 0]:
            if r >= 0:
                best_route_load[r] += table.load[e]
    units = np.ceil(capacity * best_route_load / table.stations).astype(np.int64)
    units[rng.random(n_types) < 0.1] = 0
    block_minutes = {f"exercise{e}": float(rng.uniform(4.0, 25.0)) for e in range(n_exercises)}
    return table, units, block_minutes


@pytest.mark.parametrize(("servers", "load"), [(1, 0.5), (2, 1.0), (4, 4.0), (10, 8.0)])
def test_one_block_visits_match_erlang_b(servers: int, load: float) -> None:
    block = 1.0 # Poisson arrivals, gamma blocks, no waiting: blocking is Erlang B whatever the block length distribution (insensitivity), so the skipped share must converge to it.
    sim = simulate_peak(
        single_station_table(load),
        np.array([servers]),
        {"squat": block},
        one_block_visits(load / block, measure_min=8000.0 * block / load),
    )
    assert sim.exercise_blocks > 7000
    assert sim.skipped_share == pytest.approx(erlang_b(servers, load), abs=0.02)
    assert sim.first_choice_share == pytest.approx(1.0 - sim.skipped_share)
    assert sim.mean_wait_min == 0.0


@pytest.mark.parametrize(("servers", "load"), [(4, 4.0), (10, 8.0)])
def test_full_visits_match_erlang_b(servers: int, load: float) -> None:
    idle, block = 0.95, 1.0 # Four-cycle visits with congestion-independent attempts should offer near-Poisson load of peak_users * (1 - idle).
    cycle = block / (1.0 - idle)
    sim = simulate_peak(
        single_station_table(load),
        np.array([servers]),
        {"squat": block},
        config(
            peak_users=load / (1.0 - idle),
            mean_floor_minutes=4 * cycle,
            idle_share=idle,
            patience_min=0.0,
            warmup_min=3 * cycle,
            measure_min=8000.0,
        ),
    )
    assert sim.skipped_share == pytest.approx(erlang_b(servers, load), abs=0.03)


@pytest.mark.parametrize(("utilization", "cv"), [(0.6, 0.5), (0.5, 0.25)])
def test_unlimited_patience_waits_match_pollaczek_khinchine(utilization: float, cv: float) -> None:
    block = 1.0 # For an M/G/1 queue, mean wait is rho * (1 + cv^2) / (2 * (1 - rho)) blocks.
    sim = simulate_peak(
        single_station_table(utilization),
        np.array([1]),
        {"squat": block},
        one_block_visits(
            utilization / block,
            patience_min=math.inf,
            block_minutes_cv=cv,
            warmup_min=200.0,
            measure_min=20_000.0,
        ),
    )
    expected = utilization * (1.0 + cv**2) / (2.0 * (1.0 - utilization)) * block
    assert sim.skipped_share == 0.0
    assert sim.mean_wait_min == pytest.approx(expected, rel=0.1)


def test_unlimited_patience_waits_match_erlang_c() -> None:
    servers, load, block = 3, 2.1, 1.0 # Three stations and exponential blocks (cv 1): an M/M/3 queue, mean wait C(c, a) / (c - a).
    sim = simulate_peak(
        single_station_table(load),
        np.array([servers]),
        {"squat": block},
        one_block_visits(
            load / block,
            patience_min=math.inf,
            block_minutes_cv=1.0,
            warmup_min=200.0,
            measure_min=20_000.0,
        ),
    )
    expected = erlang_c(servers, load) / (servers - load) * block
    assert sim.mean_wait_min == pytest.approx(expected, rel=0.1)


def test_patience_turns_skips_into_waits() -> None:
    table = route_table( # Both routes are equally good and scarce; waiting should rescue skipped blocks without exceeding patience.
        {"hack_squat": 1, "goblet_area": 1},
        [("squat", 2.0, [(1.0, ["hack_squat"]), (1.0, ["goblet_area"])])],
    )
    units, blocks, patience = np.array([1, 1]), {"squat": 1.0}, 1.0
    impatient = simulate_peak(table, units, blocks, one_block_visits(2.0, measure_min=3000.0))
    patient = simulate_peak(table, units, blocks, one_block_visits(2.0, measure_min=3000.0, patience_min=patience))
    assert impatient.skipped_share == pytest.approx(erlang_b(2, 2.0), abs=0.03)
    assert patient.skipped_share < impatient.skipped_share - 0.1
    assert patient.first_choice_share > impatient.first_choice_share
    assert 0.0 < patient.mean_wait_min <= patient.p90_wait_min <= patience
    assert impatient.mean_wait_min == 0.0


def test_timeout_takes_a_freed_substitute_or_skips_and_records_the_patience() -> None:
    table = route_table( # Check immediate service, a free substitute, timeout, a released first choice, and substitution when patience expires.
        {"hack_squat": 1, "goblet_area": 1},
        [("squat", 2.0, [(1.0, ["hack_squat"]), (0.5, ["goblet_area"])])],
    )
    run = staged_run(
        table,
        [1, 1],
        {"squat": 10.0},
        scripted(patience_min=3.0, measure_min=40.0),
        attempts=[0.0, 1.0, 5.0, 9.0, 10.5],
    )
    run.tolerance = repeat(0.0) # every member accepts the substitute: isolate the queueing
    run._advance()
    sim = run._result()
    assert run.waits == [0.0, 0.0, 3.0, 1.0, 3.0]
    assert (sim.first_choice_share, sim.substituted_share, sim.skipped_share) == pytest.approx((0.4, 0.4, 0.2))
    assert (sim.mean_wait_min, sim.p90_wait_min) == pytest.approx((1.4, 3.0))
    assert sim.utilization == pytest.approx({"hack_squat": 0.5, "goblet_area": 0.5})


def test_freed_stations_go_to_the_longest_waiting_member() -> None:
    table = route_table( # The older bench-only request goes first; the later press request must wait without holding the free dumbbells.
        {"dumbbells": 1, "bench": 1},
        [("db_press", 1.0, [(1.0, ["dumbbells", "bench"])]), ("step_up", 1.0, [(1.0, ["bench"])])],
    )
    run = staged_run(
        table,
        [1, 1],
        {"db_press": 6.0, "step_up": 5.0},
        scripted(patience_min=10.0, measure_min=30.0),
        attempts=[0.0, 1.0, 2.0],
    )
    run.uniform = iter([0.2, 0.8, 0.2]) # Presses are 5/11 of blocks (1 Erlang over 6 minutes against 1 over 5), so these uniforms pick press, step-up, press.
    run._advance()
    sim = run._result()
    assert run.waits == [0.0, 5.0, 9.0]
    assert sim.first_choice_share == 1.0
    assert sim.utilization == pytest.approx({"dumbbells": 12.0 / 30.0, "bench": 17.0 / 30.0})


def test_two_station_route_needs_both_types_free() -> None:
    table = route_table( # A press starts only when both bench and dumbbells are free; waiting users must never reserve one resource.
        {"dumbbells": 1, "bench": 1},
        [("db_press", 6.0, [(1.0, ["dumbbells", "bench"])]), ("db_curl", 4.0, [(1.0, ["dumbbells"])])],
    )
    blocks = {"db_press": 6.0, "db_curl": 4.0}
    busy_config = config(peak_users=30.0, measure_min=600.0)
    ample = simulate_peak(table, np.array([40, 1]), blocks, busy_config)
    floor = _build_floor(table, np.array([4, 1]), blocks, busy_config)
    run = _Run(floor, busy_config)
    scarce = run.execute()
    assert ample.utilization["bench"] > 0.97
    assert scarce.utilization["bench"] < ample.utilization["bench"] - 0.05
    assert scarce.utilization["dumbbells"] > 0.9
    assert min(ample.mean_wait_min, scarce.mean_wait_min) > 0.0

    held = np.zeros(2, dtype=np.int64) # Station bookkeeping: nothing leaked or double-booked when the run stops mid-block.
    for route in run.holding:
        if route != _IDLE:
            for r, n in floor.route_slots[route]:
                held[r] += n
    assert (np.array(run.free) >= 0).all()
    assert (np.array(run.free) + held == np.array(floor.servers)).all()


def test_ample_capacity_serves_every_block_first_choice_without_waiting() -> None:
    table = route_table(
        {"rack": 1, "bench": 1, "dumbbells": 2, "treadmill": 1},
        [
            ("squat", 6.0, [(1.0, ["rack"])]),
            ("db_press", 5.0, [(1.0, ["dumbbells", "bench"]), (0.6, ["dumbbells"])]),
            ("run", 19.0, [(1.0, ["treadmill"])]),
        ],
    )
    sim = simulate_peak(
        table,
        np.array([40, 40, 40, 80]),
        {"squat": 8.0, "db_press": 6.0, "run": 25.0},
        config(peak_users=40.0),
    )
    assert sim.exercise_blocks > 100
    assert sim.first_choice_share == 1.0
    assert sim.substituted_share == sim.skipped_share == 0.0
    assert sim.mean_wait_min == sim.p90_wait_min == 0.0


def test_offered_load_and_floor_population_match_the_demand_model() -> None:
    peak, idle, measure = 120.0, 0.25, 6000.0 # Spare capacity exposes offered load directly: station time must equal peak_users * (1 - idle_share), split by exercise.
    shares = {"squat": 0.3, "row": 0.25, "bike": 0.3, "run": 0.15}
    blocks = {"squat": 7.0, "row": 9.0, "bike": 25.0, "run": 30.0}
    offered = {eid: peak * (1.0 - idle) * share for eid, share in shares.items()}
    table = route_table(
        {f"{eid}_station": 1 for eid in shares},
        [(eid, offered[eid], [(1.0, [f"{eid}_station"])]) for eid in shares],
    )
    units = np.array([int(3 * offered[eid]) + 15 for eid in shares])
    sim = simulate_peak(table, units, blocks, config(peak_users=peak, idle_share=idle, measure_min=measure))
    busy = {eid: sim.utilization[f"{eid}_station"] * units[i] for i, eid in enumerate(shares)}
    assert sum(busy.values()) == pytest.approx(sum(offered.values()), rel=0.03)
    for eid in shares:
        assert busy[eid] == pytest.approx(offered[eid], rel=0.08)
    starts = sum(offered[eid] / blocks[eid] for eid in shares) * measure # Little's law for blocks: starts per minute = busy stations / block length.
    assert sim.exercise_blocks == pytest.approx(starts, rel=0.03)
    assert sim.visits / measure == pytest.approx(peak / 60.0, rel=0.03) # Little's law for the floor: arrivals per minute x mean visit = peak users.


def test_seeded_floor_opens_the_window_at_the_peak_population() -> None:
    peak = 300.0 # With no warm-up the window opens on the seeded floor: about peak_users members at once, not just the ten or so who arrive in its first two minutes.
    sim = simulate_peak(
        single_station_table(1.0),
        np.array([400]),
        {"squat": 5.0},
        config(peak_users=peak, warmup_min=0.0, measure_min=2.0),
    )
    assert 0.85 * peak <= sim.peak_concurrent_users <= 1.2 * peak


def test_busy_preferred_route_sends_members_to_the_substitute() -> None:
    load = 2.0 # The single preferred station is an M/G/1/1 loss system: a member finds it busy with probability B(1, a) = a / (1 + a). Half of them (relative fit 0.5) accept the always-free substitute; the rest skip the block.
    table = route_table(
        {"hack_squat": 1, "goblet_area": 1},
        [("squat", load, [(1.0, ["hack_squat"]), (0.5, ["goblet_area"])])],
    )
    sim = simulate_peak(table, np.array([1, 50]), {"squat": 1.0}, one_block_visits(load, measure_min=4000.0))
    assert sim.substituted_share == pytest.approx(0.5 * erlang_b(1, load), abs=0.02)
    assert sim.skipped_share == pytest.approx(0.5 * erlang_b(1, load), abs=0.02)


def test_missing_preferred_equipment_counts_as_substitution() -> None:
    table = route_table( # Without a hack squat, squats move to the goblet area only as willingly as it fits (0.5): the member did not get the station they wanted, whether it is busy or was never bought.
        {"hack_squat": 1, "goblet_area": 1},
        [("squat", 2.0, [(1.0, ["hack_squat"]), (0.5, ["goblet_area"])])],
    )
    sim = simulate_peak(table, np.array([0, 50]), {"squat": 1.0}, one_block_visits(2.0, measure_min=2000.0))
    assert sim.substituted_share == pytest.approx(0.5, abs=0.03)
    assert sim.skipped_share == pytest.approx(0.5, abs=0.03)
    assert sim.first_choice_share == 0.0
    assert set(sim.utilization) == {"goblet_area"}


def test_equipment_left_out_of_the_table_still_counts_as_the_first_choice() -> None:
    table = replace( # The same gym with the hack squat left out of the plan altogether (an exclusion, or too tall for the ceiling): the table no longer holds it, but its reference quality does.
        route_table({"goblet_area": 1}, [("squat", 2.0, [(0.5, ["goblet_area"])])]),
        best_quality=np.array([1.0]),
    )
    sim = simulate_peak(table, np.array([50]), {"squat": 1.0}, one_block_visits(2.0, measure_min=2000.0))
    assert sim.substituted_share == pytest.approx(0.5, abs=0.03)
    assert sim.skipped_share == pytest.approx(0.5, abs=0.03)
    assert sim.first_choice_share == 0.0


def test_an_equally_good_route_is_still_first_choice() -> None:
    table = route_table( # A squat rack serves a back squat as well as a power rack (both quality 1), so a plan with only squat racks is no compromise; the leg press (0.6) is, when they are busy.
        {"power_rack": 1, "squat_rack": 1, "leg_press": 1},
        [("back_squat", 2.0, [(1.0, ["power_rack"]), (1.0, ["squat_rack"]), (0.6, ["leg_press"])],)],
    )
    blocks = {"back_squat": 1.0}
    ample = simulate_peak(table, np.array([0, 50, 50]), blocks, one_block_visits(2.0))
    one_rack = simulate_peak(table, np.array([0, 1, 50]), blocks, one_block_visits(2.0, measure_min=4000.0))
    assert ample.first_choice_share == 1.0
    assert one_rack.substituted_share == pytest.approx(0.6 * erlang_b(1, 2.0), abs=0.02) # Members who find the one rack busy take the leg press as often as it fits (0.6).


def test_no_equipment_skips_every_block() -> None:
    table = route_table(
        {"rack": 1, "bench": 1},
        [("squat", 3.0, [(1.0, ["rack"])]), ("bench_press", 3.0, [(1.0, ["rack", "bench"])])],
    )
    sim = simulate_peak(table, np.array([0, 0]), {"squat": 8.0, "bench_press": 8.0}, config(idle_share=0.0))
    assert sim.exercise_blocks > 100
    assert sim.skipped_share == 1.0
    assert sim.mean_wait_min == 0.0 # nobody waits for equipment that is not there
    assert sim.utilization == {}


def test_unservable_exercises_are_skipped_in_proportion_to_their_blocks() -> None:
    table = route_table( # Missing racks and unroutable exercises are always skipped; equal block lengths make the skipped load share exact.
        {"rack": 1, "bike": 1},
        [("squat", 2.0, [(1.0, ["rack"])]), ("ride", 4.0, [(1.0, ["bike"])])],
        unroutable_load=3.0,
    )
    sim = simulate_peak(table, np.array([0, 60]), {"squat": 8.0, "ride": 8.0}, config(measure_min=3000.0))
    assert sim.skipped_share == pytest.approx(5.0 / 9.0, abs=0.02)
    assert sim.first_choice_share == pytest.approx(4.0 / 9.0, abs=0.02)


def test_unroutable_exercises_are_skipped_at_their_own_block_length() -> None:
    peak, idle = 100.0, 0.25 # Unavailable and unroutable cardio must produce the same skips; long cardio blocks make 35% of load about 12% of blocks.
    active = peak * (1.0 - idle)
    strength = {"squat": (0.2, 8.0), "bench_press": (0.2, 7.0), "row": (0.15, 6.0)}
    strength |= {"curl": (0.1, 5.0)}
    cardio = {"run": (0.2, 25.0), "bike": (0.15, 30.0)}
    every = strength | cardio
    blocks = {eid: block for eid, (_, block) in every.items()}
    settings = config(peak_users=peak, idle_share=idle, measure_min=3000.0)

    routable = route_table(
        {f"{eid}_station": 1 for eid in every},
        [(eid, active * share, [(1.0, [f"{eid}_station"])]) for eid, (share, _) in every.items()],
    )
    unbought = simulate_peak(routable, np.array([40, 40, 40, 40, 0, 0]), blocks, settings)

    cardio_load = {eid: active * share for eid, (share, _) in cardio.items()}
    strength_only = route_table(
        {f"{eid}_station": 1 for eid in strength},
        [
            (eid, active * share, [(1.0, [f"{eid}_station"])])
            for eid, (share, _) in strength.items()
        ],
        unroutable_load=sum(cardio_load.values()),
    )
    excluded = simulate_peak(strength_only, np.array([40, 40, 40, 40]), blocks, settings, unroutable=cardio_load)

    frequency = {eid: share / block for eid, (share, block) in every.items()}
    expected = sum(frequency[eid] for eid in cardio) / sum(frequency.values())
    assert excluded.skipped_share == pytest.approx(unbought.skipped_share, abs=0.005)
    assert excluded.skipped_share == pytest.approx(expected, abs=0.01)
    assert excluded.utilization == pytest.approx(unbought.utilization, rel=0.02)


@pytest.mark.parametrize(
    ("unroutable", "message"),
    [
        ({"run": 1.0}, "add up to"),
        ({"run": 3.0, "squat": 0.0}, "has routes"),
        ({"swim": 3.0}, "block_minutes"),
        ({"run": float("nan")}, "finite"),
    ],
)
def test_unroutable_breakdown_must_match_the_table(
    unroutable: dict[str, float], message: str
) -> None:
    table = route_table({"rack": 1}, [("squat", 2.0, [(1.0, ["rack"])])], unroutable_load=3.0)
    with pytest.raises(ValueError, match=message):
        simulate_peak(table, np.array([2]), {"squat": 8.0, "run": 25.0}, config(), unroutable=unroutable)


def test_zero_peak_users_leaves_the_window_empty() -> None:
    sim = simulate_peak(single_station_table(1.0), np.array([3]), {"squat": 5.0}, config(peak_users=0.0))
    assert (sim.visits, sim.exercise_blocks, sim.peak_concurrent_users) == (0, 0, 0)
    assert sim.first_choice_share == sim.skipped_share == sim.mean_wait_min == 0.0
    assert sim.utilization == {"rack": 0.0}
    assert sim.simulated_minutes == 180.0


def test_window_counts_blocks_started_inside_it_and_clips_station_time() -> None:
    run = staged_run( # Count starts only in minutes 10-30, but include station time overlapping either edge of that window.
        single_station_table(1.0),
        [1],
        {"squat": 10.0},
        scripted(patience_min=0.0, warmup_min=10.0, measure_min=20.0),
        attempts=[3.0, 4.0, 12.0, 27.0],
    )
    run._advance()
    sim = run._result()
    assert sim.exercise_blocks == 2
    assert sim.first_choice_share == sim.skipped_share == 0.5
    assert sim.utilization["rack"] == pytest.approx(6.0 / 20.0)
    assert sim.visits == 2


def test_peak_concurrency_counts_the_window_only() -> None:
    run = staged_run( # Five members train one-minute blocks right at the start and are gone by minute 1.4; inside the window (minutes 10-20) two arrivals overlap from 12.5 to 13.
        single_station_table(1.0),
        [10],
        {"squat": 1.0},
        scripted(warmup_min=10.0, measure_min=10.0),
        attempts=[0.0, 0.1, 0.2, 0.3, 0.4, 12.0, 12.5],
    )
    run._advance()
    sim = run._result()
    assert sim.peak_concurrent_users == 2
    assert sim.visits == 2


def test_peak_concurrency_matches_a_brute_force_count() -> None:
    rng = np.random.default_rng(4) # Whole-minute times make hand-overs common: someone leaving as someone else arrives is not an overlap, because a stay covers [arrival, departure).
    arrival = rng.integers(0, 60, 400).astype(np.float64)
    departure = arrival + rng.integers(1, 15, 400)
    departure[::25] = np.inf # still on the floor when the run ends
    start, end = 20.0, 45.0
    moments = [start, *arrival[(arrival > start) & (arrival < end)].tolist()] # The head count only rises at arrivals, so its maximum is at the start or an arrival.
    expected = max(int(np.count_nonzero((arrival <= t) & (departure > t))) for t in moments)
    assert _peak_concurrency(arrival, departure, start, end) == expected


def test_same_seed_reproduces_the_run() -> None:
    table, units, blocks = design_scale_plan(seed=3, capacity=0.8)
    first = simulate_peak(table, units, blocks, config(peak_users=400.0, seed=11))
    again = simulate_peak(table, units, blocks, config(peak_users=400.0, seed=11))
    numpy_seed = simulate_peak(table, units, blocks, config(peak_users=400.0, seed=np.int64(11)))
    other = simulate_peak(table, units, blocks, config(peak_users=400.0, seed=12))
    assert first == again == numpy_seed
    assert first != other
    assert first.seed == 11


def test_utilization_obeys_littles_law() -> None:
    servers, load, block, measure = 3, 3.0, 2.0, 6000.0 # L = lambda W per station type: average busy stations = served blocks per minute x mean block length, and with no waiting that is the Erlang carried load a (1 - B(c, a)).
    sim = simulate_peak(
        single_station_table(load),
        np.array([servers]),
        {"squat": block},
        one_block_visits(load / block, measure_min=measure),
    )
    busy = sim.utilization["rack"] * servers
    assert 0.0 < sim.utilization["rack"] < 1.0
    assert busy == pytest.approx(served_blocks(sim) / measure * block, rel=0.03)
    assert busy == pytest.approx(load * (1.0 - erlang_b(servers, load)), rel=0.03)


def test_design_scale_outputs_are_consistent() -> None:
    table, units, blocks = design_scale_plan(seed=5, capacity=0.6)
    sim = simulate_peak(table, units, blocks, config(peak_users=400.0, mean_floor_minutes=65.0))
    present = {table.equipment_ids[r] for r in np.flatnonzero(units)}
    assert set(sim.utilization) == present
    assert all(0.0 <= u <= 1.0 for u in sim.utilization.values())
    shares = sim.first_choice_share + sim.substituted_share + sim.skipped_share
    assert shares == pytest.approx(1.0)
    assert sim.substituted_share > 0.0 and sim.skipped_share > 0.0
    assert 0.0 < sim.mean_wait_min <= sim.p90_wait_min <= 3.0
    assert sim.visits == pytest.approx(400.0 / 65.0 * 120.0, rel=0.15)
    assert 400 <= sim.peak_concurrent_users <= 520


def test_runtime_at_design_scale() -> None:
    table, units, blocks = design_scale_plan(seed=1, capacity=0.8)
    started = time.perf_counter()
    sim = simulate_peak(table, units, blocks, config(peak_users=400.0, mean_floor_minutes=65.0))
    elapsed = time.perf_counter() - started
    assert sim.simulated_minutes == 180.0
    assert sim.exercise_blocks > 2000
    assert elapsed < 2.0 # typically ~0.02 s; the budget inside a plan request is 0.5 s


def test_long_queues_stay_cheap() -> None:
    table = route_table( # Hundreds of members queue for dumbbells + a bench while one-minute step-ups churn the bench. Only queue heads are examined when stations free up, so a run costs about the same per block however long the queues grow.
        {"dumbbells": 1, "bench": 1},
        [
            ("db_press", 100.0, [(1.0, ["dumbbells", "bench"])]),
            ("step_up", 100.0, [(1.0, ["bench"])]),
            ("curl", 100.0, [(1.0, ["dumbbells"])]),
        ],
    )
    started = time.perf_counter()
    sim = simulate_peak(
        table,
        np.array([2, 40]),
        {"db_press": 6.0, "step_up": 1.0, "curl": 6.0},
        config(peak_users=2000.0, patience_min=120.0),
    )
    elapsed = time.perf_counter() - started
    assert sim.mean_wait_min > 30.0 # the queues really were long
    assert elapsed < 0.5 # ~0.04 s; rescanning whole queues on every release took ~1.6 s


@pytest.mark.parametrize(
    "frequency",
    [
        np.array([0.3, 0.25, 0.2, 0.15, 0.1]),
        np.concatenate([[0.4], np.full(60, 0.01)]),
        np.concatenate([[0.49], np.full(51, 0.01)]),
    ],
    ids=["spread", "top-40%", "top-49%"],
)
def test_no_repeat_picks_keep_the_target_mix(frequency: NDArray[np.float64]) -> None:
    weights = no_repeat_weights(frequency) # Past about a third of all blocks the top exercise needs the larger root of q (1 - q) = c p; small roots alone cannot sum to one.
    assert weights is not None
    stationary = weights * (1.0 - weights) # Stationary distribution of the no-repeat chain is proportional to q (1 - q).
    np.testing.assert_allclose(stationary / stationary.sum(), frequency, atol=1e-9)

    mix = ExerciseMix.from_frequency(frequency)
    uniform = iter(np.random.default_rng(0).random(100_000).tolist())
    picks, previous = [], -1
    for _ in range(100_000):
        previous = mix.pick(previous, uniform)
        picks.append(previous)
    sequence = np.array(picks)
    assert not np.any(sequence[1:] == sequence[:-1])
    shares = np.bincount(sequence, minlength=frequency.size) / sequence.size
    np.testing.assert_allclose(shares, frequency, atol=0.006)


def test_dominant_exercise_allows_repeats() -> None:
    assert no_repeat_weights(np.array([0.7, 0.2, 0.1])) is None # No repeat-free sequence gives one exercise half of all blocks or more.
    assert no_repeat_weights(np.array([0.5, 0.25, 0.25])) is None
    assert no_repeat_weights(np.array([1.0])) is None


@pytest.mark.parametrize(
    ("units", "blocks", "overrides"),
    [
        (np.array([1, 1]), {"squat": 5.0}, {}),
        (np.array([-1]), {"squat": 5.0}, {}),
        (np.array([1.5]), {"squat": 5.0}, {}),
        (np.array([1]), {}, {}),
        (np.array([1]), {"squat": math.inf}, {}),
        (np.array([1]), {"squat": 5.0}, {"idle_share": 1.0}),
        (np.array([1]), {"squat": 5.0}, {"mean_floor_minutes": 0.0}),
        (np.array([1]), {"squat": 5.0}, {"measure_min": 0.0}),
        (np.array([1]), {"squat": 5.0}, {"peak_users": math.nan}),
        (np.array([1]), {"squat": 5.0}, {"peak_users": math.inf}),
        (np.array([1]), {"squat": 5.0}, {"warmup_min": math.inf}),
        (np.array([1]), {"squat": 5.0}, {"measure_min": math.inf}),
        (np.array([1]), {"squat": 5.0}, {"block_minutes_cv": math.inf}),
        (np.array([1]), {"squat": 5.0}, {"floor_minutes_cv": math.inf}),
        (np.array([1]), {"squat": 5.0}, {"block_minutes_cv": 1e6}),
        (np.array([1]), {"squat": 5.0}, {"patience_min": math.nan}),
    ],
)
def test_invalid_inputs_are_rejected(
    units: NDArray[np.int64], blocks: dict[str, float], overrides: dict[str, float]
) -> None:
    with pytest.raises(ValueError):
        simulate_peak(single_station_table(1.0), units, blocks, config(**overrides))


@pytest.mark.parametrize("load", [-1.0, math.nan, math.inf])
def test_invalid_loads_are_rejected(load: float) -> None:
    with pytest.raises(ValueError, match="load"):
        simulate_peak(single_station_table(load), np.array([1]), {"squat": 5.0}, config())


def test_runaway_runs_are_refused() -> None:
    with pytest.raises(ValueError, match="exercise blocks"): # Microsecond blocks would mean billions of events: refused up front, not left to hang.
        simulate_peak(single_station_table(1.0), np.array([1]), {"squat": 1e-6}, config())


def test_simulation_agrees_with_the_selection_model_on_substitution() -> None:
    from gymplanner.selection.evaluator import evaluate

    load = 2.0 # Single-block visits without waiting should match the loss model, including rejected substitutes.
    table = route_table(
        {"hack_squat": 1, "goblet_area": 1},
        [("squat", load, [(1.0, ["hack_squat"]), (0.5, ["goblet_area"])])],
    )
    units = np.array([1, 3])
    sim = simulate_peak(table, units, {"squat": 1.0}, one_block_visits(load, measure_min=6000.0))
    model = evaluate(table, units, tolerance=1e-10, max_iterations=2_000)
    assert 1.0 - sim.skipped_share == pytest.approx(model.served[0] / load, abs=0.02)
