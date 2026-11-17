"""Exact small-depth path routines and greedy C6-saturation construction."""

import random


N = 100


def path5_exists(adjacency, start, target):
    """Return whether start and target have a simple path of exactly 5 edges."""
    target_bit = 1 << target

    def visit(vertex, depth, seen):
        if depth == 5:
            return vertex == target
        candidates = adjacency[vertex] & ~seen
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            neighbor = bit.bit_length() - 1
            if neighbor == target:
                if depth == 4:
                    return True
                continue
            if visit(neighbor, depth + 1, seen | bit):
                return True
        return False

    if start == target or adjacency[start] & target_bit:
        return False
    return visit(start, 0, 1 << start)


def greedy_saturated(edge_order):
    """Add edges in a fixed order when they do not complete a simple C6."""
    adjacency = [0] * N
    edges = []
    for left, right in edge_order:
        if not path5_exists(adjacency, left, right):
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
            edges.append([left, right])
    return {"vertices": N, "edges": edges}


def shuffled_edge_order(rng):
    order = [(left, right) for left in range(N) for right in range(left + 1, N)]
    rng.shuffle(order)
    return order
