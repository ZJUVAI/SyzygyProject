"""Fixed-restart simulated annealing with exact periodic energy updates."""

import math
import os
import random
import time

from tasks.t090.check import CONFIG_ID
from tasks.t090.heuristics import anneal, energy, correlations


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    trials = int(os.environ.get("T090_SEARCH_TRIALS", "4"))
    steps = int(os.environ.get("T090_ANNEAL_STEPS", "5000"))
    if trials < 0 or steps < 0:
        raise ValueError("search counts must be nonnegative")
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None
    if seconds is not None:
        duration = float(seconds)
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + duration
    rng = random.Random(seed)
    best = [1] * 64
    best_energy = energy(correlations(best))
    completed = 0
    for _ in range(trials):
        if deadline is not None and time.monotonic() >= deadline:
            break
        start = [rng.choice((-1, 1)) for _ in range(64)]
        candidate, candidate_energy = anneal(start, rng, steps=steps)
        completed += 1
        if candidate_energy < best_energy:
            best, best_energy = candidate, candidate_energy
    return {
        "sequence": best,
        "search_metadata": {
            "algorithm": "seeded multistart single-spin simulated annealing with exact correlation deltas and one-bit descent",
            "seed": seed,
            "trial_limit": trials,
            "steps_per_trial": steps,
            "trials_completed": completed,
            "reference_data_read": False,
            "time_cutoff_enabled": deadline is not None,
        },
    }
