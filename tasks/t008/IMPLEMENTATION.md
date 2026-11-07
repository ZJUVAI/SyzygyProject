# T008 implementation notes

## Configurations

T008-C01 remains the accepted C(24,14,4) instance. T008-C02 is C(20,10,4) and is accepted by Sol on 2026-11-07. Its frozen human reference and best verified public record are the reproduced 36-block LJCR construction. Deliever et al. list a 35-block tabu-search attempt with 18 uncovered four-subsets; it is infeasible and excluded from SOTA. LJCR reports the lower bound 32, so optimality is unknown.

The C02 witness comes from the complete block listing on the LJCR record. The Zenodo v1.2 `coverdata.json` index confirms the 36 upper bound and lower bound 32. The source uses labels 1..20. The saved JSON maps each label x to x-1. The task checker independently enumerates all C(20,4)=4,845 required subsets; it finds no uncovered subset among the 36 distinct blocks.

## Programs

`check.py` reads v, k, and t from the selected configuration, rejects malformed or duplicate blocks, and recomputes the exact block count and coverage. It does not use the candidate's declared objective. `init_program.py` keeps the accepted C01 start unchanged and gives C02 a deterministic complete-cover fallback by extending each uncovered t-set with the lowest available points. The fallback is finite and valid; it is not intended as a competitive baseline.

`baseline.py` uses greedy set cover over 500 seeded random k-subsets plus the valid initial cover. `human.py`, `sota.py`, and `reference.py` load the saved C02 witness. `evolution.py` keeps its specialized C01 search kernel. For C02 it currently returns the configuration-aware valid initial cover as a valid fallback; it has no tuned evolutionary kernel yet.

## Limits and replay

Generation budget: 300 seconds. Verification budget: 60 seconds. Memory: 4 GiB. Threads: one. Reproduce C02 with:

```sh
MATHBENCH_CONFIG_ID=T008-C02 .venv/bin/python -m mathbench evaluate T008 tasks/t008/sota.py --strict --config T008-C02
```

The configuration is accepted by Sol on 2026-11-07. No Sol acceptance is inferred from the existing C01 review.
