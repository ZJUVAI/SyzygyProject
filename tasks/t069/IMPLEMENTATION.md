# T069 implementation record

Status: `accepted_by_sol`.

The fixed configuration is the 100,000-city `mona-lisa100K` TSPLIB instance. The checker validates a closed Hamiltonian cycle and sums all edge weights with exact integer arithmetic. For squared distance `s`, it sets `r=isqrt(s)` and returns `r+1` exactly when `4s >= (2r+1)^2`, matching nearest-integer EUC_2D rounding without floating-point ambiguity.

The pinned instance is `data/source/mona-lisa100K.tsp`, SHA-256 `532fefbfb9ad66cc2550bece766fa069acaa8e34ee511ac1949ae101da4d70ad`. The official Nagata tour is frozen separately in `data/human/monalisa_5757191.tour` and `data/human/monalisa_5757191.tour`, each SHA-256 `d8a98a936d01b0317ff63a43646fbbbfa74bf6ee954a9449ad659128e579eb88`. Independent checking confirms a 100,000-city permutation and exact length 5,757,191, including the return edge.

The official Waterloo challenge page currently lists this tour and the lower bound 5,757,084. Hougardy and Schroeder (2024), §3.1, state that the instance has not been solved to proven optimality. The lower bound is preserved as a published result; this task does not re-check Concorde's certificate. The official source attributes the tour to Yuichi Nagata's genetic algorithm, with no generative-AI provenance stated.

The simple program uses input order. The traditional search baseline uses alternating horizontal coordinate bands and 20,000 fixed-seed local 2-opt proposals. It reads the public instance but no comparison tour. With seed 0, it returned a valid tour of length 6,856,309 after 153 accepted exchanges in 2.320 seconds. The witness is in `best/seed-0.json`; `best/seed-0.metadata.json` records the seed, step count, limits, environment, exact recomputed score, and replay command.

Validation command:

```sh
.venv/bin/python -m pytest tasks/t069/test_task.py -q
```

The tests cover all five entries, both frozen Nagata copies, exact edge rounding, the full permutation constraint, duplicates, range and numeric type errors, ignored claimed scores, repeatable seeded search, and runner error/timeout controls using `mathbench.evaluate._run` without a registry change. Default generation and verification limits are 300 seconds and 60 seconds, with 4 GiB and one thread.

Result: 13 passed in 16.07 seconds on Python 3.13.12, Linux x86_64. JSON syntax checks passed for the task definition, SOTA, records, and saved run metadata. `git diff --check -- tasks/t069` passed.
