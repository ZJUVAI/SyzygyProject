"""Load the fixed human constructions for T003."""
import json
import os
from pathlib import Path

def load_witness(prefix):
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T003-C02")
    if config != "T003-C02":
        raise ValueError(f"unsupported T003 configuration: {config}") from None
    return json.loads((Path(__file__).parent / "data" / f"{prefix}32.json").read_text())


def run_code():
    return load_witness("human")
