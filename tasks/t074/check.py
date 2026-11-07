"""Exact checker for the free-convex-domain 12-point Heilbronn task."""

from collections.abc import Mapping
from fractions import Fraction
from itertools import combinations
import math
import sys


sys.set_int_max_str_digits(0)

CONFIG_ID = "T074-C01"
POINT_COUNT = 12
PARAMETERS = {
    "point_count": 12,
    "coordinate_domain": "unbounded rational coordinates in the plane",
    "container": "convex hull of the selected points",
    "objective": "minimum_triangle_area / convex_hull_area",
    "no_three_collinear": True,
}


def _fraction(value):
    if isinstance(value, bool):
        raise ValueError("boolean coordinates are invalid")
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("coordinate strings must encode exact rational numbers") from exc
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("coordinates must be finite")
        return Fraction(str(value))
    raise ValueError("coordinates must be integers, rational strings, or finite floats")


def _cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _convex_hull(points):
    ordered = sorted(points)
    lower = []
    for point in ordered:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(ordered):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    hull = lower[:-1] + upper[:-1]
    if len(hull) < 3:
        raise ValueError("the convex hull must have positive area")
    return hull


def _twice_polygon_area(vertices):
    return abs(sum(
        vertices[i][0] * vertices[(i + 1) % len(vertices)][1]
        - vertices[(i + 1) % len(vertices)][0] * vertices[i][1]
        for i in range(len(vertices))
    ))


def _check_config(config):
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix the unbounded rational free-convex n=12 problem")


def validate(solution, config, strict=False):
    """Check all constraints and return the exact area ratio as a fraction string."""
    _check_config(config)
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")
    raw_points = solution.get("points")
    if not isinstance(raw_points, (list, tuple)) or len(raw_points) != POINT_COUNT:
        raise ValueError("solution must contain exactly 12 points")
    points = []
    for index, point in enumerate(raw_points):
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise ValueError(f"point {index} must contain two coordinates")
        points.append((_fraction(point[0]), _fraction(point[1])))
    if len(set(points)) != POINT_COUNT:
        raise ValueError("points must be distinct")

    minimum_twice_area = None
    for triple in combinations(points, 3):
        twice_area = abs(_cross(*triple))
        if twice_area == 0:
            raise ValueError("no three points may be collinear")
        if minimum_twice_area is None or twice_area < minimum_twice_area:
            minimum_twice_area = twice_area

    hull = _convex_hull(points)
    hull_twice_area = _twice_polygon_area(hull)
    if hull_twice_area <= 0:
        raise ValueError("the convex hull must have positive area")
    minimum_area = minimum_twice_area / 2
    hull_area = Fraction(hull_twice_area, 2)
    ratio = minimum_area / hull_area
    return {
        "objective": str(ratio),
        "verification_status": "exact",
        "details": {
            "point_count": POINT_COUNT,
            "triangles_checked": POINT_COUNT * (POINT_COUNT - 1) * (POINT_COUNT - 2) // 6,
            "minimum_triangle_area": str(minimum_area),
            "convex_hull_area": str(hull_area),
            "hull_vertex_count": len(hull),
            "claimed_objective_ignored": True,
            "strict": bool(strict),
        },
    }
