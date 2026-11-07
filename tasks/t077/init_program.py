"""Small valid seed A={0,1,3}."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T077-C01") != "T077-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    solution = {"set": [0, 1, 3]}
    # EVOLVE-BLOCK-END
    return solution


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
