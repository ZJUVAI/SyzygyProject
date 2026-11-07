"""Rebuild the classical D4 24-cell spherical 5-design."""

import os

from tasks.t073.construction import d4_24cell_points, serialize_rational_points


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T073-C01")
    if chosen != "T073-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return serialize_rational_points(d4_24cell_points())
