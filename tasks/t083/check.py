"""Exact checker for four unit equilateral triangles in an axis-aligned square.

Coordinates are pairs [a,b] for a+b*sqrt(3); directions are rational pairs.
"""
from fractions import Fraction
import math


def _bigint_text(value):
    """Format integers in chunks to avoid Python's decimal-digit guard."""
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    value = abs(value)
    chunks = []
    while value:
        value, part = divmod(value, 10**9)
        chunks.append(part)
    return sign + str(chunks[-1]) + "".join(f"{part:09d}" for part in reversed(chunks[:-1]))


def _bigint_parse(text):
    if not isinstance(text, str) or not text:
        raise ValueError("invalid rational integer")
    sign = 1
    if text[0] in "+-":
        if text[0] == "-":
            sign = -1
        text = text[1:]
    if not text or not text.isascii() or not text.isdigit():
        raise ValueError("invalid rational integer")
    value = 0
    first = len(text) % 9 or 9
    value = int(text[:first])
    for start in range(first, len(text), 9):
        value = value * 10**9 + int(text[start:start + 9])
    return sign * value


def _rational_parse(value):
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    if not isinstance(value, str):
        raise ValueError("rational values must be integer or fraction strings")
    if value.count("/") > 1:
        raise ValueError("invalid rational string")
    if "/" in value:
        left, right = value.split("/")
        denominator = _bigint_parse(right)
        if denominator == 0:
            raise ValueError("zero rational denominator")
        return Fraction(_bigint_parse(left), denominator)
    return Fraction(_bigint_parse(value))


class Q:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a, self.b = _rational_parse(a), _rational_parse(b)

    @staticmethod
    def parse(value):
        if isinstance(value, Q):
            return value
        if type(value) is int:
            return Q(value)
        if isinstance(value, Fraction):
            return Q(value)
        if isinstance(value, str):
            try:
                return Q(_rational_parse(value))
            except (ValueError, ZeroDivisionError) as exc:
                raise ValueError("rational coefficients must be exact strings") from exc
        if isinstance(value, (list, tuple)) and len(value) == 2:
            if not all(isinstance(x, (str, int)) and type(x) is not bool for x in value):
                raise ValueError("Q(sqrt(3)) values need two rational coefficients")
            try:
                return Q(_rational_parse(value[0]), _rational_parse(value[1]))
            except (ValueError, ZeroDivisionError) as exc:
                raise ValueError("invalid rational coefficient") from exc
        raise ValueError("exact values must be rational strings or [a,b] pairs")

    def __add__(x, y):
        y = Q.parse(y)
        return Q(x.a + y.a, x.b + y.b)

    __radd__ = __add__

    def __neg__(x):
        return Q(-x.a, -x.b)

    def __sub__(x, y):
        return x + -Q.parse(y)

    def __rsub__(x, y):
        return Q.parse(y) - x

    def __mul__(x, y):
        y = Q.parse(y)
        return Q(x.a * y.a + 3 * x.b * y.b, x.a * y.b + x.b * y.a)

    __rmul__ = __mul__

    def __truediv__(x, y):
        y = Q.parse(y)
        den = y.a * y.a - 3 * y.b * y.b
        if not den:
            raise ZeroDivisionError
        return Q((x.a * y.a - 3 * x.b * y.b) / den,
                 (x.b * y.a - x.a * y.b) / den)

    def sign(x):
        a, b = x.a, x.b
        if not a:
            return (b > 0) - (b < 0)
        if not b:
            return (a > 0) - (a < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        delta = a * a - 3 * b * b
        if a > 0:
            return (delta > 0) - (delta < 0)
        return -((delta > 0) - (delta < 0))

    def __lt__(x, y):
        return (x - Q.parse(y)).sign() < 0

    def __le__(x, y):
        return (x - Q.parse(y)).sign() <= 0

    def __eq__(x, y):
        try:
            y = Q.parse(y)
        except ValueError:
            return False
        return x.a == y.a and x.b == y.b

    def __str__(x):
        def frac(v):
            return _bigint_text(v.numerator) if v.denominator == 1 else f"{_bigint_text(v.numerator)}/{_bigint_text(v.denominator)}"
        return f"[{frac(x.a)},{frac(x.b)}]"


PARAMETERS = {
    "triangle_count": 4,
    "triangle_side": 1,
    "container": "axis-aligned square with lower-left corner (0,0)",
    "pose_domain": "dense Q(sqrt(3)) translations and rational unit directions",
}


def _min(values):
    out = values[0]
    for value in values[1:]:
        if value < out:
            out = value
    return out


def _max(values):
    out = values[0]
    for value in values[1:]:
        if out < value:
            out = value
    return out


def _triangle(record):
    if not isinstance(record, dict) or set(record) != {"anchor", "direction"}:
        raise ValueError("each triangle needs exactly anchor and direction")
    anchor, direction = record["anchor"], record["direction"]
    if not isinstance(anchor, (list, tuple)) or len(anchor) != 2:
        raise ValueError("anchor must contain two exact coordinates")
    if not isinstance(direction, (list, tuple)) or len(direction) != 2:
        raise ValueError("direction must contain two rational coordinates")
    p0 = tuple(Q.parse(c) for c in anchor)
    if any(isinstance(c, (list, tuple)) and len(c) != 1 for c in direction):
        raise ValueError("direction coefficients must be rational scalars")
    if any(type(c) is bool or not isinstance(c, (str, int)) for c in direction):
        raise ValueError("direction must use rational strings or integers")
    try:
        u, v = (_rational_parse(c) for c in direction)
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        raise ValueError("direction must be rational") from exc
    if u * u + v * v != 1:
        raise ValueError("edge direction must be a rational unit vector")
    p1 = (p0[0] + u, p0[1] + v)
    # Counterclockwise rotation of the unit edge by +60 degrees.
    p2 = (p0[0] + (u - Q(0, v)) / 2,
          p0[1] + (v + Q(0, u)) / 2)
    return [p0, p1, p2]


def _separated(poly_a, poly_b):
    for poly in (poly_a, poly_b):
        for i, point in enumerate(poly):
            nxt = poly[(i + 1) % 3]
            axis = (nxt[1] - point[1], point[0] - nxt[0])
            proj_a = [p[0] * axis[0] + p[1] * axis[1] for p in poly_a]
            proj_b = [p[0] * axis[0] + p[1] * axis[1] for p in poly_b]
            if _max(proj_a) <= _min(proj_b) or _max(proj_b) <= _min(proj_a):
                return True
    return False


def _sqrt3_bounds(digits=70):
    scale = 10 ** digits
    root = math.isqrt(3 * scale * scale)
    return Fraction(root, scale), Fraction(root + 1, scale)


def _interval(value):
    low_root, high_root = _sqrt3_bounds()
    lower = value.a + value.b * (low_root if value.b >= 0 else high_root)
    upper = value.a + value.b * (high_root if value.b >= 0 else low_root)
    return lower, upper


def _fraction_text(value):
    return _bigint_text(value.numerator) if value.denominator == 1 else f"{_bigint_text(value.numerator)}/{_bigint_text(value.denominator)}"


def validate(solution, config, strict=False):
    parameters = config.get("parameters") if isinstance(config, dict) else None
    if (not isinstance(config, dict) or config.get("id") != "T083-C01"
            or not isinstance(parameters, dict) or parameters != PARAMETERS
            or any(type(parameters[key]) is not type(value) for key, value in PARAMETERS.items())):
        raise ValueError("unsupported configuration or parameters")
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    if "side" not in solution or not isinstance(solution.get("triangles"), (list, tuple)):
        raise ValueError("solution needs side and triangles")
    side = Q.parse(solution["side"])
    if side.sign() <= 0:
        raise ValueError("square side must be positive")
    raw = solution["triangles"]
    if len(raw) != 4:
        raise ValueError("exactly four triangles are required")
    triangles = [_triangle(record) for record in raw]
    for i in range(4):
        for j in range(i):
            if not _separated(triangles[i], triangles[j]):
                raise ValueError("triangle interiors overlap")
    for tri in triangles:
        for x, y in tri:
            if x.sign() < 0 or y.sign() < 0 or side < x or side < y:
                raise ValueError("triangle vertex lies outside the square")
    lower, upper = _interval(side)
    return {
        "objective": str(side),
        "objective_value": _fraction_text(upper),
        "verification_status": "exact" if not strict else "certified",
        "details": {
            "objective_interval": [_fraction_text(lower), _fraction_text(upper)],
            "exact_side_coefficients": [_fraction_text(side.a), _fraction_text(side.b)],
            "triangle_pairs_checked": 6,
            "claimed_score_ignored": True,
            "domain_note": "Exact Q(sqrt(3)) pose subset; dense in all real poses, so the infimum is unchanged.",
        },
    }
