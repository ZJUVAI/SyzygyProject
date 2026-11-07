"""Reproduce the current cube20.org Golomb ruler records for T007."""

import json
import os
from pathlib import Path


_DATA = {
    "T007-C01": ("public_29.json", None),
    "T007-C02": ("public_30_32.json", "T007-C02"),
    "T007-C03": ("public_30_32.json", "T007-C03"),
}


def run_code():
    """Return the published ruler witness for the selected configuration."""
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T007-C01")
    try:
        filename, key = _DATA[config_id]
    except KeyError as exc:
        raise ValueError(f"unknown T007 configuration: {config_id}") from exc

    path = Path(__file__).parent / "data" / filename
    data = json.loads(path.read_text())
    entry = data if key is None else data[key]
    return {"marks": list(entry["marks"])}


if __name__ == "__main__":
    print(json.dumps(run_code()))
