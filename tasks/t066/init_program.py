"""Simple standalone seed: 17 points on a rational parabola."""

import os


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T066-C01")
    if chosen != "T066-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    # EVOLVE-BLOCK-START
    points = [{"x": [i], "y": [i * i]} for i in range(17)]
    return {
        "minimal_polynomial": [0, 1],
        "isolating_interval": ["-1", "1"],
        "points": points,
    }
    # EVOLVE-BLOCK-END
