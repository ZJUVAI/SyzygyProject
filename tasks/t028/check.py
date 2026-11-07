"""Exact makespan checker for Taillard PFSP instance Ta051."""

from pathlib import Path
import json


_TASK_DIR = Path(__file__).parent
_DATA_PATH = _TASK_DIR / "data" / "ta051.json"
_N_JOBS = 50
_N_MACHINES = 20
_SOURCE_SHA256 = "57e114d970f7af11c64a3280068ef2ee1cfc037afd312e30d0d176900df564de"


def load_processing_times():
    """Read the fixed Taillard source snapshot; candidates cannot supply data."""
    import hashlib

    raw = _DATA_PATH.read_bytes()
    if hashlib.sha256(raw).hexdigest() != _SOURCE_SHA256:
        raise RuntimeError("trusted Ta051 input hash does not match the frozen snapshot")
    payload = json.loads(raw)
    matrix = payload.get("processing_times") if isinstance(payload, dict) else None
    if not isinstance(matrix, list) or len(matrix) != _N_MACHINES:
        raise RuntimeError("Ta051 processing-time matrix has the wrong number of machines")
    if any(not isinstance(row, list) or len(row) != _N_JOBS for row in matrix):
        raise RuntimeError("Ta051 processing-time matrix has the wrong number of jobs")
    if any(type(value) is not int or value <= 0 for row in matrix for value in row):
        raise RuntimeError("Ta051 processing times must be positive integers")
    return tuple(tuple(row) for row in matrix)


def makespan(permutation, processing_times=None):
    """Return exact integer Cmax from the standard PFSP completion recurrence."""
    if processing_times is None:
        processing_times = load_processing_times()
    completion = [0] * _N_MACHINES
    for job in permutation:
        for machine in range(_N_MACHINES):
            previous_machine = completion[machine - 1] if machine else 0
            completion[machine] = max(completion[machine], previous_machine) + processing_times[machine][job - 1]
    return completion[-1]


def validate(solution, config, strict=False):
    """Validate a 1-based permutation and recompute its integer makespan."""
    del strict  # The checker evaluates every operation with exact integer arithmetic.
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    if config.get("id", "T028-C01") != "T028-C01":
        raise ValueError("configuration id must be T028-C01")
    params = config.get("parameters", config)
    expected = {
        "instance": "Ta051",
        "jobs": _N_JOBS,
        "machines": _N_MACHINES,
        "schedule_type": "permutation",
        "processing_times_sha256": _SOURCE_SHA256,
    }
    if not isinstance(params, dict) or any(params.get(key) != value for key, value in expected.items()):
        raise ValueError("configuration must fix the trusted Ta051 50-job, 20-machine permutation instance")
    permutation = solution.get("permutation")
    if not isinstance(permutation, list):
        raise ValueError("permutation must be a list")
    if len(permutation) != _N_JOBS:
        raise ValueError("permutation must contain exactly 50 jobs")
    if any(type(job) is not int for job in permutation):
        raise ValueError("job labels must be integers, not bool or numeric values")
    if any(job < 1 or job > _N_JOBS for job in permutation):
        raise ValueError("job labels must be in 1..50")
    if set(permutation) != set(range(1, _N_JOBS + 1)):
        raise ValueError("each job must occur exactly once in the common permutation")
    value = makespan(permutation)
    return {
        "objective": value,
        "verification_status": "exact",
        "details": {
            "instance": "Ta051",
            "jobs": _N_JOBS,
            "machines": _N_MACHINES,
            "schedule_type": "permutation",
            "all_operations_recomputed": True,
            "processing_times_source_sha256": _SOURCE_SHA256,
            "claimed_objective_ignored": True,
        },
    }
