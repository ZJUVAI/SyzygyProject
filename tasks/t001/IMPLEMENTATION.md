# T001 expansion implementation report

Status: **pending Sol review** for T001-C02 and T001-C03. The original T001-C01 entry in `task.json` is unchanged. The new configuration metadata is staged separately in `configuration_expansion.json`.

## Implementation

- `check.py` validates C01/C02/C03 with exact rational boundary and pair-distance checks. The objective comes from the supplied radius; candidate score fields are ignored.
- `init_program.py` creates a deterministic exact grid selected by `MATHBENCH_CONFIG_ID`.
- `baseline.py` provides bounded seeded SLSQP multistart search. It uses the exact checker before accepting a candidate and falls back to the grid.
- `human.py` and `reference.py` replay task-local files. C02 uses a local copy of the saved 32-circle construction from T005; C03 uses a local copy of Packomania's n=50 coordinate text, translated into the unit square and checked after reducing its radius by `10^-10`.
- `EXPANSION.md` and `records_expansion.json` state source URLs, cutoff date, exact reproduced values, attribution gaps, and that these feasible constructions do not prove optimality.

## Validation

Commands run:

```sh
python3 -m json.tool tasks/t001/configuration_expansion.json >/dev/null
python3 -m json.tool tasks/t001/records_expansion.json >/dev/null
.venv/bin/python -m pytest tasks/t001/test_task.py -q
```

The JSON parser checks passed. The task test command completed successfully (all test cases passed). Tests cover all three configurations, both saved witnesses, grid feasibility, exact objective recomputation, corrupt boundary and overlap cases, non-finite and Boolean inputs, ignored claimed objectives, and staged/live metadata separation. n=32 has 496 pair checks; n=50 has 1,225 pair checks. Sol review must independently replay the witnesses and baselines before acceptance.

## Open items

- Packomania's detailed source attribution for n=32 was not independently resolved.
- The author and year behind Packomania reference [14] for n=50 were not resolved. The implementation does not invent an attribution.
- No claim is made that either packing is globally optimal. The current record evidence is limited to the cited Packomania sources checked on 2026-11-04.
