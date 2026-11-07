"""Reproducible human construction baselines, selected by configuration."""
import json, os
from pathlib import Path

def run_code():
    cid=os.environ.get('MATHBENCH_CONFIG_ID','T002-C01')
    name={'T002-C01':'data/human_friedman_1997.json','T002-C02':'data/human_schadt_2025.json','T002-C03':'data/human_gobel_figure1.json'}.get(cid)
    if name is None: raise ValueError('unknown T002 configuration')
    return json.loads((Path(__file__).parent/name).read_text())
