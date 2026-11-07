"""Exact checker for two-color 7-AP-free colorings of [1,n]."""

from collections.abc import Mapping
from typing import Any


CONFIG_ID = "T034-C01"
COLOR_COUNT = 2
PROGRESSION_LENGTH = 7


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate(solution: Any, config: Mapping[str, Any], strict: bool = False) -> dict[str, Any]:
    """Recompute the prefix length and inspect every positive-step 7-AP."""
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be a JSON object")
    if config.get("id") != CONFIG_ID:
        raise ValueError("unsupported configuration id")
    parameters = config.get("parameters")
    expected = {
        "colors": COLOR_COUNT,
        "progression_length": PROGRESSION_LENGTH,
        "domain": "consecutive_prefix_of_positive_integers",
        "common_difference": "positive_integer",
    }
    if parameters != expected:
        raise ValueError("configuration parameters do not match T034-C01")
    n = solution.get("n")
    colors = solution.get("colors")
    if not _is_int(n) or n < 1:
        raise ValueError("n must be a positive integer, not bool")
    if not isinstance(colors, list) or len(colors) != n:
        raise ValueError("colors must be a list of length n for [1,n]")
    if any(not _is_int(color) or color not in (0, 1) for color in colors):
        raise ValueError("each color must be integer 0 or 1; bool is not accepted")

    # Index i represents positive integer i+1. The AP condition is translation invariant.
    progressions_checked = 0
    max_step = (n - 1) // (PROGRESSION_LENGTH - 1)
    for step in range(1, max_step + 1):
        last_start = n - (PROGRESSION_LENGTH - 1) * step
        for start in range(last_start):
            progressions_checked += 1
            color = colors[start]
            if all(colors[start + j * step] == color for j in range(1, PROGRESSION_LENGTH)):
                terms = [start + j * step + 1 for j in range(PROGRESSION_LENGTH)]
                raise ValueError(f"monochromatic 7-term arithmetic progression {terms}")

    return {
        "objective": n,
        "verification_status": "exact",
        "details": {
            "n": n,
            "colors": COLOR_COUNT,
            "progression_length": PROGRESSION_LENGTH,
            "positive_steps_checked": max_step,
            "progressions_checked": progressions_checked,
            "claimed_objective_ignored": True,
        },
    }
