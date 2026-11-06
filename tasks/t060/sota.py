"""Replayed 23-block C(24,14,4) witness from the La Jolla repository."""

import json
from pathlib import Path


def run_code():
    path = Path(__file__).parent / "data" / "sota_witness.json"
    return json.loads(path.read_text(encoding="utf-8"))
