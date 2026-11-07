# T063 implementation and reproduction record

## Configuration

`T063-C01` is the exact-degree-100 problem over primitive irreducible integer polynomials. The domain is not restricted to reciprocal, sparse, or monic polynomials. The objective is the Mahler measure, minimized. The non-cyclotomic condition is checked by proving the measure interval has lower endpoint greater than 1.

## Sources and comparison witness

- Mossinghoff, [Mahler Measure Database](https://github.com/mossinghoff/Mahler-Measure-Database), pinned commit `7e3798516710370a758e16eb5de6bccbee98bb6a`, file `BestByDegree_200.txt`, degree-100 row. The source row reports `1.247365098370`, `v=8`, and 51 reciprocal coefficients. The repository does not describe the row's degree-specific search process.
- Source-row and expanded-polynomial data: `data/source/mossinghoff_degree_100_row.json`.
- Certificate-backed reference: `data/reference/mossinghoff_degree_100_certificate.json`, SHA-256 `fb01470875be798525b061a301e401dffa3bab18c50de35d6816defda976afb3`.
- Chervonyi, Gukov, and Luong, [arXiv:2610.30277v1](https://arxiv.org/html/2610.30277v1), submitted 2026-10-21, §1 and §3.3/Table 4/§6. The paper describes an AI-assisted workflow at project level. It reports matching 85 of 91 literature values and strict improvements at degrees 178, 188, 190, 202, 242, and 250; it lists no degree-100 improvement. This is kept separate from the older Mossinghoff record. The paper reports optimality proofs only through degree 54.

The published decimal is a rounded record, not an exact score. The independently certified upper endpoint for this witness is `1.2473650983705...`; the frozen comparison value is rounded upward to `1.247365098371`. The degree-100 minimum remains open.

## Certificate method

The reference polynomial is reciprocal, so root enumeration used the reduction `P(z) / z^50 = Q(z + 1/z)` to solve a degree-50 polynomial and map its roots back to 100 proposed complex centers. SymPy produced 110-digit proposals; centers were rounded to rationals with denominator `10^24`; all disks use radius `10^-15`. These numerical operations only propose the disks.

The checker then uses exact rational arithmetic to prove, for each center `c` and radius `r`,

`r * lower(|P'(c)|) > upper(|P(c)|) + r^2/2 * sum(k(k-1)|a_k| R^(k-2))`,

where `R` is a rational upper bound on `|c|+r`. Rouché's theorem gives exactly one root per disk. Exact pair checks prove the 100 disks are disjoint; together they cover all degree-100 roots. Rational modulus bounds then give a certified interval for the full Mahler measure. The observed relative interval width is about `9.96e-14`, below the required `1e-10`. The checker returns the rational upper endpoint. Root-disk precision has no fixed ceiling; normal runner data and memory limits apply.

The checker also proves content 1 and exact irreducibility over `Q` with SymPy. The x^100-2 start is Eisenstein at 2, but the checker does not rely on that shortcut. No floating-point root computation contributes to the accepted objective.

## Programs and controls

- `init_program.py`: self-contained, valid `x^100-2` seed with proposed root disks. It does not import task code or comparison data.
- `baseline.py`: fixed-count prime scan of `x^100-p`. Eisenstein proves irreducibility for prime `p`, and the family's Mahler measure is `p`. It does not read the comparison witness.
- `evolution.py`: seeded mutation and elitist selection in the same prime-constant family. Defaults: 60 iterations per restart, 4 restarts; `MATHBENCH_EVOLUTION_ITERATIONS` and `MATHBENCH_RESTARTS` permit bounded changes. This is a transparent traditional-search baseline, not a competitive general search over all degree-100 polynomials.
- `human.py`: reconstructs the published Mossinghoff row from the saved reference certificate.
- `reference.py`: fixed replay of the same public polynomial.

All entries read the fixed configuration and seed. Search defaults use fixed iteration counts. `MATHBENCH_SEARCH_SECONDS` enables the shared exploration cutoff. The standard evaluator limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one thread.

## Reproduction environment and commands

Environment: Python 3.13.12, Linux x86_64, repository `.venv`.

Commands:

```sh
.venv/bin/python -m pytest tasks/t063 -q
.venv/bin/python -m json.tool tasks/t063/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t063/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t063/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t063/data/source/mossinghoff_degree_100_row.json > /dev/null
.venv/bin/python -m json.tool tasks/t063/data/reference/mossinghoff_degree_100_certificate.json > /dev/null
```

The public witness was also checked through `mathbench.worker` in a separate process with the 4-GiB limit, one CPU, and a 60-second verification timeout. It completed in about 14.6 seconds and returned `certified`, 100 Rouché disks, 4,950 disjointness checks, and relative interval width `9.9564e-14`. The suite tests each program entry, valid and invalid coefficient/disk data, duplicate disks, degree boundaries, bool/float/NaN inputs, arbitrary-length rational strings, claimed-score invariance, worker errors, and worker timeouts.

The baseline and evolution programs are reproducible with seed `0`; the test suite sets 2 iterations for the scan, 2 generations and 1 restart for evolution. Default budgets are recorded above. Direct shared-runner `evaluate()` admission is deferred until Sol registers this configuration; the separate trusted worker check and `_run` error/timeout controls were exercised locally.

## Status and limitations

Implementation is `accepted_by_sol`. The construction proves an upper bound only. No proof shows that a degree-100 primitive irreducible polynomial with smaller measure does not exist. The traditional baseline explores only the Eisenstein family `x^100-p`; it is not a global search baseline. The Mossinghoff source does not document its degree-100 search details, and the 2026 paper does not give a degree-specific provenance statement for this matching old record.
