# T031 implementation evidence

Status: accepted by Sol on 2026-11-06.

## Sources and research status

- The fixed definition is a string over `1` through `7` that contains all 5,040 permutations as contiguous length-7 substrings. The objective is the string length, minimized.
- The 5,905 public word was downloaded from the attachment `5905_7_sol1.txt` in Andrei Teodorescu's 2026-08-17 Superpermutators post. The original attachment has 5,907 bytes because it includes whitespace. After removing whitespace, it has 5,905 symbols. Raw attachment SHA-256: `f0208fb0e8ea98b015799b8f0dfaadc58d5909bad4a089603f2c9c4768536f67`. Normalized word SHA-256: `98564c93f955c9256ca69c819e1b106a2be79e3286be2635d8374bc5595be6ac`.
- Andrew Balint wrote in the thread that he checked each of the four posted words and found all 5,040 permutations. This task independently checked the saved attachment. The post names a search program and kernel but does not disclose AI contribution. The task records this public record under `source_unattributed_records`.
- The human method baseline reimplements the Ashlock–Tillotson recursive construction. Houston's 2014 paper, Section 1, states the recursive construction and gives its length formula. The generated 5,913-symbol witness has SHA-256 `115550fd796c1db7babe54ea6fe1d9bd6b77530e2a8280030e9e7b89ac3f9ae2`. This is a weak same-parameter human-method baseline, not a record claim.
- The `jhalfar/superpermutations` lower-bound package says its 5,901 result is a computer-assisted proof whose Lean reduction depends on thirty search equations. Its 2026-11-01 README reports that twenty-three Lean equations are not evaluated, most of the associated searches used one program, and many run artifacts are absent. We do not mark that bound as a fully replayed certificate.
- The separate `jlebar/superperm7-ge-5898` release states `5898 <= s(7) <= 5906`, records 380 `native_decide` certificates, and documents a compiler/runtime trust base. Its README discloses AI-generated proof authorship. This provides a lower-bound artifact but does not close the optimization problem. The stronger 5,901 claim remains conditional in this task.
- Separately, the 2026 six-symbol `a(6)=872` repository still labels continuation abstraction (O5) and prune monotonicity (O6) open in its paper. It reports 190 of 208 prune sites certified, seven insufficient, and six previously failed sites repaired, while stating end-to-end certification still depends on O5/O6. This six-symbol claim is not evidence that the seven-symbol task is solved.

## Implemented files

- `check.py` enumerates all length-7 windows, accepts only windows that are permutations, and compares the set against all 5,040 required strings. It recomputes length and ignores declared scores.
- `init_program.py` is self-contained. It concatenates the 5,040 permutations and returns a valid 35,280-symbol word.
- `human.py` rebuilds the recursive 5,913-symbol Ashlock–Tillotson word. `data/reference/human_ashlock_tillotson_5913.txt` stores the generated witness.
- `baseline.py` runs eight seeded randomized maximum-overlap greedy searches. It reads no comparison witness. Seed 0 produced a best word of length 6,240 in about 0.092 seconds on the implementation machine. The exact result, checker output, and run settings are saved in `best/greedy_seed0_*.json`.
- `reference.py` reads the fixed 5,905 public attachment from `data/reference/public_5905_attachment.txt`. The 5,913 human witness is saved at `data/reference/human_ashlock_tillotson_5913.txt`. The `best/` directory contains only the task's own search result and its verification/provenance records. It is not imported by the initial seed or search baseline.
- `evolution.py` exposes the required `run_code()` entry point.
- The implementation-stage registry error was resolved by Sol admission. All five shared-runner entries and the complete control checks passed; see records.json.

## Verification commands and results

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t031/test_task.py -q
.venv/bin/python -m json.tool tasks/t031/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t031/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t031/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t031/records.json > /dev/null
```

The task test suite passed (7 tests in 0.54 seconds) and covers the exact 5,905 witness, the 5,913 human-method witness, the simple seed, a repeated valid word, a missing-window word, invalid symbols and types, altered configuration, ignored scores, deterministic seeded search, and generation error/timeout reporting. The JSON formatting commands all exited successfully.

## Limits and open review points

- The lower-bound artifacts are computer assisted. The 5,901 package has unevaluated equations and incomplete independent search replay, so this implementation does not present it as a fully checked proof.
- The 5,905 public result has no AI provenance disclosure in the inspected post.
- The human construction is independently reconstructed from the published recursive rule. It is not an archived transcription by the original authors.
- Sol must review the literature state, saved witnesses, exact checker, and results before this configuration is accepted.
