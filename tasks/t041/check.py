"""Exact rational checker for 17 squares in the closed unit square.

Each square is encoded by its centre, side, and rational unit edge direction
(`cos`, `sin`). This gives exact rational corners and exact separating-axis
tests. Decimal floats are interpreted as their exact binary rational values.
"""
from fractions import Fraction
import math

_CONFIG = {
    "id": "T041-C01",
    "parameters": {
        "square_count": 17,
        "container": "closed unit square [0,1]^2",
        "orientation": "arbitrary",
        "interior_disjoint": True,
        "objective": "sum of the 17 side lengths",
    },
}


def _q(value, label):
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError(f"{label} must be a rational number") from exc
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError(f"{label} must be finite")
        return Fraction.from_float(value)
    raise ValueError(f"{label} must be an integer, finite float, or rational string")


def _square(raw):
    if not isinstance(raw, dict):
        raise ValueError("each square must be an object")
    required = {"x", "y", "side", "cos", "sin"}
    if set(raw) != required:
        raise ValueError(f"each square must have exactly {sorted(required)}")
    x, y, side, c, s = (_q(raw[k], k) for k in ("x", "y", "side", "cos", "sin"))
    if side <= 0:
        raise ValueError("square side lengths must be positive")
    if c*c + s*s != 1:
        raise ValueError("orientation must be an exact rational unit vector")
    return x, y, side, c, s


def _corners(square):
    x, y, side, c, s = square
    hx, hy = side*c/2, side*s/2
    vx, vy = -side*s/2, side*c/2
    return tuple((x + a*hx + b*vx, y + a*hy + b*vy)
                 for a, b in ((-1,-1),(-1,1),(1,-1),(1,1)))


def _separated(a, b):
    """Return true iff some exact square-edge axis separates interiors."""
    ax, ay, _, ac, ass = a
    bx, by, _, bc, bs = b
    dx, dy = bx-ax, by-ay
    for ux, uy in ((ac, ass), (-ass, ac), (bc, bs), (-bs, bc)):
        # These are unit edge directions; the corresponding normal axis is
        # obtained by a quarter turn. A quarter turn preserves dot magnitudes.
        distance = abs(dx*ux + dy*uy)
        ra = a[2] * (abs(ux*ac + uy*ass) + abs(ux*(-ass) + uy*ac)) / 2
        rb = b[2] * (abs(ux*bc + uy*bs) + abs(ux*(-bs) + uy*bc)) / 2
        if distance >= ra + rb:
            return True
    return False


def validate(solution, config, strict=False):
    if (not isinstance(config, dict) or config.get("id") != _CONFIG["id"]
            or config.get("parameters") != _CONFIG["parameters"]):
        raise ValueError("unsupported T041 configuration")
    if not isinstance(solution, dict) or not isinstance(solution.get("squares"), (list, tuple)):
        raise ValueError("solution must contain a squares list")
    items = solution["squares"]
    if len(items) != 17:
        raise ValueError("expected exactly 17 squares")
    squares = [_square(raw) for raw in items]
    for index, square in enumerate(squares):
        for x, y in _corners(square):
            if not (0 <= x <= 1 and 0 <= y <= 1):
                raise ValueError(f"square {index} is not contained in the unit square")
    pair_count = 0
    for i, a in enumerate(squares):
        for j in range(i):
            pair_count += 1
            if not _separated(a, squares[j]):
                raise ValueError(f"squares {j} and {i} have intersecting interiors")
    total = sum((sq[2] for sq in squares), Fraction())
    value = str(total.numerator) if total.denominator == 1 else f"{total.numerator}/{total.denominator}"
    return {
        "objective": value,
        "objective_value": value,
        "verification_status": "exact",
        "details": {
            "square_count": len(squares),
            "pairs_checked": pair_count,
            "corners_checked": 68,
            "objective_name": "sum_of_side_lengths",
            "touching_allowed": True,
            "arithmetic": "exact rational arithmetic",
            "claimed_objective_ignored": True,
            "strict": bool(strict),
        },
    }
