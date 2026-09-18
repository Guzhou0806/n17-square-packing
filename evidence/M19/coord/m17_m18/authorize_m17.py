from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[2]
paths=['coord/m17_m18/PLAN.md','research/m17_work/run_refined_net.py',
       'research/m17_work/THEOREM_DRAFT.md','research/m12_work/independent_sweep.py',
       'workers/T1/outputs/m17_m18/PRE_REVIEW.md',
       'workers/T2/outputs/m17_lower/STAGE_A_STATIC_AUDIT.json']
audit=json.loads((root/paths[-1]).read_text())
if audit['status']!='GO_CONDITIONAL_180_ODD_ROWS_UNCHECKED': raise ValueError('stage A not accepted')
obj={'status':'AUTHORIZED','authorized_at':datetime.now(timezone.utc).isoformat(),
     'question':'Does the fixed T019 measure cover all 180 new midpoint directions above M/17?',
     'maximum_new_directions':180,'pilot_old_interval_indices':[0,89,179],
     'continuation':'remaining ascending unused old interval indices only if all pilot rows pass',
     'strict_threshold':'423327/425000','seconds_soft_limit':120,
     'failure_stop':'first exact row <= threshold; preserve counterexample',
     'bindings':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}}
with (root/'coord/m17_m18/M17_COMPUTE_AUTHORIZATION.json').open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
print(json.dumps(obj))
