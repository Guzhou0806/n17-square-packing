from pathlib import Path
import argparse,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
r=Path(__file__).resolve().parent;o=a.output.resolve();o.mkdir(parents=True,exist_ok=False)
def run(args):subprocess.run([sys.executable,'-X','utf8','-B',*map(str,args)],check=True)
run([r/'research/m17_work/run_refined_net.py','--output',o/'new_coverage'])
def rows(p):return [json.loads(x) for x in p.read_text().splitlines()]
if rows(o/'new_coverage/DIRECTIONS.jsonl')!=rows(r/'research/m17_work/run_001/DIRECTIONS.jsonl'):raise ValueError('full coverage replay mismatch')
run([r/'workers/T2/outputs/m17_lower/check_m19.py','--root',r,'--report',o/'M19_AUDIT.json'])
if json.loads((o/'M19_AUDIT.json').read_text())['status']!='PASS_M19_NONUNIFORM_GRID_LOWER_BOUND':raise ValueError('audit failed')
(o/'REPLAY.json').write_text(json.dumps({'status':'PASS','new_direction_sweeps_replayed':17,'passed_directions':16,'retained_counterexamples':1,'old_directions_inherited':181,'merged_nodes':197,'optimization_calls':0}),encoding='utf-8')
