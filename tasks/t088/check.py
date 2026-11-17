"""Exact checker for the ordinary addition chain for the P-192 exponent."""
TARGET_TEXT = "2^192-2^64-3"
TARGET = 2**192 - 2**64 - 3
CONFIG_ID = "T088-C01"


def validate(solution, config, strict=False):
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    cid = config.get("id", CONFIG_ID)
    params = config.get("parameters", config)
    if cid != CONFIG_ID or not isinstance(params, dict) or params.get("target") != TARGET_TEXT:
        raise ValueError("configuration must be T088-C01")
    target = TARGET
    chain = solution.get("chain")
    if not isinstance(chain, list) or len(chain) < 2:
        raise ValueError("chain must be a list with at least two entries")
    if any(isinstance(x, bool) or not isinstance(x, int) for x in chain):
        raise ValueError("chain entries must be integers, not booleans")
    if chain[0] != 1:
        raise ValueError("chain must start at 1")
    previous = {1}
    for i in range(1, len(chain)):
        if chain[i] <= chain[i-1]:
            raise ValueError("chain must be strictly increasing")
        # Set membership checks the exact same sum rule. The two addends may
        # coincide. This uses O(L^2) total work for an L-entry chain.
        if not any(chain[i] - value in previous for value in previous):
            raise ValueError(f"chain entry at index {i} is not a sum of two earlier entries")
        previous.add(chain[i])
    if chain[-1] != target:
        raise ValueError("chain endpoint does not equal the selected target")
    # Every addition is checked exactly with Python integers; strict mode needs no
    # relaxation because this certificate covers every step and the endpoint.
    return {"objective": len(chain)-1, "verification_status": "exact",
            "details": {"target": str(target), "chain_entries": len(chain), "configuration_id": cid,
                        "strictly_increasing": True, "all_steps_verified": True}}
