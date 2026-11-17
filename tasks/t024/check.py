"""Exact checker for subsets of the 100 by 100 integer grid."""
from collections.abc import Mapping
from typing import Any

CONFIG_ID = "T024-C01"
N = 100

def _d2(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def validate(solution: Any, config: Mapping[str, Any], strict: bool = False) -> dict[str, Any]:
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError("unsupported configuration")
    if config.get("parameters") != {"grid_size": N}:
        raise ValueError("configuration parameters do not match T024-C01")
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")
    points = solution.get("points")
    if not isinstance(points, (list, tuple, set, frozenset)):
        raise ValueError("points must be a list or set")
    clean = []
    for p in points:
        if not isinstance(p, (list, tuple)) or len(p) != 2 or any(type(v) is not int for v in p):
            raise ValueError("each point must be a pair of integers")
        x, y = p
        if not (0 <= x < N and 0 <= y < N):
            raise ValueError("point outside the zero-based 100 by 100 grid")
        clean.append((x, y))
    if len(set(clean)) != len(clean):
        raise ValueError("points must be distinct")
    # An isosceles triangle exists exactly when some vertex has two other
    # points at equal squared distance. This also rejects collinear midpoint triples.
    checks = 0
    for i, a in enumerate(clean):
        seen = set()
        for j, b in enumerate(clean):
            if i == j: continue
            d = _d2(a, b); checks += 1
            if d in seen:
                raise ValueError("two points have equal squared distance from one vertex")
            seen.add(d)
    return {"objective": len(clean), "verification_status": "exact", "details": {"point_count": len(clean), "apex_distance_checks": checks, "claimed_objective_ignored": True, "strict_full_domain_check": True}}
