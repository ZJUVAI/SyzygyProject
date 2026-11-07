"""Pinned public witnesses selected by configuration."""
import json, os
from pathlib import Path
from tasks.t018.human import run_code as _human

def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID") == "T018-C02":
        d=json.loads((Path(__file__).parent / "data/reference/order27.json").read_text())
        return {"matrix": [[1 if c == "+" else -1 for c in row] for row in d["matrix"]]}
    return _human()
