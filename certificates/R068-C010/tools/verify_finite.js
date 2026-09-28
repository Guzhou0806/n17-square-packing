// Independent JavaScript BigInt finite-pose / fixed-dictionary dual checker.
// No numerical LP and no inference of all-angle coverage.
'use strict';
const fs=require('fs'),crypto=require('crypto'),path=require('path');
const [,,cp,sp,op]=process.argv;
function need(b,s){if(!b)throw Error(s)}
need(cp&&sp&&op&&!fs.existsSync(op),'usage: verify_finite certificate spec output (fresh)');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const raw=fs.readFileSync(cp),specraw=fs.readFileSync(sp),d=JSON.parse(raw),spec=JSON.parse(specraw);
need(sha(raw)===spec.certificate_sha256,'certificate identity');
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a;}
function Q(n,d=1n){n=BigInt(n);d=BigInt(d);need(d!==0n,'zero denominator');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function parse(x){need(typeof x==='string','rational string required');const p=x.split('/');need(p.length<=2&&p.every(z=>/^-?[0-9]+$/.test(z)),'rational syntax');return Q(p[0],p[1]||'1');}
const add=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const sub=(a,b)=>Q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]);
const le=(a,b)=>a[0]*b[1]<=b[0]*a[1];
const rationalString=q=>q[0]+'/'+q[1];
const integer=x=>{need(Number.isSafeInteger(x),'unsafe JSON integer');return BigInt(x);};
const L=parse(d.L),A=div(L,parse(spec.target)),D=integer(d.coordinate_denominator);
need(A[0]>0n&&le(A,L),'parent side');need(L[0]*D%L[1]===0n,'coordinate scale');const LD=L[0]*D/L[1];
const points=[],pw=[];
for(const row of d.point_orbits){const [x,y,w]=row.map(integer),orbit=new Map();for(const swap of [0,1])for(const fx of [0,1])for(const fy of [0,1]){let a=swap?y:x,b=swap?x:y;if(fx)a=LD-a;if(fy)b=LD-b;orbit.set(a+','+b,[a,b]);}
 const list=[...orbit.values()].sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:a[1]<b[1]?-1:a[1]>b[1]?1:0);points.push(...list);pw.push(...list.map(()=>w));}
need(new Set(points.map(p=>p.join(','))).size===points.length,'duplicate physical sites');
const columns=d.threshold_orbits.map(g=>{
 const n=g.sets[0].length,co=g.coefficients||Array(n).fill(1),winning=g.winning_masks||[];
 need(n<=12&&n>=1&&g.sets.length<=255,'arity or image count');need(co.every(x=>Number.isSafeInteger(x)&&x>0),'coefficient');
 const cap=winning.length?1:Math.floor(co.reduce((a,b)=>a+b,0)/g.threshold);
 return {sets:g.sets,co,winning,k:g.threshold,w:integer(g.weight),cost:BigInt(g.sets.length*cap)};
});
let M=pw.reduce((a,b)=>a+b,0n);for(const g of columns)M+=g.w*g.cost;need(M===integer(d.budget_units),'budget');
const rows=[],matrix=Buffer.alloc(spec.poses.length*columns.length);let offset=0;
for(let pi=0;pi<spec.poses.length;pi++){
 const pose=spec.poses[pi],t=parse(pose.t),x=parse(pose.cx),y=parse(pose.cy);need(le(Q(0),t)&&le(t,Q(1)),'pose angle');
 const C=t[1]*t[1]-t[0]*t[0],S=2n*t[0]*t[1],T=t[1]*t[1]+t[0]*t[0];
 const r=mul(A,Q(abs(C)+abs(S),2n*T));need(le(r,x)&&le(x,sub(L,r))&&le(r,y)&&le(y,sub(L,r)),'illegal parent');
 const hit=[],closed=[],boundary=[];let fee=0n,cf=0n;
 // Cross-multiply the exact rational projections; no rounded coordinates.
 const den=T*D*x[1]*y[1],rhs=A[0]*den,lhsFactor=2n*A[1];
 for(let i=0;i<points.length;i++){
  const dx=(points[i][0]*x[1]-x[0]*D)*y[1],dy=(points[i][1]*y[1]-y[0]*D)*x[1];
  const u=abs(C*dx+S*dy)*lhsFactor,v=abs(C*dy-S*dx)*lhsFactor;
  hit[i]=u<rhs&&v<rhs;closed[i]=u<=rhs&&v<=rhs;
  if(hit[i])fee+=pw[i];if(closed[i])cf+=pw[i];if(closed[i]&&!hit[i])boundary.push(i);
 }
 for(const g of columns){let count=0,closedCount=0;for(const ids of g.sets){let mask=0,cmask=0,sum=0,csum=0;for(let j=0;j<ids.length;j++){if(hit[ids[j]]){mask|=1<<j;sum+=g.co[j];}if(closed[ids[j]]){cmask|=1<<j;csum+=g.co[j];}}
  if(g.winning.length?g.winning.some(w=>(mask&w)===w):sum>=g.k)count++;
  if(g.winning.length?g.winning.some(w=>(cmask&w)===w):csum>=g.k)closedCount++;
 }
 matrix[offset++]=count;fee+=g.w*BigInt(count);cf+=g.w*BigInt(closedCount);}
 if(spec.expected_open_fees)need(fee===BigInt(spec.expected_open_fees[pi]),'open fee mismatch');
 rows.push({pose_index:pi,open_fee:String(fee),closed_fee:String(cf),open_surplus:String(17n*fee-M),boundary_sites:boundary});
}
let matrix_agrees=null;
if(spec.cpp_matrix){const mr=fs.readFileSync(path.resolve(path.dirname(sp),spec.cpp_matrix.path));need(sha(mr)===spec.cpp_matrix.sha256,'matrix identity');need(mr.equals(matrix),'C++/BigInt finite capture matrix mismatch');matrix_agrees=true;}
let dual=null;
if(spec.dual_weights){need(spec.dual_weights.length===spec.poses.length,'dual size');need(pw.every(w=>w===0n),'direct point columns not included');const yy=spec.dual_weights.map(parse);need(yy.every(y=>y[0]>=0n),'negative dual weight');let Y=yy.reduce(add,Q(0));const column_lhs=[];for(let j=0;j<columns.length;j++){let s=Q(0);for(let i=0;i<yy.length;i++)s=add(s,mul(yy[i],Q(matrix[i*columns.length+j])));need(le(s,Q(columns[j].cost)),'dual column violated');column_lhs.push(rationalString(s));}need(le(Q(17),Y),'dual total below 17');dual={total:rationalString(Y),columns_checked:columns.length,column_lhs,status:'PASS_EXACT_FINITE_FIXED_DICTIONARY_OBSTRUCTION'};}
if(spec.require_counterexample)need(rows.some(r=>BigInt(r.open_surplus)<=0n),'no actual fixed-charge counterexample');
const result={status:dual?'PASS_EXACT_FINITE_FIXED_DICTIONARY_OBSTRUCTION':spec.require_counterexample?'PASS_EXACT_ACTUAL_PARENT_COUNTEREXAMPLE':'PASS_EXACT_FINITE_POSE_COMPARISON',scope:'Finite exact legal parents; not a nonpacking theorem',certificate_sha256:sha(raw),spec_sha256:sha(specraw),target:spec.target,A:rationalString(A),budget_units:String(M),physical_sites:points.length,column_count:columns.length,rows,matrix_sha256:sha(matrix),cpp_matrix_agrees:matrix_agrees,dual};
fs.writeFileSync(op,JSON.stringify(result,null,2));console.log(JSON.stringify({...result,rows:undefined,dual:dual?{status:dual.status,total:dual.total,columns_checked:dual.columns_checked}:null}));
