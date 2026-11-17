"""Public reproducible baseline from three copies of RM(1,4)."""
import json
import os
from pathlib import Path

def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T046-C01')
    if config_id != 'T046-C01': raise ValueError('unsupported configuration')
    obj=json.loads((Path(__file__).parent/'data'/'human_generator.json').read_text())
    return {'generator_matrix':obj['matrix']}
