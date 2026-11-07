"""Pass this evaluator to DREAM-RSI with the matching instruction and seed."""
from mathbench.adapters import make_evaluator

evaluate = make_evaluator("T003", "T003-C02", strict=True)
