"""Deterministic evolutionary search for unequal circle packings.

The search evolves center coordinates on a fixed rational grid. A conservative
integer-square-root repair produces a feasible rational construction before
any candidate can become the incumbent.
"""
import os
import random
from fractions import Fraction
from math import isqrt

_D = 1_000_000_000
_RESTART_AFTER = 100


def _accept(current, proposed, temperature, rng):
    """Metropolis acceptance for a chain; the global incumbent is separate."""
    if proposed >= current:
        return True
    if temperature <= 0:
        return False
    return rng.random() < __import__("math").exp((proposed - current) / temperature)


def _count():
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T005-C01")
    if config == "T005-C01":
        return 26
    if config == "T005-C02":
        return 32
    raise ValueError("unsupported MATHBENCH_CONFIG_ID")


def _repair(points, proposed_radii=None):
    """Return exact feasible radii for integer-grid centers, or None."""
    n = len(points)
    # Keep centers away from the walls so every radius remains positive.
    margin = 10
    radii = ([max(1, int(r)) for r in proposed_radii] if proposed_radii is not None else
             [min(_D // 12, x - margin, y - margin, _D - margin - x, _D - margin - y)
              for x, y in points])
    if min(radii) <= 0:
        return None
    # One uniform rational scale preserves proposed proportions. Integer
    # square roots round pair distances down, so repaired constraints are safe.
    from fractions import Fraction
    scale = Fraction(1)
    for i in range(n):
        xi, yi = points[i]
        wall = min(xi - margin, yi - margin, _D - margin - xi, _D - margin - yi)
        if radii[i] > 0:
            scale = min(scale, Fraction(wall, radii[i]))
        for j in range(i):
            xj, yj = points[j]
            distance = isqrt((xi - xj) ** 2 + (yi - yj) ** 2)
            total = radii[i] + radii[j]
            if total > 0:
                scale = min(scale, Fraction(distance, total))
    radii = [(r * scale.numerator) // scale.denominator for r in radii]
    if min(radii) <= 0:
        return None
    circles = [{"x": f"{x}/{_D}", "y": f"{y}/{_D}", "r": f"{r}/{_D}"}
               for (x, y), r in zip(points, radii)]
    return circles, Fraction(sum(radii), _D)


def _initial(n, rng):
    # Alternate 5- and 6-column grids to vary contact topology without witnesses.
    columns = rng.choice((5, 6))
    rows = (n + columns - 1) // columns
    sites = [((2 * c + 1) * _D // (2 * columns),
              (2 * r + 1) * _D // (2 * rows))
             for r in range(rows) for c in range(columns)]
    rng.shuffle(sites)
    return sites[:n]


def _polish(points, radii):
    """One bounded SLSQP solve with analytic wall and pair derivatives."""
    import numpy as np
    from scipy.optimize import minimize
    n = len(points)
    z0 = np.array([v / _D for pair in points for v in pair] +
                  [r / _D for r in radii], dtype=float)
    pairs = [(i, j) for i in range(n) for j in range(i)]

    def constraints(z):
        xy = z[:2*n].reshape(n, 2)
        rr = z[2*n:]
        walls = np.concatenate((xy[:, 0] - rr, 1 - xy[:, 0] - rr,
                                xy[:, 1] - rr, 1 - xy[:, 1] - rr))
        delta = xy[[i for i, _ in pairs]] - xy[[j for _, j in pairs]]
        return np.concatenate((walls, np.einsum("ij,ij->i", delta, delta) -
                               (rr[[i for i, _ in pairs]] + rr[[j for _, j in pairs]])**2))

    def jacobian(z):
        xy = z[:2*n].reshape(n, 2)
        rr = z[2*n:]
        jac = np.zeros((4*n + len(pairs), 3*n))
        for i in range(n):
            jac[i, 2*i] = 1; jac[i, 2*n+i] = -1
            jac[n+i, 2*i] = -1; jac[n+i, 2*n+i] = -1
            jac[2*n+i, 2*i+1] = 1; jac[2*n+i, 2*n+i] = -1
            jac[3*n+i, 2*i+1] = -1; jac[3*n+i, 2*n+i] = -1
        for k, (i, j) in enumerate(pairs, 4*n):
            dx, dy = xy[i] - xy[j]
            jac[k, 2*i:2*i+2] = (2*dx, 2*dy)
            jac[k, 2*j:2*j+2] = (-2*dx, -2*dy)
            jac[k, 2*n+i] = jac[k, 2*n+j] = -2*(rr[i]+rr[j])
        return jac

    def objective(z):
        return -float(np.sum(z[2*n:]))

    def objective_jac(z):
        out = np.zeros(3*n)
        out[2*n:] = -1
        return out

    result = minimize(objective, z0, jac=objective_jac, method="SLSQP",
                      bounds=[(1e-5, 1-1e-5)]*(2*n) + [(1e-8, .5)]*n,
                      constraints={"type": "ineq", "fun": constraints, "jac": jacobian},
                      options={"maxiter": 20, "ftol": 1e-8, "disp": False})
    candidate = result.x
    p = [(max(1, min(_D-1, int(round(candidate[2*i] * _D)))),
          max(1, min(_D-1, int(round(candidate[2*i+1] * _D))))) for i in range(n)]
    rs = [max(1, int(candidate[2*n+i] * _D)) for i in range(n)]
    return p, rs


def run_code():
    n = _count()
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    generations = max(1, min(2000, int(os.environ.get("MATHBENCH_EVOLUTION_GENERATIONS", "12"))))
    population_size = max(4, min(48, int(os.environ.get("MATHBENCH_EVOLUTION_POPULATION", "6"))))
    # Keep the canonical grid as an independent exact incumbent.
    seed_points = [((2 * c + 1) * _D // 12, (2 * r + 1) * _D // 12)
                   for r in range(6) for c in range(6)][:n]
    seed_circles = [{"x": f"{2*c+1}/12", "y": f"{2*r+1}/12", "r": "1/12"}
                    for r in range(6) for c in range(6)][:n]
    best = (Fraction(n, 12), seed_points, seed_circles)
    chains = [best]
    for _ in range(population_size - 1):
        points = _initial(n, rng)
        repaired = _repair(points)
        chains.append((repaired[1], points, repaired[0]) if repaired else best)
    history = [{"generation": 0, "objective": str(best[0]), "stagnation": 0,
                "temperature": "0.01", "mutation_scale": str(_D // 10),
                "restarts": 0, "downhill_accepts": 0}]
    evaluations = population_size
    generations_run = 0
    stagnant = 0
    restarts = 0
    restart_evaluations = 0
    downhill_accepts = 0
    solver_calls = 0
    mutation_scale = _D // 20
    for generation in range(generations):
        generations_run = generation + 1
        improved = False
        polished_improved = False
        for chain_index in range(population_size):
            current_score, parent, parent_circles = chains[chain_index]
            child = list(parent)
            scale = max(_D // 100_000, mutation_scale)
            # Larger collective moves keep chains mobile between contact basins.
            pure_polish = ((generation // population_size + generation % population_size) % 4 == 3
                           and chain_index == generation % population_size)
            mutation_count = 0 if pure_polish else 1 + rng.randrange(max(1, n // 8))
            for _mutation in range(mutation_count):
                idx = rng.randrange(n)
                x, y = child[idx]
                child[idx] = (max(1, min(_D - 1, x + rng.randint(-scale, scale))),
                              max(1, min(_D - 1, y + rng.randint(-scale, scale))))
            parent_radii = [int(Fraction(circle["r"]) * _D) for circle in parent_circles]
            proposal_radii = parent_radii
            was_polished = chain_index == generation % population_size
            if was_polished:
                child, proposal_radii = _polish(child, parent_radii)
                solver_calls += 1
            repaired = _repair(child, proposal_radii)
            evaluations += 1
            if repaired:
                proposal = (repaired[1], child, repaired[0])
                # Cooling is slow; occasional downhill transitions escape local basins.
                temperature = max(0.00015, 0.01 * (0.997 ** generation))
                if _accept(current_score, proposal[0], temperature, rng):
                    if proposal[0] < current_score:
                        downhill_accepts += 1
                    chains[chain_index] = proposal
                if proposal[0] > best[0]:
                    best = proposal
                    improved = True
                    polished_improved = polished_improved or was_polished
        stagnant = 0 if polished_improved else stagnant + 1
        if stagnant >= _RESTART_AFTER:
            # Restart the weakest chain from a fresh shuffled grid, never a witness.
            weakest = min(range(population_size), key=lambda i: chains[i][0])
            points = _initial(n, rng)
            repaired = _repair(points)
            restart_evaluations += 1
            evaluations += 1
            if repaired:
                chains[weakest] = (repaired[1], points, repaired[0])
            restarts += 1
            stagnant = 0
        # Broaden moves after stagnation and gradually recover after progress.
        if improved:
            mutation_scale = max(_D // 500, mutation_scale * 9 // 10)
        else:
            mutation_scale = min(_D * 2 // 25, mutation_scale * 11 // 10)
        history.append({"generation": generation + 1, "objective": str(best[0]),
                        "stagnation": stagnant, "temperature": f"{max(0.00015, 0.01 * (0.997 ** generation)):.9g}",
                        "mutation_scale": str(mutation_scale), "restarts": restarts,
                        "downhill_accepts": downhill_accepts})
    return {"circles": best[2], "search": {
        "algorithm": "persistent multi-chain basin hopping with adaptive mutations and exact rational repair",
        "algorithm_version": 2,
        "seed": int(os.environ.get("MATHBENCH_SEED", "0")),
        "generations": generations_run,
        "population_size": population_size,
        "evaluations": evaluations,
        "candidate_slots_per_generation": population_size,
        "solver_calls": solver_calls,
        "optimizer": "SLSQP, analytic Jacobian, maxiter=20, rotating one chain per generation",
        "restart_interval": _RESTART_AFTER,
        "restarts": restarts,
        "restart_evaluations": restart_evaluations,
        "downhill_accepts": downhill_accepts,
        "final_mutation_scale": str(mutation_scale),
        "coordinate_denominator": _D,
        "history": history,
    }}


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
