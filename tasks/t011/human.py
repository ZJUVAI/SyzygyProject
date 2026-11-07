"""Replay frozen public or traditional product constructions by configuration."""
import json
import os
from pathlib import Path


def run_human():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T011-C01")
    paths = {
        "T011-C01": "human_reference.json",
        "T011-C02": "human_product_C7_4_100.json",
        "T011-C03": "human_product_C7_6_1101.json",
    }
    try:
        filename = paths[config_id]
    except KeyError as exc:
        raise ValueError(f"unsupported configuration: {config_id}") from exc
    return json.loads((Path(__file__).parent / "data" / filename).read_text())


def run_code():
    return run_human()
