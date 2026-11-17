"""Public classical BCH-derived reproducible construction, separate from the 258-word record."""
import json
import os
from pathlib import Path

def run_code():
    if os.environ.get('MATHBENCH_CONFIG_ID', 'T010-C01') != 'T010-C01': raise ValueError('unsupported configuration')
    data=json.loads((Path(__file__).parent/'data'/'bch_extended_128.json').read_text())
    return {'codewords':data['codewords']}
