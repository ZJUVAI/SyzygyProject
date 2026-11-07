import os
import random

def _config():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T016-C01")
    if config_id != "T016-C01":
        raise ValueError("unsupported configuration: " + config_id)
    return config_id

def run_code():
    _config()
    # EVOLVE-BLOCK-START
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    coefficients = [rng.uniform(-0.15, 1.0) for _ in range(208)]
    mean = sum(coefficients) / len(coefficients)
    coefficients = [x - mean + 1.0 for x in coefficients]
    # EVOLVE-BLOCK-END
    return {"coefficients": coefficients}
