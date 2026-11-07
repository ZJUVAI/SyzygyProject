# T091 implementation and verification

Status: `accepted_by_sol`.

## Sources and open status

- Carlet, Kiss, and Nagy, *Simplicity conditions for binary orthogonal arrays*, DOI [10.1007/s10623-022-01105-4](https://doi.org/10.1007/s10623-022-01105-4). The local PDF is `data/source/carlet_kiss_nagy_2023.pdf`, downloaded from the authors' publication copy. SHA-256: `77f9cc38166c80b07cae8777730ecf0281c2dff065a2676b77aa6c7f9f2870`.
- Remark 5 states that duals of double-error-correcting BCH codes provide the relevant binary orthogonal arrays. The local human/reference witness has 4096 rows.
- Proposition 10 and Remark 11 state a shortened Kerdock construction of 2048 rows at 63 columns, strength 4, and explicitly state that optimality is unknown. The paper's Rao bound is 2017 rows; divisibility by 16 strengthens it to 2032.
- Searches through 2026-11-06 for `F*(63,2,4)`, `F*(2^m-1,2,4)`, and `OA(2048,63,2,4)` found no later proof closing this 16-row gap. Sloane's orthogonal array directory was also checked.

## Construction and check

`human.py` rebuilds the BCH-dual array using the primitive polynomial `x^6+x+1` for GF(64). Column `i` is labelled by the 12 binary coordinates of `(alpha^i, alpha^(3i))`; all 4096 linear forms give the rows. The checker does not rely on a claimed array family or score. It builds 63 column bitsets and checks every nonempty parity character of size 1 through 4. The 637392 exact parity counts equal 2048. Binary Fourier inversion then gives all 16 patterns on each set of four columns exactly 256 times.

The standalone initializer greedily selects labels from F₂¹⁴, rejecting each label whose XOR with up to three prior labels is zero. Enumerating all 16384 linear forms gives a valid 16384-row seed with distinct rows. The traditional search independently runs the same generic selection rule in F₂¹³, yielding 8192 rows, then tests fixed seeded deletions of 16 rows. It does not import or read the BCH human/reference data. No proposal improved the 8192-row search seed. The generated best witness is stored under `best/T091-C01/`; the human/reference comparison files remain in `data/`.

## Validation commands

- `.venv/bin/python -m pytest tasks/t091 -q`
- `.venv/bin/python -m json.tool tasks/t091/task.json > /dev/null`
- `.venv/bin/python -m json.tool tasks/t091/sota.json > /dev/null`
- `.venv/bin/python -m json.tool tasks/t091/records.json > /dev/null`

The tests check the reproduced array, the distinct-row random-greedy initializer, acceptance of valid row repetitions, bit corruption, duplicate columns, malformed types and widths, the Rao/divisibility boundary, claimed-score invariance, all five `run_code()` entries, cold export, reproducibility, runner errors/timeouts, and evaluator execution with a temporary registry patch. `.venv/bin/python -m pytest tasks/t091 -q -x` passed 27 tests in 57.55 seconds. Validation used Python 3.13.12 on Linux with one numerical thread. The recorded run uses seed 0, 4098 label proposals, and 12 fixed row-deletion proposals.
