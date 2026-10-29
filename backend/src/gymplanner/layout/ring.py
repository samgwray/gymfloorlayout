"""Ring configurations: equipment lines the side walls as well, facing into the room.

Small gyms, studios and hotel fitness rooms line their walls with equipment around an open
centre. A ring configuration keeps the spine and halves of a row configuration and lines the
walls of each half:

* the half's first row stands along the front wall, exactly as in a row configuration;
* the back wall takes a row of wall units. With a half on each side of the spine it may run
  across the whole width (``Config.across``): the spine then stops at a main-width walkway in
  front of the row, and the main aisle reaches the back wall through a rear exit in a corner,
  so a long dumbbell run need not fit beside the spine. Otherwise each half has its own;
* in an ``open`` ring, a row of free-standing units may face the back wall row from in
  front of its walkway (``Config.facing``: benches in front of a dumbbell run), taking the
  zones nearest the back first;
* the front and back rows run out to the side walls and own the corners. Between their
  walkways a band lines the side wall: one unit deep, every unit backed onto the wall (cardio
  may face it instead, its rear safety zone toward the room, and a turf lane runs along it),
  each as close to the wall as its clearance allows while its approach zone still reaches the
  floor beside the band;
* that floor stays open as circulation (``open``), or holds island rows from the spine to a
  walkway along the band (``core``). That walkway reaches the main aisle through the walkway
  across the half in front of the back row (or behind the front row), made main-aisle wide;
  where that walkway does not fit between the rows, the half has no band, and the walkways
  its rows need are all it keeps.

Wall units go to the back wall first, the widest first; then the front rows, the bands and the
islands take the rest in zone order, so cardio stays near the entrance and the zones read from
the front to the back on both sides. Bands take wall units first, so they stay on a wall, and
when the zone order leaves units over, the widest go first instead (first fit decreasing, wall
units still ahead), each band keeping its units in zone order when they still fit.

A band is built as a row in a local frame turned to its wall: ``t`` runs along the wall from
the front end, local ``n`` faces the room and local ``s`` the wall. Turning the frame onto the
west wall is a quarter turn clockwise, onto the east wall three quarter turns, so a unit's
rotation, footprint and clearances turn with it.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace

from gymplanner.catalog.schema import ZoneId
from gymplanner.layout.geometry import ROTATIONS, TOL, item_envelope
from gymplanner.layout.rows import (
    Choice,
    Row,
    RowBuilder,
    RowFrame,
    flexible_options,
    pose_options,
    rotation_order,
    spread,
)
from gymplanner.layout.stacking import (
    CORNER_ZONES,
    FACING_ZONES,
    Bin,
    Config,
    Context,
    Half,
    Stack,
    back_wall_rows,
    facing_back_row,
    facing_partners,
    fill_rows,
    narrowest_after,
    next_row,
    stack_all,
    take,
    zone_queues,
)
from gymplanner.layout.types import LayoutItem, Placement, Rect, Rotation, ZoneRect

CORE_MIN_SHARE = 1.0
"""Floor a band in a ``core`` configuration leaves beside its walkway for the islands, as a
share of the walkway width."""
_ENDLESS = 1e9
"""Row length that never limits an orientation (see ``_band_choices``)."""
CORE_MIN_LENGTH = 24.0
"""Shortest island row worth stacking (about a bench's width)."""


@dataclass(frozen=True)
class BandFrame:
    """Where a half's band may stand: along its outer side wall from ``y0`` to ``y1``."""

    half: Half
    y0: float
    y1: float
    max_depth: float
    """How far from the wall a footprint may reach."""
    row: RowFrame
    """The band as a row in its local frame; its depth bounds how far clearances and approach
    zones may reach from the wall."""

    @property
    def west(self) -> bool:
        """True for the band on the wall at the half's ``x0`` (the spine lies east)."""
        return self.half.frame.inward == "e"


@dataclass
class Band:
    """A built band: units along the wall, each set off the wall by its own offset."""

    frame: BandFrame
    row: Row
    offsets: list[float]
    """Distance from the wall to each unit's footprint."""
    depth: float
    """How far the band reaches from the wall: its room edge, where the open floor starts."""
    walk: float
    """Depth of the walkway the band needs beyond its room edge."""


@dataclass
class RingStack(Stack):
    """A half of a ring configuration: the rows along its front and back walls (``rows`` and
    ``back``, at most one each), the band along its side wall and the island rows beside it."""

    y0: float = 0.0
    """Front end of the band and the islands: behind the front row and its walkway."""
    y1: float = 0.0
    """Back end: in front of the back wall row and its walkway."""
    front_walk: float = 0.0
    """Depth of the walkway behind the front row, or 0 when it has none."""
    back_walk: float = 0.0
    """Depth of the aisle behind the band and islands: the walkway in front of the back wall
    row, or 0 when there is none."""
    band: Band | None = None
    core: Stack | None = None
    """The island rows, in a half of their own between the band and the spine."""


@dataclass
class RingBack(Stack):
    """A back wall row across the whole width, the spine stopping at the main-width walkway
    in front of it. The main aisle reaches the back wall through a gap in a corner (a rear
    exit), so long wall units (a dumbbell run) need not be split around the spine."""

    walk: float = 0.0
    """Depth of the walkway in front of the row."""
    exit: Rect | None = None
    """The gap in the corner from that walkway to the back wall."""


def arrange(ctx: Context, config: Config, items: Sequence[LayoutItem]) -> list[Stack] | None:
    """Rows (and bands) for every unit, or None when something does not fit."""
    if config.ring:
        return _stack_ring(ctx, config, items)
    return stack_all(ctx, config, items)


def _stack_ring(ctx: Context, config: Config, items: Sequence[LayoutItem]) -> list[Stack] | None:
    if not items:
        return [RingStack(h) for h in config.halves]
    if not config.halves:
        return None
    halves, back, floor = _back_across(ctx, config, items)
    stacks = [RingStack(h) for h in halves]
    if back is None:
        floor = back_wall_rows(ctx, list(stacks), items, longest_first=True)
    floor = facing_partners(ctx, list(stacks), floor, back) # Benches face their dumbbell run across its walkway, whatever else the halves hold.
    faced = {id(stack) for stack in stacks if len(stack.back) > (0 if back is not None else 1)}
    (queue,) = zone_queues(ctx, floor, flow=True)
    width = sum(h.width for h in halves)
    pending = sum(b.area * len(b.units) for b in queue)
    for stack in stacks: # A row along the front wall of each half; lanes and wall units stand along a side wall.
        fixed = [b for b in queue if not (b.units[0].flexible_length or b.units[0].against_wall)]
        step = next_row(ctx, stack, fixed, "dense", pending, width) if fixed else None
        if step is not None:
            pending = step[1]
            queue = [b for b in queue if b.units]
    for stack in stacks: # units facing the back wall row, sharing its walkway
        if not config.facing or not (stack.back or stack.half.back_allow > 0):
            continue
        if id(stack) in faced:
            continue # its benches already face the back wall row
        toward = _toward_back(ctx, queue)
        step = facing_back_row(ctx, stack, toward, pending, width) if toward else None
        if step is not None:
            pending = step[1]
            queue = [b for b in queue if b.units]
    frames = [_band_frame(ctx, stack, config) for stack in stacks]
    builders, taken = _fill_bands(ctx, frames, queue, config.ring == "open")
    pending -= sum(queue[b].area * count for b, count in taken.items())
    queue = take(queue, taken)
    for stack, frame, builder in zip(stacks, frames, builders, strict=True):
        if frame is not None and builder is not None and builder.slots:
            stack.band = _measure(builder, frame, config.ring == "open")
    out: list[Stack] = [*stacks, *([back] if back is not None else [])]
    if not queue:
        return out
    if config.ring != "core":
        return None
    cores = [c for c in (_core(ctx, s) for s in stacks) if c is not None]
    room = sum(c.half.frame.length * c.half.depth for c in cores) # Footprints never overlap, so the islands cannot hold more than their area.
    if sum(it.width_in * _min_length(it) for b in queue for it in b.units) > room + TOL:
        return None
    left = fill_rows(ctx, cores, queue, "flow", pending, sum(c.half.width for c in cores))
    return None if left is None else out


def _back_across(
    ctx: Context, config: Config, items: Sequence[LayoutItem]
) -> tuple[tuple[Half, ...], RingBack | None, list[LayoutItem]]:
    """With a half on each side of the spine, a back wall row across the whole width: the
    halves (ending at the walkway in front of it), the row, and the units left for the floor.
    Without wall units for it, the halves as configured and no row."""
    if not config.across or len(config.halves) != 2 or not any(it.against_wall for it in items):
        return config.halves, None, list(items)
    left, right = config.halves
    spine, sec = ctx.spine, ctx.secondary
    y0, y1 = left.y0, left.y1
    frame = RowFrame(length=right.x1 - left.x0 - spine, depth=y1 - y0, inward="e", inner_allow=spine, secondary=sec)
    back = RingBack(Half(len(config.halves), left.x0, right.x1 - spine, y0, y1, 0.0, frame))
    floor = back_wall_rows(ctx, [back], items, longest_first=True)
    if not back.back:
        return config.halves, None, list(items)
    back.walk = max(_ahead(back.back[0], sec), spine)
    end = y1 - back.back_used - back.walk
    if end - y0 < sec - TOL:
        return config.halves, None, list(items)
    back.exit = Rect(right.x1 - spine, end, spine, y1 - end) # The exit runs from the front of the walkway to the back wall, so it is main-aisle wide both ways however shallow the row is.
    halves = tuple(
        Half(
            index=h.index,
            x0=h.x0,
            x1=h.x1,
            y0=h.y0,
            y1=end,
            front_allow=h.front_allow,
            frame=replace(h.frame, depth=end - h.y0),
            back_allow=back.walk,
        )
        for h in config.halves
    )
    return halves, back, floor


def _band_frame(ctx: Context, stack: RingStack, config: Config) -> BandFrame | None:
    """Where the band may stand, and the walkways the front and back rows keep beside it.

    The stack always ends up with walkways that fit: the ones its front and back rows need,
    which the stacking left room for, or, when a band is accepted in a ``core`` configuration,
    the main-width walkway its own walkway reaches the main aisle through. A main-width walkway
    that does not fit between the rows rules the band out instead of running into them."""
    half, sec = stack.half, ctx.secondary
    front = stack.rows[-1] if stack.rows else None
    back = stack.back[-1] if stack.back else None
    need_front = _behind(front, sec) if front is not None else 0.0
    need_back = _ahead(back, sec) if back is not None else 0.0
    front_walk = front is not None and front.walk_s
    behind = half.back_allow if back is None else need_back if back.walk_n else 0.0 # A row facing the back wall row turns its back to the band: no walkway there.
    _keep_walks(stack, need_front, need_back, front_walk, behind)
    if config.ring == "core" and behind < ctx.spine - TOL:
        if back is not None and (front is None or (back.walk_n and need_back >= need_front)): # The walkway along the band reaches the main aisle through a main-width walkway across the half, in front of the back wall row if there is one.
            need_back = behind = max(need_back, ctx.spine)
        elif front is not None:
            need_front = max(need_front, ctx.spine)
            front_walk = True
        else:
            return None
    y0 = half.y0 + stack.front_used + need_front
    y1 = half.y1 - stack.back_used - need_back
    if y1 - y0 < sec - TOL:
        return None
    if config.ring == "open":
        max_depth, reach = half.width, half.width + half.frame.inner_allow
    else:
        reach = half.width - CORE_MIN_SHARE * sec
        max_depth = reach - sec
    if max_depth <= TOL:
        return None
    _keep_walks(stack, need_front, need_back, front_walk, behind)
    row = RowFrame(
        length=y1 - y0,
        depth=reach,
        inward="w" if half.frame.inward == "e" else "e",
        inner_allow=stack.front_walk,
        secondary=sec,
        outer_allow=stack.back_walk,
    )
    return BandFrame(half, y0, y1, max_depth, row)


def _keep_walks(
    stack: RingStack, need_front: float, need_back: float, front_walk: bool, behind: float
) -> None:
    """Record the walkways behind the front row and in front of the back row, and the floor
    between them that the band and the islands may use."""
    stack.y0 = stack.half.y0 + stack.front_used + need_front
    stack.y1 = stack.half.y1 - stack.back_used - need_back
    stack.front_walk = need_front if front_walk else 0.0
    stack.back_walk = behind


def _toward_back(ctx: Context, queue: list[Bin]) -> list[Bin]:
    """What a row facing the back wall row may take, the zones nearest the back first (free
    weights face a dumbbell run): no wall units, which the side walls take, no cardio, which
    keeps to the front, and stretching, which keeps to a corner, only last."""
    rank = {z: i for i, z in enumerate(ctx.rules.zone_order)}
    keep = [
        b
        for b in queue
        if not b.units[0].against_wall
        and b.units[0].zone not in FACING_ZONES
        and not b.units[0].flexible_length
    ]
    return sorted(keep, key=lambda b: (b.units[0].zone in CORNER_ZONES, -rank.get(b.units[0].zone, len(rank))))


def _ahead(row: Row, secondary: float) -> float:
    """Depth a row needs in front of it: its walkway there, or room for its clearances."""
    if row.walk_n:
        return max(row.reach_n, secondary, row.appr_n)
    return max(0.0, row.reach_n)


def _behind(row: Row, secondary: float) -> float:
    """Depth a row needs behind it."""
    if row.walk_s:
        return max(row.reach_s, secondary, row.appr_s)
    return max(0.0, row.reach_s)


def _fill_bands(
    ctx: Context, frames: list[BandFrame | None], queue: list[Bin], all_or_none: bool
) -> tuple[list[RowBuilder | None], dict[int, int]]:
    """Line the bands with units from the queue, each going to the band filled least so far;
    returns the bands and how many units each bin gave them (always its first ones). Kinds that
    fit neither band wait for the islands.

    Wall units go first, then the rest in queue order. When that leaves units over, the widest
    go first instead (first fit decreasing, wall units still ahead of the rest, so that a wide
    free-standing unit never pushes a wall unit off the wall into the islands) if that leaves
    less over; each band then keeps its units in queue order when they still fit that way, so
    zones run front to back. With ``all_or_none`` (no islands to take the rest) the second order
    is skipped when it could not place everything."""
    wall = [block.units[0].against_wall for block in queue]
    orders = [sorted(range(len(queue)), key=lambda b: not wall[b])]
    orders.append(sorted(range(len(queue)), key=lambda b: (not wall[b], -_along(queue[b].units[0]))))
    best: tuple[float, list[RowBuilder | None], dict[int, int]] | None = None
    for order in orders:
        builders = [RowBuilder(f.row, "n") if f is not None else None for f in frames]
        taken: dict[int, int] = {}
        narrowest = narrowest_after([queue[b] for b in order])
        for k, b in enumerate(order):
            if all(
                f is None or u is None or u.end + narrowest[k] > f.row.length + TOL
                for f, u in zip(frames, builders, strict=True)
            ):
                break # the bands are full for every unit left
            count = 0
            for unit in queue[b].units:
                if not _band_add(ctx, frames, builders, unit):
                    break # the rest of the kind fits no better
                count += 1
            if count:
                taken[b] = count
        left = sum(block.area * (len(block.units) - taken.get(b, 0)) for b, block in enumerate(queue))
        if best is None or left < best[0] - TOL:
            best = (left, builders, taken)
        if left <= TOL or (all_or_none and not _could_take_rest(frames, builders, queue, taken)):
            break
    assert best is not None
    _, builders, taken = best
    rank = {id(unit): b for b, block in enumerate(queue) for unit in block.units}
    return [_in_queue_order(b, rank) for b in builders], taken


def _could_take_rest(
    frames: list[BandFrame | None],
    builders: list[RowBuilder | None],
    queue: list[Bin],
    taken: dict[int, int],
) -> bool:
    """Whether the floor the bands have left could hold the footprints they left over: when
    it could not, no other order would place them all (footprints never overlap)."""
    free = sum(
        max(0.0, f.row.length - b.end) * f.max_depth
        for f, b in zip(frames, builders, strict=True)
        if f is not None and b is not None
    )
    rest = sum(it.width_in * _min_length(it) for b, block in enumerate(queue) for it in block.units[taken.get(b, 0) :])
    return rest <= free + TOL


def _along(item: LayoutItem) -> float:
    """Wall length a unit would take in a band, at most: its larger side."""
    return max(item.width_in, item.length_in if not item.flexible_length else 0.0)


def _in_queue_order(builder: RowBuilder | None, rank: dict[int, int]) -> RowBuilder | None:
    """The band with its units in queue order (zones front to back) if they still fit."""
    if builder is None or not builder.slots:
        return builder
    slots = sorted(builder.slots, key=lambda s: rank[id(s.item)])
    if [id(s.item) for s in slots] == [id(s.item) for s in builder.slots]:
        return builder
    ordered = RowBuilder(builder.frame, builder.walk_edge)
    for slot in slots:
        if not ordered.try_add(slot.item, Choice(slot.pose, slot.mode)):
            return builder
    return ordered


def _band_add(
    ctx: Context,
    frames: list[BandFrame | None],
    builders: list[RowBuilder | None],
    unit: LayoutItem,
) -> bool:
    shortest = min(unit.width_in, _min_length(unit))
    bands = [
        (f, b)
        for f, b in zip(frames, builders, strict=True)
        if f is not None and b is not None and b.end + shortest <= f.row.length + TOL
    ]
    bands.sort(key=lambda fb: fb[1].fill)
    for frame, builder in bands:
        if unit.flexible_length:
            choices = _band_lane(ctx, unit, frame, builder)
        else:
            choices = _band_choices(ctx, unit, frame)
        for choice in choices:
            if builder.end + choice.pose.w <= frame.row.length + TOL and builder.try_add(unit, choice):
                return True
    return False


def _band_lane(
    ctx: Context, item: LayoutItem, frame: BandFrame, builder: RowBuilder
) -> tuple[Choice, ...]:
    """A flexible unit (a turf lane) runs along the wall, as long as what is left of the band
    allows up to its nominal length, but never shorter than its minimum."""
    nominal = item.length_in
    shortest = min(nominal, item.min_length_in or nominal)
    for option in flexible_options(item, frame.row, ("n",), (90, 270), ctx.pose):
        if not _fits_band(option.choice, frame):
            continue
        length = min(option.max_length, builder.room(option.choice))
        if length >= shortest - TOL:
            pose = option.choice.pose
            if length < nominal - TOL:
                pose = ctx.pose(item, pose.rotation, length)
            return (Choice(pose, option.choice.mode),)
    return ()


def _band_choices(ctx: Context, item: LayoutItem, frame: BandFrame) -> tuple[Choice, ...]:
    """Orientations of a unit in a band, best first: its back to the wall (cardio facing the
    wall, its rear zone toward the room), then turned another way. Whether one fits what is
    left of the band's length is for the row builder to say, so they depend on the band's
    depth alone and are shared between attempts."""
    row = frame.row
    key = (ctx.kind(item), row.inward, row.depth, frame.max_depth)
    found = ctx.bands.get(key)
    if found is None:
        rotations: tuple[Rotation, ...]
        if item.against_wall:
            rotations = (0,)
        elif item.zone in FACING_ZONES:
            rotations = (180, 0, 90, 270)
        else:
            rotations = rotation_order(item, "n", False)
        endless = replace(row, length=_ENDLESS, inner_allow=0.0, outer_allow=0.0)
        options = pose_options(item, endless, ("n",), rotations, ctx.pose, len(rotations))
        found = ctx.bands[key] = tuple(c for c in options if _fits_band(c, frame))
    return found


def _min_length(item: LayoutItem) -> float:
    if item.flexible_length:
        return min(item.length_in, item.min_length_in or item.length_in)
    return item.length_in


def _fits_band(choice: Choice, frame: BandFrame) -> bool:
    """Whether the unit stands within the band's depth, and so do its zones once aligned."""
    pose = choice.pose
    if pose.clear["s"] + pose.h > frame.max_depth + TOL:
        return False
    if choice.mode != "n": # aligned with the room edge, at most ``max_depth`` from the wall
        return frame.max_depth + pose.clear["n"] <= frame.row.depth + TOL
    return True


def _measure(builder: RowBuilder, frame: BandFrame, open_floor: bool) -> Band:
    """Set each unit off the wall: as close as its clearance allows while its approach zone
    still reaches the band's room edge; units reached from the side stand at that edge."""
    row = builder.finish("wall")
    half, sec = frame.half, frame.row.secondary
    depth = max(s.pose.clear["s"] + s.pose.h for s in row.slots)
    if open_floor and depth > half.width - sec + TOL:
        depth = half.width # too little floor for a walkway: the units open onto the spine
    offsets: list[float] = []
    walk = sec
    for slot in row.slots:
        pose = slot.pose
        if slot.mode == "n":
            offset = max(pose.clear["s"], depth - pose.h - pose.approach["n"])
            walk = max(walk, offset + pose.h + pose.approach["n"] - depth)
        else:
            offset = depth - pose.h
        walk = max(walk, offset + pose.h + pose.clear["n"] - depth)
        offsets.append(offset)
    return Band(frame, row, offsets, depth, walk)


def _core(ctx: Context, stack: RingStack) -> Stack | None:
    """The island half beside the band, if the floor there takes a row.

    Its rows run from the spine to the band's walkway, their clearances reaching into it; the
    half itself reaches the band's room edge, so the walkways between the rows run on to the
    band's walkway and stay walkway-wide however narrow the islands are."""
    half, sec = stack.half, ctx.secondary
    band = stack.band
    depth, walk = (band.depth, band.walk) if band is not None else (0.0, 0.0)
    length = half.width - depth - walk
    if length < CORE_MIN_LENGTH - TOL or stack.y1 - stack.y0 < sec - TOL:
        return None
    west = half.frame.inward == "e"
    frame = RowFrame(
        length=length,
        depth=stack.y1 - stack.y0,
        inward=half.frame.inward,
        inner_allow=half.frame.inner_allow,
        secondary=sec,
        outer_allow=walk if band is not None else half.frame.outer_allow,
    )
    core = Half(
        index=half.index,
        x0=half.x0 + depth if west else half.x0,
        x1=half.x1 if west else half.x1 - depth,
        y0=stack.y0,
        y1=stack.y1,
        front_allow=stack.front_walk if stack.rows else half.front_allow,
        frame=frame,
        back_allow=stack.back_walk,
    )
    stack.core = Stack(core)
    return stack.core


def band_layout(band: Band, cap: float, secondary: float) -> tuple[list[Placement], list[ZoneRect]]:
    """The band's placements and zone rects. Spare length spaces the units apart (up to
    ``cap`` per gap); the rest stays at the back end of the band. A zone reaches from the wall
    across the band and its walkway."""
    frame, row = band.frame, band.row
    ts = spread(row, frame.row, cap, None)
    placements: list[Placement] = []
    for slot, t, offset in zip(row.slots, ts, band.offsets, strict=True):
        rect = _world(frame, t, offset, slot.pose.w, slot.pose.h)
        rotation = ROTATIONS[(ROTATIONS.index(slot.pose.rotation) + (1 if frame.west else 3)) % 4]
        placements.append(
            Placement(item=slot.item, rect=rect, envelope=item_envelope(slot.item, rect, rotation), rotation=rotation)
        )
    reach = min(frame.half.width, band.depth + band.walk)
    zones = [
        ZoneRect(zone, _world(frame, lo, 0.0, hi - lo, reach))
        for zone, lo, hi in _runs(row, ts, frame.row, secondary)
    ]
    return placements, zones


def band_walkway(band: Band, islands: bool) -> Rect | None:
    """The walkway the band opens onto: along it when islands stand beyond, otherwise the
    open floor up to the spine (none when the band's units reach the spine themselves)."""
    frame = band.frame
    width = band.walk if islands else frame.half.width - band.depth
    if width <= TOL:
        return None
    return _world(frame, 0.0, band.depth, frame.y1 - frame.y0, width)


def _world(frame: BandFrame, t: float, offset: float, along: float, across: float) -> Rect:
    """A rect given in the band's frame: ``t`` from the front end, ``offset`` from the wall."""
    half = frame.half
    x = half.x0 + offset if frame.west else half.x1 - offset - across
    return Rect(x, frame.y0 + t, across, along)


def _runs(
    row: Row, ts: list[float], frame: RowFrame, secondary: float
) -> list[tuple[ZoneId, float, float]]:
    """``(zone, lo, hi)`` along the band for each zone run: its units and their clearances,
    split from the next run halfway between their footprints; the first run reaches the front
    end of the band and the last one the back end when they come close."""
    slots = row.slots
    runs = row.runs()
    cuts = [(ts[stop - 1] + slots[stop - 1].pose.w + ts[stop]) / 2 for _, _, stop in runs[:-1]]
    out: list[tuple[ZoneId, float, float]] = []
    for r, (zone, first, stop) in enumerate(runs):
        lo = min(ts[k] - slots[k].pose.clear[frame.inward] for k in range(first, stop))
        hi = max(ts[k] + slots[k].pose.w + slots[k].pose.clear[frame.outward] for k in range(first, stop))
        if r == 0 and lo <= secondary:
            lo = 0.0
        if r == len(runs) - 1 and frame.length - hi <= secondary:
            hi = frame.length
        lo = max(lo, 0.0, cuts[r - 1] if r else 0.0)
        hi = min(hi, frame.length, cuts[r] if r < len(cuts) else frame.length)
        out.append((zone, lo, hi))
    return out
