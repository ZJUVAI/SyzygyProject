# T076: Minimum maximum element in a sum-distinct set

## Definition

For fixed `n`, choose `n` distinct positive integers so that all `2^n` subset sums, including zero, are distinct. Minimize the largest element. T076-C01 fixes `n=15`.

The checker enumerates every subset in Gray-code order using exact integer arithmetic. Several modular fingerprints group possible collisions, but every collision is resolved by recomputing exact sums. The fingerprints are an index only. The checker accepts positive decimal strings for large integers and has no magnitude cap.

## Human constructions and public bounds

The human witness from the Conway-Guy recurrence has maximum 8,807. The verified public witness from Sharp has maximum 8,635. Both constructions are described in the [source records](data/bestknown.json).

## Programs and cold start

The initial program returns powers of two. The traditional search uses a deterministic, seed-controlled sweep of descending greedy constructions. It reads no human or reference assets. The human and reference programs are separate comparison entries. Evolution delegates to the same search routine.

## Sources

- W. F. Lunnon, [Integer Sets with Distinct Subset-Sums](https://doi.org/10.1090/S0025-5718-1988-0917837-5), *Mathematics of Computation* 50 (1988), 297–320, Table 1 and formula (1.4).
- [OEIS A006756](https://oeis.org/A006756), generalized Conway-Guy sequence `w²`.
- Tom Bohman, [A construction for sets of integers with distinct subset sums](https://www.combinatorics.org/volume_5/pdf/v5i1r3.pdf), *Electronic Journal of Combinatorics* 5 (1998), R3, §2 and Theorem 2.1.
- [OEIS A005318](https://oeis.org/A005318), Conway-Guy recurrence and values.
- [OEIS A276661](https://oeis.org/A276661), Sharp's n=15 upper-bound witness and the listed extension rule.
- Quentin Dubroff, Jacob Fox, and Max Wenqiang Xu, [A note on the Erdős distinct subset sums problem](https://arxiv.org/abs/2006.12988), Theorem 1.

## Reproduction

Run `.venv/bin/python -m pytest tasks/t076 -q`. See [IMPLEMENTATION.md](data/IMPLEMENTATION.md) for file hashes, exact counts, source limitations, and validation evidence.
