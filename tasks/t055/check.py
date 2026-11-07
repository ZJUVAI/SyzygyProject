"""Exact checker for the pinned partial MaxSAT instance T055-C01."""

from tasks.t055.maxsat import HARD_COUNT, NVAR, SOFT_COUNT, load_formula, score_assignment

HARD, SOFT = load_formula()
SOFT_TOTAL_WEIGHT = sum(weight for weight, _ in SOFT)
PARAMETERS = {
    "instance": "b4794d123e18a908924d3d33cdeeae3b",
    "family": "inconsistency-measurement",
    "variables": NVAR,
    "hard_clauses": HARD_COUNT,
    "soft_clauses": SOFT_COUNT,
    "soft_total_weight": SOFT_TOTAL_WEIGHT,
    "objective": "max_satisfied_soft_weight",
}


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("parameters") != PARAMETERS:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict) or "assignment" not in solution:
        raise ValueError("solution must contain assignment")
    assignment = solution["assignment"]
    if not isinstance(assignment, (list, tuple)) or len(assignment) != NVAR:
        raise ValueError("assignment must contain exactly 1630 Boolean values")
    if any(type(value) is not bool for value in assignment):
        raise ValueError("assignment values must be booleans")

    result = score_assignment(assignment, HARD, SOFT)
    if result["hard_satisfied"] != HARD_COUNT:
        raise ValueError(
            f"assignment violates {HARD_COUNT - result['hard_satisfied']} hard clauses"
        )
    return {
        "objective": result["soft_satisfied_weight"],
        "verification_status": "exact",
        "details": {
            "variables_checked": NVAR,
            "hard_clauses_satisfied": result["hard_satisfied"],
            "hard_clauses_total": HARD_COUNT,
            "soft_clauses_satisfied_weight": result["soft_satisfied_weight"],
            "soft_unsatisfied_weight": result["soft_cost"],
            "soft_total_weight": result["soft_total_weight"],
            "claimed_objective_ignored": True,
        },
    }
