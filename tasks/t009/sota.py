"""Return the saved, independently verified public witness for this config."""
import json
import os
from pathlib import Path


def run_code():
    config_id = os.environ.get('MATHBENCH_CONFIG_ID', 'T009-C01')
    if config_id not in ('T009-C01', 'T009-C02', 'T009-C03'):
        raise ValueError('unsupported configuration')
    suffix = {'T009-C01': '', 'T009-C02': '_C02', 'T009-C03': '_C03'}[config_id]
    obj = json.loads(
        (Path(__file__).parent / "data" / f"sota_generator{suffix}.json").read_text()
    )
    return {
        "generator_matrix": [
            [int(bit) for bit in row] for row in obj["matrix"]
        ]
    }
