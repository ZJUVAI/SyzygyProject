import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

from mathbench.evaluate import _run
from tasks.t099.check import CONFIG_ID, _EXPECTED, validate
from tasks.t099.human import run_code as human_run
from tasks.t099.reference import run_code as reference_run

ROOT = Path(__file__).parent
CONFIG = json.loads((ROOT / "task.json").read_text())["configurations"][0]


def test_public_witness_hash_and_exact_coverage():
    path = ROOT / "data/reference/11P1_54x55.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "4ca03f1b4984073bc481c76e90e1cabfd4c49351831784813f070686fb7877f0"
    )
    result = validate(reference_run(), CONFIG)
    assert result["verification_status"] == "exact"
    assert result["objective_value"] == 270
    assert result["details"]["rectangle"] == [54, 55]
    assert result["details"]["covered_cells"] == 2970


def test_human_program_replays_public_human_construction():
    assert validate(human_run(), CONFIG)["objective_value"] == 270


def test_independent_solver_seed_hash_and_exact_score():
    path = ROOT / "best/independent_cpsat_seed_270.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "5d194c9589c9dab166b66f85feeeca8fe6f3ac831dc3400e9e66da506a10c225"
    )
    assert validate(json.loads(path.read_text()), CONFIG)["objective_value"] == 270


def test_all_program_entries_produce_exact_tilings():
    from tasks.t099.baseline import run_code as baseline_run
    from tasks.t099.evolution import run_code as evolution_run
    from tasks.t099.init_program import run_code as init_run

    for run in (init_run, baseline_run, evolution_run, human_run, reference_run):
        result = validate(run(), CONFIG)
        assert result["verification_status"] == "exact"
        assert result["details"]["covered_cells"] == result["details"]["area"]
        assert result["objective_value"] == result["details"]["tile_count"]


def test_invalid_dimensions_orientation_overlap_and_hole_are_rejected():
    witness = reference_run()
    bad = {**witness, "width": True}
    with pytest.raises(ValueError, match="positive integers"):
        validate(bad, CONFIG)
    bad = json.loads(json.dumps(witness))
    bad["placements"][0]["orientation"] = True
    with pytest.raises(ValueError, match="Orientation"):
        validate(bad, CONFIG)
    bad = json.loads(json.dumps(witness))
    bad["placements"][0] = dict(bad["placements"][1])
    with pytest.raises(ValueError):
        validate(bad, CONFIG)
    bad = json.loads(json.dumps(witness))
    bad["placements"].pop()
    with pytest.raises(ValueError, match="area"):
        validate(bad, CONFIG)


def test_bad_translation_and_noninteger_are_rejected():
    witness = reference_run()
    for x in (True, 0.5, float("nan"), -1):
        bad = json.loads(json.dumps(witness))
        bad["placements"][0]["x"] = x
        with pytest.raises(ValueError):
            validate(bad, CONFIG)
    bad = json.loads(json.dumps(witness))
    bad["placements"][0]["orientation"] = 8
    with pytest.raises(ValueError):
        validate(bad, CONFIG)


def test_fixed_parameters_and_forged_score_do_not_change_result():
    with pytest.raises(ValueError, match="fixed"):
        validate(reference_run(), {
            "id": CONFIG_ID,
            "parameters": {**_EXPECTED, "tile_area": True},
            "direction": "minimize",
        })
    expected = validate(reference_run(), CONFIG)
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", {"fake": 1})):
        assert validate({**reference_run(), key: value}, CONFIG) == expected


def test_runner_error_and_timeout_controls():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T099 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T099 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
