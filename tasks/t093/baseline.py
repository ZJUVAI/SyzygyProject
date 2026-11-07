"""Bounded random greedy placement search; it reads only the public instance."""

import math
import os
import random
import time

from tasks.t093.check import CONFIG_ID, PARAMETERS, placement_geometry
from tasks.t093.instance import load_instance, polygon_bbox


CONFIG = {"id": CONFIG_ID, "parameters": PARAMETERS, "direction": "maximize"}


def _greedy_trial(data, rng, attempts_per_copy, deadline):
    copies = []
    for item_id, item in enumerate(data["items"]):
        area2 = abs(sum(a[0] * b[1] - b[0] * a[1]
                        for a, b in zip(item["polygon"], item["polygon"][1:] + item["polygon"][:1])))
        density = item["value"] / area2
        copies.extend((density, rng.random(), item_id) for _ in range(item["quantity"]))
    copies.sort(reverse=True)
    solution = {"item_indices": [], "x_translations": [], "y_translations": []}
    placed_geometries = []
    value = 0
    attempted = 0
    placed = 0
    container_x0, container_y0, container_x1, container_y1 = polygon_bbox(data["container"])
    for _, _, item_id in copies:
        if deadline is not None and time.monotonic() >= deadline:
            break
        item = data["items"][item_id]
        item_x0, item_y0, item_x1, item_y1 = polygon_bbox(item["polygon"])
        lo_x = container_x0 - item_x0
        hi_x = container_x1 - item_x1
        lo_y = container_y0 - item_y0
        hi_y = container_y1 - item_y1
        if lo_x > hi_x or lo_y > hi_y:
            continue
        for _ in range(attempts_per_copy):
            if deadline is not None and time.monotonic() >= deadline:
                break
            dx = rng.randint(lo_x, hi_x)
            dy = rng.randint(lo_y, hi_y)
            attempted += 1
            geometry = placement_geometry(item_id, dx, dy, placed_geometries, data)
            if geometry is not None:
                solution["item_indices"].append(item_id)
                solution["x_translations"].append(dx)
                solution["y_translations"].append(dy)
                placed_geometries.append(geometry)
                value += item["value"]
                placed += 1
                break
    return solution, value, attempted, placed


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    trials = int(os.environ.get("T093_TRIALS", "3"))
    attempts = int(os.environ.get("T093_PLACEMENT_TRIES", "30"))
    if trials < 0 or attempts < 0:
        raise ValueError("search counts must be nonnegative")
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None
    if seconds is not None:
        duration = float(seconds)
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + duration
    data = load_instance()
    rng = random.Random(seed)
    best = {"item_indices": [], "x_translations": [], "y_translations": []}
    best_value = 0
    completed = 0
    candidate_attempts = 0
    placements_found = 0
    for _ in range(trials):
        if deadline is not None and time.monotonic() >= deadline:
            break
        candidate, value, attempted, placed = _greedy_trial(data, rng, attempts, deadline)
        completed += 1
        candidate_attempts += attempted
        placements_found += placed
        if value > best_value:
            best, best_value = candidate, value
    return {
        **best,
        "search_metadata": {
            "algorithm": "value-density ordered random first-fit translations; exact geometric feasibility kernel checks each proposal",
            "seed": seed,
            "trial_limit": trials,
            "trials_completed": completed,
            "placement_attempt_limit_per_copy": attempts,
            "placement_attempts": candidate_attempts,
            "placements_found_across_trials": placements_found,
            "reference_data_read": False,
            "time_cutoff_enabled": deadline is not None,
        },
    }
