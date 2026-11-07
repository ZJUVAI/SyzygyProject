"""Read the fixed public 43-element witness; not used by search programs."""

import json
from pathlib import Path


def run_code():
    path = Path(__file__).parent / "data" / "reference" / "ergezer_n212_k43_witness.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    return {"elements": record["A"]}
