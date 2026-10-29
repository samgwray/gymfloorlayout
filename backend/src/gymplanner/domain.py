"""Value objects passed between the engine's stages (room -> demand -> selection -> layout)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from gymplanner.catalog.schema import GradeId, Modality

SQIN_PER_SQFT = 144.0

Entrance = Literal["left", "center", "right"]


@dataclass(frozen=True)
class PlanInputs:
    """Validated user inputs, with defaults resolved against the catalog."""

    area_sqft: float
    budget_usd: float
    profile_id: str
    grade_id: GradeId
    width_ft: float | None = None
    depth_ft: float | None = None
    ceiling_ft: float | None = None
    members: int | None = None
    include_flooring: bool = True
    include_installation: bool = True
    entrance: Entrance = "center"
    excluded_equipment: tuple[str, ...] = ()


@dataclass(frozen=True)
class Room:
    """The training floor: the space given for equipment, aisles and stretching. x runs along
    the entrance wall, y runs away from it."""

    width_in: float
    depth_in: float
    entrance: Entrance
    ceiling_in: float

    @property
    def training_sqft(self) -> float:
        return self.width_in * self.depth_in / SQIN_PER_SQFT


@dataclass(frozen=True)
class PeakEstimate:
    peak_users: float
    method: Literal["members", "density"]
    """Which estimate set the design peak."""
    members: float | None
    """Membership supplied by the user, or the membership implied by the area estimate."""
    area_users: float
    """Comfortable design-peak users for the floor area."""
    member_users: float | None
    """Design-peak users implied by the supplied membership."""
    capped_by_code: bool
    """True when the building-code occupant load, not demand, limited the estimate."""


@dataclass(frozen=True)
class Demand:
    """Offered load, in Erlangs, for every exercise during the design hour."""

    profile_id: str
    peak: PeakEstimate
    active_users: float
    """Users occupying a station at a random moment (peak users minus idle time)."""
    modality_share: dict[Modality, float]
    exercise_load: dict[str, float]

    @property
    def total_load(self) -> float:
        return sum(self.exercise_load.values())
