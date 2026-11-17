"""Pinned historical human witness, stored within this task."""
import json
from pathlib import Path

def run_code():
    data = json.loads((Path(__file__).parent / "data" / "human_labs100_record.json").read_text())
    return {"sequence": data["sequence"]}
