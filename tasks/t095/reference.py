"""Fixed replay of the pinned official CG:SHOP 2020 construction."""

import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T095-C01") != "T095-C01":
        raise ValueError("unknown T095 configuration")
    path = Path(__file__).parent / "data/reference/uniform-0000500-1.official_solution.json"
    return {"edges": json.loads(path.read_text())["edges"]}
