// Independent exact wall minimum checker. Unlike the C++ site-mask sweep,
// each resource is evaluated on its own local one-dimensional arrangement,
// then its before/at/after charge transitions are added to a scalar sweep.
'use strict';
const fs=require('fs'),crypto=require('crypto');
const [mp,jp,cppp,outp]=process.argv.slice(2);
const need=(x,m)=>{if(!x)throw Error(m)};need(mp&&jp&&cppp&&outp&&!fs.existsSync(outp),'model jobs cpp-results fresh-output');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');const raw=fs.readFileSync(mp),jr=fs.readFileSync(jp),cr=fs.readFileSync(cppp),d=JSON.parse(raw),jobs=JSON.parse(jr),cpp=JSON.parse(cr);
const abs=x=>x<0n?-x:x;const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a};
function q(a,b=1n){a=BigInt(a);b=BigInt(b);need(b!==0n,'zero denominator');if(b<0n){a=-a;b=-b}const g=gcd(a,b);return[a/g,b/g]}
function parse(s){need(typeof s==='string'&&/^-?\d+(\/-?\d+)?$/.test(s),'rational string');return q(...s.split('/'))}
const add=(a,b)=>q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]),mul=(a,b)=>q(a[0]*b[0],a[1]*b[1]),div=(a,b)=>q(a[0]*b[1],a[1]*b[0]);
const cmp=(a,b)=>{const x=a[0]*b[1]-b[0]*a[1];return x<0n?-1:x>0n?1:0},str=a=>a.join('/'),min=(a,b)=>cmp(a,b)<0?a:b,max=(a,b)=>cmp(a,b)>0?a:b;
const integer=x=>{need(Number.isSafeInteger(x),'unsafe model integer');return BigInt(x)};
const L=parse(d.L),D=integer(d.coordinate_denominator),LD=div(mul(L,q(D)),q(1));need(LD[1]===1n,'grid');const points=[],pw=[];
for(const row of d.point_orbits){const [x,y,w]=row.map(integer),o=new Map();need(w>=0n,'point weight');for(let sw=0;sw<2;sw++)for(let fx=0;fx<2;fx++)for(let fy=0;fy<2;fy++){let a=sw?y:x,b=sw?x:y;if(fx)a=LD[0]-a;if(fy)b=LD[0]-b;o.set(a+','+b,[a,b])}const s=[...o.values()].sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:a[1]<b[1]?-1:a[1]>b[1]?1:0);points.push(...s);pw.push(...s.map(()=>w))}
need(new Set(points.map(x=>x.join(','))).size===points.length,'duplicate physical point');let budget=pw.reduce((a,b)=>a+b,0n);const resources=[];
for(let i=0;i<points.length;i++)if(pw[i]>0n)resources.push({ids:[i],co:[1],k:1,win:[],w:pw[i]});
for(const g of d.threshold_orbits){const n=g.sets[0].length,co=g.coefficients||Array(n).fill(1),win=g.winning_masks||[],w=integer(g.weight);need(n>=1&&n<=12&&co.length===n&&co.every(x=>Number.isSafeInteger(x)&&x>0)&&Number.isSafeInteger(g.threshold)&&g.threshold>0&&w>=0n,'rule');need(win.every(a=>Number.isSafeInteger(a)&&a>0&&a<(1<<n)&&win.every(b=>(a&b)!==0)),'intersecting rule');const cap=win.length?1:Math.floor(co.reduce((a,b)=>a+b,0)/g.threshold);budget+=BigInt(cap*g.sets.length)*w;for(const ids of g.sets){need(ids.length===n&&new Set(ids).size===n&&ids.every(i=>Number.isSafeInteger(i)&&i>=0&&i<points.length),'support');if(w>0n)resources.push({ids,co,k:g.threshold,win,w})}}
need(budget===BigInt(d.budget_units),'budget');need(cpp.model_sha256===hash(raw)&&cpp.rows.length===jobs.length,'C++ model/jobs');
const results=[];
for(let ji=0;ji<jobs.length;ji++){
 const target=parse(jobs[ji].target),P=div(L,target),a=parse(jobs[ji].a),b=parse(jobs[ji].b),W=parse(jobs[ji].width);need(cmp(q(0),a)<=0&&cmp(a,b)<0&&cmp(b,q(207107,500000))<=0&&cmp(q(0),W)<=0,'strip parameters');
 const t=min(div(add(a,b),q(2)),q(414213,1000000));function trig(u){return[q(u[1]*u[1]-u[0]*u[0],u[1]*u[1]+u[0]*u[0]),q(2n*u[0]*u[1],u[1]*u[1]+u[0]*u[0])]};const ca=trig(a),cb=trig(b),ct=trig(t);let rlo=div(mul(P,min(add(...ca),add(...cb))),q(2));let rhi=div(mul(P,max(add(...ca),add(...cb))),q(2));if(cmp(b,q(414213,1000000))>0){need(1414214n*1414214n>2n*1000000n*1000000n,'sqrt bound');rhi=mul(P,q(707107,1000000))}
 const grid=1000000000000n;rlo=q(rlo[0]*grid/rlo[1],grid);rhi=q((rhi[0]*grid+rhi[1]-1n)/rhi[1],grid);
 let H=q(0);for(const z of [ca,cb]){const dot=add(mul(ct[0],z[0]),mul(ct[1],z[1])),cross=sub(mul(ct[0],z[1]),mul(ct[1],z[0])),cr=q(abs(cross[0]),cross[1]);need(cmp(q(0),dot)<0&&cmp(cr,dot)<=0,'angle support bound');H=max(H,add(dot,cr))};
 const dy=div(add(sub(rhi,rlo),W),q(2)),y=div(add(add(rlo,rhi),W),q(2)),cap=min(div(sub(P,mul(q(2),dy)),H),div(mul(q(2),rlo),add(...ct))),A=q(cap[0]*grid/cap[1]-1n,grid),strict=sub(sub(P,mul(A,H)),mul(q(2),dy));need(cmp(A,q(0))>0&&cmp(strict,q(0))>0,'strict shifted-core containment');const left=rlo,right=sub(L,rlo),radius=div(mul(A,add(...ct)),q(2));need(cmp(radius,left)<=0&&cmp(right,sub(L,radius))<=0&&cmp(radius,y)<=0&&cmp(y,sub(L,radius))<=0&&cmp(left,right)<0,'core line legality');
 const C=q(t[1]*t[1]-t[0]*t[0]),S=q(2n*t[0]*t[1]),T=q(t[1]*t[1]+t[0]*t[0]),h=div(mul(A,T),q(2));
 const ev=new Map();function event(x){const k=str(x);if(!ev.has(k))ev.set(k,{x,starts:[],ends:[],at:0n,after:0n});return ev.get(k)}event(left);event(right);
 const intervals=points.map(([px0,py0],id)=>{const px=q(px0,D),py=q(py0,D),ku=add(mul(C,px),mul(S,sub(py,y))),kv=add(sub(q(0),mul(S,px)),mul(C,sub(py,y)));let lo=div(sub(ku,h),C),hi=div(add(ku,h),C);
  if(S[0]===0n){if(cmp(q(abs(kv[0]),kv[1]),h)>=0)return null}else{lo=max(lo,div(sub(sub(q(0),h),kv),S));hi=min(hi,div(sub(h,kv),S))}
  if(cmp(lo,hi)>=0||cmp(hi,left)<=0||cmp(right,lo)<=0)return null;
  if(cmp(left,lo)<=0&&cmp(lo,right)<0)event(lo).starts.push(id);if(cmp(left,hi)<0&&cmp(hi,right)<=0)event(hi).ends.push(id);return[lo,hi];});
 const events=[...ev.values()].sort((a,b)=>cmp(a.x,b.x));let text='';for(const e of events)text+=str(e.x)+':'+e.ends.map(i=>'-'+i+',').join('')+e.starts.map(i=>'+'+i+',').join('')+'\n';
 function fires(g,x){let mask=0,s=0;for(let j=0;j<g.ids.length;j++){const ab=intervals[g.ids[j]];if(ab&&cmp(ab[0],x)<0&&cmp(x,ab[1])<0){mask|=1<<j;s+=g.co[j]}}return g.win.length?g.win.some(w=>(mask&w)===w):s>=g.k}
 for(const g of resources){const keys=new Map([[str(left),left],[str(right),right]]);for(const id of g.ids){const ab=intervals[id];if(ab)for(const x of ab)if(cmp(left,x)<=0&&cmp(x,right)<=0)keys.set(str(x),x)}const xs=[...keys.values()].sort(cmp);let prev=false;
  for(let k=0;k<xs.length;k++){const x=xs[k],at=fires(g,x),after=k+1<xs.length?fires(g,div(add(x,xs[k+1]),q(2))):at;const e=event(x);e.at+=(BigInt(at)-BigInt(prev))*g.w;e.after+=(BigInt(after)-BigInt(at))*g.w;prev=after;}}
 let fee=0n,minimum=null,minX=null,minKind=null,states=0;for(let k=0;k<events.length;k++){const e=events[k];fee+=e.at;states++;if(minimum===null||fee<minimum){minimum=fee;minX=e.x;minKind='boundary'}fee+=e.after;if(k+1<events.length){states++;if(fee<minimum){minimum=fee;minX=div(add(e.x,events[k+1].x),q(2));minKind='open_cell'}}}
 const c=cpp.rows[ji];need(c.mode==='continuous_angle_wall_strip_shifted_core'&&str(P)===c.parent_A&&str(a)===c.a&&str(b)===c.b&&str(W)===c.width&&str(dy)===c.dy_bound&&str(H)===c.h_bound&&str(strict)===c.strict_margin,'shifted-core premise binding');need(str(t)===c.t&&str(A)===c.A&&str(left)===c.left&&str(right)===c.right&&str(y)===c.wall_y,'family identity');need(hash(text)===c.event_sha256&&events.length===c.events&&states===c.states,'partition disagrees');need(minimum===BigInt(c.minimum_open_fee),'minimum disagrees');
 results.push({mode:'continuous_angle_wall_strip_shifted_core',a:str(a),b:str(b),width:str(W),parent_A:str(P),strict_margin:str(strict),family:ji,target:str(target),t:str(t),A:str(A),wall_y:str(y),minimum_open_fee:String(minimum),surplus:String(17n*minimum-budget),events:events.length,states,event_sha256:hash(text),witness:{cx:str(minX),cy:str(y),kind:minKind}});console.log('INDEPENDENT_STRIP',ji,String(minimum),states);
}
fs.writeFileSync(outp,JSON.stringify({status:'PASS_PAIRED_LOCAL_CONTINUOUS_ANGLE_WALL_STRIP_MINIMA',scope:'Each listed angle interval and its full wall-adjacent strip of parent centres; local coverage only, not an all-domain exclusion',model_sha256:hash(raw),jobs_sha256:hash(jr),cpp_sha256:hash(cr),checker_sha256:hash(fs.readFileSync(__filename)),budget_units:String(budget),rows:results},null,2)+'\n');
