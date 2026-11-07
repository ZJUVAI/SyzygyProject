"""Seeded simulated annealing with vertex-swap moves for the MinLA objective."""

import math
import os
import random
import time

from tasks.t045.graph import load_graph


def _cost(ordering, edges):
    pos = [0] * (len(ordering) + 1)
    for i, vertex in enumerate(ordering, start=1):
        pos[vertex] = i
    return sum(abs(pos[u + 1] - pos[v + 1]) for u, v in edges), pos


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T045-C01") != "T045-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    steps = max(1, min(2_000_000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "100000"))))
    from mathbench.search import search_deadline
    deadline = search_deadline()
    from tasks.t045.baseline import _adjacency, run_code as baseline_run
    start = time.monotonic()
    n, edges = load_graph()
    adjacency = _adjacency(n, edges)
    incumbent = baseline_run()
    order = incumbent["ordering"][:]
    current_cost, position = _cost(order, edges)
    best_order, best_cost = order[:], current_cost
    rng = random.Random(seed ^ 0x10896A)
    accepted = 0
    iterations_run = 0
    for step in range(steps):
        if time.monotonic() >= deadline:
            break
        iterations_run += 1
        i = rng.randrange(n)
        j = rng.randrange(n - 1)
        if j >= i:
            j += 1
        a, b = order[i], order[j]
        delta = 0
        for neighbor0 in adjacency[a - 1]:
            neighbor = neighbor0 + 1
            if neighbor != b:
                delta += abs((j + 1) - position[neighbor]) - abs((i + 1) - position[neighbor])
        for neighbor0 in adjacency[b - 1]:
            neighbor = neighbor0 + 1
            if neighbor != a:
                delta += abs((i + 1) - position[neighbor]) - abs((j + 1) - position[neighbor])
        fraction = step / max(1, steps - 1)
        temperature = 1200.0 * (1.0 - fraction) + 20.0
        if delta <= 0 or rng.random() < math.exp(-delta / temperature):
            order[i], order[j] = b, a
            position[a], position[b] = j + 1, i + 1
            current_cost += delta
            accepted += 1
            if current_cost < best_cost:
                best_order, best_cost = order[:], current_cost
    return {
        "ordering": best_order,
        "search_metadata": {
            "algorithm": "randomized RCM incumbent and simulated annealing with vertex-swap neighborhood",
            "seed": seed,
            "iterations_requested": steps,
            "iterations_run": iterations_run,
            "accepted_moves": accepted,
            "objective_recomputed": best_cost,
            "generation_seconds": time.monotonic() - start,
            "budget": {"fixed_iteration_limit": steps, "runner_generation_seconds": 300},
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
