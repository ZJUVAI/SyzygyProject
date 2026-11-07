"""Public reproducible baseline from three copies of RM(1,4)."""
import json
import os
from pathlib import Path

def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T009-C01')
    if config_id in ('T009-C02','T009-C03'):
        from tasks.t009.qc import build_matrix
        return {'generator_matrix':build_matrix(config_id)}
    if config_id != 'T009-C01': raise ValueError('unsupported configuration')
    obj=json.loads((Path(__file__).parent/'data'/'human_generator.json').read_text())
    return {'generator_matrix':obj['matrix']}
