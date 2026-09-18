"""Deterministic consequence of all M17 passed rows, not another search."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    auth=ROOT/'coord/m17_m18/M19_COMPUTE_AUTHORIZATION.json'
    if not auth.exists():raise ValueError('authorization missing')
    source=ROOT/'workers/T1/outputs/m10_m11/global_followup/certificate.json'
    oldpath=ROOT/'research/m12_work/run_001/DIRECTIONS.jsonl'
    newpath=ROOT/'research/m17_work/run_001/DIRECTIONS.jsonl'
    resultpath=ROOT/'research/m17_work/run_001/RESULT.json'
    old=[json.loads(x) for x in oldpath.read_text().splitlines()]
    new=[json.loads(x) for x in newpath.read_text().splitlines()]
    src=json.loads(source.read_text());mass=F(src['total_mass']);threshold=mass/17
    passed=[r for r in new if F(r['minimum'])>threshold]
    failed=[r for r in new if F(r['minimum'])<=threshold]
    if len(old)!=181 or len(new)!=17 or len(passed)!=16 or len(failed)!=1:raise ValueError('frozen row count mismatch')
    ts=sorted(F(r['t']) for r in old+passed)
    if len(set(ts))!=197:raise ValueError('duplicate or missing direction')
    gaps=[(b-a)/(1+a*b) for a,b in zip(ts,ts[1:])]
    D=max(gaps);worst=gaps.index(D);h=F(207107,90000000)
    if D!=h/(1+210*h*h) or not D<h:raise ValueError('unexpected maximum angular gap')
    m=min(F(r['minimum']) for r in old+passed)
    if not 17*m>mass:raise ValueError('mass contradiction absent')
    L=F(src['outer_side']);B=F(src['square_side'])
    sq=L*L*(1+D*D)/(B*B*(1+D)**2)
    oldsq=L*L*(1+h*h)/(B*B*(1+h)**2)
    if not sq>oldsq:raise ValueError('no lower-bound improvement')
    scale=10**20; floor=isqrt(sq.numerator*scale*scale//sq.denominator)
    lo=F(floor,scale);hi=F(floor+1,scale)
    if not lo*lo<=sq<hi*hi:raise ValueError('decimal interval fails')
    decimal=lambda x:f'{x//scale}.{x%scale:020d}'
    cert={'schema':'n17.m19.nonuniform-grid-lower-bound.v1',
      'status':'PRODUCED_AWAITING_INDEPENDENT_AUDIT',
      'source_sha256':sha(source),'old_rows_sha256':sha(oldpath),'m17_rows_sha256':sha(newpath),
      'm17_result_sha256':sha(resultpath),'producer_sha256':sha(Path(__file__)),
      'selection_rule':'all and only M17 observed rows strictly above total_mass/17; all old nodes retained',
      'old_count':181,'new_pass_count':16,'rejected_count':1,'merged_count':197,
      'passed_refined_indices':[r['refined_index'] for r in passed],
      'failed_refined_indices':[r['refined_index'] for r in failed],
      'directions':list(map(str,ts)),'adjacent_half_gap_tangents':list(map(str,gaps)),
      'maximum_gap':str(D),'maximum_gap_pair':list(map(str,ts[worst:worst+2])),
      'L':str(L),'B':str(B),'mass':str(mass),'minimum_mass':str(m),
      'strict_counting_slack':str(17*m-mass),'threshold':str(threshold),
      'side_square':str(sq),'old_m14_side_square':str(oldsq),'squared_improvement':str(sq-oldsq),
      'radical_expression':f'sqrt({sq.numerator}/{sq.denominator})',
      'decimal_bracket_20':[decimal(floor),decimal(floor+1)],
      'claim':'s(17) >= sqrt(side_square)',
      'endpoint_certificate':False,'claims_strict_endpoint_infeasibility':False,
      'M17_uniform_refinement_status':'FAILED_AND_RETAINED'}
    out=Path(__file__).with_name('CERTIFICATE.json')
    with out.open('x',encoding='utf-8') as f:json.dump(cert,f,indent=2)
    print(json.dumps({k:cert[k] for k in ['maximum_gap','side_square','decimal_bracket_20','strict_counting_slack']}))
if __name__=='__main__':main()
