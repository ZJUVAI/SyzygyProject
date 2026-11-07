"""Task-local constructors for triangulations of the regular 120-gon."""

import random


N = 120


def random_recursive_triangulation(seed):
    rng = random.Random(seed)
    edges = set()

    def split(left, right):
        if right - left < 2:
            return
        pivot = rng.randrange(left + 1, right)
        edges.add((left, pivot))
        edges.add((pivot, right))
        split(left, pivot)
        split(pivot, right)

    split(0, N - 1)
    edges.discard((0, N - 1))
    edges.update((i, i + 1) for i in range(N - 1))
    edges.add((0, N - 1))
    return [list(edge) for edge in sorted(edges)]

