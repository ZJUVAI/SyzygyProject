# T082 implementation and verification

Status: `accepted_by_sol`.

## Source review and record

- Definition and recent research: Clinch, Drescher, Huynh, and Saffidine, *Constructions, bounds, and algorithms for peaceable queens*, arXiv:2406.06974 v3 / ALENEX 2025: <https://arxiv.org/abs/2406.06974>. Their regular-board asymptotic upper bound applies only for sufficiently large board size. Their local search quickly finds the Ainley construction. Neither statement proves the n=30 construction optimal.
- Human construction: OEIS A250000 attributes the construction family for n<=30 to Stephen Ainley (1977) and gives `a(30)>=131`. Kamenetsky's public layout file, dated 2019-10-15, includes the complete n=30 board: <https://oeis.org/A250000/a250000_3.txt>. The task-local source copy has SHA-256 `a5da2c9d852ecc24f8abcfcdc1b219d998e58d27ca6758cc4757041714fb4cfc`.
- The source chart was parsed into `data/reference/peaceable_queens_n30_131.json`, SHA-256 `97350f71d71e4537ec694259c8b9c5805560bdfdb0198702887c2c4f158cd5a4`. The human entry parses the 30 source rows; the reference entry replays the coordinate JSON. Both recalculate to 131 queens per color with no attacking cross-color pair.
- DiMichele and Forbes, *Puzzle—Queen Puzzles: An Educational Approach to Integer Programming Techniques*, INFORMS Transactions on Education, reports a confirmed optimum `n=16 -> 37`: <https://pubsonline.informs.org/doi/full/10.1287/ited.2024.0122>. This updates older OEIS text that says only the first 15 terms are known, but does not settle n=30.
- A finite upper bound is 225. Opposite colors use disjoint row sets and disjoint column sets. If the counts are `rW,rB,cW,cB`, then `rW+rB<=30`, `cW+cB<=30`, and `m<=rW*cW`, `m<=rB*cB`. Therefore `2*sqrt(m)<=sqrt(rW*cW)+sqrt(rB*cB)<=30`, so `m<=225`. The checked finite gap is 131..225. No n=30 optimality proof was found in the sources reviewed on 2026-11-06.
- The Ainley construction predates modern generative AI. The saved file is Kamenetsky's later transcription; no claim is made that it is Ainley's original working record. The 2025 paper describes a local-search algorithm but does not claim that its 131 construction is a new record.

## Programs and search isolation

`init_program.py` returns white `(0,0)` and black `(1,2)`. `baseline.py` repeats a randomized greedy construction from this simple seed. `evolution.py` keeps feasible layouts and attempts to remove a pair and add another feasible pair. Search code reads no human, reference, or source file. `human.py` parses the task-local public text file. `reference.py` loads the frozen coordinate witness.

Defaults use seed 0, 12 baseline restarts, 30 evolutionary generations, and population 4. On this environment, the baseline returned 45 per color in 2.56 seconds and evolution returned 58 per color in 0.75 seconds. These are search outputs, not public records. Explicit `MATHBENCH_SEARCH_SECONDS` can set a wall-clock cutoff; the runner cap remains 300 seconds for generation.

## Checker and tests

The checker accepts only exact integer coordinate pairs on `0..29`, rejects booleans and non-integers, duplicate squares, unequal army sizes, opposite-color overlap, and every cross-color row, column, or diagonal attack. Same-color attacks remain allowed. It checks every white-black pair and returns the exact integer army size. It ignores any claimed objective or score.

Commands run with repository `.venv/bin/python` (Python 3.13), seed 0:

- `.venv/bin/python -m pytest tasks/t082 -q` — 9 passed.
- Ran `init_program`, `baseline`, `evolution`, `human`, and `reference` via their module entry points. All returned checker-valid solutions; scores were 1, 45, 58, 131, and 131.
- Validated task, SOTA, records, source notes, and reference JSON with `python -m json.tool` — passed.
- `git diff --check -- tasks/t082` — passed.

Task tests independently recount all 17,161 cross-color pairs in the 131 witness, check the row/column upper-bound arithmetic, test legal same-color attacks and illegal cross-color attacks, cover malformed and boundary coordinates, verify claimed-score tampering, run all five entries, compare records with recomputed scores, and exercise worker error and timeout paths through `mathbench.evaluate._run`.

Full upstream search and model comparison runs have not been performed. The best public result is recorded as a feasible lower bound, not as an optimum.
