"""Exact checker for the CVRPLIB X-n1001-k43 capacitated routing instance."""

from tasks.t057.instance import load_instance, total_route_cost


CONFIG_ID = "T057-C01"
PARAMETERS = {
    "instance": "X-n1001-k43",
    "customers": 1000,
    "depot_node_id": 1,
    "vehicle_capacity": 131,
    "distance": "TSPLIB EUC_2D nearest-integer rounding",
    "route_count": "unrestricted; k43 is part of the instance name, not a fleet-size constraint",
}


def _check_config(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    if config.get("id") not in (None, CONFIG_ID):
        raise ValueError(f"unsupported configuration: expected {CONFIG_ID}")
    parameters = config.get("parameters")
    if not isinstance(parameters, dict) or parameters != PARAMETERS:
        raise ValueError("configuration must fix X-n1001-k43, capacity 131, and unrestricted route count")


def validate(solution, config, strict=False):
    """Check every route and recompute its full integer travel cost."""
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    routes = solution.get("routes")
    if not isinstance(routes, list) or not routes:
        raise ValueError("routes must be a nonempty list")
    instance = load_instance()
    expected = set(instance["customer_ids"])
    seen = set()
    loads = []
    for route_index, route in enumerate(routes, start=1):
        if not isinstance(route, list) or not route:
            raise ValueError(f"route {route_index} must be a nonempty list")
        load = 0
        for node in route:
            if type(node) is not int or node not in expected:
                raise ValueError(f"route {route_index} has invalid customer node id {node!r}")
            if node in seen:
                raise ValueError(f"customer {node} appears more than once")
            seen.add(node)
            load += instance["demands"][node]
        if load > instance["capacity"]:
            raise ValueError(f"route {route_index} load {load} exceeds capacity 131")
        loads.append(load)
    missing = sorted(expected - seen)
    if missing:
        raise ValueError(f"missing {len(missing)} customers; first missing ids: {missing[:10]}")
    objective = total_route_cost(routes, instance)
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "instance": instance["name"],
            "customer_count": len(expected),
            "route_count": len(routes),
            "route_count_unrestricted": True,
            "capacity": instance["capacity"],
            "route_loads": loads,
            "claimed_objective_ignored": True,
        },
    }
