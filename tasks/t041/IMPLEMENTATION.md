# T041 implementation notes

Status: accepted by Sol on 2026-11-06.

## Definition and representation

The fixed task is 17 positive-area squares inside the closed unit square, with pairwise-disjoint interiors and unrestricted orientations. The objective is the sum of side lengths and is maximized. Boundary contact is legal. The frozen human-method comparison is 4.

The checker uses exact rational centres, side lengths, and unit edge directions. Rational points on the unit circle are dense. The rational encoding does not lower the supremum of the unrestricted problem: shrink every square about its centre by a common factor below 1. Each wall and pair separation then has a positive margin. A sufficiently small perturbation of centres, sides, and unit directions preserves feasibility, and rational centres, sides, and rational unit directions can approximate those perturbed data. The resulting scores approach the original score. The checker therefore accepts a dense exact certificate language while retaining an exact feasible witness for every submitted result.

## Sources and records

The human-method witness is the 4 by 4 grid with one cell split into two side-1/8 squares. Its 17 coordinates are reconstructed for this package; they are not attributed as original coordinates from Erdős and Graham (1975).

The AI-assisted public construction is pinned to `Sprite143/erdos-106-counterexample` commit `edbfb534e78d4f1f9b1a5a7298b9b022285b4962`. The task package stores its constructor, source archive, original search certificate, closed-form output, source license, and hashes under `data/`. The closed-form value is `2190452873/547596200`; the earlier numerical certificate is `2000062156200269/500000000000000`. A separate checker independently verifies all corners, containment, all 136 pairs, and the recomputed sum. The score is a lower bound only.

Current-source review on 2026-11-06 found a ProbXiv record identifying AI assistance and Claude Opus 5 as the discoverer; the record states that no person has examined the submission. It reports Lean checking of a formalization and cautions that this does not prove the formalization matches the page claim. The repository also says human referee review has not occurred. The task does not identify the construction as a human result or as optimal.

For all 17 squares, disjoint interiors imply the sum of their areas is at most 1. Thus `sum(side^2) <= 1`, and Cauchy–Schwarz gives `sum(side) <= sqrt(17)`. The checked public witness gives the lower bound above. The review did not locate a matching unrestricted upper bound.

## Programs

- `init_program.py`: exact row of 17 side-`1/17` squares, score 1; independent of comparison assets.
- `baseline.py`: fixed-seed enumeration of 16 split cells and two orientations; fixed budget of 32 layouts, optionally cut by `MATHBENCH_SEARCH_SECONDS`.
- `human.py`: rebuilds the grid construction from its formula.
- `reference.py`: replays the pinned closed-form public construction from task-local data.
- `evolution.py`: task-qualified `run_code()` entry which calls the witness-free search baseline.
- `check.py`: exact rational square structure, containment, 68 corner checks, all 136 pairwise SAT checks, and recomputed side sum.

## Validation run by the implementation agent

Command:

```sh
.venv/bin/python -m pytest tasks/t041/test_task.py -q
```

Result: 15 passed. This includes the score-1 initial seed, human and public witnesses; exact recomputation of the public score; legal boundary contact; damaged overlap, wall, zero side, malformed orientation, Boolean, NaN, positive and negative infinity, and wrong-count inputs; ignored claimed scores; and evaluator valid-result, program-error, and timeout handling.

The public exact value was also independently checked directly by `tasks/t041/check.py`: `2190452873/547596200`, with all 136 unordered pairs tested. The human formula recomputes to exactly 4. This is an implementation self-check, not the Sol acceptance review.

JSON validation:

```sh
.venv/bin/python -m json.tool tasks/t041/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t041/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t041/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t041/acceptance.json > /dev/null
```

All four JSON files parse. Shared task registration is intentionally unchanged; the main reviewer must register the new task only after review. Consequently, standalone evaluator error/timeout tests add T041 to the registry tuple locally with a test monkeypatch; no shared registry was changed.

## Limits

The public construction has not had human referee review according to the checked source. The exact verifier certifies feasibility and score, not global optimality. The simple baseline's finite construction family reaches 4 and is not intended to compete with the fixed public reference. Current acceptance status is accepted by Sol on 2026-11-06.
