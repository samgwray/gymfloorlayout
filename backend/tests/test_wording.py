"""Plain-English helpers used in plan notes and assumptions."""

from __future__ import annotations

import pytest

from gymplanner.planning.wording import feet_inches, in_sentence, list_of, people, the_units


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Treadmill", "treadmill"),
        ("Elliptical cross-trainer", "elliptical cross-trainer"),
        ("Olympic flat bench station", "Olympic flat bench station"),
        ("GHD raise", "GHD raise"),
        ("T-bar row", "T-bar row"),
        ("", ""),
    ],
)
def test_in_sentence_lowercases_all_but_proper_names_and_initials(name: str, expected: str) -> None:
    assert in_sentence(name) == expected


@pytest.mark.parametrize(
    ("name", "units", "expected"),
    [
        ("Treadmill", 1, "the treadmill"),
        ("Treadmill", 3, "the 3 treadmills"),
        ("Stair climber", 2, "the 2 stair climbers"),
        ("Bench press station", 2, "the 2 bench press stations"),
        ("Hip thrust bench", 2, "the 2 hip thrust benches"),
        ("Assault body", 2, "the 2 assault bodies"),
        ("Dumbbells 5-50 lb with rack", 2, "the dumbbells 5-50 lb with rack (2)"),
        ("Multi-station gym (3-4 stacks)", 2, "the multi-station gym (3-4 stacks) (2)"),
    ],
)
def test_the_units_counts_and_pluralizes(name: str, units: int, expected: str) -> None:
    assert the_units(name, units) == expected


def test_list_of_joins_with_commas_and_a_final_and() -> None:
    assert list_of([]) == ""
    assert list_of(["a"]) == "a"
    assert list_of(["a", "b"]) == "a and b"
    assert list_of(["a", "b", "c"]) == "a, b and c"


@pytest.mark.parametrize(("inches", "expected"), [(60, "5′"), (36, "3′"), (79, "6′ 7″"), (8, "8″"), (143.6, "12′")])
def test_feet_inches(inches: float, expected: str) -> None:
    assert feet_inches(inches) == expected


def test_people_agrees_with_its_count() -> None:
    assert people(1.2) == "1 person"
    assert people(38.4) == "38 people"
    assert people(1240) == "1,240 people"
