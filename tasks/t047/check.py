"""Exact checker for unrestricted integer difference bases of [1, 6166]."""

from collections.abc import Mapping
from typing import Any


CONFIG_ID = "T047-C01"
N = 6166


def _is_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate(solution: Any, config: Mapping[str, Any], strict: bool = False) -> dict[str, Any]:
    """Check every required distance with exact integer arithmetic."""
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError("unsupported configuration id")
    if config.get("parameters") != {
        "N": N,
        "ambient_group": "integers_under_subtraction",
        "required_differences": "positive_integers_1_through_N",
    }:
        raise ValueError("configuration parameters do not match T047-C01")
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be a JSON object")
    raw_basis = solution.get("basis")
    if not isinstance(raw_basis, (list, tuple)):
        raise ValueError("basis must be a list of integers")
    if not raw_basis:
        raise ValueError("basis must contain at least one integer")

    basis = []
    seen = set()
    for point in raw_basis:
        if not _is_integer(point):
            raise ValueError("basis elements must be integers; bool is not accepted")
        if point in seen:
            raise ValueError("basis elements must be distinct")
        seen.add(point)
        basis.append(point)

    if len(basis) < 2:
        raise ValueError("a difference basis for positive distances needs at least two points")

    covered = bytearray(N + 1)
    remaining = N
    pair_checks = 0
    ordered = sorted(basis)
    for left_index, left in enumerate(ordered):
        right_index = left_index + 1
        while right_index < len(ordered):
            right = ordered[right_index]
            pair_checks += 1
            difference = right - left
            if difference > N:
                break
            if difference <= N and not covered[difference]:
                covered[difference] = 1
                remaining -= 1
                if remaining == 0:
                    break
            right_index += 1
        if remaining == 0:
            break
    if remaining:
        first_missing = next(distance for distance in range(1, N + 1) if not covered[distance])
        raise ValueError(f"basis does not cover every required distance; {first_missing} is missing")

    return {
        "objective": len(basis),
        "verification_status": "exact",
        "details": {
            "N": N,
            "basis_size": len(basis),
            "covered_distances": N,
            "pair_checks_until_full_coverage": pair_checks,
            "ambient_group": "integers_under_subtraction; differences larger than N are allowed",
            "claimed_objective_ignored": True,
            "strict_full_interval_check": True,
        },
    }
