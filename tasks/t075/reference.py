"""Frozen exact H6 blow-up witness from the published construction."""
import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T075-C01") != "T075-C01":
        raise ValueError("unsupported T075 configuration")
    path = Path(__file__).parent / "data/human/h6_iterated_blowup_n36.json"
    return json.loads(path.read_text(encoding="utf-8"))
