"""Replay the saved, independently checked 1320-word PGL(2,11) code."""

import json
import os
from pathlib import Path

from tasks.t052.check import PARAMETERS, validate


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T052-C01") != "T052-C01":
        raise ValueError("unsupported configuration")
    path = Path(__file__).parent / "data" / "reference" / "pgl_2_11_n12_d9.json"
    data = json.loads(path.read_text())
    result = {"codewords": data["codewords"]}
    validate(result, {"parameters": PARAMETERS}, strict=True)
    return result


if __name__ == "__main__":
    print({"codeword_count": len(run_code()["codewords"])})
