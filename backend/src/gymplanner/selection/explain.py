"""Explain a selection: per-type usage, marginal value and pattern coverage."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from gymplanner.catalog.loader import Catalog
from gymplanner.catalog.schema import Pattern
from gymplanner.selection.evaluator import Evaluation, RouteTable, evaluate

WELL_SUITED_QUALITY = 0.8

PATTERN_LABELS: dict[Pattern, str] = {
    "squat": "Squat",
    "hinge": "Hinge",
    "lunge": "Lunge & single-leg",
    "glute": "Glutes & hips",
    "knee_isolation": "Quads & hamstrings",
    "calf": "Calves",
    "horizontal_push": "Horizontal push",
    "vertical_push": "Vertical push",
    "horizontal_pull": "Horizontal pull",
    "vertical_pull": "Vertical pull",
    "shoulder_isolation": "Shoulders",
    "arm": "Arms",
    "core": "Core",
    "carry": "Carries",
    "conditioning": "Conditioning",
    "cardio": "Cardio",
    "mobility": "Mobility",
}


@dataclass(frozen=True)
class TypeUsage:
    equipment_id: str
    units: int
    servers: int
    served_users: float
    utilization: float
    blocking: float
    last_unit_value: float
    """Objective lost (Erlangs) by removing one unit."""
    next_unit_value: float
    """Objective gained (Erlangs) by adding one more unit."""
    top_exercises: list[str]


@dataclass(frozen=True)
class PatternCoverage:
    pattern: Pattern
    label: str
    coverage: float
    equipment_ids: list[str]


def _route_users_by_type(table: RouteTable, evaluation: Evaluation) -> dict[int, dict[str, float]]:
    """Erlangs each exercise puts on each equipment type (plan 0 of the evaluation)."""
    per_type: dict[int, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    carried = evaluation.route_carried[0]
    for e, exercise_id in enumerate(table.exercise_ids):
        for k in range(table.route_res.shape[1]):
            if carried[e, k] <= 0:
                continue
            for r in table.route_res[e, k]:
                if r >= 0:
                    per_type[int(r)][exercise_id] += float(carried[e, k])
    return per_type


def type_usage(
    catalog: Catalog, table: RouteTable, units: NDArray[np.int64], evaluation: Evaluation
) -> dict[str, TypeUsage]:
    present = [int(r) for r in np.flatnonzero(units)]
    if not present:
        return {}
    plus = np.repeat(units[None, :], len(present), axis=0)
    minus = plus.copy()
    for i, r in enumerate(present):
        plus[i, r] += 1
        minus[i, r] -= 1
    base_value = float(evaluation.value[0])
    warm = evaluation.blocking[0]
    plus_values = evaluate(table, plus, warm_blocking=warm).value
    minus_values = evaluate(table, minus, warm_blocking=warm).value

    carried = evaluation.carried()[0]
    users_by_type = _route_users_by_type(table, evaluation)
    usage: dict[str, TypeUsage] = {}
    for i, r in enumerate(present):
        servers = int(units[r] * table.stations[r])
        ranked = sorted(users_by_type.get(r, {}).items(), key=lambda kv: -kv[1])
        usage[table.equipment_ids[r]] = TypeUsage(
            equipment_id=table.equipment_ids[r],
            units=int(units[r]),
            servers=servers,
            served_users=float(carried[r]),
            utilization=float(carried[r] / servers) if servers else 0.0,
            blocking=float(evaluation.blocking[0, r]),
            last_unit_value=base_value - float(minus_values[i]),
            next_unit_value=float(plus_values[i]) - base_value,
            top_exercises=[
                catalog.exercise_by_id[exercise_id].name
                for exercise_id, users in ranked[:4]
                if users > 1e-4
            ],
        )
    return usage


def best_route_quality(table: RouteTable, units: NDArray[np.int64]) -> NDArray[np.float64]:
    """[E] quality of the best route whose equipment is all present; [N, E] for [N, R] units."""
    present = np.concatenate([units > 0, np.ones((*units.shape[:-1], 1), dtype=bool)], axis=-1) # An empty route slot (-1) reads the appended True.
    usable = present[..., table.route_res].all(axis=-1)
    best: NDArray[np.float64] = np.where(usable, table.route_quality, 0.0).max(axis=-1)
    return best


def pattern_coverage(
    catalog: Catalog, table: RouteTable, units: NDArray[np.int64]
) -> list[PatternCoverage]:
    best = best_route_quality(table, units)
    present = units > 0
    weighted: dict[Pattern, float] = defaultdict(float)
    totals: dict[Pattern, float] = defaultdict(float)
    equipment: dict[Pattern, list[str]] = defaultdict(list)
    for e, exercise_id in enumerate(table.exercise_ids):
        pattern = catalog.exercise_by_id[exercise_id].pattern
        weighted[pattern] += table.load[e] * best[e]
        totals[pattern] += table.load[e]
        for k in range(table.route_res.shape[1]):
            if table.route_quality[e, k] < max(best[e], 1e-9) - 1e-9:
                continue
            res = [int(r) for r in table.route_res[e, k] if r >= 0]
            if res and all(present[r] for r in res):
                for r in res:
                    if table.equipment_ids[r] not in equipment[pattern]:
                        equipment[pattern].append(table.equipment_ids[r])
                break
    for exercise in catalog.exercises:
        totals.setdefault(exercise.pattern, 0.0)

    result = []
    for pattern, label in PATTERN_LABELS.items():
        if pattern not in totals:
            continue
        total = totals[pattern]
        result.append(
            PatternCoverage(
                pattern=pattern,
                label=label,
                coverage=float(weighted[pattern] / total) if total > 0 else 0.0,
                equipment_ids=equipment[pattern],
            )
        )
    return result


def coverage_share(table: RouteTable, units: NDArray[np.int64]) -> float:
    """Demand-weighted share of exercises with a well-suited option in the plan."""
    if table.total_load <= 0:
        return 0.0
    best = best_route_quality(table, units)
    covered = float(table.load[best >= WELL_SUITED_QUALITY].sum())
    return covered / table.total_load
