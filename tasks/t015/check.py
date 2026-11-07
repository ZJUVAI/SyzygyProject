"""Exact checker for T015's equally spaced step-function AC2 objective."""
from fractions import Fraction
import math


def _fraction(value):
    if isinstance(value, bool):
        raise ValueError("boolean coefficients are invalid")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("coefficient must be finite")
        return Fraction(str(value))
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("coefficient string must represent a rational") from exc
    raise ValueError("coefficients must be rational numbers")


def objective_fraction(coefficients):
    b = [sum((coefficients[j] * coefficients[k-j]
              for j in range(max(0, k-len(coefficients)+1), min(k, len(coefficients)-1)+1)), Fraction(0))
         for k in range(2*len(coefficients)-1)]
    numerator = 2 * sum((x*x for x in b), Fraction(0))
    numerator += sum((b[i]*b[i+1] for i in range(len(b)-1)), Fraction(0))
    denominator = 3 * max(b) * sum(coefficients, Fraction(0))**2
    return numerator / denominator, b


def validate(solution, config, strict=False):
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    params = config.get("parameters", config)
    if not isinstance(params, dict) or params.get("steps") != 20 or params.get("support") != ["-1/4", "1/4"] or params.get("nonnegative") is not True:
        raise ValueError("configuration must be T015-C01 (20 steps on [-1/4, 1/4])")
    raw = solution.get("coefficients")
    if not isinstance(raw, list) or len(raw) != 20:
        raise ValueError("coefficients must be a list of exactly 20 entries")
    coefficients = [_fraction(value) for value in raw]
    if any(value < 0 for value in coefficients):
        raise ValueError("coefficients must be nonnegative")
    mass = sum(coefficients, Fraction(0))
    if mass <= 0:
        raise ValueError("coefficient mass must be positive")
    value, b = objective_fraction(coefficients)
    return {"objective": str(value), "verification_status": "exact",
            "details": {"objective_fraction": str(value), "objective_float": float(value),
                        "mass": str(mass), "convolution": [str(x) for x in b],
                        "steps": 20}}
