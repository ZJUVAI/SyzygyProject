"""Standalone legal cold start: select no items."""

import os

# EVOLVE-BLOCK-START
def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T093-C01")
    if chosen != "T093-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return {"item_indices": [], "x_translations": [], "y_translations": []}
# EVOLVE-BLOCK-END
