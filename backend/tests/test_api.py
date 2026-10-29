"""HTTP API against the small fixture catalog."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from gymplanner.api.app import create_app
from gymplanner.catalog import get_catalog, load_catalog
from gymplanner.planning.shortfall import BUDGET_GOAL_SHARE, LOW_BUDGET_SHARE
from gymplanner.selection.explain import WELL_SUITED_QUALITY
from gymplanner.selection.optimizer import (
    COVERAGE_TOLERANCE,
    MIN_RELATIVE_RETURN,
    MIN_UNIT_USE,
    MOST_WANTED_BLOCKING,
    MOST_WANTED_TOLERANCE,
)
from gymplanner.simulation.types import DEFAULT_PATIENCE_MIN

FIXTURE_DATA = Path(__file__).parent / "fixtures" / "mini_data"


@pytest.fixture(scope="module")
def client() -> Iterator[TestClient]:
    app = create_app()
    fixture_catalog = load_catalog(FIXTURE_DATA)
    app.dependency_overrides[get_catalog] = lambda: fixture_catalog
    with TestClient(app) as test_client:
        yield test_client


def test_health(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_meta_lists_options_and_limits(client: TestClient) -> None:
    body = client.get("/api/meta").json()
    assert body["default_profile"] == "general"
    assert {p["id"] for p in body["profiles"]} == {"general", "strength"}
    assert {g["id"] for g in body["grades"]} >= {"value", "commercial", "premium"}
    assert body["zones"][0]["id"] == "cardio"
    assert body["limits"]["area_min_sqft"] < body["limits"]["area_max_sqft"]
    assert body["scenarios"][0]["id"] == "small"


def test_equipment_includes_prices_per_grade_and_uses(client: TestClient) -> None:
    body = client.get("/api/equipment").json()
    treadmill = next(item for item in body if item["id"] == "treadmill")
    assert treadmill["price_usd"]["refurbished"] == pytest.approx(8500 * 0.55)
    assert "Treadmill running" in treadmill["exercises"]
    assert treadmill["envelope_sqft"] > treadmill["footprint_sqft"]


def test_equipment_lists_only_exercises_it_serves_well(client: TestClient) -> None:
    body = {item["id"]: item for item in client.get("/api/equipment").json()}
    assert body["treadmill"]["exercises"] == ["Treadmill running"] # The treadmill is the best route for running but only a 0.5 substitute for cycling.
    assert "Upright cycling" in body["upright_bike"]["exercises"]
    assert "Dumbbell curl" in body["cable_crossover"]["exercises"] # A 0.85 route is still well suited.


def test_exercise_time_shares_sum_to_one(client: TestClient) -> None:
    body = client.get("/api/exercises").json()
    assert sum(item["time_share"] for item in body) == pytest.approx(1.0)
    assert all(item["routes"] for item in body)


def test_sources_and_methodology(client: TestClient) -> None:
    assert {s["id"] for s in client.get("/api/sources").json()} == {"test-standard", "test-derived"}
    body = client.get("/api/methodology").json()
    assert body["behavior"]["default_profile"] == "general"
    assert body["validation_bands"][0]["id"] == "medium"
    assert body["model"] == {
        "min_relative_return": MIN_RELATIVE_RETURN,
        "min_unit_use": MIN_UNIT_USE,
        "most_wanted_tolerance": MOST_WANTED_TOLERANCE,
        "most_wanted_blocking": MOST_WANTED_BLOCKING,
        "coverage_tolerance": COVERAGE_TOLERANCE,
        "low_budget_share": LOW_BUDGET_SHARE,
        "budget_goal_share": BUDGET_GOAL_SHARE,
        "well_suited_quality": WELL_SUITED_QUALITY,
        "patience_min": DEFAULT_PATIENCE_MIN,
    }


def test_plan_round_trip(client: TestClient) -> None:
    response = client.post("/api/plan", json={"area_sqft": 2500, "budget_usd": 60000})
    assert response.status_code == 200
    body = response.json()
    assert body["costs"]["total_usd"] <= 60000
    assert len(body["layout"]["placements"]) == body["metrics"]["unit_count"]
    assert body["inputs"]["profile"] == "general"
    assert body["budget_note"] is None


@pytest.mark.parametrize(
    "payload",
    [
        {"area_sqft": 10, "budget_usd": 50000},
        {"area_sqft": 2000, "budget_usd": 10},
        {"area_sqft": 2000, "budget_usd": 50000, "grade": "gold"},
        {"area_sqft": 2000, "budget_usd": 50000, "unknown": 1},
    ],
)
def test_invalid_requests_are_rejected_with_422(
    client: TestClient, payload: dict[str, object]
) -> None:
    assert client.post("/api/plan", json=payload).status_code == 422


@pytest.mark.parametrize(
    "body",
    [
        '{"area_sqft": NaN, "budget_usd": 50000}',
        '{"area_sqft": 2000, "budget_usd": Infinity}',
        '{"area_sqft": 2000, "budget_usd": 50000, "width_ft": NaN}',
        '{"area_sqft": 2000, "budget_usd": 50000, "ceiling_ft": -Infinity}',
    ],
)
def test_non_finite_numbers_are_rejected_with_422_not_a_server_error(
    client: TestClient, body: str
) -> None:
    response = client.post("/api/plan", content=body, headers={"content-type": "application/json"}) # JSON has no NaN or Infinity, but Python's parser accepts them: the error that names the bad input must still be valid JSON.
    assert response.status_code == 422
    (error,) = response.json()["detail"]
    assert error["msg"] == "Input should be a finite number"
    assert error["input"] in {"nan", "inf", "-inf"}


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"width_ft": 1, "depth_ft": 1}, "1 × 1 ft is 1 sq ft; plans cover 150 to 250,000 sq ft."),
        ({"width_ft": 1e-200, "depth_ft": 1e-200}, "is 0 sq ft"),
        ({"width_ft": 2000, "depth_ft": 2000}, "2,000 × 2,000 ft is 4,000,000 sq ft"),
        ({"width_ft": 2000}, "A floor 1′ deep has no room for the 5′ main aisle."), # One side given: the other is the area over it.
        ({"width_ft": 4, "depth_ft": 500}, "A floor 4′ wide has no room for the 5′ main aisle."),
    ],
)
def test_floor_dimensions_are_held_to_the_area_limits(
    client: TestClient, payload: dict[str, object], message: str
) -> None:
    response = client.post("/api/plan", json={"area_sqft": 2000, "budget_usd": 50000, **payload})
    assert response.status_code == 422
    assert message in response.json()["detail"]


def test_domain_errors_are_reported_as_422_with_a_message(client: TestClient) -> None:
    unknown_profile = client.post("/api/plan", json={"area_sqft": 2000, "budget_usd": 50000, "profile": "yoga"})
    assert unknown_profile.status_code == 422
    assert "profile" in unknown_profile.json()["detail"]
    no_flooring_budget = client.post("/api/plan", json={"area_sqft": 10000, "budget_usd": 2000})
    assert no_flooring_budget.status_code == 422
    assert "flooring" in no_flooring_budget.json()["detail"]
