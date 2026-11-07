"""Human analytical baseline: the unit circle has first eigenvalue one."""
import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T096-C01") != "T096-C01":
        raise ValueError("unknown T096 configuration")
    return {
        "rho": {"constant": "1", "cos": [], "sin": []},
        "trial": {"constant": "1", "cos": [], "sin": []},
        "rho_lower_bound": "1",
        "series_terms": 0,
    }
