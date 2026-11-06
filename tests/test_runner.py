import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import pytest

from mathbench.evaluate import _run, evaluate_candidate
from mathbench.registry import ROOT


def test_worker_round_trip(tmp_path):
    config = tmp_path / "config.json"
    output = tmp_path / "solution.json"
    checked = tmp_path / "checked.json"
    config.write_text(json.dumps({"id": "example", "parameters": {"size": 3}}))
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONPATH=str(ROOT))
    common = [str(config), str(output), "0", "1", str(4 * 1024**3), "5"]
    _run([sys.executable, "-m", "mathbench.worker", "generate", str(ROOT / "tasks/_template/init_program.py"), *common], env, 10)
    assert json.loads(output.read_text()) == {"values": [1, 2, 3]}
    env["MATHBENCH_SOLUTION_PATH"] = str(output)
    _run([sys.executable, "-m", "mathbench.worker", "check", str(ROOT / "tasks/_template/check.py"), str(config), str(checked), "0", "1", str(4 * 1024**3), "5"], env, 10)
    assert json.loads(checked.read_text()) == {"objective": 6, "verification_status": "exact"}


def test_timeout():
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(10)"], os.environ.copy(), 0.1)


def test_setup_errors_are_results():
    result = evaluate_candidate("unknown", "missing.py")
    assert result["validity"] == 0
    assert result["combined_score"] == 0
    assert result["failed_phase"] == "setup"
