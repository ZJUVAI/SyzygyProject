"""Starter program for T066."""
import os, random

def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T066-C01')
    if config_id != 'T066-C01': raise ValueError('unsupported configuration')
    rng=random.Random(int(os.environ.get('MATHBENCH_SEED','0')))
    # EVOLVE-BLOCK-START
    rows=[]
    for i in range(15):
        row=[0]*68
        row[i]=1
        for j in range(15,68):
            row[j]=rng.randrange(2)
        rows.append(row)
    # EVOLVE-BLOCK-END
    return {'generator_matrix':rows}
