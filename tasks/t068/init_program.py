"""Simple standalone seed: use every word as a codeword."""

import os


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T068-C01")
    if chosen != "T068-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    # EVOLVE-BLOCK-START
    return {"codewords": list(range(1 << 10))}
    # EVOLVE-BLOCK-END
