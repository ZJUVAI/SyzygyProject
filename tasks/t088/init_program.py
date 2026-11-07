"""Standalone simple initial ordering for arc130."""

import os

# EVOLVE-BLOCK-START
def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T088-C01")
    if chosen != "T088-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return {"ordering": list(range(1, 131))}
# EVOLVE-BLOCK-END
