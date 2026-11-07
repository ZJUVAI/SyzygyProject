"""Load a Packomania variable-radius witness by configuration."""
import json, os
from pathlib import Path

def run_code():
    config=os.environ.get('MATHBENCH_CONFIG_ID','T003-C01')
    files={'T003-C01':'sota26.json','T003-C02':'sota32.json','T003-C03':'sota40.json'}
    try: name=files[config]
    except KeyError: raise ValueError(f'unsupported T003 configuration: {config}') from None
    return json.loads((Path(__file__).parent/'data'/name).read_text())
