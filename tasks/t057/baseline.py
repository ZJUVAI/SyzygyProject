"""Bounded multistart Clarke-Wright search with randomized savings ties."""

import math
import os
import random
import time

from tasks.t057.check import CONFIG_ID
from tasks.t057.heuristics import clarke_wright
from tasks.t057.instance import load_instance, total_route_cost


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    trials = int(os.environ.get("T057_SEARCH_TRIALS", "6"))
    if trials < 0:
        raise ValueError("search trial count must be nonnegative")
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    if seconds is None:
        deadline = None
    else:
        duration = float(seconds)
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + duration

    instance = load_instance()
    best_routes = [[customer] for customer in instance["customer_ids"]]
    best_cost = total_route_cost(best_routes, instance)
    rng = random.Random(seed)
    completed = 0
    all_merges = 0
    for _ in range(trials):
        if deadline is not None and time.monotonic() >= deadline:
            break
        routes, meta = clarke_wright(instance, rng=rng)
        cost = total_route_cost(routes, instance)
        completed += 1
        all_merges += meta["merges"]
        if cost < best_cost:
            best_routes, best_cost = routes, cost
    return {
        "routes": best_routes,
        "search": {
            "algorithm": "Clarke-Wright capacity-feasible route merging with randomized equal-savings tie order",
            "seed": seed,
            "trial_limit": trials,
            "trials_completed": completed,
            "total_merges_over_trials": all_merges,
            "reference_data_read": False,
        },
    }
