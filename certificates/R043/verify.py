#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import argparse, concurrent.futures, gzip, hashlib, json, os, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parent
GZ=ROOT/'certificate/R043_CERTIFICATE.json.gz'
SHA='f0995a8dc6a3a6399be0e9c20c92adf3bb4c247928ade063940d414bd89fcf4b'
OBS=1000181993
BUDGET=17003093868
BOUND=F(461300,99851)
ROWS=7853

def read(path):
    path=Path(path); raw=gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes(); return json.loads(raw.decode('utf-8'))
def need(ok,en,zh):
    if not ok: raise ValueError(en+' / '+zh)
def cert_bytes():
    raw=gzip.decompress(GZ.read_bytes()); need(hashlib.sha256(raw).hexdigest()==SHA,'certificate SHA mismatch','证书 SHA 不匹配'); return raw
def reserve(path):
    p=Path(path).resolve(); need(not p.exists(),'output exists','输出目录已存在'); p.mkdir(parents=True); return p
def materialize(out):
    p=out/'certificate.json'; p.write_bytes(cert_bytes()); return p
def recorded_checks():
    c=json.loads(cert_bytes()); need(F(c['L'])/F(c['A'])==BOUND and c['bound']=='461300/99851','bound identity mismatch','下界身份不匹配'); need(c['budget_units']==BUDGET and c['minimum_units']==OBS and len(c['entries'])==ROWS,'certificate summary mismatch','证书汇总不匹配')
    py=read(ROOT/'results/R043_PYTHON_FULL_REPLAY.json.gz'); bi=read(ROOT/'results/R043_BIGINT_FULL_REPLAY.json'); co=read(ROOT/'results/R043_INDEPENDENT_CONTAINMENT.json'); ac=read(ROOT/'results/R043_ACCEPTANCE.json')
    need(py['status']=='PASS_FULL_EXACT_PYTHON_REPLAY' and bi['status']=='PASS_FULL_EXACT_BIGINT_REPLAY','full replay status mismatch','完整复演状态不匹配'); need(co['status']=='PASS_INDEPENDENT_EXACT_CONTROLS','containment status mismatch','包含审计状态不匹配'); need(ac['status']=='PASS_R043_ACCEPTED_TWO_COMPLETE_EXACT_REPLAYS','acceptance status mismatch','验收状态不匹配')
    need(py['certificate_sha256']==bi['certificate_sha256']==co['certificate_sha256']==ac['certificate_sha256']==SHA,'recorded certificate identity mismatch','记录证书身份不匹配'); need(py['minimum_units']==bi['minimum_units']==OBS and py['budget_units']==bi['budget_units']==BUDGET,'recorded minimum or budget mismatch','记录最低值或预算不匹配'); need({str(k):v for k,v in py['histogram'].items()}=={str(k):v for k,v in bi['histogram'].items()},'full histograms differ','完整直方图不一致'); need(sum(py['histogram'].values())==ROWS and bi['range']==[0,ROWS] and not bi['escape_rows'],'full row coverage mismatch','完整行覆盖不匹配'); need(co['containment']['intervals']==ROWS and co['containment']['quadratic_inequalities']==4*ROWS,'containment count mismatch','包含审计计数不匹配'); need(17*OBS-BUDGET==13,'counting surplus mismatch','计数余量不匹配'); return c
def run_containment(out):
    cert=materialize(out); target=out/'containment.json'; subprocess.run([sys.executable,'-X','utf8','-B','-S',str(ROOT/'src/independent_controls.py'),str(cert),'--containment-only','--output',str(target)],cwd=ROOT/'src',check=True); d=read(target); need(d['certificate_sha256']==SHA and d['containment']['quadratic_inequalities']==31412,'fresh containment mismatch','新鲜包含复演不匹配'); return 'PASS_R043_INDEPENDENT_CONTAINMENT'
def run_python(out,jobs):
    cert=materialize(out); target=out/'python.json'; subprocess.run([sys.executable,'-X','utf8','-B',str(ROOT/'src/replay_parallel.py'),str(cert),'--output',str(target),'--jobs',str(jobs)],cwd=ROOT/'src',check=True); d=read(target); frozen=read(ROOT/'results/R043_PYTHON_FULL_REPLAY.json.gz'); need(d['minimum_units']==OBS and d['histogram']==frozen['histogram'],'fresh Python replay mismatch','新鲜 Python 复演不匹配'); return 'PASS_R043_PYTHON_COMPLETE_EXACT_REPLAY'
def run_bigint(out,jobs):
    need(shutil.which('node') is not None,'Node.js executable not found','未找到 Node.js 可执行程序'); cert=materialize(out); c=read(cert); sys.path.insert(0,str(ROOT/'src')); import prepare_secondary; checker=prepare_secondary.ensure_secondary(); need(hashlib.sha256(checker.read_bytes()).hexdigest()==prepare_secondary.RESULT_SHA,'reconstructed checker SHA mismatch','重建检查器 SHA 不匹配')
    n=len(c['entries']); jobs=max(1,min(jobs,n)); spans=[(j*n//jobs,(j+1)*n//jobs) for j in range(jobs)]
    def one(span):
        lo,hi=span; p=subprocess.run(['node',str(checker),'--certificate',str(cert),'--expected-sha',SHA,'--A',c['A'],'--start',str(lo),'--stop',str(hi)],text=True,capture_output=True,encoding='utf-8',check=True); d=json.loads(p.stdout); need(d['range']==[lo,hi] and not d['escape_rows'],'BigInt chunk geometry mismatch','BigInt 分块几何不匹配'); return d
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex: parts=list(ex.map(one,spans))
    hist={}; mn=min(x['minimum_units'] for x in parts); escapes=[]
    for x in parts:
        escapes.extend(x['escape_rows']);
        for k,v in x['histogram'].items(): hist[str(k)]=hist.get(str(k),0)+v
    frozen=read(ROOT/'results/R043_BIGINT_FULL_REPLAY.json'); need(mn==OBS and hist=={str(k):v for k,v in frozen['histogram'].items()} and not escapes,'fresh BigInt replay mismatch','新鲜 BigInt 复演不匹配'); (out/'bigint.json').write_text(json.dumps({'status':'PASS_R043_BIGINT_COMPLETE_EXACT_REPLAY','certificate_sha256':SHA,'range':[0,n],'minimum_units':mn,'histogram':hist,'escape_rows':escapes},indent=2)+'\n'); return 'PASS_R043_BIGINT_COMPLETE_EXACT_REPLAY'
def main():
    ap=argparse.ArgumentParser(); mode=ap.add_mutually_exclusive_group(); mode.add_argument('--containment',action='store_true'); mode.add_argument('--python-full',action='store_true'); mode.add_argument('--bigint-full',action='store_true'); ap.add_argument('--jobs',type=int,default=5); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args(); need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'),'optimized Python is not supported','不支持 Python 优化模式'); out=reserve(a.output); recorded_checks(); status='PASS_R043_RECORDED_TWO_FULL_EXACT_REPLAYS'
    if a.containment: status=run_containment(out)
    elif a.python_full: status=run_python(out,a.jobs)
    elif a.bigint_full: status=run_bigint(out,a.jobs)
    result={'status':status,'research_id':'N17-R043','strict_lower_bound':'461300/99851','certificate_sha256':SHA,'observed_global_minimum_units':OBS,'budget_units':BUDGET,'counting_surplus_units':13}; (out/'RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(status); return 0
if __name__=='__main__': raise SystemExit(main())
