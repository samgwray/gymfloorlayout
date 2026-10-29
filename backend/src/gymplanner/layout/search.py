"""Choose which units to place: all of them if they fit, otherwise the most valuable that do.

Configurations come in families (rows, rings: ``Config.ring``), and each family is searched on
its own. Within a family, units are considered from the highest priority down, and a unit is
left out only when it does not fit on top of the higher-priority units already kept. The units
a family leaves out are therefore the least valuable ones that do not fit, never a valuable
unit crowded out by cheaper ones, and no unit left out would still fit beside the plan as
returned. The family whose outcome keeps the most priority in total wins, then the one keeping
the most units, then the one the caller's ``rank`` prefers (rows on a tie): a ring that holds
one more top-priority unit but cannot take the rest does not beat rows that hold more.

Stacking is a heuristic, so feasibility is not strictly monotone in the set of units; the search
is fast because it mostly is. In each family:

1. try every unit at once (the common case on a roomy floor; skipped when the footprints alone
   would crowd the floor). Once one family holds every unit the others are only tried this way,
   for the caller to rank;
2. search for the longest priority-ordered prefix any configuration places, which picks the
   configuration (the longest prefix keeps the most valuable units);
3. add the remaining units in priority order, in galloping runs. A unit that does not fit
   the configuration moves the plan to another configuration of the family that holds it with
   everything kept so far, if there is one; otherwise it is skipped, and so are the rest of its
   kind;
4. retry one unit of every kind still left out, in the chosen configuration, in any other of
   the family that can hold the kept units and, once none of those takes one, in the rest of
   the family, until none fits. This makes the result maximal even where stacking is not
   monotone.

Units of one kind (``stacking.kind_key``) are interchangeable, which bounds steps 3 and 4 by
the number of kinds rather than units. Both share a budget of work, one per family, so that a
stress case with hundreds of distinct kinds left out still returns promptly and one family's
search never starves the other's.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from gymplanner.layout.geometry import TOL
from gymplanner.layout.ring import arrange
from gymplanner.layout.stacking import Config, Context, KindKey, Stack, stands_alone
from gymplanner.layout.types import LayoutItem

EXTRA_WORK = 7_500
"""Work steps 3 and 4 may spend together in one family, counted per attempt as its units plus
its kinds (rows take the queue a kind at a time, so hundreds of distinct kinds cost about twice
what as many units of a few kinds do): roughly 25 ms. Realistic plans need a few hundred, 9 in
10 under 2,000, and only the most overfull large floors run out; the search then keeps what it
has placed so far."""
ATTEMPT_COST = 4
"""Fixed share of the budget per stacking attempt, for the work that does not scale with
the number of units."""
RING_COST = 2
"""Budget a ring attempt spends per unit: besides rows it lines the walls and stacks islands
in halves made afresh for every attempt, about twice the work, so both families' searches
take about the same time."""

ALL_FIT_SHARE = 0.5
"""Step 1 is skipped when the footprints alone would cover more than this share of the floor
outside the main aisle: clearances and walkways leave far less room (plans that hold every unit
stay under 0.35), and on an overfull floor a failed attempt with every unit costs as much as a
whole plan. Steps 2 and 3 still reach every unit if they do fit."""

Rank = Callable[["Outcome"], tuple[float, ...]]


@dataclass(frozen=True)
class Outcome:
    config: Config
    stacks: list[Stack]
    kept: tuple[LayoutItem, ...]

    @property
    def value(self) -> float:
        """Total priority kept, independent of the order the units were kept in."""
        return math.fsum(unit.priority for unit in self.kept)


class _Spent(Exception):
    """The search budget ran out."""


class _Budget:
    def __init__(self, ctx: Context, units: int) -> None:
        self.ctx = ctx
        self.left = units

    def stack(self, config: Config, items: Sequence[LayoutItem]) -> list[Stack] | None:
        kinds = len({id(self.ctx.kind(unit)) for unit in items})
        cost = (len(items) + kinds) * (RING_COST if config.ring else 1) + ATTEMPT_COST
        if cost > self.left:
            raise _Spent
        self.left -= cost
        return arrange(self.ctx, config, items)


def families(configs: Sequence[Config]) -> list[list[Config]]:
    """The configurations by family, rows first, each in the order given."""
    rows = [c for c in configs if not c.ring]
    rings = [c for c in configs if c.ring]
    return [family for family in (rows, rings) if family]


def placeable(
    ctx: Context, configs: Sequence[Config], items: Sequence[LayoutItem]
) -> list[LayoutItem]:
    """Units that some configuration can place on an otherwise empty floor."""
    layouts: list[Config] = [] # Modes only differ in how units share rows, so one mode per aisle layout settles a unit on its own (ring configurations keep theirs: islands fit what a band does not).
    for config in configs:
        if all(
            (config.main, config.halves, config.ring, config.across, config.facing)
            != (c.main, c.halves, c.ring, c.across, c.facing)
            for c in layouts
        ):
            layouts.append(config)
    ring = any(c.ring for c in configs)
    out: list[LayoutItem] = []
    for item in items:
        key = (ring, ctx.kind(item))
        if key not in ctx.alone:
            ctx.alone[key] = _fits_some_half(item, layouts) and (
                any(stands_alone(ctx, h, item) for c in layouts if not c.ring for h in c.halves)
                or any(arrange(ctx, config, [item]) is not None for config in layouts)
            )
        if ctx.alone[key]:
            out.append(item)
    return out


def _fits_some_half(item: LayoutItem, layouts: Sequence[Config]) -> bool:
    """Whether the bare footprint fits some half in some orientation (a quick necessary test)."""
    if item.length_in <= 0 or item.width_in <= 0:
        return False
    length = min(item.length_in, item.min_length_in or item.length_in)
    if not item.flexible_length:
        length = item.length_in
    return any(
        (item.width_in <= h.width and length <= h.depth)
        or (length <= h.width and item.width_in <= h.depth)
        for config in layouts
        for h in config.halves
    )


def search(
    ctx: Context,
    configs: Sequence[Config],
    order: Sequence[LayoutItem],
    rank: Rank | None = None,
) -> Outcome:
    """The configuration and rows for the units to keep (``order`` is by priority, highest
    first); a unit that no configuration places on its own is left out.

    Every family is searched on its own and the best outcome wins: the most priority kept, then
    the most units, then ``rank`` (the first family on a tie)."""
    units = placeable(ctx, configs, order)
    best: Outcome | None = None
    best_key: tuple[float, ...] = ()
    for family in families(configs):
        if best is not None and len(best.kept) == len(units):
            found = _all_fit(ctx, family, units) # Nothing can beat a plan that holds every unit; a family that holds them all too only competes on ``rank``.
        else:
            found = _search_family(ctx, family, units)
        if found is None:
            continue
        key = (found.value, len(found.kept), *(rank(found) if rank is not None else ()))
        if best is None or key > best_key:
            best, best_key = found, key
    assert best is not None, "search needs at least one configuration"
    return best


def _search_family(ctx: Context, configs: Sequence[Config], order: Sequence[LayoutItem]) -> Outcome:
    """Steps 1 to 4 within one family of configurations."""
    limit = _area_limit(configs, order)
    if _area_limit(configs, order, ALL_FIT_SHARE) == len(order):
        found = _all_fit(ctx, configs, order)
        if found is not None:
            return found
    outcome, live = _longest_prefix(ctx, configs, order[: limit + 1])
    budget = _Budget(ctx, EXTRA_WORK)
    rest = order[len(outcome.kept) :]
    if rest:
        outcome = _extend(ctx, live, outcome, rest, {ctx.kind(rest[0])}, budget) # The first unit past the prefix just failed in this configuration.
    return _fill(ctx, configs, outcome, order, budget)


def _all_fit(
    ctx: Context, configs: Sequence[Config], order: Sequence[LayoutItem]
) -> Outcome | None:
    """The first configuration that holds every unit, if any."""
    for config in configs:
        stacks = arrange(ctx, config, order)
        if stacks is not None:
            return Outcome(config, stacks, tuple(order))
    return None


def _area_limit(configs: Sequence[Config], order: Sequence[LayoutItem], share: float = 1.0) -> int:
    """The longest prefix whose footprints could cover no more than ``share`` of the floor
    outside the aisles. Footprints never overlap, so no configuration places a longer one than
    the whole floor allows; on a floor asked to hold many times what it can, this spares the
    attempts that cannot succeed."""
    room = share * max(sum(h.width * h.depth for h in config.halves) for config in configs)
    total = 0.0
    for k, item in enumerate(order):
        length = min(item.length_in, item.min_length_in or item.length_in)
        total += item.width_in * (length if item.flexible_length else item.length_in)
        if total > room + TOL:
            return k
    return len(order)


def _longest_prefix(
    ctx: Context, configs: Sequence[Config], order: Sequence[LayoutItem]
) -> tuple[Outcome, list[Config]]:
    """Search for the longest prefix some configuration places, preferring earlier ones; the
    whole of ``order`` is known not to fit. Also returns the configurations still worth trying
    on top of that prefix.

    The configurations likely to hold the most go first (``_DENSEST_FIRST``): the first is
    bisected, and each later one is tried at the longest prefix so far (one unit past it when
    the configuration is less preferred than the one holding it) and, only when it holds that,
    on longer ones in doubling steps and then by bisection. A configuration that does no better
    so costs a single attempt. Feasibility is taken to be monotone here: it is a guess, and the
    later steps recover what it misses. For the same reason they leave out every configuration
    that failed a prefix the kept units contain.
    """
    best = Outcome(configs[0], arrange(ctx, configs[0], ()) or [], ())
    failed_at = [len(order)] * len(configs)
    rank = {id(c): i for i, c in enumerate(configs)}
    tried = sorted(range(len(configs)), key=lambda i: (_DENSEST_FIRST[_style(configs[i])], i))
    for n, i in enumerate(tried):
        config = configs[i]
        lo, hi = len(best.kept), len(order)
        step = 1 if n else 0
        if n and lo and i < rank[id(best.config)]: # a tie goes to the preferred one
            stacks = arrange(ctx, config, order[:lo])
            if stacks is None:
                failed_at[i] = lo
                continue
            best = Outcome(config, stacks, tuple(order[:lo]))
        while hi - lo > 1:
            mid = min(lo + step, hi - 1) if step else (lo + hi) // 2
            stacks = arrange(ctx, config, order[:mid])
            if stacks is None:
                hi = failed_at[i] = mid
                step = 0
            else:
                lo, best = mid, Outcome(config, stacks, tuple(order[:mid]))
                step *= 2
    lo = len(best.kept)
    live = [c for i, c in enumerate(configs) if failed_at[i] > lo or c is best.config]
    return best, live


_DENSEST_FIRST = {"flow": 0, "dense": 1, "tidy": 2, "core": 0, "facing": 1, "open": 2}
"""Order in which the prefix search tries configurations: rows sharing zones before rows of
one zone, untidy before tidy; islands before a facing row before open floor."""


def _style(config: Config) -> str:
    if not config.ring:
        return config.mode
    return "facing" if config.facing else config.ring


def _extend(
    ctx: Context,
    configs: Sequence[Config],
    outcome: Outcome,
    rest: Sequence[LayoutItem],
    failed: set[KindKey],
    budget: _Budget,
) -> Outcome:
    """Add ``rest`` in priority order, skipping units that fit no configuration on top of the
    units kept before them. Runs that fit are found by doubling their length, then bisecting
    the first failure."""
    config, stacks, kept = outcome.config, outcome.stacks, list(outcome.kept)
    start, good = 0, 0
    run: list[LayoutItem] = []
    try:
        while True:
            good, bad, n = 0, 0, 1
            run, where = _run(ctx, rest, start, n, failed)
            if not run:
                break
            while True:
                found = budget.stack(config, [*kept, *run[:n]])
                if found is None:
                    bad = n
                    break
                good, stacks = n, found
                run, where = _run(ctx, rest, start, 2 * n, failed)
                if len(run) == n:
                    break
                n = len(run)
            while bad - good > 1:
                mid = (good + bad) // 2
                found = budget.stack(config, [*kept, *run[:mid]])
                if found is None:
                    bad = mid
                else:
                    good, stacks = mid, found
            kept += run[:good]
            if not bad:
                break
            unit, start, good = run[good], where[good] + 1, 0
            moved = _move(configs, config, [*kept, unit], budget)
            if moved is None:
                failed.add(ctx.kind(unit))
            else:
                config, stacks = moved
                kept.append(unit)
    except _Spent:
        kept += run[:good] # the run that fitted before the budget ran out
    return Outcome(config, stacks, tuple(kept))


def _move(
    configs: Sequence[Config], current: Config, items: Sequence[LayoutItem], budget: _Budget
) -> tuple[Config, list[Stack]] | None:
    """Another configuration that holds ``items`` (which the current one does not), if any."""
    for config in configs:
        if config is not current:
            stacks = budget.stack(config, items)
            if stacks is not None:
                return config, stacks
    return None


def _run(
    ctx: Context, rest: Sequence[LayoutItem], start: int, n: int, failed: set[KindKey]
) -> tuple[list[LayoutItem], list[int]]:
    """The next ``n`` units of ``rest`` from ``start`` whose kind has not failed, and where
    each sits in ``rest``."""
    run: list[LayoutItem] = []
    where: list[int] = []
    for i in range(start, len(rest)):
        if len(run) == n:
            break
        if ctx.kind(rest[i]) not in failed:
            run.append(rest[i])
            where.append(i)
    return run, where


def _fill(
    ctx: Context,
    configs: Sequence[Config],
    outcome: Outcome,
    order: Sequence[LayoutItem],
    budget: _Budget,
) -> Outcome:
    """Retry one unit of each kind still left out until none fits, in every configuration of
    the family (``configs``)."""
    try:
        while True:
            grown = _grow(ctx, configs, outcome, order, budget)
            if grown is None:
                return outcome
            outcome = grown
    except _Spent:
        return outcome


def _grow(
    ctx: Context,
    configs: Sequence[Config],
    outcome: Outcome,
    order: Sequence[LayoutItem],
    budget: _Budget,
) -> Outcome | None:
    """The outcome with the most valuable left-out unit that fits on top of it, if any.

    Each unit is tried in the outcome's configuration, then in the others that hold the kept
    units (looked for only once a unit does not fit, which saves the budget). Only when none
    of those takes any unit are the remaining configurations tried: stacking is not monotone,
    so one that cannot hold the kept units on their own may still hold them with one more."""
    kept = {id(u) for u in outcome.kept}
    seen: set[KindKey] = set()
    left: list[LayoutItem] = []
    for unit in order:
        key = ctx.kind(unit)
        if id(unit) not in kept and key not in seen:
            seen.add(key)
            left.append(unit)
    others = [c for c in configs if c is not outcome.config]
    holding: list[Config] | None = None
    for unit in left:
        items = (*outcome.kept, unit)
        stacks = budget.stack(outcome.config, items)
        if stacks is not None:
            return Outcome(outcome.config, stacks, items)
        if holding is None:
            holding = [c for c in others if budget.stack(c, outcome.kept) is not None]
        for config in holding:
            stacks = budget.stack(config, items)
            if stacks is not None:
                return Outcome(config, stacks, items)
    rest = [c for c in others if all(c is not h for h in holding or ())]
    for unit in left:
        items = (*outcome.kept, unit)
        for config in rest:
            stacks = budget.stack(config, items)
            if stacks is not None:
                return Outcome(config, stacks, items)
    return None
