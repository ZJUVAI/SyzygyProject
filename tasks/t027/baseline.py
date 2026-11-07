"""Bounded randomized first-improvement pair-swap search; no witness reads."""
import os
import random
import math
from pathlib import Path
from mathbench.search import search_steps

N = 256
ITERATION_LIMIT = 10_000


def initial_permutation():
    """Return the deterministic identity seed without opening any task data."""
    return list(range(N))


def _load_matrices():
    raw = (Path(__file__).parent / "data" / "tai256c.dat").read_text(encoding="ascii").split()
    values = [int(x) for x in raw]
    if len(values) != 1 + 2 * N * N or values[0] != N:
        raise ValueError("bad tai256c matrix data")
    cut = 1 + N * N
    a = [values[1 + i * N:1 + (i + 1) * N] for i in range(N)]
    b = [values[cut + i * N:cut + (i + 1) * N] for i in range(N)]
    return a, b


def _score(a, b, p):
    return sum(a[i][j] * b[p[i]][p[j]] for i in range(N) for j in range(N))


def _swap_delta(a, b, p, r, s):
    """Exact objective change from swapping assignments at r and s, in O(n)."""
    pr, ps = p[r], p[s]
    delta = 0
    for k in range(N):
        if k == r or k == s:
            continue
        pk = p[k]
        delta += a[r][k] * (b[ps][pk] - b[pr][pk])
        delta += a[s][k] * (b[pr][pk] - b[ps][pk])
        delta += a[k][r] * (b[pk][ps] - b[pk][pr])
        delta += a[k][s] * (b[pk][pr] - b[pk][ps])
    delta += a[r][r] * (b[ps][ps] - b[pr][pr])
    delta += a[s][s] * (b[pr][pr] - b[ps][ps])
    delta += a[r][s] * (b[ps][pr] - b[pr][ps])
    delta += a[s][r] * (b[pr][ps] - b[ps][pr])
    return delta


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T027-C01") != "T027-C01":
        raise ValueError("unsupported T027 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    seconds_env = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    seconds = None if seconds_env is None else float(seconds_env)
    if seconds is not None and (not math.isfinite(seconds) or seconds <= 0):
        raise ValueError("MATHBENCH_SEARCH_SECONDS must be finite and positive")
    rng = random.Random(seed)
    a, b = _load_matrices()
    p = initial_permutation()
    best_score = _score(a, b, p)
    checks = 0
    iterations = 0
    for _attempt in search_steps(ITERATION_LIMIT):
        r = rng.randrange(N)
        s = rng.randrange(N - 1)
        if s >= r:
            s += 1
        delta = _swap_delta(a, b, p, r, s)
        checks += 1
        if delta >= 0:
            continue
        p[r], p[s] = p[s], p[r]
        best_score += delta
        iterations += 1
    budget = {
        "mode": "wall_clock_cutoff" if seconds is not None else "fixed_iteration_count",
        "requested_checks": ITERATION_LIMIT,
        "actual_checks": checks,
        "requested_wall_clock_seconds": seconds,
        "effective_wall_clock_seconds": None if seconds is None else min(240.0, seconds),
    }
    return {"permutation": p, "search_metadata": {"seed": seed, "pair_checks": checks,
            "iterations": iterations, "budget": budget,
            "algorithm": "randomized first-improvement pair-swap local search", "reported_score": best_score}}
