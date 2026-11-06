"""Pass this evaluator to DREAM-RSI with the matching instruction and seed."""
from mathbench.adapters import make_evaluator

evaluate = make_evaluator("T005", "T005-C02", strict=True)
