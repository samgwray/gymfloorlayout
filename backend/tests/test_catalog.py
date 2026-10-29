"""Loading and checking the datasets."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from gymplanner.catalog.__main__ import main
from gymplanner.catalog.loader import CatalogError, load_catalog

FIXTURE_DATA = Path(__file__).parent / "fixtures" / "mini_data"


def copy_of_fixture(tmp_path: Path) -> Path:
    data = tmp_path / "data"
    shutil.copytree(FIXTURE_DATA, data)
    return data


def test_a_yaml_syntax_error_is_a_catalog_error_naming_the_file(tmp_path: Path) -> None:
    data = copy_of_fixture(tmp_path)
    (data / "space.yaml").write_text("version: 1\naisles: [unclosed\n", encoding="utf-8")
    with pytest.raises(CatalogError, match=r"space\.yaml: not valid YAML"):
        load_catalog(data)
    assert main(["gymplanner.catalog", str(data)]) == 1


def test_a_source_no_record_cites_is_a_catalog_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    data = copy_of_fixture(tmp_path)
    sources = data / "sources.yaml"
    sources.write_text(
        sources.read_text(encoding="utf-8")
        + "  - id: orphan\n    title: Cited by nothing\n    kind: derived\n",
        encoding="utf-8",
    )
    with pytest.raises(CatalogError, match="source 'orphan' is not cited by any record"):
        load_catalog(data)
    assert main(["gymplanner.catalog", str(data)]) == 1
    assert "source 'orphan' is not cited by any record" in capsys.readouterr().err

    scenarios = data / "scenarios.yaml" # Scenarios cite sources like every other record.
    scenarios.write_text(
        scenarios.read_text(encoding="utf-8").replace("[test-derived]", "[test-derived, orphan]"),
        encoding="utf-8",
    )
    assert load_catalog(data).scenarios[0].sources == ["test-derived", "orphan"]
