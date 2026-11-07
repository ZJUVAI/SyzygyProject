"""Reconstruct the archived free-convex 12-point record from source decimals."""

from fractions import Fraction
import json
from pathlib import Path


SOURCE = Path(__file__).resolve().parent / "data" / "source" / "tejstead_convex_n12.json"
RATIONAL_DENOMINATOR_LIMIT = 100


def reconstruct_rational_points(source_path=SOURCE):
    """Affine-normalize the first three source points, then rationalize to denominator <=100."""
    record = json.loads(Path(source_path).read_text(encoding="utf-8"))
    raw = record.get("points")
    if record.get("n") != 12 or not isinstance(raw, list) or len(raw) != 12:
        raise ValueError("archived source must contain the 12-point convex record")
    points = []
    for point in raw:
        if not isinstance(point, list) or len(point) != 2:
            raise ValueError("source point must contain two decimal coordinate strings")
        points.append((Fraction(str(point[0])), Fraction(str(point[1]))))

    origin, first, second = points[:3]
    ax, ay = first[0] - origin[0], first[1] - origin[1]
    bx, by = second[0] - origin[0], second[1] - origin[1]
    determinant = ax * by - ay * bx
    if determinant == 0:
        raise ValueError("the first three source points must be non-collinear")

    normalized = []
    for x, y in points:
        dx, dy = x - origin[0], y - origin[1]
        u = (dx * by - dy * bx) / determinant
        v = (ax * dy - ay * dx) / determinant
        normalized.append((u.limit_denominator(RATIONAL_DENOMINATOR_LIMIT),
                           v.limit_denominator(RATIONAL_DENOMINATOR_LIMIT)))
    return {"points": [[str(x), str(y)] for x, y in normalized]}
