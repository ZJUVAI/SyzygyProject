"""Run release checks. Only the main reviewer may promote task status."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench.evaluate import evaluate_candidate
from mathbench.registry import INITIAL_TASKS, load_task, task_path


REQUIRED = ["task.json", "README.md", "instruction.txt", "check.py", "evaluator.py", "init_program.py", "baseline.py", "human.py", "reference.py", "records.json", "test_task.py", "IMPLEMENTATION.md"]


def review(task_id, destination):
    folder = task_path(task_id)
    report = {"task_id": task_id, "reviewer": "main_agent", "date": "2026-11-04", "status": "pending_sol_review"}
    report["missing_files"] = [f for f in REQUIRED if not (folder / f).is_file()]
    if report["missing_files"]:
        return report
    task = load_task(task_id)
    proc = subprocess.run([sys.executable, "-m", "pytest", str(folder), "-q"], cwd=ROOT, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    report["tests"] = {"passed": proc.returncode == 0, "output": proc.stdout[-6000:]}
    runs = []
    for config in task["configurations"]:
        for name in ("init_program", "baseline", "human", "reference"):
            path = folder / (name + ".py")
            target = destination / task_id / config["id"] / name
            result = evaluate_candidate(task_id, path, config["id"], strict=True, output_dir=target)
            result["program"] = name
            runs.append(result)
            print(task_id, config["id"], name, result["validity"], result["objective"], flush=True)
    report["runs"] = runs
    report["automated_checks_passed"] = report["tests"]["passed"] and all(r["validity"] == 1 for r in runs)
    report["requires_manual_review"] = ["independent mathematical score check", "invalid construction rejection", "human provenance", "cold-start data access", "best-public versus reproduced record"]
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks", nargs="*", choices=INITIAL_TASKS)
    parser.add_argument("--output", default="runs/review")
    args = parser.parse_args()
    destination = (ROOT / args.output).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    reports = []
    for task_id in args.tasks or INITIAL_TASKS:
        try:
            record = review(task_id, destination)
        except Exception as exc:
            record = {"task_id": task_id, "status": "pending_sol_review", "error": str(exc)}
        reports.append(record)
        (destination / "review.json").write_text(json.dumps(reports, ensure_ascii=False, indent=2) + "\n")
    print("Automated results saved. No task was automatically accepted.")


if __name__ == "__main__":
    main()
