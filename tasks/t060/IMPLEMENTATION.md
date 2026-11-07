# T060 implementation and source review

Status: **已通过 Sol 验收（2026-11-06）** (`accepted_by_sol`).

## Configuration and mathematics

- Configuration: `T060-C01`, target `M61 = 2^61 - 1 = 2305843009213693951`.
- Objective: minimize the number of `1` leaves in a binary expression tree using only addition and multiplication. Shared subtrees, subtraction, and exponentiation are excluded.
- Exact lower bound: Selfridge's extremal formula gives `E(115) = 1801135623563989452 < M61` and `E(116) = 2701703435345984178 > M61`. The checker computes these with integer powers, without logarithms or floating-point arithmetic. Therefore at least 116 leaves are required.
- Human comparison: base-3 Horner reconstruction, 39 digits, 153 leaves. The saved expression was generated independently and exactly checked. This is a traditional method reconstruction, not a literature record.
- Public comparison: 127 leaves, exact expression in `data/reference/public_127_expression.json`. SHA-256: `946a56e064e60422f49c98aeeb0ceae0a99c22d5070318a7b84fcbca28699449`.
- Own search result: `best/search_seed_0.json`, 166 leaves from 1,000 seeded mixed-radix candidates. This file contains only a result produced by this task's search.

## Sources checked

- Altman, “Integer complexity: the integer defect,” *Confluentes Mathematici* 8(3), 2019. It states Selfridge's exact extremal formula and recalls Horner construction. https://msp.org/cnt/2019/8-3/moscow-v8-n3-p01-s.pdf
- EventCompute, “Integer complexity of 2^61−1: 127 ones.” Its expression is a feasible construction, not an exact complexity proof. The page describes generative AI assistants in its research process. https://eventcompute.com/en/challenges/integer-complexity-m61/
- Board repository snapshot `math-market/integer-complexity-m61`, commit `394bec0d2c976a967414d95388ca2e024ce19dd1`.
- Board PR #4, head `6b79a6324891b4b196731f78fcd7a9b978524b25`, checked 2026-11-06; open, not merged. https://github.com/math-market/integer-complexity-m61/pull/4
- The board's 150-one expression is a challenge baseline, not a record; AI provenance is unstated.
- The cited page and board state were checked on 2026-11-06. The sources support `116 <= complexity(M61) <= 127`; no exact value proof or shorter same-target witness was found in that bounded review. This is not a claim of an exhaustive web survey.

## Programs and isolation

- `init_program.py`: standalone binary Horner seed, 181 leaves. It has paired EVOLVE markers and no task imports.
- `baseline.py`: evaluates 15 fixed-radix Horner expressions (radices 2 through 16), returning a valid 153-leaf expression for the default run.
- `evolution.py`: fixed-seed mixed-radix Horner enumeration, 1,000 candidates by default. The recorded seed-0 run returns 166 leaves.
- `human.py`: reconstructs the 153-leaf base-3 expression from the integer's digits; it reads no saved expression.
- `reference.py`: loads the fixed public 127-leaf comparison expression.
- The initial and search programs do not import `human.py` or `reference.py` and do not read comparison data. The test suite checks those import boundaries.
- `check.py` accepts only the declared expression grammar, evaluates with exact Python integers, counts all `1` leaves, and ignores candidate score fields. It limits expression length and uses explicit stacks, so deeply nested valid input does not rely on Python recursion.
- The 100,000-character limit is an input resource bound, not a mathematical constraint or a guarantee for arbitrary redundant text. Any binary tree with `k` leaves can be written fully parenthesized in at most `4k-3` characters; that is 609 characters at the 153-leaf human baseline. The saved compact base-3 witness is 505 characters.

## Validation

Command:

```sh
.venv/bin/python -m pytest tasks/t060 -q
```

Result: **38 passed**.

Coverage includes all five `run_code()` entries, public and human witness replay, exact lower-bound arithmetic, cold exported seed, malformed and wrong-value expressions, repeated subexpression leaf counting, large nesting, target/configuration rejection, non-finite or forged claimed scores, fixed iteration reproducibility, explicit zero-second cutoff, and runner program-error/timeout behavior via `mathbench.evaluate._run`.

JSON files were parsed with `python3 -m json.tool`. The public expression file hash matches the cited fingerprint. The five program results were recomputed by the task checker: seed 181, baseline 153, human 153, reference 127, and evolution 166.

## Unresolved points

The exact integer complexity of M61 remains unknown in the sources checked. The public 127 expression is AI-assisted and is a feasible construction only. The human 153 baseline is a transparent reconstruction of a standard positional method, not a claim that a publication reports 153 as a record. The evolution search did not beat the 127 public construction.
