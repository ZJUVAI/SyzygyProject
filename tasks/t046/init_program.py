"""Starter program for T046."""
import os, random

def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T046-C01')
    rng=random.Random(int(os.environ.get('MATHBENCH_SEED','0')))
    if config_id != 'T046-C01': raise ValueError('unsupported configuration')
    n,k=68,15
    # EVOLVE-BLOCK-START
    rows=[]
    for i in range(k):
        row=[0]*n
        row[i]=1
        if config_id == 'T046-C01':
            for j in range(k,n): row[j]=rng.randrange(2)
        rows.append(row)
    # EVOLVE-BLOCK-END
    return {'generator_matrix':rows}
