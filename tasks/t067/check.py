"""Exact pairwise-distance validator for binary A(17,6) witnesses."""
N, D = 17, 6

def _word(value):
    if type(value) is int:
        if value < 0 or value >= (1 << N): raise ValueError('integer codeword out of range')
        return value
    if not isinstance(value, (list, tuple)) or len(value) != N: raise ValueError('codeword must be an integer or 17-bit list')
    packed = 0
    for i, bit in enumerate(value):
        if type(bit) is not int or bit not in (0, 1): raise ValueError('bits must be integer 0 or 1; bool is rejected')
        packed |= bit << i
    return packed

def validate(solution, config, strict=False):
    if config.get('parameters') != {'n': 17, 'distance': 6}: raise ValueError('unsupported configuration')
    if not isinstance(solution, dict) or 'codewords' not in solution: raise ValueError('solution must contain codewords')
    raw = solution['codewords']
    if not isinstance(raw, (list, tuple)) or not raw: raise ValueError('codewords must be a non-empty list')
    words = [_word(x) for x in raw]
    if len(set(words)) != len(words): raise ValueError('duplicate codewords')
    min_distance, checked = N, 0
    for i, a in enumerate(words):
        for b in words[i+1:]:
            dist = bin(a ^ b).count('1'); checked += 1
            if dist < D: raise ValueError('pairwise distance below 6')
            min_distance = min(min_distance, dist)
    claimed = solution.get('objective')
    mismatch = claimed is not None and (type(claimed) is not int or claimed != len(words))
    return {'objective': len(words), 'verification_status': 'exact', 'details': {'n': N, 'minimum_pairwise_distance': min_distance if len(words)>1 else None, 'pairs_checked': checked, 'claimed_objective_mismatch': mismatch}}
