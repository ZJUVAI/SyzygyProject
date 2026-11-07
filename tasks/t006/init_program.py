"""Deterministic algebraic seed for T006."""
import os
from lps import build_graph


def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T006-C01')
    if config_id not in ('T006-C01','T006-C02'):
        raise ValueError('unsupported configuration')
    seed=int(os.environ.get('MATHBENCH_SEED','0'))
    # EVOLVE-BLOCK-START
    drop_pairs=((0,2),(0,4),(2,4))
    graph=build_graph(drop_pairs[seed % len(drop_pairs)])
    # EVOLVE-BLOCK-END
    return graph
