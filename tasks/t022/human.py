"""Reproduce Exoo's public 42-vertex witness from McKay's graph6 archive."""
import json
from pathlib import Path


def run_code():
    witness = json.loads((Path(__file__).parent / "data" / "human_witness.json").read_text())
    return {"adjacency": witness["adjacency"]}
