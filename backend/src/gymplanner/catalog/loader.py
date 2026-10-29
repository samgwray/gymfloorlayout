"""Load the YAML datasets, validate them, and check cross-references between files."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any, TypeVar

import yaml
from pydantic import BaseModel

from gymplanner.catalog.schema import (
    MODALITIES,
    BehaviorFile,
    Benchmark,
    BenchmarksFile,
    CostsFile,
    Equipment,
    EquipmentFile,
    Exercise,
    ExercisesFile,
    GradeSpec,
    Profile,
    Scenario,
    ScenariosFile,
    Source,
    SourcesFile,
    SpaceFile,
    ValidationBand,
    ZoneSpec,
)

M = TypeVar("M", bound=BaseModel)


class CatalogError(ValueError):
    """Raised when the datasets are malformed or inconsistent with each other."""


def _read(path: Path, model: type[M]) -> M:
    if not path.exists():
        raise CatalogError(f"missing dataset file: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            raw: Any = yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        raise CatalogError(f"{path.name}: not valid YAML: {exc}") from exc
    try:
        return model.model_validate(raw)
    except ValueError as exc: # pydantic.ValidationError subclasses ValueError
        raise CatalogError(f"{path.name}: {exc}") from exc


@dataclass(frozen=True)
class Catalog:
    """All datasets, validated and indexed for lookup."""

    equipment: tuple[Equipment, ...]
    exercises: tuple[Exercise, ...]
    behavior: BehaviorFile
    space: SpaceFile
    costs: CostsFile
    benchmarks: tuple[Benchmark, ...]
    validation_bands: tuple[ValidationBand, ...]
    scenarios: tuple[Scenario, ...]
    sources: tuple[Source, ...]
    data_version: str = field(default="0")

    @cached_property
    def equipment_by_id(self) -> dict[str, Equipment]:
        return {item.id: item for item in self.equipment}

    @cached_property
    def exercise_by_id(self) -> dict[str, Exercise]:
        return {item.id: item for item in self.exercises}

    @cached_property
    def source_by_id(self) -> dict[str, Source]:
        return {item.id: item for item in self.sources}

    @cached_property
    def profile_by_id(self) -> dict[str, Profile]:
        return {item.id: item for item in self.behavior.profiles}

    @cached_property
    def grade_by_id(self) -> dict[str, GradeSpec]:
        return {item.id: item for item in self.costs.grades}

    @cached_property
    def zone_by_id(self) -> dict[str, ZoneSpec]:
        return {item.id: item for item in self.space.zones}

    def unit_price(self, equipment_id: str, grade_id: str) -> float:
        grade = self.grade_by_id[grade_id]
        item = self.equipment_by_id[equipment_id]
        return item.price_usd.tier(grade.price_tier) * grade.multiplier


def _duplicates(ids: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    dupes: list[str] = []
    for value in ids:
        if value in seen:
            dupes.append(value)
        seen.add(value)
    return dupes


def _citations(catalog: Catalog) -> list[tuple[str, list[str]]]:
    """Every record that cites sources, with the source ids it cites."""
    behavior, space, costs = catalog.behavior, catalog.space, catalog.costs
    return [
        *((f"equipment '{e.id}'", e.sources) for e in catalog.equipment),
        *((f"exercise '{e.id}'", e.sources) for e in catalog.exercises),
        ("behavior.session", behavior.session.sources),
        ("behavior.occupancy", behavior.occupancy.sources),
        *((f"profile '{p.id}'", p.sources) for p in behavior.profiles),
        ("space", space.sources),
        ("space.aisles", space.aisles.sources),
        ("costs.installation", costs.installation_sources),
        *((f"grade '{g.id}'", g.sources) for g in costs.grades),
        *((f"flooring '{f.id}'", f.sources) for f in costs.flooring),
        *((f"benchmark '{b.id}'", b.sources) for b in catalog.benchmarks),
        *((f"validation band '{b.id}'", b.sources) for b in catalog.validation_bands),
        *((f"scenario '{s.id}'", s.sources) for s in catalog.scenarios),
    ]


def _validate(catalog: Catalog) -> None:
    errors: list[str] = []

    for label, ids in (
        ("equipment", [e.id for e in catalog.equipment]),
        ("exercise", [e.id for e in catalog.exercises]),
        ("source", [s.id for s in catalog.sources]),
        ("profile", [p.id for p in catalog.behavior.profiles]),
        ("zone", [z.id for z in catalog.space.zones]),
        ("grade", [g.id for g in catalog.costs.grades]),
        ("benchmark", [b.id for b in catalog.benchmarks]),
        ("validation band", [b.id for b in catalog.validation_bands]),
        ("scenario", [s.id for s in catalog.scenarios]),
    ):
        for dupe in _duplicates(ids):
            errors.append(f"duplicate {label} id: {dupe}")

    equipment_ids = set(catalog.equipment_by_id)
    exercise_ids = set(catalog.exercise_by_id)
    source_ids = set(catalog.source_by_id)
    zone_ids = set(catalog.zone_by_id)
    flooring_ids = {f.id for f in catalog.costs.flooring}

    cited: set[str] = set()
    for owner, refs in _citations(catalog):
        errors += [f"{owner}: unknown source id '{ref}'" for ref in refs if ref not in source_ids]
        cited.update(refs)
    errors += [
        f"source '{s.id}' is not cited by any record" for s in catalog.sources if s.id not in cited
    ]

    for item in catalog.equipment:
        if item.zone not in zone_ids:
            errors.append(f"equipment '{item.id}': unknown zone '{item.zone}'")
        for req in item.requires:
            if req not in equipment_ids:
                errors.append(f"equipment '{item.id}': requires unknown equipment '{req}'")

    used_equipment: set[str] = set()
    modalities_with_exercises: set[str] = set()
    for exercise in catalog.exercises:
        modalities_with_exercises.add(exercise.modality)
        for option in exercise.options:
            for ref in option.uses:
                used_equipment.add(ref)
                if ref not in equipment_ids:
                    errors.append(f"exercise '{exercise.id}': unknown equipment '{ref}'")
            if len(set(option.uses)) != len(option.uses):
                errors.append(f"exercise '{exercise.id}': option repeats equipment {option.uses}")

    for item in catalog.equipment:
        if item.id not in used_equipment:
            errors.append(f"equipment '{item.id}' is not used by any exercise option")

    behavior = catalog.behavior
    if behavior.default_profile not in catalog.profile_by_id:
        errors.append(f"behavior.default_profile '{behavior.default_profile}' is not a profile")
    for profile in behavior.profiles:
        for ref in profile.exercise_multipliers:
            if ref not in exercise_ids:
                errors.append(f"profile '{profile.id}': unknown exercise '{ref}'")
        for ref in profile.excluded_equipment:
            if ref not in equipment_ids:
                errors.append(f"profile '{profile.id}': unknown excluded equipment '{ref}'")
        excluded = set(profile.excluded_equipment)
        for modality, share in profile.modality_share.as_dict().items():
            if share <= 0:
                continue
            placeable = [
                e
                for e in catalog.exercises
                if e.modality == modality
                and profile.exercise_multipliers.get(e.id, 1.0) > 0
                and any(not excluded.intersection(o.uses) for o in e.options)
            ]
            if not placeable:
                errors.append(
                    f"profile '{profile.id}': modality '{modality}' has a share but no exercise "
                    "its members can do"
                )
        for ref, factor in profile.exercise_multipliers.items():
            if factor < 0:
                errors.append(f"profile '{profile.id}': negative multiplier for '{ref}'")

    space = catalog.space
    missing_zones = {"cardio", "machines", "free_weights", "functional", "stretching"} - zone_ids
    if missing_zones:
        errors.append(f"space.zones is missing: {', '.join(sorted(missing_zones))}")
    for zone in space.zones:
        if zone.flooring not in flooring_ids:
            errors.append(f"zone '{zone.id}': unknown flooring '{zone.flooring}'")

    costs = catalog.costs
    if costs.default_grade not in catalog.grade_by_id:
        errors.append(f"costs.default_grade '{costs.default_grade}' is not a grade")

    for scenario in catalog.scenarios:
        if scenario.profile not in catalog.profile_by_id:
            errors.append(f"scenario '{scenario.id}': unknown profile '{scenario.profile}'")
        if scenario.grade not in catalog.grade_by_id:
            errors.append(f"scenario '{scenario.id}': unknown grade '{scenario.grade}'")

    if set(MODALITIES) - modalities_with_exercises:
        missing = sorted(set(MODALITIES) - modalities_with_exercises)
        errors.append(f"no exercises for modalities: {', '.join(missing)}")

    if errors:
        raise CatalogError("dataset validation failed:\n  - " + "\n  - ".join(errors))


def _fingerprint(data_dir: Path, version: int) -> str:
    """Schema version plus a short hash of the dataset contents, e.g. ``v1-3f9a0c21``."""
    digest = hashlib.sha256()
    for path in sorted(data_dir.glob("*.yaml")):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return f"v{version}-{digest.hexdigest()[:8]}"


def load_catalog(data_dir: Path) -> Catalog:
    """Load and validate every dataset in ``data_dir``."""
    equipment = _read(data_dir / "equipment.yaml", EquipmentFile)
    exercises = _read(data_dir / "exercises.yaml", ExercisesFile)
    behavior = _read(data_dir / "behavior.yaml", BehaviorFile)
    space = _read(data_dir / "space.yaml", SpaceFile)
    costs = _read(data_dir / "costs.yaml", CostsFile)
    benchmarks = _read(data_dir / "benchmarks.yaml", BenchmarksFile)
    scenarios = _read(data_dir / "scenarios.yaml", ScenariosFile)
    sources = _read(data_dir / "sources.yaml", SourcesFile)

    versions = (
        equipment.version,
        exercises.version,
        behavior.version,
        space.version,
        costs.version,
        benchmarks.version,
        scenarios.version,
        sources.version,
    )
    catalog = Catalog(
        equipment=tuple(equipment.equipment),
        exercises=tuple(exercises.exercises),
        behavior=behavior,
        space=space,
        costs=costs,
        benchmarks=tuple(benchmarks.benchmarks),
        validation_bands=tuple(benchmarks.validation_bands),
        scenarios=tuple(scenarios.scenarios),
        sources=tuple(sources.sources),
        data_version=_fingerprint(data_dir, max(versions)),
    )
    _validate(catalog)
    return catalog
