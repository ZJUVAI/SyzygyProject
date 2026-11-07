# T050 implementation evidence

Status: accepted by Sol on 2026-11-06.

## Definition and source status

- T050-C01 fixes the 9-dimensional hypercube `Q9`. A vertex is an integer in `[0,512)`, interpreted as a 9-bit string. A solution is an ordered list of distinct vertices. Consecutive vertices must have Hamming distance one; every nonconsecutive pair must have distance at least two. The score is the number of edges, `len(vertices)-1`, and is maximized.
- The current paper is Orland et al., arXiv:2607.15270v3, submitted 2026-09-30. Section 6 says the Q9=191 record came from cube-surgery simulated annealing. Appendix E prints a complete Q9 witness. The same paper says LLMs helped with manuscript work and writing and optimizing search code; it does not connect that assistance to this exact witness or run. We record the project-level disclosure and leave the precise run-level contribution unknown.
- Wynn (2012), arXiv:1201.1647v1 §VI and Appendix, reports Q9=190 and prints its full transition sequence. This is the traditional human construction and frozen baseline. The 190-step sequence is exactly replayed locally.
- The authors' data repository is pinned at commit `46c765399353a588ea50444a5d6610f53102b1c2` (2026-10-01). README blob SHA-1: `3e66ab83a2be5ddbfacd3081c0df5ce3d4b7ae04`. The `record_snakes.csv.zip` blob SHA-1 is `7854e2592325dab85a35a8a4809314edb80f7af8` and its size is 16,721,566 bytes. The local 191 witness is transcribed from the current v3 Appendix E, rather than extracted from the large archive.
- A current Q9 status page checked on 2026-11-06 lists verified lower bound 191 and unknown upper bound. The 2026 paper leaves a 192-edge snake open. The 131 reported 191-edge symmetry classes were found across millions of sampled snakes; that count is not a proof of optimality or completeness.

## Saved witnesses

- `data/reference/wynn_q9_190.json` stores 190 coordinate flips from Wynn, starting at vertex 0, and the resulting 191 vertices. SHA-256: `3f74e9ce45736179738ae16fb447e4c5ea7cb594ea776b930fa5c7acbac00882`.
- `data/reference/orland_v3_q9_191.json` stores 191 coordinate flips from Orland et al., Appendix E, starting at vertex 0, and the resulting 192 vertices. SHA-256: `fff784d8d79ec56682765735ad3263d9978338279ea1854f43438ea9bd37b7a4`.
- Both transition lists were replayed independently. The checker found scores 190 and 191, respectively, and verified every vertex pair.

## Programs and tests

- `check.py` rejects invalid labels, bools, non-integers, repeated vertices, nonadjacent consecutive vertices and nonconsecutive adjacency. It recalculates the edge count and ignores declared score fields.
- `init_program.py` makes a valid 9-edge path by flipping each coordinate once.
- `baseline.py` uses fixed-seed random greedy endpoint extension with a bounded number of restarts. It reads no comparison witness.
- `evolution.py` uses endpoint truncation and greedy regrowth from a bounded population. It reads no comparison witness.
- `human.py` and `reference.py` replay the respective fixed witness from `data/reference/`.
- `evaluator.py` adapts the task to the shared evaluator.

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t050/test_task.py -q
.venv/bin/python -m json.tool tasks/t050/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t050/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t050/records.json > /dev/null
```

The task-local suite passes: 5 tests. It checks both source witnesses, independently counts the 191 path edges, scans every nonconsecutive pair, checks boundary and malformed inputs, confirms forged score fields do not change validation, runs all five program entries, and tests runner error and timeout handling through `_run`.

The shared runner was exercised in-process with only its task lookup temporarily pointed at this unregistered task. Strict evaluation of `evolution.py` saved a 117-edge search result to `best/T050-C01/`. It used seed 0 and 32 generations. On Python 3.13.12/Linux, generation took 2.03 s and verification took 0.50 s; the runner limits were 300 s generation, 60 s verification, 4 GiB and one thread. A separate strict run of `baseline.py` with seed 1 and 32 restarts returned 103 edges (6.28 s generation, 3.50 s verification). The shared task registry was not changed.

## Limits and Sol review points

- The 191-edge public construction is a lower bound. No upper bound for `a(9)` is known in the checked current sources.
- The authors disclose project-level LLM assistance, but do not attribute it to the exact 191-edge witness or the run that found it.
- The reported 131 symmetry classes are sampled results, not a completeness certificate.
- The saved `best/` result is only this task's own seeded search output. The Wynn and Orland witnesses remain under `data/reference/` as external comparisons.
- Sol should independently replay the 190-edge human and 191-edge public witnesses, check a deliberately broken induced path, recompute the edge count and confirm that forged score fields do not change validation.


Additional configurations use the same induced-path rules. Use `MATHBENCH_CONFIG_ID`. C01 has 9 coordinates; C02 has 10; C03 has 11. Vertex labels range from zero to `2**dimension - 1`. The objective counts edges. The initial program uses only the public dimension.

C02 reproduces the 379-edge Q10 path. C03 reproduces the 746-edge Q11 path and records the later reported value 750 separately. Sources are Orland et al. arXiv:2607.15270v3 Table 1 and its Echols footnote. The historical comparator extends Wynn's Q9 path by adding an endpoint step in each new dimension. Both additions are accepted by Sol on 2026-11-07.

新增配置为10维与11维。验证复算379边和746边。11维750边另列为文献报告。新增配置已通过 Sol 验收（2026-11-07）。
