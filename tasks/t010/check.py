"""Exact pairwise-distance validator for configured binary codes."""

def _parameters(config):
    p = config.get('parameters', {})
    n, d = p.get('n'), p.get('distance')
    if type(n) is not int or type(d) is not int or (n,d) not in {(17,6),(23,10),(25,10)}:
        raise ValueError('unsupported configuration')
    return n, d

def _word(value, n):
    if type(value) is int:
        if value < 0 or value >= (1 << n): raise ValueError('integer codeword out of range')
        return value
    if not isinstance(value, (list, tuple)) or len(value) != n: raise ValueError(f'codeword must be an integer or {n}-bit list')
    packed = 0
    for i, bit in enumerate(value):
        if type(bit) is not int or bit not in (0, 1): raise ValueError('bits must be integer 0 or 1; bool is rejected')
        packed |= bit << i
    return packed

def validate(solution, config, strict=False):
    n, d = _parameters(config)
    if not isinstance(solution, dict) or 'codewords' not in solution: raise ValueError('solution must contain codewords')
    raw = solution['codewords']
    if not isinstance(raw, (list, tuple)) or not raw: raise ValueError('codewords must be a non-empty list')
    words = [_word(x, n) for x in raw]
    if len(set(words)) != len(words): raise ValueError('duplicate codewords')
    min_distance, checked = n, 0
    for i, a in enumerate(words):
        for b in words[i+1:]:
            dist = (a ^ b).bit_count(); checked += 1
            if dist < d: raise ValueError(f'pairwise distance below {d}')
            min_distance = min(min_distance, dist)
    return {'objective': len(words), 'verification_status': 'exact', 'details': {'n': n, 'minimum_pairwise_distance': min_distance if len(words)>1 else None, 'pairs_checked': checked, 'claimed_objective_ignored': True}}
