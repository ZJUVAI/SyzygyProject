# Current review status

**Accepted by Sol on 2026-11-04.** The new configurations are in `task.json`. The text below preserves the Luna submission and its source notes. Current results are in `records.json:configuration_records` and the expansion report.

# T044 configuration expansion

Luna submission status: `pending_sol_review`. C02 and C03 remain staged in
`configuration_expansion.json`; `task.json` still contains only the accepted
C01 configuration.

## Source and witness

The primary source is the [cube20 Golomb ruler page](https://cube20.org/golomb/).
It describes Singer, Bose–Chowla, and Ruzsa constructions and links the
`rulers-all-00` and `golomb-all-00` archives. The archive metadata records:

| Config | Marks | Public length | Method | Prime power | Multiplier | Modulus |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| C02 | 30 | 680 | projective-plane modular ruler | 29 | 71 | 871 |
| C03 | 32 | 784 | projective-plane modular ruler | 31 | 116 | 993 |

The corresponding `rulers-all-00.zip` rows supply the integer marks. The saved
data at `data/public_30_32.json` was extracted from those rows. I independently
checked the count, span, and all positive pairwise differences with the task
checker. The source page calls its large rulers “possibly optimal” and says the
authors are uncertain for larger sizes. No optimality proof is claimed here.
The public row does not identify a person as the witness author, so attribution
is left to the source's general construction account.

Source archive URLs:

- https://cube20.org/golomb/rulers-all-00.zip
- https://cube20.org/golomb/golomb-all-00.zip
- https://cube20.org/golomb/modrules-pp-00.zip

## Implementation

`check.py` validates the selected mark count and checks all `n(n-1)/2`
differences exactly. It ignores candidate score claims. The initializer reads
`MATHBENCH_CONFIG_ID`, uses no reference data, and builds a valid ruler by
adding the smallest next mark with fresh differences. The classical search
baseline has the same config awareness and uses no reference data. Human and
fixed-reference entry points load the exact selected public witness.

## Verification run

Commands run in the repository root:

```sh
.venv/bin/python -m pytest tasks/t044/test_task.py -q
python3 -m json.tool tasks/t044/configuration_expansion.json >/dev/null
python3 -m json.tool tasks/t044/records.json >/dev/null
```

Results on this checkout:

- `pytest`: 12 passed.
- Both JSON files parsed successfully.
- Default-seed bounded search returned valid rulers of length 1311 for C02 and
  1522 for C03. These are search outputs, not human references.
- Human and fixed-reference witnesses both recomputed to 680 and 784 in the
  per-config tests. The initializer also returned valid constructions for both
  configurations.

Sol must independently replay the human baselines, run cold seeds and the
classical search, and make the acceptance decision. The test commands do not
establish optimality.

## Sol acceptance, 2026-11-04

All four programs passed strict evaluation for each new configuration. Sol checked a cold seed export, independently recomputed a key quantity, rejected a damaged witness, and confirmed that a claimed score cannot change the score. Public record claims remain separate from reproduced witness scores.
