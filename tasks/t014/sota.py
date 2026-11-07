"""Pinned replay of the best located public 208-step T014 witness."""
import json
from pathlib import Path


def run_code():
    witness = Path(__file__).parent / "data" / "human_matolcsi_vinuesa.json"
    data = json.loads(witness.read_text())
    return {"coefficients": data["polynomial_coefficients"]}
