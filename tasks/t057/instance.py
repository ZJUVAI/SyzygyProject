"""Parser and exact TSPLIB EUC_2D integer-distance functions for T057."""

from functools import lru_cache
from math import isqrt
from pathlib import Path


INSTANCE_PATH = Path(__file__).with_name("data") / "source" / "X-n1001-k43.vrp"


@lru_cache(maxsize=1)
def load_instance():
    headers = {}
    coordinates = {}
    demands = {}
    depots = []
    section = None
    for raw_line in INSTANCE_PATH.read_text(encoding="ascii").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "EOF":
            break
        if line in {"NODE_COORD_SECTION", "DEMAND_SECTION", "DEPOT_SECTION"}:
            section = line
            continue
        if section is None:
            if ":" not in line:
                raise ValueError(f"malformed TSPLIB header line: {raw_line!r}")
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip().strip('"')
        elif section == "NODE_COORD_SECTION":
            fields = line.split()
            if len(fields) != 3:
                raise ValueError("coordinate row must contain id, x, and y")
            node, x, y = map(int, fields)
            if node in coordinates:
                raise ValueError(f"duplicate coordinate id {node}")
            coordinates[node] = (x, y)
        elif section == "DEMAND_SECTION":
            fields = line.split()
            if len(fields) != 2:
                raise ValueError("demand row must contain id and demand")
            node, demand = map(int, fields)
            if node in demands:
                raise ValueError(f"duplicate demand id {node}")
            demands[node] = demand
        elif section == "DEPOT_SECTION":
            fields = line.split()
            if len(fields) != 1:
                raise ValueError("depot row must contain one node id")
            depots.append(int(fields[0]))

    expected_dimension = 1001
    expected_ids = set(range(1, expected_dimension + 1))
    if (headers.get("NAME") != "X-n1001-k43"
            or headers.get("TYPE") != "CVRP"
            or headers.get("DIMENSION") != str(expected_dimension)
            or headers.get("EDGE_WEIGHT_TYPE") != "EUC_2D"
            or headers.get("CAPACITY") != "131"):
        raise ValueError("unexpected T057 instance header")
    if set(coordinates) != expected_ids or set(demands) != expected_ids:
        raise ValueError("instance must have coordinates and demands for node ids 1..1001")
    if depots != [1, -1] or demands[1] != 0:
        raise ValueError("instance must use node 1 as its sole depot")
    if any(type(value) is not int or value <= 0 or value > 131 for node, value in demands.items() if node != 1):
        raise ValueError("customer demands must be positive integers no greater than capacity")
    return {
        "name": headers["NAME"],
        "dimension": expected_dimension,
        "customer_ids": tuple(range(2, expected_dimension + 1)),
        "depot_id": 1,
        "capacity": 131,
        "coordinates": coordinates,
        "demands": demands,
    }


def rounded_euc_2d_distance(left, right, instance=None):
    """TSPLIB EUC_2D distance, rounded to nearest integer without floats."""
    data = load_instance() if instance is None else instance
    x1, y1 = data["coordinates"][left]
    x2, y2 = data["coordinates"][right]
    square = (x1 - x2) ** 2 + (y1 - y2) ** 2
    root = isqrt(square)
    return root + int(4 * square >= (2 * root + 1) ** 2)


def total_route_cost(routes, instance=None):
    data = load_instance() if instance is None else instance
    depot = data["depot_id"]
    cost = 0
    for route in routes:
        previous = depot
        for customer in route:
            cost += rounded_euc_2d_distance(previous, customer, data)
            previous = customer
        cost += rounded_euc_2d_distance(previous, depot, data)
    return cost
