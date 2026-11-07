"""Exact combinatorial and certified metric checker for T094-C01."""

from fractions import Fraction
import heapq
import math


N = 120
CONFIG_ID = "T094-C01"
PARAMETERS = {
    "vertices": 120,
    "polygon": "regular convex 120-gon, vertices in counterclockwise cyclic order",
    "construction": "straight-line triangulation using polygon vertices only",
    "objective": "minimize over triangulations the maximum, over distinct vertex pairs, of shortest-path length divided by Euclidean chord length",
    "distance": "Euclidean chord length",
}
FROZEN_CONFIG = {
    "id": CONFIG_ID,
    "parameters": PARAMETERS,
    "direction": "minimize",
    "human_reference": 1.449476373154,
}
SCALE = 10**24


def _atan_bounds_inverse(q, terms=24):
    """Rational lower/upper bounds for atan(1/q), from the alternating series."""
    x = Fraction(1, q)
    partial = Fraction(0)
    for k in range(terms):
        term = x ** (2 * k + 1) / (2 * k + 1)
        partial += term if k % 2 == 0 else -term
    next_term = x ** (2 * terms + 1) / (2 * terms + 1)
    return partial, partial + (next_term if terms % 2 == 0 else -next_term)


def _pi_bounds():
    a_lo, a_hi = _atan_bounds_inverse(5)
    b_lo, b_hi = _atan_bounds_inverse(239)
    return 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo


def _sin_taylor(x, last_k):
    total = Fraction(0)
    for k in range(last_k + 1):
        term = x ** (2 * k + 1) / math.factorial(2 * k + 1)
        total += term if k % 2 == 0 else -term
    return total


def _chord_bounds():
    """Integer lower/upper bounds for each chord, scaled by 10**24."""
    pi_lo, pi_hi = _pi_bounds()
    result = {0: (0, 0)}
    for k in range(1, N // 2 + 1):
        if k == N // 2:
            result[k] = (2 * SCALE, 2 * SCALE)
            continue
        x_lo = pi_lo * k / N
        x_hi = pi_hi * k / N
        # On [0, pi/2], sine is increasing. Taylor partials ending in a
        # negative/positive term bound sine from below/above respectively.
        sin_lo = _sin_taylor(x_lo, 19)
        sin_hi = _sin_taylor(x_hi, 18)
        lo = (2 * sin_lo * SCALE).numerator // (2 * sin_lo * SCALE).denominator
        hi_fraction = 2 * sin_hi * SCALE
        hi = -((-hi_fraction.numerator) // hi_fraction.denominator)
        result[k] = (lo, hi)
    return result


_CHORDS = None


def _weights():
    global _CHORDS
    if _CHORDS is None:
        _CHORDS = _chord_bounds()
    return _CHORDS


def _cyclic_distance(i, j):
    delta = abs(i - j)
    return min(delta, N - delta)


def _crosses(a, b, c, d):
    """Whether two nonincident polygon chords cross in their interiors."""
    if len({a, b, c, d}) < 4:
        return False
    if a > b:
        a, b = b, a
    if c > d:
        c, d = d, c
    return (a < c < b) != (a < d < b)


def _normalize_edges(raw):
    if not isinstance(raw, list):
        raise ValueError("edges must be a list of endpoint pairs")
    edges = []
    seen = set()
    for item in raw:
        if not isinstance(item, list) or len(item) != 2:
            raise ValueError("each edge must be a two-integer list")
        a, b = item
        if type(a) is not int or type(b) is not int:
            raise ValueError("edge endpoints must be integers; booleans are rejected")
        if not (0 <= a < N and 0 <= b < N) or a == b:
            raise ValueError("edge endpoint out of range or self-loop")
        edge = (min(a, b), max(a, b))
        if edge in seen:
            raise ValueError("duplicate edge")
        seen.add(edge)
        edges.append(edge)
    return sorted(edges)


def _validate_triangulation(edges):
    required_boundary = {(i, (i + 1) % N) if i < (i + 1) % N else ((i + 1) % N, i) for i in range(N)}
    edge_set = set(edges)
    if not required_boundary <= edge_set:
        raise ValueError("all 120 polygon boundary edges are required")
    if len(edges) != 2 * N - 3:
        raise ValueError("a triangulation must contain exactly 2*n-3 edges")
    diagonals = [e for e in edges if _cyclic_distance(*e) != 1]
    for ix, (a, b) in enumerate(diagonals):
        for c, d in diagonals[ix + 1:]:
            if _crosses(a, b, c, d):
                raise ValueError("diagonals cross")


def _dijkstra(adjacency, source):
    distances = [None] * N
    distances[source] = 0
    queue = [(0, source)]
    while queue:
        distance, vertex = heapq.heappop(queue)
        if distances[vertex] != distance:
            continue
        for neighbor, weight in adjacency[vertex]:
            candidate = distance + weight
            if distances[neighbor] is None or candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heapq.heappush(queue, (candidate, neighbor))
    if any(value is None for value in distances):
        raise ValueError("triangulation graph is disconnected")
    return distances


def certified_dilation(edges):
    """Return a rational interval enclosing the exact dilation."""
    chords = _weights()
    adjacency_lo = [[] for _ in range(N)]
    adjacency_hi = [[] for _ in range(N)]
    for a, b in edges:
        k = _cyclic_distance(a, b)
        lo, hi = chords[k]
        adjacency_lo[a].append((b, lo))
        adjacency_lo[b].append((a, lo))
        adjacency_hi[a].append((b, hi))
        adjacency_hi[b].append((a, hi))
    lower = Fraction(0)
    upper = Fraction(0)
    for source in range(N):
        dist_lo = _dijkstra(adjacency_lo, source)
        dist_hi = _dijkstra(adjacency_hi, source)
        for target in range(source + 1, N):
            direct_lo, direct_hi = chords[_cyclic_distance(source, target)]
            lower = max(lower, Fraction(dist_lo[target], direct_hi))
            upper = max(upper, Fraction(dist_hi[target], direct_lo))
    return lower, upper


def validate(solution, config, strict=False):
    del strict
    if not isinstance(config, dict) or not _same_typed(config, FROZEN_CONFIG):
        raise ValueError(f"configuration id must be {CONFIG_ID}")
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    edges = _normalize_edges(solution.get("edges"))
    _validate_triangulation(edges)
    lower, upper = certified_dilation(edges)
    return {
        "objective": str(upper),
        "objective_value": str(upper),
        "verification_status": "certified",
        "details": {
            "objective_interval": [str(lower), str(upper)],
            "scale": str(SCALE),
            "vertices": N,
            "edges": len(edges),
            "claimed_objective_ignored": True,
        },
    }


def _same_typed(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_same_typed(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(_same_typed(a, b) for a, b in zip(left, right))
    return left == right
