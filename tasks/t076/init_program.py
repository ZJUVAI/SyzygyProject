"""Self-contained powers-of-two seed for the configured set size."""
import os
_CONFIGS={"T076-C01":15,"T076-C02":16,"T076-C03":17}
def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T076-C01")
    try:n=_CONFIGS[cid]
    except KeyError:raise ValueError(f"unsupported T076 configuration: {cid}") from None
    return {"elements":[1<<bit for bit in range(n)]}
