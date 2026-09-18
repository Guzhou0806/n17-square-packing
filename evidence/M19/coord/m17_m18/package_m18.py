from pathlib import Path
import json,shutil,subprocess,sys,hashlib,zipfile
root=Path(__file__).resolve().parents[2];pack=root/'research/experiments/M18_wide_angles'
pack.mkdir(parents=True,exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,obj):
    with p.open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2)
def copy(rel):
    src=root/rel;dst=pack/rel;dst.parent.mkdir(parents=True,exist_ok=True)
    if src.is_dir():shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    else:shutil.copy2(src,dst)
for rel in ['workers/T3/outputs/m18_wide_angles','research/m18_audit',
 'baselines/verified/M1_rational_seed/verifier.py',
 'baselines/verified/M8_Burns_rational/witness.json','baselines/verified/M8_Generic_rational/witness.json',
 'baselines/verified/M15_G17_smooth_upper/witness.json','research/stages/M16_record_comparison',
 'coord/m17_m18/PLAN.md','coord/m17_m18/M18_COMPUTE_AUTHORIZATION.json',
 'workers/T1/outputs/m17_m18/PRE_REVIEW.md',
 'workers/T3/outputs/m15_smooth_upper/precheck_m15.py',
 'workers/T3/outputs/m15_smooth_upper/production/run_m15_two_smooth_nlp.py']:
    copy(rel)
shutil.copy2(root/'reports/M18_WIDE_ANGLE_REPORT.md',pack/'REPORT.md')
replay='''from pathlib import Path
import argparse,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
r=Path(__file__).resolve().parent
subprocess.run([sys.executable,'-X','utf8','-B',str(r/'research/m18_audit/audit_returned_witnesses.py'),'--output',str(a.output.resolve())],check=True)
'''
(pack/'replay.py').write_text(replay,encoding='utf-8')
subprocess.run([sys.executable,'-X','utf8','-B',str(pack/'replay.py'),'--output',str(pack/'t0_portable_replay')],check=True)
audit=json.loads((pack/'t0_portable_replay/AUDIT.json').read_text())
if audit['status']!='PASS_TWO_REPAIRED_WITNESSES_NO_RECORD_NO_PROJECT_BEST':raise ValueError('portable replay failed')
accept={'status':'ACCEPTED_FINITE_NEGATIVE_EXPERIMENT','milestone':'M18',
 'record_improvement':False,'project_best_improvement':False,'feasible_repaired_candidates':2,
 'raw_generic_exact_binary_geometry':'FAIL','portable_replay':'PASS',
 'independent_scope':audit['scope'],'reported_optimizer_calls':2,
 'certificate_sha256':sha(root/'research/m18_audit/run_001/AUDIT.json')}
dump(pack/'FINAL_ACCEPTANCE.json',accept);dump(root/'coord/m17_m18/M18_FINAL_ACCEPTANCE.json',accept)
files={p.relative_to(pack).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(pack.rglob('*')) if p.is_file()}
dump(pack/'MANIFEST.json',{'files':files})
zpath=pack.with_suffix('.zip')
with zipfile.ZipFile(zpath,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(pack.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(pack.parent))
with zipfile.ZipFile(zpath) as z:
    if z.testzip() is not None:raise ValueError('CRC failure')
    for rel,r in files.items():
        if hashlib.sha256(z.read(pack.name+'/'+rel)).hexdigest()!=r['sha256']:raise ValueError('archive mismatch')
dump(root/'coord/m17_m18/M18_ARCHIVE_RECEIPT.json',{'zip':zpath.relative_to(root).as_posix(),'sha256':sha(zpath),'bytes':zpath.stat().st_size})
print(json.dumps({'status':'PASS','archive_sha256':sha(zpath),'files':len(files)+1}))
