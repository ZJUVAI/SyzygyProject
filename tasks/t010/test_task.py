import json
from pathlib import Path
import unittest
from tasks.t010.check import validate
from tasks.t010.sota import run_code as run_sota

CONFIG={'parameters':{'n':17,'distance':6}}
DATA=Path(__file__).parent/'data'/'bch_extended_128.json'

class TaskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.words=json.loads(DATA.read_text())['codewords']

    def test_reproduced_witness_and_independent_pair_count(self):
        result=validate({'codewords':self.words,'objective':999},CONFIG)
        direct=min(bin(a^b).count('1') for i,a in enumerate(self.words) for b in self.words[i+1:])
        self.assertEqual((len(self.words),direct),(128,6))
        self.assertEqual(result['objective'],128)
        self.assertEqual(result['details']['pairs_checked'],8128)
        clean=validate({'codewords':self.words},CONFIG)
        self.assertEqual(result,clean)
        self.assertTrue(result['details']['claimed_objective_ignored'])

    def test_sota_replay_matches_saved_octacode_witness(self):
        solution = run_sota()
        result = validate(solution, CONFIG)
        saved = json.loads((Path(__file__).parent / 'data' / 'sota_nordstrom_robinson_256.json').read_text())
        self.assertEqual(solution, saved)
        self.assertEqual(result['objective'], 256)
        self.assertEqual(result['details']['minimum_pairwise_distance'], 6)
        self.assertEqual(result['details']['pairs_checked'], 32640)

    def test_accepts_bit_list(self):
        words=[[((x>>i)&1) for i in range(17)] for x in self.words[:2]]
        self.assertEqual(validate({'codewords':words},CONFIG)['objective'],2)

    def test_singleton_boundary(self):
        self.assertEqual(validate({'codewords':[0]},CONFIG)['objective'],1)

    def test_rejects_duplicate(self):
        with self.assertRaises(ValueError): validate({'codewords':[4,4]},CONFIG)

    def test_rejects_too_close(self):
        with self.assertRaises(ValueError): validate({'codewords':[0,31]},CONFIG)

    def test_rejects_bool_float_and_invalid_bit(self):
        for bad in (True, 1.0, [0]*16+[False], [0]*16+[2]):
            with self.subTest(bad=bad), self.assertRaises(ValueError): validate({'codewords':[bad]},CONFIG)

    def test_rejects_out_of_range_and_wrong_length(self):
        for bad in (-1,1<<17,[0]*16):
            with self.subTest(bad=bad), self.assertRaises(ValueError): validate({'codewords':[bad]},CONFIG)

    def test_rejects_empty_and_unknown_config(self):
        with self.assertRaises(ValueError): validate({'codewords':[]},CONFIG)
        with self.assertRaises(ValueError): validate({'codewords':[0]},{'parameters':{'n':17,'distance':5}})

if __name__=='__main__': unittest.main()
