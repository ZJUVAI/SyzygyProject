"""Seeded isotopy search that retains its best valid MOLS family."""
import os
import random
import time


def _cyclic():
    return [[(r + c) % 12 for c in range(12)] for r in range(12)]


def _is_orthogonal(a, b):
    return len({(a[r][c], b[r][c]) for r in range(12) for c in range(12)}) == 144


def _random_isotope(rng):
    rows, cols, symbols = (list(range(12)) for _ in range(3))
    rng.shuffle(rows)
    rng.shuffle(cols)
    rng.shuffle(symbols)
    base = _cyclic()
    return [[symbols[base[rows[r]][cols[c]]] for c in range(12)] for r in range(12)]


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T038-C01") != "T038-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(10000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "64"))))
    rng = random.Random(seed)
    from tasks.t038.baseline import run_code as baseline_run
    incumbent = baseline_run()["squares"]
    started = time.monotonic()
    attempts = 0
    for _ in range(iterations):
        candidate = _random_isotope(rng)
        attempts += 1
        if all(_is_orthogonal(candidate, square) for square in incumbent):
            incumbent.append(candidate)
    return {
        "squares": incumbent,
        "objective": len(incumbent),
        "search_metadata": {
            "algorithm": "seeded random isotopy augmentation of the MacNeish incumbent",
            "seed": seed,
            "iterations_requested": iterations,
            "iterations_run": attempts,
            "generation_seconds": time.monotonic() - started,
            "budget": {
                "mode": "fixed_iterations",
                "iteration_limit": iterations,
                "runner_generation_limit_seconds": 300,
            },
        },
    }
