# Task implementation contract

The main reviewer owns shared code. A task agent edits only `tasks/<lowercase-id>/`.

Required files: `task.json`, `README.md` (Chinese and English), `instruction.txt` (English model prompt), `check.py`, `evaluator.py`, `init_program.py`, `baseline.py`, `evolution.py`, `human.py`, `reference.py`, `test_task.py`, `data/bestknown.json`, and `data/results.json` (or `data/results.json.gz`). Save comparison constructions under `data/`. Reference programs must read comparison files from `data/`.

`evolution.py` must expose `run_code()` for the shared search runner. It may import the task's baseline with a task-qualified import. Test this entry directly. A checker-only helper does not satisfy this entry. The exported `init_program.py` must work without importing task modules from the source checkout. Public input files may be exported by the main reviewer's explicit whitelist; comparison witnesses and normalization records must not enter that workspace.

`task.json` contains `task_id`, `name`, `acceptance_status`, `official_configuration`, and a `configurations` list with one released configuration. A configuration has `id`, `parameters`, `direction` (`minimize` or `maximize`), and `human_reference` (positive JSON number). The release has 100 official configurations. The T002 release uses C02 for 32 circles. A draft uses `pending_sol_review` until it passes review.

The `PLAN.md` references in historical task records refer to the file in commit `942361fbd22f6abe0eefa4d18b611bc6552d3b6f`.

New configurations must have `acceptance_status: "pending_sol_review"`. The release registry excludes them until independent admission changes this field to `accepted_by_sol`. Existing configurations without a configuration-level status retain their recorded acceptance. Admission tools can inspect pending configurations in their own process.

Each of the five programs defines `run_code()` with no arguments and returns JSON data (numpy arrays and sets are supported). Test the human and reference entries too. Read the chosen configuration from `MATHBENCH_CONFIG_ID` and seed from `MATHBENCH_SEED`. Use paired EVOLVE-BLOCK markers in init_program.py. The simple seed and search baseline must not read human/reference witness files. Reference programs may read task-local data via `Path(__file__)`. All scripts need deterministic defaults and bounded search. Use fixed iteration counts by default. Explicit `MATHBENCH_SEARCH_SECONDS` may set an exploration cutoff. Do not import other task packages.

`check.py` exports `validate(solution, config, strict=False)`. Raise ValueError for invalid data. Return `{"objective": <int, finite float, or fraction string>, "verification_status": "exact"|"certified"|"numeric", "details": {...}}`. Never use a claimed score. Validate every constraint, sizes and element types. Reject bool where integer is required, NaN, infinity and duplicate objects when duplicates invalidate the construction. Numeric float coefficients can be interpreted as exact binary rationals with Fraction for strict checks. Strict checks must establish full-domain feasibility and a conservative score, or fail; no sampling certificates.

The complete validation result must stay unchanged when optional `objective`, `score`, or `claimed_score` fields are changed. Do not set a mismatch flag or change an ignored-score flag based on the presence of those fields. A fixed `claimed_objective_ignored: true` flag is valid.

`evaluator.py`: import `evaluate_candidate` from `mathbench.evaluate`; define `evaluate(program_path, config_id=None, **kwargs)` returning `evaluate_candidate("Txxx", program_path, config_id, **kwargs)`.

The shared runner uses a fresh generation subprocess, then a separate trusted verification subprocess. Default limits: generation 300 seconds, verification 60 seconds, 4 GiB virtual memory, one numerical thread. Candidate output is capped at 16 MiB. Raw objectives are primary; compatibility score is J/H for maximize or H/J for minimize, invalid score 0. The runner is a local resource limiter, not a security container.

Human baselines need public provenance and a reproduced witness. `data/bestknown.json` separates `best_human`, `best_public`, `best_reproduced` with dates, parameters, URLs, AI provenance, values and evidence state. A task requires a reproduced human baseline for release. Identify source scope and date for best-result claims.

`data/bestknown.json` uses a `configurations` object keyed by configuration ID. Each SOTA configuration has `program: "reference.py"`, scalar `reproduced_value`, scalar `public_value` when known, and a `highest_reported` object with `value`, source, and `reproduction_status`. Record the frozen human baseline and the best reported human result. Recompute each configuration's construction and score.

Test valid and invalid examples, boundary constraints, ignored claimed scores, and independent score calculations. Record test commands and results, source checks, and unresolved issues in `data/IMPLEMENTATION.md`. Your status remains pending_sol_review. The main reviewer decides acceptance.

Before registration, test runner errors and timeouts through `mathbench.evaluate._run`, or use a temporary registry patch inside the test. A missing task ID in a separate process is expected until Sol admission; do not edit the shared registry or wait for a permanent registration to test these controls.

Use `.venv/bin/python` (Python 3.13 with pytest and science libraries) for validation. The system `python3` is old. Test imports must be task-qualified, e.g. `from tasks.t073.check import validate`, not `from check import validate`, so all 73 task suites can run together without module-name collisions. Program-local imports are supported by the worker. Do not import sibling task data.

For an exact algebraic objective, the trusted checker may return the exact expression in `objective` and a rational string in `objective_value` for numeric feedback. This must be a conservative bound (upper for minimize, lower for maximize). Include a rigorously established `details.objective_interval`; the candidate's own numeric claims remain ignored. T003 implements this for Q(sqrt(2)) with integer-square-root bounds.

Search baseline amendment: defaults use fixed iteration counts and the saved random seed. `mathbench.search.search_steps` supplies this mode. Explicit `MATHBENCH_SEARCH_SECONDS` enables a wall-clock cutoff for exploration; its result can depend on machine speed. Hard runner limits apply in both modes.

The official result uses `data/results.json`, or `data/results.json.gz` for a compressed record. It contains `initial_result` for the initial score, `result` for the best score, and `provenance` and `solution` for replay. Replay accepts the combined record or a standalone JSON witness. The recorded witness hash covers the original bytes of the embedded solution after decompression.
