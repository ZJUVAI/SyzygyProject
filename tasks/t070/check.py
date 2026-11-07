"""Exact checker for a coprime square dissection of the 1000 square."""

from collections.abc import Mapping
from math import gcd


CONFIG_ID = "T070-C01"
OUTER_SIDE = 1000
FULL_COLUMN = (1 << OUTER_SIDE) - 1
PARAMETERS = {
    "outer_side": 1000,
    "tile_side_domain": "positive integers less than 1000",
    "side_length_gcd": 1,
    "compound_dissection_allowed": True,
    "objective": "square_count",
}


def _check_config(config):
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix the coprime 1000-square dissection")


def _parse_squares(solution):
    raw_squares = solution.get("squares")
    if not isinstance(raw_squares, (list, tuple)):
        raise ValueError("squares must be a list of [x,y,side] integer triples")
    squares = []
    seen = set()
    area = 0
    side_gcd = 0
    for index, square in enumerate(raw_squares):
        if not isinstance(square, (list, tuple)) or len(square) != 3:
            raise ValueError(f"square {index} must be an [x,y,side] triple")
        x, y, side = square
        if type(x) is not int or type(y) is not int or type(side) is not int:
            raise ValueError(f"square {index} coordinates and side must be integers")
        if side <= 0 or side >= OUTER_SIDE:
            raise ValueError(f"square {index} side must be from 1 through 999")
        if x < 0 or y < 0 or x + side > OUTER_SIDE or y + side > OUTER_SIDE:
            raise ValueError(f"square {index} lies outside the 1000 by 1000 outer square")
        item = (x, y, side)
        if item in seen:
            raise ValueError("duplicate square records are not allowed")
        seen.add(item)
        squares.append(item)
        area += side * side
        side_gcd = gcd(side_gcd, side)

    if not squares:
        raise ValueError("a dissection must contain at least one tile")
    if area != OUTER_SIDE * OUTER_SIDE:
        raise ValueError("tile areas must sum exactly to the outer-square area")
    if side_gcd != 1:
        raise ValueError("tile side lengths must have greatest common divisor 1")
    return squares, area, side_gcd


def validate(solution, config, strict=False):
    """Verify a full, non-overlapping, relatively-prime square dissection."""
    _check_config(config)
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")
    squares, area, side_gcd = _parse_squares(solution)

    # Each integer x-column stores the set of covered integer y-cells as bits.
    # Since the exact total area is 1,000,000, this loop performs at most
    # 1,000,000 column updates for any candidate with valid tile areas.
    columns = [0] * OUTER_SIDE
    for index, (x, y, side) in enumerate(squares):
        mask = ((1 << side) - 1) << y
        for column in range(x, x + side):
            if columns[column] & mask:
                raise ValueError(f"square {index} overlaps a previous tile")
            columns[column] |= mask
    if any(mask != FULL_COLUMN for mask in columns):
        raise ValueError("squares do not cover the entire outer square")

    return {
        "objective": len(squares),
        "verification_status": "exact",
        "details": {
            "square_count": len(squares),
            "outer_side": OUTER_SIDE,
            "total_tile_area": area,
            "covered_area": OUTER_SIDE * OUTER_SIDE,
            "tile_side_gcd": side_gcd,
            "integer_columns_checked": OUTER_SIDE,
            "claimed_objective_ignored": True,
            "strict": bool(strict),
        },
    }
