"""Reconstruct a classical spectral-sequencing plus adjacent-swap baseline."""

import os

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import laplacian
from scipy.sparse.linalg import eigsh

from tasks.t045.graph import load_graph


def _spectral_order(n, edges, seed):
    rows, columns = [], []
    for u, v in edges:
        rows.extend((u, v))
        columns.extend((v, u))
    adjacency = csr_matrix((np.ones(len(rows)), (rows, columns)), shape=(n, n))
    graph_laplacian = laplacian(adjacency, normed=False)
    v0 = np.random.default_rng(seed).normal(size=n)
    eigenvalues, eigenvectors = eigsh(
        graph_laplacian, k=2, which="SM", v0=v0, tol=1e-8, maxiter=100000)
    fiedler = eigenvectors[:, 1]
    return [int(x) + 1 for x in np.argsort(fiedler)]


def _adjacent_descent(ordering, edges, sweep_limit=100):
    order = list(ordering)
    n = len(order)
    position = [0] * (n + 1)
    adjacency = [[] for _ in range(n + 1)]
    for i, vertex in enumerate(order, start=1):
        position[vertex] = i
    for u0, v0 in edges:
        u, v = u0 + 1, v0 + 1
        adjacency[u].append(v)
        adjacency[v].append(u)
    improvements_by_sweep = []
    for _ in range(sweep_limit):
        improvements = 0
        for i in range(n - 1):
            left, right = order[i], order[i + 1]
            delta = 0
            for neighbor in adjacency[left]:
                if neighbor != right:
                    delta += abs((i + 2) - position[neighbor]) - abs((i + 1) - position[neighbor])
            for neighbor in adjacency[right]:
                if neighbor != left:
                    delta += abs((i + 1) - position[neighbor]) - abs((i + 2) - position[neighbor])
            if delta < 0:
                order[i], order[i + 1] = right, left
                position[left], position[right] = i + 2, i + 1
                improvements += 1
        improvements_by_sweep.append(improvements)
        if improvements == 0:
            break
    return order, improvements_by_sweep


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T045-C01") != "T045-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    n, edges = load_graph()
    spectral = _spectral_order(n, edges, seed)
    ordering, sweep_improvements = _adjacent_descent(spectral, edges, 200)
    return {
        "ordering": ordering,
        "method": "Fiedler-vector spectral sequencing followed by strict adjacent-swap descent",
        "method_metadata": {
            "seed": seed,
            "spectral_solver": "scipy.sparse.linalg.eigsh; two smallest-magnitude Laplacian eigenvectors",
            "eigenvector_tolerance": 1e-8,
            "adjacent_swap_sweep_limit": 200,
            "sweeps_run": len(sweep_improvements),
            "improvements_by_sweep": sweep_improvements,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
