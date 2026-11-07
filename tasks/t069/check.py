"""Exact checker for the Mona Lisa 100K Euclidean TSP instance."""

from functools import lru_cache
import hashlib
from pathlib import Path
import math


CONFIG_ID = "T069-C01"
N = 100_000
INSTANCE_NAME = "mona-lisa100K"
INSTANCE_SHA256 = "532fefbfb9ad66cc2550bece766fa069acaa8e34ee511ac1949ae101da4d70ad"
TOUR_SHA256 = "d8a98a936d01b0317ff63a43646fbbbfa74bf6ee954a9449ad659128e579eb88"
PARAMETERS = {
    "instance": INSTANCE_NAME,
    "cities": N,
    "edge_weight_type": "EUC_2D; nearest-integer rounding",
    "tour": "one Hamiltonian cycle through all cities",
    "objective": "sum of integer edge lengths, including return edge",
}


def _parse_tsplib(raw):
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        raise ValueError("pinned TSP file must be ASCII") from exc
    coords = []
    in_section = False
    for line in lines:
        row = line.strip()
        if row == "NODE_COORD_SECTION":
            in_section = True
            continue
        if row == "EOF":
            break
        if not in_section or not row:
            continue
        fields = row.split()
        if len(fields) != 3:
            raise ValueError("malformed NODE_COORD_SECTION row")
        try:
            node, x, y = map(int, fields)
        except ValueError as exc:
            raise ValueError("TSP coordinates must be integers") from exc
        if node != len(coords) + 1:
            raise ValueError("node IDs must be consecutive and 1-based")
        coords.append((x, y))
    if len(coords) != N:
        raise ValueError(f"expected exactly {N} coordinates, got {len(coords)}")
    return tuple(coords)


@lru_cache(maxsize=1)
def load_points():
    path = Path(__file__).parent / "data/source/mona-lisa100K.tsp"
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != INSTANCE_SHA256:
        raise ValueError("TSP instance does not match pinned SHA-256")
    return _parse_tsplib(raw)


def edge_length(points, a, b):
    dx = points[a][0] - points[b][0]
    dy = points[a][1] - points[b][1]
    square = dx * dx + dy * dy
    root = math.isqrt(square)
    return root + int(4 * square >= (2 * root + 1) ** 2)


def tour_length(points, tour):
    n = len(tour)
    return sum(edge_length(points, tour[i], tour[(i + 1) % n]) for i in range(n))


def _check_config(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    if config.get("id") not in (None, CONFIG_ID):
        raise ValueError(f"unsupported configuration: expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must identify the fixed Mona Lisa 100K EUC_2D instance")


def validate(solution, config, strict=False):
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    tour = solution.get("tour")
    if not isinstance(tour, list) or len(tour) != N:
        raise ValueError(f"tour must be a list of exactly {N} city indices")
    seen = bytearray(N)
    for pos, city in enumerate(tour):
        if type(city) is not int:
            raise ValueError(f"tour entry {pos} must be an integer (booleans are not accepted)")
        if not 0 <= city < N:
            raise ValueError(f"tour entry {pos} is outside 0..{N - 1}")
        if seen[city]:
            raise ValueError(f"duplicate city {city}")
        seen[city] = 1
    points = load_points()
    score = tour_length(points, tour)
    return {
        "objective": score,
        "verification_status": "exact",
        "details": {
            "instance": INSTANCE_NAME,
            "instance_sha256": INSTANCE_SHA256,
            "city_count": N,
            "unique_city_count": N,
            "closed_tour_edge_count": N,
            "distance_rule": "isqrt(squared_distance), rounded to nearest integer with exact half-up comparison",
            "claimed_score_ignored": True,
        },
    }
