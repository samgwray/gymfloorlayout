"""Rows or rings: the plan comes from whichever family of configurations keeps the most priority.

The inputs are the planning service's selections for real rooms (equipment, units, and each
type's priority, the optimizer's marginal value of its last unit; each further unit of a type
is worth less than the one before), fixed here so the tests do not depend on the optimizer.
Each room is the training floor of the gym its case is named after.
"""

from __future__ import annotations

import pytest

from gymplanner.domain import Room
from gymplanner.layout import plan_layout, validate_layout
from test_layout import FINAL_CHECK, kept_value, searched
from test_layout_ring import real_rules, spec_items

Spec = tuple[tuple[str, int, float], ...]

CARDIO_2000: Spec = (
    ("elliptical", 1, 0.50795),
    ("upright_bike", 2, 0.281634),
    ("recumbent_bike", 1, 0.405634),
    ("indoor_cycle", 1, 0.20731),
    ("air_bike", 1, 0.0984082),
    ("rower", 1, 0.189),
    ("rig_bay", 1, 0.132051),
    ("battle_rope_station", 1, 0.00717907),
    ("suspension_trainer_station", 1, 0.0286908),
    ("heavy_bag", 1, 0.0283594),
    ("stretch_area", 6, 0.00627689),
    ("accessory_pack", 1, 0.206524),
    ("dumbbell_set_light", 1, 1.05834),
    ("adjustable_bench", 1, 0.0886805),
    ("flat_bench", 2, 0.0601845),
    ("lat_pulldown_row_combo", 1, 0.353249),
    ("cable_column", 2, 0.270909),
)
"""2,000 sq ft cardio and wellness gym at $30 per sq ft (packing efficiency 0.75): a ring
holds one more of the most valuable units, rows hold five more units and more priority."""

GENERAL_7000_LEFT: Spec = (
    ("treadmill", 7, 0.449265),
    ("elliptical", 4, 0.315625),
    ("upright_bike", 2, 0.188593),
    ("recumbent_bike", 2, 0.300276),
    ("indoor_cycle", 3, 0.0785012),
    ("air_bike", 1, 0.158921),
    ("rower", 3, 0.103799),
    ("stair_climber", 1, 0.51408),
    ("ski_erg", 1, 0.10534),
    ("rig_bay", 3, 0.0712172),
    ("plyo_box_set", 1, 0.242459),
    ("wall_ball_station", 1, 0.0713435),
    ("battle_rope_station", 1, 0.0431996),
    ("suspension_trainer_station", 2, 0.016264),
    ("heavy_bag", 2, 0.0352031),
    ("kettlebell_set", 1, 0.426572),
    ("stretch_area", 9, 0.0115376),
    ("accessory_pack", 1, 0.427983),
    ("power_rack", 2, 0.314309),
    ("half_rack", 2, 0.25806),
    ("lifting_platform", 1, 0.292459),
    ("bench_press_station", 1, 0.293845),
    ("landmine", 1, 0.0598462),
    ("dumbbell_set_light", 1, 0.475306),
    ("dumbbell_set_full", 2, 1.2167),
    ("adjustable_bench", 5, 0.0526112),
    ("flat_bench", 6, 0.0522297),
    ("hyperextension", 1, 0.16183),
    ("leg_press", 1, 0.369786),
    ("calf_raise", 1, 0.110939),
    ("lat_pulldown_row_combo", 2, 0.264018),
    ("multi_station_gym", 1, 0.913752),
    ("cable_column", 4, 0.2196),
)
"""7,000 sq ft general gym, entrance on the left, $45 per sq ft (packing efficiency 0.75)."""

FUNCTIONAL_15000: Spec = (
    ("treadmill", 5, 0.201598),
    ("curved_treadmill", 4, 0.14325),
    ("upright_bike", 2, 0.0521007),
    ("indoor_cycle", 1, 0.0661217),
    ("air_bike", 7, 0.0554559),
    ("rower", 7, 0.0542319),
    ("stair_climber", 1, 0.254161),
    ("ski_erg", 7, 0.026287),
    ("rig_bay", 5, 0.0224578),
    ("turf_lane", 6, 0.185654),
    ("plyo_box_set", 4, 0.134936),
    ("wall_ball_station", 6, 0.0143104),
    ("battle_rope_station", 2, 0.0872863),
    ("suspension_trainer_station", 5, 0.0396859),
    ("heavy_bag", 4, 0.0388596),
    ("kettlebell_set", 7, 0.051762),
    ("stretch_area", 12, 0.0315466),
    ("accessory_pack", 1, 0.493241),
    ("power_rack", 6, 0.142248),
    ("half_rack", 4, 0.0844339),
    ("lifting_platform", 7, 0.0999847),
    ("bench_press_station", 3, 0.128318),
    ("landmine", 1, 0.0692111),
    ("dumbbell_set_light", 1, 0.108246),
    ("dumbbell_set_full", 2, 0.398761),
    ("adjustable_bench", 4, 0.0554307),
    ("flat_bench", 6, 0.0339953),
    ("preacher_bench", 1, 0.0370435),
    ("hyperextension", 2, 0.0391515),
    ("ghd", 1, 0.0578988),
    ("dip_chin_station", 3, 0.0350606),
    ("hip_thrust_bench", 1, 0.137793),
    ("fixed_barbell_set", 1, 0.404751),
    ("leg_ext_curl_combo", 1, 0.091962),
    ("lat_pulldown_row_combo", 1, 0.10432),
    ("functional_trainer", 1, 0.0771755),
    ("cable_column", 2, 0.0452845),
)
"""15,000 sq ft functional gym at $30 per sq ft (packing efficiency 0.75): 134 units, far more
than the floor holds, so the search runs into its work budget."""

CASES: dict[str, tuple[Room, Spec]] = {
    "2,000 sq ft cardio": (Room(width_in=438.178, depth_in=525.814, entrance="center", ceiling_in=144.0,), CARDIO_2000),
    "7,000 sq ft general": (
        Room(width_in=819.756, depth_in=892.381, entrance="left", ceiling_in=144.0),
        GENERAL_7000_LEFT,
    ),
    "15,000 sq ft functional": (
        Room(width_in=1200.0, depth_in=1196.279, entrance="center", ceiling_in=144.0),
        FUNCTIONAL_15000,
    ),
}


@pytest.mark.parametrize("case", CASES)
def test_the_plan_keeps_at_least_the_priority_either_family_keeps(case: str) -> None:
    room, spec = CASES[case] # The rows-or-rings choice once went to whichever family held the longer run of the most valuable units, so a ring holding one more of them beat rows holding more in total.
    rules = real_rules()
    items = spec_items(spec)
    result = plan_layout(room, items, rules)
    assert validate_layout(result, rules) == []
    assert not any(FINAL_CHECK in w for w in result.warnings)
    for ring in (False, True):
        family = searched(room, items, ring, rules)
        assert kept_value(result) >= family.value - 1e-9, ("rings" if ring else "rows", case)


def test_a_large_overfull_floor_keeps_what_rows_alone_keep() -> None:
    room, spec = CASES["15,000 sq ft functional"] # Each family has its own work budget: when the ring configurations shared the rows' budget, the rows search ran out early and this floor lost 5 of its 112 units.
    rules = real_rules()
    items = spec_items(spec)
    result = plan_layout(room, items, rules)
    rows = searched(room, items, False, rules)
    assert len(result.placements) >= len(rows.kept) >= 110
