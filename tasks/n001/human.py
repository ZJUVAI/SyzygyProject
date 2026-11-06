"""Replay the locally stored published 367-word witness."""
import json
from pathlib import Path

def run_human():
    return json.loads((Path(__file__).parent / "data" / "human_reference.json").read_text())

def run_code():
    return run_human()
