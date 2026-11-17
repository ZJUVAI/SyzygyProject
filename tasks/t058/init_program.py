"""Deterministic incremental seed; append marks with fresh distances."""
import os


def _mark_count():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T058-C01")
    if config_id != "T058-C01":
        raise ValueError(f"unknown T058 configuration: {config_id}")
    return 29


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
