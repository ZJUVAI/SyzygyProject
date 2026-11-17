"""Load the public spherical-code witness for the selected configuration."""
import os
from pathlib import Path

def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T011-C01")
    points = []
    if cid != "T011-C01": raise ValueError("unknown T011 configuration")
    for line in (Path(__file__).parent / "data" / "spherical_code_3_16.txt").read_text().splitlines():
        if line.strip(): points.append([x.strip() for x in line.split(",")])
    return {"points": points}
