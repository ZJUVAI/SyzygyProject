# T024 implementation notes

Status: accepted by Sol on 2026-11-06.

## Source review and parameter choice

- Checked the Afzaly–McKay extremal graph table and its explanatory note on 2026-11-06. The table says an unprefixed edge count is exact. Its order-38 value 117 is therefore solved and was not selected.
- The order-41 entry is `>=132` and links to `c4_n41e132.maybe.s6`, which contains three sparse6 records. The prefix means the authors do not claim that 132 is an upper bound. Selected parameters are exactly 41 vertices and forbidden `C4`.
- The same table gives the exact order-40 value 127. Deleting each of the 41 vertices from a candidate graph and summing induced-edge counts gives `39m <= 41*127`; hence `m <= floor(5207/39)=133`. Together with the 132-edge witness, this proves `132 <= ex(41,C4) <= 133`.
- The data page describes the tables as joint work by Narjess Afzaly and Brendan McKay and says further details were in preparation. The current checked source is the live data page; no paper version for the order-41 entry was located. This is an explicit source limitation, not a claim that an exhaustive literature survey found no proof.
- Download URL: `https://users.cecs.anu.edu.au/~bdm/data/extremal/c4_n41e132.maybe.s6`. SHA-256: `900da21cbbb59d10c30f26feb35ebab4f0e3ef65f21429939584bda497768989`.

## Reproduction

The first record was decoded from sparse6 with NetworkX 3.x, then saved as `data/human_witness.json`. The checker independently recomputes the 132 edges and tests all unordered vertex pairs for at most one common neighbor. Since a C4 exists exactly when two distinct vertices have two common neighbors, this is an exact full-graph check. The result is a feasible construction only; optimality remains open in the cited table.

The seed is a 41-vertex star with 40 edges. The classical baseline starts from that star and uses seeded random edge additions. It checks for a length-three path before accepting an edge and never loads task data. Defaults: seed 38, 3,000 iterations. It records the actual attempt count, accepted additions, seed, and optional wall-clock budget. The evolution entry point delegates to this witness-free baseline; the separate human/reference programs read the archived witness.

## Replay commands

```sh
.venv/bin/python -m pytest tasks/t024/test_task.py -q
python3 -m json.tool tasks/t024/task.json > /dev/null
python3 -m json.tool tasks/t024/sota.json > /dev/null
python3 -m json.tool tasks/t024/records.json > /dev/null
```

## Review status and limitations

Sol accepted this task on 2026-11-06 after full runner replay. See records.json. The 132-edge construction is reproduced exactly. The public table gives no optimality proof for order 41. The live web table was checked on 2026-11-06; this implementation does not establish a complete literature survey.
