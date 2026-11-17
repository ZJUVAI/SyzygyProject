"""Read candidate JSON and reject non-finite numbers."""
import json
import math


def _reject_constant(_):
    raise ValueError("Non-finite JSON")


def read_construction(path):
    value = json.loads(path.read_text(), parse_constant=_reject_constant)
    _finite_data(value)
    return value


def _finite_data(value):
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, float) and not math.isfinite(item):
            raise ValueError("Non-finite construction data")
        if isinstance(item, dict):
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
