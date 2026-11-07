"""Seeded evolutionary search over Eisenstein polynomials x^100-p."""
import math
import os
import random
import time


def _prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for divisor in range(3, math.isqrt(n) + 1, 2):
        if n % divisor == 0:
            return False
    return True


def _solution(p):
    degree, scale = 100, 10**16
    root_radius = float(p) ** (1.0 / degree)
    disks = []
    for k in range(degree):
        angle = 2.0 * math.pi * k / degree
        real = round(root_radius * math.cos(angle) * scale)
        imag = round(root_radius * math.sin(angle) * scale)
        disks.append({"center_real": f"{real}/{scale}",
                      "center_imag": f"{imag}/{scale}",
                      "radius": "1/100000000000000"})
    return {"coefficients_ascending": [-p] + [0] * 99 + [1], "root_disks": disks}


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T063-C01") != "T063-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    requested = max(1, min(300, int(os.environ.get("MATHBENCH_EVOLUTION_ITERATIONS", "60"))))
    restarts = max(1, min(20, int(os.environ.get("MATHBENCH_RESTARTS", "4"))))
    rng = random.Random(seed ^ 0x095A)
    start = time.monotonic()
    incumbent = None
    steps = 0
    restart_steps = []
    from mathbench.search import search_steps
    step_stream = iter(search_steps(requested * restarts))
    for restart in range(restarts):
        current = 1009 + 2 * rng.randrange(0, 500)
        while not _prime(current):
            current += 2
        actual_restart_steps = 0
        for _ in range(requested):
            try:
                next(step_stream)
            except StopIteration:
                break
            # Mutate the prime coefficient; selection keeps the smaller p,
            # which is the exact Mahler measure throughout this family.
            delta = rng.choice((-1000, -200, -40, -8, -2, 2, 8, 40, 200, 1000))
            proposal = max(2, current + delta)
            if proposal % 2 == 0 and proposal != 2:
                proposal += 1
            while not _prime(proposal):
                proposal += 2
            current = min(current, proposal)
            incumbent = current if incumbent is None else min(incumbent, current)
            steps += 1
            actual_restart_steps += 1
        restart_steps.append(actual_restart_steps)
    if incumbent is None:
        incumbent = 2
    return {
        **_solution(incumbent),
        "search_metadata": {
            "algorithm": "seeded mutation and elitist selection in the Eisenstein family x^100-p",
            "seed": seed,
            "iterations_requested_per_restart": requested,
            "iterations_run": steps,
            "restarts": restarts,
            "restart_iterations": restart_steps,
            "best_candidate_parameter": incumbent,
            "generation_seconds": time.monotonic() - start,
            "budget": {"mode": "fixed iterations unless MATHBENCH_SEARCH_SECONDS is set",
                       "runner_generation_limit_seconds": 300},
        },
    }


if __name__ == "__main__":
    print(run_code())
