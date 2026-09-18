from pathlib import Path
import hashlib,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
PACK=ROOT/'research/proofs/M12_global_lower_bound'
T1=ROOT/'workers/T1/outputs/m10_m11/global_followup'
T2=ROOT/'workers/T2/outputs/m12_scaling'
assert json.loads((T2/'ATTEMPT_001_AUDIT.json').read_text())['status']=='PASS'
assert json.loads((T2/'ATTEMPT_001_SCALING_BINDING.json').read_text())['status']=='PASS'
assert 'PASS_FOR_REGISTRATION' in (T2/'HANDOFF.md').read_text()
assert not PACK.exists()
PACK.mkdir(parents=True)
ignore=shutil.ignore_patterns('__pycache__','*.pyc')
for relative in ['research/m12_work','workers/T2/outputs/m12_scaling']:
 shutil.copytree(ROOT/relative,PACK/relative,ignore=ignore)
target=PACK/'workers/T1/outputs/m10_m11/global_followup'
target.mkdir(parents=True)
shutil.copytree(T1/'m12',target/'m12',ignore=ignore)
for name in ['certificate.json','DIR-012.md','SWEEP_MATH_REVIEW.md','s16-t022-dilation-limit-proof.md','NETWORK_LOG.jsonl']:
 shutil.copy2(T1/name,target/name)
shutil.copy2(ROOT/'workers/T1/outputs/m10_m11/LICENSE.txt',PACK/'UPSTREAM_LICENSE.txt')
shutil.copytree(ROOT/'coord/m12_scaling',PACK/'protocol',ignore=ignore)
shutil.copy2(ROOT/'coord/m12_scaling/portable_replay_template.py',PACK/'replay.py')
shutil.copy2(ROOT/'research/m12_work/PROOF.md',PACK/'PROOF.md')
(PACK/'ATTRIBUTION.md').write_text('''# Attribution and transformations

Source: Joshua Levy, the squares project (https://github.com/jlevy/squares), commit 035d84c655b4047bc9986c9a3db5106780d92f77. Original data: packing/cases/n17_fractional_certificate/certificate.json, SHA256 461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652.

Source code is retained under upstream MIT terms. Upstream documentation, research and data are attributed under CC BY 4.0; see UPSTREAM_LICENSE.txt. No packing/resources/ third-party archive is redistributed here.

N17 project T0/T1/T2 (AI-assisted research for Guzhou), 2026-09-17: exact coordinate dilation by 1000001/1000000, same weights/direction net; outer/probe side multiplied by the same factor. Explicit scaled data SHA256 6979561eb5137270f7baabc782cafc0580f3483a9bfcdf47fef427484285980c. The derived data retains the source attribution and applicable CC BY 4.0 terms; changes and audit evidence are included. No endorsement by upstream is implied.

The dilation method itself is already described in upstream T-022. Only this fixed N17 instance and its independently checked exact result are claimed. External priority is unknown.
''',encoding='utf-8')
(PACK/'README.md').write_text('''# Exact global lower bound s(17) >= 4.59000459

See PROOF.md for the complete argument and ATTRIBUTION.md for origin and changes.

Portable proof replay, Python 3.12+ standard library only, from any directory:

    python -X utf8 -B /path/to/M12_global_lower_bound/replay.py --output /new/output/directory

It reruns all 181 exact finite directions (about 33 seconds on the original host), verifies source/scaled output agreement, reruns independent geometric fixtures, and binds all 1184 scaled atoms. It does not run optimization or third-party code. Stored source-faithful runs used Python 3.12 and NumPy 2.5.3 with an explicitly recorded CPU-count API shim and one worker; see the retained T1 report. Their immutable source closure and environment lock are included as provenance, not required by portable replay.

The directory mirrors selected original workspace paths so the frozen independent audit resolves its inputs without edits. The independent code and all prior failure records are retained. No world-record or priority claim.
''',encoding='utf-8')
r=subprocess.run([sys.executable,'-X','utf8','-B',str(PACK/'replay.py'),'--output',str(PACK/'t0_portable_replay')])
assert r.returncode==0
print('M12 portable replay complete')
