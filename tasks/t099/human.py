"""Thomas Engelsma's 2013 published witness, copied from the audited source artifact."""
import json
from pathlib import Path


def run_code():
    record = json.loads((Path(__file__).parent / "data" / "human_343.json").read_text())
    return {"tuple": record["witness"]}
