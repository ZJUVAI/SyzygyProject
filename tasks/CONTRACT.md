# Task implementation contract

The main reviewer owns shared code. A task agent edits only `tasks/<lowercase-id>/`.

Required files: `task.json`, `README.md` (Chinese and English), `instruction.txt` (English model prompt), `check.py`, `evaluator.py`, `init_program.py`, `baseline.py`, `evolution.py`, `human.py`, `reference.py`, `sota.json`, `records.json`, `test_task.py`. Save comparison constructions under `data/`, `data/source/`, or `data/reference/`. Keep `best/` for the task's own search results. Reference programs must not read comparison files from `best/`.

`evolution.py` must expose `run_code()` for the shared search runner. It may import the task's baseline with a task-qualified import. Test this entry directly. A checker-only helper does not satisfy this entry. The exported `init_program.py` must work without importing task modules from the source checkout. Public input files may be exported by the main reviewer's explicit whitelist; comparison witnesses and normalization records must not enter that workspace.

`task.json`: `task_id`, `name`, `acceptance_status: "pending_sol_review"`, and `configurations` (list). Each config has `id` (task ID plus a consecutive C01 suffix), `parameters`, `direction` (`minimize` or `maximize`), `human_reference` (positive JSON number). Version 1.0 has 100 tasks and 139 accepted configurations. Selection and research conclusions are in `PLAN.md`. Use only the configurations assigned for implementation. A planned configuration must pass review before it enters the release registry. Do not copy an existing acceptance status to a new configuration. Each task has at most five selected configurations. T016 selects 208 steps, C01. T003 has C01/C02/C03 for 26/32/40 circles.

New configurations must have `acceptance_status: "pending_sol_review"`. The release registry excludes them until independent admission changes this field to `accepted_by_sol`. Existing configurations without a configuration-level status retain their recorded acceptance. Admission tools can inspect pending configurations in their own process.

Each of the five programs defines `run_code()` with no arguments and returns JSON data (numpy arrays and sets are supported). Test the human and reference entries too. Read the chosen configuration from `MATHBENCH_CONFIG_ID` and seed from `MATHBENCH_SEED`. Use paired EVOLVE-BLOCK markers in init_program.py. The simple seed and search baseline must not read human/reference witness files. Reference programs may read task-local data via `Path(__file__)`. All scripts need deterministic defaults and bounded search. Use fixed iteration counts by default. Explicit `MATHBENCH_SEARCH_SECONDS` may set an exploration cutoff. Do not import other task packages.

`check.py` exports `validate(solution, config, strict=False)`. Raise ValueError for invalid data. Return `{"objective": <int, finite float, or fraction string>, "verification_status": "exact"|"certified"|"numeric", "details": {...}}`. Never use a claimed score. Validate every constraint, sizes and element types. Reject bool where integer is required, NaN, infinity and duplicate objects when duplicates invalidate the construction. Numeric float coefficients can be interpreted as exact binary rationals with Fraction for strict checks. Strict checks must establish full-domain feasibility and a conservative score, or fail; no sampling certificates.

The complete validation result must stay unchanged when optional `objective`, `score`, or `claimed_score` fields are changed. Do not set a mismatch flag or change an ignored-score flag based on the presence of those fields. A fixed `claimed_objective_ignored: true` flag is valid.

`evaluator.py`: import `evaluate_candidate` from `mathbench.evaluate`; define `evaluate(program_path, config_id=None, **kwargs)` returning `evaluate_candidate("Txxx", program_path, config_id, **kwargs)`.

The shared runner uses a fresh generation subprocess, then a separate trusted verification subprocess. Default limits: generation 300 seconds, verification 60 seconds, 4 GiB virtual memory, one numerical thread. Candidate output is capped at 16 MiB. Raw objectives are primary; compatibility score is J/H for maximize or H/J for minimize, invalid score 0. The runner is a local resource limiter, not a security container.

Human baselines need public provenance and a reproduced witness. Do not invent attribution or claim a self-created weak example is the published record. `records.json` separates `best_human`, `best_public`, `best_reproduced` with dates, parameters, URLs, AI provenance, actual values and evidence state. Missing best-public witnesses do not block release; missing reproduced human baseline does. Never say world-best without specifying sources checked and snapshot date.

Both `sota.json` and `records.json` use a `configurations` object keyed by configuration ID. Each SOTA configuration has `program: "reference.py"`, scalar `reproduced_value`, scalar `public_value` when known, and a `highest_reported` object with `value`, source, and `reproduction_status`. Keep extra details in separate objects. A weak frozen human baseline can differ from the best reported human result; record both. Recompute each parameter's construction and score.

Test valid and invalid examples, boundary constraints, ignored claimed scores, and independent score calculations. Submit actual test commands and results, source checks, and unresolved issues in `IMPLEMENTATION.md`. Your status remains pending_sol_review. The main reviewer decides acceptance.

Before registration, test runner errors and timeouts through `mathbench.evaluate._run`, or use a temporary registry patch inside the test. A missing task ID in a separate process is expected until Sol admission; do not edit the shared registry or wait for a permanent registration to test these controls.

Use `.venv/bin/python` (Python 3.13 with pytest and science libraries) for validation. The system `python3` is old. Test imports must be task-qualified, e.g. `from tasks.t013.check import validate`, not `from check import validate`, so all 73 task suites can run together without module-name collisions. Program-local imports are supported by the worker. Do not import sibling task data.

For an exact algebraic objective, the trusted checker may return the exact expression in `objective` and a rational string in `objective_value` for numeric feedback. This must be a conservative bound (upper for minimize, lower for maximize). Include a rigorously established `details.objective_interval`; the candidate's own numeric claims remain ignored. T002 implements this for Q(sqrt(2)) with integer-square-root bounds.

Search baseline amendment: defaults use fixed iteration counts and the saved random seed. `mathbench.search.search_steps` supplies this mode. Explicit `MATHBENCH_SEARCH_SECONDS` enables a wall-clock cutoff for exploration; its result can depend on machine speed. Hard runner limits apply in both modes.
