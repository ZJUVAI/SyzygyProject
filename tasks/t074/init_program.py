"""Standalone valid seed from 12 points on the parabola y=x^2."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T074-C01") != "T074-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    solution = {"points": [[i, i * i] for i in range(12)]}
    # EVOLVE-BLOCK-END
    return solution


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
