"""Task-local exact checks and runner-control tests for T048."""

import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t048.check import _CONFIGS, validate
from tasks.t048.human import build_batcher_network
from tasks.t048.reference import DATA

HERE = Path(__file__).resolve().parent
CONFIG = {"id":"T048-C01", "parameters": {"inputs":17}}


def _reference_solution():
    return {"comparators": json.loads(DATA.read_text())["comparators"]}


def _scalar_sort(comparators, bits):
    wires = [(bits >> i) & 1 for i in range(17)]
    for left, right in comparators:
        if wires[left] > wires[right]:
            wires[left], wires[right] = wires[right], wires[left]
    return all(wires[i] <= wires[i + 1] for i in range(16))

def test_reference_pins_and_independent_full_scalar_replay():
    net = json.loads(DATA.read_text())
    source = net["source"]
    snapshot = HERE / "data/reference/sorterhunter_sorting_networks.html"
    digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    assert digest == source["snapshot_sha256"]
    assert len(net["comparators"]) == net["size"] == 71
    assert len(net["layers"]) == net["depth"] == 12
    assert [pair for layer in net["layers"] for pair in layer] == net["comparators"]
    assert source["sorterhunter_commit"] == "8ba90df607cbdc339409e0b173b5a2ffd60fc911"
    assert validate(_reference_solution(), CONFIG)["objective"] == 71
    # Scalar simulation is separate from the task's packed-bitset checker.
    for bits in range(1 << 17):
        assert _scalar_sort(net["comparators"], bits), bits


def test_batcher_human_method_baseline_is_exactly_valid():
    net = build_batcher_network()
    assert len(net) == 85
    checked = validate({"comparators": net}, CONFIG)
    assert checked["objective"] == 85
    assert checked["verification_status"] == "exact"


def test_unknown_configuration_is_rejected():
    with pytest.raises(ValueError, match="unsupported configuration"):
        validate(_reference_solution(), {"id": "T048-C99", "parameters": {"inputs": 17}})


@pytest.mark.parametrize("solution", [
    None,
    {},
    {"comparators": None},
    {"comparators": [[0]]},
    {"comparators": [[0, 0]]},
    {"comparators": [[1, 0]]},
    {"comparators": [[0, 17]]},
    {"comparators": [[False, 1]]},
    {"comparators": [[0, 1.0]]},
    {"comparators": [[0, float("nan")]]},
    {"comparators": [[0, float("inf")]]},
    {"comparators": []},
    {"comparators": _reference_solution()["comparators"][:-1]},
])
def test_invalid_or_broken_networks_are_rejected(solution):
    with pytest.raises(ValueError):
        validate(solution, CONFIG)


def test_duplicate_comparator_is_allowed_and_counted():
    net = _reference_solution()["comparators"]
    result = validate({"comparators": net + [net[-1]]}, CONFIG)
    assert result["objective"] == 72


def test_configuration_and_claims_are_checked_or_ignored_as_required():
    with pytest.raises(ValueError):
        validate(_reference_solution(), {"parameters": {"inputs": 16}})
    base = validate(_reference_solution(), CONFIG)
    for field, value in [("objective", -100), ("score", float("nan")),
                         ("claimed_score", {"value": float("inf")})]:
        forged = _reference_solution()
        forged[field] = value
        assert validate(forged, CONFIG) == base


@pytest.mark.parametrize("module,expected", [
    ("tasks.t048.init_program", 136),
    ("tasks.t048.baseline", 136),
    ("tasks.t048.human", 85),
    ("tasks.t048.reference", 71),
    ("tasks.t048.evolution", 136),
])
def test_all_five_run_code_entries(module, expected, monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T048-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "11")
    monkeypatch.setenv("MATHBENCH_SEARCH_ITERATIONS", "2")
    entry = __import__(module, fromlist=["run_code"])
    candidate = entry.run_code()
    checked = validate(candidate, CONFIG)
    if expected is not None:
        assert checked["objective"] == expected
    assert isinstance(checked["objective"], int)


def test_search_programs_are_independent_of_comparison_programs():
    for filename in ("baseline.py", "evolution.py"):
        source = (HERE / filename).read_text()
        assert "tasks.t048.human" not in source
        assert "tasks.t048.reference" not in source
        assert "data/reference" not in source


def test_worker_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError):
        _run([sys.executable, "-c", "raise SystemExit('intentional worker error')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.15)
