"""Pass this evaluator to DREAM-RSI with the matching instruction and seed."""
from mathbench.adapters import make_evaluator

evaluate = make_evaluator("T002", "T002-C02", strict=True)
