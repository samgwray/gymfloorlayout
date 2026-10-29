"""Resolve request inputs into concrete room geometry and the allowed equipment set."""

from __future__ import annotations

import math

from gymplanner.catalog.loader import Catalog
from gymplanner.catalog.schema import Equipment
from gymplanner.domain import SQIN_PER_SQFT, PlanInputs, Room

DEFAULT_ASPECT = 1.5
"""Depth : width of the training floor when only the area is known."""


def build_room(inputs: PlanInputs, catalog: Catalog) -> Room:
    """The training floor's rectangle: the whole area given is for equipment."""
    width_in, depth_in = _dimensions(inputs, inputs.area_sqft * SQIN_PER_SQFT)
    ceiling_in = inputs.ceiling_ft * 12 if inputs.ceiling_ft else catalog.space.default_ceiling_in
    return Room(width_in=width_in, depth_in=depth_in, entrance=inputs.entrance, ceiling_in=ceiling_in)


def _dimensions(inputs: PlanInputs, area_sqin: float) -> tuple[float, float]:
    if inputs.width_ft and inputs.depth_ft:
        return inputs.width_ft * 12, inputs.depth_ft * 12 # Explicit dimensions win; the area is rescaled to match them.
    if inputs.width_ft:
        width = inputs.width_ft * 12
        return width, area_sqin / width
    if inputs.depth_ft:
        depth = inputs.depth_ft * 12
        return area_sqin / depth, depth
    width = math.sqrt(area_sqin / DEFAULT_ASPECT)
    return width, width * DEFAULT_ASPECT


def envelope_dims(item: Equipment, use_min_length: bool = True) -> tuple[float, float]:
    """(depth, width) of footprint plus clearances in the equipment's own orientation."""
    length = item.footprint.length_in
    if use_min_length and item.layout.flexible_length and item.layout.min_length_in:
        length = min(length, item.layout.min_length_in)
    c = item.clearance
    return length + c.front_in + c.back_in, item.footprint.width_in + c.left_in + c.right_in


def envelope_area_sqin(item: Equipment) -> float:
    """Footprint plus clearances at the catalog length."""
    depth, width = envelope_dims(item, use_min_length=False)
    return depth * width


def fits_room(item: Equipment, room: Room) -> bool:
    depth, width = envelope_dims(item)
    floor_w, floor_d = room.width_in, room.depth_in
    return (depth <= floor_d and width <= floor_w) or (depth <= floor_w and width <= floor_d)


def effective_area_sqin(item: Equipment) -> float:
    """Area one unit claims on a packed floor.

    Clearance zones may overlap neighbouring clearance zones and aisles, so on a packed floor
    each unit effectively owns its footprint plus about half of its clearance on every side.
    """
    c = item.clearance
    return (item.footprint.length_in + (c.front_in + c.back_in) / 2) * (
        item.footprint.width_in + (c.left_in + c.right_in) / 2
    )
