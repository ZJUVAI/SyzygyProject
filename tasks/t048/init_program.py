"""Self-contained odd-even transposition sorting network."""
import os
_CONFIGS={"T048-C01":17}
def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T048-C01")
    try:inputs=_CONFIGS[cid]
    except KeyError:raise ValueError(f"unsupported T048 configuration: {cid}") from None
    int(os.environ.get("MATHBENCH_SEED","0"))
    comparators=[]
    for phase in range(inputs):
        for left in range(phase%2,inputs-1,2):comparators.append([left,left+1])
    return {"comparators":comparators}
