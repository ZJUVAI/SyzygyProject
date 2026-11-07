"""Reproduce Samir Loudni's published 86-color ID-VNS witness."""

import json
from pathlib import Path


def run_code():
    witness = json.loads((Path(__file__).parent / "data" / "human_witness.json").read_text())
    return {"colors": witness["colors"], "claimed_objective": witness["published_color_count"]}
