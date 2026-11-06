"""Exact checker for integer Golomb rulers."""
from itertools import combinations


def validate(solution, config, strict=False):
    parameters = config.get("parameters", {}) if isinstance(config, dict) else {}
    marks_required = parameters.get("marks")
    if isinstance(marks_required, bool) or not isinstance(marks_required, int) or marks_required < 2:
        raise ValueError("configuration must specify an integer marks count >= 2")
    marks = solution.get("marks") if isinstance(solution, dict) else solution
    if not isinstance(marks, (list, tuple)) or len(marks) != marks_required:
        raise ValueError(f"solution must contain exactly {marks_required} marks")
    if any(isinstance(x, bool) or not isinstance(x, int) for x in marks):
        raise ValueError("marks must be integers")
    if len(set(marks)) != marks_required:
        raise ValueError("marks must be distinct")
    ordered = sorted(marks)
    differences = [b - a for a, b in combinations(ordered, 2)]
    difference_count = marks_required * (marks_required - 1) // 2
    if len(set(differences)) != difference_count:
        raise ValueError(f"all {difference_count} positive pairwise differences must be unique")
    return {"objective": max(ordered) - min(ordered),
            "verification_status": "exact",
            "details": {"marks": marks_required, "differences_checked": difference_count}}
