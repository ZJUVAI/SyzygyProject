# T073 implementation record

## Accepted configuration

C01 (L=100) is accepted by Sol. Its existing witness, score, provenance, and review record remain unchanged.

## Pending expansion

C02 (L=80) and C03 (L=120) are staged in `configuration_expansion.json`. Their implementation and evidence are documented in `EXPANSION.md`. Their status is **待 Sol 验收**. They have not been added to `task.json` or the accepted configuration count.

## Validation performed

- `.venv/bin/python -m pytest tasks/t073/test_task.py -q` — 7 passed.
- `.venv/bin/python -m json.tool tasks/t073/configuration_expansion.json` — valid JSON.
- `.venv/bin/python -m json.tool tasks/t073/records.json` — valid JSON.
- Source checked: Dantus, *Merit Factor Records*, <https://www2.chemistry.msu.edu/faculty/dantus/merit_factor_records.htm>, checked 2026-11-04. The 80 and 120 rows give energies 352 and 872. Both carry the source's asterisk for records not determined by exhaustive methods. Individual discoverers are not named.

Tests recomputed the exact objectives from expanded signs. They checked configuration-aware seeds and classical baseline outputs, matching human/reference witnesses, malformed lengths, and an altered claimed score. The checker uses integer arithmetic over every aperiodic lag.

## Limits and required review

The source table is historical. It does not prove current-record status or global optimality. The new rows do not state individual attribution. The task tests do not replace Sol's required independent baseline run and review. Keep both configurations pending until that review is complete.
