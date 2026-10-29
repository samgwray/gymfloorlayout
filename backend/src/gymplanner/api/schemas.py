"""Request and response models for the HTTP API.

Lengths are inches and areas square feet unless a field name says otherwise. Layout
coordinates put the origin at the front-left corner of the training floor: x runs along the
entrance wall, y runs from the entrance wall toward the back.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from gymplanner.catalog.schema import (
    BehaviorFile,
    Benchmark,
    Category,
    CostsFile,
    GradeId,
    Modality,
    Pattern,
    SpaceFile,
    ValidationBand,
    ZoneId,
)

AREA_MIN_SQFT = 150.0
AREA_MAX_SQFT = 250_000.0
BUDGET_MIN_USD = 1_000.0
BUDGET_MAX_USD = 50_000_000.0


class _Out(BaseModel):
    model_config = ConfigDict(frozen=True)


class PlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    area_sqft: float = Field(ge=AREA_MIN_SQFT, le=AREA_MAX_SQFT)
    """The training floor: the space for equipment, aisles and stretching. Reception, locker
    rooms and restrooms are the operator's to add and are not part of it."""
    budget_usd: float = Field(ge=BUDGET_MIN_USD, le=BUDGET_MAX_USD)
    profile: str | None = None
    """Gym focus profile id; defaults to the data's average gym-goer profile."""
    grade: GradeId | None = None
    width_ft: float | None = Field(default=None, gt=0, le=2_000)
    """Side along the entrance wall. With ``depth_ft`` it replaces ``area_sqft``, and the floor
    they make is held to the same area limits; alone, the other side is the area over it. No
    side may be shorter than the main aisle is wide."""
    depth_ft: float | None = Field(default=None, gt=0, le=2_000)
    """Side from the entrance wall to the back wall (see ``width_ft``)."""
    ceiling_ft: float | None = Field(default=None, ge=7, le=60)
    members: int | None = Field(default=None, ge=1, le=200_000)
    include_flooring: bool = True
    include_installation: bool = True
    entrance: Literal["left", "center", "right"] = "center"
    exclude: list[str] = Field(default_factory=list, max_length=200)
    """Equipment ids or category ids to leave out of the plan."""


class RectOut(_Out):
    x: float
    y: float
    w: float
    h: float


class PlacementOut(_Out):
    uid: str
    equipment_id: str
    name: str
    zone: ZoneId
    rect: RectOut
    """Footprint as placed (already rotated)."""
    envelope: RectOut
    """Footprint plus required clearances."""
    rotation: Literal[0, 90, 180, 270]
    """Direction the equipment's front faces: 0 = toward the entrance wall (-y), then clockwise."""


class ZoneOut(_Out):
    id: ZoneId
    name: str
    rect: RectOut


class LayoutOut(_Out):
    width_in: float
    depth_in: float
    entrance_x_in: float
    zones: list[ZoneOut]
    aisles: list[RectOut]
    placements: list[PlacementOut]
    warnings: list[str]
    notes: list[str]
    """How the floor was laid out, such as the main aisle's route; nothing to act on."""


class LineItemOut(_Out):
    equipment_id: str
    name: str
    category: Category
    zone: ZoneId
    units: int
    stations: int
    unit_price_usd: float
    installation_usd: float
    subtotal_usd: float
    footprint_sqft: float
    """Per unit, footprint only."""
    envelope_sqft: float
    """Per unit, footprint plus clearances."""
    utilization: float
    """Average share of this type's stations in use during the design hour."""
    blocking: float
    """Probability a member finds every station of this type busy."""
    served_users: float
    """Average number of members using this type during the design hour."""
    top_exercises: list[str]
    rationale: str
    example_models: list[str]
    power: Literal["none", "standard_outlet", "dedicated_circuit"]


class CategoryCostOut(_Out):
    category: Category
    label: str
    usd: float


class CostsOut(_Out):
    budget_usd: float
    equipment_usd: float
    installation_usd: float
    flooring_usd: float
    total_usd: float
    remaining_usd: float
    by_category: list[CategoryCostOut]


class ZoneSpaceOut(_Out):
    zone: ZoneId
    name: str
    sqft: float
    share: float


class SpaceOut(_Out):
    training_sqft: float
    equipment_footprint_sqft: float
    equipment_envelope_sqft: float
    by_zone: list[ZoneSpaceOut]


class DemandOut(_Out):
    profile_id: str
    profile_name: str
    peak_users: float
    active_users: float
    members_estimate: float | None
    method: Literal["members", "density"]
    capped_by_code: bool
    modality_share: dict[Modality, float]


class MetricsOut(_Out):
    served_share: float
    """Share of design-hour demand that finds a free station on any acceptable route."""
    quality_served_share: float
    """Served share weighted by how well the route fits the exercise (the objective)."""
    coverage_share: float
    """Popularity-weighted share of exercises with a well-suited (quality >= 0.8) option."""
    unit_count: int
    type_count: int


class PatternCoverageOut(_Out):
    pattern: Pattern
    label: str
    coverage: float
    """Demand-weighted best available route quality for exercises of this pattern (0-1)."""
    equipment: list[str]
    """Names of the equipment that serves this pattern in the plan."""


class BusyEquipmentOut(_Out):
    equipment_id: str
    name: str
    utilization: float


class SimulationOut(_Out):
    seed: int
    simulated_minutes: float
    visits: int
    exercise_blocks: int
    mean_wait_min: float
    p90_wait_min: float
    first_choice_share: float
    substituted_share: float
    skipped_share: float
    peak_concurrent_users: int
    busiest: list[BusyEquipmentOut]


class UpgradeItemOut(_Out):
    equipment_id: str
    name: str
    units: int


class UpgradeOut(_Out):
    items: list[UpgradeItemOut]
    """Equipment bought together in this step (more than one when items only work together)."""
    cost_usd: float
    gain_share: float
    """Increase in quality-weighted served share from this step."""


class AssumptionOut(_Out):
    label: str
    value: str
    sources: list[str]


class ResolvedInputsOut(_Out):
    area_sqft: float
    budget_usd: float
    profile: str
    grade: GradeId
    width_ft: float
    depth_ft: float
    ceiling_ft: float
    members: int | None
    include_flooring: bool
    include_installation: bool
    entrance: Literal["left", "center", "right"]
    exclude: list[str]


class PlanResponse(_Out):
    inputs: ResolvedInputsOut
    demand: DemandOut
    metrics: MetricsOut
    costs: CostsOut
    space: SpaceOut
    items: list[LineItemOut]
    layout: LayoutOut
    coverage: list[PatternCoverageOut]
    simulation: SimulationOut
    next_upgrades: list[UpgradeOut]
    """What a bigger budget would add next on the same floor, in order; every step is one the
    layout places beside the plan and the steps before it."""
    upgrade_note: str
    """Why the upgrade list looks the way it does: what a bigger budget adds, or what stops the
    plan from growing (the floor, peak demand already met, too few members, exclusions)."""
    budget_note: str | None
    """For the top of the plan when the budget holds it far below what its floor could serve
    with no budget limit: that members would use far more, and a rough budget that would serve
    most of what the floor could. None otherwise."""
    warnings: list[str]
    assumptions: list[AssumptionOut]
    data_version: str
    compute_ms: float


class OptionOut(_Out):
    id: str
    name: str
    description: str


class ScenarioOut(_Out):
    id: str
    label: str
    description: str
    area_sqft: float
    budget_usd: float
    profile: str
    grade: GradeId


class LimitsOut(_Out):
    area_min_sqft: float
    area_max_sqft: float
    budget_min_usd: float
    budget_max_usd: float


class CategoryOut(_Out):
    id: Category
    label: str


class ZoneInfoOut(_Out):
    id: ZoneId
    name: str
    description: str


class MetaOut(_Out):
    data_version: str
    default_profile: str
    default_grade: GradeId
    profiles: list[OptionOut]
    grades: list[OptionOut]
    categories: list[CategoryOut]
    zones: list[ZoneInfoOut]
    scenarios: list[ScenarioOut]
    limits: LimitsOut


class EquipmentOut(_Out):
    id: str
    name: str
    category: Category
    zone: ZoneId
    description: str
    length_in: float
    width_in: float
    height_in: float | None
    clearance_in: dict[Literal["front", "back", "left", "right"], float]
    footprint_sqft: float
    envelope_sqft: float
    stations: int
    price_usd: dict[GradeId, float]
    power: Literal["none", "standard_outlet", "dedicated_circuit"]
    min_ceiling_in: float | None
    example_models: list[str]
    useful_life_years: float | None
    exercises: list[str]
    """Exercises this equipment serves well (a well-suited route uses it); exercises it only
    stands in for are left out."""
    sources: list[str]
    notes: str | None


class ExerciseRouteOut(_Out):
    equipment: list[str]
    quality: float


class ExerciseOut(_Out):
    id: str
    name: str
    modality: Modality
    pattern: Pattern
    popularity: float
    block_minutes: float
    time_share: float
    """Share of active floor time for the default profile."""
    routes: list[ExerciseRouteOut]
    sources: list[str]


class SourceOut(_Out):
    id: str
    title: str
    publisher: str | None
    year: str | None
    url: str | None
    kind: str
    accessed: str | None
    notes: str | None


class ModelSettingsOut(_Out):
    """Planner constants that live in code rather than in the datasets."""

    min_relative_return: float
    """Buying stops when a purchase's value per dollar falls below this share of the plan's
    average value per dollar so far (taken over at least half the budget)."""
    min_unit_use: float
    """Buying stops when a purchase would serve fewer Erlangs than this per unit at the design
    peak: a unit in use for less of the busiest hour has too few members to use it."""
    most_wanted_tolerance: float
    """The type members ask for most stays in the plan unless leaving it out serves more than
    this share more demand."""
    most_wanted_blocking: float
    """The type members ask for most is kept at enough units that at most this share of the
    members who come for it find every one busy at the peak, within the tolerance above."""
    coverage_tolerance: float
    """A station that gives more of the demand a well-suited option joins the plan when the plan
    with it serves within this share of the plan without it."""
    low_budget_share: float
    """A plan the budget stops is flagged when it serves less than this share of what its floor
    could serve with no budget limit, measured on the layout."""
    budget_goal_share: float
    """The flag gives a rough budget for a plan that serves this share of what the floor could."""
    well_suited_quality: float
    """Route quality from which an exercise counts as well served."""
    patience_min: float
    """How long a simulated member waits for a suitable station before settling or skipping."""


class MethodologyOut(_Out):
    behavior: BehaviorFile
    space: SpaceFile
    costs: CostsFile
    benchmarks: list[Benchmark]
    validation_bands: list[ValidationBand]
    model: ModelSettingsOut
    data_version: str
