"""Design-peak occupancy and its split into offered load per exercise."""

from __future__ import annotations

from dataclasses import fields
from typing import Any

import pytest

from gymplanner.catalog.loader import Catalog
from gymplanner.catalog.schema import (
    MODALITIES,
    BehaviorFile,
    Exercise,
    ExerciseOption,
    Modality,
    ModalityShares,
    OccupancyModel,
    Profile,
    SessionModel,
)
from gymplanner.demand import build_demand, estimate_peak_users, exercise_time_weights
from gymplanner.demand.occupancy import MIN_PEAK_USERS, member_peak_share

OCCUPANCY = OccupancyModel(
    peak_users_per_1000_sqft=8.0,
    daily_visit_rate=0.12,
    peak_concurrency_share=0.11,
    design_day_factor=1.25,
    occupant_load_sqft_per_person=50.0,
    sources=["fixture"],
)
SESSION = SessionModel(mean_floor_minutes=60.0, cv=0.5, idle_share=0.3, sources=["fixture"])
PEAK_SHARE = 0.12 * 0.11 * 1.25

GENERAL = Profile(
    id="general",
    name="General",
    description="fixture",
    modality_share=ModalityShares(
        cardio=0.30,
        barbell=0.15,
        dumbbell=0.17,
        machine=0.14,
        cable=0.08,
        bodyweight=0.05,
        functional=0.06,
        mobility=0.05,
    ),
    rationale="fixture",
    sources=["fixture"],
)
STRENGTH = Profile(
    id="strength",
    name="Strength",
    description="fixture",
    modality_share=ModalityShares(
        cardio=0.10,
        barbell=0.35,
        dumbbell=0.25,
        machine=0.15,
        cable=0.10,
        bodyweight=0.05,
        functional=0.0,
        mobility=0.0,
    ),
    peak_users_per_1000_sqft=6.0,
    exercise_multipliers={"deadlift": 2.0, "db_curl": 0.5},
    rationale="fixture",
    sources=["fixture"],
)


def _exercise(xid: str, modality: Modality, popularity: float, block_minutes: float) -> Exercise:
    return Exercise(
        id=xid,
        name=xid,
        modality=modality,
        pattern="core",
        popularity=popularity,
        block_minutes=block_minutes,
        options=[ExerciseOption(uses=["station"], quality=1.0)],
        sources=["fixture"],
    )


EXERCISES = (
    _exercise("treadmill_run", "cardio", 3.0, 25.0),
    _exercise("cycling", "cardio", 2.0, 20.0),
    _exercise("rowing", "cardio", 1.0, 15.0),
    _exercise("back_squat", "barbell", 2.0, 15.0),
    _exercise("deadlift", "barbell", 1.0, 12.0),
    _exercise("db_press", "dumbbell", 2.0, 10.0),
    _exercise("db_curl", "dumbbell", 3.0, 6.0),
    _exercise("leg_press", "machine", 1.0, 10.0),
    _exercise("pushdown", "cable", 1.0, 6.0),
    _exercise("face_pull", "cable", 1.0, 5.0),
    _exercise("pullups", "bodyweight", 1.0, 8.0),
    _exercise("kb_swing", "functional", 1.0, 8.0),
    _exercise("stretching", "mobility", 1.0, 10.0),
)


def make_catalog() -> Catalog:
    """Catalog with only the behavior and exercises sections, all build_demand reads.

    The other sections stay empty so the fixture does not churn as the catalog grows.
    """
    behavior = BehaviorFile(
        version=1,
        session=SESSION,
        occupancy=OCCUPANCY,
        default_profile="general",
        profiles=[GENERAL, STRENGTH],
    )
    sections: dict[str, Any] = {f.name: () for f in fields(Catalog) if f.name != "data_version"}
    sections.update(behavior=behavior, exercises=EXERCISES)
    return Catalog(**sections)


CATALOG = make_catalog()


def modality_totals(loads: dict[str, float]) -> dict[Modality, float]:
    totals = dict.fromkeys(MODALITIES, 0.0)
    for exercise in EXERCISES:
        totals[exercise.modality] += loads[exercise.id]
    return totals


def test_member_peak_share_multiplies_visit_concurrency_and_busy_day() -> None:
    assert member_peak_share(OCCUPANCY) == pytest.approx(PEAK_SHARE)


def test_area_sets_the_peak_when_membership_is_unknown() -> None:
    peak = estimate_peak_users(5_000.0, OCCUPANCY, GENERAL)
    assert peak.method == "density"
    assert peak.peak_users == pytest.approx(40.0)
    assert peak.area_users == pytest.approx(40.0)
    assert peak.member_users is None
    assert peak.members == pytest.approx(40.0 / PEAK_SHARE)
    assert not peak.capped_by_code


def test_profile_density_overrides_the_default() -> None:
    assert estimate_peak_users(5_000.0, OCCUPANCY, STRENGTH).peak_users == pytest.approx(30.0)


def test_membership_sets_the_peak_when_it_is_the_smaller_estimate() -> None:
    peak = estimate_peak_users(5_000.0, OCCUPANCY, GENERAL, members=1_000)
    assert peak.method == "members"
    assert peak.peak_users == pytest.approx(1_000 * PEAK_SHARE)
    assert peak.member_users == pytest.approx(1_000 * PEAK_SHARE)
    assert peak.area_users == pytest.approx(40.0)
    assert peak.members == 1_000.0


def test_area_caps_a_membership_that_would_overfill_the_floor() -> None:
    peak = estimate_peak_users(5_000.0, OCCUPANCY, GENERAL, members=5_000)
    assert peak.method == "density"
    assert peak.peak_users == pytest.approx(40.0)
    assert peak.member_users == pytest.approx(5_000 * PEAK_SHARE)
    assert peak.members == 5_000.0


def test_implied_membership_reproduces_the_area_estimate() -> None:
    by_area = estimate_peak_users(5_000.0, OCCUPANCY, GENERAL)
    assert by_area.members is not None
    by_members = estimate_peak_users(5_000.0, OCCUPANCY, GENERAL, members=round(by_area.members))
    assert by_members.peak_users == pytest.approx(by_area.peak_users, rel=1e-3)


@pytest.mark.parametrize("members", [None, 0])
def test_missing_or_zero_membership_falls_back_to_area(members: int | None) -> None:
    peak = estimate_peak_users(5_000.0, OCCUPANCY, GENERAL, members=members)
    assert peak.method == "density"
    assert peak.member_users is None
    assert peak.peak_users == pytest.approx(40.0)


def test_building_code_occupant_load_caps_the_peak() -> None:
    crowded = GENERAL.model_copy(update={"peak_users_per_1000_sqft": 30.0})
    peak = estimate_peak_users(5_000.0, OCCUPANCY, crowded)
    assert peak.area_users == pytest.approx(150.0)
    assert peak.peak_users == pytest.approx(5_000.0 / 50.0)
    assert peak.capped_by_code


@pytest.mark.parametrize(("training_sqft", "members"), [(100.0, None), (5_000.0, 10)])
def test_at_least_one_user_is_planned_for(training_sqft: float, members: int | None) -> None:
    peak = estimate_peak_users(training_sqft, OCCUPANCY, GENERAL, members=members)
    assert peak.peak_users == MIN_PEAK_USERS
    assert not peak.capped_by_code


def test_peak_never_exceeds_code_occupant_load_even_on_a_tiny_floor() -> None:
    peak = estimate_peak_users(40.0, OCCUPANCY, GENERAL)
    assert peak.peak_users <= 40.0 / OCCUPANCY.occupant_load_sqft_per_person


@pytest.mark.parametrize("training_sqft", [0.0, -10.0])
def test_floor_area_must_be_positive(training_sqft: float) -> None:
    with pytest.raises(ValueError, match="positive"):
        estimate_peak_users(training_sqft, OCCUPANCY, GENERAL)


def test_time_weight_is_popularity_times_block_length_times_multiplier() -> None:
    weights = exercise_time_weights(EXERCISES, {"deadlift": 2.0})
    assert weights["deadlift"] == pytest.approx(1.0 * 12.0 * 2.0)
    assert weights["back_squat"] == pytest.approx(2.0 * 15.0)


@pytest.mark.parametrize("profile_id", ["general", "strength"])
@pytest.mark.parametrize("members", [None, 800])
def test_loads_sum_to_active_users_split_by_modality_share(
    profile_id: str, members: int | None
) -> None:
    demand = build_demand(CATALOG, profile_id, 4_000.0, members)
    profile = CATALOG.profile_by_id[profile_id]
    assert demand.peak == estimate_peak_users(4_000.0, OCCUPANCY, profile, members)
    assert demand.active_users == pytest.approx(demand.peak.peak_users * (1 - SESSION.idle_share))
    assert demand.total_load == pytest.approx(demand.active_users)
    assert demand.modality_share == profile.modality_share.as_dict()
    shares = profile.modality_share.as_dict()
    for modality, total in modality_totals(demand.exercise_load).items():
        assert total == pytest.approx(demand.active_users * shares[modality], abs=1e-12)


def test_within_a_modality_load_follows_popularity_times_block_length() -> None:
    loads = build_demand(CATALOG, "general", 4_000.0).exercise_load
    assert loads["treadmill_run"] / loads["cycling"] == pytest.approx((3 * 25) / (2 * 20))
    assert loads["cycling"] / loads["rowing"] == pytest.approx((2 * 20) / (1 * 15))
    assert loads["db_curl"] / loads["db_press"] == pytest.approx((3 * 6) / (2 * 10))


def test_profile_multipliers_shift_load_within_a_modality_only() -> None:
    demand = build_demand(CATALOG, "strength", 4_000.0)
    loads = demand.exercise_load
    assert loads["deadlift"] / loads["back_squat"] == pytest.approx((1 * 12 * 2.0) / (2 * 15))
    assert loads["db_curl"] / loads["db_press"] == pytest.approx((3 * 6 * 0.5) / (2 * 10))
    totals = modality_totals(loads)
    assert totals["barbell"] == pytest.approx(demand.active_users * 0.35)
    assert totals["dumbbell"] == pytest.approx(demand.active_users * 0.25)


def test_modality_without_share_gets_no_load() -> None:
    loads = build_demand(CATALOG, "strength", 4_000.0).exercise_load
    assert loads["kb_swing"] == 0.0
    assert loads["stretching"] == 0.0


def test_load_scales_with_floor_area_until_membership_binds() -> None:
    small = build_demand(CATALOG, "general", 2_000.0).exercise_load
    large = build_demand(CATALOG, "general", 4_000.0).exercise_load
    for xid, load in small.items():
        assert large[xid] == pytest.approx(2 * load)
    capped_small = build_demand(CATALOG, "general", 2_000.0, members=800).exercise_load # 800 members give 13.2 design-peak users, below either floor's comfortable 16 or 32.
    capped_large = build_demand(CATALOG, "general", 4_000.0, members=800).exercise_load
    assert capped_small == pytest.approx(capped_large)
