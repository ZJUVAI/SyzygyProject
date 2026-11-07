import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t035.check import validate
from tasks.t035.human import build_points


CONFIG = {"parameters": {"forbidden_convex_polygon_vertices": 7}}


def test_reconstructed_human_witness_is_exact_and_score_is_recomputed():
    candidate = build_points()
    assert len(candidate["points"]) == 32
    assert validate(candidate, CONFIG)["objective"] == 32
    candidate["claimed_objective"] = -1000
    assert validate(candidate, CONFIG)["objective"] == 32


def test_saved_witness_replays():
    candidate = json.loads((Path(__file__).parent / "data" / "human_witness.json").read_text())
    assert validate(candidate, CONFIG)["objective"] == 32


def test_simple_initial_program_is_legal():
    from tasks.t035.init_program import run_code

    assert validate(run_code(), CONFIG)["objective"] == 6


def test_convex_seven_points_are_rejected():
    # Seven points on a parabola are in convex position and in general position.
    with pytest.raises(ValueError, match="convex 7-gon"):
        validate({"points": [[x, x * x] for x in range(7)]}, CONFIG)


def test_duplicate_point_is_rejected():
    with pytest.raises(ValueError, match="distinct"):
        validate({"points": [[0, 0], [1, 1], [0, 0]]}, CONFIG)


def test_collinear_triple_is_rejected():
    with pytest.raises(ValueError, match="noncollinear"):
        validate({"points": [[0, 0], [1, 1], [2, 2]]}, CONFIG)


@pytest.mark.parametrize("bad", [True, float("nan"), float("inf"), "1/0", None])
def test_invalid_coordinate_values_are_rejected(bad):
    with pytest.raises(ValueError):
        validate({"points": [[bad, 0]]}, CONFIG)


def test_finite_float_coordinate_is_rejected_without_approximation():
    with pytest.raises(ValueError, match="integers or rational strings"):
        validate({"points": [[0.5, 0]]}, CONFIG)


def test_rational_coordinates_are_exact():
    points = [["0/1", "0/1"], ["1/1", "1/1"], ["2/1", "4/1"]]
    assert validate({"points": points}, CONFIG)["objective"] == 3


def test_empty_boundary_is_valid():
    assert validate({"points": []}, CONFIG)["objective"] == 0


def test_malformed_solution_is_rejected():
    with pytest.raises(ValueError):
        validate({"points": [[0, 1, 2]]}, CONFIG)


def test_human_run_code_entry_round_trips_through_worker(tmp_path):
    import os
    import sys
    from mathbench.evaluate import _run
    from mathbench.registry import ROOT

    config = tmp_path / "config.json"
    output = tmp_path / "solution.json"
    checked = tmp_path / "checked.json"
    config.write_text(json.dumps({"id": "T035-C01", "parameters": CONFIG["parameters"]}))
    env = dict(os.environ, PYTHONPATH=str(ROOT))
    common = [str(config), str(output), "0", "1", str(4 * 1024**3), "60"]
    _run([sys.executable, "-m", "mathbench.worker", "generate",
          str(ROOT / "tasks/t035/human.py"), *common], env, 300)
    env["MATHBENCH_SOLUTION_PATH"] = str(output)
    _run([sys.executable, "-m", "mathbench.worker", "check",
          str(ROOT / "tasks/t035/check.py"), str(config), str(checked),
          "0", "1", str(4 * 1024**3), "60"], env, 60)
    assert json.loads(checked.read_text())["objective"] == 32


def test_program_error_and_timeout_are_visible_to_python_runtime(tmp_path):
    from mathbench.evaluate import _run
    from mathbench.registry import ROOT

    config = tmp_path / "config.json"
    config.write_text(json.dumps({"id": "T035-C01", "parameters": {"forbidden_convex_polygon_vertices": 7}}))
    env = dict(os.environ, PYTHONPATH=str(ROOT))
    worker = [sys.executable, "-m", "mathbench.worker", "generate"]
    output = tmp_path / "output.json"
    common = [str(config), str(output),
              "0", "1", str(4 * 1024**3), "5"]
    broken = tmp_path / "broken_candidate.py"
    broken.write_text("def run_code():\n    raise RuntimeError('candidate failed')\n")
    try:
        with pytest.raises(Exception):
            _run([*worker, str(broken), *common], env, 10)
        slow = tmp_path / "slow_candidate.py"
        slow.write_text("import time\ndef run_code():\n    time.sleep(5)\n    return {}\n")
        with pytest.raises(TimeoutError):
            _run([*worker, str(slow), *common], env, 0.5)
    finally:
        broken.unlink(missing_ok=True)
        (tmp_path / "slow_candidate.py").unlink(missing_ok=True)
