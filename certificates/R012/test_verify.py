"""Public acceptance controls / 公开验收控制. No optimizer or network."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import verify
from sweep import Tree, Direct, trig, coverage, direct_mass, GeometryError


class CertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.L, cls.A, cls.atoms, cls.gamma, cls.jobs, cls.result = verify.load_math()

    def test_exact_claim(self):
        self.assertEqual(self.result['lower_bound'], '461300/99999')

    def test_angle_closure(self):
        self.assertEqual(len(self.jobs), 2925)
        self.assertEqual(self.result['off_net_core_entries'], 48)

    def test_mass_gap(self):
        self.assertEqual(F(self.result['mass_gap']), F(701, 250000))

    def test_source_measure_identity(self):
        self.assertEqual(self.result['expanded_measure_sha256'], verify.ATOM_DIGEST)
        self.assertEqual(len(self.atoms), 1616)

    def test_decimal_bracket(self):
        a, b = map(F, self.result['decimal_bracket_20'])
        self.assertLessEqual(a, F(461300, 99999))
        self.assertLess(F(461300, 99999), b)

    def test_containment_margin_is_positive(self):
        self.assertGreater(F(self.result['minimum_containment_margin']), 0)

    def test_negative_recipe_witnesses(self):
        self.assertEqual(verify.counterexamples(self.L, self.A, self.atoms), 5)

    def test_pythagorean_axis(self):
        c, s = trig(F(2, 7))
        self.assertEqual(c*c+s*s, 1)

    def test_bad_half_tangent(self):
        for t in (F(-1), F(1), 0.25):
            with self.assertRaises(GeometryError):
                trig(t)

    def test_accumulator_agreement(self):
        a, b = Tree(6), Direct(6)
        for lo, hi, w in ((0,6,9),(1,4,-3),(3,6,7),(2,5,2)):
            a.add(lo,hi,w);b.add(lo,hi,w)
        for lo in range(6):
            for hi in range(lo+1,7):
                self.assertEqual(a.query(lo,hi),b.query(lo,hi))
                self.assertEqual(a.first(lo,hi,a.query(lo,hi)),b.first(lo,hi,b.query(lo,hi)))

    def test_closed_boundary_capture(self):
        atoms=[(F(1),F(1),F(3)),(F(2),F(2),F(5))]
        self.assertEqual(direct_mass(atoms,F(2),F(),(F(1),F(1)))[0],8)

    def test_axis_sweep(self):
        atoms=[(F(1),F(1),F(2))]
        a=coverage(F(2),F(1),atoms,F(),backend='tree')
        b=coverage(F(2),F(1),atoms,F(),backend='direct')
        self.assertEqual(a['minimum'],'2')
        self.assertEqual(a['minimum'],b['minimum'])

    def test_negative_weight_rejected(self):
        with self.assertRaises(GeometryError):
            coverage(F(2),F(1),[(F(1),F(1),F(-1))],F())

    def test_degenerate_domain_rejected(self):
        with self.assertRaises(GeometryError):
            coverage(F(1),F(1),[(F(1,2),F(1,2),F(1))],F())

    def test_duplicate_json_key(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json';p.write_text('{"a":1,"a":2}')
            with self.assertRaises(ValueError):verify.read(p)

    def test_nonfinite_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json';p.write_text('{"a":NaN}')
            with self.assertRaises(ValueError):verify.read(p)

    def test_integrity_tamper_and_extras(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'x.txt').write_text('original')
            h=hashlib.sha256(b'original').hexdigest()
            (root/'MANIFEST.json').write_text(json.dumps({'files':{'x.txt':h}}))
            with patch.object(verify,'ROOT',root):
                self.assertEqual(verify.integrity()['status'],'PASS')
                (root/'x.txt').write_text('modified')
                with self.assertRaises(ValueError):verify.integrity()
                (root/'x.txt').write_text('original');(root/'extra').write_text('x')
                with self.assertRaises(ValueError):verify.integrity()

    def test_existing_output_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(verify.main(['--records','--output',d]),1)

    def test_protected_output_rejected(self):
        self.assertEqual(verify.main(['--records','--output',str(verify.ROOT/'not-an-output')]),1)

    def test_bad_worker_count_rejected(self):
        self.assertEqual(verify.main(['--records','--output','unused','--workers','0']),1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
