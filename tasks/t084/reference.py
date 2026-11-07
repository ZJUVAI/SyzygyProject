"""Return the strongest reproduced same-parameter published witness."""

import json
from pathlib import Path


def run_code():
    witness_path = Path(__file__).parent / "data" / "reference" / "public_m31_19407.json"
    return {"elements": json.loads(witness_path.read_text(encoding="utf-8"))["elements"]}
