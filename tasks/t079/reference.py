"""Rebuild the Station's published p=31 line witnesses from its formula."""

from tasks.t079.check import CANONICAL_DIRECTIONS, P


def run_code():
    inv = lambda x: pow(x % P, -1, P)
    lines = []
    for direction in CANONICAL_DIRECTIONS:
        a, b, c = direction
        if a:
            # Rescale (a,b,c) to the source chart (1,A,B). The line
            # (t, A*t+A^2, B*t+B^2) lies in the published quadratic set.
            A, B = b * inv(a) % P, c * inv(a) % P
            origin = (0, A * A % P, B * B % P)
        elif b:
            # Match the remaining directions to the published boundary lines
            # (0,t,C*t+C/(C-1)), the diagonal, and the vertical line.
            C = c * inv(b) % P
            if C == 1:
                origin = (0, 0, 0)
            else:
                origin = (0, 0, C * inv(C - 1) % P)
        else:
            origin = (0, 0, 0)
        lines.append({"direction": list(direction), "origin": list(origin)})
    return {"lines": lines}
