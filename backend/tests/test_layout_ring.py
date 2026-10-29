"""Ring layouts: in small rooms equipment lines the walls around open floor.

The small-gym cases use the real catalog's footprints and clearances (a cable column keeps
72 in clear in front, a full dumbbell run is 174 in long), since that is where lining the walls
pays off; the unit lists are the optimizer's selections for those rooms, fixed here so the tests
do not depend on the optimizer.
"""

from __future__ import annotations

import math
import random
from collections import defaultdict
from collections.abc import Callable, Sequence
from dataclasses import replace
from functools import cache

import pytest

from gymplanner.catalog import Catalog, load_catalog
from gymplanner.domain import Entrance, Room
from gymplanner.layout import (
    LayoutItem,
    LayoutResult,
    LayoutRules,
    Placement,
    Rect,
    plan_layout,
    validate_layout,
)
from gymplanner.layout.engine import ENTRANCE_SHARE, _configs, _finalize, _main_aisle
from gymplanner.layout.search import search
from gymplanner.layout.stacking import Config, Context
from gymplanner.settings import get_settings
from test_layout import (
    FINAL_CHECK,
    RULES,
    assert_door_clear,
    kept_value,
    make_items,
    make_room,
    random_case,
    searched,
    typical_mix,
)

TOL = 1e-6
SMALL_GYM: tuple[tuple[str, float], ...] = (
    ("dumbbell_set_full", 1.5612),
    ("elliptical", 0.3187),
    ("upright_bike", 0.1936),
    ("cable_column", 0.1657),
    ("rig_bay", 0.1437),
    ("rower", 0.1413),
    ("adjustable_bench", 0.1296),
    ("indoor_cycle", 0.1136),
    ("accessory_pack", 0.0876),
    ("cable_column", 0.0828),
    ("air_bike", 0.0636),
    ("flat_bench", 0.0500),
    ("heavy_bag", 0.0366),
    ("flat_bench", 0.0250),
    ("flat_bench", 0.0167),
    ("stretch_area", 0.0070),
    ("stretch_area", 0.0035),
    ("stretch_area", 0.0023),
    ("stretch_area", 0.0018),
)
"""What the optimizer picks for a 1,200 sq ft general gym at a packing efficiency of 0.65."""
SMALL_GYM_FLOOR = Room(width_in=339.411, depth_in=407.294, entrance="center", ceiling_in=144.0)
"""That gym's 960 sq ft training floor, which the pick was made for."""


@cache
def catalog() -> Catalog:
    return load_catalog(get_settings().data_dir)


def real_rules() -> LayoutRules:
    space = catalog().space
    zones = sorted(space.zones, key=lambda z: z.order)
    return LayoutRules(
        main_aisle_in=space.aisles.main_aisle_in,
        secondary_aisle_in=space.aisles.secondary_aisle_in,
        zone_order=tuple(z.id for z in zones),
    )


def real_items(spec: Sequence[tuple[str, float]]) -> list[LayoutItem]:
    """Units of real equipment, as the planning service builds them."""
    seen: dict[str, int] = defaultdict(int)
    items: list[LayoutItem] = []
    for equipment_id, priority in spec:
        e = catalog().equipment_by_id[equipment_id]
        seen[equipment_id] += 1
        items.append(
            LayoutItem(
                uid=f"{equipment_id}-{seen[equipment_id]}",
                equipment_id=equipment_id,
                name=e.name,
                zone=e.zone,
                length_in=e.footprint.length_in,
                width_in=e.footprint.width_in,
                clearance=e.clearance,
                aisle_side=e.layout.aisle_side,
                against_wall=e.layout.against_wall,
                row_group=e.layout.row_group or equipment_id,
                flexible_length=e.layout.flexible_length,
                min_length_in=e.layout.min_length_in,
                priority=priority,
            )
        )
    return items


def building(area_sqft: float) -> Room:
    """A training floor of the planner's default 1 : 1.5 shape."""
    width = math.sqrt(area_sqft * 144 / 1.5)
    return Room(width_in=width, depth_in=1.5 * width, entrance="center", ceiling_in=144.0)


def backs_onto_a_wall(p: Placement, result: LayoutResult) -> bool:
    """Whether the side of the unit opposite its front touches a wall of the training floor."""
    r = p.rect
    if p.rotation == 0:
        return r.y2 >= result.depth_in - TOL
    if p.rotation == 90:
        return r.x <= TOL
    if p.rotation == 270:
        return r.x2 >= result.width_in - TOL
    return r.y <= TOL


def lining_a_side_wall(p: Placement, result: LayoutResult) -> bool:
    """Turned toward or away from a side wall, with its clearance zone reaching that wall."""
    if p.rotation not in (90, 270):
        return False
    return p.envelope.x <= TOL or p.envelope.x2 >= result.width_in - TOL


def spec_items(spec: Sequence[tuple[str, int, float]]) -> list[LayoutItem]:
    """Units as the planning service builds them from ``(equipment, count, priority)``: each
    further unit of a type is worth less than the one before."""
    return real_items([(eid, value / (k + 1)) for eid, count, value in spec for k in range(count)])


def configurations(room: Room, rules: LayoutRules) -> list[Config]:
    """Every configuration the engine weighs for the room."""
    width, depth = float(room.width_in), float(room.depth_in)
    entrance = width * ENTRANCE_SHARE[room.entrance]
    return _configs(Context(rules), width, depth, entrance)[0]


def ring_only(room: Room, items: list[LayoutItem], rules: LayoutRules) -> LayoutResult:
    """The layout the ring configurations alone give (the engine also weighs rows)."""
    return restricted(room, items, rules, lambda c: bool(c.ring))


def only(config: Config) -> Callable[[Config], bool]:
    """Picks just this configuration."""
    return lambda c: c == config


def restricted(
    room: Room, items: list[LayoutItem], rules: LayoutRules, which: Callable[[Config], bool]
) -> LayoutResult:
    """The layout the configurations ``which`` picks give on their own, without the engine's
    final check (which would hide a broken plan by dropping units)."""
    ctx = Context(rules)
    width, depth = float(room.width_in), float(room.depth_in)
    entrance = width * ENTRANCE_SHARE[room.entrance]
    configs = [c for c in _configs(ctx, width, depth, entrance)[0] if which(c)]
    order = sorted(items, key=lambda it: (-it.priority, it.uid))
    result = LayoutResult(width_in=width, depth_in=depth, entrance_x_in=entrance, zones=[], aisles=[], placements=[])
    if not configs:
        return result
    outcome = search(ctx, configs, order)
    result.placements, walkways, result.zones = _finalize(ctx, outcome.stacks)
    result.aisles = [*_main_aisle(outcome), *walkways]
    kept = {p.item.uid for p in result.placements}
    result.unplaced = [it for it in order if it.uid not in kept]
    return result


def test_a_1200_sqft_gym_lines_its_walls_and_holds_more() -> None:
    rules = real_rules()
    result = plan_layout(SMALL_GYM_FLOOR, real_items(SMALL_GYM), rules)
    assert validate_layout(result, rules) == []
    assert not any(FINAL_CHECK in w for w in result.warnings)
    assert len(result.placements) >= 14 # Rows alone (the engine before rings) placed 12 of these 19 units.

    wall_units = [p for p in result.placements if p.item.against_wall] # Equipment stands along the walls: wall units back onto one, and a side wall is lined with units turned to face the room (or, for cardio, the wall).
    assert sum(backs_onto_a_wall(p, result) for p in wall_units) >= 0.75 * len(wall_units)
    assert sum(lining_a_side_wall(p, result) for p in result.placements) >= 2

    def mean_y(zone: str) -> float: # Cardio keeps to the front, free weights to the back.
        ys = [p.rect.y + p.rect.h / 2 for p in result.placements if p.item.zone == zone]
        return sum(ys) / len(ys)

    assert mean_y("cardio") < mean_y("free_weights")


def test_a_long_dumbbell_run_gets_the_back_wall_and_the_main_aisle_a_rear_exit() -> None:
    rules = real_rules() # Two 11 ft halves cannot hold the 14.5 ft dumbbell run on their own back walls; a back wall row across the whole width can, with the main aisle reaching the back wall through a corner.
    result = ring_only(SMALL_GYM_FLOOR, real_items(SMALL_GYM), rules)
    assert validate_layout(result, rules) == []
    (rack,) = (p for p in result.placements if p.item.equipment_id == "dumbbell_set_full")
    assert rack.rotation == 0 and rack.rect.y2 >= result.depth_in - TOL
    exits = [
        a
        for a in result.aisles
        if a.y2 >= result.depth_in - TOL and min(a.w, a.h) >= rules.main_aisle_in - TOL
    ]
    assert exits
    assert all(a.x <= TOL or a.x2 >= result.width_in - TOL for a in exits)


@pytest.mark.parametrize(
    ("room", "spec", "before"),
    [
        (SMALL_GYM_FLOOR, SMALL_GYM, 12),
        ( # The 760 sq ft training floor of an 800 sq ft hotel fitness room.
            Room(width_in=277.128, depth_in=394.908, entrance="center", ceiling_in=144.0),
            (
                ("dumbbell_set_light", 1.0),
                ("elliptical", 0.6),
                ("recumbent_bike", 0.5),
                ("rower", 0.4),
                ("adjustable_bench", 0.35),
                ("air_bike", 0.3),
                ("cable_column", 0.25),
                ("rig_bay", 0.2),
                ("flat_bench", 0.18),
                ("hyperextension", 0.15),
                ("heavy_bag", 0.12),
                ("suspension_trainer_station", 0.1),
                ("wall_ball_station", 0.08),
                ("accessory_pack", 0.05),
                ("stretch_area", 0.03),
            ),
            10,
        ),
    ],
)
def test_small_rooms_hold_more_than_rows_alone(
    room: Room, spec: tuple[tuple[str, float], ...], before: int
) -> None:
    rules = real_rules()
    result = plan_layout(room, real_items(spec), rules)
    assert validate_layout(result, rules) == []
    assert len(result.placements) > before


def test_ring_configurations_alone_satisfy_the_hard_rules() -> None:
    for seed in range(1_200): # Exercise rings directly; the normal family selector could hide a ring walkway crossing a row.
        rng = random.Random(seed)
        room, items, rules = random_case(rng)
        result = ring_only(room, items, rules)
        context = f"seed {seed}: {room.width_in / 12:.0f}x{room.depth_in / 12:.0f} ft"
        assert validate_layout(result, rules) == [], context
        placed = [p.item.uid for p in result.placements]
        assert len(placed) == len(set(placed)), context


@pytest.mark.parametrize(("width", "depth"), [(23, 35), (28, 42), (32, 47), (41, 61), (60, 90)])
def test_ring_configurations_keep_zones_apart_and_units_in_them(width: float, depth: float) -> None:
    room = make_room(width, depth)
    items = make_items(typical_mix(), random.Random(width))
    result = ring_only(room, items, RULES)
    assert result.placements
    assert validate_layout(result, RULES) == []


def first_row_gap(result: LayoutResult, spine: Rect, left: bool) -> float | None:
    """Depth of floor between the front of one side of the main aisle (the training floor's
    front edge, or the back of a cross aisle there) and the clearance zone nearest it."""
    side = [
        p
        for p in result.placements
        if (p.rect.x2 <= spine.x + TOL if left else p.rect.x >= spine.x2 - TOL)
    ]
    if not side:
        return None
    cross = [a for a in result.aisles[1:2] if a.y <= TOL and a.w > spine.w]
    start = cross[0].y2 if cross else 0.0
    return max(0.0, min(p.envelope.y for p in side) - start)


@pytest.mark.parametrize(("width", "depth", "scale"), [(28, 42, 1), (32, 47, 1), (41, 61, 1), (52, 78, 2), (58, 87, 2)])
def test_rows_start_at_the_front_of_the_training_floor(
    width: float, depth: float, scale: int
) -> None:
    room = make_room(width, depth) # No empty band between the front wall (or a cross aisle) and the first row: the front-most clearance zone reaches it, on both sides of the main aisle.
    result = plan_layout(room, make_items(typical_mix(scale), random.Random(5)), RULES)
    assert validate_layout(result, RULES) == []
    for left in (True, False):
        gap = first_row_gap(result, result.aisles[0], left)
        assert gap is None or gap <= TOL


def test_a_lone_row_stays_at_the_front() -> None:
    room = make_room(40, 80) # Two machines a side: the row is not pushed to the back wall, leaving the front empty.
    items = make_items({"chest-press": 4}, random.Random(2))
    result = plan_layout(room, items, RULES)
    assert result.unplaced == []
    assert validate_layout(result, RULES) == []
    assert all(p.envelope.y <= TOL for p in result.placements)


def test_the_first_row_stands_right_behind_a_cross_aisle() -> None:
    room = make_room(14, 90) # A 14 ft floor runs its main aisle along a wall, with a cross aisle to the door across the front: the first row stands right behind it, its front clearances reaching into it.
    items = make_items({"treadmill": 4, "upright-bike": 4, "chest-press": 3, "flat-bench": 3}, random.Random(4))
    result = plan_layout(room, items, RULES)
    assert validate_layout(result, RULES) == []
    spine, cross = result.aisles[0], result.aisles[1]
    assert cross.w > spine.w and cross.y == 0.0
    assert min(p.rect.y for p in result.placements) == pytest.approx(cross.y2)


@pytest.mark.parametrize(("area", "scale"), [(5_000, 1), (10_000, 3), (20_000, 5)])
def test_medium_and_large_rooms_still_hold_everything(area: float, scale: int) -> None:
    room = building(area) # Rooms the row engine filled completely before rings existed.
    result = plan_layout(room, make_items(typical_mix(scale), random.Random(7)), RULES)
    assert result.unplaced == []
    assert validate_layout(result, RULES) == []


STRENGTH_ROOM: tuple[tuple[str, float], ...] = (
    ("smith_machine", 1.696),
    ("chest_press", 1.693),
    ("power_rack", 1.578),
    ("battle_rope_station", 1.301),
    ("lat_pulldown", 0.942),
    ("rotary_torso", 0.855),
    ("plate_loaded_row", 0.822),
    ("curved_treadmill", 0.739),
    ("fixed_barbell_set", 0.659),
    ("multi_station_gym", 0.426),
    ("biceps_curl_machine", 0.314),
    ("landmine", 0.300),
)
"""Machines and racks for a 38 x 26.5 ft gym, on its 38 x 25.2 ft training floor."""

STOREFRONT: tuple[tuple[str, int, float], ...] = (
    ("elliptical", 1, 0.476586),
    ("upright_bike", 1, 0.327874),
    ("recumbent_bike", 1, 0.356114),
    ("indoor_cycle", 1, 0.25733),
    ("air_bike", 1, 0.135131),
    ("rower", 1, 0.233968),
    ("ski_erg", 1, 0.0864151),
    ("rig_bay", 2, 0.102148),
    ("wall_ball_station", 1, 0.0334682),
    ("heavy_bag", 1, 0.0806216),
    ("kettlebell_set", 1, 0.258641),
    ("stretch_area", 6, 0.00881092),
    ("accessory_pack", 1, 0.208759),
    ("dumbbell_set_light", 1, 0.578058),
    ("dumbbell_set_full", 1, 1.79553),
    ("adjustable_bench", 2, 0.128357),
    ("flat_bench", 4, 0.0902708),
    ("lat_pulldown_row_combo", 1, 0.353531),
    ("cable_column", 2, 0.295988),
)
"""The planner's second selection for a 124 x 18 ft storefront (general, $35 per sq ft)."""


def test_a_ring_keeps_only_walkways_that_fit_between_its_rows() -> None:
    rules = real_rules() # A main-width cross walkway must fit between rows; rejected rings must leave the original row walkways intact.
    room = Room(width_in=456, depth_in=302, entrance="center", ceiling_in=144)
    items = real_items(STRENGTH_ROOM)
    result = plan_layout(room, items, rules)
    assert validate_layout(result, rules) == []
    assert not any(FINAL_CHECK in w for w in result.warnings)
    for config in configurations(room, rules):
        alone = restricted(room, items, rules, only(config))
        assert validate_layout(alone, rules) == [], (config.ring, config.mode, config.across)


def test_a_shallow_storefront_keeps_its_units() -> None:
    rules = real_rules() # The final check once removed 11 of these units: a core ring had kept a walkway that did not fit, and the whole plan shrank to 11 pieces.
    room = Room(width_in=1488, depth_in=216, entrance="center", ceiling_in=144)
    items = spec_items(STOREFRONT)
    result = plan_layout(room, items, rules)
    assert validate_layout(result, rules) == []
    assert not any(FINAL_CHECK in w for w in result.warnings)
    assert len(result.placements) >= 24
    assert kept_value(result) >= searched(room, items, False, rules).value - 1e-9


def shallow_case(seed: int) -> tuple[Room, list[LayoutItem]]:
    """A storefront-like room (25-120 ft wide, 20-36 ft deep) with 4-25 real equipment types,
    one to three units each."""
    rng = random.Random(seed)
    width, depth = rng.uniform(25, 120), rng.uniform(20, 36)
    entrance: Entrance = rng.choice(["left", "center", "right"])
    room = Room(width_in=width * 12, depth_in=depth * 12, entrance=entrance, ceiling_in=144.0)
    kinds = rng.sample([e.id for e in catalog().equipment], rng.randint(4, 25))
    counts = {eid: rng.randint(1, 3) for eid in kinds}
    return room, spec_items([(eid, n, rng.uniform(0.01, 2.0)) for eid, n in counts.items()])


def test_every_configuration_alone_is_valid_in_shallow_rooms() -> None:
    rules = real_rules() # Test every configuration in shallow rooms before the final validator can hide errors by dropping units.
    for seed in range(30):
        room, items = shallow_case(seed)
        for config in configurations(room, rules):
            result = restricted(room, items, rules, only(config))
            context = (seed, config.ring, config.mode, config.across, config.facing)
            assert validate_layout(result, rules) == [], context


@pytest.mark.parametrize("seeds", [range(0, 60), range(2_400, 2_460)])
def test_shallow_rooms_never_need_the_final_check(seeds: range) -> None:
    rules = real_rules() # A 116.5 x 22.8 ft room once lost 8 units to it.
    for seed in seeds:
        room, items = shallow_case(seed)
        result = plan_layout(room, items, rules)
        assert validate_layout(result, rules) == [], seed
        assert not any(FINAL_CHECK in w for w in result.warnings), seed


BENCHES: tuple[tuple[str, float], ...] = (
    ("dumbbell_set_full", 1.5),
    ("treadmill", 0.6),
    ("elliptical", 0.5),
    ("upright_bike", 0.4),
    ("cable_column", 0.3),
    ("cable_column", 0.25),
    ("adjustable_bench", 0.2),
    ("flat_bench", 0.15),
    ("flat_bench", 0.1),
)

GENERAL_2500: tuple[tuple[str, int, float], ...] = (
    ("treadmill", 2, 0.508813),
    ("elliptical", 2, 0.301958),
    ("upright_bike", 2, 0.138045),
    ("recumbent_bike", 1, 0.250966),
    ("indoor_cycle", 1, 0.128675),
    ("rower", 1, 0.218175),
    ("ski_erg", 1, 0.0948075),
    ("rig_bay", 2, 0.0898776),
    ("heavy_bag", 2, 0.007081),
    ("kettlebell_set", 1, 0.200774),
    ("stretch_area", 3, 0.14732),
    ("accessory_pack", 1, 0.160918),
    ("half_rack", 1, 0.343472),
    ("dumbbell_set_light", 1, 0.368395),
    ("dumbbell_set_full", 1, 1.41621),
    ("adjustable_bench", 2, 0.116295),
    ("flat_bench", 4, 0.0826669),
    ("lat_pulldown_row_combo", 1, 0.312566),
    ("cable_column", 2, 0.259833),
)
"""The planner's first selection for a 2,500 sq ft general gym (packing efficiency 0.55)."""
GENERAL_2500_FLOOR = Room(width_in=489.898, depth_in=587.878, entrance="center", ceiling_in=144.0)
"""That gym's 2,000 sq ft training floor, which the selection was made for."""


def test_benches_face_the_dumbbell_run_across_its_walkway() -> None:
    rules = real_rules() # An open ring may stand a row of benches in front of the back wall row, facing it and sharing its walkway, instead of leaving that floor empty.
    result = restricted(building(1_200), real_items(BENCHES), rules, lambda c: c.facing)
    assert validate_layout(result, rules) == []
    (rack,) = (p for p in result.placements if p.item.equipment_id == "dumbbell_set_full")
    benches = [p for p in result.placements if p.item.equipment_id == "flat_bench"]
    assert len(benches) == 2
    assert all(bench.rotation == 180 for bench in benches) # facing the back wall
    facing = [b for b in benches if b.rect.x < rack.rect.x2 and rack.rect.x < b.rect.x2]
    assert facing
    for bench in facing:
        between = Rect(bench.rect.x, bench.rect.y2, bench.rect.w, rack.rect.y - bench.rect.y2)
        assert 0 < between.h <= rack.item.clearance.front_in + rules.secondary_aisle_in # Only the rack's clear zone and the walkway lie between them, nothing else.
        assert not any(p.rect.intersects(between) for p in result.placements)
        assert any(a.contains(Rect(between.x, between.y, between.w, 1.0)) for a in result.aisles)


def test_wall_units_stay_on_the_walls_of_a_small_gym() -> None:
    rules = real_rules() # Rig bays and cable columns once stood as islands in the middle of this floor while wide free-standing units took the side walls.
    result = plan_layout(GENERAL_2500_FLOOR, spec_items(GENERAL_2500), rules)
    assert validate_layout(result, rules) == []
    wall_units = [p for p in result.placements if p.item.against_wall]
    assert len(wall_units) >= 7
    assert all(backs_onto_a_wall(p, result) for p in wall_units)


@pytest.mark.parametrize("entrance", ["left", "center", "right"])
def test_the_door_of_a_small_gym_stays_clear(entrance: Entrance) -> None:
    rules = real_rules()
    room = replace(SMALL_GYM_FLOOR, entrance=entrance)
    result = plan_layout(room, real_items(SMALL_GYM), rules)
    assert validate_layout(result, rules) == []
    assert_door_clear(result, rules.main_aisle_in)
