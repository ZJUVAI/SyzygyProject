"""Exact cell-by-cell checker for rectangular tilings by the P1 11-omino."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

CONFIG_ID = "T099-C01"
_EXPECTED = {
    "polyomino": "11P1",
    "tile_area": 11,
    "congruence": "translations, rotations, and reflections allowed",
    "region": "any axis-aligned integer rectangle",
    "objective": "minimize number of congruent tile copies",
}
_TASK_DIR = Path(__file__).parent
_SHAPE_PATH = _TASK_DIR / "data/source/11P1.json"
_SHAPE_SHA256 = "e547baef5aed720511c8e413bc19f80e1e33070efde1dfc3095df5d57f2f03b6"


def _shape():
    try:
        raw_bytes = _SHAPE_PATH.read_bytes()
        if _SHAPE_SHA256 and hashlib.sha256(raw_bytes).hexdigest() != _SHAPE_SHA256:
            raise ValueError("The pinned 11P1 shape file has changed")
        raw = json.loads(raw_bytes)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("The fixed P1 shape data is missing or invalid") from exc
    if raw.get("name") != "P1 11-omino (11P1)" or raw.get("area") != 11:
        raise ValueError("Unexpected fixed polyomino data")
    cells = raw.get("cells")
    if not isinstance(cells, list) or len(cells) != 11:
        raise ValueError("The fixed P1 tile must contain 11 cells")
    out = set()
    for cell in cells:
        if (not isinstance(cell, list) or len(cell) != 2
                or type(cell[0]) is not int or type(cell[1]) is not int):
            raise ValueError("P1 cell coordinates must be integer pairs")
        if tuple(cell) in out:
            raise ValueError("Duplicate cells in the fixed P1 shape")
        out.add(tuple(cell))
    if out != {(x, 0) for x in range(5)} | {(x, y) for x in range(3) for y in (1, 2)}:
        raise ValueError("Pinned P1 cells do not match the selected 11-omino")
    return out


def _oriented(cells, orientation):
    if type(orientation) is not int or not (0 <= orientation <= 7):
        raise ValueError("Orientation must be an integer code from 0 through 7")
    out = []
    for x, y in cells:
        if orientation & 1:
            x, y = y, x
        if orientation & 2:
            x = -x
        if orientation & 4:
            y = -y
        out.append((x, y))
    min_x = min(x for x, _ in out)
    min_y = min(y for _, y in out)
    return {(x-min_x, y-min_y) for x, y in out}


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("id") != CONFIG_ID:
        raise ValueError("Unknown T099 configuration")
    params = config.get("parameters")
    if (not isinstance(params, dict) or params.keys() != _EXPECTED.keys()
            or any(type(params[k]) is not type(v) or params[k] != v for k, v in _EXPECTED.items())):
        raise ValueError("T099 parameters do not match the fixed tiling problem")
    if config.get("direction") != "minimize":
        raise ValueError("T099 is a minimization configuration")
    if not isinstance(solution, dict):
        raise ValueError("Solution must be an object")
    if set(solution) - {"width", "height", "placements", "objective", "score", "claimed_score"}:
        raise ValueError("Unsupported solution fields")
    width, height, placements = solution.get("width"), solution.get("height"), solution.get("placements")
    if type(width) is not int or type(height) is not int or width <= 0 or height <= 0:
        raise ValueError("Rectangle dimensions must be positive integers")
    if not isinstance(placements, list) or not placements:
        raise ValueError("placements must be a nonempty list")
    cells = _shape()
    if width * height != 11 * len(placements):
        raise ValueError("Rectangle area must equal 11 times the tile count")
    occupied = set()
    unique_placements = set()
    for placement in placements:
        if not isinstance(placement, dict) or set(placement) != {"x", "y", "orientation"}:
            raise ValueError("Every placement needs integer x, y, and orientation")
        x, y, orientation = placement["x"], placement["y"], placement["orientation"]
        if type(x) is not int or type(y) is not int:
            raise ValueError("Tile translations must be integers")
        if type(orientation) is not int or not 0 <= orientation <= 7:
            raise ValueError("Orientation must be an integer code from 0 through 7")
        record = (x, y, orientation)
        if record in unique_placements:
            raise ValueError("Duplicate tile placements are invalid")
        unique_placements.add(record)
        for dx, dy in _oriented(cells, orientation):
            cell = (x+dx, y+dy)
            if not (0 <= cell[0] < width and 0 <= cell[1] < height):
                raise ValueError("A tile cell lies outside the rectangle")
            if cell in occupied:
                raise ValueError("Tile cells overlap")
            occupied.add(cell)
    if len(occupied) != width * height:
        raise ValueError("The placements do not cover every rectangle cell")
    count = len(placements)
    return {
        "objective": count,
        "objective_value": count,
        "verification_status": "exact",
        "details": {
            "tile_count": count,
            "rectangle": [width, height],
            "area": width*height,
            "covered_cells": len(occupied),
            "orientation_group": "D4: four rotations and four reflected rotations",
            "claimed_score_ignored": True,
        },
    }
