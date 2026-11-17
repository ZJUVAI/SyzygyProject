"""Accepted own-result records must identify the saved, replayed artifact."""
import hashlib
import json
from mathbench.registry import INITIAL_TASKS, ROOT
from mathbench.replay import read_witness_bytes, witness_path
from mathbench.saved_result import best_record_path, read_best_record


def test_saved_results_cover_each_official_configuration():
    for task in INITIAL_TASKS:
        directory = ROOT / 'tasks' / task.lower()
        config, = json.loads((directory / 'task.json').read_text())['configurations']
        path = best_record_path(directory / 'data')
        saved = read_best_record(path)
        assert saved['result']['config_id'] == config['id']
        assert saved['result']['validity'] == saved['initial_result']['validity'] == 1
        assert not (directory / 'data/best').exists()
        digest = saved['provenance'].get('solution_sha256')
        if digest:
            assert hashlib.sha256(read_witness_bytes(path)).hexdigest() == digest, task


def test_archived_witness_hashes_match_the_named_files():
    def inspect(value, directory, location):
        if isinstance(value, list):
            for i, item in enumerate(value):
                inspect(item, directory, location + '/' + str(i))
        elif isinstance(value, dict):
            digest = value.get('witness_sha256')
            if isinstance(digest, str):
                for key in ('saved_witness', 'witness_file', 'witness', 'file'):
                    name = value.get(key)
                    if isinstance(name, str) and witness_path(directory / name).is_file():
                        assert hashlib.sha256(read_witness_bytes(directory / name)).hexdigest() == digest, location
                        break
            for key, item in value.items():
                inspect(item, directory, location + '/' + key)
    for task in INITIAL_TASKS:
        directory = ROOT / 'tasks' / task.lower()
        public = directory / 'data/bestknown.json'
        inspect(json.loads(public.read_text()), directory, task + '/' + public.name)
        saved = best_record_path(directory / 'data')
        inspect(read_best_record(saved)['provenance'], directory, task + '/' + saved.name)
