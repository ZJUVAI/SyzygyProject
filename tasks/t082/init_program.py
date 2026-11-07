"""Small valid peaceable-queens seed."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T082-C01") != "T082-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    solution = {"white": [[0, 0]], "black": [[1, 2]]}
    # EVOLVE-BLOCK-END
    return solution


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
