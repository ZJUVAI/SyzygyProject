# T030 implementation notes

Status: accepted by Sol on 2026-11-06.

## Evidence and replay

- Fixed configuration: DIMACS DSJC1000.5, 1,000 vertices, 249,826 undirected edges, minimize distinct colors.
- Input source: pinned DIMACS-format text copy in `data/source/DSJC1000.5.col`; SHA-256 `17b395030fbab1e2a6564396c3a161dbb3248423953e6b462377a018b8f4bb6c`.
- Candidate input: `data/instance.json`, graph only; SHA-256 `51550de59559742f72c2da8e3963edab39124cd8f334eb63cae10d9bb3f132bd`. It has no known bounds or colorings.
- Best reported and reproduced result: 82 colors from Titiloye and Crispin. The author-hosted certificate is `data/source/DSJC1000.5_K82_col.txt`; SHA-256 `0e73778bb2934ee8a828b59cbd3b5deaaadc88716d5010af67ec7cdaec2c5109`. The task independently checks all 1000 labels and 249826 edges. Replay summary: `data/DSJC1000.5_K82_verification.json`.
- Frozen human reference H is 86, from Loudni's ID-VNS result. Its normalized witness is `data/human_witness.json`, SHA-256 `de1106b17304b59fb18809d285e91ad78f8414a892e2e5ea1e7fedbfaa630007`. `human.py` reproduces H; `reference.py` reproduces the 82-color public construction.
- `data/source/DSJC1000.5_K83.txt` preserves the earlier QA-col certificate. It replays to 83 colors and is superseded by the 82-color result.
- Cazenave, Negrevergne, and Sikora's arXiv:2504.03277v1 explicitly says in Section 6.2, Table 4's note that these difficult instances' chromatic numbers seem unknown; it reports lower bound 73. Held, Cook, and Sewell also report 73. This task does not recompute the lower bound. The reported interval is 73 to 82. The VSS-Col paper authors are Alain Hertz, Matthieu Plumettaz, and Nicolas Zufferey; it also marks χ unknown and gives k*=83.

## Programs

- `init_program.py` is self-contained and returns a valid coloring with one color per vertex.
- `baseline.py` runs eight seeded DSATUR greedy constructions by default. It reads only the fixed graph input. `MATHBENCH_SEARCH_SECONDS` enables the shared wall-clock cutoff.
- `evolution.py` exposes the required task-qualified `run_code()` entry and delegates to the traditional baseline.
- `human.py` reads the frozen 86-color human reference from `data/human_witness.json`.
- `reference.py` reads the verified 82-color public construction from `data/source/DSJC1000.5_K82_col.txt`.
- The intended candidate input allowlist is only `data/instance.json`. Files in `data/source/` and `data/human_witness.json` are comparison assets.

## Validation and limitations

- Exact mathematical checks use integer colors and inspect every fixed edge. The objective is recomputed as the cardinality of the set of submitted colors. Candidate score fields are ignored.
- Unit tests cover the source graph hash and extraction, both the 82-color public certificate and the 86-color frozen human reference, the self-contained seed, a deliberately invalid one-color assignment, malformed labels, altered score claims, deterministic baseline output, and runner program-error and timeout handling.
- `.venv/bin/python -m pytest tasks/t030/test_task.py -q`: 8 passed in 22.69 seconds.
- Saved seed 0 DSATUR baseline: 113 colors, 8 iterations, 1.6884 seconds. The trusted checker inspected all 249826 edges.
- The lower bound 73 is a reported literature value, not an independent local verification.
- The shared registry does not yet include T030. Full `evaluate_candidate` integration remains for the main reviewer after adding T030 to shared task discovery and exporting only the graph input.
- No exhaustive search of every later publication has been made. Sol should recheck current sources before acceptance.
