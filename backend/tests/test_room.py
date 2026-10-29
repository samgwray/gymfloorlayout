"""Room geometry: envelopes, packed-floor area per unit, rotation-aware fit, and room sizing."""

from __future__ import annotations

from dataclasses import fields
from typing import Any

import pytest

from gymplanner.catalog.loader import Catalog
from gymplanner.catalog.schema import (
    AisleRules,
    Clearance,
    Dimensions,
    Equipment,
    LayoutHints,
    PriceTiers,
    SpaceFile,
    ZoneSpec,
)
from gymplanner.domain import SQIN_PER_SQFT, PlanInputs, Room
from gymplanner.planning.room import (
    DEFAULT_ASPECT,
    build_room,
    effective_area_sqin,
    envelope_dims,
    fits_room,
)


def make_equipment(
    length_in: float,
    width_in: float,
    front_in: float = 0.0,
    back_in: float = 0.0,
    left_in: float = 0.0,
    right_in: float = 0.0,
    flexible_length: bool = False,
    min_length_in: float | None = None,
) -> Equipment:
    return Equipment(
        id="unit",
        name="Unit",
        category="functional",
        zone="functional",
        description="fixture",
        footprint=Dimensions(length_in=length_in, width_in=width_in),
        clearance=Clearance(front_in=front_in, back_in=back_in, left_in=left_in, right_in=right_in),
        price_usd=PriceTiers(value=100, commercial=200, premium=300),
        layout=LayoutHints(flexible_length=flexible_length, min_length_in=min_length_in),
        sources=["fixture"],
    )


def make_room(width_in: float, depth_in: float) -> Room:
    return Room(width_in=width_in, depth_in=depth_in, entrance="center", ceiling_in=120.0)


TREADMILL = make_equipment(84, 36, front_in=24, back_in=79, left_in=19.7, right_in=19.7) # A treadmill: 84 x 36 in deck, 24 in in front, 79 in behind, 19.7 in on each side.


def test_effective_area_takes_half_of_each_clearance() -> None:
    expected = (84 + (24 + 79) / 2) * (36 + (19.7 + 19.7) / 2)
    assert effective_area_sqin(TREADMILL) == pytest.approx(expected)


def test_effective_area_without_clearance_is_the_footprint() -> None:
    assert effective_area_sqin(make_equipment(80, 30)) == pytest.approx(80 * 30)


def test_effective_area_lies_between_footprint_and_envelope() -> None:
    depth, width = envelope_dims(TREADMILL)
    assert 84 * 36 < effective_area_sqin(TREADMILL) < depth * width


def test_effective_area_depends_only_on_total_clearance_per_axis() -> None:
    mirrored = make_equipment(84, 36, front_in=79, back_in=24, left_in=10, right_in=29.4)
    assert effective_area_sqin(mirrored) == pytest.approx(effective_area_sqin(TREADMILL))


def test_envelope_adds_clearance_on_every_side() -> None:
    assert envelope_dims(TREADMILL) == pytest.approx((84 + 24 + 79, 36 + 19.7 + 19.7))


def test_flexible_length_shrinks_to_its_minimum() -> None:
    turf = make_equipment(600, 72, front_in=12, back_in=12, flexible_length=True, min_length_in=240)
    assert envelope_dims(turf) == pytest.approx((240 + 24, 72))
    assert envelope_dims(turf, use_min_length=False) == pytest.approx((600 + 24, 72))


@pytest.mark.parametrize(
    ("flexible", "min_length", "expected_length"),
    [
        (True, None, 600), # flexible but no floor given: keep the full length
        (False, 240, 600), # a minimum only matters when the length may flex
        (True, 900, 600), # a minimum longer than the item never stretches it
    ],
)
def test_minimum_length_applies_only_when_it_shortens_a_flexible_item(
    flexible: bool, min_length: float | None, expected_length: float
) -> None:
    item = make_equipment(600, 72, flexible_length=flexible, min_length_in=min_length)
    assert envelope_dims(item) == pytest.approx((expected_length, 72))


@pytest.mark.parametrize(
    ("length_in", "width_in", "fits"),
    [
        (100, 40, True), # as built: 100 deep in 150 of training depth
        (180, 40, True), # only when turned to run along the 200 in wall
        (40, 180, True), # already runs along the wall
        (220, 40, False), # longer than both sides
        (160, 160, False), # deeper than the 150 in floor whichever way it faces
        (150, 200, True), # exactly the floor
        (200, 150, True), # exactly the floor, rotated
    ],
)
def test_fits_room_tries_both_orientations(length_in: float, width_in: float, fits: bool) -> None:
    room = make_room(width_in=200, depth_in=150)
    assert fits_room(make_equipment(length_in, width_in), room) is fits


def test_fits_room_counts_clearance() -> None:
    room = make_room(width_in=200, depth_in=150)
    assert fits_room(make_equipment(100, 40), room)
    assert not fits_room(make_equipment(100, 40, front_in=60, back_in=60, left_in=90), room)


def test_flexible_item_fits_at_its_minimum_length() -> None:
    room = make_room(width_in=300, depth_in=360)
    turf = make_equipment(600, 72, flexible_length=True, min_length_in=240)
    rigid = make_equipment(600, 72)
    assert fits_room(turf, room)
    assert not fits_room(rigid, room)


def make_catalog() -> Catalog:
    """Catalog with only the section build_room reads, space; the others stay empty so the
    fixture does not churn as the catalog grows."""
    space = SpaceFile(
        version=1,
        aisles=AisleRules(main_aisle_in=60, secondary_aisle_in=36, sources=["fixture"]),
        circulation_share=0.35,
        packing_efficiency=0.6,
        zones=[ZoneSpec(id="cardio", name="Cardio", order=0, flooring="rubber", description="")],
        default_ceiling_in=132.0,
        sources=["fixture"],
    )
    sections: dict[str, Any] = {f.name: () for f in fields(Catalog) if f.name != "data_version"}
    sections.update(space=space)
    return Catalog(**sections)


CATALOG = make_catalog()


def make_inputs(
    area_sqft: float,
    width_ft: float | None = None,
    depth_ft: float | None = None,
    ceiling_ft: float | None = None,
) -> PlanInputs:
    return PlanInputs(
        area_sqft=area_sqft,
        budget_usd=100_000,
        profile_id="general",
        grade_id="commercial",
        width_ft=width_ft,
        depth_ft=depth_ft,
        ceiling_ft=ceiling_ft,
        entrance="left",
    )


@pytest.mark.parametrize("area_sqft", [150.0, 2_400.0, 8_000.0, 40_000.0])
def test_area_alone_gives_a_room_of_the_default_aspect(area_sqft: float) -> None:
    room = build_room(make_inputs(area_sqft), CATALOG)
    assert room.training_sqft == pytest.approx(area_sqft)
    assert room.depth_in / room.width_in == pytest.approx(DEFAULT_ASPECT)
    assert room.entrance == "left"


def test_one_given_side_sets_the_other_from_the_area() -> None:
    by_width = build_room(make_inputs(3_000.0, width_ft=40.0), CATALOG)
    assert (by_width.width_in, by_width.depth_in) == pytest.approx((480.0, 3_000 * 144 / 480))
    by_depth = build_room(make_inputs(3_000.0, depth_ft=60.0), CATALOG)
    assert (by_depth.width_in, by_depth.depth_in) == pytest.approx((3_000 * 144 / 720, 720.0))


def test_both_sides_given_win_over_the_area() -> None:
    room = build_room(make_inputs(5_000.0, width_ft=50.0, depth_ft=80.0), CATALOG)
    assert (room.width_in, room.depth_in) == pytest.approx((600.0, 960.0))


@pytest.mark.parametrize("area_sqft", [800.0, 2_400.0, 8_000.0, 40_000.0])
def test_the_whole_area_is_training_floor(area_sqft: float) -> None:
    for inputs in (make_inputs(area_sqft), make_inputs(area_sqft, width_ft=20.0)): # Reception, locker rooms and restrooms are the operator's to add: nothing is set aside.
        room = build_room(inputs, CATALOG)
        assert room.training_sqft == pytest.approx(area_sqft)
        assert room.width_in * room.depth_in == pytest.approx(area_sqft * SQIN_PER_SQFT)


def test_ceiling_comes_from_inputs_or_the_dataset_default() -> None:
    assert build_room(make_inputs(2_400.0, ceiling_ft=14.0), CATALOG).ceiling_in == 168.0
    assert build_room(make_inputs(2_400.0), CATALOG).ceiling_in == 132.0
