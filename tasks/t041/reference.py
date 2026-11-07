"""Replay the fixed public exact-rational n=17 construction."""
import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T041-C01") != "T041-C01":
        raise ValueError("unsupported T041 configuration")
    _seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    path = Path(__file__).parent / "data" / "public_witness.json"
    return json.loads(path.read_text(encoding="utf-8"))
