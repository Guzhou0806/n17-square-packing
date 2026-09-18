from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[2]
paths=['coord/m17_m18/PLAN.md','workers/T1/outputs/m17_m18/PRE_REVIEW.md',
       'workers/T3/outputs/m18_wide_angles/INPUTS_DRAFT.json',
       'workers/T3/outputs/m18_wide_angles/precheck_m18.py',
       'workers/T3/outputs/m18_wide_angles/PRECHECK_REPORT.json',
       'workers/T3/outputs/m15_smooth_upper/precheck_m15.py',
       'research/stages/M16_record_comparison/EXACT_COMPARISON.json']
pre=json.loads((root/paths[4]).read_text())
if pre['status']!='PASS_STAGE_A_PRECHECK' or pre['optimizer_calls']!=0: raise ValueError('precheck not accepted')
obj={'status':'AUTHORIZED_TWO_FIXED_TRIALS','authorized_at':datetime.now(timezone.utc).isoformat(),
     'order':['BURNS','GENERIC'],'released_ids':list(range(17)),'delta':'1/20',
     'solver':'SLSQP','maxiter':2000,'ftol':1e-12,'analytic_jacobian':True,'smooth_rows':816,
     'calls':2,'restarts':0,'extra_position_LP':0,'parameter_tuning':False,
     'source_preservation':'Freeze production source and manifest before calls. Never overwrite an executed version.',
     'rounding':"format(value,'.15f') then Fraction",'repair':'one uniform exact same-directed-branch expansion',
     'certification':'Independent full Fraction SAT and exact comparison with M16 alpha; solver status alone irrelevant.',
     'bindings':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}}
with (root/'coord/m17_m18/M18_COMPUTE_AUTHORIZATION.json').open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
print(json.dumps(obj))
