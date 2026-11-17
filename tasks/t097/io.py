"""CVRPLIB text solution parser."""

from pathlib import Path


def read_solution(path):
    routes = []
    for raw_line in Path(path).read_text(encoding="ascii").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("Cost"):
            continue
        if not line.startswith("Route #") or ":" not in line:
            raise ValueError(f"unrecognized CVRPLIB solution line: {raw_line!r}")
        route_label, raw_customers = line.split(":", 1)
        try:
            route_number = int(route_label.removeprefix("Route #"))
        except ValueError as exc:
            raise ValueError(f"invalid route label {route_label!r}") from exc
        if route_number != len(routes) + 1:
            raise ValueError("route labels must be consecutive from 1")
        # CVRPLIB .sol files number customers 1..1000; TSPLIB node ids reserve
        # node 1 for the depot, so internal node ids are solution ids plus one.
        customers = [int(value) + 1 for value in raw_customers.split()]
        if not customers:
            raise ValueError(f"route {route_number} is empty")
        routes.append(customers)
    if not routes:
        raise ValueError("solution has no routes")
    return routes
