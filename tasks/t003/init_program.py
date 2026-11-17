import json
import os
import random

# EVOLVE-BLOCK-START

def run_code():
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T003-C02")
    if config != "T003-C02":
        raise ValueError(f"unsupported T003 configuration: {config}")
    n = 32
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    # A 6 by 6 grid with radius 1/12 gives a simple exact feasible start.
    circles = [{"x": f"{2*c+1}/12", "y": f"{2*r+1}/12", "r": "1/12"}
               for r in range(6) for c in range(6)][:n]
    rng.random()  # Keep the configured seed part of the deterministic program interface.
    return {"circles": circles}

# EVOLVE-BLOCK-END

if __name__ == "__main__":
    print(json.dumps(run_code()))
