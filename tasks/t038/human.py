"""Replay the published five-square witness preserved from Sage's database."""
import json
from pathlib import Path


DATA = Path(__file__).parent / "data/source/mckay_mols12_5.json"


def run_code():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    return {"squares": data["squares"], "objective": 5}
