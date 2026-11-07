# T009 implementation notes

## Configurations and sources

T009-C01 remains the accepted `[68,15]` instance. T009-C02 `[80,20]` and T009-C03 `[100,20]` are new and accepted by Sol on 2026-11-07.

The maintained [Grassl BKLC parameter page for `[80,20]`](https://www.codetables.de/BKLC/BKLC.php?k=20&n=80&q=2) reports construction distance 25 and bounds `25 ≤ d_max ≤ 30`. It gives three generator polynomials for a degree-three quasi-cyclic `[81,20,26]` code, then punctures coordinate 81. The [page for `[100,20]`](https://www.codetables.de/BKLC/BKLC.php?k=20&n=100&q=2) reports distance 34 and bounds `34 ≤ d_max ≤ 40`. It gives a `[99,20,34]` QC code from three polynomials, then appends one zero coordinate. Both pages attribute the QC codes to Chen Zhi, “Six New Binary Quasi-Cyclic Codes” (1994), [DOI 10.1109/18.333888](https://doi.org/10.1109/18.333888).

The exact-parameter pages expose the bounds and constructions; their code records have a 2001 modification date. On 2026-11-07, the public Magma 2.30-1 calculator returned distances 25 and 34 for `BestKnownLinearCode(GF(2),80,20)` and `BestKnownLinearCode(GF(2),100,20)`, matching the pages. The upper bounds remain 30 and 40. These are best-known status checks, not proofs that no unreported code exists. Both instances remain open.

## Matrix reconstruction and exact checks

`qc.py` stores the source polynomial exponents. For block length `m`, it forms the vector `(g0,g1,g2)` over `GF(2)[x]/(x^m-1)` and builds its `m` simultaneous cyclic shifts across three blocks. Gaussian elimination over GF(2) selects a deterministic independent-row basis. It then punctures coordinate 81 for C02 or appends a zero column for C03. Both matrices have rank 20.

The local checker enumerates all `2^20-1 = 1,048,575` nonzero messages for each matrix. It computes exact integer bit weights and returns distance 25 for C02 and 34 for C03. The saved SOTA matrix hashes are:

- C02: `68982b46a4cc81a38bc018c179161edf2f83c114ada7bbd7cd5c6ecb924e6189`
- C03: `9bf8dbee63eb97861252addea666efb5c5b9035208eb8b3a792fb9c27f924684`

`human.py` rebuilds these matrices from the polynomials. `sota.py` loads the fixed saved matrices; `reference.py` loads those same independently verified public matrices for C02/C03 and keeps the existing C01 reference unchanged. Thus the reference objectives are 25 and 34 on the new configurations, matching the `reproduced_value` entries in `sota.json`. The separate 19/26 search outputs are retained only as diagnostics and are not reference assets. The initial program uses `[I_k | 0]` and does not read reference data. The traditional search mutates systematic parity columns and exactly checks all nonzero words after each proposal. It uses seed 0 and five proposals for each new configuration. The recorded run took 4.61 seconds for C02 and 5.47 seconds for C03 on CPython 3.13.12, Linux, CPU only. C01 retains its existing search settings.

The evolutionary entry uses the existing C01 spectrum search for C01. For C02 and C03 it calls the configuration-aware systematic parity search and records that method. It does not load a witness or use a claimed score.

## Run settings

Each candidate generation has a 300 second limit; exact verification has a 60 second limit. Memory is 4 GiB and the thread count is one. Example C02 replay:

```sh
MATHBENCH_CONFIG_ID=T009-C02 .venv/bin/python -m mathbench evaluate T009 tasks/t009/sota.py --strict --config T009-C02
```

New configurations are accepted by Sol on 2026-11-07 and do not inherit C01 acceptance.
