"""Exact verifier for rational directions in the five-dimensional kissing problem."""

from fractions import Fraction

_CONFIG_ID = "T037-C01"
_PARAMETERS = {
    "dimension": 5,
    "minimum_angle_degrees": 60,
    "representation": "nonzero rational direction vectors in Q^5; exact angle check after normalization",
    "objective": "maximum cardinality",
}


def _rational(value):
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("coordinates must be finite rational strings") from exc
    raise ValueError("coordinates must be integers or rational strings; bool/float rejected")


def validate(solution, config, strict=False):
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    if config.get("id") != _CONFIG_ID or config.get("parameters") != _PARAMETERS:
        raise ValueError("configuration does not match T037-C01")
    vectors = solution.get("directions")
    if not isinstance(vectors, list):
        raise ValueError("directions must be a list")
    parsed = []
    for vector in vectors:
        if not isinstance(vector, list) or len(vector) != 5:
            raise ValueError("each direction must have five rational coordinates")
        q = tuple(_rational(x) for x in vector)
        norm2 = sum(x * x for x in q)
        if norm2 == 0:
            raise ValueError("zero direction is not allowed")
        parsed.append((q, norm2))
    for i, (u, un) in enumerate(parsed):
        for j, (v, vn) in enumerate(parsed[:i]):
            dot = sum(a * b for a, b in zip(u, v))
            # cos(theta) <= 1/2. For dot <= 0 this is immediate;
            # otherwise square only nonnegative exact rational quantities.
            if dot > 0 and 4 * dot * dot > un * vn:
                raise ValueError(f"directions {j} and {i} are less than 60 degrees apart")
    return {
        "objective": len(parsed),
        "verification_status": "exact",
        "details": {"dimension": 5, "minimum_angle_degrees": 60,
                    "pair_checks": len(parsed) * (len(parsed) - 1) // 2,
                    "representation": "exact rational directions"},
    }
