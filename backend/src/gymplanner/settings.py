"""Runtime settings, resolved from environment variables with sensible defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]


def _default_data_dir() -> Path:
    return _REPO_ROOT / "data"


def _split_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


@dataclass(frozen=True)
class Settings:
    data_dir: Path = field(default_factory=_default_data_dir)
    cors_origins: list[str] = field(default_factory=lambda: ["http://localhost:3100", "http://127.0.0.1:3100"])
    simulation_seed: int = 20_26


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    data_dir = os.environ.get("GYMPLANNER_DATA_DIR")
    origins = os.environ.get("GYMPLANNER_CORS_ORIGINS")
    seed = os.environ.get("GYMPLANNER_SIM_SEED")
    defaults = Settings()
    return Settings(
        data_dir=Path(data_dir).resolve() if data_dir else defaults.data_dir,
        cors_origins=_split_csv(origins) if origins else defaults.cors_origins,
        simulation_seed=int(seed) if seed else defaults.simulation_seed,
    )
