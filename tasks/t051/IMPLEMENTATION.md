# T051 implementation evidence

Status: accepted by Sol on 2026-11-06.

## Fixed task

T051-C01 maximizes the length of an unrestricted `{-1,+1}` sequence with discrepancy cap 3. The checker enumerates every difference `d=1,...,N` and every prefix that ends at a multiple of `d`. It adds signs with Python integers, rejects a prefix as soon as its magnitude exceeds 3, and returns the sequence length as the exact objective. For the 130000-sign witness, it checks 1550902 progression prefixes.

## Human and public construction

- Primary report: Konev and Lisitsa, [arXiv:1405.3097v2, §4](https://arxiv.org/html/1405.3097v2), and the [author data page](https://cgi.csc.liv.ac.uk/~konev/edp/), checked 2026-11-06. The paper reports an unrestricted length-130000 C=3 sequence and says its first 127600 terms are completely multiplicative.
- The author's compressed sequence URL was not directly downloadable in this environment. A public notebook on [Wolfram Community](https://community.wolfram.com/t/discrepancy-conjecture/6798) discussing this problem was recovered; the discussion refers to Konev-Lisitsa's paper and author data page. Notebook SHA-256: `cc6066cefd3c28435aee484b8ad4c952f6d17919732acc5e21a412ed45cadbca`.
- Notebook-decoded sign text SHA-256 excluding the final newline: `a46775e377eed611fe5e7c086fc761ea8aeec22c2048924c2cd28392f34883fa`. Stored source and reference files include a final newline and both have SHA-256 `024af56550adebd499df5c4e857453f518655e7e175af6e8d8a017e047f754c2`.
- The recovered sequence has exactly 130000 signs, each `-1` or `+1`. An independent exact check found discrepancy 3 and checked all 1550902 prefixes. A second check confirmed complete multiplicativity through index 127600. We do not assert that this notebook recovery is byte-identical to the author's original compressed download.
- The literature also reports maximum 1160 for unrestricted C=2 and maximum 127645 for completely multiplicative C=3. Those are different problems. Tao's infinite-sequence theorem does not give the finite maximum. The checked 2026 Princeton thesis treats the C=2 case and does not close unrestricted C=3. The selected finite maximum remains open in the checked sources; 130000 is a feasible lower bound, not a proved optimum.

## Programs, output, and tests

- `init_program.py` returns the valid seed `[1]`.
- `baseline.py` uses seed 0, 24 fixed greedy extension trials, and a 5000-term cap by default. Each trial stops when neither sign preserves all new divisor-ending prefixes. It reads no human/reference data. `evolution.py` exposes the required `run_code()` and uses the same task-qualified baseline.
- The frozen baseline run is saved under `best/T051-C01/`. It returned length 55 after 24 trials and 806 attempted extensions. Strict runner verification confirmed discrepancy 3. On Python 3.13.12/Linux, generation took 0.696 s and verification took 0.552 s. The runner enforced 300 s generation, 60 s verification, 4 GiB memory, and one thread. `result.json` SHA-256: `21fae22d065b21bdabe72a48dc19d3282a35a17e94d19ed11c7491cc4ea86649`; `solution.json` SHA-256: `f12d7bd8d78ed1a33d92c835211f9c3355d8e69db6b8bc68043b86db97390a88`.
- `human.py` and `reference.py` load only their respective task-local text data. Their outputs match and both score 130000.
- `check.py` rejects empty sequences, non-integer signs, booleans, floats, non-finite values, and signs outside `{-1,+1}`. It enforces the fixed configuration. It ignores optional objective, score, and claimed-score values and always reports `claimed_objective_ignored: true`.
- `test_task.py` exercises all five program entries, independently recomputes the 130000-sequence discrepancy and prefix count, verifies saved text hash, tests malformed and invalid sequences, checks forged-score invariance, and tests `_run` worker errors and timeout handling without changing the shared registry.

Commands run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t051/test_task.py -q
.venv/bin/python -m json.tool tasks/t051/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t051/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t051/records.json > /dev/null
```

Result: `12 passed in 3.38s`; all three JSON files parsed. A separate strict run through `evaluate_candidate` returned valid score 55 and exact verification. To avoid changing the shared registry, the in-process call supplied the T051 config and task path directly to the evaluator; the evaluator still ran generation and verification in its isolated workers.

## Remaining review points

- This is a feasible public construction, not a finite optimality proof. The exact maximum of unrestricted discrepancy-3 sequences is not claimed known.
- Confirm the linked notebook's attribution and provenance description. Its complete data were recovered and mathematically verified, but the original compressed archive was not reproduced byte-for-byte.
- Sol should independently run the human and reference programs, check a deliberately invalid sequence, recompute the objective, and verify that forged score fields do not affect the result.
