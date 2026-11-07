# T022 implementation notes

Status: accepted by Sol on 2026-11-06.

## Provenance and verification

- Exoo's 1989 paper describes a two-coloring of the edges of K42 and establishes R(5,5) >= 43.
- McKay's public Ramsey data page says the `r55_42some.g6` archive contains 328 catalogued Ramsey(5,5,42) graphs and that their 328 complements complete the 656-graph catalog.
- The first graph6 line was decoded into `data/human_witness.json`. Exact verification checked the graph and complement for every 5-clique, and recomputed 42 vertices and 425 edges.
- Angeltveit and McKay's arXiv v2 (2025-09-01), published in Journal of Graph Theory in 2026, proves R(5,5) <= 46. The checker therefore accepts at most 45 vertices. This bound leaves possible improvements over 42 open.

## Programs

`init_program.py` returns a 5-cycle. `baseline.py` uses a fixed seed for up to 40 random one-vertex extension attempts, stops at the theorem-derived 45-vertex cap, and returns the seed, budget, and actual attempt count in `search_metadata`. It does not read task reference files. `human.py` and `reference.py` read the saved public witness.

## Replay commands

```sh
.venv/bin/python -m pytest tasks/t022/test_task.py -q
python3 -m json.tool tasks/t022/task.json > /dev/null
python3 -m json.tool tasks/t022/sota.json > /dev/null
python3 -m json.tool tasks/t022/records.json > /dev/null
```

## Acceptance evidence

The task suite tests the seed, baseline metadata, published witness, independent objective, invalid clique and independent-set cases, malformed adjacency, NaN and infinite neighbor indices, empty and boundary graphs, a claimed score, and the proven upper-bound cutoff. The graph6 witness hash is recorded in `records.json`. Sol independently decoded and replayed the human graph, counted all five-vertex subsets, and checked the cold seed. The task passed review on 2026-11-06. See records.json.
