"""Exact tests for T065-C01."""

import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t065.check import PARAMETERS, validate


ROOT = Path(__file__).resolve().parent
CONFIG = {"id": "T065-C01", "parameters": PARAMETERS}
GRID_SHA256 = "5be485e67a475c9eb7a4127d9160fd7f928e9ecb241b9592151a31fa4e2e2a56"


def _grid_objective_independently():
    # For difference directions (1,0), (0,1), and (1,-1), count each
    # unordered adjacent pair once in the 10-by-10 index grid.
    return 9 * 10 + 10 * 9 + 9 * 9


def test_human_and_reference_grid_is_exact():
    from tasks.t065.human import run_code as human_run
    from tasks.t065.reference import run_code as reference_run

    path = ROOT / "data/reference/triangular_grid_10x10.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == GRID_SHA256
    assert reference_run() == human_run()
    witness = human_run()
    checked = validate(witness, CONFIG, strict=True)
    assert checked["objective"] == _grid_objective_independently() == 261
    assert checked["details"]["point_count"] == 100
    assert checked["details"]["unordered_pairs_checked"] == 4950
    assert checked["details"]["coordinate_field_degree"] == 4


def test_all_five_entries_return_valid_candidates(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T065-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    monkeypatch.setenv("MATHBENCH_EVOLUTION_ITERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_RESTARTS", "1")
    from tasks.t065.init_program import run_code as initial
    from tasks.t065.baseline import run_code as baseline
    from tasks.t065.evolution import run_code as evolution
    from tasks.t065.human import run_code as human
    from tasks.t065.reference import run_code as reference

    results = [initial(), baseline(), evolution(), human(), reference()]
    objectives = [validate(result, CONFIG, strict=True)["objective"] for result in results]
    assert objectives[0] == 0
    assert objectives[1] == 261
    assert objectives[2] >= 0
    assert objectives[3:] == [261, 261]
    assert results[1]["search_metadata"]["candidate_shapes_checked"] == 9
    assert results[2]["search_metadata"]["iterations_run"] == 2


def test_checker_rejects_bad_point_counts_duplicates_and_fields():
    from tasks.t065.init_program import run_code

    valid = run_code()
    with pytest.raises(ValueError, match="exactly 100"):
        validate({**valid, "points": valid["points"][:-1]}, CONFIG)
    with pytest.raises(ValueError, match="distinct"):
        points = list(valid["points"])
        points[1] = points[0]
        validate({**valid, "points": points}, CONFIG)
    with pytest.raises(ValueError, match="irreducible"):
        validate({**valid, "minimal_polynomial": [0, -1, 0, 1]}, CONFIG)
    with pytest.raises(ValueError, match="exactly one real root"):
        validate({**valid, "isolating_interval": ["1", "2"]}, CONFIG)
    with pytest.raises(ValueError, match="configuration must fix 100"):
        validate(valid, {"id": "T065-C01", "parameters": {**PARAMETERS, "point_count": 99}})


def test_checker_rejects_bool_nonfinite_and_float_coordinates():
    from tasks.t065.init_program import run_code

    valid = run_code()
    for bad_value in (True, float("nan"), float("inf"), float("-inf"), 1.0):
        points = list(valid["points"])
        points[0] = {"x": [bad_value], "y": ["0"]}
        with pytest.raises(ValueError):
            validate({**valid, "points": points}, CONFIG)


def test_claimed_scores_do_not_change_recomputed_result():
    from tasks.t065.init_program import run_code

    valid = run_code()
    result = validate(valid, CONFIG)
    for key, value in (("objective", 999999), ("score", float("nan")),
                       ("claimed_score", {"forged": True})):
        assert validate({**valid, key: value}, CONFIG) == result


def test_public_record_is_separate_and_marked_unreproduced():
    metadata = json.loads((ROOT / "sota.json").read_text())
    item = metadata["configurations"]["T065-C01"]
    assert item["public_value"] == 439
    assert item["reproduced_value"] == 261
    assert item["highest_reported"]["reproduction_status"].startswith("Reported in the paper but not reproduced")
    assert item["best_public"]["witness"] is None
    assert item["frozen_human_baseline"]["value"] == 261


def test_runner_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T065 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T065 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
