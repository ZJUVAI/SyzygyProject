"""Exact checker for primitive simple perfect squared squares of order 38."""

from functools import lru_cache
from math import gcd


CONFIG_ID = "T098-C01"
PARAMETERS = {
    "order": 38,
    "object": "axis-aligned tiling of an integer-sided square by 38 smaller squares",
    "perfect": "all 38 positive integer square side lengths are distinct",
    "simple": "no proper rectangle is tiled by a subset of at least two component squares",
    "primitive": "greatest common divisor of the 38 square side lengths is 1",
    "objective": "minimum outer square side length over all valid tilings",
}
FROZEN_CONFIG = {
    "id": CONFIG_ID,
    "parameters": PARAMETERS,
    "direction": "minimize",
    "human_reference": 352,
}
ORDER = 38


def _same_typed(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_same_typed(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(_same_typed(a, b) for a, b in zip(left, right))
    return left == right


def _simple_rectangle_check(side, squares):
    xs = sorted({0, side, *(x for x, _, size in squares), *(x + size for x, _, size in squares)})
    ys = sorted({0, side, *(y for _, y, size in squares), *(y + size for _, y, size in squares)})
    index = {id(square): i for i, square in enumerate(squares)}

    x_ranges = []
    for ix, x0 in enumerate(xs[:-1]):
        for x1 in xs[ix + 1 :]:
            mask = 0
            for i, (x, y, size) in enumerate(squares):
                if x0 <= x and x + size <= x1:
                    mask |= 1 << i
            x_ranges.append((x0, x1, mask))

    y_ranges = []
    for iy, y0 in enumerate(ys[:-1]):
        for y1 in ys[iy + 1 :]:
            mask = 0
            for i, (x, y, size) in enumerate(squares):
                if y0 <= y and y + size <= y1:
                    mask |= 1 << i
            y_ranges.append((y0, y1, mask))

    areas = tuple(size * size for _, _, size in squares)

    @lru_cache(maxsize=65536)
    def contained_area(mask):
        total = 0
        while mask:
            bit = mask & -mask
            total += areas[bit.bit_length() - 1]
            mask -= bit
        return total

    for x0, x1, x_mask in x_ranges:
        for y0, y1, y_mask in y_ranges:
            if x0 == 0 and x1 == side and y0 == 0 and y1 == side:
                continue
            inside = x_mask & y_mask
            if inside.bit_count() < 2:
                continue
            if contained_area(inside) == (x1 - x0) * (y1 - y0):
                raise ValueError("tiling contains a proper squared rectangle")


def validate(solution, config, strict=False):
    del strict
    if not isinstance(config, dict) or not _same_typed(config, FROZEN_CONFIG):
        raise ValueError(f"configuration must match {CONFIG_ID} exactly")
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    side = solution.get("side")
    if type(side) is not int or side <= 0:
        raise ValueError("outer side must be a positive integer")
    raw_squares = solution.get("squares")
    if not isinstance(raw_squares, list) or len(raw_squares) != ORDER:
        raise ValueError("squares must contain exactly 38 entries")
    squares = []
    for item in raw_squares:
        if not isinstance(item, list) or len(item) != 3:
            raise ValueError("each square must be [x, y, side]")
        x, y, size = item
        if any(type(value) is not int for value in item):
            raise ValueError("square coordinates and sides must be integers; booleans are rejected")
        if size <= 0:
            raise ValueError("square side lengths must be positive")
        if x < 0 or y < 0 or x + size > side or y + size > side:
            raise ValueError("square lies outside the outer square")
        squares.append((x, y, size))

    sizes = [size for _, _, size in squares]
    if len(set(sizes)) != ORDER:
        raise ValueError("all square side lengths must be distinct")
    common = 0
    for size in sizes:
        common = gcd(common, size)
    if common != 1:
        raise ValueError("the squared square must be primitive (gcd of sides equals 1)")

    area = sum(size * size for size in sizes)
    if area != side * side:
        raise ValueError("component areas do not equal the outer square area")
    for i, (x, y, size) in enumerate(squares):
        for xx, yy, other_size in squares[i + 1 :]:
            if not (
                x >= xx + other_size
                or x + size <= xx
                or y >= yy + other_size
                or y + size <= yy
            ):
                raise ValueError("square interiors overlap")

    _simple_rectangle_check(side, squares)
    return {
        "objective": side,
        "verification_status": "exact",
        "details": {
            "order": ORDER,
            "outer_side": side,
            "distinct_sizes": len(set(sizes)),
            "primitive_gcd": common,
            "area_sum": area,
            "proper_subrectangles_checked": True,
            "claimed_objective_ignored": True,
        },
    }
