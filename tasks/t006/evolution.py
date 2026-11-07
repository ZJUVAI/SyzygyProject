"""Search cyclic covers for C01 and return a valid LPS fallback for C02."""
import itertools
import json
import math
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


def _warm_voltage(path, base_adj, modulus):
    """Recover the task's own saved cyclic-cover voltages, if they fit."""
    if not path:
        return None
    try:
        with open(path, encoding='utf-8') as stream:
            solution = json.load(stream)
        old_modulus, remainder = divmod(solution['vertices'], len(base_adj))
        if remainder or old_modulus < 2 or len(solution['edges']) != 160 * old_modulus:
            return None
        config = {'parameters': {'degree': 4, 'girth': 10}}
        validate(solution, config)
        edge_index = {(p, ell): p * 4 + i
                      for p in range(40)
                      for i, ell in enumerate(base_adj[p])}
        voltage = [None] * 160
        point_limit = 40 * old_modulus
        for a, b in solution['edges']:
            if a < point_limit <= b:
                point, line = a, b
            elif b < point_limit <= a:
                point, line = b, a
            else:
                return None
            p, k = divmod(point, old_modulus)
            ell = line // old_modulus
            if not (0 <= p < 40 and 40 <= ell < 80):
                return None
            index = edge_index[p, ell]
            shift = (line % old_modulus - k) % old_modulus
            if voltage[index] is None:
                voltage[index] = shift
            elif voltage[index] != shift:
                return None
        if any(value is None for value in voltage):
            return None
        # A projection is only a starting assignment for another modulus.
        # At the source modulus it reproduces the validated cover exactly.
        return [value % modulus for value in voltage]
    except (OSError, ValueError, TypeError, KeyError, ZeroDivisionError):
        return None


def _search_modulus(modulus, cycles, edge_count, rng, deadline, stats, base_adj, initial=None):
    """Weighted min-conflicts with all eight edges of a violated cycle.

    Breakout weights give persistent constraints more influence. Tabu tenure
    stops immediate reversal; aspiration permits a new unweighted best.
    """
    import numpy as np
    edges = np.asarray([[e for e, sign in c] for c in cycles], dtype=np.int32)
    signs = np.asarray([[sign for e, sign in c] for c in cycles], dtype=np.int32)
    incidence = [[] for _ in range(edge_count)]
    for ci, cycle in enumerate(cycles):
        for edge, sign in cycle:
            incidence[edge].append((ci, sign))
    related = [(np.asarray([x for x, _ in row], dtype=np.int32),
                np.asarray([y for _, y in row], dtype=np.int32)) for row in incidence]
    best_bad, best = len(cycles) + 1, None
    pending = initial
    while time.monotonic() < deadline:
        voltage = (pending[:] if pending is not None else
                   [rng.randrange(modulus) for _ in range(edge_count)])
        pending = None
        sums = (np.asarray(voltage)[edges] * signs).sum(axis=1) % modulus
        penalties = np.ones(len(cycles), dtype=np.int32)
        tabu = np.zeros((edge_count, modulus), dtype=np.int64)
        plateau = 0
        for step in range(14000):
            if time.monotonic() >= deadline:
                return None
            bad = np.flatnonzero(sums == 0)
            if not len(bad):
                candidate = _lift(base_adj, voltage, modulus)
                try:
                    validate(candidate, {'parameters': {'degree': 4, 'girth': 10}})
                except (ValueError, RuntimeError):
                    break
                return voltage
            if len(bad) < best_bad:
                best_bad, best = len(bad), voltage[:]
                plateau = 0
            else:
                plateau += 1
            ci = int(bad[rng.randrange(len(bad))])
            choices = []
            for edge, _ in cycles[ci]:
                indices, direction = related[edge]
                deltas = np.arange(modulus) - voltage[edge]
                violations = (sums[indices, None] + direction[:, None] * deltas) % modulus == 0
                scores = (violations * penalties[indices, None]).sum(axis=0)
                old_score = int(scores[voltage[edge]])
                raw = violations.sum(axis=0) - np.count_nonzero(sums[indices] == 0)
                for value in range(modulus):
                    if value == voltage[edge]:
                        continue
                    if tabu[edge, value] > stats['iterations'] and len(bad) + raw[value] >= best_bad:
                        continue
                    choices.append((int(scores[value]) - old_score, rng.random(), edge, value))
            if not choices:
                continue
            _, _, edge, value = min(choices)
            old = voltage[edge]
            indices, direction = related[edge]
            sums[indices] = (sums[indices] + direction * (value - old)) % modulus
            voltage[edge] = value
            stats['iterations'] += 1
            tabu[edge, old] = stats['iterations'] + rng.randint(7, 20)
            if plateau and plateau % 80 == 0:
                penalties[bad] += 1
            if plateau > 2000:
                break
        if best is not None:
            pending = best[:]
            for _ in range(rng.randint(3, 15)):
                pending[rng.randrange(edge_count)] = rng.randrange(modulus)
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
    config_id=os.environ.get('MATHBENCH_CONFIG_ID', 'T006-C01')
    if config_id not in ('T006-C01','T006-C02'):
        raise ValueError('unsupported configuration')
    if config_id == 'T006-C02':
        from lps import build_graph
        graph=build_graph((0,2))
        validate(graph, {'parameters': {'degree':4,'girth':9}})
        graph['_evolution']={'method':'valid LPS girth-10 fallback for the girth-9 configuration','iterations':0}
        return graph
    try:
        budget = max(0.1, min(240.0, float(os.environ.get('MATHBENCH_EVOLUTION_SECONDS', '45'))))
    except ValueError:
        budget = 45.0
    started = time.monotonic()
    deadline = started + budget
    rng = random.Random(int(os.environ.get('MATHBENCH_SEED', '0')))
    base_adj, cycles, edge_count = _base_graph()
    preprocessing_seconds = time.monotonic() - started
    best = None
    warm_path = os.environ.get('MATHBENCH_WARM_START')
    if warm_path:
        with open(warm_path, encoding='utf-8') as stream:
            best = json.load(stream)
        validate(best, {'parameters': {'degree': 4, 'girth': 10}})
    import subprocess
    import tempfile
    from pathlib import Path
    stats = {'iterations': 0, 'moduli_succeeded': [], 'minimum_violations': {}}
    with tempfile.TemporaryDirectory(prefix='t006_voltage_') as temporary:
        executable = Path(temporary) / 'voltage_search'
        subprocess.run(['g++', '-O3', '-std=c++17', str(Path(__file__).with_name('voltage_search.cpp')),
                        '-o', str(executable)], check=True, capture_output=True, timeout=35)
        # Prioritize covers that improve the owned incumbent. Alternate the
        # schedule across seeds to give harder moduli a whole search phase.
        moduli = [16, 15, 14, 13]
        if rng.randrange(2):
            moduli = [15, 16, 14, 13]
        for index, modulus in enumerate(moduli):
            if time.monotonic() >= deadline:
                break
            if best is not None and 80*modulus >= best['vertices']:
                continue
            initial = _warm_voltage(warm_path, base_adj, modulus)
            if initial is None:
                initial = [rng.randrange(modulus) for _ in range(edge_count)]
            remaining = max(0.0, deadline-time.monotonic()) / (len(moduli)-index)
            payload = f"{rng.randrange(2**32)} {remaining:.6f} {modulus} {len(cycles)} {edge_count}\n"
            payload += '\n'.join(' '.join(f'{e} {sign}' for e, sign in cycle) for cycle in cycles)
            payload += '\n' + ' '.join(map(str, initial)) + '\n'
            run = subprocess.run([str(executable)], input=payload, text=True, capture_output=True,
                                 check=True, timeout=remaining+10)
            header, raw = run.stdout.strip().split('\n')
            iterations, bad = map(int, header.split())
            stats['iterations'] += iterations
            stats['minimum_violations'][str(modulus)] = bad
            if bad:
                continue
            voltage = list(map(int, raw.split()))
            candidate = _lift(base_adj, voltage, modulus)
            validate(candidate, {'parameters': {'degree': 4, 'girth': 10}})
            best = candidate
            stats['moduli_succeeded'].append(modulus)
    if best is not None:
        best['_evolution'] = {
            'iterations': stats['iterations'],
            'moduli_succeeded': stats['moduli_succeeded'],
            'preprocessing_seconds': preprocessing_seconds,
            'minimum_violations': stats['minimum_violations'],
            'method': 'compiled weighted tabu voltage residue histograms',
        }
        return best
    # The established independently checked algebraic seed remains a fallback.
    from lps import build_graph
    return build_graph((0, 2))
