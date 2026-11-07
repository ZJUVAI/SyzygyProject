# T068 implementation record

Status: `accepted_by_sol`.

The fixed task is to minimize the number of binary length-10 codewords whose Hamming balls of radius one cover all 1024 words. The checker verifies the complete universe exactly with 1024-bit integer masks.

The OEIS source file is stored at `data/source/oeis_a000983.txt`; the separate n=10 comparison witness is `data/reference/oeis_a000983_n10.json`, SHA-256 `65c8a7ec1574a64ef45e7334f8166966f70062cbf0ad09eb1499e5068842f8dd`. Parsing stops at the `a(11)` heading. Exact independent verification confirms 120 distinct codewords and coverage of all 1024 words.

The pinned OEIS text file has SHA-256 `d221fc00d230773ad7a696ec57b6cc1317d4492f2c594ecb8357477aa8d28900`. The exact 128-word Hamming-product baseline is saved at `data/human/hamming7_times_f2_3.json`; its SHA-256 is `e3aada0ead9ee0098d30776a53fbe932f7a7afcdfff4770ce80f6ba35b7b069f`.

The frozen human-method witness is the product of the `[7,4,3]` Hamming code and all 3-bit suffixes. It has 128 words. The traditional baseline uses greedy maximum-new-coverage set cover, then deletes redundant centers. It does not read the OEIS asset.

With seed 0, the baseline completed all eight shuffled trials in 0.416 seconds and returned a verified 135-word cover. The saved witness is `best/seed-0.json`, with replay and environment metadata in `best/seed-0.metadata.json`.

The checked lower and upper bounds are 107 and 120. OEIS A000983 and the current Kéri table both retain this range for n=10, radius 1. The 2020 OEIS list is not asserted to be the same construction as the 1991 Östergård mixed-code transformation.

Validation command:

```sh
.venv/bin/python -m pytest tasks/t068/test_task.py -q
```

Result: 15 passed in 2.62 seconds on Python 3.13.12, Linux x86_64. JSON syntax checks passed for `task.json`, `sota.json`, `records.json`, and the saved run metadata. The tests cover all five entries, the full public and human witnesses, duplicates and invalid values, ignored claims, seeded search, and runner error/timeout behavior through `mathbench.evaluate._run`.

Generation and verification use the shared 300-second and 60-second limits. The checker is exact and uses no additional dependencies.
