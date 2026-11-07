import os
import random


def _config_n():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T018-C01")
    try:
        return {"T018-C01": 29, "T018-C02": 27}[cid]
    except KeyError:
        raise ValueError(f"unknown T018 configuration: {cid}") from None


def run_code():
    # EVOLVE-BLOCK-START
    n = _config_n()
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    # A deterministic nonsingular seed: 2I-J has eigenvalues 2 (mult. 28), -27.
    matrix = [[(1 if i == j else -1) for j in range(n)] for i in range(n)]
    # EVOLVE-BLOCK-END
    return {"matrix": matrix}
