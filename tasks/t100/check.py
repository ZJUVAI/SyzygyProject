"""Exact checker for triangle minimization at n=50 and m=700."""

CONFIG_ID = "T100-C01"
PARAMETERS = {
    "vertices": 50,
    "edges": 700,
    "graph": "simple undirected graph",
    "objective": "number of triangles",
}
HUMAN_REFERENCE = 1817
N = 50
M = 700


def _same_json_types(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(right, dict):
        return left.keys() == right.keys() and all(
            _same_json_types(left[key], right[key]) for key in right
        )
    if isinstance(right, list):
        return len(left) == len(right) and all(
            _same_json_types(a, b) for a, b in zip(left, right)
        )
    return left == right


def _check_config(config):
    if not isinstance(config, dict) or set(config) != {
        "id", "parameters", "direction", "human_reference"
    }:
        raise ValueError("configuration must use the complete frozen task configuration")
    if type(config["id"]) is not str or config["id"] != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if not _same_json_types(config["parameters"], PARAMETERS):
        raise ValueError("configuration must fix a simple graph with 50 vertices and 700 edges")
    if type(config["direction"]) is not str or config["direction"] != "minimize":
        raise ValueError("configuration direction must be minimize")
    if type(config["human_reference"]) is not int or config["human_reference"] != HUMAN_REFERENCE:
        raise ValueError("configuration human_reference must be the integer 1817")


def _count_triangles(adjacency):
    count = 0
    for left in range(N):
        left_mask = adjacency[left]
        for middle in range(left + 1, N):
            if left_mask & (1 << middle):
                later = left_mask & adjacency[middle] & ~((1 << (middle + 1)) - 1)
                count += later.bit_count()
    return count


def validate(solution, config, strict=False):
    """Check the complete graph constraints and count every triangle exactly."""
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    if type(solution.get("vertices")) is not int or solution["vertices"] != N:
        raise ValueError("vertices must be the integer 50")
    edges = solution.get("edges")
    if not isinstance(edges, list):
        raise ValueError("edges must be a list")
    if len(edges) != M:
        raise ValueError("edges must contain exactly 700 pairs")

    adjacency = [0] * N
    seen = set()
    for index, edge in enumerate(edges):
        if not isinstance(edge, list) or len(edge) != 2:
            raise ValueError(f"edge {index} must be a two-element list")
        left, right = edge
        if type(left) is not int or type(right) is not int:
            raise ValueError(f"edge {index} endpoints must be integers")
        if not (0 <= left < N and 0 <= right < N):
            raise ValueError(f"edge {index} endpoint is outside 0..49")
        if left == right:
            raise ValueError(f"edge {index} is a loop")
        pair = (left, right) if left < right else (right, left)
        if pair in seen:
            raise ValueError(f"duplicate undirected edge {pair}")
        seen.add(pair)
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left

    triangles = _count_triangles(adjacency)
    return {
        "objective": triangles,
        "verification_status": "exact",
        "details": {
            "vertices": N,
            "edge_count": len(seen),
            "triangle_count": triangles,
            "simple_undirected": True,
            "claimed_objective_ignored": True,
        },
    }
