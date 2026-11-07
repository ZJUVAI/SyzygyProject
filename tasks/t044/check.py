"""Exact checker for simple graphs of maximum degree 3 and diameter at most 5."""

from collections import deque
from collections.abc import Mapping
from typing import Any


CONFIG_ID = "T044-C01"
MAXIMUM_DEGREE = 3
DIAMETER_BOUND = 5
MOORE_BOUND = 94


def _is_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _parameters_match(config: Mapping[str, Any]) -> bool:
    return config.get("parameters") == {
        "maximum_degree": MAXIMUM_DEGREE,
        "diameter_at_most": DIAMETER_BOUND,
        "graph": "simple_undirected_connected",
    }


def validate(solution: Any, config: Mapping[str, Any], strict: bool = False) -> dict[str, Any]:
    """Validate every edge and run exact breadth-first searches from all vertices."""
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError("unsupported configuration id")
    if not _parameters_match(config):
        raise ValueError("configuration parameters do not match T044-C01")
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be a JSON object")

    order = solution.get("n")
    raw_edges = solution.get("edges")
    if not _is_integer(order) or not 1 <= order <= MOORE_BOUND:
        raise ValueError("n must be an integer in [1, 94]")
    if not isinstance(raw_edges, (list, tuple, set, frozenset)):
        raise ValueError("edges must be a list or set of endpoint pairs")

    edges = set()
    adjacency = [set() for _ in range(order)]
    for edge in raw_edges:
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            raise ValueError("each edge must contain exactly two integer endpoints")
        left, right = edge
        if not _is_integer(left) or not _is_integer(right):
            raise ValueError("edge endpoints must be integers; bool is not accepted")
        if not (0 <= left < order and 0 <= right < order):
            raise ValueError("edge endpoint is outside 0..n-1")
        if left == right:
            raise ValueError("self-loops are not allowed")
        key = (min(left, right), max(left, right))
        if key in edges:
            raise ValueError("duplicate undirected edge")
        edges.add(key)
        adjacency[left].add(right)
        adjacency[right].add(left)

    degrees = [len(neighbors) for neighbors in adjacency]
    maximum_degree = max(degrees, default=0)
    if maximum_degree > MAXIMUM_DEGREE:
        raise ValueError("maximum degree exceeds 3")

    maximum_distance = 0
    distances_checked = 0
    for source in range(order):
        distances = [-1] * order
        distances[source] = 0
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        if any(distance == -1 for distance in distances):
            raise ValueError("graph must be connected")
        eccentricity = max(distances, default=0)
        if eccentricity > DIAMETER_BOUND:
            raise ValueError(f"graph diameter exceeds 5 (vertex {source} has eccentricity {eccentricity})")
        maximum_distance = max(maximum_distance, eccentricity)
        distances_checked += order

    return {
        "objective": order,
        "verification_status": "exact",
        "details": {
            "order": order,
            "edge_count": len(edges),
            "maximum_degree": maximum_degree,
            "diameter": maximum_distance,
            "all_source_distances_checked": distances_checked,
            "claimed_score_ignored": True,
            "strict_full_graph_check": True,
            "moore_bound": MOORE_BOUND,
        },
    }
