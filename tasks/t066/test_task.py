import json
from pathlib import Path
import unittest
from tasks.t066.check import validate
from tasks.t066.baseline import _distance, _mutate_parity

class _FixedMutationRng:
    def randint(self, a, b): return 1
    def randrange(self, start, stop=None):
        if stop is None: return 0
        return start

CONFIG={'parameters':{'n':68,'k':15,'q':2}}
DATA=Path(__file__).parent/'data'/'human_generator.json'
SOTA_DATA=Path(__file__).parent/'data'/'sota_generator.json'

class TaskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix=json.loads(DATA.read_text())['matrix']

    def test_public_witness_exact_distance(self):
        result=validate({'generator_matrix':self.matrix,'objective':999},CONFIG)
        # Independent direct XOR enumeration for the score cross-check.
        independent=[]
        for mask in range(1, 1 << 15):
            word=[0]*68
            for i in range(15):
                if (mask >> i) & 1:
                    word=[a ^ b for a,b in zip(word,self.matrix[i])]
            independent.append(sum(word))
        self.assertEqual(min(independent),8)
        self.assertEqual(result['objective'],min(independent))
        self.assertEqual(result['verification_status'],'exact')
        self.assertEqual(result['details']['codewords_checked'],32767)
        self.assertTrue(result['details']['claimed_objective_mismatch'])

    def test_reproduced_sota_witness_exact_distance(self):
        from tasks.t066.sota import run_code
        witness=json.loads(SOTA_DATA.read_text())
        result=validate(run_code(),CONFIG)
        self.assertEqual(len(witness['matrix']),15)
        self.assertTrue(all(len(row)==68 for row in witness['matrix']))
        self.assertEqual(result['objective'],24)
        self.assertEqual(result['verification_status'],'exact')
        self.assertEqual(result['details']['rank'],15)
        self.assertEqual(result['details']['codewords_checked'],32767)

    def test_ignores_absent_score(self):
        self.assertEqual(validate({'generator_matrix':self.matrix},CONFIG)['objective'],8)

    def test_rejects_bool_entry(self):
        m=[r[:] for r in self.matrix]; m[0][0]=True
        with self.assertRaises(ValueError): validate({'generator_matrix':m},CONFIG)

    def test_rejects_float_entry(self):
        m=[r[:] for r in self.matrix]; m[0][0]=1.0
        with self.assertRaises(ValueError): validate({'generator_matrix':m},CONFIG)

    def test_rejects_wrong_shape(self):
        with self.assertRaises(ValueError): validate({'generator_matrix':self.matrix[:-1]},CONFIG)
        m=[r[:] for r in self.matrix]; m[0].pop()
        with self.assertRaises(ValueError): validate({'generator_matrix':m},CONFIG)

    def test_rejects_rank_deficient_matrix(self):
        m=[r[:] for r in self.matrix]; m[1]=m[0][:]
        with self.assertRaises(ValueError): validate({'generator_matrix':m},CONFIG)

    def test_boundary_valid_distance_one_systematic_code(self):
        m=[]
        for i in range(15):
            row=[0]*68; row[i]=1; m.append(row)
        self.assertEqual(validate({'generator_matrix':m},CONFIG)['objective'],1)

    def test_parity_mutation_changes_code_and_distance_while_preserving_rank(self):
        # [I|I|0] has distance 2. Clearing one parity bit in row 0
        # makes that generator weight 1, so the new code has distance 1.
        rows=[]
        for i in range(15):
            rows.append((1 << i) | (1 << (15+i)))
        changed=_mutate_parity(rows, _FixedMutationRng(), max_flips=1)
        self.assertEqual(_distance(rows),2)
        self.assertEqual(_distance(changed),1)
        self.assertNotEqual(rows,changed)
        # The identity block remains intact, so rank remains 15.
        self.assertTrue(all((changed[i] >> i) & 1 for i in range(15)))

    def test_rejects_unknown_parameters(self):
        with self.assertRaises(ValueError): validate({'generator_matrix':self.matrix},{'parameters':{'n':68,'k':15,'q':3}})

if __name__=='__main__': unittest.main()
