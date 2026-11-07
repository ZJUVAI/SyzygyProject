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

@pytest.mark.parametrize("inputs,size,depth,lower", [(18,77,12,68),(19,85,12,73)])
def test_new_reference_and_batcher_human_networks(inputs,size,depth,lower,monkeypatch):
    cid=f"T048-C0{inputs-16}"
    monkeypatch.setenv("MATHBENCH_CONFIG_ID",cid)
    from tasks.t048 import reference,human
    cfg={"id":cid,"parameters":{"inputs":inputs}}
    ref=reference.run_code(); h=human.run_code()
    witness=json.loads((HERE/"data/reference"/f"sorterhunter_{inputs}_{size}_{depth}.json").read_text())
    snapshot=HERE/"data/reference/sorterhunter_sorting_networks.html"
    assert hashlib.sha256(snapshot.read_bytes()).hexdigest()==witness["source"]["snapshot_sha256"]
    assert ref["comparators"]==witness["comparators"]
    checked=validate(ref,cfg,strict=True)
    assert checked["objective"]==size
    assert checked["details"]["binary_inputs_checked"]==1<<inputs
    assert ref["reference_metadata"]["depth"]==depth
    assert len(h["comparators"])=={18:90,19:98}[inputs]
    assert validate(h,cfg)["objective"]==len(h["comparators"])
    # Source table lower bounds concern comparator count, not depth.
    assert lower < size
    forged={"comparators":ref["comparators"],"objective":-1,"score":float("nan")}
    assert validate(forged,cfg)["objective"]==size
    for bad in (ref["comparators"][:-1], [[0,inputs]]):
        with pytest.raises(ValueError): validate({"comparators":bad},cfg)

@pytest.mark.parametrize("inputs,expected", [(18,153),(19,171)])
def test_all_five_programs_support_new_configs(inputs,expected,monkeypatch):
    cid=f"T048-C0{inputs-16}"
    monkeypatch.setenv("MATHBENCH_CONFIG_ID",cid)
    monkeypatch.setenv("MATHBENCH_SEED","7")
    monkeypatch.setenv("MATHBENCH_SEARCH_ITERATIONS","1")
    from tasks.t048 import init_program,baseline,human,reference,evolution
    for module in (init_program,baseline,human,reference,evolution):
        result=module.run_code()
        checked=validate(result,{"id":cid,"parameters":{"inputs":inputs}})
        assert checked["details"]["inputs"]==inputs
        assert checked["details"]["binary_inputs_checked"]==1<<inputs
        assert isinstance(checked["objective"],int)
    assert validate(init_program.run_code(),{"id":cid,"parameters":{"inputs":inputs}})["objective"]==expected


def test_reference_pins_and_independent_full_scalar_replay():
    net = json.loads(DATA.read_text())
    source = net["source"]
    for relative, expected in [
        ("data/reference/sorterhunter_sorting_networks.html", source["snapshot_sha256"]),
        ("data/reference/valsalam_miikkulainen_2013.pdf",
         "59522734f52c0b4927e80eba4971a49ba6cc756ea5d072e382af57648544df3e"),
    ]:
        digest = hashlib.sha256((HERE / relative).read_bytes()).hexdigest()
        assert digest == expected
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
