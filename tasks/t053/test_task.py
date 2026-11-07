"""Exact mathematical, source, entry-point, and worker tests for T053."""

import ast
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t053.check import N, PARAMETERS, validate
from tasks.t053.reference import DATA

HERE = Path(__file__).resolve().parent
CONFIG = {"parameters": PARAMETERS}


def _reference_solution():
    return {"factors": json.loads(DATA.read_text(encoding="utf-8"))["factors"]}


def _independent_spf(limit):
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1
    for p in range(2, int(limit ** 0.5) + 1):
        if spf[p] == p:
            for multiple in range(p * p, limit + 1, p):
                if spf[multiple] == multiple:
                    spf[multiple] = p
    return spf


def _legendre(n, prime):
    total = 0
    power = prime
    while power <= n:
        total += n // power
        if power > n // prime:
            break
        power *= prime
    return total


def _independently_check_prime_exponents(factors):
    spf = _independent_spf(max(factors))
    counts = {}
    for value in factors:
        remaining = value
        while remaining > 1:
            prime = spf[remaining]
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            counts[prime] = counts.get(prime, 0) + exponent
    expected_primes = [p for p in range(2, N + 1) if spf[p] == p]
    assert set(counts) == set(expected_primes)
    assert all(counts[p] == _legendre(N, p) for p in expected_primes)


def test_human_witness_exact_product_and_independent_legendre_check():
    solution = _reference_solution()
    checked = validate(solution, CONFIG)
    assert checked["objective"] == 33330
    assert checked["verification_status"] == "exact"
    _independently_check_prime_exponents(solution["factors"])


def test_human_program_reconstructs_saved_reference():
    from tasks.t053.human import run_code

    generated = run_code()
    saved = json.loads(DATA.read_text(encoding="utf-8"))
    assert generated["factors"] == saved["factors"]
    assert generated["method_metadata"]["factors_before_restoring_residual"] == 100008


def test_source_hashes_and_public_bound_endpoint_meaning():
    expected_hashes = {
        "data/source/sutherland_greedy.py": "6bc0a0ac756f406d595eced22ce6d7a004256d24f8fbd913b867570c00d9e344",
        "data/source/t_large_n_bounds.txt": "9cd480d1f294a6e9d40612bd4644726e22e3ef26eef1dedcd607c260dff4178c",
    }
    for relative, expected in expected_hashes.items():
        assert hashlib.sha256((HERE / relative).read_bytes()).hexdigest() == expected
    lines = (HERE / "data/source/t_large_n_bounds.txt").read_text().splitlines()
    samples = ast.literal_eval(lines[0].split(":", 1)[1].strip())
    bounds = ast.literal_eval(lines[1].split(":", 1)[1].strip())
    assert len(samples) == len(bounds)
    assert samples[-1] == 100000
    assert bounds[-1] == (33641, 33649)


@pytest.mark.parametrize("bad", [
    None,
    {},
    {"factors": None},
    {"factors": []},
    {"factors": [1] * (N - 1)},
    {"factors": [True] + [1] * (N - 1)},
    {"factors": [float("nan")] + [1] * (N - 1)},
    {"factors": [float("inf")] + [1] * (N - 1)},
    {"factors": [1.0] + [1] * (N - 1)},
    {"factors": [0] + [1] * (N - 1)},
    {"factors": [-1] + [1] * (N - 1)},
])
def test_malformed_or_invalid_factorizations_are_rejected(bad):
    with pytest.raises(ValueError):
        validate(bad, CONFIG)


def test_initial_construction_and_claim_invariance():
    initial = importlib.import_module("tasks.t053.init_program").run_code()
    assert validate(initial, CONFIG)["objective"] == 1
    solution = _reference_solution()
    base = validate(solution, CONFIG)
    for name, value in [("objective", -1), ("score", float("nan")),
                        ("claimed_score", {"value": float("inf")})]:
        forged = dict(solution)
        forged[name] = value
        assert validate(forged, CONFIG) == base
    with pytest.raises(ValueError):
        validate(solution, {"parameters": {"n": 100001}})


@pytest.mark.parametrize("module,expected", [
    ("tasks.t053.init_program", 1),
    ("tasks.t053.baseline", None),
    ("tasks.t053.human", 33330),
    ("tasks.t053.reference", 33330),
    ("tasks.t053.evolution", None),
])
def test_all_five_run_code_entries(module, expected, monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T053-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("MATHBENCH_SEARCH_ITERATIONS", "1")
    program = importlib.import_module(module)
    result = program.run_code()
    objective = validate(result, CONFIG)["objective"]
    if expected is not None:
        assert objective == expected
    assert isinstance(objective, int)


def test_search_programs_have_no_comparison_asset_dependency():
    for filename in ("baseline.py", "evolution.py"):
        source = (HERE / filename).read_text()
        assert "tasks.t053.human" not in source
        assert "tasks.t053.reference" not in source
        assert "data/reference" not in source


def test_worker_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError):
        _run([sys.executable, "-c", "raise SystemExit('intentional worker error')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.15)
