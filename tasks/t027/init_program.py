"""Simple identity seed for T027-C01; no reference witness is read."""
import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T027-C01") != "T027-C01":
        raise ValueError("unsupported T027 configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    permutation = list(range(256))
    # EVOLVE-BLOCK-END
    return {"permutation": permutation}
