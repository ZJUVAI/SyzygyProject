"""Reconstruct the classical D5 root-system kissing configuration."""

import itertools
import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T037-C01") != "T037-C01":
        raise ValueError("unknown T037 configuration")
    directions = []
    for i, j in itertools.combinations(range(5), 2):
        for a in (-1, 1):
            for b in (-1, 1):
                v = [0] * 5
                v[i], v[j] = a, b
                directions.append(v)
    return {"directions": directions}
