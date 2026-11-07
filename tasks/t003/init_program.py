import json
import os
import random

# EVOLVE-BLOCK-START

def run_code():
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T003-C01")
    try: n = {"T003-C01": 26, "T003-C02": 32, "T003-C03": 40}[config]
    except KeyError: raise ValueError(f"unsupported T003 configuration: {config}") from None
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    # A 6 by 6 grid with radius 1/12 gives a simple exact feasible start.
    if n <= 36:
        circles = [{"x": f"{2*c+1}/12", "y": f"{2*r+1}/12", "r": "1/12"}
                   for r in range(6) for c in range(6)][:n]
    else:
        circles = [{"x": f"{2*c+1}/16", "y": f"{2*r+1}/10", "r": "1/16"}
                   for r in range(5) for c in range(8)]
    rng.random()  # Keep the configured seed part of the deterministic program interface.
    return {"circles": circles}

# EVOLVE-BLOCK-END

if __name__ == "__main__":
    print(json.dumps(run_code()))
