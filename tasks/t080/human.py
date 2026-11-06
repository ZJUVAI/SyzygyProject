"""Pinned, exactly recomputed 2009 human witness."""
import json
from pathlib import Path


def run_code():
    data = json.loads((Path(__file__).parent / "data" / "human_t080.json").read_text())
    return {"coefficients": data["coefficients"]}
