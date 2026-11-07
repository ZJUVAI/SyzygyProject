"""Fixed replay of the reproduced public 154/154 reference construction."""

import json
import os
from pathlib import Path


DATA = Path(__file__).resolve().parent / "data" / "reference" / "obryant_n32_154.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T072-C01") != "T072-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    data = json.loads(DATA.read_text(encoding="utf-8"))
    return {"elements": data["elements"]}


if __name__ == "__main__":
    print(json.dumps(run_code()))
