import json, os
from pathlib import Path

def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID', 'T010-C01')
    names={'T010-C01':'bch_extended_128.json','T010-C02':'parity_extended_23_84_10.json','T010-C03':'parity_extended_25_196_10.json'}
    if config_id not in names: raise ValueError('unsupported configuration')
    data = json.loads((Path(__file__).parent/'data'/names[config_id]).read_text())
    return {'codewords': data['codewords']}
