"""Exact checker for the fixed arc130 cutwidth instance."""

from tasks.t088.instance import EDGE_COUNT, VERTEX_COUNT, cut_profile, load_graph


CONFIG_ID = "T088-C01"
PARAMETERS = {
    "instance": "arc130.mtx.rnd",
    "vertices": 130,
    "edges": 715,
    "graph": "undirected simple graph; 1-based source labels",
    "objective": "minimum over linear vertex orders of the maximum number of edges crossing any prefix cut",
}


def _check_config(config):
    if not isinstance(config, dict) or config.get("id") != CONFIG_ID:
        raise ValueError(f"configuration id must be {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration parameters do not match the frozen arc130 instance")
    if config.get("direction") != "minimize":
        raise ValueError("cutwidth is a minimization objective")


def validate(solution, config, strict=False):
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    ordering = solution.get("ordering")
    if not isinstance(ordering, list) or len(ordering) != VERTEX_COUNT:
        raise ValueError("ordering must contain exactly 130 vertex labels")
    if any(type(vertex) is not int for vertex in ordering):
        raise ValueError("vertex labels must be integers; booleans are not accepted")
    if set(ordering) != set(range(1, VERTEX_COUNT + 1)):
        raise ValueError("ordering must be a permutation of labels 1 through 130")
    edges = load_graph()
    if len(edges) != EDGE_COUNT:
        raise ValueError("frozen source graph has an unexpected edge count")
    profile = cut_profile(ordering, edges)
    return {
        "objective": max(profile),
        "verification_status": "exact",
        "details": {
            "vertices": VERTEX_COUNT,
            "edges": EDGE_COUNT,
            "prefix_cut_count": len(profile),
            "cut_profile": profile,
            "claimed_objective_ignored": True,
        },
    }
