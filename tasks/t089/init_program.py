import os
import random


def run_code():
    # EVOLVE-BLOCK-START
    n = 29
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    # A deterministic nonsingular seed: 2I-J has eigenvalues 2 (mult. 28), -27.
    matrix = [[(1 if i == j else -1) for j in range(n)] for i in range(n)]
    # EVOLVE-BLOCK-END
    return {"matrix": matrix}
