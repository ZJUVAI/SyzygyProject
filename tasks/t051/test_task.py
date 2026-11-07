import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

import pytest

from mathbench.evaluate import _run
from tasks.t051 import baseline, check, evolution, human, init_program, reference


ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT / "tasks/t051/task.json").read_text())["configurations"][0]


def _independent_discrepancy(sequence):
    maximum = 0
    count = 0
    for d in range(1, len(sequence) + 1):
        partial = 0
        for index in range(d - 1, len(sequence), d):
            partial += sequence[index]
            maximum = max(maximum, abs(partial))
            count += 1
    return maximum, count


def test_all_five_program_entries_and_reference_witness(monkeypatch):
    programs = [init_program.run_code, baseline.run_code, evolution.run_code,
                human.run_code, reference.run_code]
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("T051_SEARCH_TRIALS", "2")
    monkeypatch.setenv("T051_SEARCH_LIMIT", "300")
    results = [program() for program in programs]
    for result in results:
        checked = check.validate(result, CONFIG)
        assert checked["verification_status"] == "exact"
        assert checked["details"]["claimed_objective_ignored"] is True
    assert len(results[0]["sequence"]) == 1
    assert results[1]["search"]["reference_data_read"] is False
    assert results[2]["search"]["reference_data_read"] is False
    assert results[3] == results[4]
    assert len(results[4]["sequence"]) == 130000
    maximum, prefix_count = _independent_discrepancy(results[4]["sequence"])
    assert maximum == 3
    validated = check.validate(results[4], CONFIG)
    assert validated["objective"] == 130000
    assert validated["details"]["homogeneous_progression_prefixes_checked"] == prefix_count
    assert validated["details"]["discrepancy"] == maximum
    witness = ROOT / "tasks/t051/data/source/sequence_130000.txt"
    assert hashlib.sha256(witness.read_bytes()).hexdigest() == (
        "024af56550adebd499df5c4e857453f518655e7e175af6e8d8a017e047f754c2"
    )


@pytest.mark.parametrize("sequence", [[], [0], [2], [1.0], [float("nan")], [True], ["+"], None])
def test_rejects_malformed_sequence(sequence):
    with pytest.raises(ValueError):
        check.validate({"sequence": sequence}, CONFIG)


def test_rejects_discrepancy_four_and_invalid_configuration():
    with pytest.raises(ValueError, match="discrepancy exceeds"):
        check.validate({"sequence": [1, 1, 1, 1]}, CONFIG)
    bad_config = json.loads(json.dumps(CONFIG))
    bad_config["parameters"]["discrepancy_cap"] = 2
    with pytest.raises(ValueError, match="configuration"):
        check.validate({"sequence": [1]}, bad_config)
    for invalid in (3.0, True):
        bad_config = json.loads(json.dumps(CONFIG))
        bad_config["parameters"]["discrepancy_cap"] = invalid
        with pytest.raises(ValueError, match="configuration"):
            check.validate({"sequence": [1]}, bad_config)
    bad_config = json.loads(json.dumps(CONFIG))
    bad_config["parameters"]["entry_domain"] = [True, -1]
    with pytest.raises(ValueError, match="configuration"):
        check.validate({"sequence": [1]}, bad_config)


def test_claimed_scores_do_not_change_complete_validation():
    base = {"sequence": [1, -1, 1]}
    forged = {**base, "objective": -1000, "score": float("nan"), "claimed_score": 1e99}
    assert check.validate(forged, CONFIG) == check.validate(base, CONFIG)


def test_runner_error_and_timeout_controls():
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    with tempfile.TemporaryDirectory() as folder:
        fail = Path(folder) / "fail.py"
        fail.write_text("raise RuntimeError('intentional worker failure')\n")
        with pytest.raises(RuntimeError, match="intentional worker failure"):
            _run([sys.executable, str(fail)], env, timeout=3)
        hang = Path(folder) / "hang.py"
        hang.write_text("import time\ntime.sleep(10)\n")
        with pytest.raises(TimeoutError, match="Wall time limit"):
            _run([sys.executable, str(hang)], env, timeout=1)
