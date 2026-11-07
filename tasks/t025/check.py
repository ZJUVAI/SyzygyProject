"""Exact checker for affine cap sets in F_3^7."""


DIMENSION = 7
FIELD_ORDER = 3
THEOREM_UPPER_BOUND = 288


def validate(solution, config, strict=False):
    """Check every pair and return the recomputed cap cardinality."""
    del strict  # The finite-domain check below is exact in both modes.
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    params = config.get("parameters", config)
    if (not isinstance(params, dict)
            or params.get("dimension") != DIMENSION
            or params.get("field_order") != FIELD_ORDER
            or params.get("max_points") != THEOREM_UPPER_BOUND):
        raise ValueError("configuration must be T025-C01 (F_3^7, at most 288 points)")
    points = solution.get("points")
    if not isinstance(points, list):
        raise ValueError("points must be a list")
    if len(points) > THEOREM_UPPER_BOUND:
        raise ValueError("point count exceeds the proved upper bound of 288")

    normalized = []
    for point in points:
        if not isinstance(point, list) or len(point) != DIMENSION:
            raise ValueError("each point must be a list of seven coordinates")
        if any(type(coordinate) is not int for coordinate in point):
            raise ValueError("coordinates must be integers, not bool or numeric values")
        if any(coordinate < 0 or coordinate >= FIELD_ORDER for coordinate in point):
            raise ValueError("coordinates must be in {0, 1, 2}")
        normalized.append(tuple(point))

    point_set = set(normalized)
    if len(point_set) != len(normalized):
        raise ValueError("duplicate points are not allowed")
    # In characteristic three, three distinct collinear points a,b,c satisfy
    # a+b+c=0. For every distinct pair, test its uniquely determined third point.
    for i, a in enumerate(normalized):
        for b in normalized[i + 1:]:
            third = tuple((-x - y) % FIELD_ORDER for x, y in zip(a, b))
            if third in point_set:
                raise ValueError("points contain three distinct points on an affine line")
    return {
        "objective": len(normalized),
        "verification_status": "exact",
        "details": {
            "dimension": DIMENSION,
            "field_order": FIELD_ORDER,
            "point_count": len(normalized),
            "distinct_points": True,
            "all_distinct_pairs_checked": True,
            "claimed_objective_ignored": True,
        },
    }
