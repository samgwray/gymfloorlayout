"""Floor layout engine: a main aisle, zones in order from the entrance, and rows of equipment.

1. A main aisle (the spine) runs from the entrance to the back wall. Centred on the entrance
   it splits the training floor into two halves; a second configuration runs it along the
   side wall nearest the entrance, for floors too narrow to split (or wherever that fits
   more). It is joined to the door by a cross aisle, unless the door is close enough to that
   wall for the spine to take in a main-aisle-wide gate around it and still leave room for a
   row beside it, which keeps every row out of the doorway.
2. Rows of equipment run from the spine out to the side walls and stack front to back in zone
   order, both halves at the same pace (``stacking``). Cardio faces the entrance with its rear
   safety zone doubling as the walkway behind it; other rows pair up back-to-back around
   shared walkways; each half's back wall holds a row of wall units. On floors too shallow
   for a row per zone, zones share rows.
3. Ring configurations (``ring``) also line the side walls, as small gyms and hotel rooms do:
   a row along the front wall and one along the back wall (across the whole width, the main
   aisle leaving through a rear exit in a corner, or split by the spine), bands of units
   backed onto the side walls between them, and either open floor (with or without a row of
   benches facing the back wall row) or island rows beside the bands. On small floors the
   walls are where most of the equipment fits.
4. Each family of configurations (rows, rings) is searched on its own for the most valuable
   units it holds, leaving out the lowest-priority ones when not everything fits
   (``search``); the family keeping the most priority wins, then the most units. When several
   configurations hold everything, the one with the most cardio facing the entrance wins (the
   zones then read in order from the door), then the one that gives lanes their full length,
   then the one that leaves the most floor free (rows on a tie).
5. Spare depth widens the walkways between rows a little. The rest stays open floor between
   the rows that keep to the front (cardio by the entrance first) and those that keep to the
   back (the back wall row, a last row facing the room, stretching), so rows always start at
   the front of the floor. Spare row length spaces units apart. Zone rects cover each zone's
   units with the clearances and walkways they need, so zone areas measure the floor the
   equipment uses rather than the floor left over.

Every result is re-checked against the hard rules. A configuration whose plan breaks one
(never expected) gives way to the next best; failing that, the units that break a rule are
dropped, and a plan whose aisles themselves are broken falls back to the bare main aisle, so
no invalid plan is ever returned.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import pairwise

from gymplanner.catalog.schema import ZoneId
from gymplanner.domain import Room
from gymplanner.layout.geometry import TOL, Direction, envelope_of
from gymplanner.layout.ring import RingBack, RingStack, band_layout, band_walkway
from gymplanner.layout.rows import Row, RowFrame, Slot, spread
from gymplanner.layout.search import Outcome, placeable, search
from gymplanner.layout.stacking import (
    CORNER_ZONES,
    FACING_ZONES,
    Config,
    Context,
    Half,
    RingMode,
    Stack,
    front_gap,
    row_gap,
    trailing,
)
from gymplanner.layout.types import (
    LayoutItem,
    LayoutResult,
    LayoutRules,
    Placement,
    Rect,
    ZoneRect,
)
from gymplanner.layout.validate import Issue, find_issues

ENTRANCE_SHARE = {"left": 0.15, "center": 0.5, "right": 0.85}
"""Door position along the front wall as a share of the floor's width."""
SPREAD_CAP_SHARE = 0.5
"""Spare row length added per gap between units, as a share of the secondary aisle width."""
BREATHING_SHARE = 1.0
"""Spare depth added per walkway between rows, as a share of the secondary aisle width."""
OPEN_MAX_HALF_IN = 288.0
"""Widest half an ``open`` ring is tried in (24 ft). Its floor beside the bands stays clear as
circulation, which pays off only while the bands, their walkways and a row facing the back
wall nearly fill the half; a wider half has room for islands there (``core``)."""
NARROW_HALF_IN = 96.0
"""A floor is too narrow to split when a central aisle leaves no side this wide (8 ft)."""


def plan_layout(room: Room, items: list[LayoutItem], rules: LayoutRules) -> LayoutResult:
    """Place as many units as fit, leaving out the lowest-priority ones when space runs out."""
    width = max(0.0, float(room.width_in))
    depth = max(0.0, float(room.depth_in))
    empty = LayoutResult(
        width_in=width,
        depth_in=depth,
        entrance_x_in=width * ENTRANCE_SHARE.get(room.entrance, 0.5),
        zones=[],
        aisles=[],
        placements=[],
    )
    order = sorted(items, key=lambda it: (-it.priority, it.uid))
    ctx = Context(rules)
    configs, narrow = _configs(ctx, width, depth, empty.entrance_x_in)
    if not configs:
        empty.unplaced = order
        if order:
            empty.warnings.append("The training floor is too small for an aisle and equipment.")
        return empty

    outcome = search(ctx, configs, order, _rank)
    result = _result(ctx, empty, outcome, order)
    issues = find_issues(result, rules)
    tried = [outcome.config] # A configuration whose plan breaks a hard rule (never expected) gives way to the others.
    while issues:
        rest = [c for c in configs if all(c is not t for t in tried)]
        if not rest:
            break
        retry = search(ctx, rest, order, _rank)
        tried.append(retry.config)
        candidate = _result(ctx, empty, retry, order)
        found = find_issues(candidate, rules)
        if not found:
            outcome, result, issues = retry, candidate, found
    _enforce(result, rules, issues, configs[0])
    result.notes += _notes(outcome, narrow, result)
    result.warnings += _shortened(result)
    return result


def fits_alone(room: Room, items: list[LayoutItem], rules: LayoutRules) -> list[LayoutItem]:
    """The items the floor can hold one at a time, each on its own with the aisles it needs: a
    unit that fails this is never placed, whatever else the plan holds."""
    ctx = Context(rules)
    width, depth = max(0.0, float(room.width_in)), max(0.0, float(room.depth_in))
    configs, _ = _configs(ctx, width, depth, width * ENTRANCE_SHARE.get(room.entrance, 0.5))
    return placeable(ctx, configs, items) if configs else []


def _result(
    ctx: Context, empty: LayoutResult, outcome: Outcome, order: list[LayoutItem]
) -> LayoutResult:
    """The plan for a search outcome."""
    placements, walkways, zones = _finalize(ctx, outcome.stacks)
    kept = {p.item.uid for p in placements}
    return replace(
        empty,
        placements=placements,
        aisles=[*_main_aisle(outcome), *walkways],
        zones=zones,
        unplaced=[it for it in order if it.uid not in kept],
        warnings=list(empty.warnings),
    )


def _main_aisle(outcome: Outcome) -> tuple[Rect, ...]:
    """The configuration's main aisle; with a back wall row across the whole width, the spine
    stops at the walkway in front of it (which leads on to the rear exit)."""
    main = outcome.config.main
    back = next((s for s in outcome.stacks if isinstance(s, RingBack)), None)
    if back is None:
        return main
    spine = main[0]
    end = back.half.y1 - back.back_used
    return (Rect(spine.x, spine.y, spine.w, end - spine.y), *main[1:])


def _rank(outcome: Outcome) -> tuple[float, float, float]:
    """How well a configuration that holds every unit uses the floor: the most cardio facing
    the entrance (in rows at the front, so the zones read in order from the door), then the
    most footprint (lanes at their longest), then the most floor left free."""
    return (round(_cardio_facing_the_door(outcome), 3), round(_footprint(outcome), 3), round(_spare(outcome), 3))


def _slots(outcome: Outcome) -> list[Slot]:
    rows: list[Row] = []
    for stack in outcome.stacks:
        rows += stack.ordered()
        if isinstance(stack, RingStack):
            rows += [stack.band.row] if stack.band is not None else []
            rows += stack.core.ordered() if stack.core is not None else []
    return [slot for row in rows for slot in row.slots]


def _cardio_facing_the_door(outcome: Outcome) -> float:
    cardio = [s for s in _slots(outcome) if s.item.zone in FACING_ZONES]
    return sum(s.pose.rotation == 0 for s in cardio) / len(cardio) if cardio else 1.0


def _footprint(outcome: Outcome) -> float:
    return sum(s.pose.w * s.pose.h for s in _slots(outcome))


def _spare(outcome: Outcome) -> float:
    """Floor still free once every unit stands at its minimum spacing: the depth a half has
    left across its width, and in a ring the floor beside its band and islands that neither
    needs."""
    free = 0.0
    for stack in outcome.stacks:
        half = stack.half
        if isinstance(stack, RingBack):
            continue # a row along the back wall, which the halves end in front of
        if not isinstance(stack, RingStack):
            free += half.width * max(0.0, half.depth - stack.used)
            continue
        middle = max(0.0, stack.y1 - stack.y0)
        used = 0.0
        if stack.band is not None:
            used += (stack.band.depth + stack.band.walk) * stack.band.row.end
        if stack.core is not None:
            used += stack.core.half.width * stack.core.used
        free += max(0.0, half.width * middle - used)
    return free


def _configs(
    ctx: Context, width: float, depth: float, entrance_x: float
) -> tuple[list[Config], bool]:
    """Every configuration to try, best first, and whether the floor is too narrow to split.

    The spine on the entrance comes first; when it differs, a spine along the side wall nearest
    the entrance follows. Rows are tried tidy, then dense; zones sharing rows come last. Rings
    follow: side walls lined around open floor, then around island rows.
    """
    spine, sec = ctx.spine, ctx.secondary
    if width < spine - TOL or depth < spine - TOL:
        return [], True
    layouts: list[tuple[tuple[Rect, ...], tuple[Half, ...]]] = []

    x = min(max(entrance_x - spine / 2, 0.0), width - spine)
    w = spine
    if x < sec: # a strip too narrow for a row joins the aisle
        w, x = w + x, 0.0
    if width - (x + w) < sec:
        w = width - x
    halves: list[Half] = []
    if x > 0:
        halves.append(_half(ctx, len(halves), 0.0, x, 0.0, depth, "e", 0.0, w))
    if x + w < width - TOL:
        halves.append(_half(ctx, len(halves), x + w, width, 0.0, depth, "w", 0.0, w))
    layouts.append(((Rect(x, 0.0, w, depth),), tuple(halves)))
    narrow = all(h.width < NARROW_HALF_IN for h in halves)

    near_left = entrance_x <= width / 2
    door = entrance_x if near_left else width - entrance_x # from the side wall nearest it
    gate = max(spine, door + spine / 2) # Keep the first row clear of the door; use a front cross aisle when the spine cannot meet the entrance.
    joined = door <= spine + TOL and width - gate >= sec - TOL
    sw = min(width, gate) if joined else spine
    sx = 0.0 if near_left else width - sw
    hx0, hx1 = (sw, width) if near_left else (0.0, width - sw)
    if (abs(sx - x) > TOL or abs(sw - w) > TOL) and hx1 - hx0 >= sec:
        rect = Rect(sx, 0.0, sw, depth)
        aisles = (rect,) if joined else (rect, Rect(0.0, 0.0, width, spine))
        y0 = 0.0 if joined else spine
        if depth - y0 >= sec:
            inward: Direction = "w" if near_left else "e"
            allow = 0.0 if joined else spine
            layouts.append((aisles, (_half(ctx, 0, hx0, hx1, y0, depth, inward, allow, sw),)))

    rows = [Config(main, h, mode) for main, h in layouts for mode in ("tidy", "dense")]
    rows += [Config(main, h, "flow") for main, h in layouts]
    kinds: tuple[tuple[RingMode, bool], ...] = (("open", False), ("open", True), ("core", False))
    rings = [
        Config(main, h, "flow", ring, across, facing)
        for across in (True, False)
        for ring, facing in kinds
        for main, h in layouts
        if (not across or len(h) == 2)
        and (ring == "core" or all(half.width <= OPEN_MAX_HALF_IN for half in h))
    ]
    return rows + rings, narrow


def _half(
    ctx: Context,
    index: int,
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    inward: Direction,
    front_allow: float,
    spine_width: float,
) -> Half:
    frame = RowFrame(length=x1 - x0, depth=y1 - y0, inward=inward, inner_allow=spine_width, secondary=ctx.secondary)
    return Half(index, x0, x1, y0, y1, front_allow, frame)


@dataclass(frozen=True)
class _Laid:
    """A half's rows at their final depth positions."""

    half: Half
    rows: list[Row]
    gaps: list[float]
    """Gap before each row, then the gap behind the last one."""
    walks: list[bool]
    """Whether each gap is a walkway."""
    open_at: int
    """The gap between the front rows and those against the back wall: it keeps the floor
    left over once the walkways have their breathing room."""
    tops: list[float]


def _finalize(
    ctx: Context, stacks: list[Stack]
) -> tuple[list[Placement], list[Rect], list[ZoneRect]]:
    placements: list[Placement] = []
    walkways: list[Rect] = []
    zones: list[ZoneRect] = []
    cap = SPREAD_CAP_SHARE * ctx.secondary
    for stack in stacks:
        if isinstance(stack, RingStack):
            _finalize_ring(ctx, stack, placements, walkways, zones)
            continue
        if isinstance(stack, RingBack):
            _finalize_back(ctx, stack, placements, walkways, zones)
            continue
        if not stack.rows and not stack.back:
            continue
        laid = _lay(ctx, stack)
        placements += _placed(laid, cap)
        walkways += _walkways(ctx, laid)
        zones += _zone_rects(ctx, laid, [_spread(laid, row, cap) for row in laid.rows])
    return placements, walkways, _merged(zones)


def _placed(laid: _Laid, cap: float) -> list[Placement]:
    half = laid.half
    out: list[Placement] = []
    for row, top in zip(laid.rows, laid.tops, strict=True):
        for slot, t in zip(row.slots, _spread(laid, row, cap), strict=True):
            pose = slot.pose
            x = half.x0 + t if half.frame.inward == "w" else half.x1 - t - pose.w
            y = top if slot.align == "n" else top + row.depth - pose.h
            rect = Rect(x, y, pose.w, pose.h)
            out.append(
                Placement(item=slot.item, rect=rect, envelope=envelope_of(rect, pose.clear), rotation=pose.rotation)
            )
    return out


def _spread(laid: _Laid, row: Row, cap: float) -> list[float]:
    return spread(row, laid.half.frame, cap, _anchor_from(row))


def _finalize_ring(
    ctx: Context,
    stack: RingStack,
    placements: list[Placement],
    walkways: list[Rect],
    zones: list[ZoneRect],
) -> None:
    """A ring half: its front and back rows where the stacking put them, the walkways they
    keep beside the band, the band, and the islands in their own half."""
    half, sec = stack.half, ctx.secondary
    cap = SPREAD_CAP_SHARE * sec
    if stack.rows or stack.back:
        laid = _skeleton(ctx, stack)
        placements += _placed(laid, cap)
        zones += _zone_rects(ctx, laid, [_spread(laid, row, cap) for row in laid.rows])
        first = laid.rows[0]
        if stack.rows and first.walk_n and laid.gaps[0] > TOL:
            if half.front_allow > 0: # it opens onto the cross aisle in front
                need = max(sec, first.appr_n)
                walkways.append(_aisle_link(half, half.y0, laid.gaps[0], need, front=True))
            elif laid.walks[0]: # onto a walkway along the front wall
                walkways.append(Rect(half.x0, half.y0, half.width, laid.gaps[0]))
        walkways += _back_walkways(laid)
    if stack.front_walk > TOL:
        walkways.append(Rect(half.x0, stack.y0 - stack.front_walk, half.width, stack.front_walk))
    if stack.back_walk > TOL:
        walkways.append(Rect(half.x0, stack.y1, half.width, stack.back_walk))
    core = stack.core if stack.core is not None and stack.core.rows else None
    if stack.band is not None:
        placed, band_zones = band_layout(stack.band, cap, sec)
        placements += placed
        zones += band_zones
        walk = band_walkway(stack.band, islands=core is not None)
        if walk is not None:
            walkways.append(walk)
    if core is not None:
        laid = _lay(ctx, core)
        placements += _placed(laid, cap)
        walkways += _walkways(ctx, laid)
        zones += _zone_rects(ctx, laid, [_spread(laid, row, cap) for row in laid.rows])


def _finalize_back(
    ctx: Context,
    back: RingBack,
    placements: list[Placement],
    walkways: list[Rect],
    zones: list[ZoneRect],
) -> None:
    """A back wall row across the whole width, the main-width walkway in front of it, and the
    rear exit from that walkway to the back wall."""
    laid = _skeleton(ctx, back)
    cap = SPREAD_CAP_SHARE * ctx.secondary
    placements += _placed(laid, cap)
    zones += _zone_rects(ctx, laid, [_spread(laid, row, cap) for row in laid.rows])
    half, end = back.half, back.half.y1 - back.back_used
    if back.exit is not None:
        walkways.append(Rect(half.x0, end - back.walk, back.exit.x - half.x0, back.walk))
        walkways.append(back.exit)


def _skeleton(ctx: Context, stack: Stack) -> _Laid:
    """The front rows from the front wall and the back rows from the back wall at their
    minimum gaps, with the floor between them open (it holds the band and the islands)."""
    half, sec = stack.half, ctx.secondary
    rows = stack.ordered()
    first = front_gap(rows[0], half, sec)
    gaps, walks = [first[0]], [first[1]]
    for a, b in pairwise(rows):
        gap, walk = row_gap(a, b, sec)
        gaps.append(gap)
        walks.append(walk)
    tail = trailing(rows[-1], half, sec)
    gaps.append(tail[0])
    walks.append(tail[1])
    open_at = len(stack.rows)
    gaps[open_at] += max(0.0, half.depth - sum(gaps) - sum(r.depth for r in rows))
    tops: list[float] = []
    y = half.y0 + gaps[0]
    for i, row in enumerate(rows):
        tops.append(y)
        y += row.depth + gaps[i + 1]
    return _Laid(half, rows, gaps, walks, open_at, tops)


def _back_walkways(laid: _Laid) -> list[Rect]:
    """The walkways among a ring half's back rows: in front of the back wall row when a row
    faces it, and from a row facing the aisle behind the half onto that aisle."""
    half, rows, n = laid.half, laid.rows, len(laid.rows)
    out: list[Rect] = []
    for i in range(laid.open_at + 1, n + 1):
        top = laid.tops[i - 1] + rows[i - 1].depth
        size = (half.y1 if i == n else laid.tops[i]) - top
        if size <= TOL:
            continue
        if i < n and laid.walks[i]:
            out.append(Rect(half.x0, top, half.width, size))
        elif i == n and half.back_allow > 0 and rows[-1].walk_s:
            out.append(Rect(half.x0, top, half.width, size + half.back_allow))
    return out


def _lay(ctx: Context, stack: Stack) -> _Laid:
    """Gaps at their minimum, plus breathing room for the walkways; the rest stays open."""
    half, rows, sec = stack.half, stack.ordered(), ctx.secondary
    first, front_walk = front_gap(rows[0], half, sec)
    gaps, walks = [first], [front_walk]
    for a, b in pairwise(rows):
        gap, walk = row_gap(a, b, sec)
        gaps.append(gap)
        walks.append(walk)
    tail, tail_walk = trailing(rows[-1], half, sec)
    gaps.append(tail)
    walks.append(tail_walk)

    n = len(rows) # Pack rows from open_at toward the back wall, including stretching; keep the earlier rows toward the entrance.
    open_at = len(stack.rows)
    if not stack.back and not tail_walk and (rows[-1].kind == "alternating" or rows[-1].walk_s):
        open_at = n - 1
    while open_at > 0 and all(s.item.zone in CORNER_ZONES for s in rows[open_at - 1].slots):
        open_at -= 1
    spare = max(0.0, half.depth - sum(gaps) - sum(r.depth for r in rows))
    takers = [i for i in range(1, n) if walks[i] and i != open_at]
    extra = min(BREATHING_SHARE * sec, spare / (len(takers) + 1)) if takers else 0.0
    for i in takers:
        gaps[i] += extra
    gaps[open_at] += spare - extra * len(takers)

    tops: list[float] = []
    y = half.y0 + gaps[0]
    for i, row in enumerate(rows):
        tops.append(y)
        y += row.depth + gaps[i + 1]
    return _Laid(half, rows, gaps, walks, open_at, tops)


def _anchor_from(row: Row) -> int | None:
    zone, first, _ = row.runs()[-1]
    return first if zone in CORNER_ZONES else None


def _walkways(ctx: Context, laid: _Laid) -> list[Rect]:
    """Each walkway spans its gap, except in the open gap, where a walkway runs along each row
    that opens onto it, as deep as that row needs, and the floor between stays open."""
    half, rows, sec = laid.half, laid.rows, ctx.secondary
    n = len(rows)
    out: list[Rect] = []
    for i in range(n + 1):
        top = half.y0 if i == 0 else laid.tops[i - 1] + rows[i - 1].depth
        bottom = half.y1 if i == n else laid.tops[i]
        size = bottom - top
        if size <= TOL:
            continue
        above = max(sec, rows[i - 1].appr_s) if i > 0 and rows[i - 1].walk_s else 0.0
        below = max(sec, rows[i].appr_n) if i < n and rows[i].walk_n else 0.0
        if i == 0 and half.front_allow > 0 and below:
            out.append(_aisle_link(half, top, size, below, front=True))
            continue
        if i == n and half.back_allow > 0 and above:
            out.append(_aisle_link(half, top, size, above, front=False))
            continue
        if i != laid.open_at:
            if laid.walks[i]:
                out.append(Rect(half.x0, top, half.width, size))
            continue
        if above + below >= size - TOL:
            if above or below:
                out.append(Rect(half.x0, top, half.width, size))
            continue
        if above:
            out.append(Rect(half.x0, top, half.width, above))
        if below:
            out.append(Rect(half.x0, bottom - below, half.width, below))
    return out


def _aisle_link(half: Half, top: float, size: float, need: float, front: bool) -> Rect:
    """The walkway of a row that opens onto the aisle in front of (or behind) its half, across
    a gap of ``size``: a shallow gap joins the aisle, a deeper one gets a walkway along the
    row."""
    if front:
        if size < need - TOL:
            return Rect(half.x0, top - half.front_allow, half.width, half.front_allow + size)
        return Rect(half.x0, top + size - need, half.width, need)
    if size < need - TOL:
        return Rect(half.x0, top, half.width, size + half.back_allow)
    return Rect(half.x0, top, half.width, need)


def _zone_rects(ctx: Context, laid: _Laid, positions: list[list[float]]) -> list[ZoneRect]:
    """A rect per run of one zone in a row: as long as the run's units and their clearances,
    as deep as the row plus its share of the gaps on either side (only what the row needs of
    the open gap)."""
    half, rows, gaps, sec = laid.half, laid.rows, laid.gaps, ctx.secondary
    n = len(rows)
    out: list[ZoneRect] = []
    for i, row in enumerate(rows):
        top, bottom = laid.tops[i], laid.tops[i] + row.depth
        need_up = max(row.reach_n, row.appr_n, sec if row.walk_n else 0.0)
        need_down = max(row.reach_s, row.appr_s, sec if row.walk_s else 0.0)
        if i == laid.open_at:
            up = min(need_up, gaps[i] if i == 0 else gaps[i] / 2)
        else:
            up = gaps[i] if i == 0 else gaps[i] / 2
        if i + 1 == laid.open_at:
            down = min(need_down, gaps[n] if i + 1 == n else gaps[i + 1] / 2)
        else:
            down = gaps[n] if i + 1 == n else gaps[i + 1] / 2
        for zone, lo, hi in _run_extents(row, positions[i], half.frame, sec):
            if half.frame.inward == "w":
                x0, x1 = half.x0 + lo, half.x0 + hi
            else:
                x0, x1 = half.x1 - hi, half.x1 - lo
            out.append(ZoneRect(zone, Rect(x0, top - up, x1 - x0, bottom + down - (top - up))))
    return out


def _run_extents(
    row: Row, ts: list[float], frame: RowFrame, secondary: float
) -> list[tuple[ZoneId, float, float]]:
    """``(zone, lo, hi)`` along the row for each zone run: its units and their clearances,
    split from the next run halfway between their footprints. A run starting at the main
    aisle reaches it, and a run ending close to the side wall reaches the wall."""
    runs = row.runs()
    slots = row.slots
    cuts = [(ts[stop - 1] + slots[stop - 1].pose.w + ts[stop]) / 2 for _, _, stop in runs[:-1]]
    out: list[tuple[ZoneId, float, float]] = []
    for r, (zone, first, stop) in enumerate(runs):
        lo = min(ts[k] - slots[k].pose.clear[frame.inward] for k in range(first, stop))
        hi = max(ts[k] + slots[k].pose.w + slots[k].pose.clear[frame.outward] for k in range(first, stop))
        if r == 0 and zone not in CORNER_ZONES:
            lo = 0.0
        if r == len(runs) - 1 and frame.length - hi <= secondary:
            hi = frame.length
        lo = max(lo, 0.0, cuts[r - 1] if r else 0.0)
        hi = min(hi, frame.length, cuts[r] if r < len(cuts) else frame.length)
        out.append((zone, lo, hi))
    return out


def _merged(zones: list[ZoneRect]) -> list[ZoneRect]:
    """Join rects of one zone that sit directly above one another with the same width."""
    out: list[ZoneRect] = []
    for z in sorted(zones, key=lambda z: (z.zone, z.rect.x, z.rect.x2, z.rect.y)):
        prev = out[-1] if out else None
        if (
            prev is not None
            and prev.zone == z.zone
            and abs(prev.rect.x - z.rect.x) <= TOL
            and abs(prev.rect.x2 - z.rect.x2) <= TOL
            and abs(prev.rect.y2 - z.rect.y) <= TOL
        ):
            r = prev.rect
            out[-1] = ZoneRect(z.zone, Rect(r.x, r.y, r.w, z.rect.y2 - r.y))
        else:
            out.append(z)
    return sorted(out, key=lambda z: (z.rect.y, z.rect.x))


def _enforce(result: LayoutResult, rules: LayoutRules, issues: list[Issue], first: Config) -> None:
    """Drop any unit that breaks a hard rule, lowest priority first (a guard, not a strategy).

    ``issues`` are the plan's issues as found. A broken aisle or zone leaves no unit to blame:
    the plan then falls back to the bare main aisle of ``first``, which is always valid."""
    dropped: list[LayoutItem] = []
    while issues:
        culprits = {uid for issue in issues for uid in issue.uids}
        involved = [p for p in result.placements if p.item.uid in culprits]
        if not involved:
            break
        worst = min(involved, key=lambda p: (p.item.priority, p.item.uid))
        result.placements = [p for p in result.placements if p is not worst]
        dropped.append(worst.item)
        issues = find_issues(result, rules)
    if issues:
        dropped += [p.item for p in result.placements]
        result.placements, result.zones, result.aisles = [], [], list(first.main)
    if dropped:
        result.unplaced = sorted([*result.unplaced, *dropped], key=lambda it: (-it.priority, it.uid))
        result.warnings.append(
            f"{len(dropped)} unit{'s' if len(dropped) > 1 else ''} removed by the final "
            "clearance check."
        )


def _notes(outcome: Outcome, narrow: bool, result: LayoutResult) -> list[str]:
    """Where the main aisle runs, when that is not straight up the middle."""
    config = outcome.config
    notes: list[str] = []
    back = next((s for s in outcome.stacks if isinstance(s, RingBack)), None)
    if back is not None and back.exit is not None and result.placements:
        side = "left" if back.exit.x <= TOL else "right"
        notes.append(
            f"The main aisle reaches the back wall in the back {side} corner, which leaves the "
            "rest of the back wall for a full row of equipment."
        )
    if len(config.main) > 1 and result.placements:
        side = "left" if config.main[0].x <= TOL else "right"
        if narrow:
            notes.append(
                f"The floor is too narrow to split around a central aisle, so the main aisle "
                f"runs along the {side} wall and a cross aisle joins it to the entrance."
            )
        else:
            notes.append(
                f"The main aisle runs along the {side} wall, joined to the entrance by a cross "
                "aisle, which fits more equipment on this floor."
            )
    return notes


def _shortened(result: LayoutResult) -> list[str]:
    """Flexible-length runs laid shorter than catalog length, which changes what to order."""
    shortened: dict[str, float] = {}
    for p in result.placements:
        if not p.item.flexible_length:
            continue
        length = p.rect.h if p.rotation in (0, 180) else p.rect.w
        if length < p.item.length_in - 1.0:
            shortened[p.item.name] = min(shortened.get(p.item.name, length), length)
    return [
        f"{name} shortened to {length / 12:.0f} ft to fit the floor."
        for name, length in sorted(shortened.items())
    ]
