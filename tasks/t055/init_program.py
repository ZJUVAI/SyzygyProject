"""Build a hard-satisfying seed with SymPy's classic DPLL implementation.

This entry is self-contained: it reads only the public WCNF input, not task
modules or comparison witnesses.
"""

import os
from pathlib import Path


INSTANCE = Path(__file__).parent / "data" / "source" / "b4794d123e18a908924d3d33cdeeae3b.wcnf"
VARIABLES = 1630


def _hard_clauses():
    clauses = []
    for raw_line in INSTANCE.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("c") or line.startswith("%"):
            continue
        fields = line.split()
        if fields[0] == "h":
            clauses.append([int(literal) for literal in fields[1:-1]])
    if len(clauses) != 6150:
        raise ValueError("unexpected hard-clause count")
    return clauses


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T055-C01") != "T055-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    from sympy.logic.algorithms.dpll2 import SATSolver

    clauses = _hard_clauses()
    model = next(SATSolver(clauses, set(range(1, VARIABLES + 1)), set(), heuristic="vsids")._find_model())
    assignment = [bool(model[index]) for index in range(1, VARIABLES + 1)]
    # EVOLVE-BLOCK-END
    return {"assignment": assignment}


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
