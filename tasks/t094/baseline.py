"""Random recursive triangulation search; it reads no comparison assets."""

import os
import random
import heapq
import math

from tasks.t094.triangulation import N, random_recursive_triangulation


def _fast_value(edges):
    adjacency = [[] for _ in range(N)]
    for a, b in edges:
        d = min((a - b) % N, (b - a) % N)
        length = 2.0 * math.sin(math.pi * d / N)
        adjacency[a].append((b, length))
        adjacency[b].append((a, length))
    worst = 1.0
    for source in range(N):
        dist = [math.inf] * N
        dist[source] = 0.0
        todo = [(0.0, source)]
        while todo:
            value, node = heapq.heappop(todo)
            if value != dist[node]:
                continue
            for other, length in adjacency[node]:
                candidate = value + length
                if candidate < dist[other]:
                    dist[other] = candidate
                    heapq.heappush(todo, (candidate, other))
        for target in range(source + 1, N):
            direct = 2.0 * math.sin(math.pi * min(target - source, N - target + source) / N)
            worst = max(worst, dist[target] / direct)
    return worst


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    trials = max(1, int(os.environ.get("T094_SEARCH_TRIALS", "6")))
    best = None
    best_value = math.inf
    for _ in range(trials):
        candidate = random_recursive_triangulation(rng.randrange(1 << 30))
        value = _fast_value(candidate)
        if value < best_value:
            best, best_value = candidate, value
    return {
        "edges": best,
        "search_metadata": {
            "algorithm": "uniform recursive split triangulations; retain the best floating feedback score",
            "trials": trials,
            "seed": seed,
            "reference_data_read": False,
            "feedback_is_certified": False,
        },
    }
