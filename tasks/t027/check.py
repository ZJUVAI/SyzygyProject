"""Exact checker for QAPLIB tai256c permutations."""
from functools import lru_cache
import hashlib
from pathlib import Path

N = 256
INSTANCE_SHA256 = "e7d72083d49f4768e5a15a02ee33fde038a794e7407e5e485c3c110f1509fafd"
CONFIG_ID = "T027-C01"


def load_instance():
    """Load the pinned QAPLIB file, rejecting changed or malformed data."""
    path = Path(__file__).parent / "data" / "tai256c.dat"
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != INSTANCE_SHA256:
        raise ValueError("tai256c.dat does not match the pinned SHA-256")
    try:
        values = [int(token) for token in raw.decode("ascii").split()]
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("tai256c.dat must contain ASCII integers") from exc
    if len(values) != 1 + 2 * N * N or values[0] != N:
        raise ValueError("tai256c.dat has an unexpected dimension or value count")
    split = 1 + N * N
    a = tuple(tuple(values[1 + i * N:1 + (i + 1) * N]) for i in range(N))
    b = tuple(tuple(values[split + i * N:split + (i + 1) * N]) for i in range(N))
    return a, b


@lru_cache(maxsize=1)
def _instance():
    return load_instance()


def objective(permutation):
    """Return the exact integer QAP objective for a validated permutation."""
    a, b = _instance()
    return sum(a[i][j] * b[permutation[i]][permutation[j]]
               for i in range(N) for j in range(N))


def validate(solution, config, strict=False):
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    if config.get("id", CONFIG_ID) != CONFIG_ID:
        raise ValueError("unsupported configuration")
    params = config.get("parameters", {})
    if not isinstance(params, dict) or params.get("n", N) != N or params.get("instance", "QAPLIB tai256c") != "QAPLIB tai256c":
        raise ValueError("configuration must identify QAPLIB tai256c with n=256")

    permutation = solution.get("permutation")
    if not isinstance(permutation, list) or len(permutation) != N:
        raise ValueError("permutation must be a list of exactly 256 entries")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in permutation):
        raise ValueError("permutation entries must be integers, not booleans")
    if any(value < 0 or value >= N for value in permutation):
        raise ValueError("permutation entries must be in 0..255")
    if len(set(permutation)) != N:
        raise ValueError("permutation entries must be unique")

    score = objective(permutation)
    return {
        "objective": score,
        "verification_status": "exact",
        "details": {
            "instance": "tai256c",
            "n": N,
            "matrix_sha256": INSTANCE_SHA256,
            "permutation_bijection_verified": True,
            "objective_terms": N * N,
            "claimed_score_ignored": True,
        },
    }
