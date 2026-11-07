# T080 implementation and verification

Status: `accepted_by_sol`.

## Sources and scope

- Primary source: Gyarmati, Hennecart, and Ruzsa, *Sums and Differences of Finite Sets*, manuscript dated 2008-05-30, Section 2 lemma before equation (11) and equations (13)-(15): <https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf>.
- The lemma requires the strict finite condition `d<q`, where `d=|U-U|` and `q=2 max(U)+1`. The checker enforces this exact hypothesis.
- The human baseline is the published `V(6,5)` projection formula reconstructed locally. Exact recounting gives 462 points, `s=8008`, `d=39733`, `max(U)=555555`, and `q=1111111`. The witness is `data/reference/gyarmati_hennecart_ruzsa_m6_l5.json`, SHA-256 `39cb22a35e93fdd3a2431a121f3b8fa015c0b8ce5c84ca5304cfcb1c59777f39`.
- No optimality proof for the bounded benchmark domain was identified. The paper's small-set result for cardinality at most 11 does not cover this domain, which allows up to 512 elements. The finite witness score is not an asymptotic exponent.
- `data/source/objective_distinction_examples.json` records exact ranking reversals against T012 and T077. It is not read by any search program.

## Programs and isolation

`init_program.py` returns the simple set `{0,1,4}`. `baseline.py` and `evolution.py` start from that seed and use only their own integer-set mutations and exact finite sum/difference counts for heuristic feedback. They do not import `human.py`, `reference.py`, or comparison data. Their defaults are 500 local-search iterations and 60 evolutionary generations with population 6. Both use seed 0 by default and accept `MATHBENCH_SEED`; the runner may also set `MATHBENCH_SEARCH_SECONDS` for a wall-clock exploration cutoff.

`human.py` generates the finite simplex projection from the cited formula. `reference.py` replays the frozen JSON witness. The source file is local to this task. The evaluator adapter uses the shared runner; no shared code or registry was changed.

## Verification

The checker rejects non-integer values (including booleans), duplicates, missing zero, invalid cardinality, out-of-range elements, configuration drift, and candidates with `d>=q`. It recomputes both sets from all ordered pairs. It ignores candidate score fields and evaluates the logarithms with outward-rounded mpmath intervals at 80 decimal digits. The returned objective is the lower interval endpoint for maximization.

The saved `V(6,5)` witness has interval:

`[1.115060403741140735041045058838694409478537675104001271984446801146236339133304588949, 1.115060403741140735041045058838694409478537675104001271984446801146236339133304591057]`.

The conservative lower endpoint is frozen as the compatibility baseline `H`. The strict condition, formula counts, witness hash, interval, and ranking reversal examples are covered by task-local tests.

## Commands run

Environment: repository `.venv/bin/python` (Python 3.13); seed 0; default fixed search budgets. Each program was run through its module entry point with `MATHBENCH_CONFIG_ID=T080-C01` and `MATHBENCH_SEED=0`.

- `.venv/bin/python -m pytest tasks/t080 -q` — 9 passed.
- Ran `init_program`, `baseline`, `evolution`, `human`, and `reference`; all returned valid output. The simple seed and both search methods returned 3-element sets; human and reference returned the 462-element witness.
- Validated `task.json`, `sota.json`, `records.json`, and both source JSON files with `python -m json.tool` — passed.
- `git diff --check -- tasks/t080` — passed.

Task-local tests cover formula counts and strict inequality, human/reference replay, all five entry points, ranking reversals, boundaries, invalid inputs, declared-score tampering, record consistency, and runner error/timeout paths. Full upstream model comparisons have not been run.
