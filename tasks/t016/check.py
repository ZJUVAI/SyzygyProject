"""Exact verifier for signed 208-step autoconvolution candidates."""
from fractions import Fraction
import math


def _rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, float, Fraction)):
        raise ValueError("coefficients must be integers, finite floats, or rational strings")
    try:
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("coefficient floats must be finite")
        return Fraction(value)
    except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
        raise ValueError("coefficients must be finite rational values") from exc


def validate(solution, config, strict=False):
    # Every accepted score is exact. `strict` is retained for runner compatibility.
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    params = config.get("parameters", config)
    expected = {
        "steps": 208,
        "support": ["-1/4", "1/4"],
        "signed_values_allowed": True,
        "integral": 1,
    }
    if not isinstance(params, dict) or any(params.get(k) != v for k, v in expected.items()):
        raise ValueError("configuration must be T016-C01: 208 signed steps on [-1/4,1/4], integral 1")
    coeff = solution.get("coefficients")
    if not isinstance(coeff, list) or len(coeff) != 208:
        raise ValueError("coefficients must contain exactly 208 values")
    values = [_rational(x) for x in coeff]
    mass = sum(values, Fraction(0))
    if mass == 0:
        raise ValueError("coefficient mass must be nonzero")
    # A constant step height on each of 208 equal bins has integral proportional
    # to this mass. Normalization to integral one cancels in the formula below.
    conv = [
        sum((values[i] * values[k-i]
             for i in range(max(0, k-207), min(207, k)+1)), Fraction(0))
        for k in range(415)
    ]
    peak = max(abs(x) for x in conv)
    objective = Fraction(416) * peak / (mass * mass)
    peak_indices = [i for i, x in enumerate(conv) if abs(x) == peak]
    return {
        "objective": str(objective),
        "verification_status": "exact",
        "details": {
            "steps": 208,
            "coefficient_count": 208,
            "mass": str(mass),
            "max_abs_convolution": str(peak),
            "max_abs_indices": peak_indices,
            "normalization": "integral-one normalization; objective is invariant under nonzero scaling",
            "objective_definition": "416 * max_k(abs(sum_i a_i*a_(k-i))) / (sum_i a_i)^2",
        },
    }
