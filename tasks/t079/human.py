"""Quadratic-residue Kakeya construction, rebuilt from its defining formula."""

from tasks.t079.check import CANONICAL_DIRECTIONS, P


def run_code():
    inv4 = pow(4, -1, P)
    lines = []
    for direction in CANONICAL_DIRECTIONS:
        a, b, c = direction
        if c == 1:
            # For direction (a,b,1), x+t^2 and y+t^2 are squares on this line.
            origin = (a * a * inv4 % P, b * b * inv4 % P, 0)
        else:
            # These directions are covered by the complete z=0 plane.
            origin = (0, 0, 0)
        lines.append({"direction": list(direction), "origin": list(origin)})
    return {"lines": lines}
