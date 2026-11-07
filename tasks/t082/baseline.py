"""Seeded repeated greedy construction, starting from a simple placement."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t082.construction import greedy_layout


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T082-C01") != "T082-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    restarts = max(1, min(100, int(os.environ.get("MATHBENCH_BASELINE_ITERATIONS", "12"))))
    rng = random.Random(seed ^ 0x119BA5E)
    best = {"white": [[0, 0]], "black": [[1, 2]]}
    completed = 0
    start = time.monotonic()
    for _ in search_steps(restarts):
        candidate = greedy_layout(rng, max_army=45)
        if len(candidate["white"]) > len(best["white"]):
            best = candidate
        completed += 1
    return {
        **best,
        "search_metadata": {
            "algorithm": "seeded randomized greedy pair extension with independent restarts",
            "seed": seed,
            "restarts_requested": restarts,
            "restarts_run": completed,
            "generation_seconds": time.monotonic() - start,
            "budget": "fixed restarts unless MATHBENCH_SEARCH_SECONDS sets a wall-clock cutoff; runner cap 300 seconds",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
