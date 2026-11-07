import os, random

def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID', 'T010-C01')
    if config_id not in ('T010-C01','T010-C02','T010-C03'): raise ValueError('unsupported configuration')
    rng = random.Random(int(os.environ.get('MATHBENCH_SEED', '0')))
    if config_id != 'T010-C01':
        # Deliberately simple cold seed. It does not inspect any reference file.
        return {'codewords':[0]}
    # EVOLVE-BLOCK-START
    codewords = [0]
    candidates = list(range(1 << 17)); rng.shuffle(candidates)
    for candidate in candidates:
        if all(bin(candidate ^ word).count('1') >= 6 for word in codewords): codewords.append(candidate)
    # EVOLVE-BLOCK-END
    return {'codewords': codewords}
