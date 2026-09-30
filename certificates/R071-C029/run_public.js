'use strict';
// Public subset orchestration / 公开科学子集启动器
const fs=require('fs'),path=require('path'),cp=require('child_process'),crypto=require('crypto'),assert=require('assert/strict');
const root=__dirname,read=p=>JSON.parse(fs.readFileSync(p,'utf8')),sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const [scope,arg]=process.argv.slice(2);assert(['bound','geometry'].includes(scope));assert(arg&&process.argv.length===4);
require('./check_package.js');
const planOnly=arg==='--plan-only',out=path.resolve(planOnly?path.join(root,'.plan-only'):arg),bin=path.join(out,'bin'),res=path.join(out,'results'),jobs=[];
const old=path.join(root,'project/followup_c028'),cur=path.join(root,'project/followup_c029'),ext=process.platform==='win32'?'.exe':'',compiler=process.env.CXX||'g++';
const job=(id,exe,args)=>jobs.push({id,exe,args}),node=(id,file,args)=>job(id,process.execPath,[file,...args]);
function compile(folder,name){job('compile_'+name,compiler,['-O2','-std=c++17','-Wall','-Wextra','-Werror',path.join(folder,'src',name+'.cpp'),'-o',path.join(bin,name+ext)]);}
function pair(folder,name,args,cargs=args){job(name+'_cpp',path.join(bin,name+ext),[...cargs,path.join(res,name+'_cpp.json')]);node(name+'_bigint',path.join(folder,'src',name+'.js'),[...args,path.join(res,name+'_bigint.json')]);}
const expected=[];
if(scope==='bound'){
 job('compile_global',compiler,['-O3','-std=c++17',path.join(root,'project/base/upstream/cpp/verify.cpp'),'-o',path.join(bin,'verify'+ext)]);
 node('global_dual_replay',path.join(root,'project/base/upstream/cpp/replay.js'),[path.join(root,'bounds/c027/certificate.json'),path.join(out,'global'),path.join(bin,'verify'+ext),'2']);
}else{
 for(const n of ['stabbing','atlas','frontier','predicates'])compile(old,n);
 const d=path.join(old,'data'),spec=path.join(d,'atlas.json');
 pair(old,'stabbing',[path.join(d,'stabbing.json')]);
 pair(old,'atlas',[spec,path.join(d,'atlas.tree')],['verify',spec,'v2',path.join(d,'atlas.tree')]);
 job('frontier_cpp',path.join(bin,'frontier'+ext),[spec,path.join(res,'atlas_cpp.json'),path.join(d,'frontier_witnesses.json'),path.join(root,'project/followup_c026/data/finite_comparison.json'),path.join(res,'frontier_cpp.json')]);
 node('frontier_bigint',path.join(old,'src/frontier.js'),[spec,path.join(res,'atlas_bigint.json'),path.join(d,'frontier_witnesses.json'),path.join(root,'project/followup_c026/data/finite_comparison.json'),path.join(res,'frontier_bigint.json')]);
 pair(old,'predicates',[path.join(d,'predicates.json')]);
 node('c028_controls',path.join(old,'src/controls.js'),[root,bin,res,path.join(out,'controls-c028')]);
 for(const n of ['stabbing','atlas','frontier','predicates'])expected.push([n,path.join(old,'results',(n==='atlas'?'atlas_final':n)+'_cpp.json')]);
 for(const n of ['pair_verify','owner_verify','joint_graph'])compile(cur,n);
 const data=path.join(cur,'data'),front=path.join(old,'results/frontier_cpp.json'),atlas=path.join(old,'results/atlas_final_cpp.json'),graph=read(path.join(data,'joint_graph.json'));
 for(const [a,b] of graph.edges){
  const name='pair_'+String(a).padStart(2,'0')+'_'+String(b).padStart(2,'0'),args=[spec,front,path.join(data,'component_pairs.json'),a+','+b,path.join(data,name+'.tree')];
  job(name+'_cpp',path.join(bin,'pair_verify'+ext),[...args,path.join(res,name+'_cpp.json')]);node(name+'_bigint',path.join(cur,'src/pair_verify.js'),[...args,path.join(res,name+'_bigint.json')]);expected.push([name,path.join(cur,'results',name+'_cpp.json')]);
 }
 for(const name of ['fullowner_00_00','fullowner_10_02']){
  const args=[spec,front,path.join(data,'full_owner_cases.json'),name,path.join(data,name+'.tree')];job(name+'_cpp',path.join(bin,'owner_verify'+ext),[...args,path.join(res,name+'_cpp.json')]);node(name+'_bigint',path.join(cur,'src/owner_verify.js'),[...args,path.join(res,name+'_bigint.json')]);expected.push([name,path.join(cur,'results',name+'_cpp.json')]);
 }
 pair(cur,'joint_graph',[spec,atlas,front,path.join(data,'joint_graph.json'),res]);expected.push(['joint_graph',path.join(cur,'results/joint_graph_cpp.json')]);
 for(const group of ['pair','owner','graph'])node('c029_controls_'+group,path.join(cur,'src/controls.js'),[root,bin,res,group,path.join(out,'controls-c029',group)]);
}
// Resolve every package input without executing proof jobs / 解析全部包内输入，不执行证明任务
for(const j of jobs)for(const a of j.args)if(a.startsWith(root+path.sep)&&!a.startsWith(out+path.sep))assert(fs.existsSync(a),'Missing package input: '+a);
if(planOnly){console.log(JSON.stringify({scope,jobs:jobs.length,paired_results:expected.length,status:'PLAN_ONLY_NO_MATHEMATICS'}));process.exit(0);}
assert(!fs.existsSync(out),'Fresh output required');fs.mkdirSync(bin,{recursive:true});fs.mkdirSync(res);fs.mkdirSync(path.join(out,'logs'));
const records=[];let active='initialization';
function save(name,value){fs.writeFileSync(path.join(out,name),JSON.stringify(value,null,2)+'\n');}
try{
 for(const j of jobs){active=j.id;const start=new Date().toISOString();const r=cp.spawnSync(j.exe,j.args,{cwd:root,encoding:'utf8',timeout:scope==='bound'?10200000:600000,maxBuffer:32*1024*1024});fs.writeFileSync(path.join(out,'logs',j.id+'.stdout'),r.stdout||'');fs.writeFileSync(path.join(out,'logs',j.id+'.stderr'),r.stderr||'');records.push({id:j.id,command:[j.exe,...j.args],start,end:new Date().toISOString(),exit:r.status,signal:r.signal,error:r.error?String(r.error):null});save('PROGRESS.json',{status:'PREFIX_NOT_COMPLETE',scope,records});assert(!r.error&&!r.signal&&r.status===0,j.id+': '+r.stderr);console.log('DONE '+records.length+'/'+jobs.length+' '+j.id);}
 if(scope==='bound'){
  const t=read(path.join(out,'global/THEOREM.json'));assert.equal(t.status,'PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION');assert.equal(t.target,'18641771/4000000');assert.equal(t.intervals,5114);assert.equal(String(t.minimum_units),'1000026844');assert.equal(String(t.budget_units),'17000448944');assert.equal(String(t.surplus),'7404');assert.equal(t.certificate_sha256,'15b6bf6a936eba71338c9ea3e3b9966ae21db8116a6f5a92a8b5da5ccabed469');
 }else{
  for(const [n,p] of expected){assert.equal(sha(path.join(res,n+'_cpp.json')),sha(p),n+' frozen result');assert.equal(sha(path.join(res,n+'_bigint.json')),sha(p),n+' BigInt result');}
  const c=read(path.join(out,'controls-c028/CONTROLS.json'));assert.equal(c.status,'PASS_C028_DIRECT_MATHEMATICAL_CONTROLS');assert.equal(c.negative_executions,96);assert.equal(c.positive_executions,12);assert(c.records.every(r=>r.passed));
  let neg=0,pos=0;for(const g of ['pair','owner','graph']){const t=read(path.join(out,'controls-c029',g,'CONTROLS.json'));assert.equal(t.status,'PASS_C029_DIRECT_CONTROLS');assert(t.records.every(r=>r.passed));neg+=t.negative_executions;pos+=t.positive_executions;}assert.equal(neg,64);assert.equal(pos,8);
 }
 save('REPLAY.json',{status:scope==='bound'?'PASS_R071_C027_GLOBAL_REPLAY':'PASS_R071_C028_C029_SCOPED_GEOMETRY',scope,records,source_manifest_sha256:sha(path.join(root,'MANIFEST.json')),new_global_bound_from_c029:false});console.log('PASS '+scope);
}catch(e){save('FAILED.json',{status:'FAILED',scope,active,error:String(e),records});throw e;}
