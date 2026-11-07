"""Rebuild the published UBC 6-fan construction for n divisible by six."""

N = 120


def _edge(a, b):
    return (min(a, b), max(a, b))


def run_code():
    edges = {_edge(i, (i + 1) % N) for i in range(N)}
    hubs = (0, 40, 80)
    edges.update(_edge(a, b) for a, b in zip(hubs, hubs[1:] + hubs[:1]))
    for vertex in range(N):
        if vertex in hubs:
            continue
        distances = [min((vertex - hub) % N, (hub - vertex) % N) for hub in hubs]
        nearest = min(distances)
        for hub, distance in zip(hubs, distances):
            if distance == nearest:
                edges.add(_edge(vertex, hub))
    return {"edges": [list(edge) for edge in sorted(edges)]}
