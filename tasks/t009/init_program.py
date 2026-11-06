import json
import os
import random

# EVOLVE-BLOCK-START

def run_code():
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    n = {"T009-C02": 16, "T009-C03": 17, "T009-C04": 19}.get(os.environ.get("MATHBENCH_CONFIG_ID", "T009-C02"))
    if n is None: raise ValueError("unknown T009 configuration")
    points = []
    # Fibonacci directions give a deterministic, nonzero start for all seeds.
    for k in range(n):
        z = 1 - 2 * (k + 0.5) / n
        phi = (k + rng.random() * 0.001) * (3.141592653589793 * (3 - 5**0.5))
        r = max(0.0, 1-z*z) ** 0.5
        points.append([r * __import__("math").cos(phi), r * __import__("math").sin(phi), z])
    return {"points": points}

# EVOLVE-BLOCK-END

if __name__ == "__main__":
    print(json.dumps(run_code()))
