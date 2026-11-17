"""Load the pinned C2000.9 upper-triangle bitset as adjacency integers."""

from functools import lru_cache
from pathlib import Path
from tasks.graph_bits import load_adjacency

N = 2000
M = 1799532
RAW_SHA256 = "aa4b1d7df7f9c1afbf8c9f35fcf5bdfc6370fd27db5c9f3fd5409dfd0d164f16"
PACKED_SHA256 = "687ce2b39ee17bad81ae8ba2253b40441e270dc61c72e5e39fe58f9d404dca4d"
SOURCE = Path(__file__).resolve().parent / "data/source/C2000.9.bits"


@lru_cache(maxsize=1)
def load_graph():
    return load_adjacency(SOURCE, N, M, PACKED_SHA256)


def bit_vertices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def greedy_clique(seed=0, randomized=True, degree_mode="static"):
    """Construct a clique by greedy candidate intersections."""
    import random

    rng = random.Random(seed)
    adj = load_graph()
    degrees = [row.bit_count() for row in adj]
    candidate = (1 << N) - 1
    clique = []
    while candidate:
        vertices = list(bit_vertices(candidate))
        if degree_mode == "dynamic":
            scores = [(adj[v] & candidate).bit_count() for v in vertices]
        elif degree_mode == "static":
            scores = [degrees[v] for v in vertices]
        else:
            raise ValueError("unknown degree mode")
        if randomized:
            noise = [rng.random() for _ in vertices]
            chosen_index = max(range(len(vertices)), key=lambda i: (scores[i], noise[i]))
        else:
            chosen_index = max(range(len(vertices)), key=lambda i: (scores[i], -vertices[i]))
        vertex = vertices[chosen_index]
        clique.append(vertex)
        candidate &= adj[vertex]
    return clique


def one_for_two_improve(clique):
    """Try deterministic one-vertex replacement by a compatible pair."""
    adj = load_graph()
    clique_set = set(clique)
    for removed in clique:
        common = (1 << N) - 1
        for v in clique:
            if v != removed:
                common &= adj[v]
        common &= ~sum(1 << v for v in clique_set)
        for u in bit_vertices(common):
            possible = common & adj[u]
            if possible:
                v = next(bit_vertices(possible))
                return sorted((clique_set - {removed}) | {u, v})
    return None


def improve_clique(clique, rounds=4):
    current = sorted(set(clique))
    for _ in range(rounds):
        improved = one_for_two_improve(current)
        if improved is None:
            break
        current = improved
    return current
