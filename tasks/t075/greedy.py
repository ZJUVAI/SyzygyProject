"""Greedy additions for K4^- avoidance; no human or reference assets are read."""
from itertools import combinations
import random


N = 36


def all_triples(n=N):
    return list(combinations(range(n), 3))


def greedy_add(order, n=N):
    """Scan a supplied edge order and add an edge when all four-set loads stay <=2."""
    loads = {}
    selected = []
    for triple in order:
        a, b, c = triple
        extensions = [tuple(sorted((a, b, c, x))) for x in range(n) if x != a and x != b and x != c]
        if all(loads.get(q, 0) < 2 for q in extensions):
            selected.append(triple)
            for q in extensions:
                loads[q] = loads.get(q, 0) + 1
    return {"edges": [list(e) for e in sorted(selected)]}


def randomized_greedy(seed, permutation=None, n=N):
    rng = random.Random(seed)
    order = all_triples(n)
    if permutation is None:
        rng.shuffle(order)
    else:
        # Random priorities give a reproducible order that can be varied by a seed.
        priorities = [rng.random() for _ in order]
        order = [e for _, e in sorted(zip(priorities, order))]
    return greedy_add(order, n)
