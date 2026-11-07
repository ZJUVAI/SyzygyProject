"""Task-local tests for exact QAPLIB tai256c evaluation."""
import math
import json
import random
import os
import shutil
import subprocess
import sys
from pathlib import Path
import pytest

from tasks.t027.check import CONFIG_ID, N, objective, validate
from tasks.t027.baseline import _load_matrices, _swap_delta, run_code as baseline_run
from tasks.t027.human import run_code as human_run
from tasks.t027.init_program import run_code as seed_run
from tasks.t027.reference import run_code as reference_run
from tasks.t027.evolution import run_code as evolution_run

CONFIG = {"id": CONFIG_ID, "parameters": {"instance": "QAPLIB tai256c", "n": N}}


def test_identity_seed_is_valid_and_scored_exactly():
    result = validate(seed_run(), CONFIG)
    assert result["verification_status"] == "exact"
    assert isinstance(result["objective"], int)
    assert result["details"]["objective_terms"] == N * N


def test_cold_seed_copy_runs_without_repository_imports(tmp_path):
    seed_copy = tmp_path / "init_program.py"
    shutil.copy(Path(__file__).with_name("init_program.py"), seed_copy)
    isolated_env = {
        "PATH": os.environ.get("PATH", ""),
        "MATHBENCH_CONFIG_ID": CONFIG_ID,
        "MATHBENCH_SEED": "0",
    }
    code = (
        "import json, runpy; "
        "module = runpy.run_path('init_program.py'); "
        "print(json.dumps(module['run_code']()))"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code], cwd=tmp_path, env=isolated_env,
        check=True, capture_output=True, text=True, timeout=10,
    )
    exported = json.loads(completed.stdout)
    assert exported == {"permutation": list(range(N))}
    assert validate(exported, CONFIG)["verification_status"] == "exact"


def test_evolution_entry_uses_task_local_baseline(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "7")
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0.02")
    result = evolution_run()
    assert validate(result, CONFIG)["verification_status"] == "exact"
    assert result["search_metadata"]["seed"] == 7


def test_default_baseline_is_reproducible_with_fixed_check_budget(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "13")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    first = baseline_run()
    second = baseline_run()
    assert first == second
    assert first["search_metadata"]["seed"] == 13
    assert first["search_metadata"]["pair_checks"] == 10000
    assert first["search_metadata"]["budget"] == {
        "mode": "fixed_iteration_count",
        "requested_checks": 10000,
        "actual_checks": 10000,
        "requested_wall_clock_seconds": None,
        "effective_wall_clock_seconds": None,
    }
    assert validate(first, CONFIG)["verification_status"] == "exact"


def test_archived_human_witness_replays_exact_value():
    witness = human_run()
    result = validate(witness, CONFIG)
    assert result["objective"] == witness["claimed_score"]
    assert validate(reference_run(), CONFIG)["objective"] == witness["claimed_score"]


def test_claimed_score_is_ignored():
    witness = human_run()
    candidate = {"permutation": witness["permutation"]}
    expected = validate(candidate, CONFIG)
    tampered = {
        **candidate,
        "claimed_score": -1,
        "reported_score": math.inf,
        "objective": float("nan"),
        "arbitrary_metadata": {"value": [True, None, "ignored"]},
    }
    result = validate(tampered, CONFIG)
    assert result == expected
    assert result["details"]["claimed_score_ignored"] is True


@pytest.mark.parametrize("bad", [
    [0] * N,
    list(range(N - 1)),
    list(range(N - 1)) + [N],
    list(range(N - 1)) + [True],
    list(range(N - 1)) + [float("nan")],
    list(range(N - 1)) + [float("inf")],
])
def test_invalid_permutations_are_rejected(bad):
    with pytest.raises(ValueError):
        validate({"permutation": bad}, CONFIG)


def test_wrong_configuration_is_rejected():
    with pytest.raises(ValueError):
        validate({"permutation": list(range(N))}, {"id": "T027-C02", "parameters": {"n": N}})


def test_swap_delta_matches_full_exact_recomputation():
    rng = random.Random(42)
    p = list(range(N))
    rng.shuffle(p)
    a, b = _load_matrices()
    for _ in range(10):
        r, s = rng.sample(range(N), 2)
        old_score = objective(p)
        delta = _swap_delta(a, b, p, r, s)
        p[r], p[s] = p[s], p[r]
        assert objective(p) == old_score + delta
