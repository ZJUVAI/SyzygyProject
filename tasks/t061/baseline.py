"""Fixed-seed randomized order greedy search for maximal C6-free graphs."""

import math
import os
import random
import time

from tasks.t061.check import CONFIG_ID
from tasks.t061.graph_alg import greedy_saturated, shuffled_edge_order


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    trials = int(os.environ.get("T061_SEARCH_TRIALS", "4"))
    if trials < 0:
        raise ValueError("trial count must be nonnegative")
    seconds_text = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    if seconds_text is None:
        deadline = None
    else:
        seconds = float(seconds_text)
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + seconds

    rng = random.Random(seed)
    incumbent = {"vertices": 100, "edges": []}
    completed = 0
    for _ in range(trials):
        if deadline is not None and time.monotonic() >= deadline:
            break
        graph = greedy_saturated(shuffled_edge_order(rng))
        completed += 1
        if len(graph["edges"]) < len(incumbent["edges"]) or not incumbent["edges"]:
            incumbent = graph
    return {
        **incumbent,
        "search": {
            "algorithm": "randomized edge-order greedy; add an edge only when it creates no simple C6",
            "seed": seed,
            "trial_limit": trials,
            "trials_completed": completed,
            "reference_data_read": False,
        },
    }
