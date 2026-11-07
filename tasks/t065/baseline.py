"""Exact finite search over rectangular patches of the triangular lattice."""

import os
import time

from mathbench.search import search_steps
from tasks.t065.construction import grid_edge_count, rectangular_grid


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T065-C01") != "T065-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    start = time.monotonic()
    factor_pairs = [(columns, 100 // columns)
                    for columns in range(1, 101) if 100 % columns == 0]
    best = (1, 100)
    checked = 0
    for step in search_steps(len(factor_pairs)):
        columns, rows = factor_pairs[step]
        if grid_edge_count(columns, rows) > grid_edge_count(*best):
            best = (columns, rows)
        checked += 1
    construction = rectangular_grid(*best)
    construction["search_metadata"] = {
        "algorithm": "exhaustive factor-pair scan of 100-point rectangular triangular-lattice patches",
        "seed": seed,
        "iterations_requested": len(factor_pairs),
        "iterations_run": checked,
        "candidate_shapes_checked": checked,
        "best_shape": {"columns": best[0], "rows": best[1]},
        "family_edge_formula": "(columns-1)*rows + columns*(rows-1) + (columns-1)*(rows-1)",
        "generation_seconds": time.monotonic() - start,
        "budget": {
            "mode": "fixed iterations unless MATHBENCH_SEARCH_SECONDS is set",
            "runner_generation_limit_seconds": 300,
        },
    }
    return construction


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
