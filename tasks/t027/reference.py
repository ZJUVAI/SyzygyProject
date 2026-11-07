"""Return the fixed archived best-known tai256c witness for external comparison."""
try:
    from human import run_code as _read_archived_witness
except ImportError:  # Task-qualified import during repository tests.
    from tasks.t027.human import run_code as _read_archived_witness


def run_code():
    return _read_archived_witness()
