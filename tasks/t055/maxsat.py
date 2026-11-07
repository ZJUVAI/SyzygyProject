"""Parser and exact helpers for the fixed MaxSAT Evaluation WCNF instance."""

from pathlib import Path
import hashlib

NVAR = 1630
HARD_COUNT = 6150
SOFT_COUNT = 649
INSTANCE_NAME = "b4794d123e18a908924d3d33cdeeae3b.wcnf"
INSTANCE_SHA256 = "cd81f483b6cc3d05e9760274eee7697d9cc0f0a5a7146d3c6887af687d149195"


def instance_path():
    return Path(__file__).parent / "data" / "source" / INSTANCE_NAME


def load_formula(path=None):
    source_path = Path(path) if path else instance_path()
    if hashlib.sha256(source_path.read_bytes()).hexdigest() != INSTANCE_SHA256:
        raise ValueError("WCNF source hash does not match the pinned instance")
    hard = []
    soft = []
    for raw_line in source_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("c") or line.startswith("%"):
            continue
        fields = line.split()
        if fields[0] == "h":
            if fields[-1] != "0":
                raise ValueError("hard clause must end in 0")
            clause = tuple(int(value) for value in fields[1:-1])
            hard.append(clause)
        else:
            weight = int(fields[0])
            if fields[-1] != "0":
                raise ValueError("soft clause must end in 0")
            clause = tuple(int(value) for value in fields[1:-1])
            soft.append((weight, clause))
    if len(hard) != HARD_COUNT or len(soft) != SOFT_COUNT:
        raise ValueError("WCNF clause counts do not match the pinned benchmark")
    for clause in [*hard, *(clause for _, clause in soft)]:
        if not clause or any(lit == 0 or abs(lit) > NVAR for lit in clause):
            raise ValueError("WCNF clause has an invalid literal")
    if any(weight <= 0 for weight, _ in soft):
        raise ValueError("soft clause weights must be positive")
    return hard, soft


def literal_value(assignment, literal):
    value = assignment[abs(literal) - 1]
    return value if literal > 0 else not value


def clause_satisfied(assignment, clause):
    return any(literal_value(assignment, literal) for literal in clause)


def score_assignment(assignment, hard=None, soft=None):
    hard = hard if hard is not None else load_formula()[0]
    soft = soft if soft is not None else load_formula()[1]
    hard_satisfied = sum(clause_satisfied(assignment, clause) for clause in hard)
    soft_cost = sum(weight for weight, clause in soft if not clause_satisfied(assignment, clause))
    soft_total = sum(weight for weight, _ in soft)
    return {
        "hard_satisfied": hard_satisfied,
        "hard_total": len(hard),
        "soft_satisfied_weight": soft_total - soft_cost,
        "soft_cost": soft_cost,
        "soft_total_weight": soft_total,
    }


def hard_sat_assignment(hard=None):
    if hard is None:
        hard, _ = load_formula()
    from sympy.logic.algorithms.dpll2 import SATSolver

    model = next(SATSolver(hard, set(range(1, NVAR + 1)), set(), heuristic="vsids")._find_model())
    return [bool(model[index]) for index in range(1, NVAR + 1)]


def random_perturb(rng, assignment, flips):
    changed = assignment[:]
    positions = rng.sample(range(NVAR), min(flips, NVAR))
    for position in positions:
        changed[position] = not changed[position]
    return changed


HARD, SOFT = load_formula()
