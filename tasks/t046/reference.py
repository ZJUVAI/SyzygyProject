"""Load the frozen reference generator for the selected configuration."""
import os

from tasks.t046.sota import read_generator, run_code as public_generator


def run_code():
    if os.environ.get('MATHBENCH_CONFIG_ID', 'T046-C01') == 'T046-C01':
        return read_generator('search_generator.json')
    return public_generator()
