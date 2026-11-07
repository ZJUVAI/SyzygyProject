"""Discretize the modified-arcsine profile described by Barnard–Steinerberger."""

import math
import os


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T087-C01")
    if config_id != "T087-C01":
        raise ValueError(f"unknown T087 configuration: {config_id}")
    d = 13 / 4800
    radius = 0.5 + 0.025
    scale = 100000
    heights = []
    for i in range(480):
        x = (i + 0.5) * d - 0.65
        value = 0.0
        if abs(x) < radius:
            value = 1.0 / math.sqrt(1.0 - (x / radius) ** 2)
        if abs(x) < 0.25:
            value -= 0.25 / math.sqrt(1.0 - 4.0 * x * x)
        numerator = int(round(value * scale))
        if numerator < 0:
            raise ArithmeticError("rounded modified-arcsine profile became negative")
        heights.append(f"{numerator}/{scale}")
    return {"heights": heights}
