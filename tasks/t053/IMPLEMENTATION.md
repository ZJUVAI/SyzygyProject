# T053 implementation record

## Configuration and open status

`T053-C01` fixes `N=100000`. A candidate has exactly 100000 positive integer factors whose exact product is `100000!`. The objective is the smallest factor and is maximized.

The current repository main branch was checked on 2026-11-06. Its HEAD is `978e4802dd413356e7e0ff97a44db803ab9596eb`, dated 2026-06-24. The source data's final sample is `N=100000`, with the reported interval `(33641, 33649)`. The tuple order follows `bounding_data.py:get_bounds`: `(Tlb, Tub)`. The lower threshold advances only when the LP-guided greedy routine constructs at least N admissible factors. The upper endpoint comes from an LP relaxation and its dual calculation.

The interval is not an exact value. The paper says that upper bounds in the cited numerical figures were not verified. The LP generator also notes that it assumes factors are at most N and says this assumption had not yet been proved in that implementation. We therefore do not treat 33649 as a certified upper bound. The paper's Theorem 1.3(i) proves `t(N) <= N/e` for `N` other than 1, 2, and 4. For this configuration it gives the rigorous integer bound `t(100000) <= floor(100000/e) = 36787`. The exact value remains open in the sources checked.

The primary paper is [Alexeev et al., Decomposing a factorial into large factors, arXiv v4](https://arxiv.org/abs/2503.20170v4), dated 2026-04-03; the article was published electronically in *Mathematics of Computation* on 2026-10-15, [DOI 10.1090/mcom/4249](https://doi.org/10.1090/mcom/4249). The current arXiv and repository sources do not give an exact value for `t(100000)`. A search for a same-parameter closure found no proof or exact record.

## Source pins and reported values

- The repository snapshot is pinned to commit `978e4802dd413356e7e0ff97a44db803ab9596eb`. The source file `data/source/sutherland_greedy.py` is `src/python/greedy.py`, SHA-256 `6bc0a0ac756f406d595eced22ce6d7a004256d24f8fbd913b867570c00d9e344`.
- The public data snapshot `data/source/t_large_n_bounds.txt` has SHA-256 `9cd480d1f294a6e9d40612bd4644726e22e3ef26eef1dedcd607c260dff4178c`. Its last sample reports `(33641, 33649)`. It contains no factor witness for this row. The repository README describes the file as LP bounds for random samples between `10^3` and `10^5`.
- The reported lower endpoint 33641 is recorded as a public lower bound, not as an independently reproduced construction. The reported 33649 upper endpoint is archived with an explicit unverified status. The rigorous published upper used here is 36787.

## Reproduced human construction

The frozen human reference is `33330`. `human.py` reconstructs the upstream Sutherland greedy algorithm for a threshold of 33330. It first builds a subfactorization with 100008 factors, each at least 33330. This satisfies the paper's relaxed formulation: a subfactorization of cardinality at least N can be converted to exactly N factors of the full factorial. The code keeps 100000 factors and distributes all leftover prime powers across those factors. This restores the exact product without lowering any factor.

The resulting witness is saved at `data/reference/human_T100000_T33330.json`, SHA-256 `6f3e45225c731021ebf20281ab66c53aa601d5160927ace684547403a4d36cbb`. It has exactly 100000 positive factors, minimum 33330, and product exactly `100000!`. A separate test factors every output factor with an independently built smallest-prime-factor table, then compares each prime's total exponent against Legendre's formula for `100000!`.

The source comment attributes the method to Andrew Sutherland's Maple code and credits Adam Wagner for help with its Python conversion. The paper describes its use of linear/integer programming and computational methods. These sources do not state whether AI tools were used; no AI-free claim is made.

## Programs and fixed seed results

All five programs expose `run_code()` and read `MATHBENCH_CONFIG_ID` and `MATHBENCH_SEED`.

| Entry | Method | Seed 0 result | Fixed work |
| --- | --- | ---: | ---: |
| `init_program.py` | Direct factorization `[1, 2, ..., 100000]` | 1 | direct construction |
| `baseline.py` | Greedy prime transfers from the simple seed | 41 | 64 iterations; 64 accepted transfers |
| `human.py` | Reconstructed Sutherland greedy method | 33330 | one deterministic run |
| `reference.py` | Replay saved exact human-method witness | 33330 | direct replay |
| `evolution.py` | Random receiver selection with exact prime transfers from the simple seed | 158 | 256 iterations; 256 accepted transfers; 157 best improvements |

The baseline and evolution entries do not read or import the human or public comparison witness. Their prime-transfer operations preserve the product exactly. Each resulting construction is then checked by the trusted evaluator. The evolution result is saved at `best/seed_0.json`, with seed, fixed iterations, platform, Python version, one-thread setting, exact result, and replay command. The reference witness remains under `data/reference/`.

Reproduce the saved search result with:

```sh
MATHBENCH_CONFIG_ID=T053-C01 MATHBENCH_SEED=0 .venv/bin/python -c 'from tasks.t053.evolution import run_code; import json; print(json.dumps(run_code()))'
```

Search defaults are fixed at 64 and 256 iterations. Explicit `MATHBENCH_SEARCH_SECONDS` may enable a wall-clock cutoff. The shared runner limits generation to 300 seconds and verification to 60 seconds, with 4 GiB memory and one numerical thread.

## Exact checker

`check.py` rejects any list with the wrong length, non-integer values (including Boolean and floating-point values), zero, negative factors, or a factor larger than `100000!`. It multiplies the factors with a balanced exact product tree and compares the result to Python's exact integer `factorial(100000)`. The objective is recomputed as `min(factors)`. Optional claimed objective and score fields do not affect the complete validation result.

## Validation

Command:

```sh
.venv/bin/python -m pytest tasks/t053/test_task.py -q
```

Result on 2026-11-06: `22 passed in 7.33s`.

The suite covers the initial exact construction, the human and reference witnesses, independent prime-exponent validation, source hashes and public-bound tuple, invalid length/type/value cases, forged scores, all five program entries, search isolation, and worker error and timeout handling through `mathbench.evaluate._run` without task registry admission.

Sol review remains pending.
