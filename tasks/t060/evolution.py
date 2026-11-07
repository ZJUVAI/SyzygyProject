"""Seeded mixed-radix Horner search; no reference or human witness is read."""
import os
import random

from mathbench.search import search_steps

TARGET = 2**61 - 1
ITERATION_LIMIT = 1000
RADICES = (2, 3, 4, 5, 6, 7, 8)


def _ones(count):
    return "+".join(["1"] * count)


def _candidate(rng):
    # Random mixed bases are selected from low to high significance. Converting
    # by successive divmod gives an exact mixed-radix expansion of the target.
    digits = []
    radices = []
    remaining = TARGET
    while remaining:
        radix = rng.choice(RADICES)
        remaining, digit = divmod(remaining, radix)
        digits.append(digit)
        radices.append(radix)
    digits.reverse()
    radices.reverse()
    expression = f"({_ones(digits[0])})"
    for radix, digit in zip(radices[1:], digits[1:]):
        expression = f"(({expression})*({_ones(radix)}))"
        if digit:
            expression = f"({expression}+({_ones(digit)}))"
    return expression


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T060-C01") != "T060-C01":
        raise ValueError("unsupported T060 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    rng = random.Random(seed)
    iterator = iter(search_steps(ITERATION_LIMIT))
    best = None
    best_count = None
    actual = 0
    while next(iterator, None) is not None:
        expression = _candidate(rng)
        count = expression.count("1")
        actual += 1
        if best_count is None or count < best_count:
            best, best_count = expression, count
    if best is None:
        # A zero-second exploration still returns a valid cold-start result.
        from tasks.t060.init_program import run_code as init_run
        best = init_run()["expression"]
        best_count = best.count("1")
    return {
        "expression": best,
        "search_metadata": {
            "algorithm": "seeded random mixed-radix Horner enumeration",
            "seed": seed,
            "iterations": actual,
            "iteration_limit": ITERATION_LIMIT,
            "best_ones": best_count,
            "radix_set": list(RADICES),
            "reference_data_read": False,
            "budget": {
                "mode": "wall_clock_cutoff" if seconds is not None else "fixed_iteration_count",
                "requested_iterations": ITERATION_LIMIT,
                "actual_iterations": actual,
                "requested_wall_clock_seconds": seconds,
            },
        },
    }
