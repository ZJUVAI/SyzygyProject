"""Simple standalone valid seed consisting of a single codeword."""

import os


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T071-C01")
    if chosen != "T071-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    # EVOLVE-BLOCK-START
    return {"codewords": [0]}
    # EVOLVE-BLOCK-END
