"""Seeded finite mutation search from the circle, with exact candidate ranking."""
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
    epsilons = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(3, 8))
    coefficients = tuple(Fraction(k, 8) for k in range(-4, 5))
    # Each mutation changes curvature radius or the trial function. There are 32 fixed steps.
    for _ in range(32):
        candidate = oval(rng.choice(epsilons), rng.choice(coefficients),
                         rng.choice(coefficients), terms=18)
        score = Fraction(validate(candidate, _CONFIG)["objective"])
        if score < incumbent_score:
            incumbent, incumbent_score = candidate, score
    return incumbent
