"""Shared exact graph helpers for T100 search programs."""

from itertools import combinations


N = 50
M = 700
ALL_EDGES = tuple(combinations(range(N), 2))


def triangle_count(edges):
    adjacency = [0] * N
    for left, right in edges:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    count = 0
    for left in range(N):
        left_mask = adjacency[left]
        for middle in range(left + 1, N):
            if left_mask & (1 << middle):
                common_later = left_mask & adjacency[middle] & ~((1 << (middle + 1)) - 1)
                count += common_later.bit_count()
    return count


def normalize_edge(edge):
    left, right = edge
    return (left, right) if left < right else (right, left)
