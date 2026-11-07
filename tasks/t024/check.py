"""Exact checker for C4-free simple graphs on 41 vertices."""

def validate(solution, config, strict=False):
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    p = config.get("parameters", config)
    if not isinstance(p, dict) or p.get("vertices") != 41 or p.get("forbidden_cycle_length") != 4:
        raise ValueError("configuration must be T024-C01 (41 vertices, C4-free)")
    rows = solution.get("adjacency")
    if not isinstance(rows, list) or len(rows) != 41:
        raise ValueError("adjacency must contain exactly 41 rows")
    normalized = []
    for v, row in enumerate(rows):
        if not isinstance(row, list):
            raise ValueError("each adjacency row must be a list")
        if any(type(w) is not int or not 0 <= w < 41 for w in row):
            raise ValueError("neighbor indices must be integers in [0, 40]")
        if v in row or len(set(row)) != len(row):
            raise ValueError("loops and duplicate neighbors are forbidden")
        normalized.append(set(row))
    for v, ns in enumerate(normalized):
        if any(v not in normalized[w] for w in ns):
            raise ValueError("adjacency must be symmetric")
    # A simple graph is C4-free iff each unordered pair has at most one common neighbor.
    common_pair_count = {}
    for neighbors in normalized:
        ns = sorted(neighbors)
        for i, u in enumerate(ns):
            for w in ns[i + 1:]:
                pair = (u, w)
                common_pair_count[pair] = common_pair_count.get(pair, 0) + 1
                if common_pair_count[pair] > 1:
                    raise ValueError("graph contains a 4-cycle")
    edges = sum(map(len, normalized)) // 2
    return {"objective": edges, "verification_status": "exact",
            "details": {"vertices": 41, "edges": edges,
                        "common_neighbor_pair_count": len(common_pair_count),
                        "maximum_common_neighbors": max(common_pair_count.values(), default=0),
                        "c4_check": "all unordered vertex pairs have at most one common neighbor",
                        "claimed_objective_ignored": True}}
