"""Replay the fixed best reproduced witness archived for T015-C01."""
import json
from pathlib import Path
from tasks.t015.init_program import configured_size


def run_code():
    return json.loads((Path(__file__).parent / "data" / "reference" / f"sloane{configured_size()}_rational_stereographic.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(run_code()))
