"""Exact-input and interval-certified checker for selected directions on S^2."""
from fractions import Fraction
import math

_OBJECTIVE = "minimum pairwise angular separation in radians"
_CONFIGS = {f"T004-C{cid}": {"n": n, "space": "S2", "objective": _OBJECTIVE} for cid,n in (("01",16),("02",17),("03",19))}

def _q(value):
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except Exception as exc:
            raise ValueError("invalid rational coordinate") from exc
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("coordinates must be finite")
        return Fraction.from_float(value)
    raise ValueError("coordinates must be integers, finite floats, or rational strings")

def _get_interval_module():
    try:
        from mpmath import iv
        return iv
    except Exception as exc:
        raise ValueError("interval arithmetic is required for strict verification") from exc

def _fraction_interval(iv, q):
    # Enclose numerator and denominator separately, then divide as intervals.
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)

def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("id") not in _CONFIGS or config.get("parameters") != _CONFIGS[config.get("id")]:
        raise ValueError("unsupported configuration")
    n_points = _CONFIGS[config["id"]]["n"]
    if not isinstance(solution, dict) or not isinstance(solution.get("points"), (list, tuple)):
        raise ValueError("solution must contain a points list")
    points = solution["points"]
    if len(points) != n_points:
        raise ValueError(f"expected exactly {n_points} points")
    parsed = []
    for point in points:
        if not isinstance(point, (list, tuple)) or len(point) != 3:
            raise ValueError("each point must have three coordinates")
        v = tuple(_q(x) for x in point)
        norm2 = sum((x*x for x in v), Fraction())
        if norm2 == 0:
            raise ValueError("zero vectors do not define directions")
        parsed.append((v, norm2))
    if len({v for v, _ in parsed}) != n_points:
        raise ValueError("duplicate vectors are not allowed")
    # Distinct positive multiples encode the same point on S^2. Detect these
    # exactly by checking zero cross product.
    for i, (a, _) in enumerate(parsed):
        for b, _ in parsed[:i]:
            dot = sum((a[k]*b[k] for k in range(3)), Fraction())
            if dot > 0 and all(a[k]*b[l] == a[l]*b[k] for k,l in ((0,1),(0,2),(1,2))):
                raise ValueError("duplicate directions are not allowed")
    # For each pair, exact rational dot products and squared norms determine
    # the normalized cosine. Its largest value gives the minimum angle.
    pair_data = []
    for i, (a, na) in enumerate(parsed):
        for b, nb in parsed[:i]:
            dot = sum((x*y for x,y in zip(a,b)), Fraction())
            pair_data.append((dot, na, nb))
    iv = _get_interval_module()
    # mpmath interval operations enclose rational conversion and square root.
    # Take the maximum cosine interval first, then evaluate its angle once.
    cos_intervals = []
    for dot, na, nb in pair_data:
        c = _fraction_interval(iv, dot) / iv.sqrt(_fraction_interval(iv, na) * _fraction_interval(iv, nb))
        cos_intervals.append(c)
    max_lo = cos_intervals[0].a
    max_hi = cos_intervals[0].b
    for c in cos_intervals[1:]:
        max_lo = max(max_lo, c.a)
        max_hi = max(max_hi, c.b)
    # Exact normalized cosines lie in [-1, 1]; clipping only removes outward
    # interval-rounding spill beyond these known mathematical bounds.
    max_lo = max(max_lo, iv.mpf(-1).a)
    max_hi = min(max_hi, iv.mpf(1).b)
    cosine_iv = iv.mpf([max_lo, max_hi])
    angle_iv = iv.atan2(iv.sqrt(1 - cosine_iv*cosine_iv), cosine_iv)
    lo = float(angle_iv.a)
    hi = float(angle_iv.b)
    if not (math.isfinite(lo) and math.isfinite(hi) and 0 <= lo <= hi <= math.pi):
        raise ValueError("could not establish a finite angle interval")
    if strict:
        # Outward safety padding covers the final conversion to binary floats.
        lo = math.nextafter(lo, -math.inf)
        hi = math.nextafter(hi, math.inf)
        if lo < 0: lo = 0.0
    return {
        "objective": lo if strict else (lo + hi) / 2,
        "verification_status": "certified" if strict else "numeric",
        "details": {"n": n_points, "pairs_checked": len(pair_data),
                    "objective_name": "minimum_pairwise_angular_separation_radians",
                    "angle_interval": [lo, hi],
                    "directions_normalized_for_scoring": True}
    }
