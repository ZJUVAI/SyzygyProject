"""Exact checker for finite integer B_3 sets."""

from itertools import combinations_with_replacement
import sys

# Python 3.11+ limits decimal conversions by default. The public domain has no
# integer-size cap, so the checker accepts decimal-string integer encodings too.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def _integer(value):
    if type(value) is int:
        return value
    if isinstance(value, str):
        digits = value[1:] if value.startswith("-") else value
        if not digits or not digits.isascii() or not digits.isdigit():
            raise ValueError("decimal-string elements must use base-10 integer notation")
        if value.startswith("-") and (len(value) == 1 or value[1] == "0"):
            raise ValueError("decimal-string elements must use canonical integer notation")
        if not value.startswith("-") and len(value) > 1 and value[0] == "0":
            raise ValueError("decimal-string elements must use canonical integer notation")
        return int(value)
    raise ValueError("elements must be exact integers or canonical decimal strings")


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("id") != "T084-C01":
        raise ValueError("unknown T084 configuration")
    parameters = config.get("parameters")
    if (not isinstance(parameters, dict)
            or set(parameters) != {"cardinality", "order", "integer_domain"}
            or type(parameters.get("cardinality")) is not int
            or parameters.get("cardinality") != 31
            or type(parameters.get("order")) is not int
            or parameters.get("order") != 3
            or type(parameters.get("integer_domain")) is not bool
            or parameters.get("integer_domain") is not True):
        raise ValueError("T084-C01 parameters must match the frozen configuration exactly")
    cardinality = 31
    order = 3
    elements = solution.get("elements") if isinstance(solution, dict) else solution
    if not isinstance(elements, (list, tuple)) or len(elements) != cardinality:
        raise ValueError("solution must contain exactly 31 integers")
    elements = [_integer(value) for value in elements]
    if len(set(elements)) != cardinality:
        raise ValueError("elements must be distinct")

    triples = combinations_with_replacement(elements, order)
    seen = set()
    checked = 0
    for triple in triples:
        total = sum(triple)
        if total in seen:
            raise ValueError("all unordered three-term sums, with repetition, must be distinct")
        seen.add(total)
        checked += 1
    if checked != 5456:
        raise ValueError("internal error: unexpected triple-sum count")
    diameter = max(elements) - min(elements)
    diameter_wire = diameter if len(str(diameter)) <= 4300 else str(diameter)
    return {
        "objective": diameter_wire,
        "verification_status": "exact",
        "details": {
            "cardinality": cardinality,
            "order": order,
            "triple_sums_checked": checked,
            "claimed_objective_ignored": True,
        },
    }
