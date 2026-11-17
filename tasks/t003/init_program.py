"""Deterministic axis-aligned grid seed selected by MATHBENCH_CONFIG_ID."""
import json, os
# EVOLVE-BLOCK-START

def run_code():
    cid = os.environ.get('MATHBENCH_CONFIG_ID', 'T003-C01')
    if cid != 'T003-C01':
        raise ValueError('unknown T003 configuration')
    return {'squares':[{'x':str(2*(i%5)+1)+'/2','y':str(2*(i//5)+1)+'/2','t':'0'} for i in range(26)]}

# EVOLVE-BLOCK-END
if __name__ == '__main__': print(json.dumps(run_code()))
