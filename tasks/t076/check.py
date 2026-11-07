"""Exact checker for positive integer sets with distinct subset sums."""
import math,re,sys
from collections import defaultdict
from functools import reduce
_CONFIGS={
'T076-C01':{'element_count':15,'elements':'positive integers','constraint':'all 2^15 subset sums are distinct','objective':'largest element'},
'T076-C02':{'element_count':16,'elements':'positive integers','constraint':'all 2^16 subset sums are distinct','objective':'largest element'},
'T076-C03':{'element_count':17,'elements':'positive integers','constraint':'all 2^17 subset sums are distinct','objective':'largest element'},}
_POSITIVE_INTEGER_RE=re.compile(r"[1-9][0-9]*\Z")
_HASH_MODULI=((1<<127)-1,(1<<61)-1,(1<<31)-1,(1<<19)-1,(1<<17)-1,(1<<13)-1,(1<<7)-1,31)
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
def _positive_integer(value,label):
    if type(value) is int and value>0:return value
    if isinstance(value,str) and _POSITIVE_INTEGER_RE.fullmatch(value):return int(value)
    raise ValueError(f'{label} must be a positive integer or positive integer string')
def _exact_subset_sum_check(values):
    common=reduce(math.gcd,values);reduced=[v//common for v in values];residues=[[v%m for m in _HASH_MODULI] for v in reduced]
    buckets=defaultdict(list);current=0;current_res=[0]*len(_HASH_MODULI);prev=0;count=1<<len(values)
    for ordinal in range(count):
        gray=ordinal^(ordinal>>1)
        if ordinal:
            changed=gray^prev;bit=changed.bit_length()-1;sign=1 if gray&changed else -1;current+=sign*reduced[bit]
            for j,m in enumerate(_HASH_MODULI):current_res[j]=(current_res[j]+sign*residues[bit][j])%m
        key=tuple(current_res);prior=buckets.get(key)
        if prior is not None:
            for mask in prior:
                total=sum(v for bit,v in enumerate(reduced) if (mask>>bit)&1)
                if total==current:return False,ordinal
            prior.append(gray)
        else:buckets[key]=[gray]
        prev=gray
    return True,count
def _config(config):
    if not isinstance(config,dict):raise ValueError('configuration must be an object')
    cid=config.get('id');params=_CONFIGS.get(cid)
    if params is None:raise ValueError('unsupported configuration')
    if config.get('parameters')!=params:raise ValueError('configuration parameters do not match id')
    return params['element_count']
def validate(solution,config,strict=False):
    del strict;n=_config(config)
    if not isinstance(solution,dict):raise ValueError('solution must be an object')
    raw=solution.get('elements')
    if not isinstance(raw,list) or len(raw)!=n:raise ValueError(f'elements must be a list of exactly {n} positive integers')
    vals=[_positive_integer(v,f'element {i}') for i,v in enumerate(raw)]
    if len(set(vals))!=n:raise ValueError(f'the {n} elements must be distinct')
    valid,count=_exact_subset_sum_check(vals)
    if not valid:raise ValueError('two different subsets have the same sum')
    return {'objective':max(vals),'verification_status':'exact','details':{'element_count':n,'subset_sums_verified':count,'elements_positive':True,'elements_distinct':True,'claimed_objective_ignored':True}}
