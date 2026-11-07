"""Exact integer checker for binary aperiodic PSL configurations."""
CONFIGS = {
    "T054-C01": {"parameters": {"length": 100}},
    "T054-C02": {"parameters": {"length": 101}},
    "T054-C03": {"parameters": {"length": 102}},
}
CONFIG_ID = "T054-C01"
LENGTH = 100
ALPHABET = [-1, 1]
PARAMETERS = {"length": LENGTH, "alphabet": ALPHABET, "correlation": "aperiodic", "objective": "max absolute off-zero autocorrelation"}

def config_id():
    import os
    return os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)

def config_length(cid=None):
    cid = cid or config_id()
    if cid not in CONFIGS: raise ValueError(f"unsupported configuration: {cid}")
    return CONFIGS[cid]["parameters"]["length"]

def aperiodic_autocorrelations(sequence):
    return [sum(sequence[i] * sequence[i + lag] for i in range(len(sequence)-lag)) for lag in range(1,len(sequence))]

def _check_config(config):
    if not isinstance(config,dict): raise ValueError("configuration must be an object")
    cid=config.get("id",CONFIG_ID)
    if cid not in CONFIGS: raise ValueError(f"unsupported configuration: {cid}")
    expected=CONFIGS[cid]["parameters"]
    params=config.get("parameters")
    if not isinstance(params,dict) or type(params.get("length")) is not int or params.get("length") != expected["length"] or params.get("alphabet") != ALPHABET or params.get("correlation") != "aperiodic" or params.get("objective") != PARAMETERS["objective"]: raise ValueError("configuration parameters do not match a registered T054 configuration")
    return expected["length"]

def validate(solution, config, strict=False):
    del strict
    length=_check_config(config)
    if not isinstance(solution,dict): raise ValueError("solution must be an object")
    sequence=solution.get("sequence")
    if not isinstance(sequence,list) or len(sequence)!=length: raise ValueError(f"sequence must be a list of exactly {length} signs")
    if any(type(v) is not int or v not in (-1,1) for v in sequence): raise ValueError("sequence entries must be integer -1 or +1; bool is invalid")
    correlations=aperiodic_autocorrelations(sequence); peak=max(map(abs,correlations))
    return {"objective":peak,"verification_status":"exact","details":{"length":length,"aperiodic_autocorrelations":correlations,"peak_sidelobe_lag":max(range(1,length),key=lambda k:abs(correlations[k-1])),"claimed_objective_ignored":True}}
