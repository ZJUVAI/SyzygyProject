"""Reproduced historical 208-step witness."""
import json
from pathlib import Path

def run_code():
    data=json.loads((Path(__file__).parent/"data"/"human_matolcsi_vinuesa.json").read_text())
    return {"coefficients":data["polynomial_coefficients"]}
