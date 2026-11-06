"""Replay the best checked public k=343 witness in this task package."""

import json
from pathlib import Path


def run_code():
    """Return the published admissible tuple; the evaluator recomputes its score."""
    record = json.loads((Path(__file__).parent / "data" / "human_343.json").read_text())
    return {"tuple": record["witness"]}
