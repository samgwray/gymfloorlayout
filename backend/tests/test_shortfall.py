"""The note at the top of a plan whose budget is far short of what its members would use."""

from __future__ import annotations

import re
from functools import cache
from pathlib import Path

import pytest

from gymplanner.api.schemas import PlanRequest, PlanResponse
from gymplanner.catalog import Catalog, load_catalog
from gymplanner.planning import create_plan, shortfall
from gymplanner.planning.shortfall import Shortfall, budget_note

FIXTURE_DATA = Path(__file__).parent / "fixtures" / "mini_data"
NOTE_START = "This budget buys far less than your members would use."
FIGURE = re.compile(r"About \$([\d,]+) would serve (\d+)% of peak demand on this floor\.$")


@cache
def catalog() -> Catalog:
    return load_catalog(FIXTURE_DATA)


@cache
def plan(area: float, budget: float, **options: object) -> PlanResponse:
    request = PlanRequest(area_sqft=area, budget_usd=budget, **options)
    return create_plan(request, catalog(), seed=11)


def named(note: str | None) -> tuple[float, float]:
    """The budget and the share a note names."""
    found = FIGURE.search(note or "")
    assert found, note
    return float(found.group(1).replace(",", "")), int(found.group(2)) / 100


def shown(share: float) -> int:
    """A share as the page shows it, a whole percentage."""
    return round(share * 100)


SHORT = [
    pytest.param(800, 15_000, {}, id="small"),
    pytest.param(600, 6_000, {"width_ft": 12, "depth_ft": 50}, id="narrow"),
    pytest.param(6_000, 40_000, {}, id="medium"),
    pytest.param(8_500, 70_000, {}, id="just-past-the-copy"), # Past ESTIMATE_LOAD the estimate works on a scaled-down copy of the floor.
    pytest.param(20_000, 160_000, {}, id="large"),
    pytest.param(20_000, 130_000, {"members": 400}, id="few-members-on-a-big-floor"), # Few members on a big floor: their demand, not the area, sets the scale.
]


@pytest.mark.parametrize(("area", "budget", "options"), SHORT)
def test_a_budget_far_short_says_so_with_a_budget_that_delivers(
    area: float, budget: float, options: dict[str, object]
) -> None:
    result = plan(area, budget, **options)
    assert result.budget_note is not None
    assert result.budget_note.startswith(NOTE_START)
    figure, share = named(result.budget_note)
    assert figure > budget
    assert share > result.metrics.quality_served_share
    at_figure = plan(area, figure, **options)
    assert shown(at_figure.metrics.quality_served_share) >= shown(share)
    assert at_figure.budget_note is None


@pytest.mark.parametrize(("area", "budget", "options"), SHORT)
def test_the_named_budget_is_not_padded(
    area: float, budget: float, options: dict[str, object]
) -> None:
    """A fifth less than the named budget falls short of the share it names."""
    figure, share = named(plan(area, budget, **options).budget_note)
    below = plan(area, 0.8 * figure, **options)
    assert shown(below.metrics.quality_served_share) < shown(share)


@pytest.mark.parametrize(("area", "budget"), [(1_500, 40_000), (6_000, 180_000), (20_000, 900_000)])
def test_a_budget_that_serves_over_half_of_what_the_floor_could_has_no_note(
    area: float, budget: float
) -> None:
    assert plan(area, budget).budget_note is None


def test_the_note_is_not_repeated_among_the_notes_under_the_costs() -> None:
    result = plan(6_000, 40_000)
    assert result.budget_note is not None
    assert not any(NOTE_START in warning for warning in result.warnings)


def test_the_named_budget_includes_flooring_only_when_the_plan_does() -> None:
    with_flooring, _ = named(plan(20_000, 160_000).budget_note)
    without, _ = named(plan(20_000, 40_000, include_flooring=False).budget_note)
    flooring = plan(20_000, 160_000).costs.flooring_usd
    assert with_flooring - without == pytest.approx(flooring, rel=0.1)


def test_the_estimate_on_a_scaled_down_copy_agrees_with_the_floor_itself(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = PlanRequest(area_sqft=20_000, budget_usd=160_000)
    scaled = named(create_plan(request, catalog(), seed=11).budget_note)
    monkeypatch.setattr(shortfall, "ESTIMATE_LOAD", float("inf"))
    direct = named(create_plan(request, catalog(), seed=11).budget_note)
    assert scaled[1] <= direct[1] # The copy pools less demand, so it never names more of it.
    assert scaled[0] == pytest.approx(direct[0], rel=0.15)


@pytest.mark.parametrize(
    ("usd", "rounded"),
    [(162_907, 165_000), (224_849.6, 225_000), (41_000, 41_000), (9_876, 9_900), (1_234_567, 1_250_000), (480, 480)],
)
def test_the_named_budget_is_rounded_up(usd: float, rounded: float) -> None:
    note = budget_note(Shortfall(goal_share=0.7, goal_equipment_usd=usd), 100, flooring_usd=0)
    assert named(note) == (rounded, 0.7)


def test_without_a_figure_above_the_budget_the_note_says_only_that_it_falls_short() -> None:
    assert budget_note(Shortfall(0.7, None), 50_000, 0) == NOTE_START
    assert budget_note(Shortfall(0.7, 45_000), 50_000, 0) == NOTE_START
