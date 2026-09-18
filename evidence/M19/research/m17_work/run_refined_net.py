"""Reuse frozen independent exact sweep; evaluate only newly added directions."""
from pathlib import Path
from fractions import Fraction as F
import hashlib, importlib.util, json, time, argparse

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'workers/T1/outputs/m10_m11/global_followup/certificate.json'
SWEEP=ROOT/'research/m12_work/independent_sweep.py'
SOURCE_SHA='461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652'
SWEEP_SHA='1ddb94bb2a1a0350489752c44a5e9c4622c247f0142570fa5b622675ca652b38'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    if sha(SOURCE)!=SOURCE_SHA or sha(SWEEP)!=SWEEP_SHA: raise ValueError('frozen input drift')
    auth=ROOT/'coord/m17_m18/M17_COMPUTE_AUTHORIZATION.json'
    if not auth.exists(): raise ValueError('not yet authorized')
    spec=importlib.util.spec_from_file_location('m12_frozen_independent',SWEEP)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    record=json.loads(SOURCE.read_text());S,B,atoms,old_ts,static=mod.check_static(record)
    order=[0,89,179]+[k for k in range(180) if k not in [0,89,179]]
    a.output.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter();rows=[];status='BUDGET_EXHAUSTED'
    with (a.output/'DIRECTIONS.jsonl').open('x',encoding='utf-8') as f:
        for k in order:
            if time.perf_counter()-started>120: break
            t=F(2*k+1,2)*F(207107,90000000)
            row=mod.coverage(S,B,atoms,t)
            row['old_interval_index']=k;row['refined_index']=2*k+1
            rows.append(row);f.write(json.dumps(row,sort_keys=True)+'\n');f.flush()
            if len(rows)<=3 or len(rows)%30==0:
                print(json.dumps({'completed':len(rows),'k':k,'minimum':row['minimum'],'seconds':time.perf_counter()-started}),flush=True)
            if 17*F(row['minimum'])<=F(record['total_mass']):
                status='FAIL_FIXED_REFINED_NET_COVERAGE';break
        else: status='PASS_ALL_180_NEW_DIRECTIONS'
    result={'status':status,'source_sha256':SOURCE_SHA,'sweep_sha256':SWEEP_SHA,
            'driver_sha256':sha(Path(__file__)),'authorization_sha256':sha(auth),
            'completed':len(rows),'old_nodes_inherited':181,'planned_new_nodes':180,
            'new_half_tangent_step':'207107/180000000',
            'minimum':str(min(F(r['minimum']) for r in rows)) if rows else None,
            'strict_mass_threshold':str(F(record['total_mass'])/17),
            'seconds':time.perf_counter()-started,'static':static,
            'final_claim':'PENDING_INDEPENDENT_AUDIT'}
    (a.output/'RESULT.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
