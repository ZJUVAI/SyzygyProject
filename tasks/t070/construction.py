"""Guillotine and skyline constructions for integer square dissections."""

from math import gcd


OUTER_SIDE = 1000


def parse_published_sizes(path):
    values = [int(value) for value in path.read_text(encoding="ascii").split()]
    if len(values) < 3:
        raise ValueError("published row is incomplete")
    count, width, height, *sides = values
    if count != 27 or width != OUTER_SIDE or height != OUTER_SIDE or len(sides) != count:
        raise ValueError("published row does not match the 27-square 1000 by 1000 entry")
    if any(side <= 0 or side >= OUTER_SIDE for side in sides):
        raise ValueError("published row contains an invalid tile side")
    return sides


def skyline_decode(sides, outer_side=OUTER_SIDE):
    """Place each square at lowest y, then lowest x, above the skyline."""
    heights = [0] * outer_side
    result = []
    for index, side in enumerate(sides):
        if type(side) is not int or side <= 0 or side >= outer_side:
            raise ValueError(f"side {index} is outside the supported range")
        best = None
        for x in range(outer_side - side + 1):
            y = max(heights[x:x + side])
            if y + side <= outer_side:
                key = (y, x)
                if best is None or key < best:
                    best = key
        if best is None:
            raise ValueError(f"side {index} does not fit the remaining skyline")
        y, x = best
        result.append([x, y, side])
        heights[x:x + side] = [y + side] * side
    return {"squares": result}


def corner_seed():
    """One 999 square plus the two unit-width strips around it."""
    squares = [[0, 0, 999]]
    squares.extend([[x, 999, 1] for x in range(999)])
    squares.extend([[999, y, 1] for y in range(1000)])
    return {"squares": squares}


def _euclidean_rectangle(x, y, width, height):
    """Tile one integer rectangle by the greedy Euclidean guillotine rule."""
    result = []
    while width and height:
        if width >= height:
            side = height
            count = width // side
            result.extend([[x + i * side, y, side] for i in range(count)])
            x += count * side
            width -= count * side
        else:
            side = width
            count = height // side
            result.extend([[x, y + i * side, side] for i in range(count)])
            y += count * side
            height -= count * side
    return result


def _split_rectangles(plan, outer_side=OUTER_SIDE):
    leaves = [(0, 0, outer_side, outer_side)]
    for leaf_code, axis_code, cut_code in plan:
        choices = [i for i, (_, _, width, height) in enumerate(leaves)
                   if width > 1 or height > 1]
        if not choices:
            break
        leaf_index = choices[leaf_code % len(choices)]
        x, y, width, height = leaves.pop(leaf_index)
        axes = [0] if width > 1 else []
        if height > 1:
            axes.append(1)
        axis = axes[axis_code % len(axes)]
        extent = width if axis == 0 else height
        cut = 1 + (cut_code % (extent - 1))
        if axis == 0:
            leaves.extend([(x, y, cut, height), (x + cut, y, width - cut, height)])
        else:
            leaves.extend([(x, y, width, cut), (x, y + cut, width, height - cut)])
    squares = []
    for x, y, width, height in leaves:
        squares.extend(_euclidean_rectangle(x, y, width, height))
    return squares


def coprime_guillotine_plan(plan, outer_side=OUTER_SIDE):
    """Build a guillotine tiling and refine one tile if its side gcd is >1."""
    squares = _split_rectangles(plan, outer_side)
    side_gcd = 0
    for _, _, side in squares:
        side_gcd = gcd(side_gcd, side)
    if side_gcd != 1:
        index = max(range(len(squares)), key=lambda i: squares[i][2])
        x, y, side = squares.pop(index)
        if side < 2:
            raise ValueError("a non-coprime dissection cannot be refined from unit tiles")
        squares.append([x, y, side - 1])
        squares.extend([[x + i, y + side - 1, 1] for i in range(side)])
        squares.extend([[x + side - 1, y + j, 1] for j in range(side - 1)])
    return {"squares": squares}


def count_squares(solution):
    return len(solution["squares"])
