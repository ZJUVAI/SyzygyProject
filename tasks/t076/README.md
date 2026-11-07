# T076: Minimum maximum element in a sum-distinct set

## Definition and configurations

For fixed `n`, choose `n` distinct positive integers so that all `2^n` subset sums, including zero, are distinct. Minimize the largest element. This task has three configurations: `T076-C01` (`n=15`), `T076-C02` (`n=16`), and `T076-C03` (`n=17`). C01 retains its prior Sol acceptance. C02 and C03 are accepted by Sol on 2026-11-07.

The checker enumerates every subset in Gray-code order using exact integer arithmetic. Several modular fingerprints group possible collisions, but every collision is resolved by recomputing exact sums. The fingerprints are an index only. The checker accepts positive decimal strings for large integers and has no magnitude cap.

## Human constructions and public bounds

The human-method witness for each size comes from the classical Conway-Guy recurrence in OEIS A005318. Bohman (1998), §2 and Theorem 2.1, proves that the resulting family has distinct subset sums. The local generator reconstructs the recurrence and difference set. Exact maxima are 8,807 (n=15), 17,305 (n=16), and 34,301 (n=17).

Lunnon's 1988 Table 1 reports the generalized Conway-Guy sequence `w²`, with maxima 17,072 (n=16) and 33,531 (n=17). The associated sets are reconstructed from his formula (1.4), then independently checked locally. The values also appear in OEIS A006756. We found no better same-size witness in the later sources checked. These values are feasible upper bounds, not proven minima. The previous local n=16 Sharp extension (17,270) and Conway-Guy n=17 set (34,301) remain archived in the records as valid but weaker candidates.

The Dubroff-Fox-Xu lower bound `binomial(n,floor(n/2))` gives 12,870 at n=16 and 24,310 at n=17. No proof of optimality was found for either size in the cited sources. The source review was limited to OEIS A005318, OEIS A276661, and the cited construction and lower-bound paper; this is not an exhaustive literature search.

## Programs and cold start

All five task programs select their size from `MATHBENCH_CONFIG_ID`. The initial program returns powers of two. The traditional search uses a deterministic, seed-controlled sweep of descending greedy constructions. It reads no human or reference assets. The human and reference programs are separate comparison entries. Evolution delegates to the same search routine. Set `MATHBENCH_CONFIG_ID` to one of the three IDs before running an entry.

## Sources

- W. F. Lunnon, [Integer Sets with Distinct Subset-Sums](https://doi.org/10.1090/S0025-5718-1988-0917837-5), *Mathematics of Computation* 50 (1988), 297–320, Table 1 and formula (1.4).
- [OEIS A006756](https://oeis.org/A006756), generalized Conway-Guy sequence `w²`.
- Tom Bohman, [A construction for sets of integers with distinct subset sums](https://www.combinatorics.org/volume_5/pdf/v5i1r3.pdf), *Electronic Journal of Combinatorics* 5 (1998), R3, §2 and Theorem 2.1.
- [OEIS A005318](https://oeis.org/A005318), Conway-Guy recurrence and values.
- [OEIS A276661](https://oeis.org/A276661), Sharp's n=15 upper-bound witness and the listed extension rule.
- Quentin Dubroff, Jacob Fox, and Max Wenqiang Xu, [A note on the Erdős distinct subset sums problem](https://arxiv.org/abs/2006.12988), Theorem 1.

## Reproduction

Run `.venv/bin/python -m pytest tasks/t076 -q`. See [IMPLEMENTATION.md](IMPLEMENTATION.md) for file hashes, exact counts, source limitations, and validation evidence.
