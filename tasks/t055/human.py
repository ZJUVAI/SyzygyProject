"""Traditional DPLL hard-SAT construction, followed by legal soft hill-climbs."""

import os
from collections import defaultdict

from tasks.t055.check import PARAMETERS, validate
from tasks.t055.maxsat import HARD, SOFT, hard_sat_assignment, score_assignment


def _soft_hill_climb(assignment, max_steps=128):
    current = assignment[:]
    initial = score_assignment(current, HARD, SOFT)
    current_score = initial["soft_satisfied_weight"]
    hard_counts = [sum(1 for lit in clause if (current[abs(lit) - 1] == (lit > 0))) for clause in HARD]
    hard_occurrences = defaultdict(list)
    for clause_index, clause in enumerate(HARD):
        for literal in clause:
            hard_occurrences[abs(literal) - 1].append((clause_index, literal))
    soft_occurrences = defaultdict(list)
    for weight, clause in SOFT:
        if len(clause) == 1:
            literal = clause[0]
            soft_occurrences[abs(literal) - 1].append((weight, literal))
    accepted = 0
    for _ in range(max_steps):
        best_variable = None
        best_gain = 0
        for variable, clauses in soft_occurrences.items():
            old_value = current[variable]
            gain = sum(
                weight * (int((not old_value) == (literal > 0)) - int(old_value == (literal > 0)))
                for weight, literal in clauses
            )
            if gain <= best_gain:
                continue
            feasible = True
            for clause_index, literal in hard_occurrences[variable]:
                old_true = int(old_value == (literal > 0))
                new_true = 1 - old_true
                if hard_counts[clause_index] - old_true + new_true == 0:
                    feasible = False
                    break
            if feasible:
                best_variable, best_gain = variable, gain
        if best_variable is None:
            break
        variable = best_variable
        old_value = current[variable]
        for clause_index, literal in hard_occurrences[variable]:
            hard_counts[clause_index] += 1 if old_value != (literal > 0) else -1
        current[variable] = not old_value
        current_score += best_gain
        accepted += 1
    assert all(count > 0 for count in hard_counts)
    return current, accepted


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T055-C01") != "T055-C01":
        raise ValueError("unsupported configuration")
    assignment = hard_sat_assignment(HARD)
    assignment, steps = _soft_hill_climb(assignment)
    result = {"assignment": assignment}
    validate(result, {"parameters": PARAMETERS}, strict=True)
    result["search_metadata"] = {
        "algorithm": "SymPy DPLL hard-SAT construction plus exact feasible single-variable soft hill climb",
        "soft_improving_flips": steps,
        "objective_recomputed": score_assignment(assignment, HARD, SOFT)["soft_satisfied_weight"],
    }
    return result


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
