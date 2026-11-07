"""Load the fixed human constructions for T003."""
import json
import os
from pathlib import Path

_SIZES = {"T003-C01": 26, "T003-C02": 32, "T003-C03": 40}


def load_witness(prefix):
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T003-C01")
    try:
        size = _SIZES[config]
    except KeyError:
        raise ValueError(f"unsupported T003 configuration: {config}") from None
    return json.loads((Path(__file__).parent / "data" / f"{prefix}{size}.json").read_text())


def run_code():
    return load_witness("human")
