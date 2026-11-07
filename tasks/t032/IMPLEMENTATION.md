# T032 implementation record

Status: accepted by Sol on 2026-11-06.

## Source and construction

Pinned primary source: Saurabh, arXiv:2608.26603v1 (2026-08-27), https://arxiv.org/html/2608.26603v1. Section 4, Table 1 reports 126 <= z(14,19;3,3) <= 135. Appendix A and its ancillary archive provide the explicit matrix. The source says the classical kicked-greedy search used no language model or learned component; NOVA selected the cell, ran the search, and packaged the result. The paper does not establish optimality. Literature search on 2026-11-06 found no later primary source closing this exact cell; exact-cell search limitations remain.

Archived ancillary files are in `data/source/`. `witnesses.json` SHA-256: `5ca22e606ae1645b593ea7b36e02139d1f605226b19abc7d3569128523743578`. The author's verifier SHA-256: `5ca84b119d39ebfbd88375f2cf81c468e964f7d0c0fcff8dc730b1fc0ff76800`. The task checker independently recomputes the sum and tests every triple of rows using integer bit masks. This checks all 364 row triples, equivalent to checking every 3-row by 3-column block.

The public matrix is replayed from `data/human_witness.json`. This reproduces the construction, not the search. The paper records seed 7, but does not record the kick count. The task-local traditional search starts from the empty matrix, has a fixed 10,000-iteration default, and does not load witness data. It records and returns its global best matrix. Periodic kicks delete four existing ones, preserving feasibility; subsequent steps greedily add ones. This is a baseline implementation, not a reproduction of the published run.

## Run record and limits

Generation budget: 300 seconds. Verification budget: 60 seconds. Memory: 4 GiB. Numerical threads: 1. The baseline uses seed 0 by default. `MATHBENCH_SEARCH_SECONDS` can request a machine-dependent wall-clock cutoff; otherwise the iteration budget is fixed. Replay commands: `.venv/bin/python -m pytest tasks/t032 -q`; `.venv/bin/python -c 'from tasks.t032.human import run_code; from tasks.t032.check import validate; print(validate(run_code(), {"parameters":{"rows":14,"columns":19,"forbidden_submatrix":[3,3]}}))'`.

Validation performed in this implementation: independent task checker source was written to verify the witness, structural-invalid case, abnormal entry types, and score-claim ignoring. Task tests:9 passed after the baseline repair. Sol admission must still run all five programs and independent controls. The baseline preserves the global incumbent across kicks and returns that matrix. Its metadata records actual steps, kick count, incumbent score, final search-state score, and returned score. The seed-0 run completed 10,000 steps and 10 kicks. It returned the global incumbent with 117 ones; the final search state had 113. The task regression test checks the returned matrix is valid and its score equals the recorded incumbent and is no lower than the final state.
