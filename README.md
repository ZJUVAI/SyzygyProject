# SyzygyProject v1.0

A benchmark for mathematical constructions with 100 tasks and one official configuration per task.

- `tasks/` contains task definitions, checkers, baselines, public result records, and saved constructions.
- `mathbench/` contains the runner and evaluation tools.
- `scripts/` contains search, audit, reporting, and website update commands.

## Setup

Use Python 3.11 or later on Linux or macOS.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
```

## Run and verify

```sh
python -m mathbench list
python scripts/search.py run T013
python scripts/search.py resume
python scripts/search.py audit
python scripts/result_table.py --highlight-best
python -m pytest tests tasks -q
```

The runner saves temporary results in each task's `runs/` directory. To replay a saved construction, pass its task and configuration IDs.

```sh
python -m mathbench replay T003 tasks/t003/best/T003-C01/solution.json --config T003-C01
```

Some search programs require a C++17 compiler (`g++`). Replay of a saved JSON construction uses Python. Linux applies a 4 GiB address-space limit to workers. On macOS, the runner records that this limit is disabled.

See the [task interface](tasks/CONTRACT.md) and [repository guidelines](AGENTS.md).
