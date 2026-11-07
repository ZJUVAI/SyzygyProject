# T076 implementation and evidence

## Status

`T076-C01` remains accepted by Sol under its existing acceptance record. New configurations `T076-C02` (16 elements) and `T076-C03` (17 elements) are accepted by Sol on 2026-11-07. Their witness records are feasible upper bounds; neither is claimed optimal. This file records implementation evidence and does not grant acceptance.

## Definition and checker

For the selected `n`, a valid set has exactly `n` distinct positive integers and exactly `2^n` distinct subset sums. The objective is the largest element, minimized. `check.py` binds each configuration ID to its full parameter object. It traverses subsets in Gray-code order with exact integer sums. Multiple modular fingerprints are only bucket keys; any collision is resolved by recomputing exact integer sums. Thus the checker does not rely on probabilistic hashing. It ignores claimed score fields and does not impose an integer magnitude bound.

## C02 and C03 human and public witnesses

The human method is the Conway-Guy recurrence in OEIS A005318, with the set formula described in Bohman (1998), §2 and Theorem 2.1. The local recurrence generator creates a witness independently of stored records. Exact checking covers 65,536 subset sums for C02 and 131,072 for C03.

| Config | Human maximum | Public witness maximum | Public witness and source | Lower bound |
| --- | ---: | ---: | --- | ---: |
| C02, n=16 | 17,305 | 17,072 | `data/reference/lunnon_w2_n16.json`; Lunnon (1988), Table 1, w² column | 12,870 |
| C03, n=17 | 34,301 | 33,531 | `data/reference/lunnon_w2_n17.json`; Lunnon (1988), Table 1, w² column | 24,310 |

Lunnon's Table 1 records the `w²` sequence values; the saved sets are reconstructed using the paper's formula (1.4), `P_n={w_n-w_{n-i}:1<=i<=n}`, and independently verified. The same sequence appears in OEIS A006756. The previously selected public candidates (17,270 at n=16 and 34,301 at n=17) remain recorded as feasible but weaker witnesses. The lower bounds are `binomial(n,floor(n/2))` from Dubroff-Fox-Xu (2021), Theorem 1. We also checked Costa-Della Fiore (2026) and Hasratyan-Ruszinkó (2026) for lower-bound updates. Maltby's 1997 paper gives a general extension construction but does not report a better explicit value at these two sizes in its abstract/available source record. No finite optimum proof was located. This source review is not exhaustive.

Witness file SHA-256 values are recorded in `records.json` and `sota.json`. C02 and C03 reference hashes are checked by tests against the archived JSON files; their exact objectives are 17,072 and 33,531.

## Search and cold start

`init_program.py` creates `[1,2,...,2^(n-1)]`; it reads no comparison witness. `baseline.py` runs descending greedy searches over a fixed cap grid, using a bitset indexed by attainable sums for each bounded search trial. It records the seed and number of trials, and reads no comparison data. `evolution.py` calls this search entry. `human.py` rebuilds the Conway-Guy set from its recurrence. `reference.py` loads the fixed public witness for the selected configuration. These comparison programs are separate from initial and search context.

## Sources

- Bohman, [A construction for sets of integers with distinct subset sums](https://www.combinatorics.org/volume_5/pdf/v5i1r3.pdf), 1998, §2 and Theorem 2.1.
- Lunnon, [Integer Sets with Distinct Subset-Sums](https://doi.org/10.1090/S0025-5718-1988-0917837-5), 1988, Table 1 and formula (1.4).
- [OEIS A005318](https://oeis.org/A005318), Conway-Guy recurrence.
- [OEIS A006756](https://oeis.org/A006756), Lunnon's generalized Conway-Guy `w²` sequence.
- [OEIS A276661](https://oeis.org/A276661), Sharp n=15 witness and extension statement.
- Dubroff, Fox, and Xu, [A note on the Erdős distinct subset sums problem](https://arxiv.org/abs/2006.12988), 2021, Theorem 1.
- Maltby, [Bigger and better subset-sum-distinct sets](https://doi.org/10.1112/S0025579300011979), *Mathematika* 44 (1997), 56–60.

## Validation

Run `.venv/bin/python -m pytest tasks/t076 -q`. Tests retain C01's checks and cover the new configurations' data hashes, full exact subset-sum counts, parameter binding, five program entries, invalid sets, and ignored claim fields. The new configurations passed independent Sol review. See records.json.
