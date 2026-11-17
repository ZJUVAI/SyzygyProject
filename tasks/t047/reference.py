import json, os
from pathlib import Path

def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID', 'T047-C01')
    if config_id != 'T047-C01': raise ValueError('unsupported configuration')
    data = json.loads((Path(__file__).parent/'data'/'bch_extended_128.json').read_text())
    return {'codewords': data['codewords']}
