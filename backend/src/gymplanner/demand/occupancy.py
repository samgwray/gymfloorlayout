"""How many people are on the training floor during the design (busy-day peak) hour."""

from __future__ import annotations

from typing import Literal

from gymplanner.catalog.schema import OccupancyModel, Profile
from gymplanner.domain import PeakEstimate

MIN_PEAK_USERS = 1.0


def member_peak_share(occupancy: OccupancyModel) -> float:
    """Share of the membership on the floor at the design peak."""
    return (
        occupancy.daily_visit_rate * occupancy.peak_concurrency_share * occupancy.design_day_factor
    )


def estimate_peak_users(
    training_sqft: float,
    occupancy: OccupancyModel,
    profile: Profile,
    members: int | None = None,
) -> PeakEstimate:
    """Estimate design-peak floor occupancy.

    The floor area sets a comfortable training density. A supplied membership gives a second
    estimate (members x daily visit rate x busiest-hour concurrency x busy-day factor); the
    smaller of the two is used, because demand above what the floor holds comfortably cannot
    be served by adding equipment. The result never exceeds the building-code occupant load.
    """
    if training_sqft <= 0:
        raise ValueError("training floor area must be positive")

    density = profile.peak_users_per_1000_sqft or occupancy.peak_users_per_1000_sqft
    area_users = training_sqft / 1000.0 * density
    share = member_peak_share(occupancy)
    member_users = members * share if members else None

    method: Literal["members", "density"]
    if member_users is not None and member_users < area_users:
        users, method, member_count = member_users, "members", float(members or 0)
    else:
        users, method = area_users, "density"
        member_count = float(members) if members else area_users / share

    code_cap = training_sqft / occupancy.occupant_load_sqft_per_person
    capped = users > code_cap
    users = min(max(MIN_PEAK_USERS, users), code_cap)
    return PeakEstimate(
        peak_users=users,
        method=method,
        members=member_count,
        area_users=area_users,
        member_users=member_users,
        capped_by_code=capped,
    )
