"""Deterministic valid rational starting program for the selected configuration."""
import os

CONFIG_N = {"T005-C01": 11, "T005-C02": 12, "T005-C03": 16}

def run_code():
    n = CONFIG_N.get(os.environ.get("MATHBENCH_CONFIG_ID", "T005-C01"), 11)
    return {"points": [[f"{i}/{n-1}", f"{i*i}/{(n-1)**2}"] for i in range(n)]}
