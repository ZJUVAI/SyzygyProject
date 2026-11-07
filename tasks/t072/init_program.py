"""Simple standalone starting set for T072-C01."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T072-C01") != "T072-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    solution = {"elements": list(range(1, 33))}
    # EVOLVE-BLOCK-END
    return solution


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
