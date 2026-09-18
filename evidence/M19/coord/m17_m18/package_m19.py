from pathlib import Path
import ast,hashlib,json,shutil,subprocess,sys
root=Path(__file__).resolve().parents[2];pack=root/'research/proofs/M19_nonuniform_direction_lower_bound'
pack.mkdir(parents=True,exist_ok=False)
def copy(rel):
    src=root/rel;dst=pack/rel;dst.parent.mkdir(parents=True,exist_ok=True)
    if src.is_dir():shutil.copytree(src,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    else:shutil.copy2(src,dst)
checker=root/'workers/T2/outputs/m17_lower/check_m19.py'
tree=ast.parse(checker.read_text(encoding='utf-8'))
paths=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PATHS' for t in n.targets))
for rel in paths.values():copy(rel)
for rel in ['workers/T2/outputs/m17_lower','workers/T1/outputs/m17_m18','research/m17_work','research/m19_work',
 'coord/m17_m18','workers/T1/outputs/m10_m11/global_followup/certificate.json',
 'workers/T1/outputs/m10_m11/global_followup/m12/source/src',
 'research/proofs/M12_global_lower_bound']:
    copy(rel)
shutil.copy2(root/'research/m19_work/PROOF.md',pack/'PROOF.md')
replay='''from pathlib import Path
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
'''
(pack/'replay.py').write_text(replay,encoding='utf-8')
(pack/'README.md').write_text('''# M19 非均匀方向网证据包

运行 `python -B replay.py --output NEW_DIR`：只需Python标准库，完整重算17个新增方向（16通过、1失败），然后独立检查197节点网、质量、继承证据和精确端点。默认重放不需要NumPy、不运行装填优化。M12原181方向的完整历史复演包亦保留，可单独按其README进行全面复演。

T1的不同实现NumPy二维差分复演来源、17行报告、源码与冻结记录完整保存；重新执行它需自行提供对应NumPy环境，并调整只用于环境定位的加载入口。默认标准库重放不执行该来源源码。

M17全361节点方案失败，M19是明确另立的事后确定性复用推论。完整证明PROOF.md、机器证书research/m19_work/CERTIFICATE.json；最终状态见FINAL_ACCEPTANCE.json。源原子/代码及文档许可沿用内含M12包，不改变第三方资料许可。
''',encoding='utf-8')
subprocess.run([sys.executable,'-X','utf8','-B',str(pack/'replay.py'),'--output',str(pack/'t0_portable_replay')],check=True)
print(json.dumps({'status':'PASS','package':str(pack)}))
