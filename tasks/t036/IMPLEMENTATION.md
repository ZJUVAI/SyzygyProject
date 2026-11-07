# T036 implementation evidence — accepted by Sol on 2026-11-06

## Scope

Implemented only configuration T036-C01 (K28, minimize crossing pairs). The checker accepts integer and canonical rational-string coordinates and uses exact `Fraction` orientation tests. It checks every point triple for general position, then counts all three disjoint-edge pairings on each four-set. The human construction uses `(i,i^2)` and has `binom(28,4)=20,475` crossings.

## Sources and open status

The Lovász–Vesztergombi–Wagner–Welzl paper supports the convex four-set construction. The 2011 Abrego–Fernández-Merchant–Salazar survey says 28 remains open. The numeric interval 7,233–7,234 is recorded in Abrego’s own 2008-05-05 comment on OEIS A014540; the 2024 DMTCS paper also says only orders through 27 and 30 are solved. Current MathWorld cites Schaefer (2026), p. 86, and still calls K28 the smallest unresolved case with value 7,233 or 7,234. The public 7,234 point set was not obtained or replayed. No later proof was found in the source review supplied for this implementation. The stronger public claim is recorded as reported, not reproduced. Review date: 2026-11-06.

## Validation

- Checker suite: `.venv/bin/python -m pytest tasks/t036/test_task.py -q` — passed (11 tests).
- Human and reference programs: `.venv/bin/python -c 'from tasks.t036.human import run_code; from tasks.t036.check import validate; print(validate(run_code(), {"id":"T036-C01","parameters":{"vertices":28,"graph":"complete graph K28","general_position":"no three points collinear","crossing_definition":"unordered pairs of disjoint straight edges whose relative interiors intersect"}}))'` — passed; exact objective 20,475; all 3,276 triples and 61,425 edge-pairings checked.
- Search baseline: seed 0, 80 single-point replacement attempts, exact validation after each proposed move; replay command and outcome are in `best/seed0_search_provenance.json` — seed 0 completed 80 attempts, accepted 16 replacements, and scored 12,516. Exact result and metadata are saved in `best/`. Sol review remains pending. The exported evolution entry also ran directly and returned a valid 12,516-crossing drawing; the simple initial entry returned a valid 20,475-crossing drawing.
- Program-error and timeout behavior remains provided by the shared candidate runner. This local task test covers valid/invalid constructions, duplicates, rational and malformed coordinates, exact orientation boundaries, and ignored score claims.

Default runner budget: 300 seconds generation, 60 seconds verification, 4 GiB virtual memory, one numerical thread. Configuration status remains `accepted_by_sol`.

Main source correction: the retrieved 2011 survey has Table 1, no Table 3. It supports open status, while the numeric7233–7234 interval is attributed to Bernardo M. Abrego’s first-party comment at https://oeis.org/A014540/internal . The current crossingconstants page concerns asymptotic constants and is not cited as a K28 table. FrozenH20475 is a reconstructed weak convex-position formula; reported besthuman7234 remains unverified locally.
