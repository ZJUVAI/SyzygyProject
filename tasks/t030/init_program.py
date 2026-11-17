"""Deterministic algebraic seed for T030."""
import os
from lps import build_graph


def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T030-C01')
    if config_id != 'T030-C01':
        raise ValueError('unsupported configuration')
    seed=int(os.environ.get('MATHBENCH_SEED','0'))
    # EVOLVE-BLOCK-START
    drop_pairs=((0,2),(0,4),(2,4))
    graph=build_graph(drop_pairs[seed % len(drop_pairs)])
    # EVOLVE-BLOCK-END
    return graph
