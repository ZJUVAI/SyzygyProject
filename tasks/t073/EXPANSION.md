# Current review status

**Accepted by Sol on 2026-11-04.** The new configurations are in `task.json`. The text below preserves the Luna submission and its source notes. Current results are in `records.json:configuration_records` and the expansion report.

# T073 configuration expansion: C02 and C03

Status: **待 Sol 验收**. The live `task.json` still lists only accepted C01 (L=100). The two new configurations are staged in `configuration_expansion.json` and must not enter the live registry before Sol review.

## Source rows and reconstruction

The primary source is the Dantus *Merit Factor Records* table, checked on 2026-11-04: <https://www2.chemistry.msu.edu/faculty/dantus/merit_factor_records.htm>. The page defines its sequence encoding as run lengths, starting with +1 and changing sign after each run. It says lengths with `*` were not determined by exhaustive methods and larger merit factors may exist.

- C02, L=80: row energy E=352, found 2003-02-06. The row has no individual discoverer citation. Its expanded signs are saved in `data/human_labs80_record.json`.
- C03, L=120: row energy E=872, found 2003-02-28. The row has no individual discoverer citation. Its expanded signs are saved in `data/human_labs120_record.json`.

Both rows have `*`. Attribution is unknown. The table is a historical record table; these values are not presented as current best results or as optimality proofs. For the minimum-energy objective, a higher merit factor means lower energy.

## Implementation and exact results

`check.py` recalculates each non-periodic autocorrelation as an integer and returns the sum of their squares. It ignores any candidate score. The initial program and the seeded single-bit simulated annealing baseline read the selected ID from `MATHBENCH_CONFIG_ID`. The search baseline does not load witness data. `human.py` and `reference.py` load the corresponding local witness. `task.json` is unchanged.

The task tests independently exercised both staged configurations. They confirmed lengths 80 and 120, exact energies 352 and 872, matching witness output, valid initial and classical baseline outputs, rejection of a truncated sequence, and rejection of a claimed score as a substitute for recomputation.

## Reproduction

From the repository root:

```sh
.venv/bin/python -m pytest tasks/t073/test_task.py -q
.venv/bin/python -m json.tool tasks/t073/configuration_expansion.json >/dev/null
.venv/bin/python -m json.tool tasks/t073/records.json >/dev/null
```

Test result: 7 passed. Both JSON checks passed. The classical baseline smoke checks use its fixed default 4,000 iterations. No full comparison or optimality search was run. These additions remain pending Sol review, including Sol's independent execution of the human and classical baselines and malformed-construction checks.

## Sol acceptance, 2026-11-04

All four programs passed strict evaluation for each new configuration. Sol checked a cold seed export, independently recomputed a key quantity, rejected a damaged witness, and confirmed that a claimed score cannot change the score. Public record claims remain separate from reproduced witness scores.
