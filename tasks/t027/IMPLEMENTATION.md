# T027 implementation record

Status: `accepted_by_sol`.

## Implemented

- Fixed QAPLIB `tai256c`, `n=256`, with SHA-256-pinned integer matrices.
- Exact permutation checker; it validates all indices and recomputes the integer objective over 65,536 terms.
- Self-contained identity seed, bounded randomized first-improvement pair-swap baseline, evolution entry point, public-witness replay, and task interface wrapper.
- Bilingual task README, model instruction, records, and configuration-level SOTA record.

## Source and witness checks

- Downloaded the versioned Debian `r-cran-qap` 0.1-1-2 matrix and solution files. Hashes are in `data/README.md` and `sota.json`.
- Parsed dimensions and the archived one-based permutation. It is a bijection on 1..256.
- Recomputed the objective exactly with integer arithmetic: 44,759,294; this matches the `.sln` score and QAPLIB table entry.
- QAPLIB labels the feasible record ANT. QAPLIB history identifies T. Stützle as providing an improved tai256c solution in 1997. The archive witness is reproduced; the original search is not.
- The authoritative arXiv version page identifies v2 as last revised 2024-09-30; the v2 PDF title page says 2024-10-01. The paper body reports LB 44,200,000 and a 1.25% gap. Its abstract retains the earlier 1.48% gap.
- The checked QAPLIB pages disagree on the older LB: Lehigh lists 43,849,646 and the QAPLIB mirror lists 44,095,032. The paper treats 44,095,032 as the previous LB and reports 44,200,000. Searches on 2026-11-06 found no later primary result or proof that tai256c is solved. This search was not exhaustive.

## Validation

- `.venv/bin/python -m pytest tasks/t027 -q`: 14 passed.
- Cold-seed export test copies only `init_program.py` to a temporary directory, clears `PYTHONPATH`, and runs it without repository imports. It returns the identity permutation.
- Evolution-entry test calls the task-local baseline with a short explicit budget and validates its output.
- The default baseline uses 10,000 fixed pair checks. A test runs the same seed twice and confirms that the full output is identical.
- Baseline smoke run with seed 0 and an explicit 0.05-second cutoff returned a feasible permutation after 74 improving swaps and 254 pair checks; the checker recomputed 51,043,722 exactly. This is a smoke check, not the saved human reference.
- Checker tests confirm that the full result is unchanged when arbitrary claimed-score, objective, or metadata fields are added to the candidate.
- Swap-delta tests compare ten seeded pair swaps against full exact objective recomputation.
- Sol must still independently replay the human witness, review the candidate evaluator path, and decide whether the source evidence and reproduced human baseline satisfy admission.

## Limitations

- No global optimum proof is claimed. The checker validates candidate feasibility and exact objective only.
- The original ANT search and run are not reconstructed.
- The lower-bound report is a result reported by the cited paper; the task checker does not verify its proof.
- Acceptance is accepted by Sol on 2026-11-06; this task is not in the shared registry.
