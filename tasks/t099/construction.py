"""Small local search over rectangle symmetries and removable tile-aligned borders."""
from __future__ import annotations

import random

from tasks.t099.check import _oriented


def _cells_for(placement):
    x0, y0 = placement["x"], placement["y"]
    return {(x0 + x, y0 + y) for x, y in _oriented(
        {(x, 0) for x in range(5)} | {(x, y) for x in range(3) for y in (1, 2)},
        placement["orientation"],
    )}


def _placement_for(cells):
    for orientation in range(8):
        local = _oriented(
            {(x, 0) for x in range(5)} | {(x, y) for x in range(3) for y in (1, 2)},
            orientation,
        )
        min_x = min(x for x, _ in cells)
        min_y = min(y for _, y in cells)
        if cells == {(min_x + x, min_y + y) for x, y in local}:
            return {"x": min_x, "y": min_y, "orientation": orientation}
    raise ValueError("Transformed tile is not congruent to the fixed 11-omino")


def _whole_board_transform(solution, kind):
    width, height = solution["width"], solution["height"]
    swap = kind in (1, 3, 5, 7)
    out_w, out_h = (height, width) if swap else (width, height)
    placements = []
    for placement in solution["placements"]:
        transformed = set()
        for x, y in _cells_for(placement):
            if kind & 1:
                x, y = y, x
            if kind & 2:
                x = out_w - 1 - x
            if kind & 4:
                y = out_h - 1 - y
            transformed.add((x, y))
        placements.append(_placement_for(transformed))
    return {"width": out_w, "height": out_h, "placements": placements}


def _clean_cuts(solution):
    width, height = solution["width"], solution["height"]
    tile_cells = [_cells_for(p) for p in solution["placements"]]
    vertical = {0, width}
    horizontal = {0, height}
    for cut in range(1, width):
        if all(not (min(x for x, _ in cells) < cut <= max(x for x, _ in cells))
               for cells in tile_cells):
            vertical.add(cut)
    for cut in range(1, height):
        if all(not (min(y for _, y in cells) < cut <= max(y for _, y in cells))
               for cells in tile_cells):
            horizontal.add(cut)
    return sorted(vertical), sorted(horizontal), tile_cells


def _trim_candidates(solution, rng):
    xs, ys, cells = _clean_cuts(solution)
    rectangles = [(x0, x1, y0, y1)
                  for i, x0 in enumerate(xs) for x1 in xs[i + 1:]
                  for j, y0 in enumerate(ys) for y1 in ys[j + 1:]
                  if (x1 - x0) * (y1 - y0) < solution["width"] * solution["height"]]
    rng.shuffle(rectangles)
    for x0, x1, y0, y1 in rectangles:
        kept = []
        valid = True
        for placement, tile in zip(solution["placements"], cells):
            inside = [(x0 <= x < x1 and y0 <= y < y1) for x, y in tile]
            if all(inside):
                kept.append({**placement, "x": placement["x"] - x0,
                             "y": placement["y"] - y0})
            elif any(inside):
                valid = False
                break
        if valid and (x1 - x0) * (y1 - y0) == 11 * len(kept):
            yield {"width": x1 - x0, "height": y1 - y0, "placements": kept}


def run_search(seed_solution, seed=0, trials=8):
    """Try D4 board transforms and tile-aligned rectangular border cuts."""
    rng = random.Random(seed)
    best = seed_solution
    best_count = len(best["placements"])
    transforms = list(range(8))
    rng.shuffle(transforms)
    for kind in transforms[:max(1, min(8, trials))]:
        candidate = _whole_board_transform(seed_solution, kind)
        if len(candidate["placements"]) < best_count:
            best, best_count = candidate, len(candidate["placements"])
        for trimmed in _trim_candidates(candidate, rng):
            if len(trimmed["placements"]) < best_count:
                best, best_count = trimmed, len(trimmed["placements"])
    return best
