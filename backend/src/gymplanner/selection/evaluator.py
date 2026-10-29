"""Served-demand objective: a loss-network model of members choosing equipment.

Each exercise can be performed several ways ("routes"), each occupying one or more equipment
types at once (dumbbell press = dumbbells + a bench) and rated by how well it serves the
exercise (quality 0-1). A member tries the best route first. If its equipment is busy or not
in the gym, they move on to the next route only as willingly as it fits: the chance of trying
a route is its quality relative to the one before it, so nearly everyone accepts a power rack
and bench for a bench press (0.95) but few runners settle for a rower. The rest wait it out
or skip the exercise, which counts as unserved demand at the peak. Without that attrition,
cheap poor substitutes could soak up demand that members would never actually move. Routes
on equipment this plan cannot have (left out, too tall for the ceiling, too big for the room)
still count as the ones before: a gym without treadmills does not make runners any keener on
an elliptical.

Blocking per equipment type comes from the Erlang loss formula, and the coupled system is
solved with the reduced-load (Erlang fixed-point) approximation used for loss networks.
The objective is quality-weighted served demand in Erlangs, so a plan scores highest when
the most people can do the exercise they came for, on the equipment best suited to it.

Everything is vectorized over a batch of candidate plans so the optimizer can score every
possible next move in one pass.
"""

from __future__ import annotations

from collections.abc import Collection, Sequence
from dataclasses import dataclass
from functools import cached_property

import numpy as np
from numpy.typing import NDArray

from gymplanner.catalog.loader import Catalog
from gymplanner.domain import Demand
from gymplanner.queueing.erlang import erlang_b_vec

MAX_ROUTES_PER_EXERCISE = 8
_EPS = 1e-12


@dataclass(frozen=True)
class RouteTable:
    """Exercises, their routes, and the equipment types those routes occupy."""

    equipment_ids: tuple[str, ...]
    stations: NDArray[np.int64]
    """[R] simultaneous users per unit of each equipment type."""
    exercise_ids: tuple[str, ...]
    load: NDArray[np.float64]
    """[E] offered Erlangs per exercise."""
    route_res: NDArray[np.int64]
    """[E, K, U] equipment index per route slot, -1 for an empty slot."""
    route_quality: NDArray[np.float64]
    """[E, K] route quality, 0 where the route does not exist."""
    incidence: NDArray[np.float64]
    """[K, U, E, R] one-hot of ``route_res`` used to scatter loads onto equipment."""
    unroutable_load: float
    """Offered load of exercises with no available route at all (always unserved)."""
    best_quality: NDArray[np.float64] | None = None
    """[E] quality of each exercise's best route over all the equipment the gym's format
    offers, including types this plan cannot have; None when that is the table's own best."""

    @cached_property
    def reference_quality(self) -> NDArray[np.float64]:
        """[E] the quality members measure fallbacks against: the best way to do the exercise,
        whether or not this plan can offer it."""
        own: NDArray[np.float64] = self.route_quality.max(axis=1, initial=0.0)
        if self.best_quality is None:
            return own
        reference: NDArray[np.float64] = np.maximum(own, self.best_quality)
        return reference

    @property
    def n_equipment(self) -> int:
        return len(self.equipment_ids)

    @property
    def total_load(self) -> float:
        return float(self.load.sum()) + self.unroutable_load

    def index_of(self, equipment_id: str) -> int:
        return self.equipment_ids.index(equipment_id)

    @cached_property
    def sweep_plan(self) -> _SweepPlan:
        return _SweepPlan.of(self)

    @cached_property
    def type_neighbours(self) -> NDArray[np.bool_]:
        """[R, R] whether two types appear in routes of a common exercise (incl. itself)."""
        neighbours = np.eye(self.n_equipment, dtype=bool)
        for e in range(self.route_res.shape[0]):
            types = np.unique(self.route_res[e][self.route_res[e] >= 0])
            neighbours[np.ix_(types, types)] = True
        return neighbours


@dataclass(frozen=True)
class _SweepPlan:
    """Per-route index structures for :func:`_sweep`, computed once per table."""

    rows: NDArray[np.int64]
    """[E, 1] exercise index, broadcast against ``slots``."""
    slots: tuple[NDArray[np.int64], ...]
    """Per route rank: [E, U] equipment index per slot, empty slots pointing at a padding
    column that is always free and present."""
    filled: tuple[NDArray[np.bool_], ...]
    """Per route rank: [E, U] whether the slot holds equipment."""
    scatter: tuple[NDArray[np.float64], ...]
    """Per route rank: [E * U, R] one-hot rows that add slot loads onto equipment types."""
    willing: NDArray[np.float64]
    """[E, K] share of members still searching who will try route k: its quality relative
    to the route before it, or for the first route to the exercise's reference quality."""

    @classmethod
    def of(cls, table: RouteTable) -> _SweepPlan:
        n_exercises, n_routes, n_slots = table.route_res.shape
        n_types = table.n_equipment
        quality = table.route_quality
        previous = np.concatenate([table.reference_quality[:, None], quality[:, :-1]], axis=1) # Routes the plan cannot have would come in between; their ratios multiply out, so only the first route needs the reference.
        slots, filled, scatter = [], [], []
        for k in range(n_routes):
            res = table.route_res[:, k, :]
            filled.append(res >= 0)
            slots.append(np.where(res >= 0, res, n_types))
            scatter.append(table.incidence[k].transpose(1, 0, 2).reshape(n_exercises * n_slots, n_types))
        return cls(
            rows=np.arange(n_exercises)[:, None],
            slots=tuple(slots),
            filled=tuple(filled),
            scatter=tuple(scatter),
            willing=np.divide(quality, previous, out=np.zeros_like(quality), where=previous > 0),
        )


def build_route_table(
    catalog: Catalog,
    demand: Demand,
    equipment_ids: Sequence[str],
    offered: Collection[str] | None = None,
) -> RouteTable:
    """Index the exercises' routes over the allowed equipment types.

    ``offered`` is all the equipment the gym's format offers, allowed here or not (by default
    the allowed types): members measure the routes this plan has against the best of those.
    """
    index = {eid: i for i, eid in enumerate(equipment_ids)}
    expected = set(index) if offered is None else set(offered) | set(index)
    rows: list[tuple[str, float, list[tuple[float, list[int]]], float]] = []
    unroutable = 0.0
    for exercise in catalog.exercises:
        load = demand.exercise_load.get(exercise.id, 0.0)
        if load <= 0:
            continue
        routes = [
            (option.quality, [index[eid] for eid in option.uses])
            for option in exercise.options
            if all(eid in index for eid in option.uses)
        ]
        if not routes:
            unroutable += load
            continue
        routes.sort(key=lambda r: (-r[0], len(r[1])))
        best = max((o.quality for o in exercise.options if expected.issuperset(o.uses)), default=0.0)
        rows.append((exercise.id, load, routes[:MAX_ROUTES_PER_EXERCISE], best))

    n_exercises = len(rows)
    n_routes = max((len(r[2]) for r in rows), default=1)
    n_slots = max((len(res) for r in rows for _, res in r[2]), default=1)
    n_equipment = len(equipment_ids)

    route_res = np.full((n_exercises, n_routes, n_slots), -1, dtype=np.int64)
    route_quality = np.zeros((n_exercises, n_routes), dtype=np.float64)
    incidence = np.zeros((n_routes, n_slots, n_exercises, n_equipment), dtype=np.float64)
    for e, (_, _, routes, _) in enumerate(rows):
        for k, (quality, res) in enumerate(routes):
            route_quality[e, k] = quality
            for u, r in enumerate(res):
                route_res[e, k, u] = r
                incidence[k, u, e, r] = 1.0

    stations = np.array([catalog.equipment_by_id[eid].stations for eid in equipment_ids], dtype=np.int64)
    return RouteTable(
        equipment_ids=tuple(equipment_ids),
        stations=stations,
        exercise_ids=tuple(r[0] for r in rows),
        load=np.array([r[1] for r in rows], dtype=np.float64),
        route_res=route_res,
        route_quality=route_quality,
        incidence=incidence,
        unroutable_load=unroutable,
        best_quality=None if offered is None else np.array([r[3] for r in rows], dtype=np.float64),
    )


@dataclass(frozen=True)
class Evaluation:
    """Model outputs for a batch of N candidate plans."""

    value: NDArray[np.float64]
    """[N] quality-weighted served Erlangs (the objective)."""
    served: NDArray[np.float64]
    """[N] served Erlangs regardless of route quality."""
    blocking: NDArray[np.float64]
    """[N, R] probability that every station of a type is busy when someone arrives."""
    offered: NDArray[np.float64]
    """[N, R] Erlangs offered to each equipment type after fallbacks."""
    route_carried: NDArray[np.float64]
    """[N, E, K] Erlangs served on each route."""

    def carried(self) -> NDArray[np.float64]:
        """[N, R] average stations in use per equipment type."""
        return self.offered * (1.0 - self.blocking)


def _sweep(
    table: RouteTable, blocking: NDArray[np.float64], present: NDArray[np.bool_]
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Route demand through each exercise's fallbacks given fixed per-type blocking.

    Types are treated as independent (the reduced-load approximation), but each member's view
    of a type is conditioned on the routes they have already found blocked.
    """
    plan = table.sweep_plan
    n_plans, n_types = blocking.shape
    n_exercises, n_routes, n_slots = table.route_res.shape
    available = np.ones((n_plans, n_types + 1)) # A padding column (always free, always present) absorbs empty route slots.
    available[:, :n_types] -= blocking
    present = np.concatenate([present, np.ones((n_plans, 1), dtype=bool)], axis=1)
    conditional = np.repeat(available[:, None, :], n_exercises, axis=1)
    remaining = np.broadcast_to(table.load, (n_plans, n_exercises)).copy()
    value = np.zeros(n_plans)
    served = np.zeros(n_plans)
    offered = np.zeros_like(blocking)
    route_carried = np.zeros((n_plans, n_exercises, n_routes))
    rows = plan.rows

    for k in range(n_routes):
        remaining *= plan.willing[:, k]
        idx = plan.slots[k]
        seen = conditional[:, rows, idx]
        exists = present[:, idx].all(axis=2) & (table.route_quality[:, k] > 0)
        p_free = seen.prod(axis=2) * exists
        carried = remaining * p_free
        route_carried[:, :, k] = carried
        value += carried @ table.route_quality[:, k]
        served += carried.sum(axis=1)
        thinned = carried[:, :, None] / np.maximum(available[:, idx], _EPS) # Thin by other stations' availability. Unconditional availability counts each member once even when routes share equipment.
        offered += thinned.reshape(n_plans, n_exercises * n_slots) @ plan.scatter[k]
        failed = np.maximum(1.0 - p_free, _EPS)[:, :, None] # Condition on this route having failed: a type that probably caused the failure is probably still busy when the member tries a fallback that also needs it.
        updated = np.clip(1.0 - (1.0 - seen) / failed, 0.0, 1.0)
        conditional[:, rows, idx] = np.where(plan.filled[k] & exists[:, :, None], updated, seen)
        remaining -= carried

    return value, served, offered, route_carried


def evaluate(
    table: RouteTable,
    units: NDArray[np.int64],
    warm_blocking: NDArray[np.float64] | None = None,
    max_iterations: int = 200,
    tolerance: float = 1e-5,
    damping: float = 0.5,
) -> Evaluation:
    """Solve the Erlang fixed point for each plan in ``units`` ([N, R] or [R]).

    Plans converge independently; once a plan's blocking stops moving it drops out of the
    iteration so a batch costs roughly its average, not its slowest, member. Plain substitution
    converges fastest on realistic plans; a plan whose updates start growing (oscillation in
    heavily loaded networks) switches to partial ``damping`` steps for the rest of the solve.
    """
    units = np.atleast_2d(np.asarray(units, dtype=np.int64))
    servers = units * table.stations[None, :]
    present = servers > 0
    if warm_blocking is None:
        blocking = np.zeros(servers.shape, dtype=np.float64)
    else:
        blocking = np.broadcast_to(warm_blocking, servers.shape).copy()

    n_plans = servers.shape[0]
    active = np.arange(n_plans)
    damped = np.zeros(n_plans, dtype=bool)
    previous = np.full(n_plans, np.inf)
    for _ in range(max_iterations):
        _, _, offered, _ = _sweep(table, blocking[active], present[active])
        updated = erlang_b_vec(servers[active], offered)
        delta = np.max(np.abs(updated - blocking[active]), axis=1, initial=0.0)
        damped[active] |= delta > previous[active]
        step = np.where(damped[active], damping, 1.0)[:, None]
        blocking[active] = step * updated + (1.0 - step) * blocking[active]
        previous[active] = delta
        active = active[delta >= tolerance]
        if active.size == 0:
            break

    value, served, offered, route_carried = _sweep(table, blocking, present)
    return Evaluation(value=value, served=served, blocking=blocking, offered=offered, route_carried=route_carried)
