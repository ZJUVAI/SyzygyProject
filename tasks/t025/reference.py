"""Fixed public reference witness, stored as task-local data."""

import json
from pathlib import Path


def run_code():
    return json.loads((Path(__file__).parent / "data" / "human_witness.json").read_text())
