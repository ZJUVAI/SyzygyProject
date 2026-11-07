"""Simple valid starting form: four times the identity matrix."""

import os


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T078-C01")
    if chosen != "T078-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    # EVOLVE-BLOCK-START
    return {"gram": [[4 if i == j else 0 for j in range(10)] for i in range(10)]}
    # EVOLVE-BLOCK-END
