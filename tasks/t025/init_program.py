"""A simple cap in F_3^7: all binary vectors."""

from itertools import product


# EVOLVE-BLOCK-START
def run_code():
    return {"points": [list(point) for point in product((0, 1), repeat=7)]}
# EVOLVE-BLOCK-END
