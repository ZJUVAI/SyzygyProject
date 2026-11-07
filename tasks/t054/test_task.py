import json
import os
from pathlib import Path
import sys
import tempfile

import pytest

from mathbench.evaluate import _run
from tasks.t054 import baseline, check, evolution, human, init_program, reference


ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT / "tasks/t054/task.json").read_text())["configurations"][0]


def _independent_correlations(sequence):
    values = []
    for lag in range(1, len(sequence)):
        total = 0
        for i, left in enumerate(sequence):
            if i + lag < len(sequence):
                total += left * sequence[i + lag]
        values.append(total)
    return values


def test_human_reference_and_initial_sequence():
    human_result = human.run_code()
    reference_result = reference.run_code()
    initial = init_program.run_code()
    assert human_result == reference_result
    assert len(human_result["sequence"]) == 100
    correlations = _independent_correlations(human_result["sequence"])
    assert max(abs(value) for value in correlations) == 5
    checked = check.validate(human_result, CONFIG)
    assert checked["objective"] == 5
    assert checked["details"]["aperiodic_autocorrelations"] == correlations
    assert check.validate(initial, CONFIG)["objective"] == 99
    assert len(initial["sequence"]) == 100 and set(initial["sequence"]) == {1}


def test_baseline_and_evolution_are_deterministic_and_do_not_read_witnesses(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "17")
    monkeypatch.setenv("T054_SEARCH_RESTARTS", "2")
    monkeypatch.setenv("T054_SEARCH_ITERATIONS", "500")
    first = baseline.run_code()
    second = evolution.run_code()
    assert first == second
    assert first["search"]["reference_data_read"] is False
    assert check.validate(first, CONFIG)["verification_status"] == "exact"


def test_exact_flip_delta_matches_full_recomputation():
    sequence = [1 if (i * i + 3 * i + 1) % 5 < 2 else -1 for i in range(100)]
    correlations = check.aperiodic_autocorrelations(sequence)
    for position in (0, 1, 49, 98, 99):
        trial = sequence.copy()
        trial_corr = correlations.copy()
        deltas = baseline._flip(trial, trial_corr, position)
        assert trial_corr == check.aperiodic_autocorrelations(trial)
        trial[position] = -trial[position]
        for lag in range(1, len(sequence)):
            trial_corr[lag - 1] -= deltas[lag]
        assert trial_corr == correlations


@pytest.mark.parametrize("sequence", [None, [], [1] * 99, [1] * 101,
                                        [1] * 99 + [0], [1] * 99 + [2],
                                        [1] * 99 + [True], [1] * 99 + [1.0],
                                        [1] * 99 + [float("nan")]])
def test_rejects_invalid_sequence(sequence):
    with pytest.raises(ValueError):
        check.validate({"sequence": sequence}, CONFIG)


def test_repeated_signs_are_valid_and_have_expected_boundary_psl():
    checked = check.validate({"sequence": [1] * 100}, CONFIG)
    assert checked["objective"] == 99
    assert checked["details"]["aperiodic_autocorrelations"] == list(range(99, 0, -1))


def test_fixed_configuration_rejects_numeric_type_substitutions():
    for value in (100.0, True, 101):
        config = json.loads(json.dumps(CONFIG))
        config["parameters"]["length"] = value
        with pytest.raises(ValueError, match="configuration"):
            check.validate({"sequence": [1] * 100}, config)
    config = json.loads(json.dumps(CONFIG))
    config["parameters"]["alphabet"] = [True, 1]
    with pytest.raises(ValueError, match="configuration"):
        check.validate({"sequence": [1] * 100}, config)


def test_forged_objective_fields_do_not_change_validation():
    solution = {"sequence": [1] * 100}
    forged = {**solution, "objective": 0, "score": float("nan"), "claimed_score": 1e99}
    assert check.validate(forged, CONFIG) == check.validate(solution, CONFIG)


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


@pytest.mark.parametrize("config_index,length,hex_code", [(1,101,"1A5048216CCF18F83E910DD4C5"),(2,102,"2945A4F11CE44FF664850D182A")])
def test_added_public_configurations(monkeypatch, config_index, length, hex_code):
    configs=json.loads((ROOT / "tasks/t054/task.json").read_text())["configurations"]
    config=configs[config_index]; monkeypatch.setenv("MATHBENCH_CONFIG_ID",config["id"])
    witness=human.run_code(); replay=reference.run_code(); initial=init_program.run_code()
    assert witness==replay and len(witness["sequence"])==length
    bits=bin(int(hex_code,16))[2:].zfill(length)
    assert witness["sequence"]==[1 if b=="1" else -1 for b in bits]
    corr=_independent_correlations(witness["sequence"])
    assert max(map(abs,corr))==5
    assert check.validate(witness,config)["objective"]==5
    assert check.validate(initial,config)["objective"]==length-1
    with pytest.raises(ValueError): check.validate({"sequence":witness["sequence"][:-1]},config)

@pytest.mark.parametrize("config_id,length", [("T054-C01",100),("T054-C02",101),("T054-C03",102)])
def test_init_program_runs_as_cold_export(tmp_path, config_id, length):
    import subprocess
    import shutil
    exported = tmp_path / "init_program.py"
    shutil.copy(ROOT / "tasks/t054/init_program.py", exported)
    code = (
        "import importlib.util,json; "
        f"s=importlib.util.spec_from_file_location('candidate',{str(exported)!r}); "
        "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
        "print(json.dumps(m.run_code()))"
    )
    env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
    env["MATHBENCH_CONFIG_ID"] = config_id
    result = subprocess.run([sys.executable, "-I", "-c", code], cwd=tmp_path,
                            env=env, text=True, capture_output=True, check=True)
    candidate = json.loads(result.stdout)
    assert len(candidate["sequence"]) == length
    assert set(candidate["sequence"]) == {1}
