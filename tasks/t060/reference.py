"""Reproduce the fixed public 127-one comparison expression."""
import json
from pathlib import Path


def run_code():
    path = Path(__file__).with_name("data") / "reference" / "public_127_expression.json"
    return json.loads(path.read_text(encoding="utf-8"))
