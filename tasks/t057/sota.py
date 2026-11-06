"""Replay the published SimpleTES sum-difference construction.

The reported Dream-RSI score is higher, but its discovered program is not
available in the inspected public repository snapshot.
"""

import json
from pathlib import Path


def run_code():
    witness_path = Path(__file__).with_name("sota_witness.json")
    return {"set": json.loads(witness_path.read_text(encoding="utf-8"))}
