"""Erlang loss (M/G/c/c) formulas.

A station type with ``c`` identical stations offered ``a`` Erlangs of demand (the average
number of people who want to be on it at once) turns a fraction ``B(c, a)`` of arrivals away
because every station is busy. The blocking probability is insensitive to the distribution
of time spent on a station; only its mean matters, which suits gym sets of varied length.

Carried load ``a * (1 - B(c, a))`` is increasing and concave in ``c``, so every extra station
of a type is worth less than the previous one. That diminishing return is what makes the
optimizer prefer variety when demand is light and redundancy when demand is heavy.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

_SCALAR_TAIL = 8
"""Elements left in the recursion below which plain floats are faster than array calls."""


def erlang_b(servers: int, load: float) -> float:
    """Blocking probability for ``servers`` stations offered ``load`` Erlangs."""
    if servers < 0:
        raise ValueError("servers must be non-negative")
    if load < 0:
        raise ValueError("load must be non-negative")
    if load == 0:
        return 0.0
    blocking = 1.0
    for c in range(1, servers + 1):
        blocking = load * blocking / (c + load * blocking)
    return blocking


def carried_load(servers: int, load: float) -> float:
    """Average number of stations in use: the demand that is actually served."""
    return load * (1.0 - erlang_b(servers, load))


def erlang_b_vec(servers: NDArray[np.int64], load: NDArray[np.float64]) -> NDArray[np.float64]:
    """Element-wise Erlang B for arrays of equal shape.

    Runs the stable recursion ``B(c) = a B(c-1) / (c + a B(c-1))`` on all elements at once.
    Elements are sorted by server count so step ``c`` only touches the prefix that still has
    at least ``c`` servers, making the cost proportional to total servers, not to
    elements x largest count. Once only a few elements are left (the largest types of a big
    gym), they finish on plain floats, which is the same arithmetic without the array calls.
    """
    servers = np.asarray(servers, dtype=np.int64)
    load = np.asarray(load, dtype=np.float64)
    if servers.shape != load.shape:
        raise ValueError("servers and load must have the same shape")
    flat_servers = servers.ravel()
    order = np.argsort(-flat_servers, kind="stable")
    sorted_servers = flat_servers[order]
    sorted_load = load.ravel()[order]
    blocking = np.ones_like(sorted_load)
    max_servers = int(sorted_servers[0]) if sorted_servers.size else 0
    at_least = np.cumsum(np.bincount(sorted_servers, minlength=max_servers + 1)[::-1])[::-1] # at_least[c] = number of elements with at least c servers.
    for c in range(1, max_servers + 1):
        n = int(at_least[c])
        if n <= _SCALAR_TAIL:
            for i in range(n):
                b, a = float(blocking[i]), float(sorted_load[i])
                for k in range(c, int(sorted_servers[i]) + 1):
                    b = a * b / (k + a * b)
                blocking[i] = b
            break
        head = sorted_load[:n] * blocking[:n]
        blocking[:n] = head / (c + head)
    result = np.empty_like(blocking)
    result[order] = blocking
    result = result.reshape(load.shape)
    return np.where(load <= 0.0, 0.0, result)


def servers_for_blocking(load: float, target: float, limit: int = 10_000) -> int:
    """Smallest server count whose blocking probability is at or below ``target``."""
    if not 0 < target < 1:
        raise ValueError("target must be in (0, 1)")
    if load <= 0:
        return 0
    blocking = 1.0
    for c in range(1, limit + 1):
        blocking = load * blocking / (c + load * blocking)
        if blocking <= target:
            return c
    raise ValueError("target blocking not reachable within limit")
