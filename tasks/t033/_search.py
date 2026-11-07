"""Seeded 1-flip local search shared by the task's classical programs."""

import json
import random
from pathlib import Path


_DATA = json.loads((Path(__file__).parent / "data" / "instance.json").read_text())
_N = _DATA["n"]
_EDGES = _DATA["edges"]
_ADJ = [[] for _ in range(_N)]
for _u, _v, _w in _EDGES:
    _ADJ[_u].append((_v, _w))
    _ADJ[_v].append((_u, _w))


def cut_value(labels):
    return sum(w for u, v, w in _EDGES if labels[u] != labels[v])


def _improve_with_count(labels, rng, max_flips):
    """Choose positive-gain vertex flips until locally optimal or capped."""
    labels = labels[:]
    gains = [sum(w if labels[v] == labels[side] else -w
                 for v, w in _ADJ[side]) for side in range(_N)]
    flips = 0
    for _ in range(max_flips):
        positive = [i for i, gain in enumerate(gains) if gain > 0]
        if not positive:
            break
        best_gain = max(gains[i] for i in positive)
        choices = [i for i in positive if gains[i] == best_gain]
        vertex = rng.choice(choices)
        old_side = labels[vertex]
        labels[vertex] = 1 - old_side
        flips += 1
        gains[vertex] = -gains[vertex]
        for neighbor, weight in _ADJ[vertex]:
            old_contribution = weight if labels[neighbor] == old_side else -weight
            gains[neighbor] -= 2 * old_contribution
    return labels, flips


def improve(labels, rng, max_flips):
    """Choose positive-gain vertex flips until locally optimal or capped."""
    improved, _ = _improve_with_count(labels, rng, max_flips)
    return improved


def repeated_local_search(seed, restarts=1, max_flips=10000, start=None):
    labels, value, _ = repeated_local_search_with_metadata(
        seed, restarts=restarts, max_flips=max_flips, start=start)
    return labels, value


def repeated_local_search_with_metadata(seed, restarts=1, max_flips=10000,
                                        start=None):
    rng = random.Random(seed)
    best = None
    best_value = -1
    flips_per_restart = []
    for attempt in range(restarts):
        if attempt == 0 and start is not None:
            labels = start[:]
        else:
            labels = [rng.randrange(2) for _ in range(_N)]
        labels, flips = _improve_with_count(labels, rng, max_flips)
        flips_per_restart.append(flips)
        value = cut_value(labels)
        if value > best_value:
            best, best_value = labels, value
    return best, best_value, {
        "algorithm": "steepest_improving_single_vertex_flip",
        "seed": seed,
        "restarts": restarts,
        "max_flips_per_restart": max_flips,
        "flips_per_restart": flips_per_restart,
        "total_flips": sum(flips_per_restart),
        "budget": "fixed iteration cap; stop early at 1-flip local optimum",
    }
