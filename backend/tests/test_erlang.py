"""Erlang loss formulas: textbook values, exactness, shape properties and the vector kernel.

The optimizer's preference for variety on small floors and redundancy on busy ones rests on
two facts checked here: blocking falls as stations are added, and every extra station carries
less new demand than the one before (carried load is concave in the station count).
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import pairwise

import numpy as np
import pytest

from gymplanner.queueing import carried_load, erlang_b, erlang_b_vec, servers_for_blocking

pytestmark = pytest.mark.filterwarnings("error") # Overflow or 0/0 warnings would mean the stable recursion broke down on valid input.

LOADS = (0.05, 0.5, 1.0, 3.0, 10.0, 40.0, 150.0)


def exact_erlang_b(servers: int, load: float) -> float:
    """Direct Poisson-ratio definition, (a^c / c!) / sum_k a^k / k!, in exact arithmetic."""
    a = Fraction(load)
    term = total = Fraction(1)
    for k in range(1, servers + 1):
        term = term * a / k
        total += term
    return float(term / total)


def log_space_erlang_b(servers: int, load: float) -> float:
    """The same definition in log space, for station counts where exact fractions get slow."""
    logs = [k * math.log(load) - math.lgamma(k + 1) for k in range(servers + 1)]
    peak = max(logs)
    log_total = peak + math.log(math.fsum(math.exp(x - peak) for x in logs))
    return math.exp(logs[-1] - log_total)


@pytest.mark.parametrize(
    ("servers", "load", "expected"),
    [
        (1, 1.0, 0.5),
        (2, 1.0, 0.2),
        (3, 2.0, 4 / 19),
        (10, 5.0, 0.018384570336648),
        (0, 3.0, 1.0),
        (4, 0.0, 0.0),
        (0, 0.0, 0.0),
    ],
)
def test_textbook_values(servers: int, load: float, expected: float) -> None:
    assert erlang_b(servers, load) == pytest.approx(expected, rel=1e-12, abs=1e-15)


@pytest.mark.parametrize(("servers", "load"), [(5, 1.361), (10, 4.461), (20, 12.031), (50, 37.90), (100, 84.06)])
def test_one_percent_grade_of_service_table(servers: int, load: float) -> None:
    """Published Erlang B tables list these loads as 1% blocking (to 4 significant figures)."""
    assert erlang_b(servers, load) == pytest.approx(0.01, rel=1e-3)


@pytest.mark.parametrize("servers", [1, 2, 3, 5, 8, 13, 21, 34, 55])
@pytest.mark.parametrize("load", [0.01, 0.3, 1.0, 2.5, 7.0, 19.5, 60.0, 150.0])
def test_recursion_matches_direct_poisson_ratio(servers: int, load: float) -> None:
    assert erlang_b(servers, load) == pytest.approx(exact_erlang_b(servers, load), rel=1e-12)


@pytest.mark.parametrize(
    ("servers", "load"),
    [(300, 450.0), (500, 480.0), (2_000, 1_950.0), (5_000, 4_900.0), (10, 1_000.0)],
)
def test_recursion_is_stable_for_large_counts(servers: int, load: float) -> None:
    """Factorials overflow long before these counts; the recursion must not."""
    assert erlang_b(servers, load) == pytest.approx(log_space_erlang_b(servers, load), rel=1e-9)


def test_rejects_negative_inputs() -> None:
    with pytest.raises(ValueError, match="servers"):
        erlang_b(-1, 1.0)
    with pytest.raises(ValueError, match="load"):
        erlang_b(2, -0.5)


@pytest.mark.parametrize("load", LOADS)
def test_blocking_decreases_with_servers(load: float) -> None:
    values = [erlang_b(c, load) for c in range(400)]
    assert values[0] == 1.0
    for c in range(len(values) - 1):
        assert 0.0 <= values[c + 1] <= values[c]
        if values[c] > 1e-200: # strict until the value sinks into the subnormal range
            assert values[c + 1] < values[c]


@pytest.mark.parametrize("servers", [1, 2, 5, 20, 100])
def test_blocking_increases_with_load(servers: int) -> None:
    values = [erlang_b(servers, a) for a in np.linspace(0.5, 300.0, 400)] # Starts at 0.5: B(100, 0.01) ~ 1e-358 would underflow and tie at zero.
    assert all(later > earlier for earlier, later in pairwise(values))
    assert all(0.0 < v < 1.0 for v in values)


@pytest.mark.parametrize("load", LOADS)
def test_carried_load_is_increasing_and_concave_in_servers(load: float) -> None:
    """Diminishing returns: each extra station serves less new demand than the previous one."""
    counts = np.arange(3 * int(load) + 60)
    carried = np.array([carried_load(int(c), load) for c in counts])
    marginal = np.diff(carried)
    assert carried[0] == 0.0
    assert np.all(marginal >= -1e-12)
    assert np.all(np.diff(marginal) <= 1e-12)
    assert np.all(carried <= np.minimum(counts, load) + 1e-12)


def test_marginal_station_values_for_one_erlang() -> None:
    """B(1,1)=1/2, B(2,1)=1/5, B(3,1)=1/16: stations add 0.5, 0.3, then 0.1375 Erlangs."""
    gains = np.diff([carried_load(c, 1.0) for c in range(4)])
    assert gains == pytest.approx([0.5, 0.3, 0.1375], rel=1e-12)


def test_carried_load_limits() -> None:
    assert carried_load(10, 1e6) == pytest.approx(10.0, rel=1e-5)
    assert carried_load(500, 3.0) == pytest.approx(3.0, rel=1e-15)
    assert carried_load(0, 7.0) == 0.0


def scalar_reference(servers: np.ndarray, load: np.ndarray) -> np.ndarray:
    flat = [erlang_b(int(c), float(a)) for c, a in zip(servers.ravel(), load.ravel(), strict=True)]
    return np.array(flat, dtype=np.float64).reshape(load.shape)


def test_vec_matches_scalar_on_random_mixed_arrays() -> None:
    rng = np.random.default_rng(2026)
    servers = rng.integers(0, 60, size=(40, 9))
    load = rng.uniform(0.0, 80.0, size=servers.shape)
    servers[rng.random(servers.shape) < 0.1] = 0
    load[rng.random(load.shape) < 0.1] = 0.0
    servers[0, :6] = [3_000, 1_500, 250, 0, 0, 7] # Large and tiny counts in one call: the kernel sorts by count and shrinks the active prefix.
    load[0, :6] = [2_950.0, 1_600.0, 0.0, 12.0, 0.0, 1_000.0]
    np.testing.assert_allclose(erlang_b_vec(servers, load), scalar_reference(servers, load), 1e-12)


@pytest.mark.parametrize("seed", range(5))
def test_vec_matches_scalar_with_many_ties(seed: int) -> None:
    rng = np.random.default_rng(seed)
    servers = rng.choice([0, 1, 1, 2, 3, 3, 3, 40], size=200)
    load = rng.choice([0.0, 0.2, 1.0, 1.0, 5.0, 30.0], size=200)
    np.testing.assert_allclose(erlang_b_vec(servers, load), scalar_reference(servers, load), 1e-12)


def test_vec_zero_servers_and_zero_load() -> None:
    result = erlang_b_vec(np.array([0, 0, 3, 5]), np.array([0.0, 2.0, 0.0, 1e-300]))
    np.testing.assert_array_equal(result[:3], [0.0, 1.0, 0.0])
    assert 0.0 <= result[3] < 1e-300


def test_vec_result_does_not_depend_on_element_order() -> None:
    rng = np.random.default_rng(11)
    servers = rng.integers(0, 30, size=64)
    load = rng.uniform(0.0, 25.0, size=64)
    perm = rng.permutation(64)
    np.testing.assert_array_equal(erlang_b_vec(servers[perm], load[perm]), erlang_b_vec(servers, load)[perm])


def test_vec_preserves_shape_layout_and_inputs() -> None:
    rng = np.random.default_rng(3)
    servers = rng.integers(0, 12, size=(6, 5))
    load = rng.uniform(0.0, 9.0, size=(6, 5))
    servers_before, load_before = servers.copy(), load.copy()
    expected = scalar_reference(servers, load)

    np.testing.assert_allclose(erlang_b_vec(servers, load), expected, 1e-12)
    np.testing.assert_allclose(erlang_b_vec(np.asfortranarray(servers), np.asfortranarray(load)), expected, 1e-12)
    np.testing.assert_allclose(erlang_b_vec(servers[:, ::2], load[:, ::2]), expected[:, ::2], 1e-12)
    np.testing.assert_array_equal(servers, servers_before)
    np.testing.assert_array_equal(load, load_before)


def test_vec_degenerate_shapes() -> None:
    scalar = erlang_b_vec(np.array(10), np.array(5.0))
    assert scalar.shape == ()
    assert float(scalar) == pytest.approx(erlang_b(10, 5.0), rel=1e-12)
    assert erlang_b_vec(np.array([], dtype=np.int64), np.array([])).shape == (0,)
    assert erlang_b_vec(np.zeros((0, 3), dtype=np.int64), np.zeros((0, 3))).shape == (0, 3)


def test_vec_rejects_mismatched_shapes() -> None:
    with pytest.raises(ValueError, match="same shape"):
        erlang_b_vec(np.array([1, 2]), np.array([1.0]))


@pytest.mark.parametrize(
    ("load", "servers"),
    [
        (1.36, 5),
        (1.362, 6),
        (4.46, 10),
        (4.462, 11),
        (12.03, 20),
        (12.032, 21),
        (37.89, 50),
        (37.91, 51),
        (84.06, 100),
        (84.07, 101),
    ],
)
def test_servers_for_one_percent_blocking_match_table(load: float, servers: int) -> None:
    """Just under a table entry fits that many stations; just over needs one more."""
    assert servers_for_blocking(load, 0.01) == servers


@pytest.mark.parametrize("load", [0.01, 0.4, 1.0, 4.46, 12.0, 37.9, 84.0, 300.0])
@pytest.mark.parametrize("target", [0.5, 0.1, 0.02, 0.01, 0.001])
def test_servers_for_blocking_is_smallest_sufficient_count(load: float, target: float) -> None:
    servers = servers_for_blocking(load, target)
    assert servers >= 1
    assert erlang_b(servers, load) <= target
    assert erlang_b(servers - 1, load) > target


def test_servers_for_blocking_edge_cases() -> None:
    assert servers_for_blocking(0.0, 0.05) == 0
    for target in (0.0, 1.0, -0.1, 1.5):
        with pytest.raises(ValueError, match="target"):
            servers_for_blocking(3.0, target)
    with pytest.raises(ValueError, match="not reachable"):
        servers_for_blocking(1_000.0, 1e-6, limit=5)
