"""Exact checker for ordinary Schur colorings of a consecutive prefix."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _parse_coloring(solution: Mapping[str, Any], color_limit: int) -> tuple[int, list[int]]:
    if "n" not in solution or not _is_int(solution["n"]):
        raise ValueError("n must be an integer, not bool")
    n = solution["n"]
    if n < 1:
        raise ValueError("n must be positive")

    has_colors = "colors" in solution
    has_classes = "classes" in solution
    if has_colors == has_classes:
        raise ValueError("provide exactly one of colors or classes")

    if has_colors:
        colors = solution["colors"]
        if not isinstance(colors, list) or len(colors) != n:
            raise ValueError("colors must be a list with exactly n entries for [1,n]")
        if any(not _is_int(color) for color in colors):
            raise ValueError("color labels must be integers, not bool or non-integers")
        if any(color < 0 or color >= color_limit for color in colors):
            raise ValueError(f"color labels must lie in [0,{color_limit - 1}]")
        return n, colors

    classes = solution["classes"]
    if not isinstance(classes, list) or not (1 <= len(classes) <= color_limit):
        raise ValueError(f"classes must contain between 1 and {color_limit} color classes")
    colors = [-1] * n
    for color, members in enumerate(classes):
        if not isinstance(members, list):
            raise ValueError("each color class must be a list")
        for number in members:
            if not _is_int(number):
                raise ValueError("class members must be integers, not bool or non-integers")
            if not 1 <= number <= n:
                raise ValueError("class member is outside [1,n]")
            position = number - 1
            if colors[position] != -1:
                raise ValueError("duplicate class member or overlapping color classes")
            colors[position] = color
    if any(color == -1 for color in colors):
        raise ValueError("classes must cover every integer in the continuous prefix [1,n]")
    return n, colors


def validate(solution: Any, config: Mapping[str, Any], strict: bool = False) -> dict[str, Any]:
    """Recompute the largest feasible prefix length from the coloring itself."""
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be a JSON object")
    parameters = config.get("parameters", config)
    color_limit = parameters.get("colors")
    if not _is_int(color_limit) or color_limit < 1:
        raise ValueError("configuration colors must be a positive integer")
    n, colors = _parse_coloring(solution, color_limit)

    masks = [0] * color_limit
    for number, color in enumerate(colors, start=1):
        masks[color] |= 1 << number

    for color, mask in enumerate(masks):
        remaining = mask
        while remaining:
            least = remaining & -remaining
            x = least.bit_length() - 1
            if (mask << x) & mask:
                # The loop below is used only to report a concrete exact violation.
                members = [y for y in range(1, n + 1) if (mask >> y) & 1]
                for index, left in enumerate(members):
                    for right in members[index:]:
                        if left + right <= n and colors[left - 1] == colors[right - 1] == color and colors[left + right - 1] == color:
                            raise ValueError(f"monochromatic Schur triple ({left}, {right}, {left + right})")
                raise ValueError("monochromatic Schur triple")
            remaining ^= least

    return {
        "objective": n,
        "verification_status": "exact",
        "details": {
            "n": n,
            "color_limit": color_limit,
            "colors_used": len(set(colors)),
            "continuous_prefix": True,
            "all_pairs_checked_including_equal_terms": True,
            "claimed_objective_ignored": True,
        },
    }
