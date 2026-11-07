"""Small self-contained product seed for a selected C7 strong power."""
import os
import itertools

_POWERS = {"T011-C01": 5, "T011-C02": 4, "T011-C03": 6}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T011-C01")
    try:
        power = _POWERS[config_id]
    except KeyError as exc:
        raise ValueError(f"unsupported configuration: {config_id}") from exc
    return {"words": [list(word) for word in itertools.product((0, 2, 4), repeat=power)]}
