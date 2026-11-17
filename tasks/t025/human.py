"""Reconstruct the classical convex-position construction for n=28."""


def run_code():
    # The parabola y=x^2 is strictly convex: every four selected points form
    # a convex quadrilateral and its two diagonals cross once.
    return {"points": [[i, i * i] for i in range(28)], "claimed_objective": 20475}
