"""Load the pinned DIMACS C2000.9 graph as Python integer bitsets."""

import gzip
import hashlib
from functools import lru_cache
from pathlib import Path

N = 2000
M = 1799532
RAW_SHA256 = "aa4b1d7df7f9c1afbf8c9f35fcf5bdfc6370fd27db5c9f3fd5409dfd0d164f16"
SOURCE = Path(__file__).resolve().parent / "data/source/C2000.9.clq.gz"


@lru_cache(maxsize=1)
def load_graph():
    adjacency = [0] * N
    digest = hashlib.sha256()
    header = None
    edge_count = 0
    with gzip.open(SOURCE, "rb") as stream:
        for raw in stream:
            digest.update(raw)
            fields = raw.split()
            if not fields or fields[0] == b"c":
                continue
            if fields[0] == b"p":
                if len(fields) != 4 or fields[1] not in (b"edge", b"col"):
                    raise RuntimeError("invalid DIMACS problem line")
                header = (int(fields[2]), int(fields[3]))
            elif fields[0] == b"e":
                if len(fields) != 3:
                    raise RuntimeError("invalid DIMACS edge line")
                u, v = int(fields[1]) - 1, int(fields[2]) - 1
                if not (0 <= u < N and 0 <= v < N) or u == v:
                    raise RuntimeError("invalid DIMACS vertex index")
                bit_u, bit_v = 1 << u, 1 << v
                if adjacency[u] & bit_v:
                    raise RuntimeError("duplicate DIMACS edge")
                adjacency[u] |= bit_v
                adjacency[v] |= bit_u
                edge_count += 1
            else:
                raise RuntimeError("unknown DIMACS record")
    if digest.hexdigest() != RAW_SHA256:
        raise RuntimeError("raw graph source hash mismatch")
    if header != (N, M) or edge_count != M:
        raise RuntimeError("unexpected C2000.9 dimensions")
    return tuple(adjacency)


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
