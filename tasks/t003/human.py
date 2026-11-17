"""Reproducible human construction baselines, selected by configuration."""
import json, os
from pathlib import Path

def run_code():
    cid=os.environ.get('MATHBENCH_CONFIG_ID','T003-C01')
    if cid != 'T003-C01': raise ValueError('unknown T003 configuration')
    return json.loads((Path(__file__).parent/'data/human_friedman_1997.json').read_text())
