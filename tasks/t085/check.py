"""Exact continuous-coverage checker for 21 unit disks covering a disk.

Centers and target radius are rational. Coverage is certified by enumerating
the vertices and boundary extrema of the restricted Voronoi diagram.
"""
from fractions import Fraction
from itertools import combinations
import math


def _bigint_text(value):
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
        sign = -1 if text[0] == "-" else 1
        text = text[1:]
    if not text or not text.isascii() or not text.isdigit():
        raise ValueError("invalid rational integer")
    first = len(text) % 9 or 9
    value = int(text[:first])
    for start in range(first, len(text), 9):
        value = value * 10**9 + int(text[start:start + 9])
    return sign * value


def _fraction(value):
    if type(value) is int:
        return Fraction(value)
    if not isinstance(value, str) or value.count("/") > 1:
        raise ValueError("coordinates and radius must be rational strings or integers")
    if "/" in value:
        a, b = value.split("/")
        denominator = _bigint_parse(b)
        if denominator == 0:
            raise ValueError("rational denominator cannot be zero")
        return Fraction(_bigint_parse(a), denominator)
    return Fraction(_bigint_parse(value))


def _fraction_text(value):
    return (_bigint_text(value.numerator) if value.denominator == 1
            else f"{_bigint_text(value.numerator)}/{_bigint_text(value.denominator)}")


PARAMETERS = {
    "circle_count": 21,
    "covering_circle_radius": 1,
    "target": "closed disk centered at origin",
    "center_domain": "unbounded rational coordinates",
    "radius_domain": "positive rational",
}


def _norm(p):
    return p[0] * p[0] + p[1] * p[1]


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def _sqrt_sign(a, b, d):
    """Sign of a+b*sqrt(d), where a,b,d are rational and d>=0."""
    if d < 0:
        raise ValueError("negative quadratic radicand")
    if not b or not d:
        return (a > 0) - (a < 0)
    if not a:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    delta = a * a - b * b * d
    if not delta:
        return 0
    return ((a > 0) - (a < 0)) * ((delta > 0) - (delta < 0))


def _covered_rational(p, centers):
    return any(_norm((p[0] - c[0], p[1] - c[1])) <= 1 for c in centers)


def _covered_algebraic(p0, v, d, radius2, centers):
    # p = p0 + v*sqrt(d); compare |p-c|^2 <= 1 without approximation.
    for c in centers:
        a = radius2 + _norm(c) - 1 - 2 * _dot(c, p0)
        b = -2 * _dot(c, v)
        if _sqrt_sign(a, b, d) <= 0:
            return True
    return False


def _critical_counts(centers, radius):
    radius2 = radius * radius
    checked = 0
    # A Voronoi vertex at the origin, if present, is also a candidate.
    checked += 1
    if not _covered_rational((Fraction(0), Fraction(0)), centers):
        return False, checked

    # Interior extrema of the nearest-center distance occur at Voronoi vertices.
    for a, b, c in combinations(centers, 3):
        n = (2 * (b[0] - a[0]), 2 * (b[1] - a[1]))
        m = (2 * (c[0] - a[0]), 2 * (c[1] - a[1]))
        det = n[0] * m[1] - n[1] * m[0]
        if not det:
            continue
        rhs1, rhs2 = _norm(b) - _norm(a), _norm(c) - _norm(a)
        p = ((rhs1 * m[1] - n[1] * rhs2) / det,
             (n[0] * rhs2 - rhs1 * m[0]) / det)
        if _norm(p) <= radius2:
            checked += 1
            if not _covered_rational(p, centers):
                return False, checked

    # Four fixed boundary points cover the case of a center at the origin,
    # whose boundary distance is constant.
    for p in ((radius, 0), (-radius, 0), (0, radius), (0, -radius)):
        checked += 1
        if not _covered_rational(p, centers):
            return False, checked

    # Smooth boundary extrema of distance from each noncentral center.
    for center in centers:
        d = _norm(center)
        if not d:
            continue
        for sign in (-1, 1):
            v = (sign * radius * center[0] / d,
                 sign * radius * center[1] / d)
            checked += 1
            if not _covered_algebraic((0, 0), v, d, radius2, centers):
                return False, checked

    # Boundary changes in the nearest-center identity occur at pair bisectors.
    for a, b in combinations(centers, 2):
        n = (2 * (b[0] - a[0]), 2 * (b[1] - a[1]))
        nn = _norm(n)
        if not nn:
            continue
        rhs = _norm(b) - _norm(a)
        p0 = (rhs * n[0] / nn, rhs * n[1] / nn)
        d = (radius2 - _norm(p0)) / nn
        if d < 0:
            continue
        v = (-n[1], n[0])
        for sign in (-1, 1):
            checked += 1
            if not _covered_algebraic(p0, (sign * v[0], sign * v[1]), d, radius2, centers):
                return False, checked
    return True, checked


def validate(solution, config, strict=False):
    parameters = config.get("parameters") if isinstance(config, dict) else None
    if (not isinstance(config, dict) or config.get("id") != "T085-C01"
            or not isinstance(parameters, dict) or parameters != PARAMETERS
            or any(type(parameters[k]) is not type(v) for k, v in PARAMETERS.items())):
        raise ValueError("unsupported configuration or parameters")
    if not isinstance(solution, dict) or not isinstance(solution.get("centers"), (list, tuple)):
        raise ValueError("solution must contain a centers list")
    raw = solution["centers"]
    if len(raw) != 21:
        raise ValueError("exactly 21 unit-circle centers are required")
    centers = []
    for center in raw:
        if not isinstance(center, (list, tuple)) or len(center) != 2:
            raise ValueError("each center must have two rational coordinates")
        centers.append((_fraction(center[0]), _fraction(center[1])))
    try:
        radius = _fraction(solution["radius"])
    except KeyError as exc:
        raise ValueError("solution must provide a radius") from exc
    if radius <= 0:
        raise ValueError("target radius must be positive")
    covered, count = _critical_counts(centers, radius)
    if not covered:
        raise ValueError("unit disks do not cover the full target disk")
    return {
        "objective": _fraction_text(radius),
        "verification_status": "exact",
        "details": {
            "circle_count": 21,
            "target_radius": _fraction_text(radius),
            "critical_points_checked": count,
            "coverage_certificate": "All restricted Voronoi vertices, pair-bisector boundary crossings, boundary distance extrema, and fixed boundary representatives were checked exactly.",
            "claimed_score_ignored": True,
        },
    }
