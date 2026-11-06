"""Published human witness reproduced from Orrick et al. (2003)."""
import json
from pathlib import Path


def run_code():
    data = json.loads((Path(__file__).parent / "data" / "human_order29.json").read_text())
    return {"matrix": [[1 if c == "+" else -1 for c in row] for row in data["matrix"]]}
