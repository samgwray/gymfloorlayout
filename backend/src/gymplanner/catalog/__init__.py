"""Versioned datasets: equipment, exercises, behavior, space rules, costs, and sources."""

from functools import lru_cache

from gymplanner.catalog.loader import Catalog, CatalogError, load_catalog
from gymplanner.settings import get_settings


@lru_cache(maxsize=1)
def get_catalog() -> Catalog:
    """Process-wide catalog loaded from the configured data directory."""
    return load_catalog(get_settings().data_dir)


__all__ = ["Catalog", "CatalogError", "get_catalog", "load_catalog"]
