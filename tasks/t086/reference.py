"""Load the fixed, locally normalized Laderman witness for external comparison."""
import json
from pathlib import Path

_DATA = Path(__file__).parent / "data" / "laderman_rank23.json"


def run_code():
    payload = json.loads(_DATA.read_text())
    return {"terms": payload["terms"]}
