"""Replay the best public addition chains listed by additionchains.com."""

import json
import os
from pathlib import Path


FILES = {
    "T088-C01": "human_t088.json",
}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T088-C01")
    try:
        filename = FILES[config_id]
    except KeyError as exc:
        raise ValueError(f"unsupported T088 configuration: {config_id}") from exc
    witness = Path(__file__).parent / "data" / filename
    return json.loads(witness.read_text())
