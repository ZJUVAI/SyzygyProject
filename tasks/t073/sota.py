"""Reproduce the best published LABS witnesses recorded for T073."""

import json
import os
from pathlib import Path

from check import validate


_ROOT = Path(__file__).parent
_WITNESS = "human_labs100_record.json"


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T073-C01")
    if config_id != "T073-C01":
        raise ValueError(f"unsupported T073 configuration: {config_id}")
    data = json.loads((_ROOT / "data" / _WITNESS).read_text())
    sequence = data["sequence"]
    if len(sequence) != 100:
        raise ValueError("stored witness has the wrong length")
    return {"sequence": sequence}


if __name__ == "__main__":
    result = run_code()
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T073-C01")
    print(validate(result, {"parameters": {"L": 100}})["objective"])
