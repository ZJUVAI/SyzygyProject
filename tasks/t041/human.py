"""Rebuild the 17-square grid-derived human baseline from its formula."""
import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T041-C01") != "T041-C01":
        raise ValueError("unsupported T041 configuration")
    _seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    squares = []
    for row in range(4):
        for col in range(4):
            if (row, col) == (0, 0):
                continue
            squares.append({"x": f"{2*col+1}/8", "y": f"{2*row+1}/8",
                            "side": "1/4", "cos": "1", "sin": "0"})
    squares.extend([
        {"x": "1/16", "y": "1/16", "side": "1/8", "cos": "1", "sin": "0"},
        {"x": "3/16", "y": "1/16", "side": "1/8", "cos": "1", "sin": "0"},
    ])
    return {"squares": squares, "objective": "4"}
