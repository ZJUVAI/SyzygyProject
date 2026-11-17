"""Embed the classical ternary 3-AP-free construction on one grid row."""
import os

def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T101-C01") != "T101-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    xs = [1 + sum(bit * (3**i) for i, bit in enumerate(bits))
          for mask in range(16)
          for bits in [[(mask >> i) & 1 for i in range(4)]]]
    return {"points": [[x, 0] for x in xs]}
