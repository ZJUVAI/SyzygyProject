"""Exact checker for the 51-bin minimum-overlap construction."""
from fractions import Fraction
import math

STEPS = 51
EXPECTED = {"steps": 51, "support": "[0,2]", "range": "0≤f≤1", "integral": 1}


def _fraction(value):
    if isinstance(value, bool):
        raise ValueError("boolean heights are invalid")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("heights must be finite")
        return Fraction(str(value))
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("height strings must be rational") from exc
    raise ValueError("heights must be rational numbers")


def lag_integral(heights, lag):
    """Integral at t=lag*2/51; both functions vanish outside [0,2]."""
    n = len(heights)
    return Fraction(2, n) * sum(
        (heights[i] * (1 - heights[i + lag])
         for i in range(n) if 0 <= i + lag < n), Fraction(0))


def objective_fraction(heights):
    # The cross-correlation of two uniform-bin step functions is linear
    # between successive bin-difference knots. Its maximum is at a knot.
    profile = [(lag, lag_integral(heights, lag))
               for lag in range(-(len(heights)-1), len(heights))]
    lag, value = max(profile, key=lambda item: item[1])
    return value, lag, profile


def validate(solution, config, strict=False):
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    params = config.get("parameters", config)
    if params != EXPECTED:
        raise ValueError("configuration must be T017-C01 (51 equal bins on [0,2])")
    raw = solution.get("heights")
    if not isinstance(raw, list) or len(raw) != STEPS:
        raise ValueError("heights must contain exactly 51 entries")
    heights = [_fraction(x) for x in raw]
    if any(x < 0 or x > 1 for x in heights):
        raise ValueError("each height must lie in [0,1]")
    mass = Fraction(2, STEPS) * sum(heights, Fraction(0))
    if mass != 1:
        raise ValueError("integral must equal exactly 1")
    value, lag, profile = objective_fraction(heights)
    return {"objective": str(value), "verification_status": "exact",
            "details": {"objective_fraction": str(value), "objective_float": float(value),
                        "integral": str(mass), "maximizing_lag_bins": lag,
                        "maximizing_shift": str(Fraction(2*lag, STEPS)),
                        "lag_profile": [str(v) for _, v in profile],
                        "profile_lags": [k for k, _ in profile],
                        "piecewise_linear_certificate": "cross-correlation is linear between bin-difference knots; endpoints and zero exterior are included"}}
