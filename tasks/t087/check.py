"""Exact checker for rational step-function autocorrelation."""

from fractions import Fraction
import math
import re

N = 480
D = Fraction(13, 4800)
W = Fraction(13, 10)
END_K = 369
END_PART = Fraction(3, 13)
_RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")


def _height(value):
    if isinstance(value, bool):
        raise ValueError("heights must be nonnegative rational numbers")
    if isinstance(value, int):
        out = Fraction(value)
    elif isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("heights must be finite")
        out = Fraction.from_float(value)
    elif isinstance(value, str) and _RATIONAL.fullmatch(value):
        out = Fraction(value)
    else:
        raise ValueError("each height must be an integer, finite float, or rational string")
    if out < 0:
        raise ValueError("heights must be nonnegative")
    return out


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("id") != "T087-C01":
        raise ValueError("unknown T087 configuration")
    parameters = config.get("parameters")
    if (not isinstance(parameters, dict)
            or set(parameters) != {"steps", "step_size", "support", "height_domain"}
            or type(parameters.get("steps")) is not int
            or parameters.get("steps") != N
            or parameters.get("step_size") != "13/4800"
            or parameters.get("support") != "13/10"
            or parameters.get("height_domain") != "nonnegative_rational"):
        raise ValueError("T087-C01 parameters must match the frozen configuration exactly")
    raw = solution.get("heights") if isinstance(solution, dict) else solution
    if not isinstance(raw, (list, tuple)) or len(raw) != N:
        raise ValueError("solution must contain exactly 480 step heights")
    heights = [_height(value) for value in raw]
    mass_sum = sum(heights, Fraction())
    if mass_sum <= 0:
        raise ValueError("the function must have positive L1 mass")

    # For t=(k+theta)d, the autocorrelation is linear in theta.
    # Thus its minimum on [0,1] is at a node k*d, k=0..369, or at t=1.
    correlations = []
    for lag in range(N):
        value = sum((heights[i] * heights[i + lag]
                     for i in range(N - lag)), Fraction())
        correlations.append(value)
    candidates = [(correlations[k], {"type": "grid_node", "k": k})
                  for k in range(END_K + 1)]
    endpoint_g = ((1 - END_PART) * correlations[END_K]
                  + END_PART * correlations[END_K + 1])
    candidates.append((endpoint_g, {"type": "endpoint", "t": "1"}))
    min_g, minimum_at = min(candidates, key=lambda item: item[0])
    min_autocorrelation = D * min_g
    l1_norm = D * mass_sum
    objective = min_autocorrelation / (l1_norm * l1_norm)
    objective_text = f"{objective.numerator}/{objective.denominator}"
    return {
        "objective": objective_text,
        "objective_value": objective_text,
        "verification_status": "exact",
        "details": {
            "steps": N,
            "step_size": str(D),
            "support_length": str(W),
            "l1_norm": f"{l1_norm.numerator}/{l1_norm.denominator}",
            "minimum_autocorrelation": (
                f"{min_autocorrelation.numerator}/{min_autocorrelation.denominator}"),
            "minimum_location": minimum_at,
            "continuous_interval_check": "all 370 grid nodes and t=1 exact interpolation",
            "claimed_objective_ignored": True,
        },
    }
