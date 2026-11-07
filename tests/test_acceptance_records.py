"""Accepted own-result records must identify the saved, replayed artifact."""
import hashlib
import json
from pathlib import Path
from mathbench.registry import INITIAL_TASKS, ROOT


def test_own_records_match_selected_artifacts():
    for task in INITIAL_TASKS:
        d=ROOT/'tasks'/task.lower()
        metadata=json.loads((d/'task.json').read_text())
        records=json.loads((d/'records.json').read_text())
        sota=json.loads((d/'sota.json').read_text())
        for config in metadata['configurations']:
            cid=config['id'];folder=d/'best'/cid
            if not (folder/'provenance.json').exists():continue
            provenance=json.loads((folder/'provenance.json').read_text())
            if provenance.get('reviewer')!='Sol main agent':continue
            result=json.loads((folder/'result.json').read_text())
            digest=hashlib.sha256((folder/'solution.json').read_bytes()).hexdigest()
            for doc in (records,sota):
                archive=doc.get('configurations',{}).get(cid,{})
                for key in ('best_own_search','own_search_record'):
                    entry=archive.get(key,{})
                    if not isinstance(entry,dict):continue
                    witness=entry.get('witness',entry.get('witness_file'))
                    if witness!=f'best/{cid}/solution.json':continue
                    if 'witness_sha256' in entry:
                        assert entry['witness_sha256']==digest,(task,key,'hash')
                    if 'program' in entry and 'program' in provenance:
                        assert entry['program']==provenance['program'],(task,key,'program')
                    if 'value' in entry:
                        assert str(entry['value'])==str(result['objective']),(task,key,'value')


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
                    if isinstance(name, str) and (directory / name).is_file():
                        assert hashlib.sha256((directory / name).read_bytes()).hexdigest() == digest, location
                        break
            for key, item in value.items():
                inspect(item, directory, location + '/' + key)
    for task in INITIAL_TASKS:
        directory = ROOT / 'tasks' / task.lower()
        for name in ('records.json', 'sota.json'):
            inspect(json.loads((directory / name).read_text()), directory, task + '/' + name)
