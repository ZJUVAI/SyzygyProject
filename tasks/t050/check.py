"""Exact validator for induced paths in the configured cube."""
from tasks.t050.init_program import CONFIG_DIMENSIONS

DIMENSION = 9
VERTEX_COUNT = 1 << DIMENSION
PARAMETERS = {
    "dimension": DIMENSION,
    "graph": "Q9",
    "object": "induced_path",
    "length_unit": "edges",
}


def validate(solution, config, strict=False):
    params = config.get("parameters")
    if not isinstance(params, dict):
        raise ValueError("unsupported configuration")
    dimension = params.get("dimension")
    if type(dimension) is not int or dimension not in CONFIG_DIMENSIONS.values():
        raise ValueError("unsupported dimension")
    if params != dict(PARAMETERS, dimension=dimension, graph=f"Q{dimension}"):
        raise ValueError("unsupported configuration")
    if "id" in config and CONFIG_DIMENSIONS.get(config["id"]) != dimension:
        raise ValueError("configuration ID does not match dimension")
    vertex_count = 1 << dimension
    if not isinstance(solution, dict) or "vertices" not in solution:
        raise ValueError("solution must contain vertices")
    vertices = solution["vertices"]
    if not isinstance(vertices, (list, tuple)):
        raise ValueError("vertices must be a list or tuple")
    if len(vertices) < 2:
        raise ValueError("an induced path must contain at least one edge")
    if any(type(vertex) is not int for vertex in vertices):
        raise ValueError("vertex labels must be integers; bool and non-integer values are rejected")
    if any(vertex < 0 or vertex >= vertex_count for vertex in vertices):
        raise ValueError(f"vertex labels must be in the range [0, {vertex_count})")
    if len(set(vertices)) != len(vertices):
        raise ValueError("path vertices must be distinct")
    for index, (left, right) in enumerate(zip(vertices, vertices[1:])):
        if (left ^ right).bit_count() != 1:
            raise ValueError(f"consecutive vertices {index} and {index + 1} are not adjacent")
    for i, left in enumerate(vertices):
        for j in range(i + 2, len(vertices)):
            if (left ^ vertices[j]).bit_count() == 1:
                raise ValueError(f"nonconsecutive vertices {i} and {j} are adjacent")
    objective = len(vertices) - 1
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "dimension": dimension,
            "vertices_checked": len(vertices),
            "nonconsecutive_pairs_checked": (len(vertices) - 1) * (len(vertices) - 2) // 2,
            "claimed_objective_ignored": True,
        },
    }
