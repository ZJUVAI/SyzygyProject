"""Deterministic incremental seed; append marks with fresh distances."""
import os


def _mark_count():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T007-C01")
    counts = {"T007-C01": 29, "T007-C02": 30, "T007-C03": 32}
    if config_id not in counts:
        raise ValueError(f"unknown T007 configuration: {config_id}")
    return counts[config_id]


def run_code():
    # EVOLVE-BLOCK-START
    marks = [0]
    differences = set()
    for _ in range(_mark_count() - 1):
        candidate = marks[-1] + 1
        while True:
            new = [candidate - old for old in marks]
            if len(set(new)) == len(new) and not (set(new) & differences):
                marks.append(candidate)
                differences.update(new)
                break
            candidate += 1
    return {"marks": marks}
    # EVOLVE-BLOCK-END
