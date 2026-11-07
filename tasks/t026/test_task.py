import hashlib
import json
from pathlib import Path

import pytest

from tasks.t026.baseline import run_code as run_baseline
from tasks.t026.check import validate
from tasks.t026.evolution import run_code as run_evolution
from tasks.t026.human import run_code as run_human
from tasks.t026.init_program import run_code as run_init
from tasks.t026.reference import run_code as run_reference


ROOT = Path(__file__).parent
CONFIG = {"parameters": {"colors": 6}}


def _assert_invalid(solution):
    with pytest.raises(ValueError):
        validate(solution, CONFIG)


def test_simple_seed_human_witness_and_public_reference():
    assert validate(run_init(), CONFIG)["objective"] == 4
    human = run_human()
    assert validate(human, CONFIG)["objective"] == 536
    public = run_reference()
    assert validate(public, CONFIG)["objective"] == 537


def test_evolution_entry_point_directly_calls_the_task_baseline(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    result = run_evolution()
    assert result["n"] == 4
    assert validate(result, CONFIG)["objective"] == 4


def test_partition_schema_and_claimed_score_is_ignored():
    classes = [[1, 4], [2, 3]]
    assert validate({"n": 4, "classes": classes, "objective": 10**9}, CONFIG)["objective"] == 4
    assert validate({"n": 4, "colors": [0, 1, 1, 0], "score": -100}, CONFIG)["objective"] == 4


def test_rejects_monochromatic_schur_triples_including_equal_terms():
    # 1+1=2 must be detected even though the two addends are equal.
    _assert_invalid({"n": 2, "colors": [0, 0]})
    _assert_invalid({"n": 3, "colors": [0, 0, 0]})  # 1+2=3


@pytest.mark.parametrize("solution", [
    {"n": True, "colors": [0]},
    {"n": 2, "colors": [False, 1]},
    {"n": 2, "colors": [0, 1.0]},
    {"n": 2, "colors": [0, float("nan")]},
    {"n": 2, "colors": [0, float("inf")]},
    {"n": 3, "colors": [0, 1]},  # not a complete prefix
    {"n": 2, "colors": [0, 6]},
    {"n": 0, "colors": []},
    {"n": 4, "classes": [[1, 4], [2, 3], [3]]},  # duplicate class member
    {"n": 4, "classes": [[1, 4], [2]]},  # incomplete prefix
    {"n": 2, "colors": [0, 1], "classes": [[1], [2]]},
])
def test_rejects_malformed_solutions(solution):
    _assert_invalid(solution)


def test_baseline_is_deterministic_and_reports_replay_metadata(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "8128")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    first = run_baseline()
    second = run_baseline()
    assert first == second
    assert validate(first, CONFIG)["objective"] == first["n"]
    metadata = first["search_metadata"]
    assert metadata["seed"] == 8128
    assert metadata["placement_budget"] > 0
    assert metadata["reference_data_read"] is False


def test_zero_second_search_budget_returns_valid_simple_seed(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    result = run_baseline()
    assert result["search_metadata"]["placements"] == 0
    assert result["n"] == 4
    assert validate(result, CONFIG)["objective"] == 4


def test_pinned_certificate_matches_upstream_checksum():
    checksum_path = ROOT / "data" / "chen_zhu_long_SHA256SUMS"
    checksum_lines = checksum_path.read_text().splitlines()
    expected = next(line.split()[0] for line in checksum_lines if line.endswith(" certificate.col"))
    certificate_path = ROOT / "data" / "chen_zhu_long_537_certificate.col"
    actual = hashlib.sha256(certificate_path.read_bytes()).hexdigest()
    assert actual == expected
    manifest = json.loads((ROOT / "source_hashes.json").read_text())
    public_source = manifest["arxiv_2610_31362_v1"]
    assert public_source["repository_commit"] == "92a9d5f1336a5a064b2bfe6597d967f59191e365"
    assert public_source["certificate_sha256"] == actual
    checksum_digest = hashlib.sha256(checksum_path.read_bytes()).hexdigest()
    assert public_source["checksum_file_sha256"] == checksum_digest


def test_saved_human_source_and_transcription_hashes():
    manifest = json.loads((ROOT / "source_hashes.json").read_text())
    human_source = manifest["fredricksen_sweet_2000"]
    for relative_path, expected in [
        (human_source["local_file"], human_source["sha256"]),
        ("data/fredricksen_sweet_536_halfsets.json", human_source["transcribed_witness_sha256"]),
    ]:
        actual = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()
        assert actual == expected


def test_runner_reports_candidate_error_and_generation_timeout(monkeypatch, tmp_path):
    import mathbench.evaluate as runner

    monkeypatch.setattr(runner, "load_config", lambda task_id, config_id=None: {
        "id": "T026-C01",
        "direction": "maximize",
        "human_reference": 536,
        "parameters": {"colors": 6, "color_limit": "at most"},
    })
    monkeypatch.setattr(runner, "task_path", lambda task_id: ROOT)

    error_program = tmp_path / "error_candidate.py"
    error_program.write_text("def run_code():\n    raise RuntimeError('expected candidate failure')\n")
    failed = runner.evaluate_candidate("T026", error_program, "T026-C01", strict=True)
    assert failed["validity"] == 0
    assert failed["failed_phase"] == "generation"
    assert failed["error_category"] == "program_error"

    timeout_program = tmp_path / "timeout_candidate.py"
    timeout_program.write_text(
        "import time\ndef run_code():\n    time.sleep(5)\n    return {'n': 1, 'colors': [0]}\n"
    )
    timed_out = runner.evaluate_candidate(
        "T026", timeout_program, "T026-C01", strict=True, generation_timeout=0.5
    )
    assert timed_out["validity"] == 0
    assert timed_out["failed_phase"] == "generation"
    assert timed_out["error_category"] == "generation_timeout"
