"""Standalone simple Hamiltonian cycle seed for T069."""

import os


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T069-C01")
    if chosen != "T069-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    # EVOLVE-BLOCK-START
    return {"tour": list(range(100_000))}
    # EVOLVE-BLOCK-END
