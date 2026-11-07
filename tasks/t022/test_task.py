import unittest

from tasks.t022.baseline import run_code as baseline
from tasks.t022.check import validate
from tasks.t022.human import run_code as human
from tasks.t022.init_program import run_code as initial
from tasks.t022.reference import run_code as reference

CONFIG = {"id": "T022-C01", "parameters": {
    "clique_size": 5, "independent_set_size": 5, "max_vertices": 45}}


def _cycle(n):
    return {"adjacency": [[(v - 1) % n, (v + 1) % n] for v in range(n)]}


class TaskTests(unittest.TestCase):
    def test_seed_and_search_are_valid(self):
        self.assertEqual(validate(initial(), CONFIG)["objective"], 5)
        result = baseline()
        self.assertEqual(validate(result, CONFIG)["verification_status"], "exact")
        metadata = result["search_metadata"]
        self.assertEqual(metadata["seed"], 0)
        self.assertEqual(metadata["iteration_budget"], 40)
        self.assertGreaterEqual(metadata["iterations_attempted"], 1)
        self.assertLessEqual(metadata["iterations_attempted"], 40)
        self.assertLessEqual(len(result["adjacency"]), 45)

    def test_public_human_witness_replays(self):
        result = validate(human(), CONFIG)
        self.assertEqual((result["objective"], result["details"]["edges"]), (42, 425))
        self.assertEqual(reference(), human())

    def test_claimed_score_is_ignored(self):
        witness = human()
        witness["claimed_score"] = 10**100
        self.assertEqual(validate(witness, CONFIG)["objective"], 42)

    def test_bad_constructions(self):
        # K5 violates the clique constraint.
        complete = {"adjacency": [[w for w in range(5) if w != v] for v in range(5)]}
        # Empty 5-vertex graph violates the independent-set constraint.
        empty = {"adjacency": [[] for _ in range(5)]}
        malformed = [
            complete, empty,
            {"adjacency": [[1], []]},  # asymmetric edge
            {"adjacency": [[0]]},  # loop
            {"adjacency": [[1, 1], [0]]},  # duplicate edge entry
            {"adjacency": [[True], [0]]},  # bool is not an integer vertex ID
            {"adjacency": [[] for _ in range(46)]},  # published upper bound
        ]
        for candidate in malformed:
            with self.subTest(candidate=candidate):
                with self.assertRaises(ValueError):
                    validate(candidate, CONFIG)

    def test_boundary_and_objective(self):
        self.assertEqual(validate({"adjacency": []}, CONFIG)["objective"], 0)
        self.assertEqual(validate(_cycle(4), CONFIG)["objective"], 4)
        result = validate(human(), CONFIG)
        self.assertEqual(result["details"]["vertices"], len(human()["adjacency"]))

    def test_nonfinite_and_out_of_range_neighbors(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate({"adjacency": [[value]]}, CONFIG)
        with self.assertRaises(ValueError):
            validate({"adjacency": [[1], []]}, CONFIG)


if __name__ == "__main__":
    unittest.main()
