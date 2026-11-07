"""Return the frozen, exactly rechecked 6-fan reference witness."""

import json
from pathlib import Path


def run_code():
    path = Path(__file__).resolve().parent / "data/reference/6fan_120.json"
    return json.loads(path.read_text(encoding="utf-8"))
