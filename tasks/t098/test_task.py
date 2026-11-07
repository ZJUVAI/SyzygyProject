import copy
import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from mathbench.evaluate import _run
import tasks.t098.baseline as baseline_module
from tasks.t098.baseline import _MUTATIONS, run_code as baseline_run
from tasks.t098.builder import tile_bouwkamp_line
from tasks.t098.check import CONFIG_ID, FROZEN_CONFIG, PARAMETERS, _simple_rectangle_check, validate
from tasks.t098.evolution import run_code as evolution_run
from tasks.t098.human import run_code as human_run
from tasks.t098.init_program import run_code as init_run
from tasks.t098.reference import run_code as reference_run

TASK = Path(__file__).parent
CONFIG = FROZEN_CONFIG


def test_five_entries_and_reconstructed_construction(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("T098_SEARCH_ITERS", "0")
    initial = init_run()
    baseline = baseline_run()
    evolved = evolution_run()
    human = human_run()
    reference = reference_run()
    assert baseline == evolved
    assert human == reference
    for solution in (initial, baseline, evolved, human, reference):
        result = validate(solution, CONFIG)
        assert result["verification_status"] == "exact"
        assert result["objective"] == solution["side"]
        assert result["details"]["claimed_objective_ignored"] is True
    assert initial["side"] == 4755
    assert human["side"] == 352



def test_baseline_proposes_new_side_sets_and_outer_sides(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("T098_SEARCH_ITERS", "40")
    result = baseline_run()
    assert any(delta != 0 for delta, _, _, _ in _MUTATIONS)
    assert baseline_module.LAST_SEARCH_STATS["size_set_and_outer_side_proposals"] == 40
    assert any(side != 4755 for side in baseline_module.LAST_SEARCH_STATS["distinct_proposed_outer_sides"])
    assert baseline_module.LAST_SEARCH_STATS["best_objective"] == validate(result, CONFIG)["objective"]
    assert baseline_module.LAST_SEARCH_STATS["baseline_fallback_used"] is True
    assert baseline_module.LAST_SEARCH_STATS["valid_candidates"] == 0


def test_bouwkamp_reconstruction_and_source_hash():
    path = TASK / "data/source/williams_38_352A.bkp"
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == "ec1858af8249dc4aba58e116f87646f31e3c240f1efdbcf030c72b4b603fcd5b"
    assert tile_bouwkamp_line(raw.decode().strip()) == reference_run()


def test_saved_own_seed_and_exact_score():
    witness = json.loads((TASK / "best/seed_4755.json").read_text())
    assert witness == init_run()
    assert validate(witness, CONFIG)["objective"] == 4755
    metadata = json.loads((TASK / "best/seed_4755.metadata.json").read_text())
    assert metadata["objective"] == 4755


def test_claimed_scores_do_not_change_result():
    solution = reference_run()
    expected = validate(solution, CONFIG)
    for key, value in (("objective", -999), ("score", float("nan")), ("claimed_score", "fake")):
        assert validate({**solution, key: value}, CONFIG) == expected


@pytest.mark.parametrize("bad", [
    {"id": "T098-C01", "parameters": PARAMETERS, "direction": "minimize", "human_reference": 352.0},
    {"id": "T098-C01", "parameters": {**PARAMETERS, "order": 38.0}, "direction": "minimize", "human_reference": 352},
    {"id": "T098-C01", "parameters": {**PARAMETERS, "extra": True}, "direction": "minimize", "human_reference": 352},
    {"id": "T098-C02", "parameters": PARAMETERS, "direction": "minimize", "human_reference": 352},
])
def test_wrong_config_rejected(bad):
    with pytest.raises(ValueError, match="configuration"):
        validate(reference_run(), bad)


def test_bad_square_data_rejected():
    source = reference_run()
    duplicate_size = copy.deepcopy(source)
    duplicate_size["squares"][1][2] = duplicate_size["squares"][0][2]
    with pytest.raises(ValueError, match="distinct"):
        validate(duplicate_size, CONFIG)

    overlap = copy.deepcopy(source)
    overlap["squares"][1][:2] = overlap["squares"][0][:2]
    with pytest.raises(ValueError, match="overlap"):
        validate(overlap, CONFIG)

    bool_coordinate = copy.deepcopy(source)
    bool_coordinate["squares"][0][0] = True
    with pytest.raises(ValueError, match="integers"):
        validate(bool_coordinate, CONFIG)

    float_side = copy.deepcopy(source)
    float_side["side"] = 352.0
    with pytest.raises(ValueError, match="positive integer"):
        validate(float_side, CONFIG)

    nan_coordinate = copy.deepcopy(source)
    nan_coordinate["squares"][0][0] = float("nan")
    with pytest.raises(ValueError, match="integers"):
        validate(nan_coordinate, CONFIG)

    missing_tile = copy.deepcopy(source)
    missing_tile["squares"].pop()
    with pytest.raises(ValueError, match="exactly 38"):
        validate(missing_tile, CONFIG)


def test_nonprimitive_and_area_mismatch_rejected():
    source = reference_run()
    scaled = {"side": source["side"] * 2, "squares": [[2*x, 2*y, 2*s] for x, y, s in source["squares"]]}
    with pytest.raises(ValueError, match="primitive"):
        validate(scaled, CONFIG)
    wrong_area = copy.deepcopy(source)
    wrong_area["side"] += 1
    with pytest.raises(ValueError, match="area"):
        validate(wrong_area, CONFIG)


def test_proper_rectangle_tiled_by_multiple_squares_is_rejected():
    with pytest.raises(ValueError, match="proper squared rectangle"):
        _simple_rectangle_check(3, [(0, 0, 1), (1, 0, 1)])


def test_runner_error_and_timeout_without_registry():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T098 failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T098 failure')"], env, 3)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(5)"], env, 0.2)
