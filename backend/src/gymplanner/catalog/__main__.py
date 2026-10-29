"""Validate the datasets and print a summary: ``python -m gymplanner.catalog [data_dir]``."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from gymplanner.catalog.loader import CatalogError, load_catalog
from gymplanner.settings import get_settings


def main(argv: list[str]) -> int:
    data_dir = Path(argv[1]) if len(argv) > 1 else get_settings().data_dir
    try:
        catalog = load_catalog(data_dir)
    except CatalogError as exc:
        print(exc, file=sys.stderr)
        return 1
    categories = Counter(e.category for e in catalog.equipment)
    modalities = Counter(e.modality for e in catalog.exercises)
    print(f"data version {catalog.data_version} from {data_dir}")
    print(f"  equipment: {len(catalog.equipment)} ({dict(categories)})")
    print(f"  exercises: {len(catalog.exercises)} ({dict(modalities)})")
    print(f"  profiles:  {', '.join(p.id for p in catalog.behavior.profiles)}")
    print(f"  sources:   {len(catalog.sources)}")
    print(f"  benchmarks: {len(catalog.benchmarks)}, scenarios: {len(catalog.scenarios)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
