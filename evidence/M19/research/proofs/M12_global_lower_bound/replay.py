"""Standard-library proof replay; paths are relative to the evidence package."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys

p=argparse.ArgumentParser()
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
root=Path(__file__).resolve().parent
out=a.output.resolve()
out.mkdir(parents=True,exist_ok=False)
source=root/'research/m12_work/independent_sweep.py'
original=root/'workers/T1/outputs/m10_m11/global_followup/certificate.json'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='1ddb94bb2a1a0350489752c44a5e9c4622c247f0142570fa5b622675ca652b38'
run=subprocess.run([sys.executable,'-X','utf8','-B',str(source),'--input',str(original),'--output',str(out/'coverage'),'--seconds','600'],check=True)
result=json.loads((out/'coverage/RESULT.json').read_text())
assert result['status']=='PASS_EXACT_COVERAGE_AND_FIXED_SCALING'
assert result['directions_completed']==181
saved=[json.loads(x) for x in (root/'research/m12_work/run_001/DIRECTIONS.jsonl').read_text().splitlines()]
fresh=[json.loads(x) for x in (out/'coverage/DIRECTIONS.jsonl').read_text().splitlines()]
assert [(r['index'],r['t'],r['minimum']) for r in fresh]==[(r['index'],r['t'],r['minimum']) for r in saved]
auditpath=root/'workers/T2/outputs/m12_scaling/audit_m12.py'
spec=importlib.util.spec_from_file_location('m12_independent_audit',auditpath)
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
module=audit.load_t0()
tests=audit.test_fixture_suite(module)+audit.test_static_gates(module)+[audit.test_full_outputs()]
assert all(t['status']=='PASS' for t in tests)
# Independently bind the archived scaled data to the exact coordinate dilation.
from fractions import Fraction as F
orig=json.loads(original.read_text())
scaledpath=root/'workers/T1/outputs/m10_m11/global_followup/m12/results/scaled_certificate.json'
scaled=json.loads(scaledpath.read_text())
q=F(1000001,1000000)
for key in ('outer_side','square_side'):
 assert F(scaled[key])==q*F(orig[key])
for key in ('n','angle_limit','direction_steps','total_mass','least_cell_mass','symmetry'):
 assert scaled[key]==orig[key]
assert len(scaled['atoms'])==len(orig['atoms'])==1184
for (x,y,w),(xx,yy,ww) in zip(orig['atoms'],scaled['atoms']):
 assert (F(xx),F(yy),F(ww))==(q*F(x),q*F(y),F(w))
report={'status':'PASS','coverage_directions':181,'tests':tests,
 'scaled_atoms_bound':1184,'new_lower_bound':'459000459/100000000',
 'standard_library_only':True,'source_solver_reexecuted':False,
 'meaning':'Full independent coverage replay, archived source/scaled comparison, exact scaling and geometry edge-case tests.'}
(out/'REPLAY.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PASS: global lower bound 459000459/100000000; 181 exact directions and independent audit fixtures.')
