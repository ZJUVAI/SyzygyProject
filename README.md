# SyzygyProject v1.0

A benchmark for mathematical constructions with 100 tasks and one official configuration per task.

- `tasks/` contains one package per task.
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

Each task's `task.json` holds its one official configuration. Its top level contains the runner entry points, checker, and tests. `data/` holds inputs, comparison constructions, source records, and implementation notes. `data/best/result.json` stores the score, provenance, and saved construction in one file. Larger records use `result.json.gz`. Seeded search evidence is in `data/search/`.

The runner saves temporary results in each task's `runs/` directory. To replay a saved construction, pass its task and witness path.

```sh
python -m mathbench replay T003 tasks/t003/data/best/result.json
```

Some search programs require a C++17 compiler (`g++`). Replay of a saved JSON construction uses Python. Linux applies a 4 GiB address-space limit to workers. On macOS, the runner records that this limit is disabled.

See the [task interface](tasks/CONTRACT.md) and [repository guidelines](AGENTS.md).
