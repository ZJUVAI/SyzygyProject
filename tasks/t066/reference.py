"""Load the task's public, independently checkable reference construction."""
import json
import os
from pathlib import Path

def run_code():
    if os.environ.get('MATHBENCH_CONFIG_ID','T066-C01') != 'T066-C01':
        raise ValueError('unsupported configuration')
    obj=json.loads((Path(__file__).parent/'data'/'search_generator.json').read_text())
    return {'generator_matrix':obj['matrix']}
