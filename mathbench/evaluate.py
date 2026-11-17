"""Run candidate programs, then verify their data in a new process."""
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import time

from .construction import read_construction
from .process import run_process as _run
from .registry import ROOT, load_config, task_path
from .scoring import score_result


def evaluate_candidate(task_id, program_path, config_id=None, *, strict=False, seed=0,
                       generation_timeout=300, verification_timeout=60,
                       memory_bytes=4 * 1024**3, output_dir=None):
    start = time.monotonic()
    phase = "setup"
    result = {"task_id": task_id, "config_id": config_id, "validity": 0.0,
              "combined_score": 0.0, "objective": None, "verification_status": "failed"}
    try:
        config = load_config(task_id, config_id)
        if config["direction"] not in ("maximize", "minimize"):
            raise ValueError("Unknown objective direction")
        if type(seed) is not int:
            raise ValueError("Seed must be an integer")
        result["config_id"] = config["id"]
        program_path = Path(program_path).resolve(strict=True)
        if min(generation_timeout, verification_timeout, memory_bytes) <= 0:
            raise ValueError("Resource limits must be positive")
        env = dict(os.environ)
        env.update({key: "1" for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")})
        env["PYTHONPATH"] = str(ROOT)
        with tempfile.TemporaryDirectory(prefix="mathbench-") as folder:
            work = Path(folder)
            config_file = work / "config.json"
            config_file.write_text(json.dumps(config))
            solution_file, checked_file = work / "solution.json", work / "checked.json"
            def command(mode, module, output, timeout):
                return [sys.executable, "-m", "mathbench.worker", mode, str(module), str(config_file),
                        str(output), str(seed), str(int(strict)), str(memory_bytes), str(max(1, math.ceil(timeout)))]
            phase = "generation"
            phase_start = time.monotonic()
            _run(command("generate", program_path, solution_file, generation_timeout), env, generation_timeout)
            result["generation_time"] = time.monotonic() - phase_start
            if solution_file.stat().st_size > 16 * 1024**2:
                raise ValueError("Construction exceeds 16 MiB")
            solution = read_construction(solution_file)
            phase = "verification"
            phase_start = time.monotonic()
            env["MATHBENCH_SOLUTION_PATH"] = str(solution_file)
            _run(command("check", task_path(task_id) / "check.py", checked_file, verification_timeout), env, verification_timeout)
            result["verification_time"] = time.monotonic() - phase_start
            checked = json.loads(checked_file.read_text())
            result.update(score_result(checked, config, strict))
            if output_dir is not None:
                saved = Path(output_dir)
                saved.mkdir(parents=True, exist_ok=True)
                (saved / "solution.json").write_text(json.dumps(solution, allow_nan=False))
                (saved / "verification.json").write_text(json.dumps(checked, indent=2, allow_nan=False))
    except Exception as exc:
        result.update(error_type=type(exc).__name__, error=str(exc), failed_phase=phase)
        result["error_category"] = (phase + "_timeout" if isinstance(exc, TimeoutError)
                                    else {"setup": "setup_error", "generation": "program_error",
                                          "verification": "verification_failure"}[phase])
    result["eval_time"] = time.monotonic() - start
    result["seed"] = seed
    result["strict"] = strict
    result["budget"] = {"generation_seconds": generation_timeout, "verification_seconds": verification_timeout, "memory_bytes": memory_bytes, "threads": 1}
    result["environment"] = {"python": sys.version.split()[0], "platform": sys.platform,
                              "memory_limit_enforced": sys.platform != "darwin",
                              "worker_cpu": min(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None}
    if output_dir is not None:
        try:
            saved = Path(output_dir)
            saved.mkdir(parents=True, exist_ok=True)
            (saved / "result.json").write_text(json.dumps(result, indent=2, allow_nan=False))
        except Exception as exc:
            result["artifact_error"] = str(exc)
    return result
