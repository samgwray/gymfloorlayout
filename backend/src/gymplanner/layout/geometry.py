"""Orientation conventions and rectangle helpers shared by the layout engine and validator.

Directions are compass-style in plan view with the entrance wall at the top: ``n`` points
toward the entrance wall (-y), ``s`` toward the back wall (+y), ``w`` toward x = 0 and ``e``
toward x = width. A rotation names the direction the equipment's front faces, turning
clockwise as drawn: 0 = n, 90 = e, 180 = s, 270 = w. The item's other sides turn with it:

======== ===== ===== ===== =====
rotation front right back  left
======== ===== ===== ===== =====
0        n     e     s     w
90       e     s     w     n
180      s     w     n     e
270      w     n     e     s
======== ===== ===== ===== =====

So at rotation 0 the front clearance extends toward the entrance, the back clearance toward
the back wall, the left clearance toward x = 0 and the right clearance toward x = width.
"""

from __future__ import annotations

from typing import Literal

from gymplanner.catalog.schema import Clearance
from gymplanner.layout.types import LayoutItem, Rect, Rotation

Direction = Literal["n", "e", "s", "w"]
Side = Literal["front", "right", "back", "left"]

DIRECTIONS: tuple[Direction, ...] = ("n", "e", "s", "w")
ROTATIONS: tuple[Rotation, ...] = (0, 90, 180, 270)
OPPOSITE: dict[Direction, Direction] = {"n": "s", "s": "n", "e": "w", "w": "e"}
ACCESS_SIDES: dict[str, tuple[Side, ...]] = {
    "front": ("front",),
    "back": ("back",),
    "side": ("left", "right"),
    "any": ("front", "back", "left", "right"),
}
"""Sides of the footprint that satisfy each ``aisle_side`` value."""

_CLOCKWISE_FROM_FRONT: dict[Side, int] = {"front": 0, "right": 1, "back": 2, "left": 3}
TOL = 1e-6


def facing(rotation: Rotation, side: Side) -> Direction:
    """World direction that one side of the equipment faces at a rotation."""
    return DIRECTIONS[(rotation // 90 + _CLOCKWISE_FROM_FRONT[side]) % 4]


def side_clearance(clearance: Clearance, side: Side) -> float:
    return float(getattr(clearance, f"{side}_in"))


def clearance_by_direction(clearance: Clearance, rotation: Rotation) -> dict[Direction, float]:
    """Clearances keyed by the world direction they extend toward."""
    return {
        facing(rotation, side): side_clearance(clearance, side) for side in _CLOCKWISE_FROM_FRONT
    }


def footprint_size(width_in: float, length_in: float, rotation: Rotation) -> tuple[float, float]:
    """(x extent, y extent) of a footprint: the length runs along y when facing n or s."""
    if rotation in (0, 180):
        return width_in, length_in
    return length_in, width_in


def envelope_of(rect: Rect, clear: dict[Direction, float]) -> Rect:
    return rect.expanded(left=clear["w"], top=clear["n"], right=clear["e"], bottom=clear["s"])


def item_envelope(item: LayoutItem, rect: Rect, rotation: Rotation) -> Rect:
    return envelope_of(rect, clearance_by_direction(item.clearance, rotation))


def strip_beside(rect: Rect, direction: Direction, depth: float) -> Rect:
    """The ``depth``-deep strip along one side of ``rect``, as long as that side."""
    if direction == "n":
        return Rect(rect.x, rect.y - depth, rect.w, depth)
    if direction == "s":
        return Rect(rect.x, rect.y2, rect.w, depth)
    if direction == "w":
        return Rect(rect.x - depth, rect.y, depth, rect.h)
    return Rect(rect.x2, rect.y, depth, rect.h)


def approach_depth(clearance: Clearance, side: Side, min_depth: float) -> float:
    """Depth of the clear zone users need on an access side."""
    return max(side_clearance(clearance, side), min_depth)


def touches(a: Rect, b: Rect, tol: float = TOL) -> bool:
    """True when two rects overlap or share a stretch of edge (a corner alone does not count)."""
    ox = min(a.x2, b.x2) - max(a.x, b.x)
    oy = min(a.y2, b.y2) - max(a.y, b.y)
    return (ox > tol and oy >= -tol) or (oy > tol and ox >= -tol)
