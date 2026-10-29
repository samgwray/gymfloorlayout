"""Why a plan stops where it does, in plain sentences.

A plan stops buying for one of a few reasons, and the notes it carries say which, from what the
plan can still buy rather than from what it looks like:

* ``floor``: something worth buying is affordable, but the layout has no room for it;
* ``budget``: something worth buying exists, but it costs more than is left;
* nothing is worth buying at any price, because the plan already serves nearly all of peak
  demand (``met``), because most of what it leaves unserved needs equipment the plan rules out
  (``ruled_out``), because each further unit would see little use at the peak (``use``: a gym
  with few members), or because what it would serve is small for its price (``returns``).
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Literal

import numpy as np

from gymplanner.catalog.loader import Catalog
from gymplanner.domain import Demand
from gymplanner.planning.fitting import Upgrade
from gymplanner.planning.wording import capitalized, feet_inches, in_sentence, list_of, people
from gymplanner.selection import Constraints, RouteTable, Selection
from gymplanner.selection.optimizer import MIN_UNIT_USE, additions, best_unit_gain

DEMAND_MET_SHARE = 0.9
"""Share of peak demand served (on any acceptable route) from which it counts as met."""
NAMED_SHARE = 0.01
"""A type ruled out of the plan is named in its note only when it is the first choice for at
least this share of peak demand: the rest are pieces few members would miss."""
NAMES_IN_NOTE = 3

Reason = Literal["floor", "budget", "met", "ruled_out", "use", "returns"]


@dataclass(frozen=True)
class Limit:
    reason: Reason
    next_piece: tuple[tuple[str, ...], float] | None = None
    """For ``budget``: the names of the next pieces worth buying together (one, or a bench with
    its dumbbells) and what they cost."""


@dataclass(frozen=True)
class RuledOut:
    """Equipment the plan cannot have, by cause (ids)."""

    excluded: bool
    """Whether the request excluded anything."""
    too_tall: Sequence[str]
    too_big: Sequence[str]


def plan_limit(
    catalog: Catalog,
    table: RouteTable,
    cons: Constraints,
    selection: Selection,
    upgrades: Sequence[Upgrade],
) -> Limit:
    """What stops the plan from buying more (see the module docstring). ``upgrades`` are the
    steps a bigger budget would add next, each one the layout places beside the plan."""
    worth = additions(table, cons, selection, np.inf)
    left = cons.budget_usd - selection.cost
    if any(move.cost <= left + 1e-6 for move in worth) or (worth and not upgrades): # The plan was grown with everything affordable it could place: what is left has no room.
        return Limit("floor")
    if worth:
        first = upgrades[0]
        types = sorted(first.added, key=lambda r: -cons.unit_cost[r])
        names = tuple(catalog.equipment_by_id[table.equipment_ids[r]].name for r in types)
        return Limit("budget", (names, first.cost))
    total = max(table.total_load, 1e-9)
    served = float(selection.evaluation.served[0])
    if served / total >= DEMAND_MET_SHARE:
        return Limit("met")
    if table.unroutable_load >= 0.5 * (total - served):
        return Limit("ruled_out")
    if best_unit_gain(table, cons, selection) < MIN_UNIT_USE:
        return Limit("use")
    return Limit("returns")


def _ruled_out_by(ruled_out: RuledOut) -> str:
    causes = [
        cause
        for cause, applies in (
            ("the exclusions", ruled_out.excluded),
            ("the ceiling", bool(ruled_out.too_tall)),
            ("the floor's size", bool(ruled_out.too_big)),
        )
        if applies
    ]
    return list_of(causes) or "the plan's limits"


def _why(limit: Limit, demand: Demand, served_share: float, ruled_out: RuledOut) -> str:
    """The reason as the end of a sentence."""
    if limit.reason == "floor":
        return "nothing more that is worth buying fits on this floor"
    if limit.reason == "budget" and limit.next_piece is not None:
        names, cost = limit.next_piece
        pieces = list_of([f"the {in_sentence(name)}" for name in names])
        if len(names) == 1:
            return f"the next piece worth adding, {pieces}, costs ${cost:,.0f}"
        return f"the next pieces worth adding, {pieces}, cost ${cost:,.0f} together"
    if limit.reason == "met":
        return (
            f"the plan already serves {served_share:.0%} of peak demand, and more equipment "
            "would add very little"
        )
    if limit.reason == "ruled_out":
        return (
            "most of the demand the plan cannot serve needs equipment ruled out by "
            f"{_ruled_out_by(ruled_out)}"
        )
    if limit.reason == "use":
        return (
            f"with about {people(demand.peak.peak_users)} on the floor at the busiest hour, "
            "more equipment would see little use"
        )
    return "more equipment would add very little for its price"


def unallocated_warning(
    remaining: float, limit: Limit, demand: Demand, served_share: float, ruled_out: RuledOut
) -> str:
    why = _why(limit, demand, served_share, ruled_out)
    text = f"${remaining:,.0f} of the budget is unallocated: {why}."
    if limit.reason == "floor":
        text += " More floor space, or a higher equipment grade, would put it to use."
    return text


def upgrade_note(
    has_upgrades: bool, limit: Limit, demand: Demand, served_share: float, ruled_out: RuledOut
) -> str:
    """Why the upgrade list looks the way it does."""
    if has_upgrades:
        return "What a bigger budget would add next, in order, on the same floor."
    if limit.reason in ("floor", "budget"):
        return "The floor is full: more equipment would need more space, not more budget." # A bigger budget was tried: what it would buy does not fit.
    if limit.reason == "met":
        return "Peak demand is already met: more equipment would add very little."
    return capitalized(_why(limit, demand, served_share, ruled_out)) + "."


def ruled_out_notes(
    catalog: Catalog, first_choice: Mapping[str, float], total_load: float, ruled_out: RuledOut
) -> list[str]:
    """Notes on what the ceiling and the floor rule out, naming the pieces members would miss
    most and counting the rest."""
    notes: list[str] = []
    for ids, one, many in (
        (
            ruled_out.too_tall,
            "The ceiling is too low for {names}.",
            "The ceiling is too low for {count} kinds of equipment, among them {names}.",
        ),
        (
            ruled_out.too_big,
            "{names} won’t fit on this floor.",
            "{count} kinds of equipment won’t fit on this floor, among them {names}.",
        ),
    ):
        missed = sorted(
            (eid for eid in ids if first_choice.get(eid, 0.0) >= NAMED_SHARE * total_load),
            key=lambda eid: -first_choice.get(eid, 0.0),
        )
        if not missed:
            continue
        names = list_of([f"the {in_sentence(catalog.equipment_by_id[eid].name)}" for eid in missed[:NAMES_IN_NOTE]]) # Each name keeps its own article: catalog names carry "and" and "with" of their own.
        if len(ids) <= NAMES_IN_NOTE and len(missed) == len(ids):
            notes.append(capitalized(one.format(names=names)))
        else:
            notes.append(many.format(count=len(ids), names=names))
    return notes


def nothing_to_plan(
    catalog: Catalog,
    width_in: float,
    depth_in: float,
    ruled_out: RuledOut,
    allowed: bool,
    equipment_budget: float,
    cheapest: float | None,
    demand: Demand,
) -> str:
    """Why a plan can hold no equipment at all, for the error that says so."""
    aisle = feet_inches(catalog.space.aisles.main_aisle_in)
    size = f"{feet_inches(width_in)} × {feet_inches(depth_in)}"
    if not allowed:
        if ruled_out.too_big:
            return f"Nothing fits a {size} floor with its {aisle} main aisle kept clear."
        if ruled_out.too_tall:
            return "Nothing is left to plan: the equipment not excluded needs a higher ceiling."
        return "Nothing is left to plan: the exclusions leave out every piece of equipment."
    if cheapest is not None and equipment_budget < cheapest:
        return ( # Rounded apart, so the two amounts never read the same.
            f"After flooring, ${math.floor(equipment_budget):,} is left for equipment, less than "
            f"the cheapest piece (${math.ceil(cheapest):,}). Raise the budget or leave flooring "
            "out."
        )
    return (
        f"With about {people(demand.peak.peak_users)} on the floor at the busiest hour, no "
        "equipment would see enough use to be worth buying."
    )
