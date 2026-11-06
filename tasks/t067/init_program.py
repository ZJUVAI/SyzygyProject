import os, random

def run_code():
    if os.environ.get('MATHBENCH_CONFIG_ID', 'T067-C01') != 'T067-C01': raise ValueError('unsupported configuration')
    rng = random.Random(int(os.environ.get('MATHBENCH_SEED', '0')))
    # EVOLVE-BLOCK-START
    codewords = [0]
    candidates = list(range(1 << 17)); rng.shuffle(candidates)
    for candidate in candidates:
        if all(bin(candidate ^ word).count('1') >= 6 for word in codewords): codewords.append(candidate)
    # EVOLVE-BLOCK-END
    return {'codewords': codewords}
