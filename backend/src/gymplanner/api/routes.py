"""HTTP endpoints."""

from __future__ import annotations

from collections import defaultdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from gymplanner.api import schemas as out
from gymplanner.catalog import Catalog, get_catalog
from gymplanner.catalog.schema import Equipment
from gymplanner.demand import exercise_time_weights
from gymplanner.domain import SQIN_PER_SQFT
from gymplanner.planning import PlanError, create_plan
from gymplanner.planning.room import envelope_area_sqin
from gymplanner.planning.service import CATEGORY_LABELS
from gymplanner.planning.shortfall import BUDGET_GOAL_SHARE, LOW_BUDGET_SHARE
from gymplanner.selection.explain import WELL_SUITED_QUALITY
from gymplanner.selection.optimizer import (
    COVERAGE_TOLERANCE,
    MIN_RELATIVE_RETURN,
    MIN_UNIT_USE,
    MOST_WANTED_BLOCKING,
    MOST_WANTED_TOLERANCE,
)
from gymplanner.settings import get_settings
from gymplanner.simulation.types import DEFAULT_PATIENCE_MIN

router = APIRouter(prefix="/api")
CatalogDep = Annotated[Catalog, Depends(get_catalog)]


@router.get("/health")
def health(catalog: CatalogDep) -> dict[str, str]:
    return {"status": "ok", "data_version": catalog.data_version}


@router.get("/meta", response_model=out.MetaOut)
def meta(catalog: CatalogDep) -> out.MetaOut:
    return out.MetaOut(
        data_version=catalog.data_version,
        default_profile=catalog.behavior.default_profile,
        default_grade=catalog.costs.default_grade,
        profiles=[
            out.OptionOut(id=p.id, name=p.name, description=p.description)
            for p in catalog.behavior.profiles
        ],
        grades=[
            out.OptionOut(id=g.id, name=g.name, description=g.description)
            for g in catalog.costs.grades
        ],
        categories=[out.CategoryOut(id=c, label=label) for c, label in CATEGORY_LABELS.items()],
        zones=[
            out.ZoneInfoOut(id=z.id, name=z.name, description=z.description)
            for z in sorted(catalog.space.zones, key=lambda z: z.order)
        ],
        scenarios=[
            out.ScenarioOut(
                id=s.id,
                label=s.label,
                description=s.description,
                area_sqft=s.area_sqft,
                budget_usd=s.budget_usd,
                profile=s.profile,
                grade=s.grade,
            )
            for s in catalog.scenarios
        ],
        limits=out.LimitsOut(
            area_min_sqft=out.AREA_MIN_SQFT,
            area_max_sqft=out.AREA_MAX_SQFT,
            budget_min_usd=out.BUDGET_MIN_USD,
            budget_max_usd=out.BUDGET_MAX_USD,
        ),
    )


def _equipment_out(
    item: Equipment, catalog: Catalog, fit: dict[str, dict[str, float]]
) -> out.EquipmentOut:
    fp = item.footprint
    c = item.clearance
    return out.EquipmentOut(
        id=item.id,
        name=item.name,
        category=item.category,
        zone=item.zone,
        description=item.description,
        length_in=fp.length_in,
        width_in=fp.width_in,
        height_in=fp.height_in,
        clearance_in={"front": c.front_in, "back": c.back_in, "left": c.left_in, "right": c.right_in},
        footprint_sqft=round(fp.length_in * fp.width_in / SQIN_PER_SQFT, 2),
        envelope_sqft=round(envelope_area_sqin(item) / SQIN_PER_SQFT, 2),
        stations=item.stations,
        price_usd={g.id: round(catalog.unit_price(item.id, g.id), 2) for g in catalog.costs.grades},
        power=item.power,
        min_ceiling_in=item.min_ceiling_in,
        example_models=list(item.example_models),
        useful_life_years=item.useful_life_years,
        exercises=[name for name, q in fit[item.id].items() if q >= WELL_SUITED_QUALITY],
        sources=list(item.sources),
        notes=item.notes,
    )


@router.get("/equipment", response_model=list[out.EquipmentOut])
def equipment(catalog: CatalogDep) -> list[out.EquipmentOut]:
    fit: dict[str, dict[str, float]] = defaultdict(dict) # Equipment id -> exercise name -> best quality among the routes that use it.
    for exercise in catalog.exercises:
        for option in exercise.options:
            for eid in option.uses:
                best = fit[eid].get(exercise.name, 0.0)
                fit[eid][exercise.name] = max(best, option.quality)
    return [_equipment_out(item, catalog, fit) for item in catalog.equipment]


@router.get("/exercises", response_model=list[out.ExerciseOut])
def exercises(catalog: CatalogDep) -> list[out.ExerciseOut]:
    profile = catalog.profile_by_id[catalog.behavior.default_profile]
    weights = exercise_time_weights(
        catalog.exercises, profile.exercise_multipliers, frozenset(profile.excluded_equipment)
    )
    shares = profile.modality_share.as_dict()
    modality_totals: dict[str, float] = defaultdict(float)
    for exercise in catalog.exercises:
        modality_totals[exercise.modality] += weights[exercise.id]
    names = {e.id: e.name for e in catalog.equipment}
    result = []
    for exercise in catalog.exercises:
        total = modality_totals[exercise.modality]
        share = shares[exercise.modality] * weights[exercise.id] / total if total else 0.0
        result.append(
            out.ExerciseOut(
                id=exercise.id,
                name=exercise.name,
                modality=exercise.modality,
                pattern=exercise.pattern,
                popularity=exercise.popularity,
                block_minutes=exercise.block_minutes,
                time_share=share,
                routes=[
                    out.ExerciseRouteOut(equipment=[names[eid] for eid in option.uses], quality=option.quality)
                    for option in sorted(exercise.options, key=lambda o: -o.quality)
                ],
                sources=list(exercise.sources),
            )
        )
    return result


@router.get("/sources", response_model=list[out.SourceOut])
def sources(catalog: CatalogDep) -> list[out.SourceOut]:
    return [
        out.SourceOut(
            id=s.id,
            title=s.title,
            publisher=s.publisher,
            year=s.year,
            url=s.url,
            kind=s.kind,
            accessed=s.accessed,
            notes=s.notes,
        )
        for s in catalog.sources
    ]


@router.get("/methodology", response_model=out.MethodologyOut)
def methodology(catalog: CatalogDep) -> out.MethodologyOut:
    return out.MethodologyOut(
        behavior=catalog.behavior,
        space=catalog.space,
        costs=catalog.costs,
        benchmarks=list(catalog.benchmarks),
        validation_bands=list(catalog.validation_bands),
        model=out.ModelSettingsOut(
            min_relative_return=MIN_RELATIVE_RETURN,
            min_unit_use=MIN_UNIT_USE,
            most_wanted_tolerance=MOST_WANTED_TOLERANCE,
            most_wanted_blocking=MOST_WANTED_BLOCKING,
            coverage_tolerance=COVERAGE_TOLERANCE,
            low_budget_share=LOW_BUDGET_SHARE,
            budget_goal_share=BUDGET_GOAL_SHARE,
            well_suited_quality=WELL_SUITED_QUALITY,
            patience_min=DEFAULT_PATIENCE_MIN,
        ),
        data_version=catalog.data_version,
    )


@router.post("/plan", response_model=out.PlanResponse)
def plan(request: out.PlanRequest, catalog: CatalogDep) -> out.PlanResponse:
    try:
        return create_plan(request, catalog, seed=get_settings().simulation_seed)
    except PlanError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
