# T071 implementation record

Status: `accepted_by_sol`.

The fixed configuration is a binary length-16 code correcting one deletion. A candidate is valid when no two distinct codewords share any length-15 string obtained by deleting one bit. The checker forms every distinct one-deletion output and checks pairwise disjointness exactly. It does not assume that each codeword has 16 distinct outputs.

The frozen VT_0(16) witness is stored at `data/reference/vt16_3856.json`, SHA-256 `f28bab01ad058ae1c17cd311d102f72fea1dad9cdc77815fd99a5f373eebf2ae`. The human asset is a separate copy at `data/human/vt16_3856.json` with the same hash. The formula program independently reconstructs all 3,856 words from the checksum modulo 17, and the checker confirms their deletion outputs are disjoint.

The 2026 paper, arXiv:2504.00613v2, §1 and §2.2 says VT codes are conjectured maximum for all finite lengths and that optimality is proved only for n≤11. Its §5.1 Table 1 records 3,856 at n=16 for VT_0 and an LP upper bound of 4,202. The same paper reports an AI-assisted priority-function rediscovery proved equivalent to VT_0; it reaches the same 3,856 and does not prove the n=16 maximum. Classical and AI-assisted provenance are recorded separately.

The initial program returns the valid one-word code `{0}`. The fixed-seed traditional baseline greedily scans two random permutations of all 65,536 words, adding a word only if all its deletion outputs are new. Seed 0 yielded 1,941 codewords after 131,072 candidate visits in 0.992 seconds. The verified witness is saved in `best/seed-0.json`; the replay command and environment are in `best/seed-0.metadata.json`. The baseline does not read either comparison witness.

Validation command:

```sh
.venv/bin/python -m pytest tasks/t071/test_task.py -q
```

The tests cover all five entries, the exact VT checksum witness, repeated deletion outputs within a word, a deliberately colliding pair, duplicates, invalid types and ranges, ignored claimed scores, repeatable seeded search, and `_run` error/timeout behavior without changing the task registry. Default generation and verification budgets are 300 and 60 seconds, with 4 GiB and one thread.

Result: 15 passed in 24.29 seconds on Python 3.13.12, Linux x86_64. JSON syntax checks passed for the task definition, SOTA, records, and saved run metadata. `git diff --check -- tasks/t071` passed.
