"""Simple cyclic starter for the order-12 MOLS task."""
import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T038-C01") != "T038-C01":
        raise ValueError("unsupported configuration")
    # EVOLVE-BLOCK-START
    square = [[(row + column) % 12 for column in range(12)] for row in range(12)]
    # EVOLVE-BLOCK-END
    return {"squares": [square], "objective": 1}
