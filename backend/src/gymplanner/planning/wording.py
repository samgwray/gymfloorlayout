"""Plain-English pieces for the sentences a plan carries: notes, warnings and assumptions."""

from __future__ import annotations

import re
from collections.abc import Sequence

PROPER_FIRST_WORDS = frozenset(
    {"Olympic", "Smith", "Bulgarian", "Romanian", "Pallof", "Farmer's", "Nordic", "Copenhagen"}
)
"""First words that keep their capital inside a sentence."""


def in_sentence(name: str) -> str:
    """'Treadmill' -> 'treadmill'; 'Olympic bench', 'GHD raise' and 'T-bar row' keep capitals."""
    first = name.split(maxsplit=1)[0] if name else ""
    if first in PROPER_FIRST_WORDS or re.match(r"^.[A-Z-]", first):
        return name
    return name[:1].lower() + name[1:]


def capitalized(text: str) -> str:
    return text[:1].upper() + text[1:]


def list_of(items: Sequence[str]) -> str:
    """'a', 'a and b', 'a, b and c'."""
    if len(items) <= 1:
        return "".join(items)
    return f"{', '.join(items[:-1])} and {items[-1]}"


def _plural(word: str) -> str:
    if re.search(r"(s|x|z|ch|sh)$", word, re.IGNORECASE):
        return f"{word}es"
    if re.search(r"[^aeiou]y$", word, re.IGNORECASE):
        return f"{word[:-1]}ies"
    return f"{word}s"


def the_units(name: str, units: int) -> str:
    """'the treadmill', 'the 3 treadmills'.

    Names with sizes or extras ('Dumbbells 5-50 lb with rack') don't take a plural ending, so
    the count follows them instead: 'the dumbbells 5-50 lb with rack (2)'.
    """
    phrase = in_sentence(name)
    if units == 1:
        return f"the {phrase}"
    if re.search(r"[\d(]|\bwith\b", phrase):
        return f"the {phrase} ({units})"
    head, _, last = phrase.rpartition(" ")
    return f"the {units} {head} {_plural(last)}" if head else f"the {units} {_plural(last)}"


def feet_inches(inches: float) -> str:
    """60 -> 5′, 79 -> 6′ 7″, 8 -> 8″."""
    feet, rest = divmod(round(inches), 12)
    if feet == 0:
        return f"{rest}″"
    return f"{feet}′" if rest == 0 else f"{feet}′ {rest}″"


def people(count: float) -> str:
    rounded = round(count)
    return f"{rounded:,} {'person' if rounded == 1 else 'people'}"
