"""Exact tests for T070-C01."""

import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t070.check import PARAMETERS, validate
from tasks.t070.construction import parse_published_sizes, skyline_decode


ROOT = Path(__file__).resolve().parent
CONFIG = {"id": "T070-C01", "parameters": PARAMETERS}
WITNESS_SHA256 = "237d543109959c8939d22f98e91832d3bda47603cfe243f19a6e7beee0c7bfee"
SOURCE_ROW_SHA256 = "011cbfe1a1933cf20ba51f78f4c721ca447636bc4e52d8ea1255b7cb92a5e880"


def _independent_pairwise_check(squares):
    area = 0
    side_gcd = 0
    pairs = 0
    for i, (x1, y1, s1) in enumerate(squares):
        area += s1 * s1
        side_gcd = __import__("math").gcd(side_gcd, s1)
        for x2, y2, s2 in squares[:i]:
            assert max(x1, x2) >= min(x1 + s1, x2 + s2) or max(y1, y2) >= min(y1 + s1, y2 + s2)
            pairs += 1
    return area, side_gcd, pairs


def test_source_row_decodes_exactly_to_saved_skyline_witness():
    row_path = ROOT / "data/source/pegg_2017_row_1000.txt"
    witness_path = ROOT / "data/reference/pegg_1000_27.json"
    assert hashlib.sha256(row_path.read_bytes()).hexdigest() == SOURCE_ROW_SHA256
    assert hashlib.sha256(witness_path.read_bytes()).hexdigest() == WITNESS_SHA256
    sizes = parse_published_sizes(row_path)
    assert len(sizes) == 27
    assert sizes == [352, 312, 336, 40, 248, 24, 360, 184, 208, 160, 24, 107, 181,
                     192, 33, 74, 115, 41, 4, 56, 304, 37, 74, 4, 259, 248, 189]
    reconstructed = skyline_decode(sizes)
    saved = json.loads(witness_path.read_text(encoding="utf-8"))
    assert reconstructed == saved


def test_published_human_and_reference_witness_exactly_replay():
    from tasks.t070.human import run_code as human_run
    from tasks.t070.reference import run_code as reference_run

    witness = human_run()
    assert reference_run() == witness
    checked = validate(witness, CONFIG, strict=True)
    area, side_gcd, pairs = _independent_pairwise_check(witness["squares"])
    assert checked["objective"] == len(witness["squares"]) == 27
    assert checked["details"]["total_tile_area"] == area == 1_000_000
    assert checked["details"]["tile_side_gcd"] == side_gcd == 1
    assert checked["details"]["covered_area"] == 1_000_000
    assert pairs == 27 * 26 // 2


def test_all_five_entries_return_valid_candidates(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T070-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "4")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    monkeypatch.setenv("MATHBENCH_EVOLUTION_ITERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_POPULATION", "2")
    from tasks.t070.init_program import run_code as initial
    from tasks.t070.baseline import run_code as baseline
    from tasks.t070.evolution import run_code as evolution
    from tasks.t070.human import run_code as human
    from tasks.t070.reference import run_code as reference

    results = [initial(), baseline(), evolution(), human(), reference()]
    values = [validate(result, CONFIG, strict=True)["objective"] for result in results]
    assert values[0] == 2000
    assert values[1] == 299
    assert values[2] >= 1
    assert values[3:] == [27, 27]
    assert results[1]["search_metadata"]["candidates_checked"] == len(results[1]["search_metadata"]["candidate_block_counts"])
    assert results[2]["search_metadata"]["generations_run"] == 2


def test_checker_accepts_small_tiles_and_repeated_sizes_from_witness():
    witness = json.loads((ROOT / "data/reference/pegg_1000_27.json").read_text())
    assert witness["squares"].count([640, 312, 24]) == 1
    assert len([s for _, _, s in witness["squares"] if s == 24]) >= 2
    assert validate(witness, CONFIG)["objective"] == 27


def test_checker_rejects_overlap_gap_and_non_coprime_sides():
    witness = json.loads((ROOT / "data/reference/pegg_1000_27.json").read_text())
    duplicate = [list(square) for square in witness["squares"]]
    duplicate.append(list(duplicate[0]))
    with pytest.raises(ValueError, match="duplicate"):
        validate({"squares": duplicate}, CONFIG)

    overlap = [list(square) for square in witness["squares"]]
    overlap[1] = [300, 0, overlap[1][2]]
    with pytest.raises(ValueError, match="overlaps"):
        validate({"squares": overlap}, CONFIG)

    with pytest.raises(ValueError, match="sum exactly"):
        validate({"squares": witness["squares"][:-1]}, CONFIG)

    four_half_squares = {"squares": [[0, 0, 500], [500, 0, 500],
                                     [0, 500, 500], [500, 500, 500]]}
    with pytest.raises(ValueError, match="greatest common divisor 1"):
        validate(four_half_squares, CONFIG)


def test_checker_rejects_bad_shape_types_bounds_and_config():
    for invalid in (True, 1.0, float("nan"), float("inf"), None):
        with pytest.raises(ValueError):
            validate({"squares": [[0, 0, invalid]]}, CONFIG)
    with pytest.raises(ValueError, match="triple"):
        validate({"squares": [[0, 0]]}, CONFIG)
    with pytest.raises(ValueError, match="integers"):
        validate({"squares": [[False, 0, 1000]]}, CONFIG)
    for bad_square in ([[-1, 0, 1]], [[0, -1, 1]], [[1000, 0, 1]], [[0, 1000, 1]]):
        with pytest.raises(ValueError, match="outside"):
            validate({"squares": bad_square}, CONFIG)
    with pytest.raises(ValueError, match="side must"):
        validate({"squares": [[0, 0, 1000]]}, CONFIG)
    with pytest.raises(ValueError, match="at least one"):
        validate({"squares": []}, CONFIG)
    with pytest.raises(ValueError, match="configuration must fix"):
        validate({"squares": []}, {"id": "T070-C01", "parameters": {**PARAMETERS, "outer_side": 999}})


def test_claimed_scores_do_not_change_recomputed_result():
    from tasks.t070.init_program import run_code

    valid = run_code()
    result = validate(valid, CONFIG)
    for key, value in (("objective", 1), ("score", float("nan")),
                       ("claimed_score", {"forged": True})):
        assert validate({**valid, key: value}, CONFIG) == result


def test_record_separates_reproduced_27_from_optimality():
    sota = json.loads((ROOT / "sota.json").read_text())
    records = json.loads((ROOT / "records.json").read_text())
    item = sota["configurations"]["T070-C01"]
    assert item["public_value"] == item["reproduced_value"] == 27
    assert item["optimality_status"]["status"].startswith("open")
    assert records["configurations"]["T070-C01"]["frozen_human_baseline"]["value"] == 27


def test_runner_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T070 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T070 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
