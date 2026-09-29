// Full native C++ + independent upstream BigInt replay. No Python dependency.
'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),cp=require('child_process');
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const need=(v,m)=>{if(!v)throw Error(m)};
async function main(){
 const [certificateArg,outputArg,exeArg,workerArg='2']=process.argv.slice(2);
 need(certificateArg&&outputArg&&exeArg,'node replay.js certificate.json NEW_OUTPUT_DIRECTORY verify-executable [workers]');
 const certificate=path.resolve(certificateArg),out=path.resolve(outputArg),exe=path.resolve(exeArg),workers=Number(workerArg);
 const reference=path.join(__dirname,'reference','verify_global_variable.js');
 const certificateRaw=fs.readFileSync(certificate);
 const cert=JSON.parse(certificateRaw.toString('utf8').replace(/([:\[,]\s*)(-?\d+)(?=\s*[,}\]])/g,'$1"$2"'));
 const N=cert.entries.length;need(Number.isSafeInteger(workers)&&workers>=1&&workers<=8&&workers<=N,'workers 1..8');
 fs.mkdirSync(out,{recursive:false});
 const bindings={certificate_sha256:crypto.createHash('sha256').update(certificateRaw).digest('hex'),executable_sha256:hash(exe),reference_sha256:hash(reference),launcher_sha256:hash(__filename)};
 fs.writeFileSync(path.join(out,'INPUTS.json'),JSON.stringify(bindings,null,2));
 const commands=[];
 for(let i=0;i<workers;i++){const lo=Math.floor(N*i/workers),count=Math.floor(N*(i+1)/workers)-lo;
  commands.push([exe,[certificate,path.join(out,`cpp-${i}.json`),'--range',String(lo),String(count)],`cpp-${i}`]);
  commands.push([process.execPath,[reference,certificate,path.join(out,`node-${i}.json`),String(lo),String(count),'audit'],`node-${i}`]);
 }
 const timeoutMinutes=Number(process.env.N17_TIMEOUT_MINUTES||'60');need(Number.isFinite(timeoutMinutes)&&timeoutMinutes>0,'timeout');
 const children=new Set();const stopAll=()=>{for(const child of children)child.kill()};
 const start=Date.now();const processes=await Promise.all(commands.map(([command,args,label])=>new Promise((resolve,reject)=>{
  const log=fs.openSync(path.join(out,label+'.log'),'wx');const child=cp.spawn(command,args,{windowsHide:true,stdio:['ignore',log,log]});children.add(child);let expired=false,error=null;
  const timer=setTimeout(()=>{expired=true;child.kill();},timeoutMinutes*60000);
  child.on('error',e=>{error=String(e);stopAll()});
  child.on('close',(exit,signal)=>{clearTimeout(timer);fs.closeSync(log);children.delete(child);if(exit!==0)stopAll();resolve({label,exit,signal,expired,error})});
 })));
 need(processes.every(p=>p.exit===0&&!p.expired),'checker process failed; inspect logs; no theorem accepted');
 const cpp=[],node=[];
 for(let i=0;i<workers;i++)for(const [kind,rows]of [['cpp',cpp],['node',node]]){
  const d=JSON.parse(fs.readFileSync(path.join(out,`${kind}-${i}.json`),'utf8'));
  need(d.certificate_sha256===bindings.certificate_sha256,'input identity mismatch');
  if(kind==='cpp'){const q=s=>String(s).split('/').map(BigInt),a=q(d.target),b=q(cert.normalized_target);need(a[0]*(b[1]||1n)===b[0]*(a[1]||1n),'target mismatch');}
  need(String(d.budget_units)===String(cert.budget_units)&&String(d.required_units)===String(cert.minimum_units),'budget/threshold mismatch');
  need(d.start===Math.floor(N*i/workers)&&d.end_exclusive===Math.floor(N*(i+1)/workers),'partition range mismatch');
  need(d.total_intervals===N&&d.rows.length===d.end_exclusive-d.start,'partition incomplete');
  const allowed=kind==='cpp'?['PASS_INTERVAL_PARTITION','PASS_COMPLETE_SEVENTEEN_SQUARE_EXCLUSION']:['PASS_INDEPENDENT_INTERVAL_PARTITION','PASS_INDEPENDENT_GLOBAL_THRESHOLD_CERTIFICATE'];need(allowed.includes(d.status),'partition status');
  rows.push(...d.rows);
 }
 need(cpp.length===N&&node.length===N,'incomplete coverage');let minimum=null;
 for(let i=0;i<N;i++){
  need(cpp[i].interval===i&&node[i].interval===i,'missing/duplicate/reordered interval');
  need(Number.isSafeInteger(cpp[i].minimum_units)&&Number.isSafeInteger(cpp[i].cells)&&cpp[i].cells>0&&Number.isSafeInteger(node[i].cells)&&node[i].cells>0,'receipt integer range exceeded');
  need(BigInt(cpp[i].minimum_units)===BigInt(node[i].minimum_units)&&BigInt(cpp[i].cells)===BigInt(node[i].cells),'row mismatch '+i);
  const v=BigInt(cpp[i].minimum_units);need(v>=BigInt(cert.minimum_units),'failed interval '+i);if(minimum===null||v<minimum)minimum=v;
 }
 for(const [key,p]of [['certificate_sha256',certificate],['executable_sha256',exe],['reference_sha256',reference],['launcher_sha256',__filename]])need(hash(p)===bindings[key],'file changed during run');
 const budget=BigInt(cert.budget_units),surplus=17n*minimum-budget;need(surplus>0n,'no strict exclusion');
 const result={status:'PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION',target:cert.normalized_target,intervals:N,budget_units:String(budget),minimum_units:String(minimum),surplus:String(surplus),...bindings,processes,seconds:(Date.now()-start)/1000,verified_utc:new Date().toISOString()};
 fs.writeFileSync(path.join(out,'THEOREM.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
}
main().catch(e=>{console.error(e.stack);process.exitCode=1});
