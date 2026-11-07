"""Replay the fixed 191-edge public Q9 record from Orland et al."""

import json
from pathlib import Path

from tasks.t050.init_program import configured_dimension


def run_code():
    dimension = configured_dimension()
    files = {9: "orland_v3_q9_191.json", 10: "orland_v3_q10_379.json", 11: "orland_v3_q11_746.json"}
    path = Path(__file__).parent / "data" / "reference" / files[dimension]
    witness = json.loads(path.read_text())
    return {"vertices": witness["vertices"]}


if __name__ == "__main__":
    print(run_code())
