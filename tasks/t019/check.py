"""Exact checker for point sets with no convex seven-point subset."""

from fractions import Fraction
from itertools import combinations


def _coordinate(value):
    if type(value) is int:
        return value
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("coordinate strings must be rational numbers") from exc
    raise ValueError("coordinates must be integers or rational strings such as '3/5'")


def _orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _has_convex_seven(points):
    """Search exactly using the fact that a set is convex iff all 4-subsets are."""
    n = len(points)
    triple_masks = {}
    for i, j, k in combinations(range(n), 3):
        a, b, c = points[i], points[j], points[k]
        mask = 0
        for q, p in enumerate(points):
            if q in (i, j, k):
                continue
            quad = (a, b, c, p)
            convex = True
            for u in range(4):
                triangle = [quad[v] for v in range(4) if v != u]
                z = quad[u]
                x = _orient(triangle[0], triangle[1], z)
                y = _orient(triangle[1], triangle[2], z)
                w = _orient(triangle[2], triangle[0], z)
                # In general position, a vertex is outside the triangle of
                # the other three iff these signs are mixed.
                if (x > 0 and y > 0 and w > 0) or (x < 0 and y < 0 and w < 0):
                    convex = False
                    break
            if convex:
                mask |= 1 << q
        triple_masks[(i, j, k)] = mask

    def extend(chosen, candidates):
        if len(chosen) == 7:
            return True
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            q = bit.bit_length() - 1
            next_candidates = candidates
            triples = list(combinations(chosen + [q], 3))
            for triple in triples:
                next_candidates &= triple_masks[triple]
                if not next_candidates:
                    break
            if len(chosen) + 1 == 7:
                return True
            if next_candidates and extend(chosen + [q], next_candidates):
                return True
        return False

    if n < 7:
        return False
    # Start with each increasing triple; each candidate mask is restricted to
    # indices above the last selected point, so every subset is visited once.
    for i, j, k in combinations(range(n), 3):
        candidates = ((1 << n) - 1) ^ ((1 << (k + 1)) - 1)
        candidates &= triple_masks[(i, j, k)]
        if candidates and extend([i, j, k], candidates):
            return True
    return False


def validate(solution, config, strict=False):
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    parameters = config.get("parameters", config)
    if not isinstance(parameters, dict) or parameters.get("forbidden_convex_polygon_vertices") != 7:
        raise ValueError("configuration must forbid a convex 7-gon")
    raw_points = solution.get("points")
    if not isinstance(raw_points, list):
        raise ValueError("points must be a list")
    points = []
    for point in raw_points:
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise ValueError("each point must have two coordinates")
        points.append((_coordinate(point[0]), _coordinate(point[1])))
    if len(set(points)) != len(points):
        raise ValueError("points must be distinct")
    for a, b, c in combinations(points, 3):
        if _orient(a, b, c) == 0:
            raise ValueError("every three points must be noncollinear")
    if _has_convex_seven(points):
        raise ValueError("point set contains a convex 7-gon")
    return {
        "objective": len(points),
        "verification_status": "exact",
        "details": {"point_count": len(points), "general_position": True,
                    "convex_seven_gon": False, "claimed_objective_ignored": True},
    }
