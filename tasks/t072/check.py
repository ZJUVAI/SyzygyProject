"""Exact checker for the 32-element positive-integer sum-product problem."""

from collections.abc import Mapping


CONFIG_ID = "T072-C01"
CARDINALITY = 32
PARAMETERS = {
    "cardinality": 32,
    "element_domain": "all positive integers, unbounded",
    "sumset": "{a+b : a,b in A}",
    "product_set": "{a*b : a,b in A}",
    "objective": "max(|A+A|, |AA|)",
}


def _check_config(config):
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix the unbounded positive-integer problem with 32 elements")


def validate(solution, config, strict=False):
    """Recompute |A+A| and |AA| exactly; ignore candidate score fields."""
    _check_config(config)
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")
    raw = solution.get("elements")
    if not isinstance(raw, (list, tuple)):
        raise ValueError("elements must be a list of positive integers")
    if len(raw) != CARDINALITY:
        raise ValueError("elements must contain exactly 32 integers")
    values = []
    for index, value in enumerate(raw):
        if type(value) is not int:
            raise ValueError(f"element {index} must be an integer")
        if value <= 0:
            raise ValueError(f"element {index} must be positive")
        values.append(value)
    if len(set(values)) != CARDINALITY:
        raise ValueError("elements must be distinct")

    sums = {a + b for a in values for b in values}
    products = {a * b for a in values for b in values}
    sum_size = len(sums)
    product_size = len(products)
    objective = max(sum_size, product_size)
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "cardinality": CARDINALITY,
            "sumset_size": sum_size,
            "product_set_size": product_size,
            "claimed_objective_ignored": True,
            "strict": bool(strict),
        },
    }
