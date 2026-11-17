"""Load the fixed MIT-published human tuple for k=343."""
import json
from pathlib import Path


def run_code():
    record = json.loads((Path(__file__).parent / "data" / "human_343.json").read_text())
    return {"tuple": record["witness"] if "witness" in record else record["tuple"]}
