"""Exact rational checker for equal circles in a unit square."""
from fractions import Fraction
import math

_CONFIGS = {
    "T001-C01": {"n": 26, "container": "unit square"},
    "T001-C02": {"n": 32, "container": "unit square"},
    "T001-C03": {"n": 50, "container": "unit square"},
}


def _q(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Fraction)):
        raise ValueError(f"{label} must be an integer, finite float, or decimal string")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{label} must be finite")
    try:
        return value if isinstance(value, Fraction) else Fraction(str(value))
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"{label} is not a valid finite number") from None


def validate(solution, config, strict=False):
    if not isinstance(config, dict):
        raise ValueError("unsupported configuration")
    cid = config.get("id")
    n = _CONFIGS.get(cid)
    if n is None or config.get("parameters") != n:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    centers = solution.get("centers")
    if not isinstance(centers, (list, tuple)) or len(centers) != n["n"]:
        raise ValueError(f"centers must contain exactly {n['n']} points")
    radius = _q(solution.get("radius"), "radius")
    if radius <= 0 or radius > Fraction(1, 2):
        raise ValueError("radius must be in (0, 1/2]")
    points = []
    for i, point in enumerate(centers):
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise ValueError(f"center {i} must have two coordinates")
        x, y = (_q(point[j], f"center {i} coordinate {j}") for j in range(2))
        if not (radius <= x <= 1-radius and radius <= y <= 1-radius):
            raise ValueError(f"center {i} violates square boundary clearance")
        points.append((x, y))
    required = (2*radius)**2
    for i, (x1, y1) in enumerate(points):
        for j in range(i):
            x2, y2 = points[j]
            if (x1-x2)**2 + (y1-y2)**2 < required:
                raise ValueError(f"centers {j} and {i} overlap")
    return {"objective": str(radius), "verification_status": "exact", "details": {
        "n": n["n"], "all_boundary_clearances_exact": True,
        "all_pairwise_distances_exact": True,
        "optimality_proved": False}}
