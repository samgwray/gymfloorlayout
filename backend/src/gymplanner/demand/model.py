"""Turn the average member's behavior into offered load per exercise.

At a random moment in the design hour, ``active_users`` people each occupy one exercise
block. The modality shares say how that time splits across cardio, barbell, dumbbell, machine,
cable, bodyweight, functional and mobility work. Within a modality, an exercise's share of
time is its popularity times how long one block of it ties up a station.
"""

from __future__ import annotations

from collections import defaultdict

from gymplanner.catalog.loader import Catalog
from gymplanner.catalog.schema import MODALITIES, Exercise, Modality
from gymplanner.demand.occupancy import estimate_peak_users
from gymplanner.domain import Demand


def exercise_time_weights(
    exercises: tuple[Exercise, ...],
    multipliers: dict[str, float],
    excluded_equipment: frozenset[str] = frozenset(),
) -> dict[str, float]:
    """Unnormalized share of floor time per exercise: popularity x block length x profile.

    Exercises the gym format rules out entirely (every way of doing them needs equipment the
    profile excludes, e.g. Olympic lifts in a hotel room) get no time: that format's members
    spend it on other exercises of the same modality instead.
    """
    weights: dict[str, float] = {}
    for e in exercises:
        possible = any(not excluded_equipment.intersection(o.uses) for o in e.options)
        weight = e.popularity * e.block_minutes * multipliers.get(e.id, 1.0)
        weights[e.id] = weight if possible else 0.0
    return weights


def build_demand(
    catalog: Catalog,
    profile_id: str,
    training_sqft: float,
    members: int | None = None,
) -> Demand:
    profile = catalog.profile_by_id[profile_id]
    behavior = catalog.behavior
    peak = estimate_peak_users(training_sqft, behavior.occupancy, profile, members)
    active_users = peak.peak_users * (1.0 - behavior.session.idle_share)

    weights = exercise_time_weights(
        catalog.exercises,
        profile.exercise_multipliers,
        frozenset(profile.excluded_equipment),
    )
    by_modality: dict[Modality, list[Exercise]] = defaultdict(list)
    for exercise in catalog.exercises:
        by_modality[exercise.modality].append(exercise)

    shares = profile.modality_share.as_dict()
    exercise_load: dict[str, float] = {}
    for modality in MODALITIES:
        members_of_modality = by_modality.get(modality, [])
        total_weight = sum(weights[e.id] for e in members_of_modality)
        if total_weight <= 0:
            continue
        modality_load = active_users * shares[modality]
        for exercise in members_of_modality:
            exercise_load[exercise.id] = modality_load * weights[exercise.id] / total_weight

    return Demand(
        profile_id=profile_id,
        peak=peak,
        active_users=active_users,
        modality_share=shares,
        exercise_load=exercise_load,
    )
