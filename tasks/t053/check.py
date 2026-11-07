"""Exact checker for factorizations of 100000!."""

from functools import lru_cache
from math import factorial

N = 100000
PARAMETERS = {"n": N}


@lru_cache(maxsize=1)
def _target():
    return factorial(N)


def _product_tree(values):
    level = list(values)
    if not level:
        return 1
    while len(level) > 1:
        next_level = [level[i] * level[i + 1]
                      for i in range(0, len(level) - 1, 2)]
        if len(level) % 2:
            next_level.append(level[-1])
        level = next_level
    return level[0]


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("parameters") != PARAMETERS:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict) or "factors" not in solution:
        raise ValueError("solution must contain factors")
    factors = solution["factors"]
    if not isinstance(factors, list):
        raise ValueError("factors must be a list")
    if len(factors) != N:
        raise ValueError("factor list must contain exactly 100000 entries")
    target = _target()
    for value in factors:
        if type(value) is not int:
            raise ValueError("factors must be integers; bool and float are rejected")
        if value < 1:
            raise ValueError("factors must be positive")
        if value > target:
            raise ValueError("a factor cannot exceed the product 100000!")
    if _product_tree(factors) != target:
        raise ValueError("factor product is not exactly 100000!")
    return {
        "objective": min(factors),
        "verification_status": "exact",
        "details": {
            "n": N,
            "factor_count": len(factors),
            "product_equals_factorial": True,
            "product_check": "exact balanced product tree",
            "claimed_objective_ignored": True,
        },
    }
