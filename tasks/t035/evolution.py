"""Search small cyclic covers of the symplectic generalized quadrangle."""
import itertools
import os
import random
import time

from check import validate


def _normalize(v):
    first = next(x for x in v if x)
    inv = pow(first, -1, 3)
    return tuple(x * inv % 3 for x in v)


def _base_graph():
    # Points and totally isotropic projective lines of W(3,3).
    points = sorted({_normalize(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    lines = set()
    for a, b in itertools.combinations(points, 2):
        if (a[0]*b[1] - a[1]*b[0] + a[2]*b[3] - a[3]*b[2]) % 3:
            continue
        line = set()
        for x, y in itertools.product(range(3), repeat=2):
            v = tuple((x*u + y*w) % 3 for u, w in zip(a, b))
            if any(v):
                line.add(_normalize(v))
        lines.add(tuple(sorted(line)))
    lines = sorted(lines)
    if len(points) != 40 or len(lines) != 40:
        raise RuntimeError('unexpected W(3,3) incidence structure')
    adj = [[] for _ in range(80)]
    for p, point in enumerate(points):
        for ell, line in enumerate(lines):
            if point in line:
                adj[p].append(40 + ell)
                adj[40 + ell].append(p)
    if any(len(row) != 4 for row in adj):
        raise RuntimeError('W(3,3) incidence graph is not 4-regular')
    edge_id = {}
    for p in range(40):
        for ell in adj[p]:
            edge_id[p, ell] = len(edge_id)
    cycles = []

    def walk(start, path):
        u = path[-1]
        if len(path) == 8:
            if start in adj[u] and path[1] < u:
                terms = []
                for i, v in enumerate(path):
                    w = path[(i + 1) % 8]
                    p, ell = (v, w) if v < 40 else (w, v)
                    terms.append((edge_id[p, ell], 1 if v < 40 else -1))
                cycles.append(terms)
            return
        for v in adj[u]:
            if v == start or v in path or v < start:
                continue
            walk(start, path + [v])

    for start in range(80):
        walk(start, [start])
    if len(cycles) != 1620:
        raise RuntimeError('unexpected number of base 8-cycles')
    return adj, cycles, len(edge_id)


def _search_modulus(modulus, cycles, edge_count, rng, deadline, stats):
    incidence = [[] for _ in range(edge_count)]
    for ci, cycle in enumerate(cycles):
        for edge, sign in cycle:
            incidence[edge].append((ci, sign))
    while time.monotonic() < deadline:
        voltage = [rng.randrange(modulus) for _ in range(edge_count)]
        sums = [sum(voltage[e] * s for e, s in c) % modulus for c in cycles]
        bad = {i for i, value in enumerate(sums) if value == 0}
        # Min-conflicts on the 8-cycle constraints. Random restarts avoid
        # keeping a locally optimal voltage assignment.
        steps = 6000
        for step in range(steps):
            stats['iterations'] += 1
            if step % 16 == 0 and time.monotonic() >= deadline:
                return None
            if not bad:
                return voltage
            ci = rng.choice(tuple(bad))
            edge, _ = rng.choice(cycles[ci])
            related = incidence[edge]
            old = voltage[edge]
            best_values = []
            best_cost = len(bad)
            for value in range(modulus):
                if value == old:
                    continue
                cost = len(bad)
                for cj, sign in related:
                    before = sums[cj] == 0
                    after = (sums[cj] + sign * (value - old)) % modulus == 0
                    cost += int(after) - int(before)
                if cost < best_cost:
                    best_cost, best_values = cost, [value]
                elif cost == best_cost:
                    best_values.append(value)
            if best_values:
                value = rng.choice(best_values)
            else:
                value = rng.randrange(modulus)
            delta = value - old
            voltage[edge] = value
            for cj, sign in related:
                sums[cj] = (sums[cj] + sign * delta) % modulus
                if sums[cj]:
                    bad.discard(cj)
                else:
                    bad.add(cj)
    return None


def _lift(base_adj, voltage, modulus):
    n = len(base_adj) * modulus
    edges = []
    for p in range(40):
        for index, ell in enumerate(base_adj[p]):
            # Each point has four incident edges; this ordering matches the
            # edge IDs assigned in _base_graph.
            edge = p * 4 + index
            shift = voltage[edge]
            for k in range(modulus):
                u = p * modulus + k
                v = ell * modulus + (k + shift) % modulus
                edges.append([u, v])
    return {'vertices': n, 'edges': edges}


def run_code():
    if os.environ.get('MATHBENCH_CONFIG_ID', 'T035-C01') != 'T035-C01':
        raise ValueError('unsupported configuration')
    try:
        budget = max(0.1, min(45.0, float(os.environ.get('MATHBENCH_EVOLUTION_SECONDS', '45'))))
    except ValueError:
        budget = 45.0
    started = time.monotonic()
    deadline = started + budget
    rng = random.Random(int(os.environ.get('MATHBENCH_SEED', '0')))
    base_adj, cycles, edge_count = _base_graph()
    preprocessing_seconds = time.monotonic() - started
    best = None
    stats = {'iterations': 0, 'moduli_succeeded': []}
    # Start with the largest practical prime: more voltage values make the
    # cycle constraints easier. Descend only after finding and certifying a lift.
    moduli = (37, 31, 29, 23, 19, 17, 13, 11, 7)
    slice_seconds = budget / len(moduli)
    for modulus in moduli:
        if time.monotonic() >= deadline:
            break
        modulus_deadline = min(deadline, time.monotonic() + slice_seconds)
        voltage = _search_modulus(modulus, cycles, edge_count, rng, modulus_deadline, stats)
        if voltage is None:
            continue
        candidate = _lift(base_adj, voltage, modulus)
        try:
            validate(candidate, {'parameters': {'degree': 4, 'girth': 10}})
        except (ValueError, RuntimeError):
            continue
        best = candidate
        stats['moduli_succeeded'].append(modulus)
    if best is not None:
        best['_evolution'] = {
            'iterations': stats['iterations'],
            'moduli_succeeded': stats['moduli_succeeded'],
            'preprocessing_seconds': preprocessing_seconds,
        }
        return best
    # The established independently checked algebraic seed remains a fallback.
    from lps import build_graph
    return build_graph((0, 2))
