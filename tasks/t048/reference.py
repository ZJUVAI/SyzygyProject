"""Load the pinned SorterHunter size record for the selected input count."""
import json,os
from pathlib import Path
DATA=Path(__file__).parent/"data/reference/sorterhunter_17_71_12.json"
_FILES={"T048-C01":"sorterhunter_17_71_12.json"}
def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T048-C01")
    try:name=_FILES[cid]
    except KeyError:raise ValueError(f"unsupported T048 configuration: {cid}") from None
    data=json.loads((Path(__file__).parent/'data/reference'/name).read_text())
    return {'comparators':data['comparators'],'reference_metadata':{'source':data['source'],'size':data['size'],'depth':data['depth']}}
