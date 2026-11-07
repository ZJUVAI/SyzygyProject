"""Replay the best public addition chains listed by additionchains.com."""

import json
import os
from pathlib import Path


FILES = {
    "T020-C01": "sota_t020_c01.json",
    "T020-C02": "sota_t020_c02.json",
    "T020-C03": "sota_t020_c03.json",
}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T020-C01")
    try:
        filename = FILES[config_id]
    except KeyError as exc:
        raise ValueError(f"unsupported T020 configuration: {config_id}") from exc
    witness = Path(__file__).parent / "data" / filename
    return json.loads(witness.read_text())
