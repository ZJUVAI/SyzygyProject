# T044 implementation evidence

Status: accepted by Sol on 2026-11-06.

## Definition and source status

- T044-C01 asks for the maximum order of a simple undirected connected graph with maximum degree at most 3 and diameter at most 5.
- The current Comellas table lists order 70 for `(3,5)`. It does not bold the entry. The Moore bound is 94, so the exact maximum remains open.
- The human baseline replays the historical Alegre-Fiol-Yebra adjacency list, attributed by the detail page to von Conta (1983) and Alegre, Fiol, and Yebra (1986). The second fixed reference replays Comellas's 2024 Coxeter construction output. Both source files have pinned SHA-256 values and pass this task's exact checker.
- The source site states that its material is AI-free except for some SageMath scripts. It does not identify the 2024 Coxeter script as one of those. The human baseline is the historical 1983/1986 graph. The fixed reference uses the saved 2024 adjacency output and does not execute its SageMath construction script.

## Programs and data

- `check.py` validates a fixed vertex set `0..n-1`, unique simple undirected edges, maximum degree, connectivity, and diameter. It runs BFS from every vertex and recomputes `n`; it ignores score claims. The Moore bound 94 also caps declared order.
- `init_program.py` is self-contained and returns a one-vertex graph.
- `baseline.py` samples random cubic graphs with the configuration model and checks each candidate with BFS. It rejects loops, duplicate edges, disconnected graphs, and diameter above 5. It searches only this subclass of the task's graph space and reads no human/reference data.
- `human.py` replays the AFY historical adjacency list. `reference.py` replays the Comellas 2024 Coxeter adjacency list.
- `evolution.py` exposes the required `run_code()` entry point. `evaluator.py` wraps the shared evaluator.
- `best/T044-C01/` stores the seed-0 search output, exact result, replay command, environment, budget, and output hash. The search returned 26 vertices after 384 attempts, with 2 accepted cubic candidates. It does not store either comparison graph.

## Verification commands and results

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t044/test_task.py -q
.venv/bin/python -m json.tool tasks/t044/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t044/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t044/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t044/best/T044-C01/solution.json > /dev/null
.venv/bin/python -m json.tool tasks/t044/best/T044-C01/result.json > /dev/null
.venv/bin/python -m json.tool tasks/t044/best/T044-C01/provenance.json > /dev/null
.venv/bin/python -m json.tool tasks/t044/best/T044-C01/verification.json > /dev/null
```

The task tests passed: 7 tests. They cover both order-70 source files and hashes, an independent all-source distance audit, the one-vertex seed, small boundary graphs, loops, duplicate undirected edges, endpoint and type errors, degree overflow, disconnected graphs, diameter overflow, Moore-bound input range, altered configuration, forged scores, all five `run_code()` functions, deterministic search metadata, and shared-runner candidate errors and timeout reporting.

The saved seed-0 search result was replayed through `evaluate_candidate` with strict checking. It returned objective 26, exact status, 0.61 seconds generation, 0.70 seconds verification, Python 3.13.12 on Linux, and the default 300-second/60-second/4-GiB/one-thread policy. The task ID was added only to the local in-process registry tuple; no shared registry file was changed.

The 70-vertex witnesses were checked by BFS from all 70 vertices and independently audited by a second test routine. Each has 105 edges, maximum degree 3, and diameter 5.

## Limits and review points

- This implementation verifies feasible graphs only. It does not prove that order 71 or larger is impossible.
- The baseline samples only simple cubic graphs. A failed random run gives no upper-bound evidence for all graphs with maximum degree at most 3.
- The 2024 Coxeter graph construction script is not run; only its published adjacency output is replayed and validated.
- Sol must independently run the human, reference, and baseline programs, recompute degree and diameter, reject a broken graph, and confirm that a forged score does not change the result before acceptance.
