"""Exact rational validator for circles in the unit square."""
from fractions import Fraction
import math

_CONFIGS = {"T005-C01": 26, "T005-C02": 32}

def _q(value):
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except Exception as exc:
            raise ValueError("invalid rational") from exc
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite number")
        return Fraction.from_float(value)
    raise ValueError("values must be integers, finite floats, or rational strings")

def validate(solution, config, strict=False):
    config_id = config.get("id")
    n = _CONFIGS.get(config_id)
    if n is None:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict) or not isinstance(solution.get("circles"), (list, tuple)):
        raise ValueError("solution must contain circles")
    circles = solution["circles"]
    if len(circles) != n:
        raise ValueError(f"expected exactly {n} circles")
    parsed = []
    for circle in circles:
        if not isinstance(circle, dict) or not all(k in circle for k in ("x", "y", "r")):
            raise ValueError("each circle needs x, y, and r")
        x, y, r = (_q(circle[k]) for k in ("x", "y", "r"))
        if r <= 0:
            raise ValueError("radii must be positive")
        if x-r < 0 or x+r > 1 or y-r < 0 or y+r > 1:
            raise ValueError("circle crosses the unit-square wall")
        parsed.append((x, y, r))
    for i, (x1, y1, r1) in enumerate(parsed):
        for x2, y2, r2 in parsed[:i]:
            if (x1-x2)**2 + (y1-y2)**2 < (r1+r2)**2:
                raise ValueError("circle interiors overlap")
    objective = sum((r for _, _, r in parsed), Fraction())
    claimed = solution.get("objective")
    mismatch = claimed is not None and _q(claimed) != objective
    return {
        "objective": str(objective),
        "verification_status": "certified" if strict else "exact",
        "details": {"n": n, "pair_checks": n*(n-1)//2,
                    "claimed_objective_mismatch": mismatch},
    }
