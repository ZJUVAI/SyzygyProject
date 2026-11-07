"""Self-contained initial factorization 100000! = 1*2*...*100000."""

import os

N = 100000


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T053-C01") != "T053-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    factors = list(range(1, N + 1))
    # EVOLVE-BLOCK-END
    return {"factors": factors}


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
