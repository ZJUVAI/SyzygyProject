"""Reproduce the best published LABS witnesses recorded for T013."""

import json
import os
from pathlib import Path

from check import validate


_ROOT = Path(__file__).parent
_WITNESSES = {
    "T013-C01": "human_labs100_record.json",
    "T013-C02": "human_labs80_record.json",
    "T013-C03": "sota_labs120.json",
}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T013-C01")
    if config_id not in _WITNESSES:
        raise ValueError(f"unsupported T013 configuration: {config_id}")
    data = json.loads((_ROOT / "data" / _WITNESSES[config_id]).read_text())
    sequence = data["sequence"]
    expected_length = {"T013-C01": 100, "T013-C02": 80, "T013-C03": 120}[config_id]
    if len(sequence) != expected_length:
        raise ValueError("stored witness has the wrong length")
    return {"sequence": sequence}


if __name__ == "__main__":
    result = run_code()
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T013-C01")
    length = {"T013-C01": 100, "T013-C02": 80, "T013-C03": 120}[config_id]
    print(validate(result, {"parameters": {"L": length}})["objective"])
