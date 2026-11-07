"""Exact rational checker for Thomson energy on the unit sphere."""

from fractions import Fraction
import math


def _q(value):
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("coordinates must be finite")
        return Fraction.from_float(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("coordinates must be rational strings") from exc
    raise ValueError("coordinates must be integers, finite floats, or rational strings")


def _sphere_point(pair):
    if not isinstance(pair, (list, tuple)) or len(pair) != 2:
        raise ValueError("each stereographic point needs two parameters")
    u, v = (_q(item) for item in pair)
    d = 1 + u * u + v * v
    return (2 * u / d, 2 * v / d, (1 - u * u - v * v) / d)


def _sqrt_bounds(q, scale):
    """Return rational bounds lo <= sqrt(q) <= hi for q > 0."""
    if q <= 0:
        raise ValueError("points must be distinct")
    # floor(scale * sqrt(a/b)) = floor(sqrt(a*b*scale**2) / b).
    a, b = q.numerator, q.denominator
    floor_scaled = math.isqrt(a * b * scale * scale) // b
    return Fraction(floor_scaled, scale), Fraction(floor_scaled + 1, scale)


CONFIG_N = {"T021-C01": 32, "T021-C02": 40, "T021-C03": 50}

def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("id") not in CONFIG_N:
        raise ValueError("unsupported T021 configuration")
    n = CONFIG_N[config["id"]]
    expected_parameters = {
        "n": n,
        "space": "unit sphere S2",
        "potential": "sum over unordered pairs 1 / Euclidean distance",
        "objective_unit": "Coulomb energy in unit-charge, unit-radius units",
    }
    if config.get("parameters") != expected_parameters:
        raise ValueError("unsupported T021 configuration")
    if not isinstance(solution, dict) or not isinstance(solution.get("points"), (list, tuple)):
        raise ValueError("solution must contain stereographic points")
    raw = solution["points"]
    if len(raw) != n:
        raise ValueError(f"expected exactly {n} points")
    points = [_sphere_point(pair) for pair in raw]

    # Recheck the defining equation with exact arithmetic, even though the
    # parameterization makes it hold algebraically.
    for point in points:
        if sum(x * x for x in point) != 1:
            raise ValueError("point is not exactly on the unit sphere")

    scale = 10**25
    output_scale = 10**30
    lower_units = 0
    upper_units = 0
    pair_count = 0
    for i in range(n):
        for j in range(i):
            squared_distance = sum((points[i][k] - points[j][k]) ** 2 for k in range(3))
            if squared_distance <= 0:
                raise ValueError("points must be distinct")
            # Energy contribution is sqrt(1 / squared_distance). Bounding
            # this directly also handles distinct points that are extremely
            # close, where a lower distance bound at fixed precision is zero.
            term_lower, term_upper = _sqrt_bounds(1 / squared_distance, scale)
            lower_units += (term_lower.numerator * output_scale) // term_lower.denominator
            upper_units += -(-term_upper.numerator * output_scale // term_upper.denominator)
            pair_count += 1

    lower = Fraction(lower_units, output_scale)
    upper = Fraction(upper_units, output_scale)
    interval = [str(lower), str(upper)]
    return {
        "objective": str(upper),
        "objective_value": str(upper),
        "verification_status": "certified",
        "details": {
            "objective_interval": interval,
            "point_count": n,
            "pairs_checked": pair_count,
            "coordinate_model": "exact rational stereographic projection",
            "sqrt_bound_scale": str(scale),
            "energy_bound_scale": str(output_scale),
            "claimed_score_ignored": True,
        },
    }
