"""Load the public spherical-code witness for the selected configuration."""
import os
from pathlib import Path

def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T004-C01")
    names = {"T004-C01": "16", "T004-C02": "17", "T004-C03": "19"}
    if cid not in names: raise ValueError("unknown T004 configuration")
    points = []
    for line in (Path(__file__).parent / "data" / f"spherical_code_3_{names[cid]}.txt").read_text().splitlines():
        if line.strip(): points.append([x.strip() for x in line.split(",")])
    return {"points": points}
