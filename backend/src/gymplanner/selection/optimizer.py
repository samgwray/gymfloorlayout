"""Choose how many units of each equipment type to buy under a budget and a space limit.

The search is a greedy multi-dimensional knapsack on the served-demand objective:

1. Every step scores all feasible moves in one vectorized evaluation. A move adds one unit
   of a type (several at once for types that already have many units), or completes a
   route that needs two missing types together (a bench is worthless until there are
   dumbbells), always pulling in prerequisites.
2. Moves are ranked by gain per unit of *scarce* resource: cost / remaining budget plus
   area / remaining area, so whichever constraint is running out is weighted more.
3. Afterwards a swap search removes the unit that contributes least per resource it frees
   and refills greedily, keeping the change only when the objective improves.
4. The type members ask for most (usually a treadmill) is kept in the plan, with enough units
   for its own demand, unless leaving them out serves clearly more; see ``most_wanted_holds``.
5. Between plans that serve about the same, the one that gives more of the demand a well-suited
   station wins (``coverage_moves``, ``held_addition``): a squat rack over a third bench.

Buying stops when a move would serve too little: too small a share of demand, too little use
for each unit it adds (``MIN_UNIT_USE``, which is what stops a gym with few members from
spending its whole budget), or too little for its price next to the plan so far.

Because each extra unit of a type serves less new demand than the one before (Erlang carried
load is concave in station count), small plans spread money across many types while large
plans add redundancy exactly where peak demand queues up.
"""

from __future__ import annotations

import math
from collections.abc import Iterator
from dataclasses import dataclass, field, replace

import numpy as np
from numpy.typing import NDArray

from gymplanner.queueing.erlang import servers_for_blocking
from gymplanner.selection.evaluator import Evaluation, RouteTable, evaluate
from gymplanner.selection.explain import WELL_SUITED_QUALITY, best_route_quality

COARSE_FROM_UNITS = 6
"""Types with at least this many units grow by a fraction of their count per step."""
COARSE_FRACTION = 0.15
MIN_GAIN_FRACTION = 2e-4
"""Stop adding when a move would serve less than this share of total demand."""
MIN_RELATIVE_RETURN = 0.04
"""Stop adding when a move's value per dollar falls below this share of the plan's average
value per dollar so far: past that point peak demand is met and extra spend buys little."""
RETURN_BASIS_SHARE = 0.5
"""The plan's average value per dollar is taken over at least this share of the budget, so
that a plan of one or two cheap pieces (a stretching mat) does not make everything else look
poor value and stop a small budget early."""
MIN_UNIT_USE = 0.05
"""Stop adding when a move would serve fewer Erlangs than this per unit it buys: a unit in use
less than 3 minutes of the design hour has too few members to use it. The rules above are
relative to the plan, so on their own a gym with 20 members would spend its whole budget."""
UNCAPPED = 10_000
LAZY_BATCH = 16
"""Moves scored per lazy evaluation batch."""
FULL_RESCORE_EVERY = 8
MAX_MOVES_PER_STEP = 4
"""Most moves one greedy step takes when the runners-up are independent of each other."""
PARALLEL_RATIO = 0.8
"""Runners-up are taken only when their ratio is within this share of the step's best."""
SCREEN_TOLERANCE = 1e-4
"""Looser fixed-point tolerance when ranking candidate moves; accepted states use the default."""
DROP_TRIES = 4
"""Weakest units the swap search tries dropping per round."""
ROOM_TRIES = 3
"""Expensive additions the swap search tries making room for per round."""
ROOM_MIN_GAIN = 1e-3
"""Making room must raise the plan's value by this share: on big floors the reshuffle buys
hundredths of a percent and costs seconds."""
MOST_WANTED_TOLERANCE = 0.05
"""The most-wanted type stays in the plan unless the best plan without it serves more than this
share more demand. Closer than that the two plans are a judgement call the demand data cannot
settle, and members expect to find what they ask for most; much further, the type would take
too much of a small budget."""
MOST_WANTED_BLOCKING = 0.25
"""The most-wanted type is held at enough units that, on the demand it is first choice for, at
most this share of the members who come for it find every one busy at the design peak (Erlang
B). Cheaper machines that serve it only as substitutes would otherwise take its place."""
COVERAGE_TOLERANCE = 0.02
"""A station that gives more of the demand a well-suited option joins the plan when the plan
with it serves within this share of the plan without it. Closer than that the demand data cannot
tell the two apart, and the plan where more members find the station their exercise is done on
is the better gym; further, the station would cost the members who queue elsewhere."""
COVERAGE_MIN_SHARE = 0.01
"""A station is tried only when it gives at least this share of all demand a well-suited option."""
COVERAGE_TRIES = 3
"""Stations tried per plan, the one giving the most demand a well-suited option first."""
_TINY = 1e-9


@dataclass(frozen=True)
class Constraints:
    budget_usd: float
    """Money available for equipment (flooring already deducted); unit costs include install."""
    area_sqin: float
    """Effective area available for equipment envelopes."""
    unit_cost: NDArray[np.float64]
    unit_area: NDArray[np.float64]
    max_units: NDArray[np.int64]
    requires: tuple[tuple[int, ...], ...]
    min_units: NDArray[np.int64] | None = None


@dataclass(frozen=True)
class Step:
    added: dict[int, int]
    gain: float
    cost: float
    area: float
    value: float
    total_cost: float
    total_area: float


@dataclass
class Selection:
    units: NDArray[np.int64]
    evaluation: Evaluation
    cost: float
    area: float
    steps: list[Step] = field(default_factory=list)

    @property
    def value(self) -> float:
        return float(self.evaluation.value[0])


def _with_prerequisites(
    delta: dict[int, int], units: NDArray[np.int64], requires: tuple[tuple[int, ...], ...]
) -> dict[int, int]:
    pending = list(delta)
    while pending:
        r = pending.pop()
        for prereq in requires[r]:
            if units[prereq] == 0 and prereq not in delta:
                delta[prereq] = 1
                pending.append(prereq)
    return delta


MoveKey = tuple[str, tuple[int, ...]]


@dataclass(frozen=True)
class _Move:
    key: MoveKey
    delta: dict[int, int]
    cost: float
    area: float


def _candidate_moves(
    units: NDArray[np.int64],
    table: RouteTable,
    cons: Constraints,
    budget_left: float,
    area_left: float,
) -> list[_Move]:
    moves: dict[MoveKey, _Move] = {}

    def add(key: MoveKey, delta: dict[int, int]) -> bool:
        full = _with_prerequisites(dict(delta), units, cons.requires)
        if any(units[r] + n > cons.max_units[r] for r, n in full.items()):
            return False
        cost = float(sum(cons.unit_cost[r] * n for r, n in full.items()))
        area = float(sum(cons.unit_area[r] * n for r, n in full.items()))
        if cost > budget_left + 1e-6 or area > area_left + 1e-6:
            return False
        moves.setdefault(key, _Move(key=key, delta=full, cost=cost, area=area))
        return True

    for r in range(table.n_equipment):
        if units[r] >= cons.max_units[r]:
            continue
        size = 1 if units[r] < COARSE_FROM_UNITS else max(1, round(units[r] * COARSE_FRACTION)) # Well-stocked types grow geometrically so a big floor takes tens of steps, not hundreds; a single unit is the fallback when the larger step no longer fits.
        if not add(("unit", (r,)), {r: size}) and size > 1:
            add(("unit", (r,)), {r: 1})

    for e in range(table.route_res.shape[0]):
        for k in range(table.route_res.shape[1]):
            missing = tuple(sorted(int(r) for r in table.route_res[e, k] if r >= 0 and units[r] == 0))
            if len(missing) >= 2:
                add(("bundle", missing), dict.fromkeys(missing, 1))
    return list(moves.values())


def _worthwhile(gain: float, move: _Move, value: float, basis: float, min_gain: float) -> bool:
    """Whether a move clears the stopping rules on top of a plan worth ``value``, its average
    value per dollar taken over ``basis`` dollars: a share of demand, use for every unit it buys
    (prerequisites aside), and a return per dollar not far below the plan's."""
    units = sum(move.delta[r] for r in move.key[1])
    return gain > max(min_gain, MIN_UNIT_USE * units) and (
        gain * basis >= MIN_RELATIVE_RETURN * value * move.cost
    )


def _return_basis(cost: float, cons: Constraints) -> float:
    return max(cost, RETURN_BASIS_SHARE * cons.budget_usd)


def greedy(
    table: RouteTable,
    cons: Constraints,
    start: NDArray[np.int64] | None = None,
    record_steps: bool = True,
    max_steps: int | None = None,
    until_value: float | None = None,
) -> Selection:
    """Add the best moves per scarce resource until nothing feasible is worth adding (or, with
    ``max_steps``, once that many moves are recorded; with ``until_value``, once the plan is
    worth that much).

    Moves are scored lazily: each step re-scores only the moves whose last known ratio could
    still beat the best fresh one (ratios fall as units accumulate and resources tighten),
    with a full re-score every few steps to pick up complements whose value rose. A step also
    takes up to ``MAX_MOVES_PER_STEP - 1`` runners-up that scored nearly as well and touch no
    equipment sharing an exercise with the moves already taken: their gains do not interact,
    so taking them together gives the same result as taking them one per step.
    """
    units = np.zeros(table.n_equipment, dtype=np.int64) if start is None else start.astype(np.int64)
    if cons.min_units is not None:
        units = np.maximum(units, cons.min_units)
    current = evaluate(table, units)
    cost = float(units @ cons.unit_cost)
    area = float(units @ cons.unit_area)
    min_gain = MIN_GAIN_FRACTION * max(table.total_load, _TINY)
    neighbours = table.type_neighbours
    steps: list[Step] = []
    stale: dict[MoveKey, float] = {}

    for step_index in range(10_000):
        budget_left = cons.budget_usd - cost
        area_left = cons.area_sqin - area
        moves = _candidate_moves(units, table, cons, budget_left, area_left)
        if not moves:
            break
        basis = _return_basis(cost, cons)
        if step_index % FULL_RESCORE_EVERY == 0:
            stale.clear()
        moves.sort(key=lambda m: -stale.get(m.key, np.inf))

        fresh: list[tuple[float, float, _Move, NDArray[np.float64]]] = []
        best_ratio = -np.inf
        for start_at in range(0, len(moves), LAZY_BATCH):
            chunk = moves[start_at : start_at + LAZY_BATCH]
            batch = np.repeat(units[None, :], len(chunk), axis=0)
            for i, move in enumerate(chunk):
                for r, n in move.delta.items():
                    batch[i, r] += n
            scored = evaluate(table, batch, warm_blocking=current.blocking[0], tolerance=SCREEN_TOLERANCE)
            gains = scored.value - current.value[0]
            for i, move in enumerate(chunk):
                pressure = move.cost / max(budget_left, _TINY) + move.area / max(area_left, _TINY)
                worthwhile = _worthwhile(float(gains[i]), move, float(current.value[0]), basis, min_gain)
                ratio = gains[i] / max(pressure, _TINY) if worthwhile else -np.inf
                stale[move.key] = ratio
                if np.isfinite(ratio):
                    fresh.append((ratio, float(gains[i]), move, scored.blocking[i]))
                    best_ratio = max(best_ratio, ratio)
            following = start_at + LAZY_BATCH
            if following >= len(moves):
                break
            if fresh and best_ratio >= stale.get(moves[following].key, np.inf): # Stop early only once something worth buying is found: a move cached as worthless may have become useful since (a bench after dumbbells are bought).
                break

        if not fresh:
            break
        fresh.sort(key=lambda f: -f[0])
        taken = [fresh[0]]
        blocked = np.asarray(neighbours[list(fresh[0][2].delta)].any(axis=0), dtype=bool)
        spent = (fresh[0][2].cost, fresh[0][2].area)
        for candidate in fresh[1:]:
            if len(taken) >= MAX_MOVES_PER_STEP or candidate[0] < PARALLEL_RATIO * best_ratio:
                break
            move = candidate[2]
            if blocked[list(move.delta)].any() or any(r in t[2].delta for t in taken for r in move.delta):
                continue
            if spent[0] + move.cost > budget_left + 1e-6 or spent[1] + move.area > area_left + 1e-6:
                continue
            taken.append(candidate)
            blocked |= np.asarray(neighbours[list(move.delta)].any(axis=0), dtype=bool)
            spent = (spent[0] + move.cost, spent[1] + move.area)

        value_before = float(current.value[0])
        for _, _, move, _ in taken:
            for r, n in move.delta.items():
                units[r] += n
            stale.pop(move.key, None)
        current = evaluate(table, units, warm_blocking=taken[0][3])
        if record_steps:
            scale = (float(current.value[0]) - value_before) / max(sum(t[1] for t in taken), _TINY) # Independent moves add up, so each step's value is the running sum of gains, rescaled to land exactly on the re-solved value after the last one.
            running = value_before
            for _, gain, move, _ in taken:
                cost += move.cost
                area += move.area
                running += gain * scale
                steps.append(
                    Step(
                        added=dict(move.delta),
                        gain=gain,
                        cost=move.cost,
                        area=move.area,
                        value=running,
                        total_cost=cost,
                        total_area=area,
                    )
                )
        else:
            cost += spent[0]
            area += spent[1]
        if max_steps is not None and len(steps) >= max_steps:
            break
        if until_value is not None and current.value[0] >= until_value:
            break

    return Selection(units=units, evaluation=current, cost=cost, area=area, steps=steps)


def _removal_candidates(units: NDArray[np.int64], cons: Constraints) -> list[int]:
    floor = cons.min_units if cons.min_units is not None else np.zeros_like(units)
    needed = {p for r in np.flatnonzero(units) for p in cons.requires[int(r)]}
    return [
        int(r) for r in np.flatnonzero(units > floor) if not (units[r] == 1 and int(r) in needed)
    ]


def _drop_and_refill(table: RouteTable, cons: Constraints, best: Selection) -> Selection | None:
    """Drop one of the weakest units and refill greedily; the first refill that beats ``best``."""
    candidates = _removal_candidates(best.units, cons)
    if not candidates:
        return None
    batch = np.repeat(best.units[None, :], len(candidates), axis=0)
    for i, r in enumerate(candidates):
        batch[i, r] -= 1
    scored = evaluate(table, batch, warm_blocking=best.evaluation.blocking[0], tolerance=SCREEN_TOLERANCE)
    losses = best.value - scored.value
    freed = cons.unit_cost[candidates] / max(cons.budget_usd, _TINY) + cons.unit_area[candidates] / max(cons.area_sqin, _TINY)
    for i in np.argsort(losses / np.maximum(freed, _TINY))[:DROP_TRIES]:
        trial = greedy(table, cons, start=batch[i], record_steps=False)
        if trial.value > best.value * (1 + 1e-6) + 1e-9:
            return trial
    return None


def _room_candidates(table: RouteTable, cons: Constraints, best: Selection) -> list[dict[int, int]]:
    """Additions that no longer fit what is left but would be among the best buys if they did.

    They are ranked by value per share of the whole budget and floor, the greedy's ratio before
    anything was spent, so an expensive unit the greedy reached too late still scores well.
    """
    budget_left = cons.budget_usd - best.cost
    area_left = cons.area_sqin - best.area
    moves: list[tuple[dict[int, int], float, float]] = []
    for r in range(table.n_equipment):
        delta = _with_prerequisites({r: 1}, best.units, cons.requires)
        if any(best.units[x] + n > cons.max_units[x] for x, n in delta.items()):
            continue
        cost = float(sum(cons.unit_cost[x] * n for x, n in delta.items()))
        area = float(sum(cons.unit_area[x] * n for x, n in delta.items()))
        fits_now = cost <= budget_left + 1e-6 and area <= area_left + 1e-6
        fits_at_all = cost <= cons.budget_usd and area <= cons.area_sqin
        if fits_at_all and not fits_now:
            moves.append((delta, cost, area))
    if not moves:
        return []
    batch = np.repeat(best.units[None, :], len(moves), axis=0)
    for i, (delta, _, _) in enumerate(moves):
        for x, n in delta.items():
            batch[i, x] += n
    scored = evaluate(table, batch, warm_blocking=best.evaluation.blocking[0], tolerance=SCREEN_TOLERANCE)
    gains = scored.value - best.value
    pressure = np.array(
        [
            cost / max(cons.budget_usd, _TINY) + area / max(cons.area_sqin, _TINY)
            for _, cost, area in moves
        ]
    )
    order = np.argsort(-gains / np.maximum(pressure, _TINY))
    return [moves[i][0] for i in order[:ROOM_TRIES] if gains[i] > 0]


def _make_room(
    table: RouteTable, cons: Constraints, best: Selection, delta: dict[int, int]
) -> Selection | None:
    """Add ``delta``, then drop the units that lose the least value per scarce resource freed
    until the plan fits again, and refill whatever is left over."""
    units = best.units.copy()
    for r, n in delta.items():
        units[r] += n
    cost = float(units @ cons.unit_cost)
    area = float(units @ cons.unit_area)
    while cost > cons.budget_usd + 1e-6 or area > cons.area_sqin + 1e-6:
        candidates = [r for r in _removal_candidates(units, cons) if r not in delta]
        if not candidates:
            return None
        batch = np.repeat(units[None, :], len(candidates) + 1, axis=0) # Row 0 is the current plan, so losses come from one consistent solve.
        for i, r in enumerate(candidates, start=1):
            batch[i, r] -= 1
        scored = evaluate(table, batch, warm_blocking=best.evaluation.blocking[0], tolerance=SCREEN_TOLERANCE)
        losses = scored.value[0] - scored.value[1:]
        freed = np.zeros(len(candidates))
        if cost > cons.budget_usd + 1e-6:
            freed += cons.unit_cost[candidates] / max(cons.budget_usd, _TINY)
        if area > cons.area_sqin + 1e-6:
            freed += cons.unit_area[candidates] / max(cons.area_sqin, _TINY)
        drop = candidates[int(np.argmin(losses / np.maximum(freed, _TINY)))]
        units[drop] -= 1
        cost -= float(cons.unit_cost[drop])
        area -= float(cons.unit_area[drop])
    return greedy(table, cons, start=units, record_steps=False)


def improve(
    table: RouteTable, cons: Constraints, selection: Selection, max_rounds: int = 25
) -> Selection:
    """Swap search; each change is kept only if the plan's value rises.

    First it drops one of the weakest units and refills greedily. When that stops paying, it
    makes room for an expensive unit the greedy reached too late: dropping one unit at a time
    rarely frees enough money or floor for it.
    """
    best = selection
    for _ in range(max_rounds):
        trial = _drop_and_refill(table, cons, best)
        if trial is None:
            for delta in _room_candidates(table, cons, best):
                made = _make_room(table, cons, best, delta)
                if made is not None and made.value > best.value * (1 + ROOM_MIN_GAIN):
                    trial = made
                    break
        if trial is None:
            break
        best = Selection(
            units=trial.units,
            evaluation=trial.evaluation,
            cost=trial.cost,
            area=trial.area,
            steps=selection.steps,
        )
    return best


def optimize(table: RouteTable, cons: Constraints) -> Selection:
    return improve(table, cons, greedy(table, cons))


@dataclass(frozen=True)
class Addition:
    """A move on top of a plan: what it adds, and what that serves and costs."""

    added: dict[int, int]
    gain: float
    cost: float
    area: float


def additions(
    table: RouteTable, cons: Constraints, selection: Selection, budget_usd: float | None = None
) -> list[Addition]:
    """Moves the greedy would still find worth buying on top of ``selection`` and that cost at
    most ``budget_usd`` (by default whatever the budget has left), best value per dollar first.
    Space is not checked: the caller lays them out."""
    left = cons.budget_usd - selection.cost if budget_usd is None else budget_usd
    moves = _candidate_moves(selection.units, table, cons, left, np.inf)
    if not moves:
        return []
    batch = np.repeat(selection.units[None, :], len(moves), axis=0)
    for i, move in enumerate(moves):
        for r, n in move.delta.items():
            batch[i, r] += n
    scored = evaluate(table, batch, warm_blocking=selection.evaluation.blocking[0], tolerance=SCREEN_TOLERANCE)
    min_gain = MIN_GAIN_FRACTION * max(table.total_load, _TINY)
    basis = _return_basis(selection.cost, cons)
    found = [
        Addition(added=dict(move.delta), gain=float(gain), cost=move.cost, area=move.area)
        for move, gain in zip(moves, scored.value - selection.value, strict=True)
        if _worthwhile(float(gain), move, selection.value, basis, min_gain)
    ]
    return sorted(found, key=lambda a: -a.gain / max(a.cost, _TINY))


def best_unit_gain(table: RouteTable, cons: Constraints, selection: Selection) -> float:
    """The most any move on top of ``selection`` would serve per unit it buys, at any price:
    below ``MIN_UNIT_USE`` the gym's members are too few to use more equipment."""
    moves = _candidate_moves(selection.units, table, cons, np.inf, np.inf)
    if not moves:
        return 0.0
    batch = np.repeat(selection.units[None, :], len(moves), axis=0)
    for i, move in enumerate(moves):
        for r, n in move.delta.items():
            batch[i, r] += n
    scored = evaluate(table, batch, warm_blocking=selection.evaluation.blocking[0], tolerance=SCREEN_TOLERANCE)
    units = np.array([sum(move.delta[r] for r in move.key[1]) for move in moves])
    return float(((scored.value - selection.value) / np.maximum(units, 1)).max())


def unlimited_plan(table: RouteTable, cons: Constraints) -> Selection:
    """What the greedy buys when money is no limit, step by step: it stops when the floor is full
    or more equipment would see too little use (``MIN_UNIT_USE``)."""
    return greedy(table, replace(cons, budget_usd=np.inf, min_units=None))


def plan_worth(
    table: RouteTable, cons: Constraints, value: float, spend: float
) -> tuple[NDArray[np.int64], float] | None:
    """The greedy's plan when it is first worth ``value``, and what it costs, run with a budget
    of ``spend``. Price weighs less against floor space the more money is left, so a run with
    more than the plan needs can pay more for ``value`` than a budget near its cost would. None
    when the greedy stops short of ``value``."""
    plan = greedy(table, replace(cons, budget_usd=spend, min_units=None), until_value=value)
    if plan.value < value:
        return None
    units = np.zeros_like(plan.units) # Each step's value is a running estimate that lands on the plan's value at the end.
    for step in plan.steps:
        for r, n in step.added.items():
            units[r] += n
        if step.value >= value:
            return units, step.total_cost
    return plan.units, plan.cost


def first_choice_load(table: RouteTable) -> NDArray[np.float64]:
    """[R] offered load of the exercises each type is in the best route of."""
    load = np.zeros(table.n_equipment)
    best = table.route_quality.argmax(axis=1)
    for e, k in enumerate(best):
        if table.route_quality[e, k] > 0:
            types = table.route_res[e, k]
            load[types[types >= 0]] += table.load[e]
    return load


def most_wanted(table: RouteTable) -> int | None:
    """The type in the best route of the most offered load: what members ask for most."""
    load = first_choice_load(table)
    return int(load.argmax()) if load.any() else None


def most_wanted_units(table: RouteTable, cons: Constraints) -> tuple[int, int] | None:
    """The most-wanted type and how many units its own demand needs (``MOST_WANTED_BLOCKING``),
    as many of those as the budget and the floor hold; None when not even one does."""
    top = most_wanted(table)
    if top is None:
        return None
    servers = servers_for_blocking(float(first_choice_load(table)[top]), MOST_WANTED_BLOCKING)
    wanted = min(max(1, math.ceil(servers / table.stations[top])), int(cons.max_units[top]))
    for units in range(wanted, 0, -1):
        if _held_floor(cons, top, units) is not None:
            return top, units
    return None


def _holdable(cons: Constraints, floor: NDArray[np.int64]) -> bool:
    """Whether ``floor`` as ``min_units`` leaves a feasible plan."""
    return (
        float(floor @ cons.unit_cost) <= cons.budget_usd + 1e-6
        and float(floor @ cons.unit_area) <= cons.area_sqin + 1e-6
        and bool((floor <= cons.max_units).all())
    )


def _held_floor(cons: Constraints, top: int, units: int) -> NDArray[np.int64] | None:
    """``min_units`` that hold ``units`` of ``top`` and their prerequisites, if they fit."""
    seed = np.zeros(len(cons.unit_cost), dtype=np.int64)
    for r, n in _with_prerequisites({top: units}, seed, cons.requires).items():
        seed[r] = n
    floor = seed if cons.min_units is None else np.maximum(cons.min_units, seed)
    return floor if _holdable(cons, floor) else None


HOLD_PROBES = 48
"""Hold counts the quick estimate scores at most (spread over the range when it is wider)."""


def _cut_back(
    cons: Constraints, selection: Selection, floor: NDArray[np.int64]
) -> NDArray[np.int64] | None:
    """The longest stretch of the greedy's build-up of ``selection`` that still leaves room for
    ``floor``, with ``floor`` added: a plan that holds it, quickly found."""
    if not selection.steps:
        return None
    prefix = np.zeros((len(selection.steps) + 1, len(floor)), dtype=np.int64)
    for k, step in enumerate(selection.steps, start=1):
        prefix[k] = prefix[k - 1]
        for r, n in step.added.items():
            prefix[k, r] += n
    plans = np.maximum(prefix, floor[None, :])
    fits = (plans @ cons.unit_cost <= cons.budget_usd + 1e-6) & (
        plans @ cons.unit_area <= cons.area_sqin + 1e-6
    )
    if not fits.any():
        return None
    out: NDArray[np.int64] = plans[int(np.flatnonzero(fits)[-1])]
    return out


def _largest_hold(
    table: RouteTable, cons: Constraints, selection: Selection, top: int, wanted: int
) -> int | None:
    """The most units of ``top``, up to ``wanted``, that a plan can hold and still serve within
    ``MOST_WANTED_TOLERANCE`` of ``selection``, judged on the greedy's build-up cut back to
    make room for them. That plan is a lower bound on the best one holding them, so a hold it
    passes is safe; None when no hold above what the selection has passes, or there is no
    build-up to cut back."""
    have = int(selection.units[top])
    probes = min(HOLD_PROBES, max(wanted - have, 1))
    counts = np.unique(np.round(np.linspace(have + 1, wanted, probes)).astype(int))
    held: list[tuple[int, NDArray[np.int64]]] = []
    for count in counts:
        floor = _held_floor(cons, top, int(count))
        plan = None if floor is None else _cut_back(cons, selection, floor)
        if plan is not None:
            held.append((int(count), plan))
    if not held:
        return None
    values = evaluate(table, np.array([plan for _, plan in held]), tolerance=SCREEN_TOLERANCE).value
    passing = [
        count
        for (count, _), value in zip(held, values, strict=True)
        if serves_within_tolerance(float(value), selection.value)
    ]
    return max(passing, default=None)


def _held_plan(
    table: RouteTable, cons: Constraints, selection: Selection, top: int, units: int
) -> tuple[Selection, Constraints] | None:
    """The best plan found that keeps ``units`` of ``top``, with the constraints that hold
    them. It starts from the greedy's build-up cut back to make room (or, without one, from
    ``selection`` with room made), and is refilled and swap-searched: much cheaper than a fresh
    search on a big floor."""
    floor = _held_floor(cons, top, units)
    if floor is None:
        return None
    held = replace(cons, min_units=floor)
    start = _cut_back(held, selection, floor)
    if start is not None:
        made = greedy(table, held, start=start, record_steps=False)
    else:
        missing = floor - selection.units
        added = {int(r): int(missing[r]) for r in np.flatnonzero(missing > 0)}
        room = _make_room(table, held, selection, added)
        if room is None:
            return None
        made = room
    return improve(table, held, made), held


def most_wanted_holds(
    table: RouteTable, cons: Constraints, selection: Selection
) -> Iterator[tuple[Selection, Constraints]]:
    """Plans that hold the most-wanted type, strongest hold first, with the constraints that
    hold it.

    A plan that leaves out an expensive favourite for several cheaper pieces can score about
    the same, and the greedy reaches the favourite last. The first plan holds as many units
    as its own demand needs (``MOST_WANTED_BLOCKING``), or the most of those that a quick
    estimate finds within ``MOST_WANTED_TOLERANCE`` of ``selection``; for a plan without any,
    the next holds one. The caller keeps the first that serves within tolerance (compared
    once both are laid out: the floor may hold one better than the other). Nothing is yielded
    when the selection already has enough, or when not even one fits the budget and the floor.
    """
    wanted = most_wanted_units(table, cons)
    if wanted is None:
        return
    top, units = wanted
    have = int(selection.units[top])
    if units <= have:
        return
    strongest = units if not selection.steps else _largest_hold(table, cons, selection, top, units)
    for hold in dict.fromkeys(h for h in (strongest, 1) if h is not None and h > have):
        found = _held_plan(table, cons, selection, top, hold)
        if found is not None:
            yield found


def serves_within_tolerance(
    held: float, free: float, tolerance: float = MOST_WANTED_TOLERANCE
) -> bool:
    """Whether a plan worth ``free`` serves no more than ``tolerance`` more than one worth
    ``held``."""
    return free <= held * (1 + tolerance) + 1e-12


def with_most_wanted(
    table: RouteTable, cons: Constraints, selection: Selection
) -> tuple[Selection, Constraints]:
    """The first plan of ``most_wanted_holds`` that serves within tolerance of ``selection``
    (compared before any layout), or the selection; with the constraints it was made under."""
    for plan, held in most_wanted_holds(table, cons, selection):
        if serves_within_tolerance(plan.value, selection.value):
            return plan, held
    return selection, cons


@dataclass(frozen=True)
class CoverageMove:
    added: dict[int, int]
    """One unit of each type the move adds, prerequisites included."""
    covered: float
    """Offered load (Erlangs) that gains a well-suited route."""


def coverage_moves(
    table: RouteTable, cons: Constraints, units: NDArray[np.int64]
) -> list[CoverageMove]:
    """Stations the plan lacks, by how much demand without a well-suited route
    (``WELL_SUITED_QUALITY``) they give one, most first and at least ``COVERAGE_MIN_SHARE``.

    A move adds one type (a power rack serves squats, presses and rows) or the missing types of
    one well-suited route together (a bench with the dumbbells it needs)."""
    best = best_route_quality(table, units)
    lacking = (best < WELL_SUITED_QUALITY) & (table.load > 0)
    candidates: dict[frozenset[int], dict[int, int]] = {}
    for absent in np.flatnonzero((units == 0) & (cons.max_units > 0)):
        delta = _with_prerequisites({int(absent): 1}, units, cons.requires)
        candidates.setdefault(frozenset(delta), delta)
    for e, k in zip(*np.nonzero(table.route_quality >= WELL_SUITED_QUALITY), strict=True):
        if not lacking[e]:
            continue
        missing = [int(r) for r in table.route_res[e, k] if r >= 0 and units[r] == 0]
        if len(missing) >= 2:
            delta = _with_prerequisites(dict.fromkeys(missing, 1), units, cons.requires)
            candidates.setdefault(frozenset(delta), delta)
    if not candidates:
        return []
    deltas = list(candidates.values())
    trials = np.repeat(units[None, :], len(deltas), axis=0)
    for i, delta in enumerate(deltas):
        for r, n in delta.items():
            trials[i, r] += n
    gained = lacking[None, :] & (best_route_quality(table, trials) >= WELL_SUITED_QUALITY)
    covered = gained.astype(np.float64) @ table.load
    least = max(COVERAGE_MIN_SHARE * table.total_load, _TINY)
    moves = [
        CoverageMove(added=delta, covered=float(load))
        for delta, load in zip(deltas, covered, strict=True)
        if load >= least
    ]
    return sorted(moves, key=lambda m: -m.covered)


def held_addition(
    table: RouteTable, cons: Constraints, selection: Selection, added: dict[int, int]
) -> tuple[Selection, Constraints] | None:
    """The best plan found that keeps ``selection``'s units of the types in ``added``, plus
    ``added``, on top of any ``cons.min_units``: room is made by dropping what loses least per
    resource freed, then the plan is refilled and swap-searched. With the constraints that hold
    it; None when the held units alone do not fit."""
    floor = np.zeros_like(selection.units) if cons.min_units is None else cons.min_units.copy()
    for r, n in added.items():
        floor[r] = max(floor[r], selection.units[r] + n)
    if not _holdable(cons, floor):
        return None
    held = replace(cons, min_units=floor)
    made = _make_room(table, held, selection, added)
    return None if made is None else (improve(table, held, made), held)
