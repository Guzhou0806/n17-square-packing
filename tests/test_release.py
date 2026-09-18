"""Release-integrity and refusal tests; not a new coverage proof."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify


class ReleaseTests(unittest.TestCase):
    def test_frozen_manifest_and_acceptance(self):
        r = verify.preflight()
        self.assertEqual(r['frozen_files_checked'], 131)
        self.assertTrue(r['acceptance_certificate_and_audit_bound'])

    def test_original_m19_archive_matches_every_extracted_file(self):
        with zipfile.ZipFile(ROOT/'archives/M19_nonuniform_direction_lower_bound.zip') as z:
            self.assertEqual(len(z.infolist()), 129)
            for item in z.infolist():
                rel = Path(item.filename).relative_to('M19_nonuniform_direction_lower_bound')
                self.assertEqual(z.read(item), (ROOT/'evidence/M19'/rel).read_bytes())

    def test_separate_m12_archive_matches_nested_dependency(self):
        with zipfile.ZipFile(ROOT/'archives/M12_global_lower_bound.zip') as z:
            self.assertEqual(len(z.infolist()), 57)
            for item in z.infolist():
                rel = Path(item.filename).relative_to('M12_global_lower_bound')
                self.assertEqual(z.read(item), (ROOT/verify.M12_REL/rel).read_bytes())

    def test_uploaded_input_map(self):
        for item in verify.read_json(ROOT/'provenance/INPUTS.json')['inputs']:
            path=ROOT/item['retained_as']
            self.assertEqual(verify.sha256(path), item['sha256'])
            self.assertEqual(path.stat().st_size, item['bytes'])

    def test_byte_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'a.txt').write_bytes(b'abc')
            entries={'a.txt':{'bytes':3,'sha256':hashlib.sha256(b'abc').hexdigest()}}
            self.assertEqual(verify.check_file_map(p,entries),1)
            (p/'a.txt').write_bytes(b'abd')
            with self.assertRaises(verify.VerificationError):verify.check_file_map(p,entries)

    def test_wrong_length_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'a.txt').write_bytes(b'abc')
            with self.assertRaises(verify.VerificationError):
                verify.check_file_map(p,{'a.txt':{'bytes':4,'sha256':hashlib.sha256(b'abc').hexdigest()}})

    def test_missing_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(verify.VerificationError):verify.safe_file(Path(d),'absent.txt')

    def test_unsafe_manifest_paths_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            for name in ('../outside','/absolute','C:/windows','a\\b'):
                with self.subTest(name=name), self.assertRaises(verify.VerificationError):
                    verify.safe_file(Path(d),name)

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'target').write_text('x')
            try:(p/'link').symlink_to(p/'target')
            except OSError:self.skipTest('Symlinks unavailable on this platform')
            with self.assertRaises(verify.VerificationError):verify.safe_file(p,'link')

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json';p.write_text('{"x":1,"x":2}')
            with self.assertRaises(verify.VerificationError):verify.read_json(p)

    def test_nonfinite_json_constant_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json';p.write_text('{"x":NaN}')
            with self.assertRaises(verify.VerificationError):verify.read_json(p)

    def test_protected_output_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            with self.assertRaises(verify.VerificationError):verify.reserve_output(p/'evidence'/'bad',p)
            self.assertFalse((p/'evidence').exists())

    def test_existing_output_not_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            with self.assertRaises(verify.VerificationError):verify.reserve_output(p)

    def test_new_output_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fresh';self.assertEqual(verify.reserve_output(p),p.resolve())

    def test_optimized_python_refused(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'not-created'
            env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
            p=subprocess.run([sys.executable,'-O','-B',str(ROOT/'verify.py'),'--quick','--output',str(out)],
                             capture_output=True,text=True,env=env,timeout=20)
            self.assertNotEqual(p.returncode,0)
            self.assertIn('Do not use -O',p.stderr)
            self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main()
