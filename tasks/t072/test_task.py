"""Exact tests for T072-C01."""

import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t072.check import PARAMETERS, validate


ROOT = Path(__file__).resolve().parent
CONFIG = {"id": "T072-C01", "parameters": PARAMETERS}
SOURCE_SHA256 = "0cd52d3292fdef5a69e851e8c6d8c37c285666c6064377dc09e3c6cd7e0a58e4"
WITNESS_SHA256 = "21862735ba6d83cb1017b2c3cfad783d0fc039ba18d0ac85d45a7398240d7e25"


def _independent_counts(values):
    sums = set()
    products = set()
    for a in values:
        for b in values:
            sums.add(a + b)
            products.add(a * b)
    return len(sums), len(products)


def test_author_row_and_saved_witness_match_and_recompute_exactly():
    row_path = ROOT / "data/source/obryant_spp_n32_row_1005722.txt"
    witness_path = ROOT / "data/reference/obryant_n32_154.json"
    assert hashlib.sha256(row_path.read_bytes()).hexdigest() == SOURCE_SHA256
    assert hashlib.sha256(witness_path.read_bytes()).hexdigest() == WITNESS_SHA256
    row_values = [int(item) for item in row_path.read_text().strip().strip("{}").split(",")]
    witness = json.loads(witness_path.read_text(encoding="utf-8"))
    assert row_values == witness["elements"]
    assert len(row_values) == len(set(row_values)) == 32
    assert min(row_values) == 1
    assert _independent_counts(row_values) == (154, 154)


def test_human_reference_and_checker_replay_public_witness():
    from tasks.t072.human import run_code as human_run
    from tasks.t072.reference import run_code as reference_run

    human = human_run()
    reference = reference_run()
    assert human == reference
    result = validate(human, CONFIG, strict=True)
    sums, products = _independent_counts(human["elements"])
    assert result["objective"] == 154
    assert result["details"]["sumset_size"] == sums == 154
    assert result["details"]["product_set_size"] == products == 154


def test_all_five_program_entries_return_valid_sets(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T072-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "4")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    monkeypatch.setenv("MATHBENCH_BASELINE_ITERATIONS", "8")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_ITERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_POPULATION", "2")
    from tasks.t072.init_program import run_code as initial
    from tasks.t072.baseline import run_code as baseline
    from tasks.t072.evolution import run_code as evolution
    from tasks.t072.human import run_code as human
    from tasks.t072.reference import run_code as reference

    outputs = [initial(), baseline(), evolution(), human(), reference()]
    values = [validate(item, CONFIG, strict=True)["objective"] for item in outputs]
    assert len(outputs[0]["elements"]) == 32
    assert values[0] == max(_independent_counts(outputs[0]["elements"]))
    assert values[1] >= 1 and values[2] >= 1
    assert outputs[1]["search_metadata"]["iterations_run"] == 8
    assert outputs[2]["search_metadata"]["generations_run"] == 2
    assert values[3:] == [154, 154]


def test_checker_rejects_wrong_cardinality_duplicates_and_invalid_types():
    valid = list(range(1, 33))
    for invalid in (True, 1.0, float("nan"), float("inf"), None, "4"):
        candidate = valid.copy()
        candidate[0] = invalid
        with pytest.raises(ValueError):
            validate({"elements": candidate}, CONFIG)
    with pytest.raises(ValueError, match="exactly 32"):
        validate({"elements": valid[:-1]}, CONFIG)
    with pytest.raises(ValueError, match="distinct"):
        validate({"elements": [*valid[:-1], valid[0]]}, CONFIG)
    for bad in (0, -1):
        candidate = valid.copy()
        candidate[0] = bad
        with pytest.raises(ValueError, match="positive"):
            validate({"elements": candidate}, CONFIG)
    with pytest.raises(ValueError, match="configuration must fix"):
        validate({"elements": valid}, {"id": "T072-C01", "parameters": {**PARAMETERS, "cardinality": 31}})


def test_arbitrary_precision_values_are_unbounded_and_exact():
    huge = 10**500
    values = [huge + i * (10**250 + 7) for i in range(32)]
    result = validate({"elements": values}, CONFIG, strict=True)
    sums, products = _independent_counts(values)
    assert result["verification_status"] == "exact"
    assert result["objective"] == max(sums, products)
    assert result["details"]["sumset_size"] == sums
    assert result["details"]["product_set_size"] == products


def test_claimed_scores_do_not_change_recomputed_result():
    from tasks.t072.init_program import run_code

    candidate = run_code()
    expected = validate(candidate, CONFIG)
    for key, value in (("objective", 1), ("score", float("nan")), ("claimed_score", {"fake": True})):
        assert validate({**candidate, key: value}, CONFIG) == expected


def test_records_distinguish_reproduced_record_from_optimality():
    sota = json.loads((ROOT / "sota.json").read_text())
    records = json.loads((ROOT / "records.json").read_text())
    item = sota["configurations"]["T072-C01"]
    assert item["reproduced_value"] == item["public_value"] == 154
    assert "not a proved optimum" in item["highest_reported"]["reproduction_status"]
    assert records["configurations"]["T072-C01"]["frozen_human_baseline"]["value"] == 154
    assert records["configurations"]["T072-C01"]["optimality_status"]["status"] == "open"


def test_runner_reports_program_error_and_timeout():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T072 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T072 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
