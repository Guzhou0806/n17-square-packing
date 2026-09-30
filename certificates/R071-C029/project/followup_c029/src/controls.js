'use strict';
// Direct mathematical mutations. Hash mismatch alone is not an accepted rejection.
const fs=require('fs'),path=require('path'),cp=require('child_process'),crypto=require('crypto');
const need=(x,s)=>{if(!x)throw Error(s);},hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
try{
 need(process.argv.length===7,'USAGE_ROOT_BIN_RECEIPTS_GROUP_NEW_OUTPUT');const[root,bin,receipts,group,out]=process.argv.slice(2);need(['pair','owner','graph'].includes(group),'CONTROL_GROUP');need(!fs.existsSync(out),'FRESH_OUTPUT_REQUIRED');fs.mkdirSync(out,{recursive:true});
 const src=path.join(root,'project/followup_c029/src'),data=path.join(root,'project/followup_c029/data'),old=path.join(root,'project/followup_c028'),spec=path.join(old,'data/atlas.json'),front=path.join(old,'results/frontier_cpp.json'),atlas=path.join(old,'results/atlas_final_cpp.json');
 const read=p=>JSON.parse(fs.readFileSync(p,'utf8')),copy=x=>JSON.parse(JSON.stringify(x));let tasks=[];
 function put(name,x){let p=path.join(out,name);fs.writeFileSync(p,typeof x==='string'?x:JSON.stringify(x)+'\n');return p;}
 function task(id,name,args,reason,positive=false){tasks.push({id,name,args,reason,positive});}
 if(group==='pair'){
  const input=path.join(data,'component_pairs.json'),tree=path.join(data,'pair_00_01.tree'),j=read(input),full=fs.readFileSync(tree,'utf8');
  const mutate=(id,fn,reason)=>{let x=copy(j);fn(x);task(id,'pair_verify',[spec,front,put(id+'.json',x),'0,1',tree],reason);};
  mutate('schema',x=>x.schema='bad','SCHEMA');mutate('target',x=>x.cap='467/100','TARGET_IDENTITY');mutate('anchor',x=>x.anchor[0][0]='1/1','ANCHOR_IDENTITY');mutate('grid',x=>x.grid[0][0]='1/1','GRID_IDENTITY');mutate('root',x=>x.roots[0][0][0]='1/2','COMPONENT_ROOT');mutate('angle',x=>x.roots[0][2][0]='-1/10','ANGLE_CHART');
  task('pair_range','pair_verify',[spec,front,input,'0,18',tree],'PAIR_RANGE');
  for(const[id,text,reason]of[['header','BAD\n','TREE_HEADER'],['truncated','C029_PAIR_V1\n','TREE_TRUNCATED'],['extra',full+'X\n','TREE_EXTRA'],['overlap','C029_PAIR_V1\nX\n','UNPROVED_PAIR_OVERLAP'],['split','C029_PAIR_V1\nS 0 3\n','SPLIT_INDEX'],['capture','C029_PAIR_V1\nP 0 15\n','UNPROVED_GRID_CAPTURE'],['unresolved','C029_PAIR_V1\nU 0 0\n','UNKNOWN_OPCODE']])task(id,'pair_verify',[spec,front,input,'0,1',put(id+'.tree',text)],reason);
  task('valid_other_pair','pair_verify',[spec,front,input,'0,3',path.join(data,'pair_00_03.tree')],'PASS',true);
 }else if(group==='owner'){
  const input=path.join(data,'full_owner_cases.json'),tree=path.join(data,'fullowner_00_00.tree'),id='fullowner_00_00',j=read(input);
  const mutate=(n,fn,reason)=>{let x=copy(j);fn(x.cases.find(r=>r.id===id));task(n,'owner_verify',[spec,front,put(n+'.json',x),id,tree],reason);};
  mutate('root',x=>x.root[0][0]='1/1','OWNER_ROOT_COVERAGE');mutate('angles',x=>x.root[2][0]='1/1000','OWNER_ALL_ANGLES');mutate('point',x=>x.point=1,'CASE_RANGE');
  for(const[n,t,reason]of[['wrong_N','C029_AVOID_OWNER_V1\nN 0 0\n','UNPROVED_REQUIRED_POINT_MISS'],['wrong_P','C029_AVOID_OWNER_V1\nP 1 0\n','UNPROVED_AVOIDER_GRID_CAPTURE'],['overlap','C029_AVOID_OWNER_V1\nX\n','UNPROVED_PAIR_OVERLAP'],['truncated','C029_AVOID_OWNER_V1\n','TREE_TRUNCATED']])task(n,'owner_verify',[spec,front,input,id,put(n+'.tree',t)],reason);
  task('bad_id','owner_verify',[spec,front,input,'missing',tree],'CASE_ID');
  task('valid_other_hole','owner_verify',[spec,front,input,'fullowner_10_02',path.join(data,'fullowner_10_02.tree')],'PASS',true);
 }else{
  const input=path.join(data,'joint_graph.json'),j=read(input);const mutate=(n,fn,reason,positive=false)=>{let x=copy(j);fn(x);task(n,'joint_graph',[spec,atlas,front,put(n+'.json',x),receipts],reason,positive);};
  mutate('schema',x=>x.schema='bad','SCHEMA');mutate('duplicate_edge',x=>x.edges.push(x.edges[0]),'PAIR_RANGE_OR_DUPLICATE');mutate('matching',x=>x.matching[0]=[0,17],'INVALID_MATCHING');mutate('count',x=>x.expected_counts[1]++,'GRAPH_COUNT_MISMATCH');mutate('incomplete_pairs',x=>x.unknown_pairs.pop(),'PAIR_INVENTORY_COMPLETE');mutate('outside_wall',x=>x.compatible_pairs[0].poses[0].cx='-1/1','ILLEGAL_WITNESS');mutate('wrong_component',x=>x.compatible_pairs[0].poses[0]=copy(x.anchor),'WITNESS_COMPONENT');mutate('zero_width',x=>x.partial_halfwidths[0]='0/1','POSITIVE_WIDTH');mutate('duplicate_partial',x=>x.partial_components[1]=x.partial_components[0],'PARTIAL_COMPONENT');mutate('false_maximum',x=>x.max_independent_mask=0,'MAX_GRAPH_WITNESS');
  mutate('valid_reordered',x=>{x.compatible_pairs.reverse();x.matching.reverse();},'PASS',true);
  mutate('valid_smaller_boxes',x=>x.partial_halfwidths=['1/2000000','1/2000000','1/20000000'],'PASS',true);
 }
 let records=[];const ext=process.platform==='win32'?'.exe':'';
 for(const t of tasks)for(const lang of['cpp','bigint']){
  const op=path.join(out,t.id+'_'+lang+'.json'),exe=lang==='cpp'?path.join(bin,t.name+ext):process.execPath,args=lang==='cpp'?[...t.args,op]:[path.join(src,t.name+'.js'),...t.args,op];let start=new Date().toISOString(),r=cp.spawnSync(exe,args,{encoding:'utf8',timeout:60000,maxBuffer:4*1024*1024});
  const stdout=path.join(out,t.id+'_'+lang+'.stdout'),stderr=path.join(out,t.id+'_'+lang+'.stderr');fs.writeFileSync(stdout,r.stdout||'');fs.writeFileSync(stderr,r.stderr||'');
  let passed=!r.error&&!r.signal&&(t.positive?r.status===0&&fs.existsSync(op)&&String(r.stdout).includes('PASS'):r.status!==0&&!fs.existsSync(op)&&String(r.stderr).includes('REJECT '+t.reason));
  records.push({id:t.id,lang,positive:t.positive,expected:t.reason,command:[exe,...args],started_utc:start,finished_utc:new Date().toISOString(),exit:r.status,signal:r.signal,error:r.error?String(r.error):null,passed,stdout_sha256:hash(stdout),stderr_sha256:hash(stderr),input_files:t.args.filter(x=>fs.existsSync(x)&&fs.statSync(x).isFile()).map(p=>({path:p,sha256:hash(p)}))});
  fs.writeFileSync(path.join(out,'CONTROLS.json'),JSON.stringify({status:passed?'RUNNING':'FAILED',group,records},null,2)+'\n');need(passed,'UNEXPECTED_CONTROL '+t.id+' '+lang+' '+(r.stderr||''));
 }
 let result={schema:'n17.c029.controls.v1',status:'PASS_C029_DIRECT_CONTROLS',group,negative_executions:records.filter(x=>!x.positive).length,positive_executions:records.filter(x=>x.positive).length,records};fs.writeFileSync(path.join(out,'CONTROLS.json'),JSON.stringify(result,null,2)+'\n');console.log('PASS '+group+' negative='+result.negative_executions+' positive='+result.positive_executions);
}catch(e){console.error('REJECT '+e.message);process.exit(1);}
