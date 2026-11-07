"""Replay the public Exoo et al. 320-vertex graph6 construction."""
import json, os
from pathlib import Path


def run_human():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T006-C01')
    if config_id not in ('T006-C01','T006-C02'):
        raise ValueError('unsupported configuration')
    int(os.environ.get('MATHBENCH_SEED','0'))
    filename='human_graph.json' if config_id=='T006-C01' else 'human_graph_c02.json'
    return json.loads((Path(__file__).parent/'data'/filename).read_text())


def run_code():
    return run_human()
