"""Small traditional factor-exponent search, evaluated on a fixed dyadic grid."""

import math
import os
import random
import time


DEGREE = 146
ITERATION_LIMIT = 74


def _coefficients(a, b):
    """Return x^a(1-x)^a(2x-1)^b in low-to-high power order."""
    result = [0] * (2 * a + b + 1)
    for j in range(a + 1):
        for k in range(b + 1):
            result[a + j + k] += (
                (-1) ** (j + b - k)
                * math.comb(a, j)
                * math.comb(b, k)
                * 2**k
            )
    return result


def _sample_norm(a, b):
    best = 0.0
    denominator = 512
    for i in range(denominator + 1):
        x = i / denominator
        value = (x * (1.0 - x)) ** a * abs(2.0 * x - 1.0) ** b
        if value > best:
            best = value
    return best


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T046-C01")
    if config_id != "T046-C01":
        raise ValueError(f"unsupported configuration: {config_id}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    start = time.monotonic()
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None if seconds is None else start + max(0.0, float(seconds))
    candidates = [(a, DEGREE - 2 * a) for a in range(DEGREE // 2, -1, -1)]
    rng.shuffle(candidates)
    incumbent = (0, DEGREE)
    incumbent_value = 1.0  # x^146 is the simple search seed, not comparison data.
    iterations = 0
    for a, b in candidates:
        if deadline is not None and time.monotonic() >= deadline:
            break
        value = _sample_norm(a, b)
        iterations += 1
        if value < incumbent_value:
            incumbent, incumbent_value = (a, b), value
    a, b = incumbent
    chosen = _coefficients(a, b) if iterations else [0] * DEGREE + [1]
    return {
        "coefficients": chosen,
        "search_metadata": {
            "algorithm": "enumerate h1^a h2^b with 2a+b=146; rank by 513-point dyadic sample",
            "seed": seed,
            "iteration_limit": ITERATION_LIMIT,
            "iterations": iterations,
            "budget": {"iteration_limit": ITERATION_LIMIT},
            "reference_data_read": False,
            "selected_exponents": (
                {"h1_x_1_minus_x": a, "h2_2x_minus_1": b}
                if iterations > 0 else None
            ),
            "search_seconds_cutoff": seconds,
        },
    }
