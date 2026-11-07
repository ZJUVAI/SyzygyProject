"""Public classical BCH-derived reproducible construction, separate from the 258-word record."""
import os

GENERATOR = sum(1 << i for i in (0,2,4,6,7,9,10,13,17,18,20))

def _shortened_bch(n, shortened_coordinates):
    punctured_coordinate=max(shortened_coordinates)+1
    kept=[j for j in range(31) if j not in shortened_coordinates and j!=punctured_coordinate]
    words=[]
    for message in range(1 << 11):
        word=0
        for i in range(11):
            if (message >> i) & 1: word ^= GENERATOR << i
        if any((word >> j) & 1 for j in shortened_coordinates): continue
        words.append(sum(((word >> j)&1) << i for i,j in enumerate(kept)))
    if len(kept)!=n: raise AssertionError('wrong shortened BCH length')
    return words

def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID', 'T010-C01')
    if config_id=='T010-C01':
        import json
        from pathlib import Path
        data=json.loads((Path(__file__).parent/'data'/'bch_extended_128.json').read_text())
        return {'codewords':data['codewords']}
    cases={'T010-C02':(23,range(7)),'T010-C03':(25,range(5))}
    if config_id not in cases: raise ValueError('unsupported configuration')
    n,coordinates=cases[config_id]
    return {'codewords':_shortened_bch(n,list(coordinates))}
