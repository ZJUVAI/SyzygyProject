"""Traditional fixed-seed local search over rational Fourier perturbations."""
from __future__ import annotations

import os
import random
from fractions import Fraction

from tasks.t096.check import CONFIG_ID, validate
from tasks.t096.construction import circle, oval

_CONFIG = {
    "id": CONFIG_ID,
    "direction": "minimize",
    "parameters": {
        "dimension": 2,
        "curve_class": "smooth strictly convex simple closed plane curves",
        "length": "2*pi",
        "objective": "minimize joint Rayleigh quotient over curve and nonzero periodic trial function",
    },
}


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID) != CONFIG_ID:
        raise ValueError("unknown T096 configuration")
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    incumbent = circle()
    incumbent_score = Fraction(validate(incumbent, _CONFIG)["objective"])
    # 24 deterministic random perturbations around the circular candidate.
    for _ in range(24):
        denominator = rng.choice((4, 8, 16, 32))
        epsilon = Fraction(rng.randint(1, denominator-1), denominator)
        alpha = Fraction(rng.randint(-3, 3), 8)
        beta = Fraction(rng.randint(-3, 3), 8)
        candidate = oval(epsilon, alpha, beta, terms=18)
        score = Fraction(validate(candidate, _CONFIG)["objective"])
        if score < incumbent_score:
            incumbent, incumbent_score = candidate, score
    return incumbent
