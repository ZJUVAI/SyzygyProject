"""Exact checker for 3-AP-free subsets of the fixed universe [1, 212]."""

from collections.abc import Mapping, Set
from typing import Any


CONFIG_ID = "T042-C01"
N = 212


def _is_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate(solution: Any, config: Mapping[str, Any], strict: bool = False) -> dict[str, Any]:
    """Check every possible midpoint pair in the submitted finite set."""
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError("unsupported configuration id")
    expected_parameters = {
        "N": N,
        "universe": "integers_1_through_N",
        "forbidden_pattern": "nontrivial_three_term_arithmetic_progression",
    }
    if config.get("parameters") != expected_parameters:
        raise ValueError("configuration parameters do not match T042-C01")
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be a JSON object")

    elements = solution.get("elements")
    if not isinstance(elements, (list, tuple, set, frozenset)):
        raise ValueError("elements must be a list or set of integers")
    if any(not _is_integer(value) for value in elements):
        raise ValueError("each element must be an integer; bool and non-finite values are invalid")
    if isinstance(elements, (list, tuple)) and len(set(elements)) != len(elements):
        raise ValueError("elements must not contain duplicates")
    ordered = sorted(elements)
    if ordered and (ordered[0] < 1 or ordered[-1] > N):
        raise ValueError("each element must lie in [1, 212]")

    selected = set(ordered)
    pair_checks = 0
    for a_index, a in enumerate(ordered):
        for b in ordered[a_index + 1 :]:
            c = 2 * b - a
            pair_checks += 1
            if c in selected:
                raise ValueError(f"nontrivial 3-term arithmetic progression ({a}, {b}, {c})")

    return {
        "objective": len(ordered),
        "verification_status": "exact",
        "details": {
            "N": N,
            "selected_size": len(ordered),
            "midpoint_pairs_checked": pair_checks,
            "claimed_score_ignored": True,
            "strict_full_domain_check": True,
        },
    }
