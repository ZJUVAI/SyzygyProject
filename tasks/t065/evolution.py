"""Seeded mutation search over rectangular triangular-lattice patches."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t065.construction import grid_edge_count, rectangular_grid


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T065-C01") != "T065-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    requested = max(1, min(500, int(os.environ.get("MATHBENCH_EVOLUTION_ITERATIONS", "60"))))
    restarts = max(1, min(20, int(os.environ.get("MATHBENCH_RESTARTS", "4"))))
    rng = random.Random(seed ^ 0x029A)
    shapes = [(columns, 100 // columns)
              for columns in range(1, 101) if 100 % columns == 0]
    start = time.monotonic()
    best = (1, 100)
    total_steps = 0
    restart_steps = []
    step_stream = iter(search_steps(requested * restarts))
    for _restart in range(restarts):
        current = rng.choice(shapes)
        actual = 0
        for _ in range(requested):
            try:
                next(step_stream)
            except StopIteration:
                break
            proposal = rng.choice(shapes)
            if grid_edge_count(*proposal) > grid_edge_count(*current):
                current = proposal
            if grid_edge_count(*current) > grid_edge_count(*best):
                best = current
            actual += 1
            total_steps += 1
        restart_steps.append(actual)
    construction = rectangular_grid(*best)
    construction["search_metadata"] = {
        "algorithm": "seeded mutation and elitist selection over factorized rectangular triangular-lattice patches",
        "seed": seed,
        "iterations_requested_per_restart": requested,
        "iterations_run": total_steps,
        "restarts": restarts,
        "restart_iterations": restart_steps,
        "best_shape": {"columns": best[0], "rows": best[1]},
        "best_family_edge_count": grid_edge_count(*best),
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
