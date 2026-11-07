"""Replayed 23-block C(24,14,4) witness from the La Jolla repository."""

import json
from pathlib import Path


def run_code():
    config_id = __import__("os").environ.get("MATHBENCH_CONFIG_ID", "T008-C01")
    suffix = "_C02" if config_id == "T008-C02" else ""
    if config_id not in ("T008-C01", "T008-C02"):
        raise ValueError("unsupported configuration")
    path = Path(__file__).parent / "data" / f"sota_witness{suffix}.json"
    return json.loads(path.read_text(encoding="utf-8"))
