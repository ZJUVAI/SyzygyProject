"""Bounded seeded search over short self-Fourier Hermite combinations."""

from __future__ import annotations

import os
import random

import numpy as np


def _hermite_mode_in_t(j):
    """Monic H_(4j)(sqrt(2t)) as ascending rational coefficients."""
    n = 4 * j
    coefficients = [0] * (2 * j + 1)
    # H_n(x)=n! sum_r (-1)^r (2x)^(n-2r)/(r!(n-2r)!).
    # For n=4j and x^2=2t, put m=2j-r.
    leading = 2 ** (6 * j)
    import math

    for m in range(2 * j + 1):
        r = 2 * j - m
        numerator = math.factorial(n) * (-1) ** r * 8**m
        denominator = math.factorial(r) * math.factorial(2 * m) * leading
        from fractions import Fraction

        coefficients[m] = Fraction(numerator, denominator)
    return coefficients


def _candidate(rng):
    from fractions import Fraction

    h4 = _hermite_mode_in_t(1)
    h8 = _hermite_mode_in_t(2)
    scale4 = Fraction(rng.randint(-300, 300), 100)
    scale8 = Fraction(rng.randint(1, 120), 100)
    epsilon = Fraction(rng.randint(1, 1000), 1000)
    degree = max(len(h4), len(h8))
    values = [Fraction(0)] * degree
    for i, value in enumerate(h4):
        values[i] += scale4 * value
    for i, value in enumerate(h8):
        values[i] += scale8 * value
    # The H0 coefficient is selected so p(0)=-epsilon. All modes used here
    # have Fourier eigenvalue +1, so q=p and q(0)<0 as well.
    # Add the required H0 eigenmode by choosing the constant term directly.
    values[0] = -epsilon
    return values


def _approximate_last_root(coefficients):
    array = np.asarray([float(x) for x in coefficients[::-1]], dtype=np.float64)
    roots = np.roots(array)
    positive = [float(root.real) for root in roots
                if abs(float(root.imag)) < 1e-7 and float(root.real) > 0]
    if not positive:
        return float("inf")
    return max(positive)


def run_search(seed=0, steps=100):
    rng = random.Random(seed)
    best = None
    best_root = float("inf")
    for _ in range(steps):
        candidate = _candidate(rng)
        # The highest Hermite mode has a positive coefficient, so the tail
        # is positive. Fast roots guide the search; check.py certifies exactly.
        root = _approximate_last_root(candidate)
        if root < best_root:
            best, best_root = candidate, root
    if best is None or not np.isfinite(best_root):
        best = _candidate(random.Random(seed + 1))
    return best, {"search_steps": steps, "approximate_tail_root": best_root,
                  "random_seed": seed,
                  "search_method": "fixed-step seeded random Hermite coefficient search; exact final root isolation"}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T089-C01")
    if config_id != "T089-C01":
        raise ValueError(f"unknown T089 configuration: {config_id}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    coefficients, metadata = run_search(seed=seed, steps=80)
    return {"coefficients": [str(value) for value in coefficients], **metadata}
