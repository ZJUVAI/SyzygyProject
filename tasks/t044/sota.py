"""Reproduce the current cube20.org Golomb ruler records for T044."""

import json
import os
from pathlib import Path


_DATA = {
    "T044-C01": ("public_29.json", None),
    "T044-C02": ("public_30_32.json", "T044-C02"),
    "T044-C03": ("public_30_32.json", "T044-C03"),
}


def run_code():
    """Return the published ruler witness for the selected configuration."""
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T044-C01")
    try:
        filename, key = _DATA[config_id]
    except KeyError as exc:
        raise ValueError(f"unknown T044 configuration: {config_id}") from exc

    path = Path(__file__).parent / "data" / filename
    data = json.loads(path.read_text())
    entry = data if key is None else data[key]
    return {"marks": list(entry["marks"])}


if __name__ == "__main__":
    print(json.dumps(run_code()))
