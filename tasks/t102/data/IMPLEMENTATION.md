# T102 implementation status

Status: accepted by Sol on 2026-11-09. The checker parses feasible rational pairs once, then evaluates all routes and all one-based cuts exactly with scaled integers. It recomputes `11/10` for the Skutella Figure 2 construction and `47/42` for the rationalized, pinned AlphaEvolve witness.

`init_program.py` returns the uniform feasible seed. `baseline.py` and `evolution.py` call the shared heterogeneous rational mutation search for 16 and 32 iterations. The search reads only `MATHBENCH_SEED` and never reads witness files. `human.py` and `reference.py` are external comparison programs.
