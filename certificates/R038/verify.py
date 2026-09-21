#!/usr/bin/env python3
"""R038 public verifier / R038 公开验证器。

Records mode checks frozen arithmetic and file identity only. / records 模式只检查冻结算术与文件身份。
Full mode additionally reruns every exact geometric chunk against the pinned upstream certificate. / full 模式还会针对锁定上游证书重新运行全部精确几何分块。
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PIN = '5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3'
A = '99974999999/100000000000'
RANGES = [(0,500),(500,1500),(1500,2500),(2500,3500),(3500,4391)]
FULL = 'PASS_R038_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND'
RECORDS = 'PASS_R038_RECORDS_ONLY'


def need(ok, en, zh):
    if not ok:
        raise ValueError(f'{en} / {zh}')


def readj(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def integrity():
    m = readj(ROOT/'MANIFEST.json')
    expected = {x['path']:(x['bytes'],x['sha256']) for x in m['files']}
    actual = {p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('*') if p.is_file() and p.name != 'MANIFEST.json' and '__pycache__' not in p.parts and '.replay-runs' not in p.parts}
    need(set(expected)==set(actual),'manifest file set mismatch','清单文件集合不匹配')
    for name,path in actual.items():
        got=(path.stat().st_size,sha256(path))
        need(got==expected[name],f'manifest mismatch: {name}',f'清单哈希或字节数不匹配：{name}')
    return len(actual)


def recorded_checks():
    c=readj(ROOT/'CLAIMS.json')
    q=readj(ROOT/'results/R038_CONTAINMENT.json')
    b=readj(ROOT/'results/R038_BASE_CONTROL_CHUNKS.json')
    a=readj(ROOT/'results/R038_AUGMENTED_CONTROL_CHUNKS.json')
    need(q['strict_positive'] and F(q['new_minimum_containment_margin_lower_bound'])>0,'strict containment failed','严格内含检查失败')
    need(b['rows']==4391 and b['global_minimum_units']==1000000030 and b['mass_units']==16999991644,'base ledger mismatch','基础测度账本不匹配')
    need(b['counting_surplus_units']==8866 and b['escape_rows']==0 and b['center_slabs']==27918671,'base totals mismatch','基础测度汇总不匹配')
    need(b['histogram']=={'1000000030':2860,'1000000032':1428,'1000000035':103},'base histogram mismatch','基础测度直方图不匹配')
    need(a['rows']==4391 and a['global_minimum_units']==1000000032 and a['mass_units']==16999991652,'augmented ledger mismatch','增广测度账本不匹配')
    need(a['counting_surplus_units']==8892 and a['escape_rows']==0 and a['center_slabs']==27967621,'augmented totals mismatch','增广测度汇总不匹配')
    need(a['histogram']=={'1000000032':2860,'1000000034':1428,'1000000037':103},'augmented histogram mismatch','增广测度直方图不匹配')
    target=F(4613,1000)/F(99974999999,100000000000)
    need(str(target)==c['strict_lower_bound_reduced'],'target arithmetic mismatch','端点精确算术不匹配')
    need(17*b['global_minimum_units']>b['mass_units'],'base counting contradiction failed','基础测度计数矛盾失败')
    need(17*a['global_minimum_units']>a['mass_units'],'augmented counting contradiction failed','增广测度计数矛盾失败')
    return c,q,b,a


def merge_chunks(chunks):
    hist={}; slabs=0; minimum=None; escapes=[]
    for z in chunks:
        minimum=z['minimum_units'] if minimum is None else min(minimum,z['minimum_units'])
        slabs += z['center_slabs']
        for k,v in z['histogram'].items(): hist[k]=hist.get(k,0)+v
        escapes.extend(z['escape_rows'])
    return minimum,hist,slabs,escapes


def full_geometry(certificate, out, base_record, augmented_record):
    need(shutil.which('node') is not None,'Node.js executable not found','未找到 Node.js 可执行程序')
    need(sha256(certificate)==PIN,'certificate SHA mismatch','证书 SHA 不匹配')
    scan=ROOT/'src/exact_parent_side_scan.js'
    for measure,record in [('base',base_record),('combined',augmented_record)]:
        chunks=[]
        for start,stop in RANGES:
            cmd=['node',str(scan),'--certificate',str(certificate),'--A',A,'--measure',measure,'--start',str(start),'--stop',str(stop)]
            p=subprocess.run(cmd,text=True,capture_output=True,encoding='utf-8')
            (out/f'{measure}-{start}-{stop}.stdout.json').write_text(p.stdout,encoding='utf-8')
            (out/f'{measure}-{start}-{stop}.stderr.log').write_text(p.stderr,encoding='utf-8')
            need(p.returncode==0,f'geometric chunk failed: {measure} {start}:{stop}',f'几何分块失败：{measure} {start}:{stop}')
            z=json.loads(p.stdout); chunks.append(z)
            frozen=next(x for x in record['chunks'] if x['range']==[start,stop])
            need(z['range']==[start,stop] and z['histogram']==frozen['histogram'],'chunk histogram mismatch','分块直方图不匹配')
            need(z['center_slabs']==frozen['slabs'] and len(z['escape_rows'])==frozen['escape_rows'],'chunk geometry totals mismatch','分块几何汇总不匹配')
        minimum,hist,slabs,escapes=merge_chunks(chunks)
        need(minimum==record['global_minimum_units'],'global minimum mismatch','全局最低值不匹配')
        need(hist==record['histogram'] and slabs==record['center_slabs'] and not escapes,'merged geometry mismatch','合并几何结果不匹配')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--certificate',type=Path,help='Pinned upstream certificate for full replay / 完整复演所需的锁定上游证书')
    ap.add_argument('--output',type=Path,required=True,help='New output directory / 新输出目录')
    args=ap.parse_args()
    need(not sys.flags.optimize,'optimized Python is not supported','不支持 Python 优化模式')
    need(not os.environ.get('PYTHONOPTIMIZE'),'PYTHONOPTIMIZE is not supported','不支持 PYTHONOPTIMIZE')
    need(not args.output.exists(),'output directory already exists','输出目录已经存在')
    args.output.mkdir(parents=True)
    try:
        c,q,b,a=recorded_checks(); n=integrity()
        status=RECORDS
        if args.certificate is not None:
            full_geometry(args.certificate,args.output,b,a); status=FULL
        report={
          'status':status,'research_id':'N17-R038','claim':c['claim'],'strict_lower_bound':c['strict_lower_bound'],
          'strict_lower_bound_reduced':c['strict_lower_bound_reduced'],'integrity_files':n,
          'base_counting_surplus_units':b['counting_surplus_units'],'augmented_counting_surplus_units':a['counting_surplus_units'],
          'geometry_recomputed':args.certificate is not None,
          'scope':'Full status requires the SHA-pinned upstream certificate and all ten exact chunk scans; records-only status does not establish geometric coverage. / 完整状态要求 SHA 锁定的上游证书与十个精确分块扫描；仅账本状态不能建立几何覆盖。'
        }
        (args.output/'RESULT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(status)
        return 0
    except BaseException as exc:
        fail={'status':'FAIL_OR_INCOMPLETE','error':f'{type(exc).__name__}: {exc}'}
        (args.output/'FAILURE.json').write_text(json.dumps(fail,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f"FAIL_OR_INCOMPLETE: {exc}",file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
