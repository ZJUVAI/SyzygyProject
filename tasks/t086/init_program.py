"""Simple feasible seed: four 3x3 identity matrices."""

import os


def _identity():
    return [
        [[1, 0], [0, 0], [0, 0]],
        [[0, 0], [1, 0], [0, 0]],
        [[0, 0], [0, 0], [1, 0]],
    ]


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T086-C01") != "T086-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    solution = {"matrices": [_identity(), _identity(), _identity(), _identity()]}
    # EVOLVE-BLOCK-END
    return solution


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
