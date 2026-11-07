"""Command-line entry point."""
import argparse
import json
from .evaluate import evaluate_candidate
from .registry import INITIAL_TASKS, load_task, resolve_task_id


def resolve_task_argument(value):
    try:
        return resolve_task_id(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def main():
    parser = argparse.ArgumentParser(prog="mathbench")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    export = commands.add_parser("export-seed")
    export.add_argument("task", type=resolve_task_argument, metavar="TASK_ID")
    export.add_argument("destination")
    export.add_argument("--config")
    replay = commands.add_parser("replay")
    replay.add_argument("task", type=resolve_task_argument, metavar="TASK_ID")
    replay.add_argument("solution")
    replay.add_argument("--config")
    replay.add_argument("--output")
    run = commands.add_parser("evaluate")
    run.add_argument("task", type=resolve_task_argument, metavar="TASK_ID")
    run.add_argument("program")
    run.add_argument("--config")
    run.add_argument("--strict", action="store_true")
    run.add_argument("--seed", type=int, default=0)
    run.add_argument("--generation-timeout", type=float, default=300)
    run.add_argument("--verification-timeout", type=float, default=60)
    run.add_argument("--output")
    args = parser.parse_args()
    if args.command == "list":
        for task in INITIAL_TASKS:
            try:
                record = load_task(task)
                print(task, record.get("name", ""), record.get("acceptance_status", "pending_sol_review"))
            except FileNotFoundError:
                print(task, "not_implemented")
    elif args.command == "export-seed":
        from .export import export_seed
        print(export_seed(args.task, args.destination, args.config))
    elif args.command == "replay":
        from .replay import replay
        print(json.dumps(replay(args.task, args.solution, args.config, strict=True, output_dir=args.output), indent=2))
    else:
        print(json.dumps(evaluate_candidate(args.task, args.program, args.config,
              strict=args.strict, seed=args.seed, generation_timeout=args.generation_timeout,
              verification_timeout=args.verification_timeout, output_dir=args.output), indent=2))


if __name__ == "__main__":
    main()
