"""Replay the official 60-second BouMS assignment for the selected instance."""

import json
import os
from pathlib import Path

from tasks.t055.check import PARAMETERS, validate


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T055-C01") != "T055-C01":
        raise ValueError("unsupported configuration")
    path = Path(__file__).parent / "data" / "reference" / "mse2026_boums_60_assignment.json"
    saved = json.loads(path.read_text())
    result = {"assignment": [bool(value) for value in saved["assignment"]]}
    validate(result, {"parameters": PARAMETERS}, strict=True)
    return result


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
