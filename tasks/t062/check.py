"""Exact checker for square-difference-free subsets of [42025]."""

from math import isqrt

CONFIG_ID = "T062-C01"
N = 42025
PARAMETERS = {
    "N": N,
    "set": "subset of {1,...,N}",
    "forbidden_difference": "positive perfect square",
    "objective": "cardinality",
}


def _check_config(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    if config.get("id") not in (None, CONFIG_ID):
        raise ValueError(f"unsupported configuration: expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must describe square-difference-free subsets of [42025]")


def validate(solution, config, strict=False):
    """Recompute cardinality and reject every positive-square difference."""
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    elements = solution.get("elements")
    if not isinstance(elements, list):
        raise ValueError("elements must be a list")
    seen = set()
    for index, value in enumerate(elements):
        if type(value) is not int:
            raise ValueError(f"element {index} must be an integer")
        if not 1 <= value <= N:
            raise ValueError(f"element {value} is outside 1..{N}")
        if value in seen:
            raise ValueError(f"duplicate element {value}")
        seen.add(value)

    checked_offsets = 0
    for value in seen:
        for root in range(1, isqrt(N - value) + 1):
            checked_offsets += 1
            if value + root * root in seen:
                raise ValueError(
                    f"forbidden square difference {root * root} between {value} and {value + root * root}"
                )

    return {
        "objective": len(seen),
        "verification_status": "exact",
        "details": {
            "N": N,
            "cardinality": len(seen),
            "positive_square_translations_checked": checked_offsets,
            "claimed_objective_ignored": True,
        },
    }
