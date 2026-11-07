# T075 implementation notes

Status: `accepted_by_sol`.

## Configuration and research

- Fixed configuration `T075-C01`: `n=36`, 3-uniform, maximize edges with at most two triples on every four-vertex set.
- Primary source: Victor Falgas-Ravry, Oleg Pikhurko, Emil Vaughan, and Jan Volec, “The codegree threshold of `K4^-`,” Journal of the London Mathematical Society 107 (2023), DOI `10.1112/jlms.12722`: <https://pikhurko.github.io/E/FalgasravryPikhurkoVaughanVolec23jlms.pdf>.
- Section 6.3, page 27, gives `H6={123,234,345,145,125,136,356,256,246,146}`, attributes it to Frankl and Füredi (1984), notes each vertex link is a 5-cycle, and states that blow-ups and iterated blow-ups are `K4^-`-free.
- The same section states that the ordinary Turán density of `K4^-` is unknown and cites the `2/7` conjecture. Its codegree results concern a different constrained extremal problem.
- Current-source queries on 2026-11-06 did not find a finite `n=36` exact result or proof that 2,220 is optimal. The 2026 exact result for the uniform Turán density of complete `K4^(3)` is a different forbidden hypergraph and a different density notion.
- Public H6 template is archived at `data/source/h6_template.json`. The derived 2,220-edge witness is archived at `data/reference/h6_iterated_blowup_n36.json`.

## Construction and checker

- The witness has ten outer H6 triples, each expanded to `6^3` triples across three parts, plus ten inner H6 edges in each of six parts: `10*216+6*10=2220`.
- `check.py` requires the exact configuration ID and parameter dictionary. It parses unordered triples, rejects duplicate edges and invalid labels, then checks all `C(36,4)=58905` four-sets. It returns the recomputed edge count and a direct double-counting upper bound of `C(36,3)/2=3570`.
- `human.py` rebuilds the recursive H6 witness from the public template. `reference.py` reads the frozen witness from `data/reference/`.
- `init_program.py` returns the empty hypergraph. Baseline and evolution use seeded random-order greedy additions from the empty set. These programs do not read human/reference assets.
- A direct seed-0 baseline run tested five orders and got 1,245 edges from trial counts `[1226, 1245, 1243, 1226, 1211]`. It was exactly rechecked and saved under `best/T075-C01/`. This task-local run was invoked directly; the record states that runner memory/time limits were not installed.

## Validation

Use `.venv/bin/python`:

```sh
.venv/bin/python -m pytest tasks/t075/test_task.py -q
```

Tests cover the exact 2,220-edge witness, the H6 link cycles, a deliberate three-edge four-set, duplicate/unordered triples, invalid labels and numeric types, empty construction, ignored scores, the direct double-counting bound, all program entries, reproducible search counts, evaluator use with a temporary registry patch, and runner errors/timeouts. The final command completed with 36 passed tests in 16.77 seconds:

```sh
.venv/bin/python -m pytest tasks/t075/test_task.py -q
```
