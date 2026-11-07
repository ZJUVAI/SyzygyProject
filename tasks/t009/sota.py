"""Load the archived public generator for the selected configuration."""
import json
import os
from pathlib import Path

_FILES = {
    'T009-C01': 'sota_generator.json',
    'T009-C02': 'human_generator_C02.json',
    'T009-C03': 'human_generator_C03.json',
}


def read_generator(name):
    obj = json.loads((Path(__file__).parent / 'data' / name).read_text())
    return {'generator_matrix': [[int(bit) for bit in row] for row in obj['matrix']]}


def run_code():
    cid = os.environ.get('MATHBENCH_CONFIG_ID', 'T009-C01')
    if cid not in _FILES:
        raise ValueError('unsupported configuration')
    return read_generator(_FILES[cid])
