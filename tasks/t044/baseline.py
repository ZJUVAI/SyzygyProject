"""Seeded search over random simple cubic graphs, without comparison data."""

from collections import deque
import os
import random

from mathbench.search import search_steps


CONFIG_ID = "T044-C01"
ATTEMPT_LIMIT = 384
ORDER_CHOICES = tuple(range(14, 95, 2))


def _random_cubic_graph(order, rng):
    stubs = [vertex for vertex in range(order) for _ in range(3)]
    rng.shuffle(stubs)
    edges = set()
    adjacency = [set() for _ in range(order)]
    for index in range(0, len(stubs), 2):
        left, right = stubs[index : index + 2]
        if left == right:
            return None
        edge = (min(left, right), max(left, right))
        if edge in edges:
            return None
        edges.add(edge)
        adjacency[left].add(right)
        adjacency[right].add(left)
    if any(len(neighbors) != 3 for neighbors in adjacency):
        return None

    for source in range(order):
        distances = [-1] * order
        distances[source] = 0
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[current] + 1
                    if distances[neighbor] > 5:
                        return None
                    queue.append(neighbor)
        if -1 in distances:
            return None
    return {"n": order, "edges": [list(edge) for edge in sorted(edges)]}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if config_id != CONFIG_ID:
        raise ValueError("unsupported configuration id")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    best = {"n": 1, "edges": []}
    attempts = 0
    accepted = 0
    for _ in search_steps(ATTEMPT_LIMIT):
        order = rng.choice(ORDER_CHOICES)
        candidate = _random_cubic_graph(order, rng)
        attempts += 1
        if candidate is not None:
            accepted += 1
            if order > best["n"]:
                best = candidate
    return {
        **best,
        "claimed_objective": best["n"],
        "search_metadata": {
            "algorithm": "seeded configuration-model sampling of simple cubic graphs; exact BFS rejects disconnected graphs and diameter above 5",
            "configuration_id": config_id,
            "seed": seed,
            "attempts": attempts,
            "attempt_limit": ATTEMPT_LIMIT,
            "accepted_candidates": accepted,
            "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            "comparison_data_read": False,
            "budget": {
                "attempt_limit": ATTEMPT_LIMIT,
                "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            },
        },
    }
