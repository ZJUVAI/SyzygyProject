"""Generic seeded center mutations; no human or reference data is read."""
import os
import random
import time

from tasks.t085.check import PARAMETERS, validate


CONFIG = {"id": "T085-C01", "parameters": PARAMETERS}


def _seed():
    return {"radius": "1", "centers": [["0", "0"] for _ in range(21)]}


def search(iterations, *, evolutionary=False):
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    best = _seed()
    tested = valid = improved = accepted = 0
    larger_radius_trials = 0
    cutoff = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None if cutoff is None else time.monotonic() + max(0.0, float(cutoff))
    for step in range(iterations):
        if deadline is not None and time.monotonic() >= deadline:
            break
        candidate = {"radius": best["radius"], "centers": [list(c) for c in best["centers"]]}
        count = 2 if evolutionary and step % 4 == 0 else 1
        for idx in rng.sample(range(21), count):
            candidate["centers"][idx] = [str(rng.randrange(-4, 5)), str(rng.randrange(-4, 5))]
        # Alternate feasible-layout mutations with a concrete radius expansion
        # trial. A failed trial never replaces the saved incumbent.
        if step % 2 == 0:
            candidate["radius"] = "3/2"
            larger_radius_trials += 1
        tested += 1
        try:
            validate(candidate, CONFIG)
            valid += 1
            from fractions import Fraction
            candidate_radius = Fraction(candidate["radius"])
            best_radius = Fraction(best["radius"])
            if candidate_radius > best_radius:
                best = candidate
                improved += 1
            elif candidate_radius == best_radius:
                best = candidate
                accepted += 1
        except ValueError:
            pass
    best["search_metadata"] = {
        "algorithm": "seeded generic integer-center mutation with exact coverage checks",
        "fixed_iterations": iterations,
        "candidate_count": tested,
        "valid_candidate_count": valid,
        "improvement_count": improved,
        "accepted_neutral_move_count": accepted,
        "larger_radius_trials": larger_radius_trials,
        "seed": seed,
        "comparison_data_read": False,
        "starting_radius": 1,
    }
    return best
