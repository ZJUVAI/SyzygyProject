"""Simple deterministic grid seed for each staged T001 configuration."""
import os
from fractions import Fraction

_N = {"T001-C01": 26, "T001-C02": 32, "T001-C03": 50}


def run_code():
    # EVOLVE-BLOCK-START
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T001-C01")
    n = _N[cid]
    cols = math_ceil_sqrt(n)
    rows = (n + cols - 1) // cols
    radius = min(Fraction(1, 2*cols), Fraction(1, 2*rows))
    centers = [[str(Fraction(2*col+1, 2*cols)), str(Fraction(2*row+1, 2*rows))]
               for row in range(rows) for col in range(cols)][:n]
    # EVOLVE-BLOCK-END
    return {"radius": str(radius), "centers": centers}


def math_ceil_sqrt(n):
    k = 1
    while k*k < n:
        k += 1
    return k
