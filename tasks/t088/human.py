"""Reconstruction of a published GRASP-style cutwidth heuristic."""

import os

from tasks.t088.heuristics import randomized_method
from tasks.t088.instance import load_graph


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T088-C01")
    if chosen != "T088-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    order, metadata = randomized_method(
        load_graph(), seed=seed, trials=3, vertex_trials=8, alpha=0.20
    )
    metadata["provenance"] = (
        "Local reconstruction of the GRASP construction and insertion-local-search "
        "method family described by Marti et al.; this output is not claimed to "
        "reproduce their reported arc130 ordering."
    )
    return {"ordering": order, "search_metadata": metadata}
