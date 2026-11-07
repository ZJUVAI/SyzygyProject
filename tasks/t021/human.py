"""Rebuild CCD coordinate witness using exact rational stereographic projection."""
import os
from fractions import Fraction
from pathlib import Path

_LENGTHS = {"T021-C01": 32, "T021-C02": 40, "T021-C03": 50}

def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T021-C01")
    if cid not in _LENGTHS: raise ValueError(f"unsupported configuration: {cid}")
    n=_LENGTHS[cid]
    lines=(Path(__file__).parent/"data"/f"ccd_{n}.xyz").read_text(encoding="ascii").splitlines()
    if int(lines[0].strip()) != n: raise ValueError("unexpected coordinate archive")
    points=[]
    for line in lines[1:]:
        fields=line.split()
        if not fields: continue
        if len(fields)!=4 or fields[0]!="LA": raise ValueError("unexpected CCD xyz row")
        x,y,z=(Fraction(value) for value in fields[1:])
        # Rotate (x,y,z) to (x,z,-y), moving source coordinates away from chart pole.
        x,y,z=x,z,-y
        denominator=1+z
        if denominator==0: raise ValueError("source point lies at chart pole")
        points.append([str(x/denominator),str(y/denominator)])
    if len(points)!=n: raise ValueError("coordinate count mismatch")
    return {"points":points}
