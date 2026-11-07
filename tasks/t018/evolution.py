"""Warm-started multistart determinant search for T018 (n=29)."""

import json
import os
import random
import time

import numpy as np

from tasks.t018.check import validate


def _det_inverse(matrix):
    sign, logabs = np.linalg.slogdet(matrix)
    if sign == 0:
        return 0.0, None
    return float(sign * np.exp(logabs)), np.linalg.inv(matrix)


def _exact_score(matrix):
    n = int(np.asarray(matrix).shape[0])
    return validate({"matrix": np.asarray(matrix, dtype=int).tolist()}, {"n": n})["objective"]


def _gf27_hadamard():
    """Construct a 28-order Hadamard matrix from GF(27) characters."""
    def coeffs(value):
        return [(value // (3**i)) % 3 for i in range(3)]

    def add(a, b):
        return sum(((x + y) % 3) * (3**i) for i, (x, y) in enumerate(zip(coeffs(a), coeffs(b))))

    def sub(a, b):
        return sum(((x - y) % 3) * (3**i) for i, (x, y) in enumerate(zip(coeffs(a), coeffs(b))))

    def mul(a, b):
        left, right = coeffs(a), coeffs(b)
        product = [0] * 5
        for i in range(3):
            for j in range(3):
                product[i + j] = (product[i + j] + left[i] * right[j]) % 3
        # x^3 + 2x + 1 = 0, so x^3 = x + 2.
        for degree in (4, 3):
            c = product[degree]
            product[degree] = 0
            product[degree - 2] = (product[degree - 2] + c) % 3
            product[degree - 3] = (product[degree - 3] + 2 * c) % 3
        return sum(product[i] * (3**i) for i in range(3))

    def power(value, exponent):
        result = 1
        while exponent:
            if exponent & 1:
                result = mul(result, value)
            value = mul(value, value)
            exponent //= 2
        return result

    character = [0] + [1 if power(a, 13) == 1 else -1 for a in range(1, 27)]
    q = np.asarray([[character[sub(i, j)] for j in range(27)] for i in range(27)], dtype=np.int8)
    h = np.ones((28, 28), dtype=np.int8)
    h[1:, 1:] = q - np.eye(27, dtype=np.int8)
    return h


def _paley_extension(rng, hadamard, restarts=96):
    """Find a strong bordered 29-order seed by maximizing ||H.T u||_1."""
    best_matrix = None
    best_value = -1
    for _ in range(restarts):
        u = np.asarray([rng.choice((-1, 1)) for _ in range(28)], dtype=np.int8)
        values = hadamard.T @ u
        score = int(np.abs(values).sum())
        while True:
            best_flip, best_flip_score = -1, score
            for i in range(28):
                flipped = values - 2 * int(u[i]) * hadamard[i, :]
                candidate_score = int(np.abs(flipped).sum())
                if candidate_score > best_flip_score:
                    best_flip, best_flip_score = i, candidate_score
            if best_flip < 0:
                break
            values -= 2 * int(u[best_flip]) * hadamard[best_flip, :]
            u[best_flip] *= -1
            score = best_flip_score
        if score > best_value:
            # With a=1 and v=-sign(H.T u), the Schur complement gives
            # |det| = 28^13 * (28 + ||H.T u||_1).
            v = np.where(values >= 0, -1, 1).astype(np.int8)
            matrix = np.ones((29, 29), dtype=np.int8)
            matrix[:28, :28] = hadamard
            matrix[:28, 28] = u
            matrix[28, :28] = v
            matrix[28, 28] = 1
            best_matrix, best_value = matrix, score
    return best_matrix, best_value


def _two_row_move(matrix, inverse, rng, trials=64):
    """Enumerate the planar projection vertices for each sampled row pair.

    A convex absolute bilinear objective reaches a maximum on a vertex of
    the projected sign cube. The sign changes occur at the cofactor angles.
    """
    best_ratio, best = 1.0, None
    for _ in range(trials):
        i, k = rng.sample(range(matrix.shape[0]), 2)
        p, q = inverse[:, i], inverse[:, k]
        angles = np.sort(np.mod(np.arctan2(q, p)+np.pi/2, np.pi))
        end = np.r_[angles[1:], angles[0]+np.pi]
        mid = (angles+end)/2
        x = np.where(np.cos(mid[:,None])*p+np.sin(mid[:,None])*q >= 0, 1, -1).astype(np.int8)
        weights = (x@p)[:,None]*q-(x@q)[:,None]*p
        ratios = np.abs(weights).sum(axis=1)
        j = int(np.argmax(ratios))
        if ratios[j]>best_ratio+1e-9:
            best_ratio = float(ratios[j])
            y = np.where(weights[j]>=0, 1, -1).astype(np.int8)
            best = (i,k,x[j].copy(),y)
    return best


def _improve(matrix, deadline, rng):
    """Single-entry ascent followed by simultaneous two-row optimization."""
    matrix = np.asarray(matrix, dtype=np.int8).copy()
    det, inverse = _det_inverse(matrix.astype(float))
    if inverse is None:
        return None, 0.0
    steps = 0
    while time.monotonic() < deadline:
        gains = np.abs(1.0 - 2.0 * matrix * inverse.T)
        i, j = divmod(int(np.argmax(gains)), matrix.shape[0])
        if gains[i, j] > 1.0 + 1e-9:
            matrix[i, j] *= -1
        else:
            move = _two_row_move(matrix, inverse, rng)
            if move is None:
                break
            i, k, x, y = move
            matrix[i], matrix[k] = x, y
        det, inverse = _det_inverse(matrix.astype(float))
        if inverse is None:
            return None, 0.0
        steps += 1
    return matrix, abs(det)


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T018-C01")
    n = {"T018-C01": 29, "T018-C02": 27, "T018-C03": 31}.get(config_id, 29)
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    seconds = max(0.1, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    rng = random.Random(seed)
    deadline = time.monotonic() + seconds

    # The only optional start is the task's own saved incumbent, staged by the
    # search runner. Validate it with the task's exact checker before use.
    best = None
    best_exact = -1
    warm_start = os.environ.get("MATHBENCH_WARM_START")
    if warm_start:
        with open(warm_start, encoding="utf-8") as stream:
            candidate = json.load(stream)
        if isinstance(candidate, dict) and "matrix" in candidate:
            exact = validate(candidate, {"n": n})["objective"]
            best = np.asarray(candidate["matrix"], dtype=np.int8)
            best_exact = exact

    if best is None:
        best = np.asarray([[1 if i == j else -1 for j in range(n)] for i in range(n)], dtype=np.int8)
        best_exact = _exact_score(best)
    best_float = abs(_det_inverse(best.astype(float))[0])
    incumbent = best.copy()
    paley = None
    if n == 29:
        hadamard = _gf27_hadamard()
        paley, border_l1 = _paley_extension(rng, hadamard)
        paley_exact = _exact_score(paley)
        if paley_exact > best_exact:
            best, best_exact = paley.copy(), paley_exact
            best_float = abs(_det_inverse(best.astype(float))[0])
            incumbent = best.copy()
        elif border_l1 > 0 and warm_start is None:
            incumbent = paley.copy()
    restart = 0
    while time.monotonic() < deadline:
        restart += 1
        # Begin with a small basin perturbation; grow the kick after repeated
        # failures, while periodically testing independent random starts.
        if restart == 1:
            start = paley.copy() if paley is not None else incumbent.copy()
        elif restart % 6 == 0:
            start = np.asarray([[rng.choice((-1, 1)) for _ in range(n)] for _ in range(n)], dtype=np.int8)
        else:
            start = incumbent.copy()
            count = min(40, 2 + (restart % 6) * 2)
            for _ in range(count):
                i, j = rng.randrange(n), rng.randrange(n)
                start[i, j] = -start[i, j]

        candidate, approximate = _improve(start, min(deadline, time.monotonic() + 2.0), rng)
        if candidate is None or approximate <= best_float * (1.0 + 1e-12):
            continue
        exact = _exact_score(candidate)
        # Exact Bareiss scores decide every incumbent update. The float score
        # is only a proposal filter for the local search.
        if exact > best_exact:
            best = candidate.copy()
            incumbent = candidate.copy()
            best_exact = exact
            best_float = abs(_det_inverse(best.astype(float))[0])
        elif rng.random() < 0.15:
            incumbent = candidate.copy()

    # Final guard: return only the exact incumbent retained above.
    _exact_score(best)
    return {"matrix": best.astype(int).tolist(), "search_metadata": {"restarts": restart, "budget_seconds": seconds, "method": "single-entry ascent with exact planar two-row proposals"}}
