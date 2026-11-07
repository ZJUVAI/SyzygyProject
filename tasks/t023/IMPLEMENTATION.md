# T023 implementation record

Status: accepted by Sol on 2026-11-06.

## Configuration and sources

- Configuration: `T023-C01`, CA(4; 20, 2). Minimize rows.
- NIST's downloadable IPOG-F witness has 65 rows and is replayed by `human.py`. The source's dash entries are completed as zero and the completed binary array passes exact checking.
- The frozen Colbourn table (November 2024) reports a 39-row construction, listed as Hadamard (Colbourn-Keri) with NCK postoptimization. The linked table does not include a witness.
- Lower bound: 32. Deleting columns gives a 13-column strength-four CA, and Izquierdo-Marquez and Torres-Jimenez prove CAN(4,13,2)=32 in arXiv:1711.10040v2. Thus 32 <= CAN(4,20,2) <= 39.
- An exact-parameter source search located the 39-row upper bound but no proof that CAN(4,20,2) is exact. This is a bounded survey, not a complete literature review.

## Replay and checks

- Human witness: `data/nist_ca_t4_v2_k20.txt`, SHA-256 `fd79ad1d35cdcbf6a8f594ffc7aab18abd6358e3722cad78039559223de4a12c`.
- Exact checker: enumerate 4,845 four-column sets and all 16 binary patterns. Candidate score claims are ignored.
- Cold seed: all 20-bit vectors with Hamming weight at most four. There are 6,196 rows. For any four columns and target pattern, choose the support of its 1 entries and set every other column to zero; that row is in the seed.
- Classical baseline: 256 seeded random rows, exact uncovered-pattern repair, then seeded greedy deletion. It keeps exact projection-pattern counts and uses compact unsigned-integer storage. `MATHBENCH_SEED` controls order; `search_steps` fixes the default iteration count and supports the shared optional time cutoff. The fixed-seed replay with seed 7 returned 96 rows in 4.064 s; exact verification took 0.095 s on Python 3.13.12, Linux x86_64. The simple seed returned 6,196 rows and passed exact verification in 0.472 s. It does not read human or reference files.
- Evolution entry point delegates to the task search baseline and does not read reference data.
- Run `.venv/bin/python -m pytest tasks/t023/test_task.py -q` for legal and damaged arrays, duplicates, malformed rows, exceptional values, score-claim ignoring, and upper-bound rejection.

## Limits

The Colbourn 39-row witness is not reproduced. The NIST source generator is not rerun. The exact 20-column optimum remains unknown in the cited sources. Full runner process-error and timeout checks are part of Sol's shared-runner acceptance.
