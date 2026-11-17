"""Replay Wynn's published traditional 190-edge Q9 snake."""

import json
from pathlib import Path


def run_code():
    path = Path(__file__).parent / "data" / "reference" / "wynn_q9_190.json"
    witness = json.loads(path.read_text())
    return {"vertices": witness["vertices"]}


if __name__ == "__main__":
    print(run_code())
