"""Load the best fixed public witness checked for each configured n."""
import json,os
from pathlib import Path
_FILES={"T076-C01":"sharp_8635_transcribed.json","T076-C02":"lunnon_w2_n16.json","T076-C03":"lunnon_w2_n17.json"}
def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T076-C01")
    try:name=_FILES[cid]
    except KeyError:raise ValueError(f"unsupported T076 configuration: {cid}") from None
    d=json.loads((Path(__file__).parent/'data/reference'/name).read_text())
    return {"elements":d["elements"],"reference_metadata":d.get("source",{})}
