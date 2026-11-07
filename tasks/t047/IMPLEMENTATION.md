# T047 implementation evidence

Status: accepted by Sol on 2026-11-06.

## Definition and source status

- T047-C01 minimizes the size of a finite set of unrestricted integers whose pairwise differences include every `d` from 1 through 6166. Marks may be negative or greater than 6166. This is not the sparse-ruler problem with marks constrained to `[0,6166]`.
- Leech and Golay's reported 128-point construction gives an upper bound. Banakh and Gavrylkiv (2017), Theorem 4.1 and Table 3, and Georgiev et al. (2025), arXiv:2511.02864v1 §6.3, report this construction. Neither source claims `Delta(6166)=128`.
- The strongest source-reported human construction is 128 points. The historical point list was not recovered. The separately reproduced Wichmann construction has 158 marks and is the frozen human reference.
- The checked analytic lower bound is 123. Banakh and Gavrylkiv show `inf_n Delta(n)^2/n >= 2 + max 2 sin(phi)/(phi+pi)`. At `phi=pi/2`, using `pi<22/7` gives the strict bound `>80/33`. Hence `33*Delta(6166)^2 > 80*6166 = 493280`. Since `122^2*33=491172` and `123^2*33=499257`, `Delta(6166)>=123`. The simple pair-counting bound 112 is also valid but weaker.
- The source survey found no checked exact solution for this finite parameter by 2026-11-06; the checked gap is 123–128. It is a bounded survey, not a proof that no later result exists.
- The AlphaEvolve paper separately reports a later AI-assisted improvement to the asymptotic upper bound using `N=49109` and 360 points. The human-given Singer-set code and this different parameter are recorded separately; the result is not used as T047-C01's record.

## Human and public witnesses

- `human.py` rebuilds Wichmann `W(38,3)` from the published gap formula. It has 158 marks and length 6548. The construction is a restricted ruler, so it is also a valid witness for the unrestricted integer-difference model at N=6166. Saarela and Vanhatalo (2026), EJC #P1.40, Definitions 8 and 16 and Theorem 18, provide the formula and a completeness proof. The saved witness is `data/reference/wichmann_w38_s3_n6166_158.json`, SHA-256 `39bb5d5aaecf6a5ed3c38e088d18cc0759d28b40d2908d68a9ded3a3e7b9c6e4`.
- `reference.py` replays a separate 128-mark Singer/Leech-family witness. The cyclic factor comes from the 32 trace-zero exponents in `GF(31^3)` with defining polynomial `x^3 - 2*x^2 - 3`; multiplying its exponents by 172 modulo 993 gives a 32-element cyclic difference set whose ordinary positive differences include 1 through 208. The product with `{0,1,4,6}` gives 128 distinct marks and covers every required distance through 6166. The witness is saved at `data/reference/singer_q31_leech_product_n6166_128.json`, SHA-256 `e7af998f30472857a1403e637b595e7d69dbde02dc851060c03bbdf1fe0e248c`.
- The 128-point witness is an independent computational reconstruction of the classical method. The multiplier was selected by a finite search. It is not claimed to be the exact witness used by Leech or Golay. This distinction is recorded in `sota.json` and `records.json`.
- The pinned AlphaEvolve notebook is 68,217 bytes at repository commit `8f447457957deac61e28bf1676746f0753b3b2f8`; blob SHA-1 `0cdb812ada3b6053f749e05301a743fd191e8700`; raw SHA-256 `e5bd224563055caf53c0fef9b9c67620c7124a14aa77094cce456d9927b65489`. It provides the separate 49109-parameter evolved construction, not the 6166/128 witness.

## Programs

- `check.py` checks exact integer types, rejects bools and duplicates, and recomputes the entire required interval using exact differences. It ignores claimed objective fields. Differences greater than 6166 are allowed.
- `init_program.py` returns `{0,1,...,6166}`, a simple valid seed that reads no comparison data.
- `baseline.py` runs a seeded randomized greedy set-cover search. Each insertion includes a guaranteed progress candidate built from the smallest missing distance. It reads no human or reference witness.
- `human.py` reconstructs the Wichmann human baseline.
- `reference.py` reads the pinned 128-point comparison witness.
- `evolution.py` exposes `run_code()` through the traditional search baseline.
- `evaluator.py` adapts T047 to the shared evaluator.

## Verification commands and results

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t047/test_task.py -q
.venv/bin/python -m json.tool tasks/t047/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t047/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t047/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t047/data/reference/singer_q31_leech_product_n6166_128.json > /dev/null
.venv/bin/python -m json.tool tasks/t047/data/reference/wichmann_w38_s3_n6166_158.json > /dev/null
```

The task tests pass: 19 tests. They cover the exact 128-point witness, an independent all-distances scan, the 158-mark Wichmann formula and length, the initial seed, empty and incomplete bases, duplicate marks, bool/float/NaN/infinity, claimed-score invariance, a mismatched configuration, all five program entries and their configuration checks, seeded search metadata, runner error and timeout handling, and strict JSON witness replay.

The baseline was also run through `evaluate_candidate` in strict mode with the local task config temporarily patched in process. It returned objective 234, exact status, generation time 1.99 s, verification time 0.40 s, seed 0, Python 3.13.12 on Linux, and the default 300 s / 60 s / 4 GiB / one-thread limits. The result is saved under `best/T047-C01/`. No shared registry file was edited.

## Limits and Sol review points

- The checked bounds are `123 <= Delta(6166) <= 128`; the implementation does not prove the exact value of `Delta(6166)`.
- The saved 128-point witness is not claimed to be the identical historical Leech/Golay witness.
- The main reviewer should independently replay the Wichmann human baseline and the 128-point reference, check a deliberately broken basis, recompute at least one coverage quantity, and confirm that forged score fields do not change validation.
