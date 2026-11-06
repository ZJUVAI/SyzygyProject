import json
from pathlib import Path
import pytest

TASK_DIR=Path(__file__).parent
from tasks.t035 import check

CONFIG={'parameters':{'degree':4,'girth':10}}
DATA=json.loads((TASK_DIR/'data'/'human_graph.json').read_text())


def test_published_graph_and_independent_score():
    result=check.validate(DATA,CONFIG)
    assert result['objective']==320
    assert result['verification_status']=='exact'
    assert result['details']['edges']==640
    assert result['details']['girth']==10


def test_claimed_objective_is_not_used():
    altered=dict(DATA,objective=1)
    result=check.validate(altered,CONFIG)
    assert result['objective']==320
    assert result['details']['claimed_objective_mismatch']


def test_duplicate_edge_rejected():
    edges=list(DATA['edges']); edges[-1]=edges[0]
    with pytest.raises(ValueError): check.validate({'vertices':320,'edges':edges},CONFIG)


def test_loop_rejected():
    edges=list(DATA['edges']); edges[0]=[0,0]
    with pytest.raises(ValueError): check.validate({'vertices':320,'edges':edges},CONFIG)


def test_boolean_endpoint_rejected():
    edges=list(DATA['edges']); edges[0]=[0,True]
    with pytest.raises(ValueError): check.validate({'vertices':320,'edges':edges},CONFIG)


def test_out_of_range_endpoint_rejected():
    edges=list(DATA['edges']); edges[0]=[0,320]
    with pytest.raises(ValueError): check.validate({'vertices':320,'edges':edges},CONFIG)


def test_short_cycle_rejected_after_degree_preserving_switch():
    edges={tuple(e) for e in DATA['edges']}
    edges.remove((0,2)); edges.remove((272,308))
    edges.add((0,308)); edges.add((2,272))
    with pytest.raises(ValueError): check.validate({'vertices':320,'edges':[list(e) for e in edges]},CONFIG)


def test_non_integer_order_rejected():
    with pytest.raises(ValueError): check.validate({'vertices':True,'edges':[]},CONFIG)
