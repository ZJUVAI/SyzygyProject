"""Search snapshots must not include their own generated output."""
from scripts.search import source_files
from mathbench.search import search_deadline


def test_source_files_prunes_generated_directories(tmp_path):
    (tmp_path / 'evolution.py').write_text('')
    (tmp_path / 'search_kernel.cpp').write_text('')
    helper = tmp_path / 'helpers'
    helper.mkdir()
    (helper / 'build.py').write_text('')
    for excluded in ('runs', '__pycache__'):
        nested = tmp_path / excluded / 'sources'
        nested.mkdir(parents=True)
        (nested / 'copied.py').write_text('')
    assert {p.relative_to(tmp_path).as_posix() for p in source_files(tmp_path)} == {
        'evolution.py', 'helpers/build.py', 'search_kernel.cpp',
    }


def test_explicit_long_search_budget_is_honored(monkeypatch):
    monkeypatch.setenv('MATHBENCH_SEARCH_SECONDS', '180')
    monkeypatch.setattr('mathbench.search.time.monotonic', lambda: 1000.0)
    assert search_deadline() == 1180.0


def test_search_budget_leaves_generation_headroom(monkeypatch):
    monkeypatch.setenv('MATHBENCH_SEARCH_SECONDS', '10000')
    monkeypatch.setattr('mathbench.search.time.monotonic', lambda: 1000.0)
    assert search_deadline() == 1240.0


def test_resume_order_covers_every_released_task_once():
    from mathbench.registry import INITIAL_TASKS
    from scripts.search import resume_order

    order = resume_order()
    assert len(order) == len(set(order))
    assert set(order) == set(INITIAL_TASKS)
    assert order[:3] == ('T013', 'T015', 'T018')
