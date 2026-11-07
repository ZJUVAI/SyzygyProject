"""Pinned exact-rational transcription of Haugland's printed 51-step witness."""
import json
from pathlib import Path


def run_code():
    data = json.loads((Path(__file__).parent / "data" / "human_t017.json").read_text())
    return {"heights": data["coefficients"]}
