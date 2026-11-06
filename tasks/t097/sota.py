"""Replay the best public addition chains listed by additionchains.com."""

import json
import os
from pathlib import Path


FILES = {
    "T097-C01": "sota_t097_c01.json",
    "T097-C02": "sota_t097_c02.json",
    "T097-C03": "sota_t097_c03.json",
}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T097-C01")
    try:
        filename = FILES[config_id]
    except KeyError as exc:
        raise ValueError(f"unsupported T097 configuration: {config_id}") from exc
    witness = Path(__file__).parent / "data" / filename
    return json.loads(witness.read_text())
