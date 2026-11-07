"""Simple exact seed: 28 points on the integer parabola."""
import os

# EVOLVE-BLOCK-START
def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T036-C01") != "T036-C01":
        raise ValueError("unsupported configuration id")
    return {"points": [[i, i * i] for i in range(28)]}
# EVOLVE-BLOCK-END
