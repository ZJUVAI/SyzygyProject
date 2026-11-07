"""Exact bit-parallel zero-one verifier for sorting networks."""
from functools import lru_cache

_CONFIGS={"T048-C01":17,"T048-C02":18,"T048-C03":19}
@lru_cache(maxsize=3)
def _input_bitsets(inputs):
    lanes=1<<inputs;patterns=[]
    for wire in range(inputs):
        period=1<<(wire+1);half=1<<wire;block=(1<<half)-1;pattern=0
        for start in range(half,lanes,period):pattern|=block<<start
        patterns.append(pattern)
    return tuple(patterns)
def _comparators(solution,inputs):
    if not isinstance(solution,dict) or "comparators" not in solution:raise ValueError("solution must contain comparators")
    comps=solution["comparators"]
    if not isinstance(comps,(list,tuple)):raise ValueError("comparators must be an ordered list")
    out=[]
    for item in comps:
        if not isinstance(item,(list,tuple)) or len(item)!=2:raise ValueError("each comparator must contain exactly two wire indices")
        left,right=item
        if type(left) is not int or type(right) is not int:raise ValueError("wire indices must be strict integers")
        if not (0<=left<right<inputs):raise ValueError(f"comparator indices must satisfy 0 <= left < right < {inputs}")
        out.append((left,right))
    return out
def _zero_one_check(comps,inputs):
    lanes=1<<inputs;all_lanes=(1<<lanes)-1;wires=list(_input_bitsets(inputs))
    for a,b in comps:wires[a],wires[b]=wires[a]&wires[b],wires[a]|wires[b]
    for i in range(inputs-1):
        if wires[i]&(~wires[i+1]&all_lanes):raise ValueError("network fails exact zero-one sorting check")
def _asap_depth(comps,inputs):
    last=[0]*inputs
    for a,b in comps:
        layer=max(last[a],last[b])+1;last[a]=last[b]=layer
    return max(last,default=0)
def validate(solution,config,strict=False):
    del strict
    if not isinstance(config,dict):raise ValueError("configuration must be an object")
    cid=config.get('id');inputs=_CONFIGS.get(cid)
    if inputs is None:raise ValueError("unsupported configuration")
    params=config.get('parameters',{})
    if params and params.get('inputs')!=inputs:raise ValueError("configuration parameters do not match id")
    comps=_comparators(solution,inputs);_zero_one_check(comps,inputs)
    return {'objective':len(comps),'verification_status':'exact','details':{'inputs':inputs,'comparators_checked':len(comps),'binary_inputs_checked':1<<inputs,'asap_depth':_asap_depth(comps,inputs),'zero_one_principle':True,'claimed_objective_ignored':True}}
