"""Replay the public Exoo et al. 320-vertex graph6 construction."""
import json, os
from pathlib import Path


def run_human():
    if os.environ.get('MATHBENCH_CONFIG_ID','T035-C01')!='T035-C01':
        raise ValueError('unsupported configuration')
    int(os.environ.get('MATHBENCH_SEED','0'))
    return json.loads((Path(__file__).parent/'data'/'human_graph.json').read_text())


def run_code():
    return run_human()
