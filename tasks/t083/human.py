"""Reconstruct Friedman's published n=4 pinwheel construction."""
import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T083-C01") != "T083-C01":
        raise ValueError("unsupported configuration")
    # A coordinate is [a,b] and denotes a+b*sqrt(3).
    return {
        "side": ["1", "1/3"],
        "triangles": [
            {"anchor": [["0", "0"], ["1", "0"]], "direction": ["0", "-1"]},
            {"anchor": [["0", "1/3"], ["0", "0"]], "direction": ["1", "0"]},
            {"anchor": [["1", "1/3"], ["0", "1/3"]], "direction": ["0", "1"]},
            {"anchor": [["1", "0"], ["1", "1/3"]], "direction": ["-1", "0"]},
        ],
    }
