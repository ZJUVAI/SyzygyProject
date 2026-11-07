"""Seeded randomized reverse-Cuthill-McKee starts with adjacent-swap descent."""

import os
import random
import time

from tasks.t045.graph import load_graph


def _adjacency(n, edges):
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    return adjacency


def _randomized_rcm(adjacency, rng):
    n = len(adjacency)
    degrees = [len(neighbors) for neighbors in adjacency]
    unseen = set(range(n))
    order = []
    while unseen:
        min_degree = min(degrees[v] for v in unseen)
        roots = [v for v in unseen if degrees[v] == min_degree]
        root = rng.choice(roots)
        unseen.remove(root)
        queue = [root]
        cursor = 0
        while cursor < len(queue):
            vertex = queue[cursor]
            cursor += 1
            order.append(vertex)
            neighbors = [v for v in adjacency[vertex] if v in unseen]
            rng.shuffle(neighbors)
            neighbors.sort(key=lambda v: degrees[v])
            for neighbor in neighbors:
                unseen.remove(neighbor)
                queue.append(neighbor)
    return [v + 1 for v in reversed(order)]


def _descent(ordering, adjacency, sweep_limit):
    order = list(ordering)
    n = len(order)
    position = [0] * (n + 1)
    for index, vertex in enumerate(order, start=1):
        position[vertex] = index
    sweep_improvements = []
    for _ in range(sweep_limit):
        accepted = 0
        for i in range(n - 1):
            left, right = order[i], order[i + 1]
            delta = 0
            for neighbor0 in adjacency[left - 1]:
                neighbor = neighbor0 + 1
                if neighbor != right:
                    delta += abs(i + 2 - position[neighbor]) - abs(i + 1 - position[neighbor])
            for neighbor0 in adjacency[right - 1]:
                neighbor = neighbor0 + 1
                if neighbor != left:
                    delta += abs(i + 1 - position[neighbor]) - abs(i + 2 - position[neighbor])
            if delta < 0:
                order[i], order[i + 1] = right, left
                position[left], position[right] = i + 2, i + 1
                accepted += 1
        sweep_improvements.append(accepted)
        if accepted == 0:
            break
    return order, sweep_improvements


def _score(ordering, edges):
    position = [0] * (len(ordering) + 1)
    for index, vertex in enumerate(ordering, start=1):
        position[vertex] = index
    return sum(abs(position[u + 1] - position[v + 1]) for u, v in edges)


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T045-C01") != "T045-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(1000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "8"))))
    sweep_limit = max(1, min(100, int(os.environ.get("MATHBENCH_ADJACENT_SWEEPS", "12"))))
    from mathbench.search import search_steps

    start = time.monotonic()
    n, edges = load_graph()
    adjacency = _adjacency(n, edges)
    rng = random.Random(seed)
    best_order, best_score, best_iteration = None, None, None
    sweep_counts = []
    iterations_run = 0
    for iteration in search_steps(iterations):
        candidate = _randomized_rcm(adjacency, rng)
        candidate, improvements = _descent(candidate, adjacency, sweep_limit)
        score = _score(candidate, edges)
        iterations_run += 1
        sweep_counts.append(len(improvements))
        if best_score is None or score < best_score:
            best_order, best_score, best_iteration = candidate, score, iteration
    if best_order is None:
        best_order = list(range(1, n + 1))
        best_score = _score(best_order, edges)
    return {
        "ordering": best_order,
        "search_metadata": {
            "algorithm": "seeded randomized RCM construction plus adjacent-swap descent",
            "seed": seed,
            "iterations_requested": iterations,
            "iterations_run": iterations_run,
            "best_iteration": best_iteration,
            "adjacent_sweep_limit": sweep_limit,
            "sweeps_per_iteration": sweep_counts,
            "candidate_objective_recomputed": best_score,
            "generation_seconds": time.monotonic() - start,
            "budget": {"mode": "fixed_iterations unless MATHBENCH_SEARCH_SECONDS is set",
                       "runner_generation_seconds": 300},
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
