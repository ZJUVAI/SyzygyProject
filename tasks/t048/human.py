"""Reconstruct Batcher odd-even mergesort with padded sentinel wires removed."""
import os
_CONFIGS={"T048-C01":17,"T048-C02":18,"T048-C03":19}
def build_batcher_network(inputs=None):
    if inputs is None:
        cid=os.environ.get("MATHBENCH_CONFIG_ID","T048-C01")
        try:inputs=_CONFIGS[cid]
        except KeyError:raise ValueError(f"unsupported T048 configuration: {cid}") from None
    padded=1
    while padded<inputs:padded*=2
    comps=[]
    def merge(start,length,stride):
        step=2*stride
        if step<length:
            merge(start,length,step);merge(start+stride,length,step)
            for left in range(start+stride,start+length-stride,step):
                right=left+stride
                if right<inputs:comps.append((left,right))
        else:
            right=start+stride
            if right<inputs:comps.append((start,right))
    def sort(start,length):
        if length>1:
            half=length//2;sort(start,half);sort(start+half,half);merge(start,length,1)
    sort(0,padded)
    return comps
def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T048-C01")
    if cid not in _CONFIGS:raise ValueError(f"unsupported T048 configuration: {cid}")
    return {"comparators":[list(x) for x in build_batcher_network(_CONFIGS[cid])],"method":"Batcher odd-even mergesort padded to the next power of two; sentinel-wire comparisons omitted","method_metadata":{"inputs":_CONFIGS[cid]}}
