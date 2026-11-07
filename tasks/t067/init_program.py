"""Standalone one-word valid seed for A(17,4,5)."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T067-C01") != "T067-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    solution = {"codewords": ["00000000000011111"]}
    # EVOLVE-BLOCK-END
    return solution


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
