"""Replay the pinned public exact-rational 480-step AI certificate."""

import json
import os
from pathlib import Path


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T087-C01")
    if config_id != "T087-C01":
        raise ValueError(f"unknown T087 configuration: {config_id}")
    path = Path(__file__).parent / "data" / "source" / "certificate_n480.json"
    certificate = json.loads(path.read_text(encoding="utf-8"))
    return {"heights": certificate["heights_over_denom"]}
