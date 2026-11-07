"""Simple valid seed for T062."""

import os


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T062-C01")
    if chosen != "T062-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    # EVOLVE-BLOCK-START
    return {"elements": [1]}
    # EVOLVE-BLOCK-END
