"""Self-contained feasible seed: two grid points."""
import os

# EVOLVE-BLOCK-START
def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T024-C01") != "T024-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return {"points": [[0, 0], [1, 0]]}
# EVOLVE-BLOCK-END
