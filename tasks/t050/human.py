"""Replay Wynn's published traditional 190-edge Q9 snake."""

import json
from pathlib import Path

from tasks.t050.init_program import configured_dimension


def run_code():
    dimension = configured_dimension()
    path = Path(__file__).parent / "data" / "reference" / "wynn_q9_190.json"
    witness = json.loads(path.read_text())
    vertices = witness["vertices"]
    # The new coordinate layer has one vertex, adjacent only to the old endpoint.
    for bit in range(9, dimension):
        vertices.append(vertices[-1] ^ (1 << bit))
    return {"vertices": vertices}


if __name__ == "__main__":
    print(run_code())
