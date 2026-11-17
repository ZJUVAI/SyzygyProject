"""Self-contained powers-of-two seed for the configured set size."""
import os
def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T062-C01")
    if cid != "T062-C01":raise ValueError(f"unsupported T062 configuration: {cid}")
    return {"elements":[1<<bit for bit in range(15)]}
