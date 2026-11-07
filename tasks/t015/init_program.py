import os
import random


def run_code():
    # EVOLVE-BLOCK-START
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    coefficients = [rng.randint(1, 1000) for _ in range(20)]
    # EVOLVE-BLOCK-END
    return {"coefficients": coefficients}
