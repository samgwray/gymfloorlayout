"""Geometry and result types for floor layout.

Coordinates are inches. The origin is the front-left corner of the training floor; x runs
along the entrance wall and y runs from the entrance wall toward the back wall.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from gymplanner.catalog.schema import Clearance, ZoneId

Rotation = Literal[0, 90, 180, 270]
"""Direction the equipment's front faces: 0 = toward the entrance wall (-y), clockwise."""


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    w: float
    h: float

    @property
    def x2(self) -> float:
        return self.x + self.w

    @property
    def y2(self) -> float:
        return self.y + self.h

    @property
    def area(self) -> float:
        return self.w * self.h

    def intersects(self, other: Rect, tolerance: float = 1e-6) -> bool:
        """True when the interiors overlap; touching edges do not count."""
        return (
            self.x < other.x2 - tolerance
            and other.x < self.x2 - tolerance
            and self.y < other.y2 - tolerance
            and other.y < self.y2 - tolerance
        )

    def contains(self, other: Rect, tolerance: float = 1e-6) -> bool:
        return (
            other.x >= self.x - tolerance
            and other.y >= self.y - tolerance
            and other.x2 <= self.x2 + tolerance
            and other.y2 <= self.y2 + tolerance
        )

    def expanded(self, left: float, top: float, right: float, bottom: float) -> Rect:
        """Grow each side; ``top`` is toward -y (the entrance), ``bottom`` toward +y."""
        return Rect(self.x - left, self.y - top, self.w + left + right, self.h + top + bottom)


@dataclass(frozen=True)
class LayoutItem:
    """One physical unit to place."""

    uid: str
    equipment_id: str
    name: str
    zone: ZoneId
    length_in: float
    """Front-to-back size as the user faces the equipment."""
    width_in: float
    clearance: Clearance
    aisle_side: Literal["front", "back", "side", "any"] = "front"
    against_wall: bool = False
    row_group: str = ""
    flexible_length: bool = False
    min_length_in: float | None = None
    priority: float = 0.0
    """Higher keeps the item when space runs out (the optimizer's marginal value)."""
    pairs_with: str = ""
    """Row group of the wall units this unit is used with (a bench with a dumbbell run): where
    they stand along the back wall, it goes in a row facing them across their walkway."""


@dataclass(frozen=True)
class Placement:
    item: LayoutItem
    rect: Rect
    """Footprint as placed, after rotation (and any flexible-length shortening)."""
    envelope: Rect
    """Footprint plus clearances as placed."""
    rotation: Rotation


@dataclass(frozen=True)
class ZoneRect:
    zone: ZoneId
    rect: Rect


@dataclass(frozen=True)
class LayoutRules:
    main_aisle_in: float
    secondary_aisle_in: float
    zone_order: tuple[ZoneId, ...]
    """Zones from the entrance toward the back wall."""


@dataclass
class LayoutResult:
    width_in: float
    depth_in: float
    entrance_x_in: float
    zones: list[ZoneRect]
    aisles: list[Rect]
    placements: list[Placement]
    unplaced: list[LayoutItem] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    """How the floor was laid out, such as the main aisle's route; nothing to act on."""
