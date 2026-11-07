"""Standalone simple periodic binary sequence seed."""

import os

# EVOLVE-BLOCK-START
def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T090-C01")
    if chosen != "T090-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return {"sequence": [1] * 64}
# EVOLVE-BLOCK-END
