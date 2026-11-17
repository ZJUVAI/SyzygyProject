"""Replay the first 41-vertex, 132-edge graph in the public archive."""
import json
from pathlib import Path

def run_code():
    return json.loads((Path(__file__).parent / "data" / "human_witness.json").read_text())
