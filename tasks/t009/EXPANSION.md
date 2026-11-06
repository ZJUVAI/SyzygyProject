# Current review status

**Accepted by Sol on 2026-11-04.** The new configurations are in `task.json`. The text below preserves the Luna submission and its source notes. Current results are in `records.json:configuration_records` and the expansion report.

# T009 staged configuration expansion

Luna submission status: **pending Sol review**. C03 (n=17) and C04 (n=19) are implemented in this task package but are not active in `task.json`.

The coordinate lists are `data/spherical_code_3_17.txt` and `data/spherical_code_3_19.txt`, copied on 2026-11-04 from the public [`n=17`](https://spherical-codes.org/data/3/17) and [`n=19`](https://spherical-codes.org/data/3/19) endpoints. The source table cites Danzer (1986) and Lazic et al. (1987). Coordinates are stored as decimal strings and parsed as exact rational inputs. The score applies to these archived decimal inputs, not unrounded source values.

Strict checker results:

| Config | n | Pair count | Certified angle interval (radians) | Human reference |
|---|---:|---:|---:|---:|
| T009-C03 | 17 | 136 | [0.8916944491515696, 0.8916944491515711] | 0.8916944491515696 |
| T009-C04 | 19 | 171 | [0.8323809277763071, 0.8323809277763087] | 0.8323809277763071 |

The interval lower endpoint is both the conservative maximize score and the human reference. `init_program.py` creates a deterministic Fibonacci-sphere seed for the selected config. `baseline.py` uses deterministic multistart numerical optimization and reads no witness files. `human.py` and `reference.py` read the archived public coordinates. The checker validates every pair and ignores claimed scores. It rejects zero, duplicate, or same-direction points and malformed coordinates.

## Validation

- `.venv/bin/python -m pytest tasks/t009/test_task.py -q` — 6 passed.
- The shared evaluator cannot resolve staged IDs until they are accepted into `task.json`; do not treat that limitation as a completed evaluator run.

Local tests cover the witnesses, strict intervals, pair counts, damaged constructions, wrong sizes, malformed values, mismatched parameters, and a tampered score. The checker certifies feasibility and score intervals. It does not prove optimality.

## Sol acceptance, 2026-11-04

All four programs passed strict evaluation for each new configuration. Sol checked a cold seed export, independently recomputed a key quantity, rejected a damaged witness, and confirmed that a claimed score cannot change the score. Public record claims remain separate from reproduced witness scores.
