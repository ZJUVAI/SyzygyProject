# T019 implementation and review evidence

## Configurations and objective

- C01: `k=343`, frozen human/public reference diameter 2340.
- C02: `k=1000`, human/public reference diameter 7802.
- C03: `k=3000`, human/public reference diameter 26606.

The objective is to minimize the diameter `max(tuple)-min(tuple)`. A tuple is admissible when it has distinct integers and misses at least one residue class modulo each prime `p <= k`. For `p > k`, fewer than `p` entries cannot cover every residue class. The checker recomputes all conditions and ignores candidate-supplied objective fields. Configuration ID and `k` must agree.

## Source and exact replay

C02 source: `https://math.mit.edu/~primegaps/tuples/admissible_1000_7802.txt`.
SHA-256: `7666fa63333ffbbf0135016f4e6bc73b5b0cecf0e244ea4b865688cefe33af25`.

C03 source: `https://math.mit.edu/~primegaps/tuples/admissible_3000_26606.txt`.
SHA-256: `309f6d8c08c5ad821f7626e64bd20bec11ee2cb16a6557874eef815a26cc05a8`.

Each downloaded artifact contains exactly `k` integers, starts at zero, and has the listed exact diameter. Local JSON witnesses are line-for-line copies. The MathBases page (`https://mathbases.org/d/narrow-admissible-tuples`) describes the database range `k=2..5000`, full-tuple records, update date 2026-07-14, and markers for proven optima. The MIT `accepted.log` was downloaded with query parameter `?x=1` (the unqueried URL intermittently closed the proxy connection); it contains `currentRecord=yes`, accepted, validation-passed rows: k=1000/H=7802, submitter Engelsma; k=3000/H=26606, submitter xfxie. Both rows have blank `description`; proven rows use `description=optimal`. The filtered rows are saved in `data/mathbases_current_records.json`; downloaded accepted.log SHA-256 is `e4187eb3fb08d9f23e5708c27a1fcedd7e19c9008b8a3023afb33cc9011c0af3`. Neither new entry is marked proven optimal. These are checked same-parameter records, not optimality proofs.

## Cold start and search

C01 retains its accepted primorial-multiple seed. For C02/C03, the initial program generates the first `k` primes greater than `k`; each selected prime is greater than k, so no prime p <= k divides it, and every such modulus misses residue zero. It reads no witness and returns small finite diameters. The traditional baseline retains its greedy residue-preserving construction for C01. C02/C03 begin from the same generated finite-span prime seed as the cold initial program and try three full-tuple random replacements, keeping only exactly admissible improvements. The evolution search uses interval residue masks and exact final validation. A warm-start file is read only from an explicit runner-provided path. Formal run budgets remain 300 seconds generation, 60 seconds verification, 4 GiB, and one thread.

C02 and C03 are accepted by Sol on 2026-11-07. The test suite checks their downloaded same-parameter witnesses, exact diameter, tampered-score handling, configuration mismatch rejection, and cold-start feasibility at sampled parameters. All five programs and replay controls passed Sol review. See acceptance.json.
