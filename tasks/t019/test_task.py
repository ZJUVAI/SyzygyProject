import unittest

from tasks.t019.check import validate
from tasks.t019.human import run_code as human
from tasks.t019.init_program import run_code as initial

CONFIG = {"id": "T019-C01", "parameters": {"k": 343}, "direction": "minimize"}
CONFIGS = {k: {"id": cid, "parameters": {"k": k}, "direction": "minimize"} for k,cid in [(343,"T019-C01"),(1000,"T019-C02"),(3000,"T019-C03")]}


class TaskTests(unittest.TestCase):
    def test_seed_feasible_and_objective(self):
        result = validate(initial(), CONFIG)
        self.assertEqual(result["objective"], 342 * initial()["tuple"][1])
        self.assertEqual(result["verification_status"], "exact")

    def test_human_witness_exact_diameter_and_claim_ignored(self):
        result = validate({**human(), "claimed_score": -1}, CONFIG)
        self.assertEqual(result["objective"], 2340)
        self.assertEqual(result["details"]["prime_count_checked"], 68)

    def test_translation_and_negative_values(self):
        values = [x - 5000 for x in human()["tuple"]]
        self.assertEqual(validate({"tuple": values}, CONFIG)["objective"], 2340)

    def test_rejects_bad_size_bool_noninteger_and_duplicates(self):
        good = human()["tuple"]
        for values in (good[:-1], good[:-1] + [True], good[:-1] + [1.5], good[:-1] + [good[0]]):
            with self.assertRaises(ValueError):
                validate({"tuple": values}, CONFIG)

    def test_rejects_covered_prime_residues(self):
        # Every residue modulo 2 is present; duplicate padding keeps the length.
        bad = list(range(343))
        with self.assertRaisesRegex(ValueError, "prime 2"):
            validate({"tuple": bad}, CONFIG)

    def test_new_same_parameter_public_witnesses_exact(self):
        import json
        from pathlib import Path
        from unittest.mock import patch
        for k, diameter in ((1000,7802),(3000,26606)):
            cid=CONFIGS[k]["id"]
            values=list(map(int,(Path(__file__).parent/"data"/f"mit_admissible_{k}_{diameter}.txt").read_text().split()))
            self.assertEqual(len(values),k)
            self.assertEqual(validate({"tuple":values,"objective":"tampered"},CONFIGS[k])["objective"],diameter)
            self.assertTrue(validate({"tuple":values},CONFIGS[k])["details"]["claimed_objective_ignored"])
            with patch.dict("os.environ",{"MATHBENCH_CONFIG_ID":cid}):
                from tasks.t019 import human,reference
                self.assertEqual(human.run_code()["tuple"], values)
                self.assertEqual(reference.run_code()["tuple"], values)

    def test_config_parameters_match_id(self):
        with self.assertRaises(ValueError):
            validate({"tuple":human()["tuple"]},{"id":"T019-C02","parameters":{"k":343}})

    def test_primorial_cold_seed_new_configurations(self):
        import json, os
        from unittest.mock import patch
        from tasks.t019.init_program import run_code
        for k in (1000,3000):
            with patch.dict(os.environ,{"MATHBENCH_CONFIG_ID":CONFIGS[k]["id"]}):
                candidate=run_code()
            self.assertEqual(len(candidate["tuple"]),k)
            result=validate(candidate,CONFIGS[k])
            self.assertEqual(result["details"]["prime_count_checked"],len(__import__("tasks.t019.check",fromlist=["_primes_through"])._primes_through(k)))
            self.assertLess(result["objective"],50000)
            self.assertTrue(__import__("math").isfinite(float(result["objective"])))
            if k==3000:
                self.assertLess(len(json.dumps(candidate,separators=(",",":"))),16*1024*1024)


if __name__ == "__main__":
    unittest.main()
