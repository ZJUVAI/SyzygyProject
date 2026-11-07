# T033 implementation notes

Status: accepted by Sol on 2026-11-06.

## Source and configuration review

- The selected configuration is Gset G70: 10,000 vertices, 9,999 undirected edges, all with weight +1.
- The byte-exact Stanford file is archived at `data/source/G70`. Its SHA-256 is `0d965a2ff1444cc71d7740824b5b3a5e09fc1843cbf6d90691b52d5221987061`.
- The normalized zero-based edge-list SHA-256 is `76223a8eea98e77f0c1769f49c42a7d202fa5d62a47c872ed7b9d179d0f23085`. The checker verifies this pinned hash when it loads the graph.
- Goudet, Goëffon, and Hao report 9,594 on the G70 test instance and 9,595 as a calibration value in their 2024 LPI paper. The paper-specific assignment was not obtained.
- Cosm v4 (revised 2026-10-11) reports a heuristic G70 score of 9,595. Its abstract distinguishes this as best-known from the certified optima it reports for G81, G72, and G77. AI-assistance disclosure is unknown.
- The LPI paper reports 9,594 on its G70 test instance and 9,595 as a calibration value. A 2019 coherent-Ising-machine paper reports numerical SDP value 9,683 for G70. This task did not independently certify it as an upper bound; the 88-point difference is not a certified gap.
- Qian and Pan's arXiv v5 (revised 2021) relaxation paper reports upper bounds and known best values on large UBPP instances. The 2026 result table does not provide a G70 upper bound or proof. No checked source proves G70 optimal.
- The reproduced traditional baseline uses a single-vertex FLIP neighborhood from published Max-Cut local search. It is a task-local implementation, not a reproduction of the full BLS algorithm or its reported G70 result.

## Reproduction and validation

- Human-method baseline: fixed seed 0, four starts, at most 10,000 steepest improving flips per start; actual flips were 2,163, 2,226, 2,227, and 2,158 (8,774 total); checker result 8,616. The saved witness records these counts.
- Cold start: 10,000 labels on side 0; checker result 0.
- Checker reads the pinned 9,999 edges and sums integer weights exactly. It ignores candidate score fields and supplied graph edges.
- Test command: `.venv/bin/python -m pytest tasks/t033/test_task.py -q`.
- Test result: 14 passed.
- Direct entry-point smoke run with `MATHBENCH_SEARCH_STEPS=1`: init 0, baseline 8,888, evolution 8,595, human 8,616, reference 8,616. The human default seed result matches frozen H=8,616.
- Standalone cold-start export was run with Python isolated mode; it returned 10,000 valid labels without importing task modules.
- The shared evaluator cannot load T033 until the main reviewer temporarily registers the task. The task-local checker and all four `run_code()` entries can be exercised directly.

## Limitations

- The reported 9,595 value has no witness replayed here. The external comparison witness is in `data/human_g70_1flip.json`; `best/` is reserved for own-search results. The saved local FLIP witness scores 8,616 and is the frozen human baseline.
- The G1 configuration was removed after a 2026 paper reported a Gurobi value matching its listed known optimum. G70 is selected because the checked literature reports 9,595 as a heuristic lower bound and no certificate was found.
- The reviewed-source search does not prove that no G70 certificate exists elsewhere.
