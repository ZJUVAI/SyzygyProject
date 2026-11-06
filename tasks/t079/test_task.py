import unittest
from tasks.t079.check import validate
from tasks.t079.human import run_code as human
from tasks.t079.init_program import run_code as initial
CONFIG={"id":"T079-C01","parameters":{"steps":208,"support":["-1/4","1/4"],"nonnegative":True}}
class TaskTests(unittest.TestCase):
 def test_human(self):
  result=validate(human(),CONFIG); self.assertEqual(result["verification_status"],"exact"); self.assertEqual(result["objective"],"6280435861361744576/4160000022692211721")
 def test_seed(self): self.assertEqual(len(initial()["coefficients"]),208)
 def test_invalid(self):
  for coeff in ([1]*207,[True]+[1]*207,[-1]+[1]*207,[0]*208,[float("nan")]+[1]*207):
   with self.assertRaises(ValueError): validate({"coefficients":coeff},CONFIG)
if __name__=="__main__": unittest.main()
