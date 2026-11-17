"""Self-contained feasible construction: one customer per vehicle route."""

import os


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T097-C01")
    if chosen != "T097-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    # EVOLVE-BLOCK-START
    return {"routes": [[customer] for customer in range(2, 1002)]}
    # EVOLVE-BLOCK-END
