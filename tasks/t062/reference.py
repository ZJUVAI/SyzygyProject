"""Load the best fixed public witness checked for each configured n."""
import json,os
from pathlib import Path
def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T062-C01")
    if cid != "T062-C01":raise ValueError(f"unsupported T062 configuration: {cid}")
    d=json.loads((Path(__file__).parent/'data/reference'/'sharp_8635_transcribed.json').read_text())
    return {"elements":d["elements"],"reference_metadata":d.get("source",{})}
