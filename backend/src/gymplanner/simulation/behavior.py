"""Member behavior for the design-hour simulation: what to train next and how long to stay.

Both are calibrated so that, with no congestion, the simulated floor reproduces the demand
model: each exercise receives its offered Erlangs, members occupy stations for
``1 - idle_share`` of their visit, and visits average ``mean_floor_minutes``.
"""

from __future__ import annotations

from bisect import bisect_right
from collections.abc import Iterator
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

_BISECTION_STEPS = 64
_MIX_TOLERANCE = 1e-6


def idle_gap_minutes(block_minutes: NDArray[np.float64], idle_share: float) -> NDArray[np.float64]:
    """Mean idle gap after a block, sized so idle time is ``idle_share`` of every cycle."""
    return block_minutes * (idle_share / (1.0 - idle_share))


def no_repeat_weights(frequency: NDArray[np.float64]) -> NDArray[np.float64] | None:
    """Draw weights whose no-immediate-repeat chain keeps ``frequency`` as the long-run mix.

    Drawing from ``q`` with the previous exercise left out is a reversible Markov chain with
    stationary distribution proportional to ``q (1 - q)``, so drawing from the target ``p``
    itself would under-represent the most popular exercises. Solving ``q (1 - q) = c p``, with
    ``c`` set so that ``q`` sums to one, restores the target. Each ``q`` is a root of that
    quadratic: the smaller root for every exercise, unless the top exercise is popular enough
    (from about a third of all blocks, depending on the rest of the mix) that it needs the
    larger one. No repeat-free sequence can give one exercise half of all blocks or more;
    ``None`` then means picks have to be drawn independently, repeats included.
    """
    p = np.asarray(frequency, dtype=np.float64)
    p = p / p.sum()
    if p.size < 2:
        return None
    top = int(np.argmax(p))
    if p[top] >= 0.5:
        return None
    c_max = 0.25 / float(p[top])

    def small_roots(c: float) -> NDArray[np.float64]:
        x = c * p # (1 - sqrt(1 - 4x)) / 2, rearranged to avoid cancellation when x is small.
        roots: NDArray[np.float64] = 2.0 * x / (1.0 + np.sqrt(np.clip(1.0 - 4.0 * x, 0.0, None)))
        return roots

    large_top = small_roots(c_max).sum() < 1.0

    def excess(c: float) -> float:
        roots = small_roots(c)
        if large_top:
            return float(roots.sum() - 2.0 * roots[top]) # Sum with the top exercise on its large root, 1 - small root, less 1. It rises from 0 at c = 0 (slope 1 - 2 p_top) and crosses below 0 once before c_max.
        return float(roots.sum()) - 1.0

    low, high = 0.0, c_max # Bisect on the sign change: excess >= 0 on one side of the root and < 0 on the other.
    for _ in range(_BISECTION_STEPS):
        mid = 0.5 * (low + high)
        if (excess(mid) >= 0.0) == large_top:
            low = mid
        else:
            high = mid
    q = small_roots(high)
    if large_top:
        q[top] = 1.0 - q[top]
    q = q / float(q.sum())
    stationary = q * (1.0 - q)
    if not np.allclose(stationary / stationary.sum(), p, rtol=0.0, atol=_MIX_TOLERANCE):
        return None # numerically degenerate (top share within rounding of one half)
    return q


@dataclass(frozen=True)
class ExerciseMix:
    """Samples the exercise a member trains next.

    A visit's first pick follows the target block frequencies directly. Later picks draw from
    the corrected weights with the previous exercise left out, a chain whose stationary mix is
    that same target, so every pick (not only the long-run average) has the intended
    distribution.
    """

    first: tuple[float, ...]
    """Cumulative target block frequencies; the last entry is exactly 1."""
    following: tuple[float, ...] | None
    """Cumulative no-repeat draw weights, or None when picks are drawn independently: a
    single exercise, or one that makes up half of all blocks or more."""

    @classmethod
    def from_frequency(cls, frequency: NDArray[np.float64]) -> ExerciseMix:
        frequency = np.asarray(frequency, dtype=np.float64)
        if frequency.size == 0:
            return cls(first=(), following=None)
        weights = no_repeat_weights(frequency)
        return cls(first=_cumulative(frequency), following=None if weights is None else _cumulative(weights))

    @property
    def size(self) -> int:
        return len(self.first)

    def pick(self, previous: int, uniform: Iterator[float]) -> int:
        """Index of the next exercise; ``previous`` is -1 at the start of a visit.

        Later picks take one uniform over the cumulative weights with the previous
        exercise's interval cut out: the same distribution as redrawing repeats, without a
        redraw loop that slows down as the top exercise's weight nears one.
        """
        if previous < 0 or self.following is None:
            return bisect_right(self.first, next(uniform))
        cumulative = self.following
        last = len(cumulative) - 1
        start = cumulative[previous - 1] if previous else 0.0
        width = cumulative[previous] - start
        point = next(uniform) * (1.0 - width)
        if point >= start:
            point += width
        choice = min(bisect_right(cumulative, point), last)
        if choice == previous: # rounding put the point on an edge of the cut-out interval
            choice = previous + 1 if previous < last else previous - 1
        return choice


def _cumulative(weights: NDArray[np.float64]) -> tuple[float, ...]:
    total = np.minimum(np.cumsum(weights / weights.sum()), 1.0)
    total[-1] = 1.0
    return tuple(total.tolist())


@dataclass(frozen=True)
class VisitModel:
    """How long members plan to stay and how often they start an exercise block."""

    planned_minutes: float
    """Mean planned floor time: the target visit less the expected overrun of the last cycle."""
    cv: float
    cycle_minutes: float
    """Mean time from one block attempt to the next (block plus idle gap), without waiting."""
    overrun_minutes: float
    """Expected time spent past the planned floor time finishing the cycle in progress."""


def visit_model(
    frequency: NDArray[np.float64],
    block_minutes: NDArray[np.float64],
    idle_share: float,
    block_cv: float,
    mean_floor_minutes: float,
    floor_cv: float,
) -> VisitModel:
    """Calibrate planned floor time so that whole visits average ``mean_floor_minutes``.

    A visit is a run of complete cycles (block, then idle gap): a member whose planned time is
    up finishes the cycle in progress. That keeps time on stations at exactly
    ``1 - idle_share`` of the visit, and renewal theory puts the expected overrun at the mean
    residual cycle, E[C^2] / (2 E[C]), with cycles mixed by block frequency. Planning that
    much less time keeps visits, and through Little's law the floor population, on target.
    """
    if frequency.size == 0:
        return VisitModel(mean_floor_minutes, floor_cv, 0.0, 0.0)
    p = frequency / frequency.sum()
    gap = idle_gap_minutes(block_minutes, idle_share)
    cycle = block_minutes + gap
    second_moment = (block_cv * block_minutes) ** 2 + gap**2 + cycle**2 # Gamma block plus exponential gap: Var = (cv * block)^2 + gap^2.
    cycle_minutes = float(p @ cycle)
    overrun = float(p @ second_moment) / (2.0 * cycle_minutes)
    return VisitModel(
        planned_minutes=max(mean_floor_minutes - overrun, 0.0),
        cv=floor_cv,
        cycle_minutes=cycle_minutes,
        overrun_minutes=overrun,
    )


def gamma_draws(rng: np.random.Generator, mean: float, cv: float, size: int) -> NDArray[np.float64]:
    """Gamma variates parameterized by mean and coefficient of variation (cv 0: constant)."""
    if mean <= 0.0:
        return np.zeros(size)
    if cv <= 0.0:
        return np.full(size, mean)
    shape = 1.0 / cv**2
    return rng.gamma(shape, mean / shape, size)


def residual_draws(
    rng: np.random.Generator, mean: float, cv: float, size: int
) -> NDArray[np.float64]:
    """Time left for people already present: the equilibrium distribution of a gamma stay.

    Someone found mid-stay is more likely to be on a long one; the length-biased gamma has
    shape + 1, and the share of it still ahead is uniform.
    """
    if mean <= 0.0:
        return np.zeros(size)
    if cv <= 0.0:
        return rng.random(size) * mean
    shape = 1.0 / cv**2
    return rng.random(size) * rng.gamma(shape + 1.0, mean / shape, size)
