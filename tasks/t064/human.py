"""Rebuild an orthogonal coordinate-grid triangulation from the public input."""
import os

from tasks.t064.grid_method import build_grid


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T064-C01") != "T064-C01":
        raise ValueError("unsupported T064 configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return build_grid(0)
