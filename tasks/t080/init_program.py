import os
import random


def run_code():
    # EVOLVE-BLOCK-START
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    heights = [0.5] * 51
    # EVOLVE-BLOCK-END
    return {"heights": heights}
