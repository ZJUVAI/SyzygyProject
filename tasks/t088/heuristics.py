"""Bounded randomized construction and insertion improvement for arc130."""

import random

from tasks.t088.instance import VERTEX_COUNT, cutwidth


def grasp_order(edges, rng, alpha=0.20):
    adjacency = [[] for _ in range(VERTEX_COUNT + 1)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    first = rng.randrange(1, VERTEX_COUNT + 1)
    order = [first]
    placed = {first}
    crossing = len(adjacency[first])
    while len(order) < VERTEX_COUNT:
        frontier = set()
        for vertex in order:
            frontier.update(adjacency[vertex])
        candidates = (frontier - placed) or (set(range(1, VERTEX_COUNT + 1)) - placed)
        scored = []
        for vertex in candidates:
            links_to_prefix = sum(neighbor in placed for neighbor in adjacency[vertex])
            next_cut = crossing + len(adjacency[vertex]) - 2 * links_to_prefix
            scored.append((next_cut, vertex))
        low = min(score for score, _ in scored)
        high = max(score for score, _ in scored)
        threshold = low + alpha * (high - low)
        rcl = [vertex for score, vertex in scored if score <= threshold]
        chosen = rng.choice(sorted(rcl))
        crossing += len(adjacency[chosen]) - 2 * sum(
            neighbor in placed for neighbor in adjacency[chosen]
        )
        order.append(chosen)
        placed.add(chosen)
    return order


def insertion_descent(order, edges, rng, vertex_trials=12, passes=1):
    """Try a bounded number of exact-scored insertions; return best order."""
    current = list(order)
    current_value = cutwidth(current, edges)
    attempted = 0
    accepted = 0
    for _ in range(passes):
        changed = False
        vertices = list(current)
        rng.shuffle(vertices)
        for vertex in vertices[:vertex_trials]:
            old_index = current.index(vertex)
            without = current[:old_index] + current[old_index + 1 :]
            best_order = current
            best_value = current_value
            for new_index in range(VERTEX_COUNT):
                if new_index == old_index:
                    continue
                candidate = without[:new_index] + [vertex] + without[new_index:]
                value = cutwidth(candidate, edges)
                attempted += 1
                if value < best_value:
                    best_order, best_value = candidate, value
            if best_value < current_value:
                current, current_value = best_order, best_value
                accepted += 1
                changed = True
        if not changed:
            break
    return current, {"insertion_moves_scored": attempted, "insertion_moves_accepted": accepted}


def randomized_method(edges, seed=0, trials=4, vertex_trials=10, alpha=0.20):
    rng = random.Random(seed)
    best_order = None
    best_value = None
    total_scored = 0
    total_accepted = 0
    completed = 0
    for _ in range(trials):
        order = grasp_order(edges, rng, alpha=alpha)
        order, meta = insertion_descent(order, edges, rng, vertex_trials=vertex_trials)
        value = cutwidth(order, edges)
        completed += 1
        total_scored += meta["insertion_moves_scored"]
        total_accepted += meta["insertion_moves_accepted"]
        if best_value is None or value < best_value:
            best_order, best_value = order, value
    return best_order, {
        "algorithm": "reconstructed GRASP-style construction with bounded insertion local search",
        "seed": seed,
        "trial_limit": trials,
        "trials_completed": completed,
        "alpha": alpha,
        "vertex_trials_per_pass": vertex_trials,
        "insertion_moves_scored": total_scored,
        "insertion_moves_accepted": total_accepted,
        "reference_data_read": False,
    }
