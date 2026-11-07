import unittest

from tasks.t024.baseline import run_code as baseline
from tasks.t024.check import validate
from tasks.t024.human import run_code as human
from tasks.t024.init_program import run_code as initial
from tasks.t024.reference import run_code as reference
from tasks.t024.evolution import run_code as evolution

CONFIG = {"id": "T024-C01", "parameters": {"vertices": 41, "forbidden_cycle_length": 4}}

class TaskTests(unittest.TestCase):
    def test_simple_seed_and_classical_search(self):
        self.assertEqual(validate(initial(), CONFIG)["objective"], 40)
        result = baseline()
        checked = validate(result, CONFIG)
        self.assertEqual(checked["verification_status"], "exact")
        self.assertEqual(result["search_metadata"]["seed"], 38)
        self.assertEqual(result["search_metadata"]["iteration_budget"], 3000)

    def test_evolution_entry_point(self):
        result = evolution()
        self.assertEqual(validate(result, CONFIG)["verification_status"], "exact")

    def test_archive_witness(self):
        result = validate(human(), CONFIG)
        self.assertEqual((result["objective"], result["details"]["vertices"]), (132, 41))
        self.assertEqual(reference(), human())

    def test_claimed_score_is_ignored(self):
        value = human(); value["claimed_score"] = 10**100
        self.assertEqual(validate(value, CONFIG)["objective"], 132)

    def test_invalid_graphs(self):
        witness = human()
        bad = [
            {"adjacency": [[] for _ in range(40)]},
            {"adjacency": [[1, 1]] + [[] for _ in range(40)]},
            {"adjacency": [[True]] + [[] for _ in range(40)]},
            {"adjacency": [[float("nan")]] + [[] for _ in range(40)]},
            {"adjacency": [[float("inf")]] + [[] for _ in range(40)]},
            {"adjacency": [[float("-inf")]] + [[] for _ in range(40)]},
        ]
        # Create a C4 by adding both diagonals to a 4-cycle-free witness only
        # when the selected vertices have no edges; the direct pattern below
        # is independently rejected by the checker.
        c4 = [[] for _ in range(41)]
        for a, b in ((0, 1), (1, 2), (2, 3), (3, 0)):
            c4[a].append(b); c4[b].append(a)
        bad.append({"adjacency": c4})
        for item in bad:
            with self.subTest(item=str(item)[:80]), self.assertRaises(ValueError):
                validate(item, CONFIG)

    def test_valid_boundary_and_actual_edge_count(self):
        star = initial()
        self.assertEqual(validate(star, CONFIG)["details"]["edges"], 40)
        self.assertEqual(validate(human(), CONFIG)["details"]["edges"],
                         sum(map(len, human()["adjacency"])) // 2)

if __name__ == "__main__":
    unittest.main()
