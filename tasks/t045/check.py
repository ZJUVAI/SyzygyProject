"""Exact verifier for minimum linear arrangement on the pinned gd96a graph."""

from tasks.t045.graph import EDGE_COUNT, VERTICES, load_graph

PARAMETERS = {"graph": "gd96a", "vertices": VERTICES, "edges": EDGE_COUNT}


def validate(solution, config, strict=False):
    if config.get("parameters") != PARAMETERS:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict) or "ordering" not in solution:
        raise ValueError("solution must contain ordering")
    ordering = solution["ordering"]
    if not isinstance(ordering, (list, tuple)) or len(ordering) != VERTICES:
        raise ValueError("ordering must contain each of the 1,096 vertices exactly once")
    if any(type(vertex) is not int for vertex in ordering):
        raise ValueError("vertex labels must be integers; bool and non-integer values are rejected")
    if any(vertex < 1 or vertex > VERTICES for vertex in ordering):
        raise ValueError("vertex labels must be in the range 1 through 1,096")
    if len(set(ordering)) != VERTICES:
        raise ValueError("ordering must be a permutation without repeated vertices")
    positions = [0] * (VERTICES + 1)
    for position, vertex in enumerate(ordering, start=1):
        positions[vertex] = position
    n, edges = load_graph()
    if n != VERTICES or len(edges) != EDGE_COUNT:
        raise ValueError("loaded graph does not match the fixed configuration")
    objective = sum(abs(positions[u + 1] - positions[v + 1]) for u, v in edges)
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "graph": "gd96a",
            "vertices": VERTICES,
            "edges_checked": EDGE_COUNT,
            "claimed_objective_ignored": True,
        },
    }
