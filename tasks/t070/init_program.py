"""Standalone valid 2000-tile initial dissection."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T070-C01") != "T070-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    squares = [[0, 0, 999]]
    squares.extend([[x, 999, 1] for x in range(999)])
    squares.extend([[999, y, 1] for y in range(1000)])
    solution = {"squares": squares}
    # EVOLVE-BLOCK-END
    return solution


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
