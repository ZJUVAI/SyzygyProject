"""Rebuild the weak published-factor baseline h_1(x)^73, h_1=x(1-x)."""


def run_code():
    import math
    import os

    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T046-C01")
    if config_id != "T046-C01":
        raise ValueError(f"unsupported configuration: {config_id}")

    coefficients = [0] * 147
    for j in range(74):
        coefficients[73 + j] = (-1) ** j * math.comb(73, j)
    return {"coefficients": coefficients}
