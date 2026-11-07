# T021 implementation record

Status: **已通过 Sol 验收（2026-11-06）**.

## Reproduction

```sh
.venv/bin/python -m pytest tasks/t021/test_task.py -q
.venv/bin/python -m json.tool tasks/t021/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t021/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t021/sota.json > /dev/null
```

Run the saved human construction through the shared evaluator with the project
runner's normal command, or call `tasks.t021.check.validate` directly on
`tasks.t021.human.run_code()` and the configuration in `task.json`.

## Independent key quantity

There are \(32\cdot31/2=496\) unordered pairs. The checker derives each point
from rational parameters and computes squared distances as `Fraction` values.
For each positive rational squared distance \(q=a/b\), it bounds the energy
term directly as \(\sqrt{1/q}\). With \(r=b/a\), it sets
`k = isqrt(r.numerator*r.denominator*10^50)//r.denominator`; then
\(k/10^{25}\le\sqrt r<(k+1)/10^{25}\). It adds the floor of
\(k\cdot10^5\) to the lower sum and the ceiling of \((k+1)\cdot10^5\) to
the upper sum, in units of \(10^{-30}\). This gives a conservative full-pair
energy interval with short rational output and handles arbitrarily close
distinct points. A separate manual count gives 496 pairs; tests check that
count and compare the witness interval with the published rounded energy.

## Provenance and limits

The table reports 412.2612746 for N=32 and point group `I_h`, and links to the
archived coordinates. The archive is included verbatim as `data/ccd_32.xyz`.
Its SHA-256 is `967ce3e92de2ab459a28d473cb80a501c6efb2c8dd274a66ab9634e7fd44456c`.
The table cites Wales and Ulker, *Physical Review B* 74, 212101 (2006), DOI
10.1103/PhysRevB.74.212101.
The CCD result is a reported low-energy structure, not a proof of the global
minimum. Rationalizing the finite-decimal coordinates by stereographic
projection changes their geometry slightly. Therefore the strict interval
computed from this task's exact rational witness, rather than the source's
rounded decimal, is the reproduced score.

The 2026-10-27 author discussion at https://www.vals.ai/blogs/thomson-exposition
states that N=32 needs a new idea for a proof. AlphaEvolve maps to repository
problem 33, fixed commit `8f447457957deac61e28bf1676746f0753b3b2f8`, paper
section 6.18. Its N=32 result is not imported as a human baseline or score.
The frozen `human_reference` is the JSON float `412.2612746505293`, the float
representation of the certified upper endpoint. The CCD's printed
`412.2612746` remains recorded separately as the source report.

## Local result

The task test command completed with `6 passed`. JSON parsing completed for all
three task metadata files. The human witness returned the certified interval
`[4122612746505293102359058597/10000000000000000000000000,
4122612746505293102359059093/10000000000000000000000000]`, which is
approximately `[412.2612746505293102359058597,
412.2612746505293102359059093]`. Sol review passed. See acceptance.json.

Sol repeated the checks and accepted this configuration on 2026-11-06.
See acceptance.json for independent energy intervals and runner evidence.

## Added configurations accepted by Sol on 2026-11-07

- T021-C02 uses n=40. CCD table row: `40 | 660.6752788 | T_d | 40.xyz`.
- T021-C03 uses n=50. CCD table row: `50 | 1055.1823147 | D_6d | 50.xyz`.
- Original coordinate assets and a fetched HTML table snapshot are saved in `data/`. SHA-256 values are recorded in `data/ccd_added_sources.json` and the SOTA metadata.
- `human.py` interprets every decimal coordinate as an exact rational, applies the fixed rotation `(x,y,z)->(x,z,-y)`, then uses exact stereographic projection. The rotation avoids the chart pole for these source files. The resulting points satisfy the unit-sphere equations exactly. `check.py` uses integer square-root bounds for every pair and returns a conservative energy interval.
- Exact checked intervals: n=40: `[6606752788346224142901769349/10000000000000000000000000, 6606752788346224142901770129/10000000000000000000000000]`; n=50: `[10551823147262960991276699871/10000000000000000000000000, 1318977893407870123909587637/1250000000000000000000000]`.
- The CCD energies are rounded decimal comparison values. Rationalization changes the geometry slightly, so do not claim equality with those table values.
- Chen and Mehta (2014), §III, say deterministic results were known only for N=2, 3, 4, 5, 6, and 12. That supports treating 40 and 50 as unsolved. The CCD “Global Minima” title does not prove optimality.
- New configurations, source archives, and saved best witnesses are accepted by Sol on 2026-11-07. T021-C01 acceptance is retained.
