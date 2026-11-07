"""Tests for the degree-100 Mahler measure task."""

import hashlib
import json
import os
from pathlib import Path
import sys
from fractions import Fraction

import pytest

from tasks.t063.check import PARAMETERS, _rat, validate

ROOT = Path(__file__).resolve().parent
CONFIG = {"id": "T063-C01", "parameters": PARAMETERS}


def test_pinned_public_witness_and_exact_measure_certificate():
    from tasks.t063.human import run_code as human_run

    path = ROOT / "data/reference/mossinghoff_degree_100_certificate.json"
    source = json.loads((ROOT / "data/source/mossinghoff_degree_100_row.json").read_text())
    witness = human_run()
    assert witness["coefficients_ascending"] == source["coefficients_ascending"]
    assert source["coefficients_descending"] == list(reversed(source["coefficients_ascending"]))
    assert source["coefficients_descending"][:51] == source["reciprocal_prefix_descending"]
    assert len(witness["root_disks"]) == 100
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "fb01470875be798525b061a301e401dffa3bab18c50de35d6816defda976afb3"
    )
    result = validate(witness, CONFIG, strict=True)
    assert result["verification_status"] == "certified"
    assert result["details"]["irreducible_over_Q"] is True
    assert result["details"]["root_disks_checked"] == 100
    assert result["details"]["pairwise_disjoint_checks"] == 4950
    assert result["details"]["outside_unit_circle_roots_certified"] == 8
    lower, upper = map(Fraction, result["details"]["objective_interval"])
    assert lower > 1
    assert upper >= lower
    assert (upper - lower) * 10**10 <= lower


def test_five_program_entries_return_valid_constructs(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T063-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("MATHBENCH_SEARCH_ITERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_ITERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_RESTARTS", "1")
    from tasks.t063.init_program import run_code as init_run
    from tasks.t063.baseline import run_code as baseline_run
    from tasks.t063.evolution import run_code as evolution_run
    from tasks.t063.human import run_code as human_run
    from tasks.t063.reference import run_code as reference_run

    init = init_run()
    baseline = baseline_run()
    evolution = evolution_run()
    human = human_run()
    reference = reference_run()
    for output in (init, baseline, evolution, human):
        checked = validate(output, CONFIG)
        assert checked["verification_status"] == "certified"
    assert reference == human
    assert baseline["coefficients_ascending"] == init["coefficients_ascending"]
    assert baseline["search_metadata"]["iterations_run"] == 2
    assert evolution["search_metadata"]["iterations_run"] == 2


def test_checker_rejects_bad_degree_coefficients_and_root_disks():
    from tasks.t063.init_program import run_code

    valid = run_code()
    with pytest.raises(ValueError, match="101 integers"):
        validate({**valid, "coefficients_ascending": [1, 2]}, CONFIG)
    with pytest.raises(ValueError, match="bool and floats"):
        bad = {**valid, "coefficients_ascending": list(valid["coefficients_ascending"])}
        bad["coefficients_ascending"][0] = True
        validate(bad, CONFIG)
    with pytest.raises(ValueError, match="bool and floats"):
        bad = {**valid, "coefficients_ascending": list(valid["coefficients_ascending"])}
        bad["coefficients_ascending"][0] = float("nan")
        validate(bad, CONFIG)
    with pytest.raises(ValueError, match="exact degree 100"):
        bad = {**valid, "coefficients_ascending": list(valid["coefficients_ascending"])}
        bad["coefficients_ascending"][-1] = 0
        validate(bad, CONFIG)
    with pytest.raises(ValueError, match="100 root disks"):
        validate({**valid, "root_disks": valid["root_disks"][:-1]}, CONFIG)
    with pytest.raises(ValueError, match="pairwise disjoint"):
        bad = {**valid, "root_disks": list(valid["root_disks"])}
        bad["root_disks"][1] = dict(bad["root_disks"][0])
        validate(bad, CONFIG)
    with pytest.raises(ValueError, match="configuration parameters do not match"):
        validate(valid, {"id": "T063-C01", "parameters": {**PARAMETERS, "degree": 99}})


def test_rational_root_certificate_precision_is_not_artificially_capped():
    large_integer = "9" * 5000
    assert _rat(large_integer + "/7", "large rational") == Fraction(int(large_integer), 7)


def test_claimed_objective_fields_do_not_change_verified_result():
    from tasks.t063.init_program import run_code

    valid = run_code()
    checked = validate(valid, CONFIG)
    for key, claim in (("objective", -100), ("score", float("nan")),
                       ("claimed_score", {"forged": True})):
        assert validate({**valid, key: claim}, CONFIG) == checked


def test_runner_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T063 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T063 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
