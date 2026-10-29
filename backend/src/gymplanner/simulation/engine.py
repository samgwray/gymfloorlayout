"""Design-hour discrete-event simulation of members training on a planned floor.

The selection objective scores plans analytically: Erlang loss blocking per equipment type,
coupled by the reduced-load approximation, with blocked demand lost on the spot. This replays
the same demand member by member on the chosen equipment, which checks those estimates and
measures what the formulas leave out: waiting, settling for a substitute, and which stations
saturate first.

* Members arrive as a Poisson process at ``peak_users / mean_floor_minutes`` per minute. The
  floor starts in steady state (a Poisson number of members part-way through their visits),
  so the warm-up only has to settle station occupancy.
* A visit is a run of cycles: pick an exercise (in proportion to block frequency, offered
  Erlangs / block length, avoiding back-to-back repeats), train a gamma-distributed block on
  the best free route the plan can perform, then idle for an exponential gap sized so idle
  time is ``idle_share`` of the visit. A member whose floor time is up finishes the cycle in
  progress and leaves.
* A block is first choice when its route is as good as the best way to do the exercise on
  the equipment the gym's format offers (``RouteTable.reference_quality``). A lesser route is a
  substitution, whether the better one was busy, is not in the plan or was left out of it, so
  a budget plan's compromises show up here and in route quality.
* Members settle for a lesser route only as far as it fits: for each block they draw a
  tolerance and accept routes whose quality, relative to the best way to do the exercise, is
  at least that draw. The chance of accepting a route is therefore its relative quality, the
  same substitution willingness the selection model uses. A member with no acceptable route
  in the plan skips the block.
* When every acceptable route is busy the member queues, first come first served, for the best
  route the plan can perform for up to ``patience_min``, then takes whichever acceptable route
  is free or skips the block.
* A skipped block still takes its time (bodyweight work, a drink) so congestion lowers the
  share of demand served instead of inflating demand with retries. Demand that no allowed
  equipment can serve is replayed as blocks that are always skipped. Offered load therefore
  matches the selection model's, less only the time members spend waiting.
"""

from __future__ import annotations

import heapq
import math
import operator
from collections import defaultdict, deque
from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass
from itertools import repeat

import numpy as np
from numpy.typing import NDArray

from gymplanner.selection.evaluator import RouteTable
from gymplanner.simulation.behavior import (
    ExerciseMix,
    VisitModel,
    gamma_draws,
    idle_gap_minutes,
    residual_draws,
    visit_model,
)
from gymplanner.simulation.types import SimulationConfig, SimulationResult

Route = tuple[tuple[int, int], ...]
"""(equipment index, stations occupied) for each equipment type a route ties up."""
Stream = tuple[float, float]
"""(offered Erlangs, block minutes) of demand that no allowed equipment can serve."""

WAIT_PERCENTILE = 90.0
MAX_CV = 4.0
"""Largest coefficient of variation accepted, well above any realistic spread of visit or
block lengths. Far larger ones make gamma draws underflow to zero, and a run of zero-length
blocks with no idle gaps would never advance the clock."""
MAX_EXPECTED_BLOCKS = 2_000_000
"""Runs expected to simulate more blocks than this (several seconds) are refused, not run."""

_RELEASE, _TIMEOUT, _ATTEMPT = 0, 1, 2
"""Event kinds, in the order simultaneous events run: freed stations go to waiting members
before a patience timeout or a newcomer at the same instant can claim them."""
_FIRST, _SUBSTITUTED, _SKIPPED = 0, 1, 2
_IDLE = -1
"""Route id of a member holding no stations."""
_QUALITY_TIE = 1e-9
"""Route qualities this close count as equally good: either is a first choice."""
_DRAW_CHUNK = 4096
_SEED_MODULUS = 1 << 64


def simulate_peak(
    table: RouteTable,
    units: NDArray[np.int64],
    block_minutes: Mapping[str, float],
    config: SimulationConfig,
    *,
    unroutable: Mapping[str, float] | None = None,
) -> SimulationResult:
    """Simulate the design hour on ``units`` of each equipment type in ``table``.

    Metrics cover exercise blocks started or skipped in the measured window that follows the
    warm-up: ``exercise_blocks`` counts both, so the first-choice, substituted and skipped
    shares sum to one, and waits include the zero waits of blocks that started right away.
    Results are reproducible for a given ``config.seed``.

    ``unroutable`` breaks ``table.unroutable_load`` down by exercise (offered Erlangs of each
    exercise that no allowed equipment can serve), so each is skipped as often as its own
    block length implies. Without it that load is replayed at the routable mix's mean block
    length, which miscounts skipped blocks when the missing exercises run longer or shorter
    than the rest (cardio, for one).
    """
    _check_config(config)
    floor = _build_floor(table, units, block_minutes, config, unroutable)
    _check_workload(floor, config)
    return _Run(floor, config).execute()


@dataclass(frozen=True)
class _Floor:
    """The plan as the event loop sees it, flattened into plain Python sequences."""

    equipment_ids: tuple[str, ...]
    units: tuple[int, ...]
    servers: tuple[int, ...]
    route_slots: tuple[Route, ...]
    """Every distinct route the plan can perform, indexed by route id."""
    options: tuple[tuple[int, ...], ...]
    """Per pickable exercise: ids of the routes the plan can perform, best first."""
    outcomes: tuple[tuple[int, ...], ...]
    """Per pickable exercise and option: first choice or substituted."""
    acceptance: tuple[tuple[float, ...], ...]
    """Per pickable exercise and option: the route's quality relative to the exercise's best
    route in the table, i.e. the share of members willing to use it."""
    contenders: tuple[tuple[int, ...], ...]
    """Per route id: the routes members queue for that share an equipment type with it."""
    block_minutes: tuple[float, ...]
    gap_minutes: tuple[float, ...]
    mix: ExerciseMix
    visit: VisitModel


def _check_config(config: SimulationConfig) -> None:
    settings = ( # Infinite patience means waiting as long as it takes; every other setting must be finite.
        config.peak_users,
        config.mean_floor_minutes,
        config.floor_minutes_cv,
        config.block_minutes_cv,
        config.idle_share,
        config.warmup_min,
        config.measure_min,
    )
    if not all(math.isfinite(value) for value in settings):
        raise ValueError("simulation settings must be finite (only patience_min may be infinite)")
    if config.peak_users < 0:
        raise ValueError("peak_users must be non-negative")
    if config.mean_floor_minutes <= 0:
        raise ValueError("mean_floor_minutes must be positive")
    if not (0 <= config.floor_minutes_cv <= MAX_CV and 0 <= config.block_minutes_cv <= MAX_CV):
        raise ValueError(f"coefficients of variation must be between 0 and {MAX_CV:g}")
    if not 0 <= config.idle_share < 1:
        raise ValueError("idle_share must be in [0, 1)")
    if not (config.patience_min >= 0 and config.warmup_min >= 0): # Written as "not x >= 0" so NaN patience is rejected too.
        raise ValueError("patience_min and warmup_min must be non-negative")
    if config.measure_min <= 0:
        raise ValueError("measure_min must be positive")


def _check_workload(floor: _Floor, config: SimulationConfig) -> None:
    """Refuse runs that would take minutes, such as near-zero block lengths, up front."""
    horizon = config.warmup_min + config.measure_min
    blocks = config.peak_users * (1.0 + horizon / config.mean_floor_minutes) # Everyone on the floor (seeded or arriving) makes at least one attempt; beyond that the floor population of about peak_users starts a cycle every cycle_minutes.
    if floor.mix.size:
        blocks += config.peak_users * horizon / floor.visit.cycle_minutes
    if blocks > MAX_EXPECTED_BLOCKS:
        raise ValueError(
            f"the run would simulate about {blocks:,.0f} exercise blocks (limit "
            f"{MAX_EXPECTED_BLOCKS:,}); check block lengths, peak_users and the horizon"
        )


def _build_floor(
    table: RouteTable,
    units: NDArray[np.int64],
    block_minutes: Mapping[str, float],
    config: SimulationConfig,
    unroutable: Mapping[str, float] | None = None,
) -> _Floor:
    counts = _unit_counts(table, units)
    servers = counts * table.stations
    load = np.asarray(table.load, dtype=np.float64)
    if not (np.isfinite(load).all() and (load >= 0).all()):
        raise ValueError("exercise loads must be finite and non-negative")
    if not (math.isfinite(table.unroutable_load) and table.unroutable_load >= 0):
        raise ValueError("unroutable_load must be finite and non-negative")

    route_ids: dict[Route, int] = {}
    options: list[tuple[int, ...]] = []
    outcomes: list[tuple[int, ...]] = []
    acceptance: list[tuple[float, ...]] = []
    loads: list[float] = []
    minutes: list[float] = []
    missing: list[str] = []
    for e, exercise_id in enumerate(table.exercise_ids):
        if load[e] == 0:
            continue
        block = _block_length(block_minutes, exercise_id)
        if block is None:
            missing.append(exercise_id)
            continue
        performable = _performable_routes(table, e, servers)
        options.append(tuple(route_ids.setdefault(route, len(route_ids)) for route, _ in performable))
        outcomes.append(tuple(outcome for _, outcome in performable))
        acceptance.append(_acceptance(table, e, servers))
        loads.append(float(load[e]))
        minutes.append(block)
    if unroutable is None:
        skipped = _pooled_unroutable(table.unroutable_load, loads, minutes, block_minutes)
    else:
        skipped = _itemized_unroutable(table, unroutable, block_minutes, missing)
    if missing:
        raise ValueError("block_minutes needs a finite positive length for: " + ", ".join(missing))
    for stream_load, stream_block in skipped:
        options.append(())
        outcomes.append(())
        acceptance.append(())
        loads.append(stream_load)
        minutes.append(stream_block)

    route_slots = tuple(route_ids) # insertion order is id order
    block_array = np.array(minutes, dtype=np.float64)
    frequency = np.array(loads, dtype=np.float64) / block_array
    return _Floor(
        equipment_ids=table.equipment_ids,
        units=tuple(counts.tolist()),
        servers=tuple(servers.tolist()),
        route_slots=route_slots,
        options=tuple(options),
        outcomes=tuple(outcomes),
        acceptance=tuple(acceptance),
        contenders=_contenders(route_slots, options),
        block_minutes=tuple(minutes),
        gap_minutes=tuple(idle_gap_minutes(block_array, config.idle_share).tolist()),
        mix=ExerciseMix.from_frequency(frequency),
        visit=visit_model(
            frequency,
            block_array,
            config.idle_share,
            config.block_minutes_cv,
            config.mean_floor_minutes,
            config.floor_minutes_cv,
        ),
    )


def _unit_counts(table: RouteTable, units: NDArray[np.int64]) -> NDArray[np.int64]:
    counts = np.asarray(units)
    if counts.shape != (table.n_equipment,):
        raise ValueError(f"expected {table.n_equipment} unit counts, got shape {counts.shape}")
    if not (
        np.isfinite(counts).all() and (counts >= 0).all() and (counts == np.floor(counts)).all()
    ):
        raise ValueError("unit counts must be non-negative whole numbers")
    return counts.astype(np.int64)


def _block_length(block_minutes: Mapping[str, float], exercise_id: str) -> float | None:
    block = block_minutes.get(exercise_id)
    if block is None or not (math.isfinite(block) and block > 0):
        return None
    return float(block)


def _performable_routes(
    table: RouteTable, exercise: int, servers: NDArray[np.int64]
) -> list[tuple[Route, int]]:
    """Routes of ``exercise`` the plan has enough stations for, best first, with the outcome
    each one counts as: first choice when it is as good as the exercise's reference route."""
    quality = table.route_quality[exercise]
    best = float(table.reference_quality[exercise])
    found: list[tuple[Route, int]] = []
    for k in sorted(np.flatnonzero(quality > 0).tolist(), key=lambda k: -quality[k]): # A stable sort keeps the table's order (fewer stations first) among equal qualities.
        slots = table.route_res[exercise, k]
        types, needed = np.unique(slots[slots >= 0], return_counts=True)
        if types.size and bool(np.all(servers[types] >= needed)):
            route = tuple(zip(types.tolist(), needed.tolist(), strict=True))
            outcome = _FIRST if quality[k] >= best - _QUALITY_TIE else _SUBSTITUTED
            found.append((route, outcome))
    return found


def _acceptance(table: RouteTable, exercise: int, servers: NDArray[np.int64]) -> tuple[float, ...]:
    """Share of members willing to use each performable route (same order as the options).

    A route's acceptance is its quality relative to the exercise's reference route, whether or
    not the plan has that route, matching the selection model's attrition.
    """
    quality = table.route_quality[exercise]
    best = float(table.reference_quality[exercise])
    if best <= 0:
        return ()
    shares: list[float] = []
    for k in sorted(np.flatnonzero(quality > 0).tolist(), key=lambda k: -quality[k]):
        slots = table.route_res[exercise, k]
        types, needed = np.unique(slots[slots >= 0], return_counts=True)
        if types.size and bool(np.all(servers[types] >= needed)):
            shares.append(float(quality[k]) / best)
    return tuple(shares)


def _pooled_unroutable(
    unroutable_load: float,
    loads: list[float],
    minutes: list[float],
    block_minutes: Mapping[str, float],
) -> list[Stream]:
    """Unroutable load as one stream, at the routable mix's mean block length.

    Only an approximation for callers that cannot say which exercises the load belongs to;
    with nothing routable, the mean of the lengths given stands in.
    """
    if unroutable_load == 0:
        return []
    if loads:
        block = sum(loads) / sum(load / b for load, b in zip(loads, minutes, strict=True))
        return [(unroutable_load, block)]
    known = [b for b in block_minutes.values() if math.isfinite(b) and b > 0]
    if not known:
        raise ValueError("block_minutes has no positive length to replay unroutable demand with")
    return [(unroutable_load, sum(known) / len(known))]


def _itemized_unroutable(
    table: RouteTable,
    unroutable: Mapping[str, float],
    block_minutes: Mapping[str, float],
    missing: list[str],
) -> list[Stream]:
    """One always-skipped stream per unroutable exercise, at that exercise's block length.

    The breakdown must add up to the table's ``unroutable_load`` so the run replays the demand
    the selection model scored. Exercises without a block length are appended to ``missing``.
    """
    routed = set(table.exercise_ids)
    streams: list[Stream] = []
    total = 0.0
    for exercise_id, value in unroutable.items():
        load = float(value)
        if not (math.isfinite(load) and load >= 0):
            raise ValueError(f"unroutable load of {exercise_id} must be finite and non-negative")
        if exercise_id in routed:
            raise ValueError(f"{exercise_id} has routes in the table, so it cannot be unroutable")
        if load == 0:
            continue
        total += load
        block = _block_length(block_minutes, exercise_id)
        if block is None:
            missing.append(exercise_id)
        else:
            streams.append((load, block))
    if not math.isclose(total, table.unroutable_load, rel_tol=1e-6, abs_tol=1e-9):
        raise ValueError(
            f"unroutable loads add up to {total:.6g} Erlangs, but the route table has "
            f"{table.unroutable_load:.6g}"
        )
    return streams


def _contenders(
    route_slots: tuple[Route, ...], options: list[tuple[int, ...]]
) -> tuple[tuple[int, ...], ...]:
    """For each route, the queued-for routes (each exercise's best) that share a type with it."""
    queued_by_type: dict[int, set[int]] = defaultdict(set)
    for choices in options:
        if choices:
            for r, _ in route_slots[choices[0]]:
                queued_by_type[r].add(choices[0])
    return tuple(tuple(sorted({q for r, _ in slots for q in queued_by_type.get(r, ())})) for slots in route_slots)


def _stream(draw: Callable[[int], NDArray[np.float64]]) -> Iterator[float]:
    """Endless variates from a numpy sampler, drawn in chunks so each costs one list step."""
    while True:
        yield from draw(_DRAW_CHUNK).tolist()


class _Run:
    """Mutable state of one simulation: free stations, queues, members and tallies."""

    def __init__(self, floor: _Floor, config: SimulationConfig) -> None:
        self.floor = floor
        self.config = config
        self.warmup = config.warmup_min
        self.end = config.warmup_min + config.measure_min
        self.patience = config.patience_min

        entropy = operator.index(config.seed) % _SEED_MODULUS # Independent streams per purpose, so a change in one kind of draw does not reshuffle the others and two plans simulated with one seed see the same arrivals.
        seeds = np.random.SeedSequence(entropy).spawn(5) # Spawned children depend only on their index, so adding a stream keeps the others.
        self.arrival_rng, pick_rng, block_rng, gap_rng, tolerance_rng = (
            np.random.default_rng(s) for s in seeds
        )
        self.uniform = _stream(lambda n: pick_rng.random(n))
        self.tolerance = _stream(lambda n: tolerance_rng.random(n))
        self.gap_factor = _stream(lambda n: gap_rng.standard_exponential(n))
        self.block_factor: Iterator[float] = repeat(1.0)
        if config.block_minutes_cv > 0:
            shape = 1.0 / config.block_minutes_cv**2
            self.block_factor = _stream(lambda n: block_rng.standard_gamma(shape, n) / shape)

        self.free = list(floor.servers)
        self.busy_minutes = [0.0] * len(floor.servers)
        self.queues: list[deque[tuple[int, int]]] = [deque() for _ in floor.route_slots]
        """Per route id, (wait token, member) of everyone queued for it, oldest first. A
        member who timed out stays in the deque until it reaches the front: their token no
        longer matches, so the entry is dropped then."""
        self.events: list[tuple[float, int, int, int]] = []
        self.sequence = 0
        self.tally = [0, 0, 0]
        self.waits: list[float] = []

        self.n_seeded = 0
        self.arrival: NDArray[np.float64] = np.zeros(0)
        self.deadline: list[float] = []
        self.departure: list[float] = []
        self.last: list[int] = []
        self.holding: list[int] = []
        self.wait_since: list[float] = []
        self.wait_token: list[int] = []
        self.accepted: list[int] = []
        """Per member, how many of the current exercise's options (best first) they accept."""


    def execute(self) -> SimulationResult:
        self._populate()
        self._advance()
        return self._result()

    def _populate(self) -> None:
        """Seed the floor at steady state and add the members who arrive during the run."""
        config, visit, rng = self.config, self.floor.visit, self.arrival_rng
        n_seeded = int(rng.poisson(config.peak_users)) # Seed steady state with Poisson occupancy and length-biased residual stays; overdue members leave after their last cycle.
        planning = rng.random(n_seeded) * config.mean_floor_minutes < visit.planned_minutes
        residual = residual_draws(rng, visit.planned_minutes, visit.cv, n_seeded)
        seeded_left = np.where(planning, residual, 0.0)
        seeded_start = rng.random(n_seeded) * visit.cycle_minutes

        rate = config.peak_users / config.mean_floor_minutes
        n_arrivals = int(rng.poisson(rate * self.end))
        arrive = np.sort(rng.random(n_arrivals) * self.end)
        stay = gamma_draws(rng, visit.planned_minutes, visit.cv, n_arrivals)

        trains = np.concatenate([seeded_start < seeded_left, np.ones(n_arrivals, dtype=bool)]) # Arrivals always complete at least one cycle; seeded members may already be done.
        if self.floor.mix.size == 0:
            trains[:] = False
        self._add_members(
            arrival=np.concatenate([np.zeros(n_seeded), arrive]),
            start=np.concatenate([seeded_start, arrive]),
            deadline=np.concatenate([seeded_left, arrive + stay]),
            trains=trains,
            n_seeded=n_seeded,
        )

    def _add_members(
        self,
        arrival: NDArray[np.float64],
        start: NDArray[np.float64],
        deadline: NDArray[np.float64],
        trains: NDArray[np.bool_],
        n_seeded: int = 0,
    ) -> None:
        """Register every member and schedule the first attempt of those who train.

        Members who never train stay from ``arrival`` to ``max(start, deadline)``. The first
        ``n_seeded`` were already on the floor when the run began, so they are not visits.
        """
        n = arrival.size
        self.n_seeded = n_seeded
        self.arrival = arrival
        self.deadline = deadline.tolist()
        self.departure = np.where(trains, np.inf, np.maximum(start, deadline)).tolist()
        self.last = [-1] * n
        self.holding = [_IDLE] * n
        self.wait_since = [0.0] * n
        self.wait_token = [-1] * n
        self.accepted = [0] * n
        self.events = [(float(start[m]), _ATTEMPT, int(m), int(m)) for m in np.flatnonzero(trains)]
        heapq.heapify(self.events)
        self.sequence = n

    def _advance(self) -> None:
        """Process events in time order until the measured window closes."""
        events, end, wait_token = self.events, self.end, self.wait_token
        while events:
            time, kind, sequence, member = heapq.heappop(events)
            if time >= end:
                break
            if kind == _ATTEMPT:
                self._attempt(member, time)
            elif kind == _RELEASE:
                self._release(member, time)
            elif wait_token[member] == sequence:
                self._give_up(member, time)


    def _attempt(self, member: int, time: float) -> None:
        """Pick the next exercise and take the best free route, else queue or skip."""
        floor = self.floor
        exercise = floor.mix.pick(self.last[member], self.uniform)
        self.last[member] = exercise
        options = floor.options[exercise]
        threshold = next(self.tolerance)
        accepted = sum(1 for share in floor.acceptance[exercise] if share >= threshold)
        self.accepted[member] = accepted
        for option in range(accepted):
            if self._fits(options[option]):
                self._start(member, exercise, option, time, 0.0)
                return
        if accepted == 0 or self.patience <= 0:
            self._skip(member, exercise, time, 0.0)
            return
        token = self._schedule(time + self.patience, _TIMEOUT, member)
        self.wait_since[member] = time
        self.wait_token[member] = token
        self.queues[options[0]].append((token, member))

    def _release(self, member: int, time: float) -> None:
        """A block (on or off the equipment) ends: free its stations, then idle or leave."""
        route = self.holding[member]
        if route != _IDLE:
            self.holding[member] = _IDLE
            free = self.free
            for r, n in self.floor.route_slots[route]:
                free[r] += n
            self._admit(route, time)
        resume = time + self.floor.gap_minutes[self.last[member]] * next(self.gap_factor)
        if resume >= self.deadline[member]:
            self.departure[member] = resume
        else:
            self._schedule(resume, _ATTEMPT, member)

    def _admit(self, released: int, time: float) -> None:
        """Hand freed stations to queued members, longest-waiting first.

        Everyone in one route's queue needs the same stations, so only queue heads can start,
        and only on routes that share a type with the freed one. The head that has waited
        longest among those whose route fits goes first, until none fits. A member whose
        route also needs a type that is still busy keeps waiting without holding anything,
        so they never hold up someone behind them who could start now.
        """
        queues, wait_token = self.queues, self.wait_token
        contenders = self.floor.contenders[released]
        while True:
            chosen, oldest = -1, -1
            for q in contenders:
                queue = queues[q]
                while queue and wait_token[queue[0][1]] != queue[0][0]:
                    queue.popleft() # timed out earlier
                if queue and (chosen < 0 or queue[0][0] < oldest) and self._fits(q):
                    chosen, oldest = q, queue[0][0]
            if chosen < 0:
                return
            _, member = queues[chosen].popleft()
            wait_token[member] = -1
            self._start(member, self.last[member], 0, time, time - self.wait_since[member])

    def _give_up(self, member: int, time: float) -> None:
        """Patience ran out: take any route that is free right now, else skip the block."""
        self.wait_token[member] = -1 # leaves the queue; the stale entry is dropped later
        exercise = self.last[member]
        options = self.floor.options[exercise]
        for option in range(self.accepted[member]):
            if self._fits(options[option]):
                self._start(member, exercise, option, time, self.patience)
                return
        self._skip(member, exercise, time, self.patience)


    def _fits(self, route: int) -> bool:
        free = self.free
        return all(free[r] >= n for r, n in self.floor.route_slots[route])

    def _start(self, member: int, exercise: int, option: int, time: float, waited: float) -> None:
        floor = self.floor
        route = floor.options[exercise][option]
        slots = floor.route_slots[route]
        free = self.free
        for r, n in slots:
            free[r] -= n
        done = time + floor.block_minutes[exercise] * next(self.block_factor)
        overlap = min(done, self.end) - max(time, self.warmup)
        if overlap > 0:
            busy = self.busy_minutes
            for r, n in slots:
                busy[r] += overlap * n
        self.holding[member] = route
        self._record(time, floor.outcomes[exercise][option], waited)
        self._schedule(done, _RELEASE, member)

    def _skip(self, member: int, exercise: int, time: float, waited: float) -> None:
        self._record(time, _SKIPPED, waited)
        done = time + self.floor.block_minutes[exercise] * next(self.block_factor)
        self._schedule(done, _RELEASE, member)

    def _record(self, time: float, outcome: int, waited: float) -> None:
        if self.warmup <= time < self.end:
            self.tally[outcome] += 1
            self.waits.append(waited)

    def _schedule(self, time: float, kind: int, member: int) -> int:
        sequence = self.sequence
        self.sequence += 1
        heapq.heappush(self.events, (time, kind, sequence, member))
        return sequence


    def _result(self) -> SimulationResult:
        floor, config = self.floor, self.config
        blocks = sum(self.tally)
        shares = [count / blocks if blocks else 0.0 for count in self.tally]
        waits = np.asarray(self.waits, dtype=np.float64)
        utilization = {
            eid: min(1.0, self.busy_minutes[r] / (floor.servers[r] * config.measure_min))
            if floor.servers[r] > 0
            else 0.0
            for r, eid in enumerate(floor.equipment_ids)
            if floor.units[r] > 0
        }
        arrivals = self.arrival[self.n_seeded :]
        return SimulationResult(
            seed=operator.index(config.seed),
            simulated_minutes=self.end,
            visits=int(np.count_nonzero((arrivals >= self.warmup) & (arrivals < self.end))),
            exercise_blocks=blocks,
            mean_wait_min=float(waits.mean()) if blocks else 0.0,
            p90_wait_min=float(np.percentile(waits, WAIT_PERCENTILE)) if blocks else 0.0,
            first_choice_share=shares[_FIRST],
            substituted_share=shares[_SUBSTITUTED],
            skipped_share=shares[_SKIPPED],
            peak_concurrent_users=_peak_concurrency(self.arrival, np.asarray(self.departure), self.warmup, self.end),
            utilization=utilization,
        )


def _peak_concurrency(
    arrival: NDArray[np.float64], departure: NDArray[np.float64], start: float, end: float
) -> int:
    """Most members on the floor at once during [start, end); a stay covers [arrival, departure)."""
    present = int(np.count_nonzero((arrival <= start) & (departure > start)))
    arriving = arrival[(arrival > start) & (arrival < end)]
    if arriving.size == 0:
        return present
    leaving = departure[(departure > start) & (departure < end)]
    times = np.concatenate([leaving, arriving])
    steps = np.concatenate([np.full(leaving.size, -1), np.ones(arriving.size, dtype=np.int64)])
    order = np.lexsort((steps, times)) # Departures sort before arrivals at the same instant, so a hand-over is not an overlap.
    return present + max(0, int(np.cumsum(steps[order]).max()))
