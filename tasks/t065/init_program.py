"""Standalone simple seed: 100 separated rational points with score zero."""
import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T065-C01") != "T065-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    points = [
        {"x": [str(2 * index)], "y": ["0"]}
        for index in range(100)
    ]
    # The minimal polynomial x selects the real algebraic number alpha=0.
    solution = {
        "minimal_polynomial": [0, 1],
        "isolating_interval": ["-1/2", "1/2"],
        "points": points,
    }
    # EVOLVE-BLOCK-END
    return solution


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
