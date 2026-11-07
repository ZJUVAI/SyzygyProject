"""Self-contained valid seed made from disjoint powers-of-three exponents."""
import os


def _configuration():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T039-C01")
    if config_id != "T039-C01":
        raise ValueError(f"unknown T039 configuration: {config_id}")
    return 7, 6


def run_code():
    # EVOLVE-BLOCK-START
    row_count, marks_per_row = _configuration()
    rows = []
    for row_index in range(row_count):
        exponents = range(row_index * (marks_per_row - 1),
                          (row_index + 1) * (marks_per_row - 1))
        rows.append([0] + [3 ** exponent for exponent in exponents])
    return {"rows": rows}
    # EVOLVE-BLOCK-END
