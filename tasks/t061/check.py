"""Exact checker for C6-free and C6-saturated simple graphs on 100 vertices."""


CONFIG_ID = "T061-C01"
PARAMETERS = {
    "vertices": 100,
    "forbidden_subgraph": "simple cycle C6",
    "saturation": "C6-free; adding any missing edge creates a simple C6",
    "objective": "number of edges",
}


def _check_config(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    if config.get("id") not in (None, CONFIG_ID):
        raise ValueError(f"unsupported configuration: expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix 100 vertices and simple C6 saturation")


def _iter_bits(mask):
    while mask:
        bit = mask & -mask
        mask ^= bit
        yield bit.bit_length() - 1


def _path_endpoint_pairs(adjacency):
    """Enumerate endpoint pairs of all simple 5-edge paths, stopping on C6."""
    endpoints = set()
    n = len(adjacency)

    def visit(start, vertex, depth, seen):
        if depth == 5:
            if adjacency[vertex] & (1 << start):
                raise ValueError("graph contains a simple cycle of length 6")
            if start < vertex:
                endpoints.add((start, vertex))
            else:
                endpoints.add((vertex, start))
            return
        for neighbor in _iter_bits(adjacency[vertex] & ~seen):
            visit(start, neighbor, depth + 1, seen | (1 << neighbor))

    for start in range(n):
        visit(start, start, 0, 1 << start)
    return endpoints


def validate(solution, config, strict=False):
    """Independently prove C6-freeness and saturation by simple path enumeration."""
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    vertices = solution.get("vertices")
    if type(vertices) is not int or vertices != 100:
        raise ValueError("vertices must be the integer 100")
    edges = solution.get("edges")
    if not isinstance(edges, list):
        raise ValueError("edges must be a list")

    adjacency = [0] * 100
    normalized_edges = set()
    for index, edge in enumerate(edges):
        if not isinstance(edge, list) or len(edge) != 2:
            raise ValueError(f"edge {index} must be a pair of vertex IDs")
        left, right = edge
        if type(left) is not int or type(right) is not int:
            raise ValueError(f"edge {index} endpoints must be integers")
        if left < 0 or right < 0 or left >= 100 or right >= 100:
            raise ValueError(f"edge {index} endpoint is outside 0..99")
        if left == right:
            raise ValueError(f"edge {index} is a loop")
        pair = (left, right) if left < right else (right, left)
        if pair in normalized_edges:
            raise ValueError(f"duplicate edge {pair}")
        normalized_edges.add(pair)
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left

    path_endpoints = _path_endpoint_pairs(adjacency)
    missing_pair = None
    for left in range(100):
        for right in range(left + 1, 100):
            if adjacency[left] & (1 << right):
                continue
            if (left, right) not in path_endpoints:
                missing_pair = (left, right)
                break
        if missing_pair is not None:
            break
    if missing_pair is not None:
        raise ValueError(
            f"graph is not C6-saturated: nonedge {missing_pair} has no simple 5-edge path"
        )

    return {
        "objective": len(normalized_edges),
        "verification_status": "exact",
        "details": {
            "vertices": 100,
            "edge_count": len(normalized_edges),
            "simple_c6_free": True,
            "saturated": True,
            "missing_pairs_checked": 4950 - len(normalized_edges),
            "simple_5_path_endpoint_pairs": len(path_endpoints),
            "claimed_objective_ignored": True,
        },
    }
