#!/usr/bin/env python3
"""Verify the public R042 package / 验证公开 R042 成果包。"""
from pathlib import Path
from fractions import Fraction as F
import argparse, concurrent.futures, gzip, hashlib, json, os, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parent
CERT_GZ=ROOT/'certificate/R042_CERTIFICATE.json.gz'
SHA='ad47686fdc49121d23b335a1d0cbfc8aa706a5d34bb0eb896aea6992db3d59de'
GZ_SHA='ec79424e30c65bbf31ad1f020b55cc8acebd0cb0f4fbea3e1841fa2b6dda8e28'
BOUND=F(115325,24963)
ROWS=7853
BUDGET=16999227356
REQUIRED=999954551
OBSERVED=1000002306

class VerificationError(RuntimeError): pass

def need(x,en,zh):
    if not x: raise VerificationError(en+' / '+zh)

def read_json(path):
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d: raise VerificationError('duplicate JSON key: '+k+' / JSON 键重复：'+k)
            d[k]=v
        return d
    def bad(x): raise VerificationError('non-finite JSON number / JSON 非有限数值')
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=bad)

def file_sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def certificate_bytes():
    need(file_sha(CERT_GZ)==GZ_SHA,'compressed certificate SHA mismatch','压缩证书 SHA 不匹配')
    raw=gzip.decompress(CERT_GZ.read_bytes())
    need(hashlib.sha256(raw).hexdigest()==SHA,'decompressed certificate SHA mismatch','解压证书 SHA 不匹配')
    return raw

def materialize_certificate(path):
    raw=certificate_bytes(); path.write_bytes(raw); return json.loads(raw)

def check_manifest():
    m=read_json(ROOT/'MANIFEST.json'); need(m['research_id']=='N17-R042','manifest research id mismatch','清单研究编号不匹配')
    count=0
    for item in m['files']:
        rel=item['path']; p=Path(rel)
        need(not p.is_absolute() and '..' not in p.parts and '\\' not in rel,'unsafe manifest path','清单路径不安全')
        q=ROOT/p
        need(q.is_file() and not q.is_symlink(),'manifest file missing or unsafe','清单文件缺失或不安全')
        need(q.stat().st_size==item['bytes'],'manifest byte count mismatch: '+rel,'清单字节数不匹配：'+rel)
        need(file_sha(q)==item['sha256'],'manifest SHA mismatch: '+rel,'清单 SHA 不匹配：'+rel)
        count+=1
    return count

def rows_digest(rows):
    b=json.dumps(rows,separators=(',',':'),sort_keys=True).encode('utf-8')
    return hashlib.sha256(b).hexdigest()

def recorded_checks():
    raw=certificate_bytes(); c=json.loads(raw)
    need(c['A']=='24963/25000' and c['L']=='4613/1000','certificate dimensions mismatch','证书尺寸不匹配')
    need(F(c['L'])/F(c['A'])==BOUND,'bound arithmetic mismatch','下界算术不匹配')
    need(len(c['entries'])==ROWS,'catalogue row count mismatch','目录行数不匹配')
    need(c['budget_units']==BUDGET and c['minimum_units']==REQUIRED,'certificate budget or required minimum mismatch','证书预算或规定最低值不匹配')
    need(17*REQUIRED-BUDGET==11,'required counting margin mismatch','规定计数余量不匹配')
    py=read_json(ROOT/'results/R042_PYTHON_FULL_REPLAY.json')
    bi=read_json(ROOT/'results/R042_BIGINT_FULL_REPLAY.json')
    co=read_json(ROOT/'results/R042_INDEPENDENT_CONTAINMENT.json')
    st=read_json(ROOT/'results/R042_STATIC_VALIDATION.json')
    sc=read_json(ROOT/'results/R042_SCHEMA_AUDIT.json')
    ac=read_json(ROOT/'results/R042_ACCEPTANCE.json')
    for z in (py,bi,co,sc): need(z.get('certificate_sha256',z.get('sha256'))==SHA,'ledger certificate SHA mismatch','账本证书 SHA 不匹配')
    need(st['sha256']==SHA,'static certificate SHA mismatch','静态账本证书 SHA 不匹配')
    need(ac['certificate_sha256']==SHA,'acceptance certificate SHA mismatch','验收账本证书 SHA 不匹配')
    need(py['status']=='PASS_FULL_EXACT_PYTHON_REPLAY' and bi['status']=='PASS_FULL_EXACT_BIGINT_REPLAY','full replay status mismatch','完整复演状态不匹配')
    need(py['intervals']==ROWS and bi['range']==[0,ROWS],'full replay range mismatch','完整复演范围不匹配')
    need(py['minimum_units']==bi['minimum_units']==OBSERVED,'observed minimum mismatch','观测最低值不匹配')
    need(py['histogram']==bi['histogram'] and sum(py['histogram'].values())==ROWS,'full histograms disagree','完整直方图不一致')
    need(not bi['escape_rows'],'BigInt escape rows are nonempty','BigInt 逃逸行非空')
    need(py['counting_surplus_units']==17*OBSERVED-BUDGET==811846,'observed surplus mismatch','观测余量不匹配')
    need(co['status']=='PASS_INDEPENDENT_EXACT_CONTROLS' and co['containment']['intervals']==ROWS and co['containment']['quadratic_inequalities']==4*ROWS,'containment ledger mismatch','包含账本不匹配')
    need(F(co['containment']['minimum_positive_quadratic_numerator'])>0,'nonpositive independent containment margin','独立包含余量非正')
    need(st['counting_margin_at_required']==11 and st['minimum_strict_containment_margin']=='1/1000000000000','static gate mismatch','静态门槛不匹配')
    need(sc['sites']==8988 and sc['physical_triples']==2008 and sc['counting_surplus_units']==11,'schema or budget audit mismatch','模式或预算审计不匹配')
    n=check_manifest()
    return c,py,bi,co,n

def reserve_output(path):
    need(not path.exists(),'output directory already exists','输出目录已经存在')
    path.mkdir(parents=True); return path.resolve()

def compare_python(fresh,frozen):
    keys=['status','certificate_sha256','parent_side','bound','intervals','budget_units','minimum_units','strict_core_margin','counting_surplus_units','slabs','cells','histogram']
    for k in keys: need(fresh[k]==frozen[k],'Python replay field mismatch: '+k,'Python 复演字段不匹配：'+k)
    need(rows_digest(fresh['rows'])==frozen['rows_sha256'],'Python row-ledger digest mismatch','Python 逐行账本摘要不匹配')

def run_containment(out):
    cert=out/'certificate.json'; materialize_certificate(cert)
    target=out/'containment.json'
    cmd=[sys.executable,'-X','utf8','-B','-S',str(ROOT/'src/independent_controls.py'),str(cert),'--containment-only','--output',str(target)]
    subprocess.run(cmd,cwd=ROOT/'src',check=True)
    fresh=read_json(target); frozen=read_json(ROOT/'results/R042_INDEPENDENT_CONTAINMENT.json')
    need(fresh['status']==frozen['status'] and fresh['certificate_sha256']==SHA,'fresh containment identity mismatch','新鲜包含复验身份不匹配')
    need(fresh['containment']==frozen['containment'],'fresh containment ledger mismatch','新鲜包含账本不匹配')
    return 'PASS_R042_INDEPENDENT_CONTAINMENT'

def run_python(out,jobs):
    cert=out/'certificate.json'; materialize_certificate(cert)
    target=out/'python-full.json'
    cmd=[sys.executable,'-X','utf8','-B',str(ROOT/'src/replay_parallel.py'),str(cert),'--output',str(target),'--jobs',str(jobs)]
    subprocess.run(cmd,cwd=ROOT/'src',check=True)
    fresh=read_json(target); frozen=read_json(ROOT/'results/R042_PYTHON_FULL_REPLAY.json'); compare_python(fresh,frozen)
    return 'PASS_R042_PYTHON_COMPLETE_EXACT_REPLAY'

def run_bigint(out,jobs):
    need(shutil.which('node') is not None,'Node.js executable not found','未找到 Node.js 可执行程序')
    cert=out/'certificate.json'; c=materialize_certificate(cert)
    sys.path.insert(0,str(ROOT/'src'))
    import prepare_secondary
    checker=prepare_secondary.ensure_secondary()
    need(file_sha(checker)==prepare_secondary.RESULT_SHA,'reconstructed checker SHA mismatch','重建检查器 SHA 不匹配')
    n=len(c['entries']); jobs=max(1,min(jobs,n)); spans=[(j*n//jobs,(j+1)*n//jobs) for j in range(jobs)]
    def one(span):
        lo,hi=span
        cmd=['node',str(checker),'--certificate',str(cert),'--expected-sha',SHA,'--A',c['A'],'--start',str(lo),'--stop',str(hi)]
        p=subprocess.run(cmd,text=True,capture_output=True,encoding='utf-8',check=True)
        d=json.loads(p.stdout); need(d['range']==[lo,hi] and not d['escape_rows'],'BigInt chunk geometry mismatch','BigInt 分块几何不匹配')
        (out/f'bigint-{lo}-{hi}.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8'); return d
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex: parts=list(ex.map(one,spans))
    hist={}; mn=min(x['minimum_units'] for x in parts); slabs=sum(x['center_slabs'] for x in parts); escapes=[]
    for x in parts:
        escapes.extend(x['escape_rows'])
        for k,v in x['histogram'].items(): hist[k]=hist.get(k,0)+v
    frozen=read_json(ROOT/'results/R042_BIGINT_FULL_REPLAY.json')
    need(mn==frozen['minimum_units']==OBSERVED,'BigInt global minimum mismatch','BigInt 全局最低值不匹配')
    need(hist==frozen['histogram'] and sum(hist.values())==ROWS,'BigInt histogram mismatch','BigInt 直方图不匹配')
    need(slabs==frozen['center_slabs'] and not escapes,'BigInt slab or escape mismatch','BigInt 条带或逃逸不匹配')
    summary={'status':'PASS_R042_BIGINT_COMPLETE_EXACT_REPLAY','certificate_sha256':SHA,'range':[0,n],'ranges':[list(x) for x in spans],'minimum_units':mn,'histogram':hist,'center_slabs':slabs,'escape_rows':escapes}
    (out/'bigint-full.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    return summary['status']

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    mode=ap.add_mutually_exclusive_group()
    mode.add_argument('--containment',action='store_true',help='Fresh independent containment replay / 新鲜独立包含复验')
    mode.add_argument('--python-full',action='store_true',help='Fresh complete Python exact replay / 新鲜完整 Python 精确复演')
    mode.add_argument('--bigint-full',action='store_true',help='Fresh complete BigInt exact replay / 新鲜完整 BigInt 精确复演')
    ap.add_argument('--jobs',type=int,default=4,help='Worker count / 工作进程数')
    ap.add_argument('--output',type=Path,required=True,help='New output directory / 新输出目录')
    a=ap.parse_args()
    need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'),'optimized Python is not supported','不支持 Python 优化模式')
    need(a.jobs>=1,'jobs must be positive','jobs 必须为正数')
    out=reserve_output(a.output)
    try:
        c,py,bi,co,n=recorded_checks()
        status='PASS_R042_RECORDS_ONLY'
        if a.containment: status=run_containment(out)
        elif a.python_full: status=run_python(out,a.jobs)
        elif a.bigint_full: status=run_bigint(out,a.jobs)
        report={'status':status,'research_id':'N17-R042','strict_lower_bound':'115325/24963','certificate_sha256':SHA,'manifest_files_checked':n,'required_counting_margin_units':11,'observed_global_minimum_units':OBSERVED,'observed_counting_surplus_units':811846,'scope':'Fresh full-replay markers require the selected fresh replay path; records-only status never implies fresh geometric recomputation. / 新鲜完整复演标记要求所选冷启动复演路径实际完成；仅账本状态从不代表已重新计算几何覆盖。'}
        (out/'RESULT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(status); return 0
    except BaseException as exc:
        failure={'status':'FAIL_OR_INCOMPLETE','error':f'{type(exc).__name__}: {exc}'}
        (out/'FAILURE.json').write_text(json.dumps(failure,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('FAIL_OR_INCOMPLETE: '+str(exc),file=sys.stderr); return 1

if __name__=='__main__': raise SystemExit(main())
