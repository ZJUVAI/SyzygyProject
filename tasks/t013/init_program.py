import os

LENGTHS = {"T013-C01": 100, "T013-C02": 80, "T013-C03": 120}


def run_code():
    # EVOLVE-BLOCK-START
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T013-C01")
    length = LENGTHS[config_id]
    sequence = [1 if i % 2 == 0 else -1 for i in range(length)]
    # EVOLVE-BLOCK-END
    return {"sequence": sequence}
