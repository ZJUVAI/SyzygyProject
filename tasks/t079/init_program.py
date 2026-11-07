import os


# EVOLVE-BLOCK-START
def run_code():
    """Simple, reference-free construction: put every line through the origin."""
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T079-C01")
    if config_id != "T079-C01":
        raise ValueError("unsupported T079 configuration")
    p = 31
    directions = [(a, b, 1) for a in range(p) for b in range(p)]
    directions += [(a, 1, 0) for a in range(p)]
    directions += [(1, 0, 0)]
    return {"lines": [{"direction": list(d), "origin": [0, 0, 0]} for d in directions]}
# EVOLVE-BLOCK-END
