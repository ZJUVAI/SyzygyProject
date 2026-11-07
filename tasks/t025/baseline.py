"""Seeded greedy search from the simple binary cap; no reference data is read."""

import os
import random

from mathbench.search import search_steps


DIM = 7
SPACE_SIZE = 3 ** DIM
ITERATION_LIMIT = 100_000


def _decode(index):
    coordinates = [0] * DIM
    for position in range(DIM - 1, -1, -1):
        index, coordinates[position] = divmod(index, 3)
    return tuple(coordinates)


def _encode(point):
    value = 0
    for coordinate in point:
        value = 3 * value + coordinate
    return value


def _target_sum(a, b):
    return _encode(tuple((-x - y) % 3 for x, y in zip(a, b)))


def _seed():
    return {_encode(_decode(i)) for i in range(SPACE_SIZE)
            if all(coordinate != 2 for coordinate in _decode(i))}


def _add_point(points, forbidden, candidate):
    if candidate in forbidden:
        return False
    point = _decode(candidate)
    for old_index in points:
        forbidden.add(_target_sum(point, _decode(old_index)))
    points.add(candidate)
    return True


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    base = _seed()
    best = set(base)
    iterations = 0
    restarts = 0
    steps = iter(search_steps(ITERATION_LIMIT))

    while True:
        points = set(base)
        forbidden = set()
        decoded = [_decode(index) for index in points]
        for i, a in enumerate(decoded):
            for b in decoded[i + 1:]:
                forbidden.add(_target_sum(a, b))
        order = [i for i in range(SPACE_SIZE) if i not in points]
        rng.shuffle(order)
        restarts += 1
        for candidate in order:
            if next(steps, None) is None:
                return {
                    "points": [list(_decode(i)) for i in sorted(best)],
                    "search_metadata": {
                        "algorithm": "seeded randomized greedy extension from the binary cap",
                        "seed": seed,
                        "iterations": iterations,
                        "iteration_limit": ITERATION_LIMIT,
                        "restarts": restarts,
                        "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
                        "budget": {
                            "iteration_limit": ITERATION_LIMIT,
                            "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
                        },
                        "reference_data_read": False,
                    },
                }
            iterations += 1
            _add_point(points, forbidden, candidate)
        if len(points) > len(best):
            best = points
