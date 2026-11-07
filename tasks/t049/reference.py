"""Frozen same-parameter lattice reference, kept under data/reference/."""

import json
from pathlib import Path


def run_code():
    path = Path(__file__).with_name("data") / "reference" / "hexagon_n91.json"
    return json.loads(path.read_text(encoding="utf-8"))
