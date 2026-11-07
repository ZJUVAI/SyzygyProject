"""Exact finite checker for Ramsey (5,5) graphs."""


def _has_clique(neighbors, size=5):
    def visit(candidates, depth):
        if depth == size:
            return True
        if candidates.bit_count() < size - depth:
            return False
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            if visit(candidates & neighbors[vertex], depth + 1):
                return True
        return False

    return visit((1 << len(neighbors)) - 1, 0)


def validate(solution, config, strict=False):
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    params = config.get("parameters", config)
    if (not isinstance(params, dict) or params.get("clique_size") != 5
            or params.get("independent_set_size") != 5
            or params.get("max_vertices") != 45):
        raise ValueError("configuration must be T022-C01 (5,5), up to 45 vertices")
    adjacency = solution.get("adjacency")
    if not isinstance(adjacency, list):
        raise ValueError("adjacency must be a list of neighbor lists")
    n = len(adjacency)
    if n > 45:
        # Angeltveit and McKay prove R(5,5) <= 46.
        raise ValueError("the published bound R(5,5) <= 46 excludes valid graphs above 45 vertices")
    neighbor_bits = [0] * n
    normalized = []
    for v, row in enumerate(adjacency):
        if not isinstance(row, list):
            raise ValueError("each adjacency row must be a list")
        if any(type(w) is not int or w < 0 or w >= n for w in row):
            raise ValueError("neighbor indices must be in-range integers")
        if v in row:
            raise ValueError("loops are not allowed")
        if len(set(row)) != len(row):
            raise ValueError("duplicate neighbors are not allowed")
        normalized.append(set(row))
    for v in range(n):
        for w in normalized[v]:
            if v not in normalized[w]:
                raise ValueError("adjacency must be symmetric")
            neighbor_bits[v] |= 1 << w
    if _has_clique(neighbor_bits):
        raise ValueError("graph contains a 5-clique")
    complement = [(((1 << n) - 1) ^ (1 << v) ^ neighbor_bits[v]) for v in range(n)]
    if _has_clique(complement):
        raise ValueError("graph contains an independent set of size 5")
    edges = sum(row.bit_count() for row in neighbor_bits) // 2
    return {"objective": n, "verification_status": "exact",
            "details": {"vertices": n, "edges": edges,
                        "clique_size": 5, "independent_set_size": 5,
                        "clique_search_exhaustive": True,
                        "complement_clique_search_exhaustive": True}}
