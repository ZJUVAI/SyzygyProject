"""Exact checker for the 12-point planar max/min squared-distance ratio."""

from fractions import Fraction
import re
import sys


CONFIG_ID = "T081-C01"
POINT_COUNT = 12
PARAMETERS = {
    "dimension": 2,
    "point_count": POINT_COUNT,
    "coordinates": "exact rational numbers",
    "constraint": "all points are distinct",
    "objective": "maximum squared pair distance divided by minimum squared pair distance",
}
_RATIONAL_RE = re.compile(r"(?:0|-[1-9][0-9]*|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def _as_fraction(value, label):
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, str) and _RATIONAL_RE.fullmatch(value):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError(f"{label} is not a valid rational number") from exc
    raise ValueError(f"{label} must be an integer or exact rational string")


def _check_config(config):
    if not isinstance(config, dict) or config.get("id") != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must specify 12 distinct points in the plane")


def _parse_points(solution):
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    raw = solution.get("points")
    if not isinstance(raw, list) or len(raw) != POINT_COUNT:
        raise ValueError(f"points must be a list of exactly {POINT_COUNT} coordinate pairs")
    points = []
    for i, point in enumerate(raw):
        if not isinstance(point, list) or len(point) != 2:
            raise ValueError(f"point {i} must contain exactly two coordinates")
        points.append((_as_fraction(point[0], f"points[{i}][0]"),
                       _as_fraction(point[1], f"points[{i}][1]")))
    return points


def validate(solution, config, strict=False):
    del strict
    _check_config(config)
    points = _parse_points(solution)
    squared_distances = []
    for i in range(POINT_COUNT):
        for j in range(i + 1, POINT_COUNT):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            distance_squared = dx * dx + dy * dy
            if distance_squared == 0:
                raise ValueError(f"points {i} and {j} coincide")
            squared_distances.append(distance_squared)
    minimum = min(squared_distances)
    maximum = max(squared_distances)
    ratio = maximum / minimum
    objective = ratio.numerator if ratio.denominator == 1 else str(ratio)
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "dimension": 2,
            "point_count": POINT_COUNT,
            "pair_distances_verified": len(squared_distances),
            "minimum_squared_distance": str(minimum),
            "maximum_squared_distance": str(maximum),
            "minimum_distance_pair_count": squared_distances.count(minimum),
            "maximum_distance_pair_count": squared_distances.count(maximum),
            "claimed_objective_ignored": True,
        },
    }
