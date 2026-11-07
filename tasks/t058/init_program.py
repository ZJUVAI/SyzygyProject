"""Simple feasible one-round partition."""

import os


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T058-C01")
    if chosen != "T058-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    # EVOLVE-BLOCK-START
    return {"rounds": [[[5 * group + offset for offset in range(5)] for group in range(7)] ]}
    # EVOLVE-BLOCK-END
