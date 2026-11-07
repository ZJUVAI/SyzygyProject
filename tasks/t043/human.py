"""Rebuild the published 333-code from its printed orbit representatives."""

import json
import os
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "source" / "heinlein_2019_appendix_c.json"


def _matrix_product(left, right):
    """Product of 7x7 binary matrices stored as row bitmasks."""
    columns = [sum(((right[i] >> j) & 1) << i for i in range(7)) for j in range(7)]
    return tuple(sum(((left[i] & columns[j]).bit_count() & 1) << j for j in range(7))
                 for i in range(7))


def _transform(vector, matrix):
    result = 0
    for j in range(7):
        column = sum(((matrix[i] >> j) & 1) << i for i in range(7))
        result |= ((vector & column).bit_count() & 1) << j
    return result


def _span(rows):
    return frozenset((a * rows[0]) ^ (b * rows[1]) ^ (c * rows[2])
                     for a in (0, 1) for b in (0, 1) for c in (0, 1))


def _canonical_basis(vectors):
    """Return a deterministic independent three-row basis of a 3-space."""
    chosen = []
    span = {0}
    for vector in sorted(vectors - {0}):
        if vector not in span:
            chosen.append(vector)
            span |= {value ^ vector for value in span}
            if len(chosen) == 3:
                break
    if len(chosen) != 3:
        raise ValueError("decoded representative does not span dimension three")
    return chosen


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T043-C01") != "T043-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    data = json.loads(DATA.read_text(encoding="utf-8"))
    generators = [tuple(sum(bit << j for j, bit in enumerate(row)) for row in matrix)
                  for matrix in data["generators"]]
    identity = tuple(1 << i for i in range(7))
    group = [identity]
    seen = {identity}
    for current in group:
        for generator in generators:
            product = _matrix_product(current, generator)
            if product not in seen:
                seen.add(product)
                group.append(product)
    if len(group) != 4:
        raise ValueError(f"expected G_{{4,6}} of order four, found {len(group)}")

    output = []
    seen_spaces = set()
    orbit_sizes = []
    for representatives, orbit_size in zip(data["representatives_by_orbit"], data["orbit_sizes"]):
        for digits in representatives:
            rows = [sum(((digit >> row) & 1) << col for col, digit in enumerate(digits))
                    for row in range(3)]
            base = _span(rows)
            orbit = set()
            for matrix in group:
                image = frozenset(_transform(vector, matrix) for vector in base)
                orbit.add(image)
            if len(orbit) != orbit_size:
                raise ValueError(f"orbit has size {len(orbit)}, expected {orbit_size}")
            orbit_sizes.append(len(orbit))
            for space in orbit:
                if space in seen_spaces:
                    raise ValueError("paper orbit representatives overlap")
                seen_spaces.add(space)
                output.append(_canonical_basis(space))
    if len(output) != 333:
        raise ValueError(f"reconstructed {len(output)} subspaces, expected 333")
    return {"codewords": [list(basis) for basis in output],
            "provenance": "Appendix C representatives expanded by G_{4,6}"}


if __name__ == "__main__":
    print(json.dumps(run_code()))
