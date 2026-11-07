"""Task-local tests for T088's fixed graph, programs, and exact checker."""

import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import time

import pytest

from tasks.t088 import baseline, check, evolution, human, init_program, reference
from tasks.t088.instance import load_graph


TASK = Path(__file__).resolve().parent
CONFIG = json.loads((TASK / "task.json").read_text(encoding="utf-8"))["configurations"][0]


def _independent_cutwidth(ordering):
    position = {vertex: index for index, vertex in enumerate(ordering)}
    edges = load_graph()
    return max(
        sum((position[left] < cut) != (position[right] < cut) for left, right in edges)
        for cut in range(1, 130)
    )


def test_graph_source_and_all_entries(monkeypatch):
    monkeypatch.setenv("T088_SEARCH_TRIALS", "1")
    monkeypatch.setenv("T088_INSERTION_VERTEX_TRIALS", "2")
    source = TASK / "data/source/arc130.mtx.rnd"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == (
        "be272e3c2b11280c2c8335ae966c3d14ecef94fb4cb8fc2b049ecd7d676734a8"
    )
    assert len(load_graph()) == 715
    assert len(set(load_graph())) == 715
    outputs = [
        init_program.run_code(),
        baseline.run_code(),
        human.run_code(),
        reference.run_code(),
        evolution.run_code(),
    ]
    values = [check.validate(item, CONFIG)["objective"] for item in outputs]
    assert values[0] == _independent_cutwidth(outputs[0]["ordering"])
    assert values[2] == values[3] == 229
    assert values[-1] == values[1]
    assert baseline.run_code()["search_metadata"]["reference_data_read"] is False
    assert human.run_code()["search_metadata"]["reference_data_read"] is False
    assert evolution.run_code()["search_metadata"]["reference_data_read"] is False


def test_checker_exactly_recomputes_and_ignores_claims():
    solution = human.run_code()
    expected = check.validate(solution, CONFIG)
    assert expected["verification_status"] == "exact"
    assert expected["objective"] == _independent_cutwidth(solution["ordering"])
    assert len(expected["details"]["cut_profile"]) == 129
    for key, value in (("objective", -999), ("score", float("nan")), ("claimed_score", "0")):
        forged = copy.deepcopy(solution)
        forged[key] = value
        assert check.validate(forged, CONFIG) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


@pytest.mark.parametrize(
    "ordering",
    [
        list(range(1, 130)),
        [1, 1] + list(range(3, 131)),
        [True] + list(range(2, 131)),
        [1.0] + list(range(2, 131)),
        [0] + list(range(2, 131)),
        [131] + list(range(2, 131)),
    ],
)
def test_invalid_orders_are_rejected(ordering):
    with pytest.raises(ValueError):
        check.validate({"ordering": ordering}, CONFIG)


def test_configuration_is_fixed_and_complete():
    bad_id = {**CONFIG, "id": "T088-C02"}
    with pytest.raises(ValueError):
        check.validate(init_program.run_code(), bad_id)
    bad_parameters = {**CONFIG, "parameters": {**CONFIG["parameters"], "vertices": 129}}
    with pytest.raises(ValueError):
        check.validate(init_program.run_code(), bad_parameters)
    bad_extra = {**CONFIG, "parameters": {**CONFIG["parameters"], "integer_domain": False}}
    with pytest.raises(ValueError):
        check.validate(init_program.run_code(), bad_extra)


def test_seeded_baseline_and_evolution_entry_are_repeatable(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T088-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "31")
    monkeypatch.setenv("T088_SEARCH_TRIALS", "1")
    monkeypatch.setenv("T088_INSERTION_VERTEX_TRIALS", "2")
    first = baseline.run_code()
    second = baseline.run_code()
    assert first == second
    assert check.validate(first, CONFIG)["objective"] >= 1
    assert evolution.run_code() == first


def test_runner_reports_program_errors_and_timeouts_without_registry_changes():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional failure')"], env, 5)
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(5)"], env, 0.1)
    assert time.monotonic() - start < 3
