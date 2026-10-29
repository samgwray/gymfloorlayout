"""Stack rows of equipment into the halves of the training floor.

A half is the part of the floor on one side of the main aisle. Its back wall takes one row of
wall units (racks, rigs, crossovers) facing the room, from the zones nearest the back first;
wall units that find no room there join their own zone's rows, so they stay in zone order.
Every other row is built from the zones in ``rules.zone_order`` and goes to whichever half is
currently shallower, so both halves fill front to back together and the zones read in order
from the entrance. Rows sit as close as clearances, approach zones and walkways allow; once a
half is nearly full, a unit too deep for what is left may turn (a machine sideways is often
shallower) or wait for the other half.

Three modes trade tidiness for density:

* ``tidy``: one zone per row; a row closes when its row group changes once it is half full;
* ``dense``: one zone per row; a row keeps taking shorter units to fill its length;
* ``flow``: like dense, but the next zone continues in the same row. Shallow floors hold only a
  few rows, and giving every zone rows of its own would leave most of their length empty.

Every depth check goes through ``_room_for``, which is also how flexible units (turf lanes)
running across a row get their length, so a length the stacker picks is one it accepts.

A half may also end at an aisle rather than the back wall (``back_allow``): ring layouts
(``ring``) stack island rows in such halves, between a band along the side wall and the spine.
The steps of ``stack_all`` (``back_wall_rows``, ``zone_queues``, ``fill_rows``, ``next_row``)
are what ring layouts reuse.
"""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Literal

from gymplanner.catalog.schema import ZoneId
from gymplanner.layout.geometry import TOL, Direction
from gymplanner.layout.rows import (
    Candidate,
    Choice,
    FlexOption,
    Pose,
    Row,
    RowBuilder,
    RowFrame,
    RowKind,
    Slot,
    fitting,
    flexible_options,
    make_pose,
    measure,
    pose_candidates,
    rotation_order,
)
from gymplanner.layout.types import LayoutItem, LayoutRules, Rect, Rotation

Mode = Literal["tidy", "dense", "flow"]
RingMode = Literal["", "open", "core"]
FACING_ZONES: frozenset[ZoneId] = frozenset({"cardio"})
"""Zones whose units all face the entrance, in rows that open onto the walkway behind."""
CORNER_ZONES: frozenset[ZoneId] = frozenset({"stretching"})
"""Zones whose runs hug the side wall instead of the main aisle (a quiet corner)."""
TIDY_FILL = 0.5
"""In tidy mode a row closes when the row group changes, once it is at least this full."""

KindKey = tuple[object, ...]
Options = tuple[tuple[Choice, Row, float], ...]
"""Orientations of a unit, best first, each with the row it would form on its own and an upper
bound on the depth that row needs with its gaps (see ``_lone``)."""


@dataclass(frozen=True)
class Half:
    index: int
    x0: float
    x1: float
    y0: float
    y1: float
    front_allow: float
    """Depth of the cross aisle directly in front of the half (0 when it starts at a wall)."""
    frame: RowFrame
    back_allow: float = 0.0
    """Depth of an aisle directly behind the half (0 when it ends at the back wall)."""

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def depth(self) -> float:
        return self.y1 - self.y0

    @property
    def walled(self) -> bool:
        """Whether the half ends at the back wall, which takes a row of wall units."""
        return self.back_allow <= 0


@dataclass(frozen=True)
class Config:
    main: tuple[Rect, ...]
    """The main aisle: the spine first, then the cross aisle to the entrance if there is one."""
    halves: tuple[Half, ...]
    mode: Mode
    """How rows take units (see the module docstring)."""
    ring: RingMode = ""
    """Whether units also line the side walls (``ring``), and how the floor beside them is
    used: kept open as circulation (``open``) or given island rows (``core``)."""
    across: bool = False
    """In a ring with a half on each side of the spine: one back wall row across the whole
    width, the main aisle reaching the back wall through a corner (see ``ring``)."""
    facing: bool = False
    """In an ``open`` ring: a row of free-standing units in front of the back wall row, facing
    it and sharing its walkway (benches in front of a dumbbell run)."""


@dataclass
class Stack:
    """A half filled from both ends: zone rows from the front, one wall row at the back."""

    half: Half
    rows: list[Row] = field(default_factory=list)
    """Rows from the front, in zone order."""
    back: list[Row] = field(default_factory=list)
    """The row against the back wall, if any."""
    front_used: float = 0.0
    """Front edge of the half to the back of its last front row, at minimum gaps."""
    back_used: float = 0.0
    """Back wall to the front of the back wall row, at minimum gaps."""

    @property
    def used(self) -> float:
        return self.front_used + self.back_used

    def ordered(self) -> list[Row]:
        return [*self.rows, *reversed(self.back)]


def group_of(item: LayoutItem) -> str:
    return item.row_group or item.equipment_id


def kind_key(item: LayoutItem) -> KindKey:
    """Everything that decides where a unit can go: units with equal keys are interchangeable."""
    c = item.clearance
    min_length = (item.min_length_in or 0.0) if item.flexible_length else 0.0
    return (
        item.zone,
        group_of(item),
        item.length_in,
        item.width_in,
        c.front_in,
        c.back_in,
        c.left_in,
        c.right_in,
        item.aisle_side,
        item.against_wall,
        item.flexible_length,
        min_length,
        item.pairs_with,
    )


class Context:
    """Rules plus caches shared by every stacking attempt of one plan."""

    def __init__(self, rules: LayoutRules) -> None:
        self.rules = rules
        self.secondary = rules.secondary_aisle_in
        self.spine = max(rules.main_aisle_in, rules.secondary_aisle_in)
        """Main aisle width: never narrower than the walkways that open onto it."""
        self.alone: dict[tuple[bool, KindKey], bool] = {}
        """Whether a kind fits an otherwise empty floor, with or without wall bands (see
        ``search.placeable``)."""
        self._kinds: dict[int, KindKey] = {}
        self._interned: dict[KindKey, KindKey] = {}
        self._sort: dict[int, tuple[object, ...]] = {}
        self._options: dict[tuple[bool, bool, RowFrame, tuple[Direction, ...]], dict[KindKey, Options]] = {}
        self._candidates: dict[tuple[object, ...], tuple[Candidate, ...]] = {}
        """Orientations of each kind with what they need (``rows.pose_candidates``), shared by
        halves of every size, such as the island halves made afresh for every attempt."""
        self._flex: dict[tuple[object, ...], tuple[tuple[FlexOption, Row, float], ...]] = {}
        self._poses: dict[tuple[object, ...], Pose] = {}
        self._lones: dict[tuple[object, ...], tuple[Choice, Row, float]] = {}
        self.bands: dict[tuple[object, ...], tuple[Choice, ...]] = {}
        """Orientations of each kind in a wall band (see ``ring``)."""

    def kind(self, item: LayoutItem) -> KindKey:
        """The unit's kind key, one shared tuple per kind so keys compare by identity."""
        key = self._kinds.get(id(item))
        if key is None:
            key = kind_key(item)
            key = self._kinds[id(item)] = self._interned.setdefault(key, key)
        return key

    def options_table(
        self, half: Half, edges: tuple[Direction, ...], every: bool = False, wall: bool = False
    ) -> dict[KindKey, Options]:
        """Orientations of each kind in rows of ``half`` opening onto ``edges`` (filled in by
        ``options``). Keyed by the half's frame, which is all they depend on: island halves are
        made afresh for every attempt."""
        key = (every, wall, half.frame, edges)
        table = self._options.get(key)
        if table is None:
            table = self._options[key] = {}
        return table

    def sort_key(self, item: LayoutItem) -> tuple[object, ...]:
        """Order within a row group: deepest first; it ignores priority, so that which units
        of a kind are in the set never changes the geometry."""
        key = self._sort.get(id(item))
        if key is None:
            rank = (-item.length_in, -item.width_in, self.kind(item), item.equipment_id, item.uid)
            key = self._sort[id(item)] = rank
        return key

    def zone_sequence(self, zones: set[ZoneId]) -> list[ZoneId]:
        ordered = [z for z in self.rules.zone_order if z in zones]
        return ordered + sorted(zones - set(ordered))

    def options(
        self,
        item: LayoutItem,
        half: Half,
        edges: tuple[Direction, ...],
        every: bool = False,
        wall: bool = False,
    ) -> Options:
        """Orientations of a fixed-length unit in rows of ``half`` opening onto ``edges``, best
        first, each with the row it would form on its own: no row holding it needs less depth.

        Only the best one unless ``every``: the others matter once a half is nearly full. In a
        back wall row (``wall``) a unit only stands facing the room, its back to the wall.
        """
        table = self.options_table(half, edges, every, wall)
        key = self.kind(item)
        found = table.get(key)
        if found is None:
            frame = half.frame
            shape = (key, edges, wall, frame.inward, frame.inner_allow, frame.outer_allow)
            candidates = self._candidates.get(shape)
            if candidates is None:
                rotations: tuple[Rotation, ...] = (
                    (0,) if wall else rotation_order(item, edges[0], item.zone in FACING_ZONES)
                )
                candidates = pose_candidates(item, frame, edges, rotations, self.pose)
                self._candidates[shape] = candidates
            choices = fitting(candidates, frame, 4 if every else 1)
            found = table[key] = tuple(self.lone(item, c, edges[0]) for c in choices)
        return found

    def choice(self, item: LayoutItem, half: Half, edges: tuple[Direction, ...]) -> Choice | None:
        """The preferred orientation of a fixed-length unit, if it fits the half at all."""
        options = self.options(item, half, edges)
        return options[0][0] if options else None

    def flex_options(
        self, item: LayoutItem, half: Half, edges: tuple[Direction, ...], face: bool
    ) -> tuple[tuple[FlexOption, Row, float], ...]:
        """Orientations of a flexible unit, each with the row it would form on its own and the
        bound on the depth it needs (as in ``Options``)."""
        key = (self.kind(item), half.frame, edges, face)
        found = self._flex.get(key)
        if found is None:
            rotations = rotation_order(item, edges[0], face)
            options = flexible_options(item, half.frame, edges, rotations, self.pose)
            found = tuple((opt, *self.lone(item, opt.choice, edges[0])[1:]) for opt in options)
            self._flex[key] = found
        return found

    def lone(
        self, item: LayoutItem, choice: Choice, walk_edge: Direction
    ) -> tuple[Choice, Row, float]:
        """``_lone`` for a unit, shared by every half (it does not depend on the half)."""
        pose = choice.pose
        key = (self.kind(item), pose.rotation, pose.length, choice.mode, walk_edge)
        found = self._lones.get(key)
        if found is None:
            found = self._lones[key] = _lone(item, choice, walk_edge, self.secondary)
        return found

    def pose(self, item: LayoutItem, rotation: Rotation, length: float) -> Pose:
        key = (self.kind(item), rotation, round(length, 6))
        found = self._poses.get(key)
        if found is None:
            found = self._poses[key] = make_pose(item, rotation, length, self.secondary)
        return found


def _lone(
    item: LayoutItem, choice: Choice, walk_edge: Direction, secondary: float
) -> tuple[Choice, Row, float]:
    """The row a unit would form on its own, and an upper bound on the depth that row needs
    with its gaps: its strip plus, on each side, the larger of its reach and a walkway
    (``_slack`` takes off the neighbours' share). Clearances and walkways do not depend on the
    unit's length, so the row serves flexible units at any length."""
    mode = choice.mode if choice.mode != "either" else "in"
    row = Row(kind="alternating", walk_edge=walk_edge, slots=[Slot(item, choice.pose, mode, 0.0)], end=0.0)
    measure(row)
    up = max(row.reach_n, row.appr_n, secondary)
    down = max(row.reach_s, row.appr_s, secondary)
    return choice, row, choice.pose.h + up + down


@dataclass
class Bin:
    """Consecutive queued units of one kind: interchangeable, so a row takes them as a block."""

    key: KindKey
    units: list[LayoutItem]
    area: float
    """Envelope area of one unit."""
    narrow: float
    """Narrowest side a unit's footprint can have (a flexible one at its minimum length)."""


def stack_all(ctx: Context, config: Config, items: Sequence[LayoutItem]) -> list[Stack] | None:
    """Rows for every unit, or None when something does not fit."""
    stacks = [Stack(h) for h in config.halves]
    if not items:
        return stacks
    if not stacks:
        return None
    floor = facing_partners(ctx, stacks, back_wall_rows(ctx, stacks, items))
    queues = zone_queues(ctx, floor, config.mode == "flow")
    width = sum(h.width for h in config.halves)
    pending = sum(b.area * len(b.units) for queue in queues for b in queue)
    for queue in queues:
        left = fill_rows(ctx, stacks, queue, config.mode, pending, width)
        if left is None:
            return None
        pending = left
    for stack in stacks:
        _face_last_row_forward(ctx, stack)
    return stacks


def back_wall_rows(
    ctx: Context, stacks: list[Stack], items: Sequence[LayoutItem], longest_first: bool = False
) -> list[LayoutItem]:
    """Give each walled half's back wall a row of wall units and return the units left for the
    floor (wall units that found no room there included).

    The zones nearest the back go first, or with ``longest_first`` the widest units (when the
    side walls take wall units too, the back wall is the only place for a long dumbbell run)."""
    wall = [it for it in items if it.against_wall]
    if not wall:
        return list(items)
    ordered = _in_zone_order(ctx, wall, reverse=True)
    if longest_first:
        ordered.sort(key=lambda it: (-it.width_in, -it.length_in, ctx.sort_key(it)))
    leftover = _back_wall(ctx, stacks, _bins(ctx, ordered))
    return [it for it in items if not it.against_wall] + leftover


def facing_partners(
    ctx: Context, stacks: list[Stack], items: Sequence[LayoutItem], across: Stack | None = None
) -> list[LayoutItem]:
    """Put the units used with a back wall run (benches with dumbbells, ``pairs_with``) in a
    row in front of it, facing it across its walkway, and return the units left for the floor.

    The run is each half's own back wall row, or ``across``, a back wall row across the whole
    width that the halves end in front of. Each half takes a share of the units by the length
    of the run behind it; what its row cannot hold stays with the floor's zone rows."""
    partners = [it for it in items if it.pairs_with]
    if not partners:
        return list(items)

    def lengths(row: Row) -> dict[str, float]:
        out: dict[str, float] = defaultdict(float)
        for slot in row.slots:
            out[group_of(slot.item)] += slot.pose.w
        return out

    if across is not None and across.back:
        behind = [stack for stack in stacks if stack.half.back_allow > 0]
        run = lengths(across.back[0])
        runs = [
            {g: length / len(behind) for g, length in run.items()} if stack in behind else {}
            for stack in stacks
        ]
    else:
        runs = [lengths(stack.back[0]) if stack.back else {} for stack in stacks]
    width = sum(stack.half.width for stack in stacks)
    taken: set[int] = set()
    for group in sorted({it.pairs_with for it in partners}):
        mine = [it for it in partners if it.pairs_with == group]
        total = sum(run.get(group, 0.0) for run in runs)
        start = 0
        for stack, run in zip(stacks, runs, strict=True):
            if run.get(group, 0.0) <= 0 or start >= len(mine):
                continue
            share = math.ceil(len(mine) * run[group] / total)
            queue = _bins(ctx, _grouped(ctx, mine[start : start + share]))
            pending = sum(b.area * len(b.units) for b in queue)
            offered = [u for b in queue for u in b.units]
            step = facing_back_row(ctx, stack, queue, pending, width)
            start += share
            if step is not None:
                left = {id(u) for b in step[0] for u in b.units}
                taken.update(id(u) for u in offered if id(u) not in left)
    return [it for it in items if id(it) not in taken]


def zone_queues(ctx: Context, items: Sequence[LayoutItem], flow: bool) -> list[list[Bin]]:
    """One queue per zone in zone order, row groups together; one queue overall for ``flow``."""
    queues = [_bins(ctx, _grouped(ctx, units)) for units in _by_zone(ctx, items)]
    return [[b for queue in queues for b in queue]] if flow else queues


def fill_rows(
    ctx: Context, stacks: list[Stack], queue: list[Bin], mode: Mode, pending: float, width: float
) -> float | None:
    """Stack rows from ``queue`` into whichever half is shallowest until the queue is empty.

    ``pending`` is the envelope area of every unit not yet placed and ``width`` the floor width
    it spreads over (see ``_build_row``). Returns the area still pending, or None when the
    next unit fits no half."""
    while queue:
        for stack in sorted(stacks, key=lambda s: (s.half.y0 + s.used, s.half.index)):
            step = next_row(ctx, stack, queue, mode, pending, width)
            if step is not None:
                queue, pending = step
                break
        else:
            return None
    return pending


def next_row(
    ctx: Context, stack: Stack, queue: list[Bin], mode: Mode, pending: float, width: float
) -> tuple[list[Bin], float] | None:
    """Add the next row from ``queue`` to the front of ``stack`` if one fits; the queue and
    pending area that remain."""
    built = _build_row(ctx, stack, queue, mode, (pending, width))
    if built is None or not _add_row(ctx, stack, built[0]):
        return None
    pending -= sum(queue[b].area * count for b, count in built[1].items())
    return take(queue, built[1]), pending


def facing_back_row(
    ctx: Context, stack: Stack, queue: list[Bin], pending: float, width: float
) -> tuple[list[Bin], float] | None:
    """Add a row in front of the stack's back rows (or the aisle behind its half) that opens
    onto the walkway there, if one fits: benches facing a dumbbell run share its walkway. The
    queue and pending area that remain."""
    built = _build_row(ctx, stack, queue, "dense", (pending, width), "alternating", "s")
    if built is None or not _add_row(ctx, stack, built[0], back=True):
        return None
    pending -= sum(queue[b].area * count for b, count in built[1].items())
    return take(queue, built[1]), pending


def take(queue: list[Bin], taken: dict[int, int]) -> list[Bin]:
    """The queue without the first ``taken[b]`` units of each bin ``b`` (bins are emptied in
    place: a queue is only ever used by the attempt that built it)."""
    for b, count in taken.items():
        del queue[b].units[:count]
    return [b for b in queue if b.units]


def _back_wall(ctx: Context, stacks: list[Stack], wall: list[Bin]) -> list[LayoutItem]:
    """Fill each half's back wall with one row of wall units; returns those left over."""
    remaining = wall
    for stack in stacks:
        if not remaining:
            break
        if not stack.half.walled:
            continue
        built = _build_row(ctx, stack, remaining, "dense", (0.0, 1.0), kind="wall")
        if built is None or not _add_row(ctx, stack, built[0], back=True):
            continue
        remaining = take(remaining, built[1])
    return [it for b in remaining for it in b.units]


def _bins(ctx: Context, units: list[LayoutItem]) -> list[Bin]:
    out: list[Bin] = []
    for unit in units:
        key = ctx.kind(unit)
        if out and out[-1].key is key:
            out[-1].units.append(unit)
        else:
            narrow = min(unit.width_in, _min_length(unit))
            out.append(Bin(key, [unit], _envelope_area(unit), narrow))
    return out


def _by_zone(ctx: Context, items: Sequence[LayoutItem]) -> list[list[LayoutItem]]:
    by_zone: dict[ZoneId, list[LayoutItem]] = defaultdict(list)
    for item in items:
        by_zone[item.zone].append(item)
    return [by_zone[z] for z in ctx.zone_sequence(set(by_zone))]


def _in_zone_order(ctx: Context, items: Sequence[LayoutItem], reverse: bool) -> list[LayoutItem]:
    zones = _by_zone(ctx, items)
    if reverse:
        zones.reverse()
    return [it for units in zones for it in _grouped(ctx, units)]


def _grouped(ctx: Context, items: list[LayoutItem]) -> list[LayoutItem]:
    """Row groups kept together, deepest units first so rows mix similar depths."""
    groups: dict[str, list[LayoutItem]] = defaultdict(list)
    for item in items:
        groups[group_of(item)].append(item)
    for members in groups.values():
        members.sort(key=ctx.sort_key)
    keys = sorted(groups, key=lambda g: (-groups[g][0].length_in, -groups[g][0].width_in, g))
    return [item for g in keys for item in groups[g]]


def _envelope_area(item: LayoutItem) -> float:
    c = item.clearance
    length = item.min_length_in if item.flexible_length and item.min_length_in else item.length_in
    return (length + c.front_in + c.back_in) * (item.width_in + c.left_in + c.right_in)


def stands_alone(ctx: Context, half: Half, item: LayoutItem) -> bool:
    """Whether a fixed-length unit's preferred orientation fits the first row of an empty half.

    A row configuration then places the unit on its own: the orientation already allows for
    the row's walkway and the unit's clearances, which is all an empty half asks of it (a wall
    unit that the back wall does not take joins such a row). False says nothing either way."""
    if item.flexible_length:
        return False
    kind: RowKind = "facing" if item.zone in FACING_ZONES else "alternating"
    edges, _ = _edges(Stack(half), kind)
    return bool(ctx.options(item, half, edges))


def _edges(stack: Stack, kind: RowKind) -> tuple[tuple[Direction, ...], Direction]:
    """Edges whose walkway the row's units may open onto, and the row's own walkway edge."""
    if kind == "facing":
        if not stack.rows and stack.half.front_allow > 0:
            return ("n", "s"), "n" # Behind a cross aisle, units reached from the front or the side open onto it, so only a row with rear-access machines needs a walkway behind it as well.
        return ("s", "n"), "s"
    if kind == "wall":
        return ("n",), "n"
    walk = _next_edge(stack)
    return (walk,), walk


def _next_edge(stack: Stack) -> Direction:
    """Alternate so each walkway serves the rows on both sides of it."""
    if not stack.rows:
        return "n" if stack.half.front_allow > 0 else "s"
    return "n" if stack.rows[-1].walk_s else "s"


def _build_row(
    ctx: Context,
    stack: Stack,
    queue: list[Bin],
    mode: Mode,
    pending: tuple[float, float],
    kind: RowKind | None = None,
    walk: Direction | None = None,
) -> tuple[Row, dict[int, int]] | None:
    """The next row for ``stack`` from the front of ``queue``, and how many units it took
    from each bin (always the bin's first ones).

    ``pending`` is the envelope area of the units not yet placed and the floor width it will
    spread over: a flexible unit running across the row leaves their share of the depth.
    ``walk`` fixes the edge the row opens onto (otherwise it follows from the rows before).
    """
    half = stack.half
    length = half.frame.length
    if kind is None:
        kind = "facing" if queue[0].units[0].zone in FACING_ZONES else "alternating"
    edges, walk_edge = ((walk,), walk) if walk is not None else _edges(stack, kind)
    wall = kind == "wall"
    table = ctx.options_table(half, edges, wall=wall)
    slack = _slack(ctx, stack)
    builder = RowBuilder(half.frame, walk_edge)
    picked: dict[int, int] = {}
    pending_area, width = pending
    for b, block in enumerate(queue):
        first = block.units[0]
        if (
            mode == "tidy"
            and builder.slots
            and group_of(first) != group_of(builder.slots[-1].item)
            and builder.fill >= TIDY_FILL
        ):
            break
        if builder.end + block.narrow > length + TOL:
            continue # too wide for what is left of the row however it turns
        fixed: Choice | None = None
        if not first.flexible_length:
            best = table.get(block.key) or ctx.options(first, half, edges, wall=wall)
            if not best:
                continue # cannot stand in this half; another half may take it
            fixed = _deep_enough(ctx, stack, best, slack)
            if ( # Turned another way the unit may be shallower, but never below its smaller side.
                fixed is None
                and not wall
                and min(first.width_in, first.length_in) <= half.depth - stack.used
            ):
                every = ctx.options(first, half, edges, every=True)
                fixed = _deep_enough(ctx, stack, every, slack)
            if fixed is None:
                continue # cannot stand in what is left of this half; another may take it
        count, full = 0, False
        for unit in block.units:
            choice = fixed
            if choice is None:
                reserve = max(0.0, pending_area - block.area) / width
                choice = _flexible_choice(ctx, stack, builder, unit, edges, mode != "tidy", reserve, slack)
                if choice is None:
                    break # no room left for this kind in this row
            if builder.end + choice.pose.w > length + TOL or not builder.try_add(unit, choice): # A footprint wider than what is left of the row cannot fit: skip the full attempt.
                full = True
                break
            count += 1
            pending_area -= block.area
        if count:
            picked[b] = count
        if full and mode == "tidy": # Tidy rows end at the first unit that does not fit; dense rows go on looking for shorter units to fill the rest of the row.
            break
    if not picked:
        return None
    return builder.finish(kind), picked


def narrowest_after(queue: Sequence[Bin]) -> list[float]:
    """For each bin, the narrowest footprint side among its units and those of the bins after
    it (a flexible unit at its minimum length): a row or band with less room left takes none of
    them, however they turn."""
    out = [math.inf] * (len(queue) + 1)
    for b in range(len(queue) - 1, -1, -1):
        out[b] = min(out[b + 1], queue[b].narrow)
    return out


def _deep_enough(ctx: Context, stack: Stack, options: Options, slack: float) -> Choice | None:
    """The best orientation the depth left in the half still holds."""
    for choice, lone, need in options:
        if need <= slack + TOL or choice.pose.h <= _room_for(ctx, stack, lone) + TOL:
            return choice
    return None


def _slack(ctx: Context, stack: Stack) -> float:
    """Depth left in a half once the neighbouring rows' largest reach or walkway is taken off
    on both sides: a row whose ``_lone`` bound fits it certainly fits, without the exact
    check (``_room_for``), which matters when hundreds of kinds are tried row after row."""
    sec = ctx.secondary
    ahead = max(stack.rows[-1].reach_s, stack.rows[-1].appr_s, sec) if stack.rows else 0.0
    behind = max(stack.back[-1].reach_n, stack.back[-1].appr_n, sec) if stack.back else 0.0
    return stack.half.depth - stack.used - ahead - behind


def _min_length(item: LayoutItem) -> float:
    """Shortest length a unit can take: a flexible unit's minimum, otherwise its length."""
    if not item.flexible_length:
        return item.length_in
    return min(item.length_in, item.min_length_in or item.length_in)


def _flexible_choice(
    ctx: Context,
    stack: Stack,
    builder: RowBuilder,
    item: LayoutItem,
    edges: tuple[Direction, ...],
    shorten_to_row: bool,
    reserve: float,
    slack: float,
) -> Choice | None:
    """The orientation that gives a flexible unit the most length, and that length.

    Along the row it may use the empty half's width (or, when ``shorten_to_row``, whatever is
    left of the row). Across the row it may use the depth still free in the half, less
    ``reserve`` for the units still to come, but never less than its minimum length.
    """
    nominal, min_length = item.length_in, _min_length(item)
    best: tuple[float, FlexOption] | None = None
    for option, lone, need in ctx.flex_options(item, stack.half, edges, item.zone in FACING_ZONES):
        if option.along_row:
            if need > slack + TOL and option.choice.pose.h > _room_for(ctx, stack, lone) + TOL:
                continue
            room = option.max_length
            if shorten_to_row and builder.slots:
                room = min(room, builder.room(option.choice))
            length = room
        else:
            room = min(option.max_length, _room_for(ctx, stack, lone))
            length = min(room, max(min_length, room - reserve))
        if room < min_length - TOL:
            continue
        if best is None or length > best[0] + TOL:
            best = (length, option)
    if best is None:
        return None
    length, option = best
    pose = option.choice.pose
    if length < nominal - TOL:
        pose = ctx.pose(item, pose.rotation, length)
    return Choice(pose, option.choice.mode)


def _room_for(ctx: Context, stack: Stack, row: Row) -> float:
    """Deepest strip ``row`` may have as the stack's next row, front or back: the half's depth
    less what is in use and the gaps the row needs on either side."""
    sec, rows, back = ctx.secondary, stack.rows, stack.back
    ahead = row_gap(rows[-1], row, sec)[0] if rows else front_gap(row, stack.half, sec)[0]
    behind = row_gap(row, back[-1], sec)[0] if back else trailing(row, stack.half, sec)[0]
    return stack.half.depth - stack.used - ahead - behind


def _add_row(ctx: Context, stack: Stack, row: Row, back: bool = False) -> bool:
    """Commit a row to the front (or the back wall) of a half if the depth allows."""
    if row.depth > _room_for(ctx, stack, row) + TOL and not _shrink(ctx, stack, row):
        return False
    sec = ctx.secondary
    if back:
        behind = (
            row_gap(row, stack.back[-1], sec)[0]
            if stack.back
            else trailing(row, stack.half, sec)[0]
        )
        stack.back.append(row)
        stack.back_used += behind + row.depth
    else:
        rows = stack.rows
        ahead = row_gap(rows[-1], row, sec)[0] if rows else front_gap(row, stack.half, sec)[0]
        rows.append(row)
        stack.front_used += ahead + row.depth
    return True


def _shrink(ctx: Context, stack: Stack, row: Row) -> bool:
    """Shorten the flexible units running across a row until it fits the depth left.

    Their lengths were set for a row of their own; neighbours with larger clearances can need a
    wider gap, and shortening can change the gaps again, hence the few rounds.
    """
    for _ in range(4):
        target = _room_for(ctx, stack, row)
        if row.depth <= target + TOL:
            return True
        changed = False
        for slot in row.slots:
            item = slot.item
            if not item.flexible_length or slot.pose.rotation not in (0, 180):
                continue
            length = max(_min_length(item), target)
            if length < slot.pose.h - TOL:
                slot.pose = ctx.pose(item, slot.pose.rotation, length)
                changed = True
        if not changed:
            return False
        measure(row)
    return row.depth <= _room_for(ctx, stack, row) + TOL


def _face_last_row_forward(ctx: Context, stack: Stack) -> None:
    """Turn a half's last row to face the room with its back to the back wall, if it fits.

    A half's only row stays where it is, so the front of the floor is not left empty."""
    if len(stack.rows) < 2 or stack.back or not stack.half.walled:
        return
    last = stack.rows[-1]
    if last.kind != "alternating" or last.walk_edge != "s":
        return
    if any(it.flexible_length for it in last.items):
        return
    builder = RowBuilder(stack.half.frame, "n")
    for item in last.items:
        choice = ctx.choice(item, stack.half, ("n",))
        if choice is None or not builder.try_add(item, choice):
            return
    flipped = builder.finish("alternating")
    stack.rows.pop()
    stack.front_used = _front_extent(ctx, stack)
    if not _add_row(ctx, stack, flipped):
        _add_row(ctx, stack, last)


def _front_extent(ctx: Context, stack: Stack) -> float:
    used = 0.0
    for i, row in enumerate(stack.rows):
        if i:
            used += row_gap(stack.rows[i - 1], row, ctx.secondary)[0]
        else:
            used += front_gap(row, stack.half, ctx.secondary)[0]
        used += row.depth
    return used


def row_gap(front: Row, back: Row, secondary: float) -> tuple[float, bool]:
    """Gap between consecutive rows and whether it is a walkway."""
    gap = max(0.0, front.reach_s, back.reach_n)
    walk = front.walk_s or back.walk_n
    if walk:
        gap = max(gap, secondary)
        if front.walk_s:
            gap = max(gap, front.appr_s)
        if back.walk_n:
            gap = max(gap, back.appr_n)
    return gap, walk


def front_gap(row: Row, half: Half, secondary: float) -> tuple[float, bool]:
    """Gap before a half's first row, and whether it needs its own walkway there."""
    gap = max(0.0, row.reach_n - half.front_allow)
    if not row.walk_n:
        return gap, False
    if half.front_allow > 0: # the cross aisle in front serves as the walkway
        return max(gap, row.appr_n - half.front_allow), False
    return max(gap, secondary, row.appr_n), True


def trailing(row: Row, half: Half, secondary: float) -> tuple[float, bool]:
    """Depth needed behind a half's last row, and whether it needs its own walkway there."""
    gap = max(0.0, row.reach_s - half.back_allow)
    if not row.walk_s:
        return gap, False
    if half.back_allow > 0: # the aisle behind the half serves as the walkway
        return max(gap, row.appr_s - half.back_allow), False
    return max(gap, secondary, row.appr_s), True
