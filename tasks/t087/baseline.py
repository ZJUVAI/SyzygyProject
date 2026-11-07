"""Fixed-step random-restart-free local search using fast numeric feedback."""

import os
import random

import numpy as np

N = 480
D = 13.0 / 4800.0
END_K = 369
END_PART = 3.0 / 13.0


def _score(heights):
    array = np.asarray(heights, dtype=np.float64)
    sums = np.correlate(array, array, mode="full")[N - 1:]
    value_at_one = (1.0 - END_PART) * sums[END_K] + END_PART * sums[END_K + 1]
    return min(float(np.min(sums[:END_K + 1])), float(value_at_one)) / (D * float(np.sum(array)) ** 2)


def run_search(seed, steps=400, start=None):
    rng = random.Random(seed)
    current = list(start) if start is not None else [1] * N
    current_score = _score(current)
    best, best_score = current[:], current_score
    accepted = 0
    for iteration in range(steps):
        trial = current[:]
        left = rng.randrange(N)
        width = rng.randint(1, 14)
        for j in range(left, min(N, left + width)):
            if rng.random() < 0.7:
                trial[j] = max(0, min(120, trial[j] + rng.choice((-3, -2, -1, 1, 2, 3))))
            else:
                trial[j] = rng.randrange(0, 13)
        if not any(trial):
            continue
        score = _score(trial)
        if score > best_score:
            best, best_score = trial[:], score
        temperature = 0.0015 * (1.0 - iteration / max(1, steps))
        if score >= current_score or rng.random() < temperature:
            current, current_score = trial, score
            accepted += 1
    return best, {"search_iterations": steps, "accepted_moves": accepted,
                  "numeric_search_score": best_score}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T087-C01")
    if config_id != "T087-C01":
        raise ValueError(f"unknown T087 configuration: {config_id}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    heights, info = run_search(seed)
    return {"heights": heights, "search_method": "seeded block mutation with exact final checking",
            "random_seed": seed, **info}
