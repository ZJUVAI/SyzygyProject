"""Bounded GRASP-style local search, independent of comparison witnesses."""

import math
import os
import time

from tasks.t088.check import CONFIG_ID
from tasks.t088.heuristics import randomized_method
from tasks.t088.instance import load_graph


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    trials = int(os.environ.get("T088_SEARCH_TRIALS", "6"))
    vertex_trials = int(os.environ.get("T088_INSERTION_VERTEX_TRIALS", "12"))
    if trials < 0 or vertex_trials < 0 or vertex_trials > 130:
        raise ValueError("search counts are outside their valid ranges")
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None
    if seconds is not None:
        duration = float(seconds)
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + duration
    edges = load_graph()
    order = list(range(1, 131))
    metadata = {
        "algorithm": "reconstructed GRASP-style construction with bounded insertion local search",
        "seed": seed,
        "trial_limit": trials,
        "trials_completed": 0,
        "insertion_moves_scored": 0,
        "insertion_moves_accepted": 0,
        "reference_data_read": False,
    }
    best_value = None
    import random

    rng = random.Random(seed)
    for _ in range(trials):
        if deadline is not None and time.monotonic() >= deadline:
            break
        from tasks.t088.heuristics import grasp_order, insertion_descent

        order_candidate = grasp_order(edges, rng)
        order_candidate, local_meta = insertion_descent(
            order_candidate, edges, rng, vertex_trials=vertex_trials
        )
        from tasks.t088.instance import cutwidth

        value = cutwidth(order_candidate, edges)
        metadata["trials_completed"] += 1
        metadata["insertion_moves_scored"] += local_meta["insertion_moves_scored"]
        metadata["insertion_moves_accepted"] += local_meta["insertion_moves_accepted"]
        if best_value is None or value < best_value:
            order, best_value = order_candidate, value
    metadata["time_cutoff_enabled"] = deadline is not None
    return {"ordering": order, "search_metadata": metadata}
