"""Simple valid cold start: the empty 3-uniform hypergraph."""
import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T037-C01") != "T037-C01":
        raise ValueError("unsupported T037 configuration")
    # EVOLVE-BLOCK-START
    edges = []
    # EVOLVE-BLOCK-END
    return {"edges": edges}
