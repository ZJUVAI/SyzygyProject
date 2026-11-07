"""Rebuild the traditional highest-weight real spherical harmonic Re((x+i y)^20)."""
import os
import math

DEGREE = 20
EXPONENTS = [(a, b, DEGREE - a - b) for a in range(DEGREE, -1, -1) for b in range(DEGREE - a, -1, -1)]


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T092-C01") != "T092-C01":
        raise ValueError("unsupported configuration")
    coefficients = []
    for a, b, c in EXPONENTS:
        value = 0
        if c == 0 and b % 2 == 0:
            j = b // 2
            value = (-1) ** j * math.comb(20, b)
        coefficients.append(value)
    return {"coefficients": coefficients}
