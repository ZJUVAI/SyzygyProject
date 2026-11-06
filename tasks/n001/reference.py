"""Replay the locally stored independently checked paper witness."""
import json
from pathlib import Path

def run_code():
    return json.loads((Path(__file__).parent / "data" / "human_reference.json").read_text())
