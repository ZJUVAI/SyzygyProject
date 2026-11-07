"""Load the fixed MIT-published human tuple for the selected parameter."""
import json, os
from pathlib import Path
_FILES={"T019-C01":"human_343.json","T019-C02":"human_1000.json","T019-C03":"human_3000.json"}
def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T019-C01")
    try:name=_FILES[cid]
    except KeyError:raise ValueError(f"unsupported T019 configuration: {cid}") from None
    record=json.loads((Path(__file__).parent/"data"/name).read_text())
    return {"tuple": record["witness"] if "witness" in record else record["tuple"]}
