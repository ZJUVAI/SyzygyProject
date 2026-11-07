"""Simple initial candidate: the unit circle and constant trial function."""
import os


def run_code():
    # EVOLVE-BLOCK-START
    if os.environ.get("MATHBENCH_CONFIG_ID", "T096-C01") != "T096-C01":
        raise ValueError("unknown T096 configuration")
    candidate = {
        "rho": {"constant": "1", "cos": [], "sin": []},
        "trial": {"constant": "1", "cos": [], "sin": []},
        "rho_lower_bound": "1",
        "series_terms": 0,
    }
    # EVOLVE-BLOCK-END
    return candidate
