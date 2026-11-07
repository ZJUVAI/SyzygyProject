"""A simple path made by flipping each coordinate once."""

import os


CONFIG_DIMENSIONS = {"T050-C01": 9, "T050-C02": 10, "T050-C03": 11}


def configured_dimension():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T050-C01")
    try:
        return CONFIG_DIMENSIONS[cid]
    except KeyError:
        raise ValueError("unsupported configuration") from None


def run_code():
    dimension = configured_dimension()
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    vertices = [0]
    current = 0
    for coordinate in range(dimension):
        current ^= 1 << coordinate
        vertices.append(current)
    # EVOLVE-BLOCK-END
    return {"vertices": vertices}


if __name__ == "__main__":
    print(run_code())
