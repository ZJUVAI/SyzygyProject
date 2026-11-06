"""Pinned historical human witness, stored within this task."""
import json
import os
from pathlib import Path

FILES = {"T073-C01": "human_labs100_record.json",
         "T073-C02": "human_labs80_record.json",
         "T073-C03": "human_labs120_record.json"}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T073-C01")
    data = json.loads((Path(__file__).parent / "data" / FILES[config_id]).read_text())
    return {"sequence": data["sequence"]}
