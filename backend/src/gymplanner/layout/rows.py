"""Equipment rows: choose each unit's orientation and pack units side by side along a row.

A row is a horizontal strip in one half of the floor, running from the main aisle (its inner
end) to a side wall (its outer end); ``t`` measures distance along it from the inner end.
Users reach a unit in one of two ways:

* edge access: the access side faces a walkway along the strip's ``n`` or ``s`` edge, and
  the unit is aligned with that edge so its approach zone opens straight onto the walkway;
* gap access: the access side faces along the row (a bike mounted from the side), so the gap
  beside it is widened to the approach depth. The unit is aligned with the row's walkway edge
  so that gap opens onto the walkway. Two neighbours accessed from the side share one gap.

Gaps along the row are the larger of the facing clearances and any approach depth that uses
them, so no footprint ever enters another unit's clearance or approach zone. Clearance and
approach zones may reach into the main aisle at the inner end (never past its far side), and
at the outer end into the aisle beyond it when there is one (``outer_allow``), but otherwise
stay inside the walls.

A row may hold several zones (shallow floors fit only a few rows); each zone's units then form
one run along it, in zone order from the inner end.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from typing import Literal

from gymplanner.catalog.schema import ZoneId
from gymplanner.layout.geometry import (
    ACCESS_SIDES,
    OPPOSITE,
    TOL,
    Direction,
    approach_depth,
    clearance_by_direction,
    facing,
    footprint_size,
)
from gymplanner.layout.types import LayoutItem, Rotation

AccessMode = Literal["n", "s", "in", "out", "either"]
RowKind = Literal["facing", "alternating", "wall"]
"""``facing``: every unit faces the entrance (cardio). ``alternating``: the row opens onto one
walkway and consecutive rows pair up back-to-back. ``wall``: backs to the wall behind."""


@dataclass(frozen=True)
class RowFrame:
    """The half of the floor a row is built in."""

    length: float
    """Usable row length: the half's width."""
    depth: float
    """Depth of the half, used to rule out orientations that could never fit."""
    inward: Direction
    """Direction along the row toward the main aisle."""
    inner_allow: float
    """How far clearance and approach zones may reach into the main aisle."""
    secondary: float
    outer_allow: float = 0.0
    """How far they may reach past the outer end: 0 at a wall, the aisle's depth at an aisle."""

    @cached_property
    def outward(self) -> Direction:
        return OPPOSITE[self.inward]


@dataclass(frozen=True)
class Pose:
    rotation: Rotation
    length: float
    """Front-to-back size actually used (shorter than nominal for shortened flexible units)."""
    w: float
    h: float
    clear: dict[Direction, float]
    approach: dict[Direction, float]
    """Approach-zone depth for each direction an access side faces."""


@dataclass(frozen=True)
class Choice:
    pose: Pose
    mode: AccessMode


PoseMaker = Callable[[LayoutItem, Rotation, float], Pose]
"""Builds (or fetches from a cache) a unit's pose at a rotation and length."""


@dataclass(frozen=True)
class FlexOption:
    """One way to lay a flexible unit (a turf lane) in a half, before its length is settled."""

    choice: Choice
    """Orientation and access, with the pose at nominal length."""
    along_row: bool
    """True when the length runs along the row; otherwise it runs front to back across it."""
    max_length: float
    """Longest length the empty half allows along that axis, capped at the nominal length."""


@dataclass
class Slot:
    item: LayoutItem
    pose: Pose
    mode: AccessMode
    """Resolved access: ``n``/``s`` for edge access, ``in``/``out`` for the gap used."""
    t: float
    align: Direction = "n"


@dataclass
class Row:
    kind: RowKind
    walk_edge: Direction
    """Edge whose walkway serves gap-access units (and every unit of an alternating row)."""
    slots: list[Slot]
    end: float
    """Row length used, including the clearance or approach after the last unit."""
    depth: float = 0.0
    walk_n: bool = False
    walk_s: bool = False
    reach_n: float = 0.0
    """How far clearances extend beyond the strip's n edge."""
    reach_s: float = 0.0
    appr_n: float = 0.0
    """How far approach zones extend beyond the strip's n edge."""
    appr_s: float = 0.0

    @property
    def zone(self) -> ZoneId:
        """The zone the row starts with, which set its kind."""
        return self.slots[0].item.zone

    @property
    def items(self) -> list[LayoutItem]:
        return [s.item for s in self.slots]

    def runs(self) -> list[tuple[ZoneId, int, int]]:
        """``(zone, first, stop)`` for each run of consecutive slots in one zone."""
        out: list[tuple[ZoneId, int, int]] = []
        start = 0
        for i in range(1, len(self.slots) + 1):
            if i == len(self.slots) or self.slots[i].item.zone != self.slots[start].item.zone:
                out.append((self.slots[start].item.zone, start, i))
                start = i
        return out


def make_pose(item: LayoutItem, rotation: Rotation, length: float, min_approach: float) -> Pose:
    w, h = footprint_size(item.width_in, length, rotation)
    return Pose(
        rotation=rotation,
        length=length,
        w=w,
        h=h,
        clear=clearance_by_direction(item.clearance, rotation),
        approach={
            facing(rotation, side): approach_depth(item.clearance, side, min_approach)
            for side in ACCESS_SIDES.get(item.aisle_side, ACCESS_SIDES["any"])
        },
    )


def rotation_order(item: LayoutItem, edge: Direction, face_entrance: bool) -> tuple[Rotation, ...]:
    """Rotations to try, best first: access side toward the walkway, then turned sideways."""
    front_to_edge: Rotation = 0 if edge == "n" else 180
    back_to_edge: Rotation = 180 if edge == "n" else 0
    if item.aisle_side == "back":
        first, second = back_to_edge, front_to_edge
    else:
        first, second = front_to_edge, back_to_edge
    order: tuple[Rotation, ...] = (first, second, 90, 270)
    if face_entrance:
        order = (0, *(r for r in order if r != 0))
    return order


def _access_mode(pose: Pose, edges: tuple[Direction, ...], frame: RowFrame) -> AccessMode | None:
    for edge in edges:
        if edge in pose.approach:
            return "n" if edge == "n" else "s"
    has_in = frame.inward in pose.approach
    has_out = frame.outward in pose.approach
    if has_in and has_out:
        return "either"
    if has_in:
        return "in"
    if has_out:
        return "out"
    return None


def _ends(pose: Pose, mode: AccessMode, frame: RowFrame) -> tuple[float, float]:
    """Room a lone unit needs before (inner end) and after (outer end) its footprint."""
    start = max(0.0, pose.clear[frame.inward] - frame.inner_allow)
    end = max(0.0, pose.clear[frame.outward] - frame.outer_allow)
    via_in = max(start, pose.approach.get(frame.inward, 0.0) - frame.inner_allow)
    via_out = max(end, pose.approach.get(frame.outward, 0.0) - frame.outer_allow)
    if mode == "in" or (mode == "either" and via_in - start <= via_out - end):
        return via_in, end
    if mode in ("out", "either"):
        return start, via_out
    return start, end


def _vertical_extra(pose: Pose, mode: AccessMode, walk_edge: Direction, frame: RowFrame) -> float:
    """Depth a lone unit needs beyond its footprint: clearances plus the walkway it opens onto."""
    up, down = pose.clear["n"], pose.clear["s"]
    edge = mode if mode in ("n", "s") else walk_edge
    if edge == "n":
        up = max(up, pose.approach.get("n", 0.0), frame.secondary)
    else:
        down = max(down, pose.approach.get("s", 0.0), frame.secondary)
    return up + down


Candidate = tuple[Choice, float, float]
"""An orientation, the row length it needs on its own and the depth of half it needs."""


def pose_options(
    item: LayoutItem,
    frame: RowFrame,
    edges: tuple[Direction, ...],
    rotations: tuple[Rotation, ...],
    make: PoseMaker,
    limit: int = 4,
) -> tuple[Choice, ...]:
    """Orientations, in preference order, in which a unit fits an empty row of the half (at
    most ``limit``).

    The first is the one to use; later ones serve when the depth left in the half is too
    shallow for it (a machine turned sideways is often shallower).
    """
    return fitting(pose_candidates(item, frame, edges, rotations, make), frame, limit)


def pose_candidates(
    item: LayoutItem,
    frame: RowFrame,
    edges: tuple[Direction, ...],
    rotations: tuple[Rotation, ...],
    make: PoseMaker,
) -> tuple[Candidate, ...]:
    """Every orientation with a way in from the row's walkways, in preference order. What
    each needs depends on the frame's direction and allowances but not on its size, so one
    list serves frames of any size (``fitting``)."""
    out: list[Candidate] = []
    for rotation in rotations:
        pose = make(item, rotation, item.length_in)
        mode = _access_mode(pose, edges, frame)
        if mode is None:
            continue
        start, end = _ends(pose, mode, frame)
        extra = _vertical_extra(pose, mode, edges[0], frame)
        out.append((Choice(pose, mode), start + pose.w + end, pose.h + extra))
    return tuple(out)


def fitting(candidates: tuple[Candidate, ...], frame: RowFrame, limit: int) -> tuple[Choice, ...]:
    """The first ``limit`` candidates that fit an empty row of ``frame``."""
    out: list[Choice] = []
    for choice, length, depth in candidates:
        if len(out) >= limit:
            break
        if length <= frame.length + TOL and depth <= frame.depth + TOL:
            out.append(choice)
    return tuple(out)


def flexible_options(
    item: LayoutItem,
    frame: RowFrame,
    edges: tuple[Direction, ...],
    rotations: tuple[Rotation, ...],
    make: PoseMaker,
) -> tuple[FlexOption, ...]:
    """Every orientation in which a flexible unit fits an empty row at its minimum length.

    The length along the row is bounded here; the length across it depends on the depth still
    free when the row is built, so the stacker settles it.
    """
    nominal = item.length_in
    min_length = min(nominal, item.min_length_in or nominal)
    options: list[FlexOption] = []
    for rotation in rotations:
        probe = make(item, rotation, nominal)
        mode = _access_mode(probe, edges, frame)
        if mode is None:
            continue
        start, end = _ends(probe, mode, frame)
        room_x = frame.length - start - end
        room_y = frame.depth - _vertical_extra(probe, mode, edges[0], frame)
        along_row = rotation in (90, 270)
        room, across, across_room = (
            (room_x, probe.h, room_y) if along_row else (room_y, probe.w, room_x)
        )
        if room < min_length - TOL or across > across_room + TOL:
            continue
        options.append(FlexOption(Choice(probe, mode), along_row, min(nominal, room)))
    return tuple(options)


class RowBuilder:
    """Appends units along a row from the inner end until the next one does not fit."""

    def __init__(self, frame: RowFrame, walk_edge: Direction) -> None:
        self.frame = frame
        self.walk_edge = walk_edge
        self.slots: list[Slot] = []
        self.end = 0.0

    def _options(self, choice: Choice) -> tuple[AccessMode, ...]:
        frame, pose, mode = self.frame, choice.pose, choice.mode
        if mode != "either":
            return (mode,)
        if self.slots and self.slots[-1].mode == "out":
            return ("in", "out") # share the previous unit's access gap
        if not self.slots and pose.approach[frame.inward] <= frame.inner_allow + TOL:
            return ("in", "out") # approach from the main aisle
        return ("out", "in") # leave the gap after it for the next unit to share

    def _position(self, pose: Pose, resolved: AccessMode) -> float:
        frame = self.frame
        need_in = pose.clear[frame.inward]
        if resolved == "in":
            need_in = max(need_in, pose.approach[frame.inward])
        if not self.slots:
            return max(0.0, need_in - frame.inner_allow)
        prev = self.slots[-1]
        prev_out = prev.pose.clear[frame.outward]
        if prev.mode == "out":
            prev_out = max(prev_out, prev.pose.approach[frame.outward])
        return prev.t + prev.pose.w + max(prev_out, need_in)

    def _after(self, pose: Pose, resolved: AccessMode) -> float:
        """Room the unit needs after its footprint if it ends the row."""
        after = pose.clear[self.frame.outward]
        if resolved == "out":
            after = max(after, pose.approach[self.frame.outward])
        return max(0.0, after - self.frame.outer_allow)

    def room(self, choice: Choice) -> float:
        """Widest footprint (along the row) this orientation could still take at the row's end."""
        pose = choice.pose
        return max(self.frame.length - self._position(pose, r) - self._after(pose, r) for r in self._options(choice))

    def try_add(self, item: LayoutItem, choice: Choice) -> bool:
        pose = choice.pose
        for resolved in self._options(choice):
            t = self._position(pose, resolved)
            end = t + pose.w + self._after(pose, resolved)
            if end <= self.frame.length + TOL:
                self.slots.append(Slot(item=item, pose=pose, mode=resolved, t=t))
                self.end = end
                return True
        return False

    @property
    def fill(self) -> float:
        return self.end / self.frame.length if self.frame.length > 0 else 1.0

    def finish(self, kind: RowKind) -> Row:
        row = Row(kind=kind, walk_edge=self.walk_edge, slots=self.slots, end=self.end)
        measure(row)
        return row


def measure(row: Row) -> None:
    """Strip depth, alignment, and how far clearances and approaches reach past the strip."""
    depth = max((s.pose.h for s in row.slots), default=0.0)
    row.depth = depth
    row.walk_n = row.walk_s = False
    row.reach_n = row.reach_s = row.appr_n = row.appr_s = 0.0
    for slot in row.slots:
        pose = slot.pose
        spare = depth - pose.h
        if slot.mode in ("n", "s"):
            slot.align = "n" if slot.mode == "n" else "s"
            if row.kind == "wall" and slot.mode == "n" and pose.approach["n"] >= spare - TOL: # Wall units sit back against the wall when their approach still reaches the walkway.
                slot.align = "s"
        else:
            slot.align = row.walk_edge
        off_n = 0.0 if slot.align == "n" else spare
        off_s = spare - off_n
        row.reach_n = max(row.reach_n, pose.clear["n"] - off_n)
        row.reach_s = max(row.reach_s, pose.clear["s"] - off_s)
        if slot.mode == "n":
            row.walk_n = True
            row.appr_n = max(row.appr_n, pose.approach["n"] - off_n)
        elif slot.mode == "s":
            row.walk_s = True
            row.appr_s = max(row.appr_s, pose.approach["s"] - off_s)
        elif slot.align == "n":
            row.walk_n = True
        else:
            row.walk_s = True


def spread(row: Row, frame: RowFrame, cap: float, anchor_from: int | None) -> list[float]:
    """Final ``t`` of each unit: slack becomes breathing room between units (up to ``cap`` per
    gap); the rest stays at the outer end, or goes before slot ``anchor_from`` so the units from
    there on sit against the side wall (a quiet corner for stretching)."""
    n = len(row.slots)
    slack = max(0.0, frame.length - row.end)
    extra = min(slack / (n + 1), cap) if n else 0.0
    rest = slack - extra * n
    return [
        slot.t + extra * (i + 1) + (rest if anchor_from is not None and i >= anchor_from else 0.0)
        for i, slot in enumerate(row.slots)
    ]
