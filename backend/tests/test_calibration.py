"""Plans on the real datasets should look like real gyms of the same size and budget.

The validation bands in ``data/benchmarks.yaml`` come from franchise disclosures, operator
reports and vendor density guides (pieces per 1,000 sq ft, cardio share of pieces). They are per
building, as their sources give them, so they are restated for the training floor the planner is
given before the comparison. These tests run the sample scenarios end to end and check each plan
against the band for its size where a band covers it (none reaches below about 800 sq ft of
training floor), with a modest tolerance because the bands describe typical gyms, not every gym.
``BELOW_DENSITY_BAND`` lists the known shortfalls and why.
"""

from __future__ import annotations

import time
from functools import cache

import pytest

from gymplanner.api.schemas import PlanRequest, PlanResponse
from gymplanner.catalog import Catalog, load_catalog
from gymplanner.catalog.schema import Scenario, ValidationBand
from gymplanner.planning import create_plan, service
from gymplanner.selection.optimizer import COVERAGE_TOLERANCE, serves_within_tolerance
from gymplanner.settings import get_settings

BAND_TOLERANCE = 0.15
"""Plans may sit this far (relative) outside a band's low-high range."""
NON_PIECES = {"mobility"}
"""Mats and accessories are not counted as pieces of equipment in the benchmarks."""
BELOW_DENSITY_BAND = {
    "private_studio": (
        "On 1,200 sq ft the pieces' safety clearances and the aisles (a 60 in main aisle from the "
        "door to the back wall, 36 in walkways) leave only about 6% of the floor unused, so it "
        "holds fewer pieces than the small band's studios, whose data come mostly from class "
        "studios."
    ),
}
"""Scenarios known to sit below their band's piece density, and why."""
SQUAT_STATIONS = {"power_rack", "half_rack", "smith_machine", "leg_press", "hack_squat"}


@cache
def catalog() -> Catalog:
    return load_catalog(get_settings().data_dir)


@cache
def planned(scenario_id: str) -> tuple[PlanResponse, float]:
    scenario = next(s for s in catalog().scenarios if s.id == scenario_id)
    started = time.perf_counter()
    plan = create_plan(_request(scenario), catalog(), seed=2026)
    return plan, time.perf_counter() - started


def _request(scenario: Scenario) -> PlanRequest:
    return PlanRequest(
        area_sqft=scenario.area_sqft,
        budget_usd=scenario.budget_usd,
        profile=scenario.profile,
        grade=scenario.grade,
    )


def _band(training_sqft: float) -> ValidationBand | None:
    """The band, restated for the training floor, whose sizes take in this floor."""
    for band in catalog().validation_bands:
        on_floor = band.on_training_floor()
        if on_floor.total_sqft.low <= training_sqft <= on_floor.total_sqft.high:
            return on_floor
    return None


def _within(value: float, low: float, high: float) -> bool:
    return low * (1 - BAND_TOLERANCE) <= value <= high * (1 + BAND_TOLERANCE)


def scenario_ids() -> list[str]:
    return [s.id for s in catalog().scenarios]


@pytest.mark.parametrize("scenario_id", scenario_ids())
def test_sample_plans_spend_within_budget_and_place_everything(scenario_id: str) -> None:
    plan, _ = planned(scenario_id)
    assert plan.costs.total_usd <= plan.inputs.budget_usd + 0.01
    assert len(plan.layout.placements) == plan.metrics.unit_count
    assert not any(w.startswith("Left out") for w in plan.warnings), plan.warnings


@pytest.mark.parametrize("scenario_id", scenario_ids())
def test_sample_plans_look_like_real_gyms_of_their_size(scenario_id: str) -> None:
    plan, _ = planned(scenario_id)
    band = _band(plan.space.training_sqft)
    if band is None:
        pytest.skip("no validation band covers this size")
    pieces = sum(i.units for i in plan.items if i.category not in NON_PIECES)
    cardio = sum(i.units for i in plan.items if i.category == "cardio")
    per_thousand = pieces / plan.space.training_sqft * 1000
    density = band.pieces_per_1000_sqft
    share = band.cardio_share_of_pieces
    assert _within(cardio / pieces, share.low, share.high), (
        f"cardio {cardio / pieces:.0%} of pieces vs band {share.low:.0%}-{share.high:.0%}"
    )
    if scenario_id in BELOW_DENSITY_BAND and per_thousand < density.low * (1 - BAND_TOLERANCE):
        pytest.xfail(f"{per_thousand:.1f} per 1,000 sq ft. {BELOW_DENSITY_BAND[scenario_id]}")
    assert _within(per_thousand, density.low, density.high), (
        f"{per_thousand:.1f} pieces per 1,000 sq ft vs band {density.low}-{density.high}"
    )


@pytest.mark.parametrize("scenario_id", scenario_ids())
def test_sample_plans_serve_most_peak_demand_without_long_waits(scenario_id: str) -> None:
    plan, _ = planned(scenario_id)
    assert plan.metrics.served_share >= 0.5
    assert plan.metrics.coverage_share >= 0.6
    assert plan.simulation.mean_wait_min <= 3.0


@pytest.mark.parametrize("scenario_id", scenario_ids())
def test_sample_plans_have_enough_of_what_members_ask_for_most(scenario_id: str) -> None:
    plan, _ = planned(scenario_id) # Treadmills are the first choice for the most demand. Cheaper machines that serve runners only as substitutes once took their place, leaving most runners at a busy-day peak with every treadmill busy.
    treadmill = next((i for i in plan.items if i.equipment_id == "treadmill"), None)
    assert treadmill is not None
    if plan.demand.peak_users >= 30:
        assert treadmill.blocking < 0.4, f"{treadmill.units} treadmills, {treadmill.blocking:.0%}"


def test_variety_grows_with_size_and_big_gyms_add_redundancy() -> None:
    ordered = sorted(catalog().scenarios, key=lambda s: s.area_sqft)
    plans = [planned(s.id)[0] for s in ordered]
    types = [p.metrics.type_count for p in plans]
    depth = [p.metrics.unit_count / p.metrics.type_count for p in plans]
    assert types[-1] > types[0]
    assert depth[-1] > 1.5 * depth[0]


@pytest.mark.parametrize("scenario_id", scenario_ids())
def test_sample_plans_compute_quickly(scenario_id: str) -> None:
    _, seconds = planned(scenario_id)
    assert seconds < 8.0


@pytest.mark.parametrize(("area", "budget"), [(1_200, 40_000), (1_500, 60_000)])
def test_small_general_gyms_have_a_squat_station(
    area: float, budget: float, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without the coverage rule these plans spend the rack's money on another bike or a second
    dumbbell set. The two plans serve within ``COVERAGE_TOLERANCE`` of each other, and the one
    with the rack gives far more of its demand a well-suited station."""
    request = PlanRequest(area_sqft=area, budget_usd=budget, profile="general")
    rounded = create_plan(request, catalog(), seed=2026)
    monkeypatch.setattr(service, "COVERAGE_TRIES", 0)
    plain = create_plan(request, catalog(), seed=2026)
    assert SQUAT_STATIONS & {i.equipment_id for i in rounded.items}
    assert not SQUAT_STATIONS & {i.equipment_id for i in plain.items}
    assert rounded.metrics.coverage_share > plain.metrics.coverage_share + 0.05
    assert serves_within_tolerance(
        rounded.metrics.quality_served_share,
        plain.metrics.quality_served_share,
        COVERAGE_TOLERANCE,
    )


def band_ids() -> list[str]:
    return [b.id for b in catalog().validation_bands]


def profile_ids() -> list[str]:
    return [p.id for p in catalog().behavior.profiles]


def _at_band_spend(band_id: str, profile: str, share_of_lowest: float) -> PlanResponse:
    """A plan at the band's typical size, at the default (commercial) grade, whose equipment
    budget is ``share_of_lowest`` of the band's lowest spend per sq ft of training floor, flooring
    left out as the bands leave it."""
    band = next(b for b in catalog().validation_bands if b.id == band_id).on_training_floor()
    sqft = band.total_sqft.typical
    request = PlanRequest(
        area_sqft=sqft,
        budget_usd=band.equipment_usd_per_sqft.low * sqft * share_of_lowest,
        profile=profile,
        include_flooring=False,
    )
    return create_plan(request, catalog(), seed=2026)


@pytest.mark.parametrize("profile", profile_ids())
@pytest.mark.parametrize("band_id", band_ids())
def test_the_lowest_spend_real_gyms_report_is_not_called_far_short(
    band_id: str, profile: str
) -> None:
    assert _at_band_spend(band_id, profile, 1.0).budget_note is None


@pytest.mark.parametrize("band_id", band_ids())
def test_a_third_of_the_lowest_spend_real_gyms_report_is_called_far_short(band_id: str) -> None:
    """For general fitness. A functional floor's equipment is cheap enough that a third of the
    lowest spend can still serve over half of what the floor could."""
    note = _at_band_spend(band_id, "general", 1 / 3).budget_note
    assert note is not None
    assert note.startswith("This budget buys far less than your members would use.")


def test_a_narrow_floor_is_measured_by_what_it_holds_laid_out() -> None:
    """On 12 x 50 ft the layout holds far less than the floor's area suggests. $10,000 buys a plan
    serving under half of what the area model says the floor could, but over half of what it
    holds laid out, so it is not called far short; $6,000 is."""
    request = PlanRequest(area_sqft=600, width_ft=12, depth_ft=50, budget_usd=10_000)
    assert create_plan(request, catalog(), seed=2026).budget_note is None
    request = request.model_copy(update={"budget_usd": 6_000})
    assert create_plan(request, catalog(), seed=2026).budget_note is not None
