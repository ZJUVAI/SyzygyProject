"""Rebuild a classic Clarke-Wright savings construction from public input."""

import os

from tasks.t097.heuristics import clarke_wright


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T097-C01")
    if chosen != "T097-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    routes, meta = clarke_wright()
    return {"routes": routes, "construction": {"method": "parallel Clarke-Wright savings", **meta}}
