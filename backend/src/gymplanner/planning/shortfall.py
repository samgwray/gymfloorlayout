"""Whether a budget is far short of what members would use, and a rough budget that would not be.

A plan the budget stops is flagged at the top when it serves less than ``LOW_BUDGET_SHARE`` of
what its floor could serve with no budget limit. That is measured on the layout: the plan the
greedy buys with money no object, laid out on the floor. Aisles and clearances take more of a
small or narrow floor than the optimizer's area model allows, and the layout keeps only what
fits.

The flag gives a rough budget for ``BUDGET_GOAL_SHARE`` of that. The greedy builds the floor up
with the money the unlimited plan spent to get there, then once more with what that build-up
cost, which ranks purchases closer to how a budget near the goal would; a small plan is settled
by a search over the budget. The plan found must reach the goal, with ``ESTIMATE_ALLOWANCE`` to
spare, once laid out; a small plan the layout cannot place in full is fitted to the floor at
rising budgets instead, as the planner would fit it.

The greedy's time grows with peak demand, so past ``ESTIMATE_LOAD`` both plans are found on a
copy of the floor scaled down to it, demand and space alike, then scaled back up and tried on the
floor itself at sizes from half to one and a half times the scale (``SCALE_UP``): a big floor
pools its demand and needs fewer spare units per member, while rounding can leave a plan just
short.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np
from numpy.typing import NDArray

from gymplanner.planning.fitting import Floor, fit_to_floor, placed_units, selection_of
from gymplanner.planning.reasons import Limit
from gymplanner.selection import Constraints, RouteTable, Selection, evaluate, greedy
from gymplanner.selection.optimizer import plan_worth, unlimited_plan

LOW_BUDGET_SHARE = 0.5
"""A plan the budget stops is flagged when it serves less than this share of what its floor could
serve with no budget limit: members would find less than half of what the floor could give them.
At the commercial grade, budgets that low sit below the lowest equipment spend per sq ft in the
validation bands, flooring aside as the bands leave it."""
BUDGET_GOAL_SHARE = 0.8
"""The flag gives a rough budget for a plan that serves this share of what the floor could, to
the nearest 5%."""
ESTIMATE_ALLOWANCE = 0.025
"""The estimate aims this much (relative) above the share it names: the plan built at a budget
serves a little less than the greedy's plan at it once it holds the piece members ask for most
(``MOST_WANTED_TOLERANCE``) or a station more of them can use (``COVERAGE_TOLERANCE``)."""
ESTIMATE_LOAD = 60.0
"""Peak demand (Erlangs) past which the estimate works on a scaled-down copy of the floor: about
7,500 sq ft of general fitness at the default density, where the estimate takes about a second
and a half."""
SCALE_UP = np.linspace(0.5, 1.5, 51)
"""Sizes, relative to the scale, at which a plan found on the copy is tried on the floor itself."""
SEARCH_UNITS = 30
"""A plan of at most this many units is settled by a search over the budget: one purchase is a
large share of it, so the build-up can overshoot by a whole piece, and a greedy run takes
milliseconds."""
SEARCH_STEPS = 8
FIT_UNITS = 60
"""A plan of at most this many units that the layout cannot place in full is fitted to the floor
(``fit_to_floor``) at budgets ``FIT_STEP`` apart, up to about twice its cost: small and odd-shaped
floors hold less than any area model allows, and fitting a plan that size takes a fraction of a
second."""
FIT_STEP = 1.15
FIT_TRIES = 6
_TINY = 1e-9


@dataclass(frozen=True)
class Shortfall:
    """A budget far short of what members would use."""

    goal_share: float
    """A share of peak demand a bigger budget would serve on this floor (a multiple of 5%)."""
    goal_equipment_usd: float | None
    """About what the equipment for it would cost, freight and installation included when the
    plan includes them; None when no plan found reaches it once laid out."""


def budget_shortfall(
    floor: Floor, cons: Constraints, selection: Selection, limit: Limit
) -> Shortfall | None:
    """Whether the budget holds the plan below ``LOW_BUDGET_SHARE`` of what its floor could serve
    with no budget limit (``cons`` as the request sets them, before any plan holds units) and, if
    so, a rough budget for ``BUDGET_GOAL_SHARE`` of that."""
    if limit.reason != "budget":
        return None
    table = floor.table
    total = max(table.total_load, _TINY)
    share = selection.value / total
    if share >= LOW_BUDGET_SHARE: # No floor serves more than all of its demand: a plan serving half of it is not flagged.
        return None
    scale = max(1.0, float(table.load.sum()) / ESTIMATE_LOAD)
    small_table, small_cons = _scaled_down(table, cons, scale)
    unlimited = unlimited_plan(small_table, small_cons)
    held, crowded = _laid_out(floor, cons, _scaled_up(unlimited.units, scale, cons))
    capacity = held.value / total
    if share >= LOW_BUDGET_SHARE * capacity:
        return None
    goal = round(BUDGET_GOAL_SHARE * capacity * 20) / 20
    aim = goal * (1 + ESTIMATE_ALLOWANCE)
    if goal <= share or aim >= capacity:
        return Shortfall(goal_share=goal, goal_equipment_usd=None)
    held_cons, small_held = cons, small_cons
    if crowded:
        held_cons = replace(cons, area_sqin=held.area) # The layout holds less than the area model allows: plan within the area it held, as the fit loop re-plans.
        small_held = replace(small_cons, area_sqin=held.area / scale)
    units = _plan_reaching(small_table, small_held, unlimited, aim * small_table.total_load)
    if units is not None and scale > 1:
        units = _on_the_floor(table, held_cons, units * scale, aim * total)
    usd = None if units is None else _budget_that_fits(floor, cons, units, aim * total)
    return Shortfall(goal_share=goal, goal_equipment_usd=usd)


def _scaled_down(
    table: RouteTable, cons: Constraints, scale: float
) -> tuple[RouteTable, Constraints]:
    """The floor ``scale`` times smaller, and its demand with it."""
    if scale == 1:
        return table, cons
    return (
        replace(table, load=table.load / scale, unroutable_load=table.unroutable_load / scale),
        replace(cons, area_sqin=cons.area_sqin / scale),
    )


def _scaled_up(units: NDArray[np.int64], scale: float, cons: Constraints) -> NDArray[np.int64]:
    """A plan for the scaled-down copy, made ``scale`` times bigger for the floor itself."""
    if scale == 1:
        return units
    scaled = np.where(units > 0, np.maximum(np.round(units * scale), 1), 0)
    return np.minimum(scaled, cons.max_units).astype(np.int64)


def _laid_out(floor: Floor, cons: Constraints, units: NDArray[np.int64]) -> tuple[Selection, bool]:
    """``units`` as laid out, and whether the layout left any out: it keeps only what fits."""
    table = floor.table
    planned = selection_of(table, cons, units)
    layout = floor.lay_out(planned)
    if not layout.unplaced:
        return planned, False
    return selection_of(table, cons, placed_units(table, cons, layout)), True


def _budget_that_fits(
    floor: Floor, cons: Constraints, units: NDArray[np.int64], value: float
) -> float | None:
    """What ``units`` cost, when the layout places enough of them to be worth ``value``; otherwise,
    for a small plan, the first budget (``FIT_STEP`` apart) at which the plan fitted to the floor
    is worth it. None when neither is."""
    placed, _ = _laid_out(floor, cons, units)
    budget = float(units @ cons.unit_cost)
    if placed.value >= value:
        return budget
    if units.sum() > FIT_UNITS:
        return None
    for _ in range(FIT_TRIES):
        if fit_to_floor(floor, replace(cons, budget_usd=budget), placed).selection.value >= value:
            return budget
        budget *= FIT_STEP
    return None


def _plan_reaching(
    table: RouteTable, cons: Constraints, unlimited: Selection, value: float
) -> NDArray[np.int64] | None:
    """The least costly plan found that is worth ``value`` (see the module docstring); None when
    the greedy does not reach it."""
    spend = next((s.total_cost for s in unlimited.steps if s.value >= value), unlimited.cost)
    found = plan_worth(table, cons, value, spend) or plan_worth(table, cons, value, unlimited.cost)
    if found is None:
        return None
    again = plan_worth(table, cons, value, found[1])
    units, cost = found if again is None or again[1] >= found[1] else again
    if units.sum() > SEARCH_UNITS:
        return units
    low = 0.0
    for _ in range(SEARCH_STEPS):
        budget = (low + cost) / 2
        trial = greedy(table, replace(cons, budget_usd=budget, min_units=None), record_steps=False, until_value=value)
        if trial.value >= value:
            units, cost = trial.units, trial.cost
        else:
            low = budget
    return units


def _on_the_floor(
    table: RouteTable, cons: Constraints, units: NDArray[np.floating], value: float
) -> NDArray[np.int64] | None:
    """The smallest of ``units`` times ``SCALE_UP`` (each type kept to at least one unit) that
    fits the floor's area and is worth ``value`` on it; None when none is."""
    scaled = np.round(units[None, :] * SCALE_UP[:, None])
    trials = np.minimum(np.where(units > 0, np.maximum(scaled, 1), 0), cons.max_units)
    trials = trials.astype(np.int64)
    worth = (evaluate(table, trials).value >= value) & (trials @ cons.unit_area <= cons.area_sqin)
    if not worth.any():
        return None
    smallest: NDArray[np.int64] = trials[int(np.argmax(worth))]
    return smallest


def _rounded_up(usd: float) -> float:
    """$162,907 -> $165,000: rounded up in steps of half a unit of the second figure, as rough as
    the estimate, so that the budget named covers the plan it stands for."""
    step = 10.0 ** max(0, math.floor(math.log10(max(usd, 1.0))) - 1) / 2
    return math.ceil(usd / step) * step


def budget_note(shortfall: Shortfall, budget_usd: float, flooring_usd: float) -> str:
    """'This budget buys far less than your members would use. About $165,000 would serve 65% of
    peak demand on this floor.' The figure is a whole budget, flooring included when the plan
    includes it, so it reads against the one entered."""
    text = "This budget buys far less than your members would use."
    if shortfall.goal_equipment_usd is None:
        return text
    needed = _rounded_up(shortfall.goal_equipment_usd + flooring_usd)
    if needed <= budget_usd:
        return text
    return (
        f"{text} About ${needed:,.0f} would serve {shortfall.goal_share:.0%} of peak demand on "
        "this floor."
    )
