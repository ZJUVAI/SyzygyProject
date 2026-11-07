"""Load the task's public, independently checkable reference construction."""
import json
import os
from pathlib import Path

def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T009-C01')
    if config_id not in ('T009-C01','T009-C02','T009-C03'):
        raise ValueError('unsupported configuration')
    if config_id == 'T009-C01':
        obj=json.loads((Path(__file__).parent/'data'/'search_generator.json').read_text())
        return {'generator_matrix':obj['matrix']}
    suffix={'T009-C02':'_C02','T009-C03':'_C03'}[config_id]
    obj=json.loads((Path(__file__).parent/'data'/f'sota_generator{suffix}.json').read_text())
    return {'generator_matrix':[[int(bit) for bit in row] for row in obj['matrix']]}
