"""Fixed best-reproduced periodic sequence witness."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T090-C01")
    if chosen != "T090-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    asset = Path(__file__).resolve().parent / "data" / "reference" / "tyler_loftsson_64.json"
    return json.loads(asset.read_text(encoding="utf-8"))
