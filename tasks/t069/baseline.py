"""Spatial-order and bounded random 2-opt baseline for T069."""

import math
import os
import random
import time

from tasks.t069.check import CONFIG_ID, load_points, edge_length, tour_length


DEFAULT_2OPT_STEPS = 20_000


def _spatial_tour(points):
    # Sweep 100-unit horizontal bands; reverse alternate bands to join their ends.
    order = sorted(range(len(points)), key=lambda i: (points[i][1] // 100, points[i][0], i))
    tour = []
    start = 0
    while start < len(order):
        band = points[order[start]][1] // 100
        end = start + 1
        while end < len(order) and points[order[end]][1] // 100 == band:
            end += 1
        row = order[start:end]
        if band & 1:
            row.reverse()
        tour.extend(row)
        start = end
    return tour


def _two_opt(points, tour, steps, seed, deadline=None):
    rng = random.Random(seed)
    n = len(tour)
    score = tour_length(points, tour)
    completed = accepted = 0
    for _ in range(steps):
        if deadline is not None and time.monotonic() >= deadline:
            break
        i = rng.randrange(n - 2)
        j = rng.randrange(i + 2, min(n, i + 51))
        a, b = tour[i], tour[i + 1]
        c, d = tour[j], tour[(j + 1) % n]
        old = edge_length(points, a, b) + edge_length(points, c, d)
        new = edge_length(points, a, c) + edge_length(points, b, d)
        completed += 1
        if new < old:
            tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
            score += new - old
            accepted += 1
    return score, completed, accepted


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen}")
    try:
        seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    except ValueError as exc:
        raise ValueError("MATHBENCH_SEED must be an integer") from exc
    seconds_text = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None
    if seconds_text is not None:
        try:
            seconds = float(seconds_text)
        except ValueError as exc:
            raise ValueError("search seconds must be numeric") from exc
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + seconds
    points = load_points()
    tour = _spatial_tour(points)
    steps = DEFAULT_2OPT_STEPS
    score, completed, accepted = _two_opt(points, tour, steps, seed, deadline)
    return {
        "tour": tour,
        "search_metadata": {
            "algorithm": "100-unit horizontal spatial bands with alternating direction, followed by local random 2-opt exchanges",
            "seed": seed,
            "two_opt_step_limit": steps,
            "two_opt_steps_completed": completed,
            "accepted_exchanges": accepted,
            "computed_objective": score,
            "reference_data_read": False,
            "search_seconds_cutoff": seconds_text,
        },
    }
