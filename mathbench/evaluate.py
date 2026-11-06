"""Run candidate programs, then verify their data in a new process."""
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from fractions import Fraction

from .registry import ROOT, load_config, task_path


def _finite_data(value):
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, float) and not math.isfinite(item):
            raise ValueError("Non-finite construction data")
        if isinstance(item, dict):
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)


def _run(args, env, timeout):
    with tempfile.TemporaryFile() as errors:
        proc = subprocess.Popen(args, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.DEVNULL, stderr=errors, start_new_session=True)
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            raise TimeoutError("Wall time limit exceeded")
        finally:
            # Stop descendants even when the immediate child has exited.
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if proc.returncode:
            errors.seek(0)
            message = errors.read(8192).decode(errors="replace")
            raise RuntimeError(message[-3000:] or "Worker failed")


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
            # Decode here too. Reject non-finite numbers before trusted verification.
            solution = json.loads(solution_file.read_text(), parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Non-finite JSON")))
            _finite_data(solution)
            phase = "verification"
            phase_start = time.monotonic()
            env["MATHBENCH_SOLUTION_PATH"] = str(solution_file)
            _run(command("check", task_path(task_id) / "check.py", checked_file, verification_timeout), env, verification_timeout)
            result["verification_time"] = time.monotonic() - phase_start
            checked = json.loads(checked_file.read_text())
            objective = checked["objective"]
            numeric = checked.get("objective_value", objective)
            score_value = float(Fraction(numeric)) if isinstance(numeric, str) else float(numeric)
            if not math.isfinite(score_value) or score_value < 0:
                raise ValueError("Objective must be finite and nonnegative")
            reference = float(config["human_reference"])
            if not math.isfinite(reference) or reference <= 0:
                raise ValueError("Positive frozen human reference required")
            score = score_value / reference if config["direction"] == "maximize" else reference / score_value
            if not math.isfinite(score):
                raise ValueError("Non-finite score")
            certification = checked.get("verification_status", "numeric")
            if certification not in ("exact", "certified", "numeric"):
                raise ValueError("Unknown verification status")
            if strict and certification not in ("exact", "certified"):
                raise ValueError("Strict verification requires a certificate")
            result.update(validity=1.0, combined_score=score, objective=objective, objective_value=numeric,
                          verification_status=certification, details=checked.get("details", {}))
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
