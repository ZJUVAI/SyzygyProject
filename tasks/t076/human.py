"""Reconstruct Conway-Guy traditional sum-distinct sets."""
import os
from math import isqrt
def _conway_guy_sequence(last_index):
    seq=[0,1]
    for n in range(1,last_index):
        root=isqrt(2*n);nearest=root+int(8*n >= (2*root+1)**2)
        seq.append(2*seq[n]-seq[n-nearest])
    return seq
def build_conway_guy_set(n):
    seq=_conway_guy_sequence(n);maximum=seq[n]
    return {"elements":sorted(maximum-seq[n-i] for i in range(1,n+1))}
def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T076-C01")
    if cid != "T076-C01":raise ValueError(f"unsupported T076 configuration: {cid}")
    return build_conway_guy_set(15)
