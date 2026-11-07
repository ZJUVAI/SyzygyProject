"""Deterministic and randomized-tie Clarke-Wright savings construction."""

import random

from tasks.t057.instance import load_instance, rounded_euc_2d_distance


def clarke_wright(instance=None, rng=None):
    data = load_instance() if instance is None else instance
    customers = data["customer_ids"]
    depot = data["depot_id"]
    capacity = data["capacity"]
    routes = {node: [node] for node in customers}
    loads = {node: data["demands"][node] for node in customers}
    route_of = {node: node for node in customers}

    depot_distances = {node: rounded_euc_2d_distance(depot, node, data) for node in customers}
    savings = []
    for offset, left in enumerate(customers):
        for right in customers[offset + 1:]:
            saving = (depot_distances[left] + depot_distances[right]
                      - rounded_euc_2d_distance(left, right, data))
            if saving > 0:
                savings.append((saving, left, right))
    savings.sort(key=lambda item: (-item[0], item[1], item[2]))

    if rng is not None:
        randomized = []
        start = 0
        while start < len(savings):
            stop = start + 1
            while stop < len(savings) and savings[stop][0] == savings[start][0]:
                stop += 1
            tie_group = savings[start:stop]
            rng.shuffle(tie_group)
            randomized.extend(tie_group)
            start = stop
        savings = randomized

    merges = 0
    for _saving, left, right in savings:
        left_route_id = route_of[left]
        right_route_id = route_of[right]
        if left_route_id == right_route_id:
            continue
        left_route = routes[left_route_id]
        right_route = routes[right_route_id]
        if left not in (left_route[0], left_route[-1]):
            continue
        if right not in (right_route[0], right_route[-1]):
            continue
        merged_load = loads[left_route_id] + loads[right_route_id]
        if merged_load > capacity:
            continue

        if left_route[0] == left:
            left_route = left_route[::-1]
        if right_route[-1] == right:
            right_route = right_route[::-1]
        merged = left_route + right_route
        keep_id = min(left_route_id, right_route_id)
        del routes[left_route_id]
        del routes[right_route_id]
        del loads[left_route_id]
        del loads[right_route_id]
        routes[keep_id] = merged
        loads[keep_id] = merged_load
        for node in merged:
            route_of[node] = keep_id
        merges += 1

    ordered = sorted(routes.values(), key=lambda route: min(route))
    return ordered, {"positive_saving_pairs": len(savings), "merges": merges}
