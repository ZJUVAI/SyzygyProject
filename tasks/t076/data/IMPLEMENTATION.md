# T076 implementation and evidence

## Status

`T076-C01` remains accepted by Sol under its existing acceptance record. This file records its implementation evidence and does not change that record.

## Definition and checker

T076-C01 fixes `n=15`. A valid construction has exactly 15 distinct positive integers and exactly 32,768 distinct subset sums, including zero. The objective is the largest element, which is minimized. `check.py` binds the configuration ID to its full parameter object. It traverses subsets in Gray-code order with exact integer sums. Modular fingerprints are bucket keys only; the checker recomputes exact sums to resolve collisions. It ignores claimed score fields and has no magnitude cap.

## Human and public witnesses

The human witness is generated from the Conway-Guy recurrence and the set formula in Bohman (1998), §2 and Theorem 2.1. Its maximum is 8,807. The public witness is Sharp's 15-element construction transcribed from the OEIS A276661 A-file. Its maximum is 8,635. Both witnesses are checked by enumerating all 32,768 subset sums. The source does not disclose whether AI assistance was used for the public witness.

The reviewed bounds are `7060 <= a(15) <= 8635`; no exact minimum was located in the sources reviewed. The lower bound is the sum of central binomial coefficients recorded in `bestknown.json`. The cited bandwidth theorem was not re-proved locally.

## Search and cold start

`init_program.py` returns the powers-of-two construction and reads no comparison witness. `baseline.py` runs a deterministic, seed-controlled sweep of descending greedy constructions. It reads no human or reference assets. `evolution.py` calls this search entry. `human.py` reconstructs the Conway-Guy witness from its recurrence. `reference.py` loads the fixed public witness.

## Validation

Run `python -m pytest tasks/t076 -q`. Tests cover the initial, search, human, and reference entries; exact subset-sum validation; rejection of invalid constructions; ignored claim fields; large decimal inputs; repeatable search; and runner failure and timeout handling. The preserved per-run results and review evidence are in `bestknown.json`, and `best/`.
