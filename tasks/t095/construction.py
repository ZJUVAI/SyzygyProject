"""Traditional triangulation and convex-face merging for the fixed input."""

from __future__ import annotations

from collections import defaultdict
import heapq
import math
import random

import numpy as np
from scipy.spatial import Delaunay

from tasks.t095.check import load_points, _cross


def triangulate(points):
    coordinates = np.asarray(points, dtype=float)
    simplices = Delaunay(coordinates).simplices
    faces = []
    for simplex in simplices:
        face = list(map(int, simplex))
        if _cross(points[face[0]], points[face[1]], points[face[2]]) < 0:
            face.reverse()
        faces.append(face)
    return faces


def _candidate_merge(a, b):
    a_edges = {(a[i], a[(i+1) % len(a)]) for i in range(len(a))}
    b_edges = {(b[i], b[(i+1) % len(b)]) for i in range(len(b))}
    shared = {tuple(sorted(edge)) for edge in a_edges
              if (edge[1], edge[0]) in b_edges}
    if not shared:
        return None
    outgoing, incoming = {}, defaultdict(int)
    for cycle in (a, b):
        for i, u in enumerate(cycle):
            v = cycle[(i+1) % len(cycle)]
            if tuple(sorted((u, v))) in shared:
                continue
            if u in outgoing:
                return None
            outgoing[u] = v
            incoming[v] += 1
    if len(outgoing) < 3 or any(incoming[u] != 1 for u in outgoing):
        return None
    start = min(outgoing)
    merged, current = [], start
    while current not in merged:
        merged.append(current)
        current = outgoing.get(current)
        if current is None:
            return None
    if current != start or len(merged) != len(outgoing):
        return None
    return merged


def _is_convex(face, points):
    for i in range(len(face)):
        if _cross(points[face[i]], points[face[(i+1) % len(face)]],
                  points[face[(i+2) % len(face)]]) < 0:
            return False
    return True


def _edges_from_faces(faces):
    edges = set()
    for face in faces:
        for i, u in enumerate(face):
            v = face[(i+1) % len(face)]
            edges.add((min(u, v), max(u, v)))
    return [{"i": u, "j": v} for u, v in sorted(edges)]


def greedy_merge(points=None, seed=0, weights=(1.0, 0.0, 0.0), shuffle_ties=False):
    if points is None:
        points = load_points()
    rng = random.Random(seed)
    faces = {i: face for i, face in enumerate(triangulate(points))}
    edge_faces = defaultdict(set)
    for fi, face in faces.items():
        for i, u in enumerate(face):
            v = face[(i+1) % len(face)]
            edge_faces[(min(u, v), max(u, v))].add(fi)
    heap, queued = [], set()
    serial, next_id = 0, len(faces)

    def add_candidate(ia, ib):
        nonlocal serial
        if ia == ib or ia not in faces or ib not in faces:
            return
        pair = tuple(sorted((ia, ib)))
        if pair in queued:
            return
        merged = _candidate_merge(faces[ia], faces[ib])
        if merged is None or not _is_convex(merged, points):
            return
        shared_edges = []
        b_set = {(faces[ib][k], faces[ib][(k+1) % len(faces[ib])])
                 for k in range(len(faces[ib]))}
        for k, u in enumerate(faces[ia]):
            v = faces[ia][(k+1) % len(faces[ia])]
            if (v, u) in b_set:
                shared_edges.append((u, v))
        length = sum(math.hypot(points[u][0]-points[v][0], points[u][1]-points[v][1])
                     for u, v in shared_edges)
        area = abs(sum(points[merged[k]][0]*points[merged[(k+1) % len(merged)]][1]
                       - points[merged[(k+1) % len(merged)]][0]*points[merged[k]][1]
                       for k in range(len(merged)))) / 2.0
        rank = weights[0]*len(merged) + weights[1]*length + weights[2]*area
        if shuffle_ties:
            rank += rng.random() * 1e-8
        heapq.heappush(heap, (rank, serial, pair[0], pair[1], merged))
        serial += 1
        queued.add(pair)

    for adjacent in edge_faces.values():
        if len(adjacent) == 2:
            ia, ib = sorted(adjacent)
            add_candidate(ia, ib)
    while heap:
        _, _, ia, ib, merged = heapq.heappop(heap)
        pair = (ia, ib)
        queued.discard(pair)
        if ia not in faces or ib not in faces:
            continue
        # Remove both old faces from the local edge map.
        for fi in (ia, ib):
            face = faces.pop(fi)
            for k, u in enumerate(face):
                v = face[(k+1) % len(face)]
                key = (min(u, v), max(u, v))
                edge_faces[key].discard(fi)
                if not edge_faces[key]:
                    del edge_faces[key]
        ni = next_id
        next_id += 1
        faces[ni] = merged
        for k, u in enumerate(merged):
            v = merged[(k+1) % len(merged)]
            key = (min(u, v), max(u, v))
            edge_faces[key].add(ni)
            adjacent = edge_faces[key]
            if len(adjacent) == 2:
                a, b = sorted(adjacent)
                add_candidate(a, b)
    return {"edges": _edges_from_faces(list(faces.values()))}


def run_greedy_trials(points=None, seed=0, trials=4, policy_pool=None):
    if points is None:
        points = load_points()
    if policy_pool is None:
        policy_pool = [(1.0, 0.0, 0.0), (1.0, 0.001, 0.0),
                       (1.0, 0.0, 0.000001), (0.5, 0.01, 0.000001)]
    rng = random.Random(seed)
    best = None
    best_edges = None
    for _ in range(trials):
        policy = rng.choice(policy_pool)
        candidate = greedy_merge(points, seed=rng.randrange(1 << 30),
                                 weights=policy, shuffle_ties=True)
        if best is None or len(candidate["edges"]) < len(best["edges"]):
            best, best_edges = candidate, len(candidate["edges"])
    return best
