"""Reference-free randomized coordinate search for Kakeya line anchors."""

import os
import random
import time

from tasks.t079.check import CANONICAL_DIRECTIONS, P


def _idx(point):
    x, y, z = point
    return x + P * y + P * P * z


def _points(origin, direction):
    ox, oy, oz = origin
    dx, dy, dz = direction
    return [_idx(((ox + t * dx) % P, (oy + t * dy) % P, (oz + t * dz) % P))
            for t in range(P)]


def _solution(origins):
    return {"lines": [
        {"direction": list(direction), "origin": list(origin)}
        for direction, origin in zip(CANONICAL_DIRECTIONS, origins)
    ]}


def run_search(seed, sweeps, samples_per_line):
    rng = random.Random(seed)
    origins = [(0, 0, 0) for _ in CANONICAL_DIRECTIONS]
    line_sets = [_points(origin, direction)
                 for origin, direction in zip(origins, CANONICAL_DIRECTIONS)]
    occupancy = [0] * (P ** 3)
    union_size = 0
    for points in line_sets:
        for index in points:
            if occupancy[index] == 0:
                union_size += 1
            occupancy[index] += 1

    requested_seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    cutoff = None if requested_seconds is None else time.monotonic() + max(0.0, float(requested_seconds))
    candidate_count = 0
    accepted_moves = 0
    completed_sweeps = 0
    for sweep in range(sweeps):
        order = list(range(len(CANONICAL_DIRECTIONS)))
        rng.shuffle(order)
        for line_id in order:
            if cutoff is not None and time.monotonic() >= cutoff:
                break
            old_points = line_sets[line_id]
            old_set = set(old_points)
            removed_unique = sum(occupancy[index] == 1 for index in old_points)
            best_origin = origins[line_id]
            best_points = old_points
            best_size = union_size
            direction = CANONICAL_DIRECTIONS[line_id]
            # Exclude the current anchor from the occupancy while scoring replacements.
            for _ in range(samples_per_line):
                if cutoff is not None and time.monotonic() >= cutoff:
                    break
                candidate_origin = (rng.randrange(P), rng.randrange(P), rng.randrange(P))
                candidate_points = _points(candidate_origin, direction)
                new_count = sum(
                    occupancy[index] == (1 if index in old_set else 0)
                    for index in candidate_points
                )
                candidate_size = union_size - removed_unique + new_count
                candidate_count += 1
                if candidate_size < best_size:
                    best_size = candidate_size
                    best_origin = candidate_origin
                    best_points = candidate_points
            if best_origin != origins[line_id]:
                for index in old_points:
                    occupancy[index] -= 1
                for index in best_points:
                    occupancy[index] += 1
                origins[line_id] = best_origin
                line_sets[line_id] = best_points
                union_size = best_size
                accepted_moves += 1
        else:
            completed_sweeps += 1
            continue
        break

    return {
        **_solution(origins),
        "search_metadata": {
            "algorithm": "seeded randomized greedy anchor replacement with exact marginal union counts",
            "seed": seed,
            "requested_sweeps": sweeps,
            "completed_sweeps": completed_sweeps,
            "samples_per_line": samples_per_line,
            "candidate_anchors_evaluated": candidate_count,
            "accepted_replacements": accepted_moves,
            "comparison_data_read": False,
            "budget": {
                "mode": "fixed iterations" if requested_seconds is None else "wall-clock cutoff",
                "requested_wall_clock_seconds": None if requested_seconds is None else float(requested_seconds),
            },
        },
    }
