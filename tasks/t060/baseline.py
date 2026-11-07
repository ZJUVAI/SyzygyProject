"""Deterministic radix-Horner search from the target; reads no comparison data."""
import os

from mathbench.search import search_steps

TARGET = 2**61 - 1
RADICES = tuple(range(2, 17))
ITERATION_LIMIT = len(RADICES)


def _ones(count):
    return "+".join(["1"] * count)


def _radix_expression(target, radix):
    digits = []
    while target:
        target, digit = divmod(target, radix)
        digits.append(digit)
    digits.reverse()
    expression = f"({_ones(digits[0])})"
    for digit in digits[1:]:
        expression = f"(({expression})*({_ones(radix)}))"
        if digit:
            expression = f"({expression}+({_ones(digit)}))"
    return expression


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T060-C01") != "T060-C01":
        raise ValueError("unsupported T060 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    iterator = iter(search_steps(ITERATION_LIMIT))
    best = None
    best_count = None
    actual = 0
    for radix in RADICES:
        if next(iterator, None) is None:
            break
        expression = _radix_expression(TARGET, radix)
        count = expression.count("1")
        actual += 1
        if best_count is None or count < best_count:
            best, best_count = expression, count
    if best is None:
        best = _radix_expression(TARGET, 2)
        best_count = best.count("1")
    return {
        "expression": best,
        "search_metadata": {
            "algorithm": "exhaustive uniform-radix Horner candidates",
            "tested_radices": list(RADICES[:actual]),
            "seed": seed,
            "iterations": actual,
            "iteration_limit": ITERATION_LIMIT,
            "reference_data_read": False,
            "budget": {
                "mode": "wall_clock_cutoff" if seconds is not None else "fixed_iteration_count",
                "requested_iterations": ITERATION_LIMIT,
                "actual_iterations": actual,
                "requested_wall_clock_seconds": seconds,
            },
        },
    }
