"""Pass this evaluator to SimpleTES with the matching instruction and seed."""
from mathbench.adapters import make_evaluator

evaluate = make_evaluator("T073", "T073-C01", strict=True)
