"""Reproduce the printed 20-step Matolcsi–Vinuesa construction."""
import json
from pathlib import Path


def run_code():
    witness = Path(__file__).parent / "data" / "human_t080.json"
    data = json.loads(witness.read_text())
    return {"coefficients": data["coefficients"]}
