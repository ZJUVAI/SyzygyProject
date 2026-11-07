"""Local exact checks for T043, independent of the shared task registry."""

import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t043.check import PARAMETERS, validate

ROOT = Path(__file__).resolve().parent
CONFIG = {"parameters": PARAMETERS}


def _one_space():
    return {"codewords": [[1, 2, 4]]}


def test_checker_valid_invalid_duplicate_and_claim_invariance():
    valid = _one_space()
    assert validate(valid, CONFIG)["objective"] == 1
    with pytest.raises(ValueError, match="rank 3"):
        validate({"codewords": [[1, 2, 3]]}, CONFIG)
    with pytest.raises(ValueError, match="intersect"):
        validate({"codewords": [[1, 2, 4], [1, 2, 8]]}, CONFIG)
    # These bases differ, but they span the same 3-space.
    with pytest.raises(ValueError, match="duplicate codeword"):
        validate({"codewords": [[1, 2, 4], [3, 2, 4]]}, CONFIG)
    with pytest.raises(ValueError, match="bool is rejected"):
        validate({"codewords": [[[True, 0, 0, 0, 0, 0, 0], [0] * 7, [0] * 7]]}, CONFIG)
    baseline = validate(valid, CONFIG)
    assert validate({**valid, "objective": 999}, CONFIG) == baseline
    assert validate({**valid, "score": float("nan")}, CONFIG) == baseline
    assert validate({**valid, "claimed_score": {"bad": True}}, CONFIG) == baseline
    assert validate({"codewords": []}, CONFIG)["objective"] == 0


def test_published_representatives_reconstruct_and_verify_exactly():
    from tasks.t043.human import run_code

    witness = run_code()
    checked = validate(witness, CONFIG, strict=True)
    assert checked["objective"] == 333
    assert checked["details"]["pairs_checked"] == 55278
    data = json.loads((ROOT / "data/source/heinlein_2019_appendix_c.json").read_text())
    assert data["source"]["source_sha256"] == (
        "26622afb1178db82948f215c7befe73172f8c30338f0632d1ae0786d487f2eb7")


def test_source_representatives_have_expected_orbit_counts():
    data = json.loads((ROOT / "data/source/heinlein_2019_appendix_c.json").read_text())
    assert [len(group) for group in data["representatives_by_orbit"]] == [9, 26, 68]
    assert len(data["generators"]) == 2
    assert 9 + 2 * 26 + 4 * 68 == 333


def test_program_entries_return_valid_constructions(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T043-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "19")
    from tasks.t043.init_program import run_code as init_run
    from tasks.t043.baseline import run_code as baseline_run
    from tasks.t043.human import run_code as human_run
    from tasks.t043.reference import run_code as reference_run
    from tasks.t043.evolution import run_code as evolution_run

    monkeypatch.setenv("MATHBENCH_SEARCH_ITERATIONS", "1")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_ITERATIONS", "1")
    for run in (init_run, baseline_run, human_run, reference_run, evolution_run):
        assert validate(run(), CONFIG)["verification_status"] == "exact"


def test_generation_worker_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T043 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T043 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
