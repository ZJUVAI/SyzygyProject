"""Replay the fixed 191-edge public Q9 record from Orland et al."""

import json
from pathlib import Path


def run_code():
    path = Path(__file__).parent / "data" / "reference" / "orland_v3_q9_191.json"
    witness = json.loads(path.read_text())
    return {"vertices": witness["vertices"]}


if __name__ == "__main__":
    print(run_code())
