"""Exact clique checker for DIMACS C2000.9."""

from tasks.t059.graph import N, RAW_SHA256, load_graph

PARAMETERS = {"instance": "C2000.9", "vertices": 2000, "edges": 1799532}


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("parameters") != PARAMETERS:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict) or "vertices" not in solution:
        raise ValueError("solution must contain vertices")
    vertices = solution["vertices"]
    if not isinstance(vertices, list):
        raise ValueError("vertices must be a list")
    seen = set()
    for vertex in vertices:
        if type(vertex) is not int:
            raise ValueError("vertex indices must be integers; bool and float are rejected")
        if not 0 <= vertex < N:
            raise ValueError("vertex index is out of range")
        if vertex in seen:
            raise ValueError("duplicate vertex")
        seen.add(vertex)
    adjacency = load_graph()
    for i, vertex in enumerate(vertices):
        neighbors = adjacency[vertex]
        for other in vertices[i + 1:]:
            if not ((neighbors >> other) & 1):
                raise ValueError(f"vertices {vertex} and {other} are not adjacent")
    return {
        "objective": len(vertices),
        "verification_status": "exact",
        "details": {
            "instance": "C2000.9",
            "vertex_count": N,
            "edge_count": PARAMETERS["edges"],
            "clique_edges_checked": len(vertices) * (len(vertices) - 1) // 2,
            "graph_source_sha256": RAW_SHA256,
            "claimed_objective_ignored": True,
        },
    }
