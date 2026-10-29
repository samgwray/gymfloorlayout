"""Check a floor layout against the hard rules every plan must satisfy.

1. Footprints lie inside the training floor.
2. Envelopes (footprint plus clearances, turned with the unit) lie inside the training floor:
   walls are obstacles for clearance zones. A wall unit with no back clearance can sit flush
   against the wall, since its envelope then ends at its footprint.
3. No footprint enters another unit's envelope. Clearance zones may overlap each other and
   aisles, but never another machine.
4. No footprint enters an aisle.
5. A main aisle starts on the front edge of the training floor at the entrance and runs to
   the back wall; every aisle is connected to it and every walkway opens directly onto it.
   With ``rules`` the main aisle is at least ``main_aisle_in`` wide and every other aisle at
   least ``secondary_aisle_in``; without them every aisle is at least ``MIN_ACCESS_IN`` wide.
6. Every unit has a clear approach zone on a side its ``aisle_side`` allows, as long as that
   side and ``max(clearance on that side, secondary aisle)`` deep, that stays inside the floor,
   holds no footprint and opens onto an aisle.
7. Zone rects contain their units' footprints and do not overlap rects of other zones.

Geometry also has to be self-consistent: each footprint matches the unit's dimensions at its
rotation and each envelope matches its clearances. Pairwise checks are vectorized so the
engine can afford to run them on every plan.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from numbers import Integral
from typing import cast

import numpy as np
from numpy.typing import NDArray

from gymplanner.layout.geometry import (
    ACCESS_SIDES,
    ROTATIONS,
    TOL,
    approach_depth,
    facing,
    footprint_size,
    item_envelope,
    strip_beside,
)
from gymplanner.layout.types import (
    LayoutItem,
    LayoutResult,
    LayoutRules,
    Placement,
    Rect,
    Rotation,
)

MIN_ACCESS_IN = 30.0
"""Approach depth and aisle width used when no rules are given: the 30 in side of the
30 x 48 in clear floor space accessibility standards require beside exercise equipment."""

Boxes = NDArray[np.float64]
Mask = NDArray[np.bool_]


@dataclass(frozen=True)
class Issue:
    message: str
    uids: tuple[str, ...] = ()
    """Placements involved, so a caller can drop the offending units."""


def validate_layout(result: LayoutResult, rules: LayoutRules | None = None) -> list[str]:
    """Human-readable rule violations; empty when the layout is valid.

    Pass the rules the layout was planned with: ``LayoutResult`` does not record its aisle
    widths, so without them aisles and approach zones are only held to ``MIN_ACCESS_IN``.
    """
    return [issue.message for issue in find_issues(result, rules)]


def training_floor(result: LayoutResult) -> Rect:
    return Rect(0.0, 0.0, result.width_in, result.depth_in)


def find_issues(result: LayoutResult, rules: LayoutRules | None = None) -> list[Issue]:
    floor = training_floor(result)
    issues: list[Issue] = []
    placements = _consistent(result, floor, issues)
    footprints = _boxes([p.rect for p in placements])
    aisles = list(result.aisles)
    aisle_boxes = _boxes(aisles)

    _check_clearances(placements, footprints, issues)
    for i, j in zip(*np.nonzero(_overlap(footprints, aisle_boxes)), strict=True):
        p = placements[int(i)]
        issues.append(Issue(f"{_label(p)} blocks aisle {_fmt(aisles[int(j)])}.", (p.item.uid,)))
    _check_aisles(result, floor, rules, bool(result.placements), issues)
    min_access = rules.secondary_aisle_in if rules is not None else MIN_ACCESS_IN
    _check_access(placements, footprints, aisle_boxes, floor, min_access, issues)
    _check_zones(result, floor, placements, issues)
    return issues


def _consistent(result: LayoutResult, floor: Rect, issues: list[Issue]) -> list[Placement]:
    """Placements whose geometry can be trusted; reports the rest and rules 1-2."""
    seen: set[str] = set()
    unplaced = {item.uid for item in result.unplaced}
    valid: list[Placement] = []
    for p in result.placements:
        uid = p.item.uid
        if uid in seen:
            issues.append(Issue(f"{_label(p)} is placed more than once.", (uid,)))
        seen.add(uid)
        if uid in unplaced:
            issues.append(Issue(f"{_label(p)} is listed as both placed and unplaced.", (uid,)))
        if not _quarter_turn(p.rotation):
            issues.append(Issue(f"{_label(p)} has an invalid rotation {p.rotation!r}.", (uid,)))
            continue
        rotation = cast(Rotation, int(p.rotation))
        if not _size_ok(p.item, p.rect, rotation):
            issues.append(Issue(f"{_label(p)} footprint does not match its dimensions at that rotation.", (uid,)))
            continue
        expected = item_envelope(p.item, p.rect, rotation)
        if not _same(expected, p.envelope):
            issues.append(Issue(f"{_label(p)} envelope does not match its clearances.", (uid,)))
        if not floor.contains(p.rect):
            issues.append(Issue(f"{_label(p)} lies outside the training floor.", (uid,)))
        elif not floor.contains(expected):
            issues.append(Issue(f"{_label(p)} clearance zone runs into a wall.", (uid,)))
        valid.append(Placement(item=p.item, rect=p.rect, envelope=expected, rotation=rotation)) # Later checks use the envelope implied by the clearances, whatever was recorded.
    return valid


def _quarter_turn(rotation: object) -> bool:
    """A whole number of quarter turns. Layouts read back from JSON may carry 90.0, which
    equals 90 but is not one."""
    return (
        isinstance(rotation, Integral)
        and not isinstance(rotation, bool)
        and int(rotation) in ROTATIONS
    )


def _size_ok(item: LayoutItem, rect: Rect, rotation: Rotation) -> bool:
    if item.length_in <= 0 or item.width_in <= 0:
        return False
    lo = item.min_length_in if item.flexible_length and item.min_length_in else item.length_in
    lo = min(lo, item.length_in)
    w, h = footprint_size(item.width_in, item.length_in, rotation)
    if rotation in (0, 180):
        return _close(rect.w, w) and lo - TOL <= rect.h <= h + TOL
    return _close(rect.h, h) and lo - TOL <= rect.w <= w + TOL


def _check_clearances(placements: list[Placement], footprints: Boxes, issues: list[Issue]) -> None:
    hits = _overlap(footprints, _boxes([p.envelope for p in placements]))
    np.fill_diagonal(hits, False)
    for i, j in zip(*np.nonzero(hits), strict=True):
        a, b = placements[int(i)], placements[int(j)]
        issues.append(Issue(f"{_label(a)} sits inside the clearance zone of {_label(b)}.", (a.item.uid, b.item.uid),))


def _check_aisles(
    result: LayoutResult,
    floor: Rect,
    rules: LayoutRules | None,
    has_units: bool,
    issues: list[Issue],
) -> None:
    """Rule 5. The main aisle is the aisles the entrance reaches through aisles at least the
    main width (without rules: as wide as the widest aisle at the entrance). It has to reach
    the back wall, and every other aisle has to touch it."""
    aisles = list(result.aisles)
    if not aisles:
        if has_units:
            issues.append(Issue("The layout has no aisles."))
        return
    for a in aisles:
        if not floor.contains(a):
            issues.append(Issue(f"Aisle {_fmt(a)} runs outside the training floor."))
    entry = [
        i
        for i, a in enumerate(aisles)
        if a.y <= floor.y + TOL and a.x - TOL <= result.entrance_x_in <= a.x2 + TOL
    ]
    if not entry:
        issues.append(Issue("No aisle starts at the entrance on the front of the training floor."))
        return
    links = _touch(_boxes(aisles), _boxes(aisles))
    reached = _reach(links, entry, np.ones(len(aisles), dtype=bool))
    for i in np.flatnonzero(~reached):
        issues.append(Issue(f"Aisle {_fmt(aisles[int(i)])} is not connected to the main aisle."))

    widths = np.array([min(a.w, a.h) for a in aisles])
    main_width = rules.main_aisle_in if rules is not None else float(widths[entry].max())
    walk_width = rules.secondary_aisle_in if rules is not None else MIN_ACCESS_IN
    wide = widths >= main_width - TOL
    main_entry = [i for i in entry if wide[i]]
    if not main_entry:
        issues.append(Issue(f"The aisle at the entrance is narrower than {main_width:g} in."))
    main = _reach(links, main_entry, wide)
    trunk = main.copy() # The main width may be the smaller one; an aisle narrower than a walkway then has to be the main aisle itself: at the entrance, or running to the back wall.
    trunk[[i for i, a in enumerate(aisles) if i not in entry and a.y2 < floor.y2 - TOL]] = False
    for k, a in enumerate(aisles):
        if (rules is None or not trunk[k]) and widths[k] < walk_width - TOL:
            issues.append(Issue(f"Aisle {_fmt(a)} is narrower than the {walk_width:g} in minimum walkway."))
    if not main_entry:
        return
    if not any(aisles[int(i)].y2 >= floor.y2 - TOL for i in np.flatnonzero(main)):
        issues.append(Issue("The main aisle does not run from the entrance to the back wall."))
    on_main = links[:, main].any(axis=1) | main
    for i in np.flatnonzero(reached & ~on_main):
        issues.append(Issue(f"Walkway {_fmt(aisles[int(i)])} does not open onto the main aisle."))


def _reach(links: Mask, start: Sequence[int], allowed: Mask) -> Mask:
    """Aisles reachable from ``start`` through touching aisles that are ``allowed``."""
    seen = np.zeros(len(allowed), dtype=bool)
    frontier = [i for i in start if allowed[i]]
    seen[frontier] = True
    while frontier:
        nxt = np.flatnonzero(links[frontier].any(axis=0) & allowed & ~seen)
        seen[nxt] = True
        frontier = [int(i) for i in nxt]
    return seen


def _check_access(
    placements: list[Placement],
    footprints: Boxes,
    aisle_boxes: Boxes,
    floor: Rect,
    min_access: float,
    issues: list[Issue],
) -> None:
    owners: list[int] = []
    zones: list[Rect] = []
    for k, p in enumerate(placements):
        for side in ACCESS_SIDES.get(p.item.aisle_side, ACCESS_SIDES["any"]):
            depth = approach_depth(p.item.clearance, side, min_access)
            zones.append(strip_beside(p.rect, facing(p.rotation, side), depth))
            owners.append(k)
    if not zones:
        return
    owner = np.array(owners)
    boxes = _boxes(zones)
    blocked = _overlap(boxes, footprints)
    blocked[np.arange(len(zones)), owner] = False
    clear = ~blocked.any(axis=1) & _inside(boxes, floor)
    opens = _touch(boxes, aisle_boxes).any(axis=1)
    any_clear = np.zeros(len(placements), dtype=bool)
    any_ok = np.zeros(len(placements), dtype=bool)
    np.logical_or.at(any_clear, owner, clear)
    np.logical_or.at(any_ok, owner, clear & opens)
    for idx in np.flatnonzero(~any_ok):
        p = placements[int(idx)]
        if any_clear[idx]:
            message = f"{_label(p)} has a clear approach zone, but it does not open onto an aisle."
        else:
            message = f"{_label(p)} has no clear approach zone on its {p.item.aisle_side} side."
        issues.append(Issue(message, (p.item.uid,)))


def _check_zones(
    result: LayoutResult, floor: Rect, placements: list[Placement], issues: list[Issue]
) -> None:
    zones = result.zones
    for z in zones:
        if not floor.contains(z.rect):
            issues.append(Issue(f"Zone {z.zone} {_fmt(z.rect)} extends outside the floor."))
    for i, a in enumerate(zones):
        for b in zones[i + 1 :]:
            if a.zone != b.zone and a.rect.intersects(b.rect):
                issues.append(Issue(f"Zones {a.zone} and {b.zone} overlap."))
    for p in placements:
        if not any(z.zone == p.item.zone and z.rect.contains(p.rect) for z in zones):
            issues.append(Issue(f"{_label(p)} is outside every {p.item.zone} zone.", (p.item.uid,)))


def _boxes(rects: Sequence[Rect]) -> Boxes:
    if not rects:
        return np.zeros((0, 4), dtype=np.float64)
    return np.array([(r.x, r.y, r.x2, r.y2) for r in rects], dtype=np.float64)


def _overlap(a: Boxes, b: Boxes) -> Mask:
    """[len(a), len(b)] interiors overlap (touching edges do not count)."""
    return (
        (a[:, None, 0] < b[None, :, 2] - TOL)
        & (b[None, :, 0] < a[:, None, 2] - TOL)
        & (a[:, None, 1] < b[None, :, 3] - TOL)
        & (b[None, :, 1] < a[:, None, 3] - TOL)
    )


def _touch(a: Boxes, b: Boxes) -> Mask:
    """[len(a), len(b)] overlap or share a stretch of edge (see ``geometry.touches``)."""
    ox = np.minimum(a[:, None, 2], b[None, :, 2]) - np.maximum(a[:, None, 0], b[None, :, 0])
    oy = np.minimum(a[:, None, 3], b[None, :, 3]) - np.maximum(a[:, None, 1], b[None, :, 1])
    return ((ox > TOL) & (oy >= -TOL)) | ((oy > TOL) & (ox >= -TOL))


def _inside(boxes: Boxes, floor: Rect) -> Mask:
    return (
        (boxes[:, 0] >= floor.x - TOL)
        & (boxes[:, 1] >= floor.y - TOL)
        & (boxes[:, 2] <= floor.x2 + TOL)
        & (boxes[:, 3] <= floor.y2 + TOL)
    )


def _same(a: Rect, b: Rect) -> bool:
    return _close(a.x, b.x) and _close(a.y, b.y) and _close(a.w, b.w) and _close(a.h, b.h)


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= TOL * max(1.0, abs(a), abs(b))


def _label(p: Placement) -> str:
    return f"{p.item.name} ({p.item.uid})"


def _fmt(r: Rect) -> str:
    return f"[x {r.x:.0f}-{r.x2:.0f}, y {r.y:.0f}-{r.y2:.0f}]"
