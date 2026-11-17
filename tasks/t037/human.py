"""Rebuild the Frankl-Furedi recursive H6 example for n=36."""
import os

try:
    from .construction import build_iterated_h6
except ImportError:
    from construction import build_iterated_h6


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T037-C01") != "T037-C01":
        raise ValueError("unsupported T037 configuration")
    return build_iterated_h6(parts=6)
