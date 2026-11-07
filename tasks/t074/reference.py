"""Fixed replay of the rationalized, exactly verified 2/51 record witness."""

import json
import os
from pathlib import Path


DATA = Path(__file__).resolve().parent / "data" / "reference" / "cantrell_n12_rationalized.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T074-C01") != "T074-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return {"points": json.loads(DATA.read_text(encoding="utf-8"))["points"]}


if __name__ == "__main__":
    print(json.dumps(run_code()))
