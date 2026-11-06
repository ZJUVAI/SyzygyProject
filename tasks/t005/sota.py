"""Replay the current Packomania best-known variable-radius witnesses."""
import json
import os
from pathlib import Path


def run_code():
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T005-C01")
    filenames = {"T005-C01": "sota26.json", "T005-C02": "sota32.json"}
    try:
        filename = filenames[config]
    except KeyError as exc:
        raise ValueError(f"unsupported T005 configuration: {config}") from exc
    return json.loads((Path(__file__).parent / "data" / filename).read_text())
