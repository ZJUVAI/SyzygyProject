import json
import math
import os
import random

# EVOLVE-BLOCK-START

CONFIG_SIZES = {'T040-C01': 11, 'T040-C02': 13, 'T040-C03': 15}


def configured_size():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T040-C01")
    try:
        return CONFIG_SIZES[config_id]
    except KeyError:
        raise ValueError(f"unsupported configuration: {config_id}") from None


def run_code():
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    n = configured_size()
    golden = math.pi * (3.0 - math.sqrt(5.0))
    parameters = []
    for k in range(n):
        z = 1.0 - 2.0 * (k + 0.5) / n
        theta = k * golden + rng.uniform(-0.002, 0.002)
        radius = math.sqrt(max(0.0, 1.0 - z * z))
        x, y = radius * math.cos(theta), radius * math.sin(theta)
        # The checker maps any finite parameter pair exactly onto S².
        parameters.append([x / (1.0 + z), y / (1.0 + z)])
    return {"stereographic": parameters}

# EVOLVE-BLOCK-END

if __name__ == "__main__":
    print(json.dumps(run_code()))
