"""Exact checker for T005 Heilbronn configurations in the unit square."""
from fractions import Fraction
from itertools import combinations
import math


def _fraction(value):
    if isinstance(value, bool):
        raise ValueError("boolean coordinates are invalid")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("coordinates must be finite")
        return Fraction(str(value))
    raise TypeError("coordinates must be integers, decimal strings, or finite floats")


def triangle_area2(a, b, c):
    return abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))


def validate(solution, config, strict=False):
    parameters = config.get("parameters", {}) if isinstance(config, dict) else {}
    n = parameters.get("n")
    if not isinstance(n, int) or isinstance(n, bool) or n < 3:
        raise ValueError("configuration must specify an integer n>=3")
    points = solution.get("points") if isinstance(solution, dict) else solution
    if not isinstance(points, (list, tuple)) or len(points) != n:
        raise ValueError(f"solution must contain exactly {n} points")
    parsed = []
    for point in points:
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise ValueError("each point must have two coordinates")
        xy = tuple(_fraction(v) for v in point)
        if any(v < 0 or v > 1 for v in xy):
            raise ValueError("all points must lie in the unit square")
        parsed.append(xy)
    if len(set(parsed)) != n:
        raise ValueError("points must be distinct")
    value = min(triangle_area2(*triple) for triple in combinations(parsed, 3)) / 2
    return {
        "objective": str(value),
        "verification_status": "exact",
        "details": {"triangles_checked": len(parsed) * (len(parsed)-1) * (len(parsed)-2) // 6},
    }
