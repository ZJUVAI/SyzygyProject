"""Load the public spherical-code witness for the selected configuration."""
import os
from pathlib import Path

def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T009-C02")
    names = {"T009-C02": "16", "T009-C03": "17", "T009-C04": "19"}
    if cid not in names: raise ValueError("unknown T009 configuration")
    points = []
    for line in (Path(__file__).parent / "data" / f"spherical_code_3_{names[cid]}.txt").read_text().splitlines():
        if line.strip(): points.append([x.strip() for x in line.split(",")])
    return {"points": points}
