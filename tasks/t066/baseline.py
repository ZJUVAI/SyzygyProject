"""Fixed-seed random search over integer-grid point sets."""

import math
import os
import random
import time
from math import gcd


CONFIG_ID = "T066-C01"
POINT_COUNT = 17
GRID = [(x, y) for x in range(-6, 7) for y in range(-6, 7)]
ITERATION_LIMIT = 96


def _line_key(p, q):
    x1, y1 = p
    x2, y2 = q
    a, b, c = y1 - y2, x2 - x1, x1 * y2 - x2 * y1
    divisor = gcd(gcd(abs(a), abs(b)), abs(c))
    a, b, c = a // divisor, b // divisor, c // divisor
    if next(value for value in (a, b, c) if value) < 0:
        a, b, c = -a, -b, -c
    return a, b, c


def _score(points):
    lines = {_line_key(points[i], points[j]) for i in range(len(points)) for j in range(i)}
    exactly_three = 0
    for a, b, c in lines:
        incidence = sum(a * x + b * y + c == 0 for x, y in points)
        exactly_three += incidence == 3
    return exactly_three


def _encode(points):
    return {
        "minimal_polynomial": [0, 1],
        "isolating_interval": ["-1", "1"],
        "points": [{"x": [x], "y": [y]} for x, y in points],
    }


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    seconds_text = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None
    if seconds_text is not None:
        seconds = float(seconds_text)
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + seconds

    incumbent = [(i, i * i) for i in range(POINT_COUNT)]
    incumbent_score = _score(incumbent)
    iterations = 0
    for _ in range(ITERATION_LIMIT):
        if deadline is not None and time.monotonic() >= deadline:
            break
        candidate = rng.sample(GRID, POINT_COUNT)
        score = _score(candidate)
        iterations += 1
        if score > incumbent_score:
            incumbent, incumbent_score = candidate, score
    return {
        **_encode(incumbent),
        "search_metadata": {
            "algorithm": "fixed-seed random sampling of 17-point subsets of the integer 13x13 grid",
            "seed": seed,
            "iteration_limit": ITERATION_LIMIT,
            "iterations": iterations,
            "reference_data_read": False,
            "search_seconds_cutoff": seconds_text,
        },
    }
