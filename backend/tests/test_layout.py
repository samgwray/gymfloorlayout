"""Floor layout engine and validator.

The catalog below is synthetic but uses real-world footprints and manufacturer / standards
clearances (e.g. a treadmill keeps a 79 in (2 m) safety zone behind it), so the property tests
exercise the same geometry the planner sees in production.
"""

from __future__ import annotations

import math
import random
import time
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Literal, cast

import pytest

from gymplanner.catalog.schema import Clearance, ZoneId
from gymplanner.domain import Entrance, Room
from gymplanner.layout import (
    LayoutItem,
    LayoutResult,
    LayoutRules,
    Placement,
    Rect,
    Rotation,
    ZoneRect,
    engine,
    fits_alone,
    plan_layout,
    validate_layout,
)
from gymplanner.layout.engine import ENTRANCE_SHARE, _configs, _rank
from gymplanner.layout.geometry import clearance_by_direction, facing, footprint_size
from gymplanner.layout.search import Outcome, search
from gymplanner.layout.stacking import Config, Context

ZONE_ORDER: tuple[ZoneId, ...] = ("cardio", "machines", "free_weights", "functional", "stretching")
RULES = LayoutRules(main_aisle_in=48.0, secondary_aisle_in=36.0, zone_order=ZONE_ORDER)
FINAL_CHECK = "final clearance check"


@dataclass(frozen=True)
class Kind:
    id: str
    zone: ZoneId
    length: float
    """Front to back, as the user faces the equipment."""
    width: float
    clearance: tuple[float, float, float, float]
    """front, back, left, right."""
    aisle_side: Literal["front", "back", "side", "any"] = "front"
    against_wall: bool = False
    flexible: bool = False
    min_length: float | None = None
    pairs_with: str = ""


KINDS: tuple[Kind, ...] = (
    Kind("treadmill", "cardio", 84, 35, (12, 79, 20, 20), "back"),
    Kind("elliptical", "cardio", 80, 30, (12, 24, 20, 20), "back"),
    Kind("upright-bike", "cardio", 44, 24, (12, 12, 20, 20), "side"),
    Kind("recumbent-bike", "cardio", 64, 28, (12, 12, 20, 20), "side"),
    Kind("rower", "cardio", 96, 24, (12, 12, 24, 24), "side"),
    Kind("stair-climber", "cardio", 60, 40, (12, 24, 20, 20), "back"),
    Kind("air-bike", "cardio", 50, 25, (12, 24, 20, 20), "side"),
    Kind("ski-erg", "cardio", 48, 24, (36, 12, 12, 12), "front"),
    Kind("chest-press", "machines", 60, 45, (24, 24, 24, 24)),
    Kind("lat-pulldown", "machines", 55, 50, (24, 24, 24, 24)),
    Kind("leg-press", "machines", 84, 55, (24, 24, 24, 24), "side"),
    Kind("leg-extension", "machines", 50, 45, (24, 24, 24, 24)),
    Kind("seated-row", "machines", 70, 40, (24, 24, 24, 24)),
    Kind("smith-machine", "machines", 50, 85, (36, 24, 24, 24)),
    Kind("functional-trainer", "machines", 40, 60, (72, 12, 12, 12)),
    Kind("cable-crossover", "machines", 40, 160, (72, 0, 12, 12), against_wall=True),
    Kind("power-rack", "free_weights", 54, 50, (48, 24, 36, 36)),
    Kind("flat-bench", "free_weights", 50, 26, (24, 24, 24, 24), "side", pairs_with="dumbbell-rack"), # Benches are used with the dumbbells, so they stand facing a dumbbell run.
    Kind("adjustable-bench", "free_weights", 55, 26, (24, 24, 24, 24), "side", pairs_with="dumbbell-rack"),
    Kind("dumbbell-rack", "free_weights", 26, 92, (36, 0, 12, 12), against_wall=True),
    Kind("lifting-platform", "free_weights", 96, 96, (24, 24, 24, 24), "any"),
    Kind("plate-tree", "free_weights", 24, 24, (12, 12, 12, 12), "any"),
    Kind("turf-lane", "functional", 600, 72, (24, 24, 12, 12), "any", flexible=True, min_length=240),
    Kind("rig", "functional", 48, 120, (48, 0, 24, 24), against_wall=True),
    Kind("heavy-bag", "functional", 24, 24, (36, 0, 36, 36), "any", against_wall=True),
    Kind("stretch-mat", "stretching", 72, 48, (12, 12, 12, 12), "any"),
    Kind("stretch-station", "stretching", 60, 40, (24, 12, 12, 12)),
)
KIND = {k.id: k for k in KINDS}


def unit(kind: Kind, n: int, priority: float) -> LayoutItem:
    f, b, left, right = kind.clearance
    return LayoutItem(
        uid=f"{kind.id}-{n}",
        equipment_id=kind.id,
        name=kind.id.replace("-", " ").title(),
        zone=kind.zone,
        length_in=kind.length,
        width_in=kind.width,
        clearance=Clearance(front_in=f, back_in=b, left_in=left, right_in=right),
        aisle_side=kind.aisle_side,
        against_wall=kind.against_wall,
        row_group=kind.id,
        flexible_length=kind.flexible,
        min_length_in=kind.min_length,
        priority=priority,
        pairs_with=kind.pairs_with,
    )


def make_items(counts: Mapping[str, int], rng: random.Random) -> list[LayoutItem]:
    """Units with service-like priorities: each extra unit of a type is worth less."""
    items: list[LayoutItem] = []
    for kind_id, count in counts.items():
        value = rng.uniform(1.0, 10.0)
        items += [unit(KIND[kind_id], n + 1, value / (n + 1)) for n in range(count)]
    return items


def make_room(width_ft: float, depth_ft: float, entrance: Entrance = "center") -> Room:
    return Room(width_in=width_ft * 12, depth_in=depth_ft * 12, entrance=entrance, ceiling_in=144.0)


def envelope_area(item: LayoutItem) -> float:
    c = item.clearance
    return (item.length_in + c.front_in + c.back_in) * (item.width_in + c.left_in + c.right_in)


def typical_mix(scale: int = 1) -> dict[str, int]:
    base = {
        "treadmill": 4,
        "elliptical": 2,
        "upright-bike": 2,
        "rower": 1,
        "stair-climber": 1,
        "chest-press": 1,
        "lat-pulldown": 1,
        "leg-press": 1,
        "seated-row": 1,
        "cable-crossover": 1,
        "power-rack": 2,
        "flat-bench": 2,
        "adjustable-bench": 2,
        "dumbbell-rack": 2,
        "turf-lane": 1,
        "rig": 1,
        "stretch-mat": 2,
    }
    return {k: v * scale for k, v in base.items()}


def random_case(rng: random.Random) -> tuple[Room, list[LayoutItem], LayoutRules]:
    width = rng.choice([12, 15, 20, 28, 40, 60, 90, 140, 250, rng.uniform(12, 250)])
    depth = rng.choice([15, 20, 30, 45, 70, 110, 180, 400, rng.uniform(15, 400)])
    entrance: Entrance = rng.choice(["left", "center", "right"])
    order = list(ZONE_ORDER)
    if rng.random() < 0.3:
        rng.shuffle(order)
    rules = LayoutRules(
        main_aisle_in=rng.choice([44.0, 48.0, 60.0]),
        secondary_aisle_in=rng.choice([30.0, 36.0, 42.0]),
        zone_order=tuple(order),
    )
    target = rng.choice([0, 1, 3, 10, 30, 80, 200]) * min(1.0, width * depth / 4000) # From empty plans to many times what the floor can hold.
    kinds = rng.sample(KINDS, rng.randint(1, len(KINDS)))
    counts = {k.id: rng.randint(0, max(1, round(2 * target / len(kinds)))) for k in kinds}
    return make_room(width, depth, entrance), make_items(counts, rng), rules


def placed_ids(result: LayoutResult) -> set[str]:
    return {p.item.uid for p in result.placements}


def length_of(p: Placement) -> float:
    """Front-to-back size as placed (shorter than nominal for a shortened flexible unit)."""
    return p.rect.h if p.rotation in (0, 180) else p.rect.w


def one_per_type(items: Sequence[LayoutItem]) -> list[LayoutItem]:
    """The most valuable unit of each equipment type (units of a type are interchangeable)."""
    seen: set[str] = set()
    out: list[LayoutItem] = []
    for item in sorted(items, key=lambda it: (-it.priority, it.uid)):
        if item.equipment_id not in seen:
            seen.add(item.equipment_id)
            out.append(item)
    return out


def all_fit(room: Room, items: list[LayoutItem], rules: LayoutRules = RULES) -> bool:
    return not plan_layout(room, items, rules).unplaced


def searched(
    room: Room, items: Sequence[LayoutItem], ring: bool | None = None, rules: LayoutRules = RULES
) -> Outcome:
    """The engine's search outcome, limited to one family of configurations (rows, or rings
    when ``ring``) unless ``ring`` is None."""
    ctx = Context(rules)
    width, depth = float(room.width_in), float(room.depth_in)
    configs, _ = _configs(ctx, width, depth, width * ENTRANCE_SHARE[room.entrance])
    if ring is not None:
        configs = [c for c in configs if bool(c.ring) == ring]
    return search(ctx, configs, sorted(items, key=lambda it: (-it.priority, it.uid)), _rank)


def family_fits(room: Room, items: Sequence[LayoutItem], ring: bool) -> bool:
    return len(searched(room, items, ring).kept) == len(items)


def kept_value(result: LayoutResult) -> float:
    return math.fsum(p.item.priority for p in result.placements)


def assert_door_clear(result: LayoutResult, main_aisle_in: float) -> None:
    """The entrance leads straight into the main aisle: an aisle starting on the front edge of
    the training floor takes in a main-aisle-wide gate centred on the door (moved inside the
    floor when the door is near a side wall), and no unit stands within a main aisle's width
    of the door."""
    width = min(main_aisle_in, result.width_in)
    x = min(max(result.entrance_x_in - width / 2, 0.0), result.width_in - width)
    door = Rect(x, 0.0, width, 1.0)
    assert any(a.y <= 1e-6 and a.contains(door) for a in result.aisles), door
    gate = Rect(x, 0.0, width, min(main_aisle_in, result.depth_in))
    assert not any(p.rect.intersects(gate) for p in result.placements), gate


def behind_a_later_zone(result: LayoutResult, depth_in: float) -> list[tuple[str, str]]:
    """Pairs ``(a, b)`` on one side of the main aisle where ``a`` sits wholly behind ``b``
    although its zone comes first; units against the back wall are exempt, and so are units
    that follow a back wall run (benches facing their dumbbells)."""
    rank = {z: i for i, z in enumerate(ZONE_ORDER)}
    spine = result.aisles[0]
    pairs: list[tuple[str, str]] = []
    for left in (True, False):
        units = [
            p
            for p in result.placements
            if (p.rect.x2 <= spine.x + 1e-6 if left else p.rect.x >= spine.x2 - 1e-6)
            and depth_in - p.rect.y2 > 1e-6
            and not p.item.pairs_with
        ]
        pairs += [
            (a.item.uid, b.item.uid)
            for a in units
            for b in units
            if rank[a.item.zone] < rank[b.item.zone] and a.rect.y >= b.rect.y2 - 1e-6
        ]
    return pairs


def test_random_rooms_and_mixes_always_satisfy_the_hard_rules() -> None:
    for seed in range(240):
        rng = random.Random(seed)
        room, items, rules = random_case(rng)
        result = plan_layout(room, items, rules)
        context = f"seed {seed}: {room.width_in / 12:.0f}x{room.depth_in / 12:.0f} ft"
        assert validate_layout(result, rules) == [], context
        assert not any(FINAL_CHECK in w for w in result.warnings), context
        placed = [p.item.uid for p in result.placements]
        unplaced = [it.uid for it in result.unplaced]
        assert len(placed) == len(set(placed)), context
        assert sorted(placed + unplaced) == sorted(it.uid for it in items), context
        priorities = [it.priority for it in result.unplaced] # Unplaced units come back most valuable first, as the planner reports them.
        assert priorities == sorted(priorities, reverse=True), context


@pytest.mark.parametrize(("main", "secondary"), [(24.0, 36.0), (30.0, 42.0)])
def test_a_main_aisle_rule_narrower_than_the_walkways_still_gives_valid_plans(
    main: float, secondary: float
) -> None:
    rules = LayoutRules(main_aisle_in=main, secondary_aisle_in=secondary, zone_order=ZONE_ORDER) # The rules allow it; the spine is still built as wide as a walkway.
    for i, (width, depth) in enumerate([(30, 40), (60, 80), (14, 90), (150, 25)]):
        result = plan_layout(make_room(width, depth), make_items(typical_mix(), random.Random(i)), rules)
        assert result.placements
        assert validate_layout(result, rules) == [], f"{width}x{depth} ft"
        assert min(result.aisles[0].w, result.aisles[0].h) >= secondary


def test_everything_fits_when_the_envelopes_need_well_under_the_floor_area() -> None:
    shapes = [(30, 40), (40, 60), (60, 40), (50, 100), (80, 80), (120, 60), (200, 300)]
    shapes += [(150, 25), (70, 30), (200, 30), (120, 22), (100, 20)] # Wide and shallow floors fit only a row or two, so zones share rows there.
    shapes += [(20, 150), (24, 200)]
    rng = random.Random(11)
    checked = 0
    for width, depth in shapes:
        room = make_room(width, depth)
        floor_area = room.width_in * room.depth_in
        for _ in range(6):
            kinds = rng.sample(KINDS, rng.randint(3, len(KINDS)))
            items = make_items({k.id: rng.randint(1, 4) for k in kinds}, rng)
            while items and sum(envelope_area(it) for it in items) > 0.3 * floor_area:
                items.pop(rng.randrange(len(items)))
            result = plan_layout(room, items, RULES)
            assert result.unplaced == [], f"{width}x{depth}: {[i.uid for i in result.unplaced]}"
            assert validate_layout(result, RULES) == []
            checked += 1
    assert checked == 6 * len(shapes)


def test_wide_shallow_floors_hold_a_whole_gym() -> None:
    room = make_room(150, 25) # 150 x 25 ft holds two rows a side: with one zone per row, zones would be left out.
    result = plan_layout(room, make_items(typical_mix(), random.Random(3)), RULES)
    assert result.unplaced == []
    assert validate_layout(result, RULES) == []
    spine = result.aisles[0]

    def zones_in_row_of(p: Placement) -> set[str]:
        """Zones beside ``p`` on its side of the main aisle, at the same depth."""
        return {
            q.item.zone
            for q in result.placements
            if (q.rect.x < spine.x) == (p.rect.x < spine.x)
            and q.rect.y < p.rect.y2
            and p.rect.y < q.rect.y2
        }

    assert max(len(zones_in_row_of(p)) for p in result.placements) >= 2


def test_a_unit_that_does_not_fit_does_not_drop_the_units_after_it() -> None:
    spec = [ # The adjustable bench finds no row of its own; everything else still fits, and with rows shared between zones the bench does too.
        ("upright-bike", 8.44),
        ("stretch-mat", 8.40),
        ("seated-row", 6.91),
        ("stretch-mat", 1.68),
        ("rower", 1.17),
        ("cable-crossover", 0.83),
        ("adjustable-bench", 0.75),
        ("upright-bike", 0.56),
        ("rig", 0.54),
        ("rig", 0.32),
        ("rower", 0.29),
        ("elliptical", 0.16),
        ("treadmill", 0.15),
        ("treadmill", 0.13),
    ]
    items = [unit(KIND[kind], i, priority) for i, (kind, priority) in enumerate(spec)]
    result = plan_layout(make_room(70, 25.5), items, RULES)
    assert result.unplaced == []
    assert validate_layout(result, RULES) == []

    room, items, rules = random_case(random.Random(1184)) # Feasibility is not monotone in the number of units: here the 28-unit priority prefix does not stack but the 29-unit one does, which a bisection alone misses.
    assert len(plan_layout(room, items, rules).placements) >= 29


@pytest.mark.parametrize(
    ("width", "depth", "scale", "seed"),
    [(35, 39.6, 3, 5), (70, 26.4, 2, 7), (70, 30, 2, 7), (20, 22, 1, 3)], # On 70 x 30 ft a rig fits beside the kept units only in a configuration that cannot stack the kept units on their own: stacking is not monotone.
)
def test_left_out_units_would_not_fit_beside_the_kept_ones(
    width: float, depth: float, scale: int, seed: int
) -> None:
    room = make_room(width, depth)
    items = make_items(typical_mix(scale), random.Random(seed))
    result = plan_layout(room, items, RULES)
    assert result.placements and result.unplaced
    assert validate_layout(result, RULES) == []
    ring = bool(searched(room, items).config.ring) # The plan comes from the family of configurations (rows, or rings) that keeps the most priority; within that family no unit is crowded out by cheaper ones.
    kept = [p.item for p in result.placements]
    for left_out in one_per_type(result.unplaced):
        assert not family_fits(room, [*kept, left_out], ring), left_out.uid # Not on top of the plan as returned ...
        better = [it for it in kept if it.priority > left_out.priority] # ... nor on top of just the more valuable units it lost to.
        assert not family_fits(room, [*better, left_out], ring), left_out.uid


@pytest.mark.parametrize(("width", "depth"), [(10, 15), (12, 20), (15, 15), (20, 30), (8, 40)])
def test_fits_alone_agrees_with_laying_each_unit_out_on_its_own(width: float, depth: float) -> None:
    rules = LayoutRules(main_aisle_in=60.0, secondary_aisle_in=36.0, zone_order=ZONE_ORDER) # The planner keeps the optimizer from spending on units the floor can never hold.
    room = make_room(width, depth)
    items = [unit(kind, 1, 1.0) for kind in KINDS]
    alone = {it.uid for it in fits_alone(room, items, rules)}
    placed = {it.uid for it in items if plan_layout(room, [it], rules).placements}
    assert alone == placed


def test_units_too_big_for_the_floor_are_left_out_without_blocking_others() -> None:
    items = [unit(KIND["turf-lane"], 1, 99.0), unit(KIND["treadmill"], 1, 5.0)] # Even shortened to its minimum, the lane cannot fit a 15 x 15 ft room in any direction.
    items.append(unit(KIND["flat-bench"], 1, 1.0))
    result = plan_layout(make_room(15, 15), items, RULES)
    assert [it.uid for it in result.unplaced] == ["turf-lane-1"]
    assert validate_layout(result, RULES) == []


def test_a_top_priority_turf_lane_leaves_room_for_lower_priority_units() -> None:
    room = Room(width_in=200, depth_in=360, entrance="center", ceiling_in=144) # 200 x 360 in: the lane fits on its own, and the bike still fits beside it.
    turf, bike = unit(KIND["turf-lane"], 1, 10.0), unit(KIND["upright-bike"], 1, 5.0)
    result = plan_layout(room, [turf, bike], RULES)
    assert placed_ids(result) == {"turf-lane-1", "upright-bike-1"}
    assert validate_layout(result, RULES) == []


@pytest.mark.parametrize(
    ("width", "depth", "longest"),
    [
        (30, 30, 312.0), # Along a side wall, opening onto the floor beside it: the 360 in floor less the lane's 24 in clearance at each end (a row beside the central aisle would also need a 36 in walkway behind it, leaving 300 in).
        (20, 40, 432.0), # The same along a 40 ft wall: 480 - 24 - 24.
    ],
)
def test_turf_lanes_take_the_longest_length_that_fits(
    width: float, depth: float, longest: float
) -> None:
    room = make_room(width, depth)
    result = plan_layout(room, [unit(KIND["turf-lane"], 1, 5.0)], RULES)
    assert validate_layout(result, RULES) == []
    (turf,) = result.placements
    assert length_of(turf) == pytest.approx(longest)
    assert any("shortened" in w for w in result.warnings)
    fixed = replace(KIND["turf-lane"], flexible=False, min_length=None) # A fixed-length lane of that length fits; one an inch longer does not.
    assert all_fit(room, [unit(replace(fixed, length=longest), 1, 5.0)])
    assert not all_fit(room, [unit(replace(fixed, length=longest + 1), 1, 5.0)])


@pytest.mark.parametrize(("entrance", "share"), [("left", 0.15), ("center", 0.5), ("right", 0.85)])
def test_main_aisle_starts_at_the_entrance(entrance: Entrance, share: float) -> None:
    room = make_room(70, 90, entrance=entrance)
    result = plan_layout(room, make_items(typical_mix(), random.Random(3)), RULES)
    assert result.entrance_x_in == pytest.approx(share * room.width_in)
    main = result.aisles[0]
    assert main.y == 0.0
    assert main.x <= result.entrance_x_in <= main.x2
    assert min(main.w, main.h) >= RULES.main_aisle_in
    assert any(a.y2 == pytest.approx(room.depth_in) and min(a.w, a.h) >= RULES.main_aisle_in for a in result.aisles) # It reaches the back wall itself, or through a rear exit in a corner when a row of wall units runs across the whole back wall (the validator checks they connect).
    assert validate_layout(result, RULES) == []


@pytest.mark.parametrize("entrance", ["left", "right"])
@pytest.mark.parametrize(("width", "depth"), [(14, 90), (28, 42), (40, 60), (34, 45), (70, 90)])
def test_a_door_near_a_side_wall_stays_clear(
    width: float, depth: float, entrance: Entrance
) -> None:
    room = make_room(width, depth, entrance=entrance) # A spine along the side wall joined to the door once stopped short of the door's far side, and the first row stood in the doorway.
    result = plan_layout(room, make_items(typical_mix(), random.Random(width)), RULES)
    assert validate_layout(result, RULES) == []
    assert_door_clear(result, RULES.main_aisle_in)


@pytest.mark.parametrize("width", [10, 10.5, 11])
def test_a_narrow_floor_with_the_door_in_the_middle_still_holds_equipment(width: float) -> None:
    rules = LayoutRules(main_aisle_in=60.0, secondary_aisle_in=36.0, zone_order=ZONE_ORDER) # A centered spine leaves unusable 30 in strips in a 10 ft room; a side spine with a front cross aisle fits.
    room = make_room(width, 15)
    for kind in ("upright-bike", "rower", "flat-bench"):
        result = plan_layout(room, [unit(KIND[kind], 1, 1.0)], rules)
        assert placed_ids(result) == {f"{kind}-1"}, (width, kind)
        assert validate_layout(result, rules) == []
        assert_door_clear(result, rules.main_aisle_in)
    deep = plan_layout(make_room(width, 100), make_items(typical_mix(), random.Random(2)), rules)
    assert len(deep.placements) >= 8
    assert validate_layout(deep, rules) == []
    assert_door_clear(deep, rules.main_aisle_in)


def test_narrow_floor_runs_the_main_aisle_along_a_wall() -> None:
    room = make_room(14, 90, entrance="center")
    items = make_items({"treadmill": 4, "upright-bike": 4, "chest-press": 3, "flat-bench": 3}, random.Random(4))
    result = plan_layout(room, items, RULES)
    assert validate_layout(result, RULES) == []
    spine = result.aisles[0]
    assert spine.x == 0.0 or spine.x2 == pytest.approx(room.width_in)
    assert len(result.placements) >= 10
    assert any("too narrow" in n for n in result.notes)


def test_a_side_aisle_on_a_wide_floor_is_not_called_narrow() -> None:
    lane = replace(KIND["turf-lane"], flexible=False, min_length=None) # 60 x 25 ft splits into two 28 ft sides around a central aisle, but a fixed 50 ft lane only fits across the one wide side left by an aisle along the wall.
    result = plan_layout(make_room(60, 25), [unit(lane, 1, 1.0)], RULES)
    assert placed_ids(result) == {"turf-lane-1"}
    assert validate_layout(result, RULES) == []
    assert result.aisles[0].x == 0.0
    assert any("runs along the left wall" in n for n in result.notes)
    assert not any("narrow" in n for n in result.notes)


def test_layout_is_deterministic_and_independent_of_input_order() -> None:
    items = make_items(typical_mix(scale=2), random.Random(9))
    room = make_room(60, 80, entrance="left")
    first = plan_layout(room, items, RULES)
    shuffled = list(items)
    random.Random(1).shuffle(shuffled)
    assert plan_layout(room, items, RULES) == first
    assert plan_layout(room, shuffled, RULES) == first


@pytest.mark.parametrize(
    ("mix", "width", "depth"), [("all kinds", 250, 360), ("all kinds", 70, 81), ("turf", 250, 360)]
)
def test_lays_out_400_units_in_under_100_ms(mix: str, width: float, depth: float) -> None:
    rng = random.Random(8)
    kinds = KINDS if mix == "all kinds" else (KIND["turf-lane"],)
    items = [unit(kinds[i % len(kinds)], i, rng.uniform(0, 10)) for i in range(400)]
    room = make_room(width, depth)
    best = float("inf")
    for _ in range(3):
        started = time.perf_counter()
        result = plan_layout(room, items, RULES)
        best = min(best, time.perf_counter() - started)
    assert best < 0.1
    assert validate_layout(result, RULES) == []


@pytest.mark.parametrize(("width", "depth"), [(70, 81), (100, 135), (120, 108)])
def test_hundreds_of_distinct_sizes_in_an_overfull_room_stay_valid_and_fast(
    width: float, depth: float
) -> None:
    rng = random.Random(4) # Unique sizes exhaust the search budget; even partial searches must account for every unit exactly once.
    items = []
    for i in range(400):
        clearance = (
            rng.choice([0, 6, 12, 24, 36]),
            rng.choice([0, 6, 12, 24, 36]),
            rng.choice([0, 6, 12, 24, 36]),
            rng.choice([0, 6, 12, 24, 36]),
        )
        kind = Kind(
            id=f"kind-{i}",
            zone=rng.choice(ZONE_ORDER),
            length=round(rng.uniform(20, 110), 1),
            width=round(rng.uniform(18, 100), 1),
            clearance=clearance,
            aisle_side=rng.choice(["front", "back", "side", "any"]),
            against_wall=rng.random() < 0.1,
        )
        items.append(unit(kind, i, rng.uniform(0, 10)))
    room = make_room(width, depth)
    best = float("inf")
    for _ in range(3):
        started = time.perf_counter()
        result = plan_layout(room, items, RULES)
        best = min(best, time.perf_counter() - started)
    assert best < 0.1
    assert validate_layout(result, RULES) == []
    placed = [p.item.uid for p in result.placements]
    assert len(placed) == len(set(placed)) > 50
    assert sorted(placed + [it.uid for it in result.unplaced]) == sorted(it.uid for it in items)


def test_empty_and_degenerate_floors() -> None:
    empty = plan_layout(make_room(30, 40), [], RULES)
    assert empty.placements == [] and empty.unplaced == [] and empty.zones == []
    assert empty.aisles and validate_layout(empty, RULES) == []

    sliver = plan_layout(make_room(3, 40), make_items({"flat-bench": 2}, random.Random(1)), RULES)
    assert sliver.placements == [] and len(sliver.unplaced) == 2
    assert sliver.warnings and validate_layout(sliver, RULES) == []

    smallest = plan_layout(make_room(12, 15), make_items(typical_mix(), random.Random(1)), RULES)
    assert validate_layout(smallest, RULES) == []


def test_a_configuration_whose_plan_breaks_a_rule_gives_way_to_the_next(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    room = make_room(40, 60) # Never expected, so simulate it: the first plan the engine builds gets an aisle that runs past the back wall, which no unit can be blamed for and dropping units cannot fix.
    items = make_items(typical_mix(), random.Random(13))
    honest = engine._result
    broken: list[Config] = []

    def result(
        ctx: Context, empty: LayoutResult, outcome: Outcome, order: list[LayoutItem]
    ) -> LayoutResult:
        plan = honest(ctx, empty, outcome, order)
        if not broken:
            broken.append(outcome.config)
            plan.aisles = [*plan.aisles, Rect(0, room.depth_in - 30, 60, 60)]
        return plan

    monkeypatch.setattr(engine, "_result", result)
    plan = plan_layout(room, items, RULES)
    assert validate_layout(plan, RULES) == []
    assert plan.placements
    assert searched(room, items).config == broken[0] # the broken plan's configuration lost
    assert not any(FINAL_CHECK in w for w in plan.warnings)


def test_reads_like_a_gym_floor() -> None:
    room = make_room(80, 96)
    result = plan_layout(room, make_items(typical_mix(scale=2), random.Random(21)), RULES)
    assert result.unplaced == []

    cardio = [p for p in result.placements if p.item.zone == "cardio"] # Cardio faces the entrance from the front of the floor, and zones follow the configured order front to back: wall units included, unless they stand on the back wall.
    assert {p.rotation for p in cardio} == {0}
    assert min(p.rect.y for p in cardio) <= 12 + 1e-6
    assert behind_a_later_zone(result, room.depth_in) == []

    wall_units = [p for p in result.placements if p.item.against_wall] # Wall units back onto the back wall, the zones nearest the back first.
    on_wall = [p for p in wall_units if room.depth_in - p.rect.y2 < 1e-6 and p.rotation == 0]
    assert len(on_wall) >= 0.75 * len(wall_units)
    assert {p.item.zone for p in on_wall} >= {"free_weights", "functional"}

    for turf in (p for p in result.placements if p.item.flexible_length): # Turf runs as a long strip, and the two sides of the main aisle carry similar loads.
        assert max(turf.rect.w, turf.rect.h) >= 5 * min(turf.rect.w, turf.rect.h)
    spine = result.aisles[0]
    left = sum(p.rect.area for p in result.placements if p.rect.x2 <= spine.x + 1e-6)
    right = sum(p.rect.area for p in result.placements if p.rect.x >= spine.x2 - 1e-6)
    assert abs(left - right) / (left + right) < 0.35


def test_benches_face_the_dumbbell_run_on_the_back_wall() -> None:
    checked = 0 # Benches are used with the dumbbells: where a dumbbell run stands on the back wall, the benches stand in the row in front of it, across its walkway, rather than mid-floor.
    for width, depth in [(80, 96), (60, 80), (50, 70), (70, 100), (100, 120), (90, 60)]:
        room = make_room(width, depth)
        result = plan_layout(room, make_items(typical_mix(scale=2), random.Random(width)), RULES)
        assert validate_layout(result, RULES) == []
        racks = [
            p
            for p in result.placements
            if p.item.equipment_id == "dumbbell-rack" and room.depth_in - p.rect.y2 < 1e-6
        ]
        benches = [p for p in result.placements if p.item.pairs_with == "dumbbell-rack"]
        if not racks:
            continue
        near = [
            b
            for b in benches
            if any(b.rect.y < r.rect.y and r.rect.y - b.rect.y2 <= 120.0 for r in racks)
        ]
        assert len(near) >= 0.7 * len(benches), (width, depth)
        checked += 1
    assert checked >= 5


def test_zone_rects_cover_the_equipment_not_the_leftover_floor() -> None:
    room = make_room(100, 100) # A nearly empty 100 x 100 ft floor: each zone is about as big as what stands in it, and spare depth opens up behind the cardio rather than pushing it off the entrance.
    items = [unit(KIND["treadmill"], 1, 5.0), unit(KIND["dumbbell-rack"], 1, 4.0)]
    result = plan_layout(room, items, RULES)
    assert validate_layout(result, RULES) == []
    zone_area: dict[str, float] = defaultdict(float)
    for zone in result.zones:
        zone_area[zone.zone] += zone.rect.area
    for p in result.placements:
        assert zone_area[p.item.zone] <= 1.25 * p.envelope.area, p.item.zone
    (treadmill,) = (p for p in result.placements if p.item.zone == "cardio")
    assert treadmill.rect.y == pytest.approx(KIND["treadmill"].clearance[0])
    (rack,) = (p for p in result.placements if p.item.against_wall)
    assert rack.rect.y2 == pytest.approx(room.depth_in)


def test_stretching_sits_against_a_side_wall() -> None:
    room = make_room(60, 70)
    items = make_items({"treadmill": 4, "chest-press": 2, "stretch-mat": 2}, random.Random(6))
    result = plan_layout(room, items, RULES)
    mats = [p for p in result.placements if p.item.zone == "stretching"]
    assert mats
    assert any(p.envelope.x <= 1e-6 or p.envelope.x2 >= room.width_in - 1e-6 for p in mats)


def test_rotation_turns_footprint_and_clearances_clockwise() -> None:
    assert [facing(r, "front") for r in (0, 90, 180, 270)] == ["n", "e", "s", "w"]
    assert [facing(90, s) for s in ("right", "back", "left")] == ["s", "w", "n"]
    clear = Clearance(front_in=1, back_in=2, left_in=3, right_in=4)
    assert clearance_by_direction(clear, 0) == {"n": 1, "s": 2, "w": 3, "e": 4}
    assert clearance_by_direction(clear, 90) == {"e": 1, "w": 2, "n": 3, "s": 4}
    assert footprint_size(35, 84, 0) == (35, 84)
    assert footprint_size(35, 84, 270) == (84, 35)


def valid_layout() -> LayoutResult:
    room = make_room(40, 60)
    result = plan_layout(room, make_items(typical_mix(), random.Random(13)), RULES)
    assert validate_layout(result, RULES) == []
    return result


def with_placement(result: LayoutResult, index: int, placement: Placement) -> LayoutResult:
    placements = list(result.placements)
    placements[index] = placement
    return replace(result, placements=placements)


def shifted(r: Rect, dx: float, dy: float) -> Rect:
    return Rect(r.x + dx, r.y + dy, r.w, r.h)


def moved(p: Placement, x: float, y: float) -> Placement:
    """The placement with its footprint (and envelope) moved to (x, y)."""
    dx, dy = x - p.rect.x, y - p.rect.y
    return replace(p, rect=shifted(p.rect, dx, dy), envelope=shifted(p.envelope, dx, dy))


def test_validator_catches_overlap() -> None:
    result = valid_layout()
    a = result.placements[0]
    broken = with_placement(result, 1, moved(result.placements[1], a.rect.x, a.rect.y))
    assert any("clearance zone of" in m for m in validate_layout(broken, RULES))


def test_validator_catches_units_outside_the_floor() -> None:
    result = valid_layout()
    p = result.placements[0]
    outside = with_placement(result, 0, moved(p, result.width_in - p.rect.w / 2, p.rect.y))
    assert any("outside the training floor" in m for m in validate_layout(outside, RULES))
    against = with_placement(result, 0, moved(p, 0.0, p.rect.y))
    if p.envelope.x < p.rect.x: # a clearance zone pushed through the wall
        assert any("runs into a wall" in m for m in validate_layout(against, RULES))
    through_front = with_placement(result, 0, moved(p, p.rect.x, -p.rect.h / 2))
    assert any("outside the training floor" in m for m in validate_layout(through_front, RULES))


def test_validator_catches_blocked_aisles_and_broken_aisle_network() -> None:
    result = valid_layout()
    p = result.placements[0]
    blocked = replace(result, aisles=[*result.aisles, Rect(p.rect.x, p.rect.y, 40, 40)])
    assert any("blocks aisle" in m for m in validate_layout(blocked, RULES))

    spine = result.aisles[0]
    island = Rect(result.width_in - 40, result.depth_in - 40, 40, 40)
    assert island.x > spine.x2
    messages = validate_layout(replace(result, aisles=[spine, island]), RULES)
    assert any("not connected" in m for m in messages)

    narrow = replace(result, aisles=[Rect(result.entrance_x_in - 10, 0, 20, 200)])
    messages = validate_layout(narrow, RULES)
    assert any("narrower than" in m for m in messages)

    no_aisles = validate_layout(replace(result, aisles=[]), RULES)
    assert "The layout has no aisles." in no_aisles
    assert any("does not open onto an aisle" in m for m in no_aisles)


def test_validator_catches_inconsistent_geometry_and_zones() -> None:
    result = valid_layout()
    p = result.placements[0]
    shrunk = with_placement(result, 0, replace(p, envelope=p.rect))
    assert any("envelope does not match" in m for m in validate_layout(shrunk, RULES))
    squashed = with_placement(result, 0, replace(p, rect=Rect(p.rect.x, p.rect.y, 1, 1)))
    assert any("does not match its dimensions" in m for m in validate_layout(squashed, RULES))

    zones = list(result.zones)
    zones.append(ZoneRect(zone="stretching", rect=zones[0].rect))
    assert any("overlap" in m for m in validate_layout(replace(result, zones=zones), RULES))
    unzoned = replace(result, zones=[z for z in result.zones if z.zone != p.item.zone])
    assert any("outside every" in m for m in validate_layout(unzoned, RULES))


def test_validator_reports_a_rotation_that_is_not_a_whole_quarter_turn() -> None:
    result = valid_layout() # Layouts read back from JSON can carry 90.0, which equals 90 but is not a valid rotation.
    p = result.placements[0]
    turned = with_placement(result, 0, replace(p, rotation=cast(Rotation, float(p.rotation))))
    assert any("invalid rotation" in m for m in validate_layout(turned, RULES))


def hand_built(*extra: Placement, aisles: Sequence[Rect] | None = None) -> LayoutResult:
    """A 20 x 20 ft floor: main aisle down the left wall, a walkway across the front."""
    machine = Kind("press", "machines", 30, 40, (0, 0, 0, 0))
    first = unit(machine, 1, 1.0)
    base = Placement(item=first, rect=Rect(60, 60, 40, 30), envelope=Rect(60, 60, 40, 30), rotation=0)
    return LayoutResult(
        width_in=240,
        depth_in=240,
        entrance_x_in=24,
        zones=[ZoneRect(zone="machines", rect=Rect(48, 0, 192, 240))],
        aisles=list(aisles) if aisles is not None else [Rect(0, 0, 48, 240), Rect(48, 0, 192, 60)],
        placements=[base, *extra],
    )


def test_validator_catches_missing_access() -> None:
    assert validate_layout(hand_built(), RULES) == []
    machine = Kind("press", "machines", 40, 40, (0, 0, 0, 0))

    behind = unit(machine, 2, 1.0) # Right behind the first press: its front approach zone is full of the other machine.
    blocked = Placement(item=behind, rect=Rect(60, 90, 40, 40), envelope=Rect(60, 90, 40, 40), rotation=0)
    assert validate_layout(hand_built(blocked), RULES) == [
        "Press (press-2) has no clear approach zone on its front side."
    ]

    alone = unit(machine, 3, 1.0) # In the open, but its approach zone does not reach any aisle.
    island = Placement(item=alone, rect=Rect(150, 160, 40, 40), envelope=Rect(150, 160, 40, 40), rotation=0)
    assert validate_layout(hand_built(island), RULES) == [
        "Press (press-3) has a clear approach zone, but it does not open onto an aisle."
    ]


def test_validator_requires_the_main_aisle_to_run_to_the_back_wall() -> None:
    front_only = hand_built(aisles=[Rect(0, 0, 240, 60)]) # A strip along the front serves the press, but it is no main aisle.
    assert validate_layout(front_only, RULES) == ["The main aisle does not run from the entrance to the back wall."]
    assert validate_layout(front_only) == ["The main aisle does not run from the entrance to the back wall."]


def test_validator_lets_the_main_aisle_be_narrower_than_the_walkways() -> None:
    rules = LayoutRules(main_aisle_in=24.0, secondary_aisle_in=36.0, zone_order=ZONE_ORDER)
    narrow_main = [Rect(0, 0, 24, 240), Rect(24, 0, 216, 60)]
    assert validate_layout(hand_built(aisles=narrow_main), rules) == []
    thin_walkway = [Rect(0, 0, 24, 240), Rect(24, 30, 216, 30)] # The walkway itself is still held to the secondary width.
    assert validate_layout(hand_built(aisles=thin_walkway), rules) == [
        "Aisle [x 24-240, y 30-60] is narrower than the 36 in minimum walkway."
    ]


def test_validator_holds_aisles_to_a_minimum_width_without_rules() -> None:
    slivers = [Rect(23.5, 0, 1, 240), Rect(24.5, 59, 215.5, 1)] # LayoutResult does not record the rule widths, so the one-argument form falls back to the 30 in accessible minimum instead of accepting any width.
    messages = validate_layout(hand_built(aisles=slivers))
    assert sum("narrower than the 30 in minimum walkway" in m for m in messages) == 2
