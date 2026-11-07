"""Starter program for T009."""
import os, random

def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T009-C01')
    rng=random.Random(int(os.environ.get('MATHBENCH_SEED','0')))
    if config_id == 'T009-C02': n,k=80,20
    elif config_id == 'T009-C03': n,k=100,20
    elif config_id == 'T009-C01': n,k=68,15
    else: raise ValueError('unsupported configuration')
    # EVOLVE-BLOCK-START
    rows=[]
    for i in range(k):
        row=[0]*n
        row[i]=1
        if config_id == 'T009-C01':
            for j in range(k,n): row[j]=rng.randrange(2)
        rows.append(row)
    # EVOLVE-BLOCK-END
    return {'generator_matrix':rows}
