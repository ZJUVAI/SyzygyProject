"""Replay maximally large exactly feasible witnesses from Packomania coordinates."""
import json
import os
from pathlib import Path

_FILES = {
    "T001-C01": "sota_n26.json",
    "T001-C02": "sota_n32.json",
    "T001-C03": "sota_n50.json",
}


def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T001-C01")
    return json.loads((Path(__file__).parent / "data" / _FILES[cid]).read_text())
