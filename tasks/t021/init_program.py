"""Simple valid Fibonacci-sphere seed; self-contained for cold export."""
import math
import os
import random

_LENGTHS = {"T021-C01": 32, "T021-C02": 40, "T021-C03": 50}

def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T021-C01")
    try:
        n = _LENGTHS[config_id]
    except KeyError as exc:
        raise ValueError(f"unsupported configuration: {config_id}") from exc
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    golden = math.pi * (3.0 - math.sqrt(5.0))
    points=[]
    for k in range(n):
        z=1.0-2.0*(k+0.5)/n
        theta=(k+rng.random()*0.0001)*golden
        radius=math.sqrt(max(0.0,1.0-z*z))
        points.append([radius*math.cos(theta)/(1.0+z),radius*math.sin(theta)/(1.0+z)])
    return {"points":points}
