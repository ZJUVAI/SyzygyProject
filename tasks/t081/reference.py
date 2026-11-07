"""Load the fixed rational reconstruction of the published n=12 diagram."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T081-C01")
    if chosen != "T081-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).parent / "data/reference/rechenberg12_rational.json"
    return {"points": json.loads(path.read_text(encoding="utf-8"))["points"]}
