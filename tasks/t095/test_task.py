import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

from mathbench.evaluate import _run
from tasks.t095.baseline import run_code as baseline_run
from tasks.t095.check import (
    CONFIG_ID,
    _EXPECTED,
    _hull_with_collinear_boundary,
    _segments_intersect,
    load_points,
    validate,
)
from tasks.t095.evolution import run_code as evolution_run
from tasks.t095.human import run_code as human_run
from tasks.t095.init_program import run_code as init_run
from tasks.t095.reference import run_code as reference_run

ROOT = Path(__file__).parent
CONFIG = json.loads((ROOT / "task.json").read_text())["configurations"][0]


def test_pinned_instance_and_official_271_face_witness():
    source = ROOT / "data/source/uniform-0000500-1.instance.json"
    public = ROOT / "data/reference/uniform-0000500-1.official_solution.json"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == (
        "c8ea5c524c52a6d7e0188f566482c124856a8cbd0318e518ff4419f09844c31a"
    )
    assert hashlib.sha256(public.read_bytes()).hexdigest() == (
        "f3de71a8fa4f98adf3314ccc2aa780e594e933b051e3d7cc715d1944eeb01190"
    )
    assert len(load_points()) == 500
    result = validate(reference_run(), CONFIG)
    assert result["verification_status"] == "exact"
    assert result["details"]["edge_count"] == 770
    assert result["objective_value"] == 271
    assert result["objective_value"] == 770 - 500 + 1


def test_human_method_baseline_is_replayed():
    result = validate(human_run(), CONFIG)
    assert result["verification_status"] == "exact"
    assert result["objective_value"] == 384


def test_all_five_entries_return_valid_partitions():
    for run in (init_run, baseline_run, evolution_run, human_run, reference_run):
        result = validate(run(), CONFIG)
        assert result["verification_status"] == "exact"
        assert result["details"]["point_count"] == 500
        assert result["details"]["face_count"] == result["objective_value"]


def test_missing_hull_edge_is_rejected():
    points = load_points()
    hull = _hull_with_collinear_boundary(points)
    a, b = hull[0], hull[1]
    bad = [e for e in reference_run()["edges"] if {e["i"], e["j"]} != {a, b}]
    with pytest.raises(ValueError, match="hull boundary edge"):
        validate({"edges": bad}, CONFIG)


def test_duplicate_self_loop_and_bad_endpoint_ids_are_rejected():
    valid = reference_run()
    with pytest.raises(ValueError, match="Duplicate edges"):
        validate({"edges": valid["edges"] + [valid["edges"][0]]}, CONFIG)
    for bad_edge in ({"i": 1, "j": 1}, {"i": True, "j": 2},
                     {"i": 0.5, "j": 2}, {"i": 0, "j": 500},
                     {"i": 0, "j": float("nan")}):
        with pytest.raises(ValueError):
            validate({"edges": [bad_edge]}, CONFIG)


def test_crossing_edge_is_rejected():
    valid = reference_run()
    edge_set = {tuple(sorted((e["i"], e["j"]))) for e in valid["edges"]}
    points = load_points()
    hull = _hull_with_collinear_boundary(points)
    crossing = None
    for pos, u in enumerate(hull):
        for v in hull[pos+1:]:
            if tuple(sorted((u, v))) in edge_set:
                continue
            for edge in valid["edges"]:
                x, y = edge["i"], edge["j"]
                if {u, v}.isdisjoint({x, y}) and _segments_intersect(
                    points[u], points[v], points[x], points[y]
                ):
                    crossing = (u, v)
                    break
        if crossing:
            break
    assert crossing is not None
    with pytest.raises(ValueError, match="cross or touch"):
        u, v = crossing
        validate({"edges": valid["edges"] + [{"i": u, "j": v}]}, CONFIG)


def test_claimed_scores_do_not_change_validation_result():
    witness = reference_run()
    expected = validate(witness, CONFIG)
    for key, value in (("objective", -100), ("score", float("nan")),
                       ("claimed_score", {"forged": True})):
        assert validate({**witness, key: value}, CONFIG) == expected


def test_config_is_strict_and_fixed():
    with pytest.raises(ValueError, match="fixed"):
        validate(reference_run(), {
            "id": CONFIG_ID,
            "parameters": {**_EXPECTED, "point_count": True},
            "direction": "minimize",
        })
    with pytest.raises(ValueError, match="minimization"):
        validate(reference_run(), {**CONFIG, "direction": "maximize"})


def test_runner_error_and_timeout_controls():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T095 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T095 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
