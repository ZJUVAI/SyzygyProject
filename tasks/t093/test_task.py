"""Exact geometry, task entries, and failure controls for T093."""

import copy
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path
import sys
import time

import pytest

from tasks.t093 import baseline, check, evolution, human, init_program, reference
from tasks.t093.instance import INSTANCE_SHA256, SOURCE_PATH, load_instance


TASK = Path(__file__).resolve().parent
CONFIG = json.loads((TASK / "task.json").read_text(encoding="utf-8"))["configurations"][0]


def _independent_value(solution):
    raw = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    return sum(raw["items"][item_id]["value"] for item_id in solution["item_indices"])


def test_frozen_instance_and_all_program_entries(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T093-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "7")
    monkeypatch.setenv("T093_TRIALS", "1")
    monkeypatch.setenv("T093_PLACEMENT_TRIES", "2")
    assert hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest() == INSTANCE_SHA256
    raw = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    assert raw["instance_name"] == "random_cf2_74ae2d30_50"
    assert raw["num_items"] == 44
    assert sum(item["quantity"] for item in raw["items"]) == 50
    assert len(load_instance()["container"]) == 15
    outputs = [
        init_program.run_code(),
        baseline.run_code(),
        human.run_code(),
        reference.run_code(),
        evolution.run_code(),
    ]
    values = [check.validate(output, CONFIG)["objective"] for output in outputs]
    assert values[0] == 0
    assert values[2] == values[3] == 2304
    assert values[-1] == values[1]
    assert values[1] > 0
    assert baseline.run_code()["search_metadata"]["reference_data_read"] is False


def test_human_public_witness_exact_score_and_claim_invariance():
    solution = human.run_code()
    checked = check.validate(solution, CONFIG, strict=True)
    assert checked["verification_status"] == "exact"
    assert checked["objective"] == 2304 == _independent_value(solution)
    assert checked["details"]["selected_items"] == 23
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", "fake")):
        changed = copy.deepcopy(solution)
        changed[key] = value
        assert check.validate(changed, CONFIG, strict=True) == checked
    assert checked["details"]["claimed_objective_ignored"] is True


def test_exact_triangle_intersection_distinguishes_touching_and_overlap():
    a = ((0, 0), (2, 0), (0, 2))
    touching = ((2, 0), (2, 2), (0, 2))
    overlapping = ((1, 0), (3, 0), (1, 2))
    bbox_a = (0, 0, 2, 2)
    bbox_touch = (0, 0, 2, 2)
    bbox_overlap = (1, 0, 3, 2)
    assert check._triangle_intersection_area(a, bbox_a, touching, bbox_touch) == 0
    assert check._triangle_intersection_area(a, bbox_a, overlapping, bbox_overlap) == Fraction(1, 2)


def test_invalid_solution_variants_are_rejected():
    witness = human.run_code()
    first_id = witness["item_indices"][0]
    first_position = witness["item_indices"].index(first_id)
    another_position = witness["item_indices"].index(first_id, first_position + 1)
    overlapping = copy.deepcopy(witness)
    overlapping["x_translations"][another_position] = overlapping["x_translations"][first_position]
    overlapping["y_translations"][another_position] = overlapping["y_translations"][first_position]
    outside = copy.deepcopy(witness)
    outside["x_translations"][0] += 100_000_000
    too_many = {
        "item_indices": [first_id, first_id, first_id],
        "x_translations": [witness["x_translations"][first_position],
                           witness["x_translations"][another_position],
                           witness["x_translations"][first_position]],
        "y_translations": [witness["y_translations"][first_position],
                           witness["y_translations"][another_position],
                           witness["y_translations"][first_position]],
    }
    broken = [
        overlapping,
        outside,
        too_many,
        {"item_indices": [0], "x_translations": [], "y_translations": [0]},
        {"item_indices": [True], "x_translations": [0], "y_translations": [0]},
        {"item_indices": [0], "x_translations": [False], "y_translations": [0]},
        {"item_indices": [0], "x_translations": [0.0], "y_translations": [0]},
        {"item_indices": [44], "x_translations": [0], "y_translations": [0]},
        {"item_indices": [-1], "x_translations": [0], "y_translations": [0]},
        {"item_indices": [0], "x_translations": [float("nan")], "y_translations": [0]},
    ]
    for solution in broken:
        with pytest.raises(ValueError):
            check.validate(solution, CONFIG)


def test_configuration_identity_and_parameters_are_frozen():
    bad_configs = [
        {**CONFIG, "id": "T093-C02"},
        {**CONFIG, "parameters": {**CONFIG["parameters"], "available_items_total": 44}},
        {**CONFIG, "parameters": {**CONFIG["parameters"], "container_vertices": True}},
        {**CONFIG, "parameters": {**CONFIG["parameters"], "new_rule": "rotate"}},
        {**CONFIG, "direction": "minimize"},
    ]
    for config in bad_configs:
        with pytest.raises(ValueError):
            check.validate(init_program.run_code(), config)


def test_seeded_baseline_and_evolution_are_repeatable(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T093-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "29")
    monkeypatch.setenv("T093_TRIALS", "1")
    monkeypatch.setenv("T093_PLACEMENT_TRIES", "2")
    first = baseline.run_code()
    assert baseline.run_code() == first
    assert evolution.run_code() == first
    assert check.validate(first, CONFIG)["objective"] > 0


def test_runner_program_errors_and_timeouts_without_registry_changes():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional failure')"], env, 5)
    started = time.monotonic()
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(5)"], env, 0.1)
    assert time.monotonic() - started < 3
