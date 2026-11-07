"""Compatibility entry point for the fixed traditional-search baseline."""

from tasks.t021.baseline import run_code


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
