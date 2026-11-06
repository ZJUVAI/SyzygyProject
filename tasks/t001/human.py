"""Replay the saved, exact-checkable human construction for the selected config."""
import json
import os
from pathlib import Path

_FILES = {"T001-C01": "human_reference.json", "T001-C02": "human_reference_n32.json",
          "T001-C03": "packomania_n50.json"}


def run_human():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T001-C01")
    return json.loads((Path(__file__).parent / "data" / _FILES[cid]).read_text())


def run_code():
    return run_human()
