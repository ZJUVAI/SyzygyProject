"""Simple valid starting set: a 4 by 3 integer grid."""

import os


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T081-C01")
    if chosen != "T081-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    # EVOLVE-BLOCK-START
    return {"points": [[x, y] for y in range(3) for x in range(4)]}
    # EVOLVE-BLOCK-END
