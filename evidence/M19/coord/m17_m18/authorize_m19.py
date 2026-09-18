from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[2]
paths=['coord/m17_m18/M19_PLAN.md','research/m17_work/run_001/DIRECTIONS.jsonl',
       'research/m17_work/run_001/RESULT.json','research/m19_work/produce_certificate.py',
       'workers/T1/outputs/m17_m18/M19_REVIEW.md','workers/T1/outputs/m17_m18/m19_source_replay_v2.py',
       'workers/T2/outputs/m17_lower/M19_DETERMINISTIC_PRE_REVIEW.md',
       'workers/T2/outputs/m17_lower/M19_STATIC_PRECHECK_ATTEMPT_002.json']
obj={'status':'AUTHORIZED','authorized_at':datetime.now(timezone.utc).isoformat(),
     'source_replay_rows':17,'new_search_directions':0,'source_replay_soft_seconds':30,
     'T1_harness':'workers/T1/outputs/m17_m18/m19_source_replay_v2.py',
     'T0_producer':'research/m19_work/produce_certificate.py',
     'selection':'all 16 M17 passed rows plus all 181 inherited rows; failure retained',
     'acceptance':'T1 full-domain minima match 17 rows; witnesses individually valid, need not share coordinates; T2 independent certificate acceptance',
     'bindings':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}}
with (root/'coord/m17_m18/M19_COMPUTE_AUTHORIZATION.json').open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
print(json.dumps(obj))
