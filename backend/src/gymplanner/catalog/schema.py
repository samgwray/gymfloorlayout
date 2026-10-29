"""Schemas for the versioned datasets in ``data/``.

Every dataset record carries ``sources`` (ids into ``sources.yaml``) so each number used by
the engine can be traced back to where it came from. Lengths are inches, prices are USD.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ZoneId = Literal["cardio", "machines", "free_weights", "functional", "stretching"]
Category = Literal[
    "cardio",
    "racks_barbells",
    "free_weights",
    "selectorized",
    "plate_loaded",
    "cables",
    "functional",
    "mobility",
]
Modality = Literal["cardio", "barbell", "dumbbell", "machine", "cable", "bodyweight", "functional", "mobility"]
MODALITIES: tuple[Modality, ...] = (
    "cardio",
    "barbell",
    "dumbbell",
    "machine",
    "cable",
    "bodyweight",
    "functional",
    "mobility",
)
Pattern = Literal[
    "squat",
    "hinge",
    "lunge",
    "glute",
    "knee_isolation",
    "calf",
    "horizontal_push",
    "vertical_push",
    "horizontal_pull",
    "vertical_pull",
    "shoulder_isolation",
    "arm",
    "core",
    "carry",
    "conditioning",
    "cardio",
    "mobility",
]
PriceTier = Literal["value", "commercial", "premium"]
GradeId = Literal["value", "commercial", "premium", "refurbished"]
SourceKind = Literal[
    "standard",
    "manufacturer",
    "retailer",
    "study",
    "industry_report",
    "filing",
    "app_data",
    "dataset",
    "article",
    "derived",
]


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Source(_Model):
    id: str
    title: str
    publisher: str | None = None
    year: str | None = None
    url: str | None = None
    kind: SourceKind
    accessed: str | None = None
    notes: str | None = None

    @field_validator("year", mode="before")
    @classmethod
    def _year_as_text(cls, value: object) -> object:
        return str(value) if isinstance(value, int) else value


class SourcesFile(_Model):
    version: int
    sources: list[Source]


class Dimensions(_Model):
    """Footprint. ``length_in`` runs front-to-back as the user faces the equipment."""

    length_in: float = Field(gt=0)
    width_in: float = Field(gt=0)
    height_in: float | None = Field(default=None, gt=0)


class Clearance(_Model):
    """Free zone beyond the footprint that must stay clear of other equipment and walls."""

    front_in: float = Field(ge=0)
    back_in: float = Field(ge=0)
    left_in: float = Field(ge=0)
    right_in: float = Field(ge=0)


class PriceTiers(_Model):
    value: float = Field(gt=0)
    commercial: float = Field(gt=0)
    premium: float = Field(gt=0)

    @model_validator(mode="after")
    def _ordered(self) -> PriceTiers:
        if not self.value <= self.commercial <= self.premium:
            raise ValueError("price tiers must satisfy value <= commercial <= premium")
        return self

    def tier(self, tier: PriceTier) -> float:
        return float(getattr(self, tier))


class LayoutHints(_Model):
    aisle_side: Literal["front", "back", "side", "any"] = "front"
    """Side of the footprint that must open onto an aisle (where the user gets on/off)."""
    against_wall: bool = False
    """Prefers a wall behind it (dumbbell racks, cable crossovers, rigs, heavy bags)."""
    row_group: str | None = None
    """Items sharing a row group are placed together in rows; defaults to the equipment id."""
    flexible_length: bool = False
    """Length may shrink to fit the room (e.g. turf lanes), down to ``min_length_in``."""
    min_length_in: float | None = Field(default=None, gt=0)


class Equipment(_Model):
    id: str
    name: str
    category: Category
    zone: ZoneId
    description: str
    footprint: Dimensions
    clearance: Clearance
    stations: int = Field(default=1, ge=1)
    """Users the unit can serve at the same time (e.g. a dual-stack cable crossover = 2)."""
    price_usd: PriceTiers
    power: Literal["none", "standard_outlet", "dedicated_circuit"] = "none"
    min_ceiling_in: float | None = Field(default=None, gt=0)
    max_units: int | None = Field(default=None, ge=1)
    requires: list[str] = Field(default_factory=list)
    """Equipment ids that must already be in the plan before this one is useful."""
    layout: LayoutHints = Field(default_factory=LayoutHints)
    example_models: list[str] = Field(default_factory=list)
    useful_life_years: float | None = Field(default=None, gt=0)
    sources: list[str] = Field(min_length=1)
    notes: str | None = None


class EquipmentFile(_Model):
    version: int
    equipment: list[Equipment]


class ExerciseOption(_Model):
    uses: list[str] = Field(min_length=1)
    """Equipment ids that are all occupied while performing the exercise this way."""
    quality: float = Field(gt=0, le=1)
    """How well this option serves the exercise relative to the ideal setup (1.0)."""


class Exercise(_Model):
    id: str
    name: str
    modality: Modality
    pattern: Pattern
    popularity: float = Field(gt=0)
    """Relative frequency with which gym-goers perform this exercise within its modality."""
    block_minutes: float = Field(gt=0)
    """Minutes a station is occupied per exercise block: sets x (work + rest) + setup."""
    options: list[ExerciseOption] = Field(min_length=1)
    sources: list[str] = Field(min_length=1)
    notes: str | None = None


class ExercisesFile(_Model):
    version: int
    exercises: list[Exercise]


class ModalityShares(_Model):
    """Share of active floor time the average member spends in each modality (sums to 1)."""

    cardio: float = Field(ge=0)
    barbell: float = Field(ge=0)
    dumbbell: float = Field(ge=0)
    machine: float = Field(ge=0)
    cable: float = Field(ge=0)
    bodyweight: float = Field(ge=0)
    functional: float = Field(ge=0)
    mobility: float = Field(ge=0)

    @model_validator(mode="after")
    def _sums_to_one(self) -> ModalityShares:
        total = sum(self.as_dict().values())
        if abs(total - 1.0) > 0.005:
            raise ValueError(f"modality shares must sum to 1.0 (got {total:.4f})")
        return self

    def as_dict(self) -> dict[Modality, float]:
        return {m: float(getattr(self, m)) for m in MODALITIES}


class SessionModel(_Model):
    mean_floor_minutes: float = Field(gt=0)
    cv: float = Field(gt=0, lt=2)
    idle_share: float = Field(ge=0, lt=1)
    """Share of floor time not occupying any station (transitions, water, changing plates)."""
    sources: list[str] = Field(min_length=1)
    notes: str | None = None


class OccupancyModel(_Model):
    peak_users_per_1000_sqft: float = Field(gt=0)
    """Design-peak users per 1,000 sq ft of training floor (comfortable training density)."""
    daily_visit_rate: float = Field(gt=0, le=1)
    """Visits per member per day."""
    peak_concurrency_share: float = Field(gt=0, le=1)
    """Users on the floor in the busiest hour as a share of that day's visits."""
    design_day_factor: float = Field(ge=1)
    """Busy-day (about 90th percentile) peak relative to an average day's peak."""
    occupant_load_sqft_per_person: float = Field(gt=0)
    """Building-code occupant load factor for exercise rooms; an absolute ceiling on users."""
    sources: list[str] = Field(min_length=1)
    notes: str | None = None


class Profile(_Model):
    id: str
    name: str
    description: str
    modality_share: ModalityShares
    peak_users_per_1000_sqft: float | None = Field(default=None, gt=0)
    exercise_multipliers: dict[str, float] = Field(default_factory=dict)
    excluded_equipment: list[str] = Field(default_factory=list)
    rationale: str
    sources: list[str] = Field(min_length=1)


class BehaviorFile(_Model):
    version: int
    session: SessionModel
    occupancy: OccupancyModel
    default_profile: str
    profiles: list[Profile] = Field(min_length=1)


class AisleRules(_Model):
    main_aisle_in: float = Field(gt=0)
    secondary_aisle_in: float = Field(gt=0)
    sources: list[str] = Field(min_length=1)
    notes: str | None = None


class ZoneSpec(_Model):
    id: ZoneId
    name: str
    order: int
    """Placement order from the entrance (0) toward the back of the room."""
    flooring: str
    description: str


class SpaceFile(_Model):
    version: int
    aisles: AisleRules
    circulation_share: float = Field(gt=0, lt=1)
    packing_efficiency: float = Field(gt=0, le=1)
    """Initial ratio of equipment envelope area to training-floor area used during selection."""
    zones: list[ZoneSpec] = Field(min_length=1)
    default_ceiling_in: float = Field(gt=0)
    sources: list[str] = Field(min_length=1)
    notes: str | None = None


class Range(_Model):
    low: float = Field(ge=0)
    typical: float = Field(ge=0)
    high: float = Field(ge=0)


class FlooringSpec(_Model):
    id: str
    name: str
    cost_per_sqft: Range
    sources: list[str] = Field(min_length=1)
    notes: str | None = None


class GradeSpec(_Model):
    id: GradeId
    name: str
    description: str
    price_tier: PriceTier
    multiplier: float = Field(default=1.0, gt=0)
    sources: list[str] = Field(min_length=1)


class CostsFile(_Model):
    version: int
    default_grade: GradeId
    grades: list[GradeSpec] = Field(min_length=1)
    flooring: list[FlooringSpec] = Field(min_length=1)
    installation_rate: float = Field(ge=0, lt=1)
    """Freight, delivery and assembly as a share of equipment cost."""
    installation_sources: list[str] = Field(min_length=1)
    notes: str | None = None


class Benchmark(_Model):
    id: str
    name: str
    format: str
    sqft: Range | None = None
    equipment_budget_usd: Range | None = None
    members: Range | None = None
    equipment_counts: dict[str, float] = Field(default_factory=dict)
    notes: str | None = None
    sources: list[str] = Field(min_length=1)


class ValidationBand(_Model):
    """What real gyms of a size class look like; plans are checked against these ranges."""

    id: str
    label: str
    total_sqft: Range
    equipment_usd_per_sqft: Range
    pieces_per_1000_sqft: Range
    cardio_share_of_pieces: Range
    training_share: float = Field(gt=0, le=1)
    """Share of a building of the band's typical size that is training floor. The sizes, spend
    and density are per building, as the sources give them; ``on_training_floor`` restates
    them for the training floor the planner is given."""
    notes: str | None = None
    sources: list[str] = Field(min_length=1)

    def on_training_floor(self) -> ValidationBand:
        """The band per sq ft of training floor: sizes scaled down, spend and density up."""
        share = self.training_share

        def scaled(r: Range, factor: float) -> Range:
            return Range(low=r.low * factor, typical=r.typical * factor, high=r.high * factor)

        return self.model_copy(
            update={
                "total_sqft": scaled(self.total_sqft, share),
                "equipment_usd_per_sqft": scaled(self.equipment_usd_per_sqft, 1 / share),
                "pieces_per_1000_sqft": scaled(self.pieces_per_1000_sqft, 1 / share),
                "training_share": 1.0,
            }
        )


class BenchmarksFile(_Model):
    version: int
    benchmarks: list[Benchmark]
    validation_bands: list[ValidationBand] = Field(default_factory=list)


class Scenario(_Model):
    id: str
    label: str
    description: str
    area_sqft: float = Field(gt=0)
    budget_usd: float = Field(gt=0)
    profile: str
    grade: GradeId
    sources: list[str] = Field(min_length=1)


class ScenariosFile(_Model):
    version: int
    scenarios: list[Scenario]
