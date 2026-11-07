"""Exact checker for the ordinary finite K4^- Turan problem on 36 vertices."""
from itertools import combinations

N = 36
CONFIG_ID = "T075-C01"
PARAMETERS = {
    "n": 36,
    "uniformity": 3,
    "forbidden_hypergraph": "K4^-: three triples on four vertices",
    "forbidden_semantics": "ordinary non-induced subhypergraph",
    "constraint": "every 4-vertex set spans at most 2 selected triples",
}


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _validate_config(config):
    if not isinstance(config, dict) or config.get("id") != CONFIG_ID:
        raise ValueError("unsupported T075 configuration")
    supplied = config.get("parameters")
    if not isinstance(supplied, dict) or supplied.keys() != PARAMETERS.keys():
        raise ValueError("unsupported T075 configuration parameters")
    if any(type(supplied[k]) is not type(v) or supplied[k] != v for k, v in PARAMETERS.items()):
        raise ValueError("unsupported T075 configuration parameters")


def validate(solution, config=None, strict=False):
    """Recompute edge count and check every 4-set exactly."""
    _validate_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be a JSON object")
    raw_edges = solution.get("edges")
    if not isinstance(raw_edges, list):
        raise ValueError("edges must be a list of triples")
    edges = set()
    for raw in raw_edges:
        if not isinstance(raw, (list, tuple)) or len(raw) != 3 or not all(_is_int(v) for v in raw):
            raise ValueError("each edge must contain exactly three integer vertex labels")
        if any(v < 0 or v >= N for v in raw):
            raise ValueError("vertex label is outside 0..35")
        if len(set(raw)) != 3:
            raise ValueError("an edge must contain three distinct vertices")
        e = tuple(sorted(raw))
        if e in edges:
            raise ValueError("duplicate hyperedge")
        edges.add(e)

    max_load = 0
    four_sets = 0
    for quad in combinations(range(N), 4):
        four_sets += 1
        load = 0
        for triple in combinations(quad, 3):
            load += triple in edges
        if load > 2:
            raise ValueError("a four-vertex set contains a copy of K4^-")
        max_load = max(max_load, load)

    objective = len(edges)
    upper_bound = (N * (N - 1) * (N - 2) // 6) // 2
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "vertex_count": N,
            "uniformity": 3,
            "edge_count": objective,
            "four_vertex_sets_checked": four_sets,
            "maximum_triples_on_any_four_set": max_load,
            "double_counting_upper_bound": upper_bound,
            "claimed_objective_ignored": True,
        },
    }
