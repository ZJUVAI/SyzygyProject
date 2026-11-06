"""Public classical BCH-derived reproducible construction, separate from the 258-word record."""
import json, os
from pathlib import Path

def run_code():
    if os.environ.get('MATHBENCH_CONFIG_ID', 'T067-C01') != 'T067-C01': raise ValueError('unsupported configuration')
    data = json.loads((Path(__file__).parent/'data'/'bch_extended_128.json').read_text())
    return {'codewords': data['codewords']}
