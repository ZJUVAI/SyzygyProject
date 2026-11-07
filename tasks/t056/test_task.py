"""Mathematical, data integrity, entry-point and failure-control tests for T056."""

import hashlib
import importlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t056.check import PARAMETERS, validate

HERE = Path(__file__).resolve().parent
CONFIG = {"parameters": PARAMETERS}


def _reference():
    return json.loads((HERE / "data/reference/ta41_2006_schedule.json").read_text())


def _independent_makespan(machine_orders):
    data = json.loads((HERE / "data/source/ta41_instance.json").read_text())
    jobs, machines = data["jobs"], data["machines"]
    ops = data["operations"]
    machine_positions = [{job: i for i, job in enumerate(row)} for row in machine_orders]
    completion = [[None] * machines for _ in range(jobs)]
    pending = jobs * machines
    while pending:
        progress = False
        for job in range(jobs):
            for index in range(machines):
                if completion[job][index] is not None:
                    continue
                machine, duration = ops[job][index]
                preds = []
                if index:
                    pred = completion[job][index - 1]
                    if pred is None:
                        continue
                    preds.append(pred)
                pos = machine_positions[machine][job]
                if pos:
                    previous_job = machine_orders[machine][pos - 1]
                    previous_index = next(k for k, op in enumerate(ops[previous_job])
                                          if op[0] == machine)
                    pred = completion[previous_job][previous_index]
                    if pred is None:
                        continue
                    preds.append(pred)
                completion[job][index] = max(preds, default=0) + duration
                pending -= 1
                progress = True
        if not progress:
            raise ValueError("independent cycle check failed")
    return max(max(row) for row in completion)


def test_reference_schedule_and_independent_exact_recomputation():
    witness = _reference()
    result = validate({"machine_orders": witness["machine_orders"]}, CONFIG)
    assert result["objective"] == witness["reported_makespan"] == 2006
    assert result["verification_status"] == "exact"
    assert _independent_makespan(witness["machine_orders"]) == 2006


def test_initial_schedule_is_valid_and_boundary_score_is_exact():
    initial = importlib.import_module("tasks.t056.init_program").run_code()
    checked = validate(initial, CONFIG)
    assert checked["objective"] == 25114
    assert checked["details"]["critical_path_lower_bound"] <= checked["objective"]


def test_source_hash_and_instance_shape():
    expected = {
        "data/source/tai30_20.txt": "fa6631f4411187bb1b43e4c444293227852860fa56f3ea6e14f48a294adbd3b9",
        "data/source/ta41_instance.json": "1857bd6845eca1147b5593e2011ae4c5da24ff8749d26f603fbf909a68087ce6",
        "data/reference/ta41_2006_schedule.json": "d3760f7a46266d9da02920433f027645056704d76fb423846414ca9d275c58ed",
    }
    for relative, digest in expected.items():
        assert hashlib.sha256((HERE / relative).read_bytes()).hexdigest() == digest
    data = json.loads((HERE / "data/source/ta41_instance.json").read_text())
    assert (data["instance"], data["jobs"], data["machines"]) == ("ta41", 30, 20)
    assert all(len(job) == 20 for job in data["operations"])
    assert all(sorted(op[0] for op in job) == list(range(20)) for job in data["operations"])


@pytest.mark.parametrize("bad", [
    None,
    {},
    {"machine_orders": None},
    {"machine_orders": []},
    {"machine_orders": [[*range(30)] for _ in range(19)]},
    {"machine_orders": [[*range(30)] for _ in range(20)] + [[*range(30)]]},
    {"machine_orders": [[*range(29)] + [28] for _ in range(20)]},
    {"machine_orders": [[True, *range(1, 30)] for _ in range(20)]},
    {"machine_orders": [[0.0, *range(1, 30)] for _ in range(20)]},
    {"machine_orders": [[30, *range(1, 30)] for _ in range(20)]},
])
def test_invalid_shapes_types_and_duplicate_jobs_rejected(bad):
    with pytest.raises(ValueError):
        validate(bad, CONFIG)


def test_cycle_is_rejected_and_claims_do_not_change_validation():
    orders = [row[:] for row in _reference()["machine_orders"]]
    orders[15][9], orders[15][10] = orders[15][10], orders[15][9]
    with pytest.raises(ValueError, match="cycle"):
        validate({"machine_orders": orders}, CONFIG)

    witness = _reference()
    base = validate({"machine_orders": witness["machine_orders"]}, CONFIG)
    for name, forged in [("objective", -1), ("score", float("nan")),
                         ("claimed_score", {"value": float("inf")})]:
        candidate = {"machine_orders": witness["machine_orders"], name: forged}
        assert validate(candidate, CONFIG) == base
    with pytest.raises(ValueError):
        validate({"machine_orders": witness["machine_orders"]},
                 {"parameters": {"instance": "ta42", "jobs": 30, "machines": 20}})


@pytest.mark.parametrize("module,expected", [
    ("tasks.t056.init_program", 25114),
    ("tasks.t056.human", 3296),
    ("tasks.t056.reference", 2006),
    ("tasks.t056.baseline", None),
    ("tasks.t056.evolution", None),
])
def test_all_five_run_code_entries(module, expected, monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T056-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("MATHBENCH_SEARCH_ITERATIONS", "1")
    result = importlib.import_module(module).run_code()
    value = validate(result, CONFIG)["objective"]
    if expected is not None:
        assert value == expected
    assert type(value) is int
    if module.endswith(("baseline", "evolution")):
        assert result["search_metadata"]["budget"]["mode"] == (
            "fixed iterations; runner generation timeout 300 seconds"
        )


def test_search_sources_do_not_read_comparison_assets():
    for filename in ("baseline.py", "evolution.py"):
        source = (HERE / filename).read_text()
        assert "tasks.t056.human" not in source
        assert "tasks.t056.reference" not in source
        assert "data/reference" not in source
    init_source = (HERE / "init_program.py").read_text()
    assert "# EVOLVE-BLOCK-START" in init_source
    assert "# EVOLVE-BLOCK-END" in init_source
    assert "tasks.t056" not in init_source


def test_worker_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError):
        _run([sys.executable, "-c", "raise SystemExit('intentional worker error')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.15)
