"""Inputs and outputs for the design-hour discrete-event simulation."""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_PATIENCE_MIN = 3.0


@dataclass(frozen=True)
class SimulationConfig:
    peak_users: float
    """Target average number of members on the floor during the measured window."""
    mean_floor_minutes: float
    floor_minutes_cv: float
    idle_share: float
    seed: int
    patience_min: float = DEFAULT_PATIENCE_MIN
    """How long a member waits for their preferred route before taking a fallback."""
    warmup_min: float = 60.0
    measure_min: float = 120.0
    block_minutes_cv: float = 0.25


@dataclass(frozen=True)
class SimulationResult:
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
    utilization: dict[str, float]
    """Equipment id -> share of station-time busy during the measured window."""
