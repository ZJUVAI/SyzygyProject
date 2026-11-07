"""Deterministic fixed-seed greedy search for large independent sets."""

import math
import os
import random
import time

from tasks.t062.check import CONFIG_ID, N


def _greedy(order):
    chosen = set()
    for value in order:
        if all(value - k * k not in chosen and value + k * k not in chosen
               for k in range(1, math.isqrt(N) + 1)):
            chosen.add(value)
    return {"elements": sorted(chosen)}


def run_code():
    chosen_config = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen_config != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen_config}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    trials = int(os.environ.get("T062_SEARCH_TRIALS", "3"))
    if trials < 0:
        raise ValueError("trial count must be nonnegative")
    seconds_text = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None
    if seconds_text is not None:
        seconds = float(seconds_text)
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + seconds

    best = _greedy(range(1, N + 1))
    rng = random.Random(seed)
    completed = 0
    for _ in range(trials):
        if deadline is not None and time.monotonic() >= deadline:
            break
        order = list(range(1, N + 1))
        rng.shuffle(order)
        candidate = _greedy(order)
        completed += 1
        if len(candidate["elements"]) > len(best["elements"]):
            best = candidate
    return {
        **best,
        "search": {
            "algorithm": "ascending greedy incumbent plus fixed-seed random-order greedy",
            "seed": seed,
            "trial_limit": trials,
            "trials_completed": completed,
            "reference_data_read": False,
        },
    }
