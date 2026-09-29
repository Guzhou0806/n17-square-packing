'use strict';
// Independent BigInt arithmetic and finite capture, adapted from the retained
// finite checker. Convex-hull intersection uses triangle/segment enumeration,
// not the C++ monotone-chain hull algorithm.
const fs=require('fs'),crypto=require('crypto');
const need=(b,m)=>{if(!b)throw Error(m);};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a;}
function Q(n,d=1n){n=BigInt(n);d=BigInt(d);need(d!==0n,'zero denominator');if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return[n/g,d/g];}
function parse(s){need(typeof s==='string'&&/^-?\d+(\/[1-9]\d*)?$/.test(s),'rational syntax');return Q(...s.split('/'));}
const add=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const sub=(a,b)=>Q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]);
const le=(a,b)=>a[0]*b[1]<=b[0]*a[1];
const str=a=>a[0]+'/'+a[1];
const int=x=>{need(Number.isSafeInteger(x),'unsafe integer');return BigInt(x);};
const cross=(o,a,b)=>(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0]);
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const between=(a,b,x)=>a<=b?a<=x&&x<=b:b<=x&&x<=a;
const on=(a,b,p)=>cross(a,b,p)===0n&&between(a[0],b[0],p[0])&&between(a[1],b[1],p[1]);
function seg(a,b,c,d){let u=cross(a,b,c),v=cross(a,b,d),w=cross(c,d,a),z=cross(c,d,b);return u===0n&&on(a,b,c)||v===0n&&on(a,b,d)||w===0n&&on(c,d,a)||z===0n&&on(c,d,b)||u*v<0n&&w*z<0n;}
function inConv(p,a){
 if(a.some(q=>eq(p,q)))return true;
 for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)if(on(a[i],a[j],p))return true;
 for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)for(let k=j+1;k<a.length;k++){
  const D=cross(a[i],a[j],a[k]);if(!D)continue;
  const u=cross(a[i],a[j],p),v=cross(a[j],a[k],p),w=cross(a[k],a[i],p);
  if(D>0n?u>=0n&&v>=0n&&w>=0n:u<=0n&&v<=0n&&w<=0n)return true;
 }return false;
}
function meets(a,b){need(a.length&&b.length,'empty convex hull');if(a.some(p=>inConv(p,b))||b.some(p=>inConv(p,a)))return true;for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)for(let k=0;k<b.length;k++)for(let l=k+1;l<b.length;l++)if(seg(a[i],a[j],b[k],b[l]))return true;return false;}
function fires(g,v){if(g.rules.length)return g.rules.some(w=>(v&w)===w);let s=0;for(let j=0;j<g.co.length;j++)if(v&(1<<j))s+=g.co[j];return s>=g.k;}
function loadModel(p){let raw=fs.readFileSync(p),d=JSON.parse(raw),L=parse(d.L),D=int(d.coordinate_denominator);need(D>0n&&L[0]*D%L[1]===0n,'coordinate denominator');let LD=L[0]*D/L[1],pts=[],sizes=[],pw=[],weights=[],costs=[],groups=[];
 for(const row of d.point_orbits){need(row.length===3,'point arity');let[x,y,w]=row.map(int);need(x>=0n&&x<=LD&&y>=0n&&y<=LD&&w>=0n,'point range');let orb=new Map;for(let sw of[0,1])for(let fx of[0,1])for(let fy of[0,1]){let a=sw?y:x,b=sw?x:y;if(fx)a=LD-a;if(fy)b=LD-b;orb.set(a+','+b,[a,b]);}let ps=[...orb.values()].sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:a[1]<b[1]?-1:a[1]>b[1]?1:0);sizes.push(ps.length);pts.push(...ps);pw.push(...ps.map(()=>w));}
 need(new Set(pts.map(p=>p.join(','))).size===pts.length,'duplicate site');
 for(let g of d.threshold_orbits){let n=g.sets[0].length,co=g.coefficients||Array(n).fill(1),k=g.threshold,rules=g.winning_masks||[];need(n>0&&n<=12&&co.length===n&&co.every(x=>Number.isSafeInteger(x)&&x>0)&&Number.isSafeInteger(k)&&k>0,'rule range');need(rules.every(w=>Number.isSafeInteger(w)&&w>0&&w<(1<<n))&&new Set(rules).size===rules.length,'rule mask');need(rules.every(a=>rules.every(b=>(a&b)!==0)),'old disjoint masks');let cost=g.sets.length*(rules.length?1:Math.floor(co.reduce((a,b)=>a+b,0)/k));need(cost>0,'old capacity');let weight=int(g.weight);need(weight>=0n,'nonnegative weights');need(g.sets.every(ss=>ss.length===n&&new Set(ss).size===n&&ss.every(i=>Number.isInteger(i)&&i>=0&&i<pts.length)),'rule sites');groups.push(g.sets.map(ids=>({ids,co:[...co],k,rules:[...rules],weight})));weights.push(weight);costs.push(BigInt(cost));}
 for(let i=0;i<sizes.length;i++){weights.push(int(d.point_orbits[i][2]));costs.push(BigInt(sizes[i]));}let M=weights.reduce((s,w,i)=>s+w*costs[i],0n);need(M===int(d.budget_units),'budget identity');return {d,raw,sha:sha(raw),L,D,LD,pts,pw,sizes,groups,weights,costs,M};
}
const canonical=(g,tr)=>JSON.stringify(g.rules.map(w=>g.ids.filter((_,j)=>w&(1<<j)).map(i=>tr?tr[i]:i).sort((a,b)=>a-b)).sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b))));
function overlay(m,ov){need(ov.schema==='n17.convex_hull_rule_overlay.v1'&&ov.base_model_sha256===m.sha,'overlay model identity');let lookup=new Map(m.pts.map((p,i)=>[p.join(','),i])),trs=[];for(let sw of[0,1])for(let fx of[0,1])for(let fy of[0,1])trs.push(m.pts.map(p=>{let a=sw?p[1]:p[0],b=sw?p[0]:p[1];if(fx)a=m.LD-a;if(fy)b=m.LD-b;let i=lookup.get(a+','+b);need(i!==undefined,'D4 site');return i;}));let seen=new Set,stats={upgraded_orbits:0,upgraded_images:0,truth_states:0,strict_abstract_states:0,disjoint_geometric_pairs:0};
 for(const up of ov.upgrades){let oi=up.orbit;need(Number.isInteger(oi)&&oi>=0&&oi<m.groups.length&&!seen.has(oi),'duplicate/range orbit');seen.add(oi);let gg=m.groups[oi];need(up.winning_masks_by_image.length===gg.length,'image count');
  for(let im=0;im<gg.length;im++){let g=gg[im],old={...g,rules:[...g.rules]},n=g.ids.length,rr=up.winning_masks_by_image[im];need((old.rules.length?1:Math.floor(old.co.reduce((a,b)=>a+b,0)/old.k))===1,'capacity-one premise');need(rr.length>0&&new Set(rr).size===rr.length&&rr.every(v=>Number.isInteger(v)&&v>0&&v<(1<<n)),'new masks');g.rules=[...rr];
   for(let a=0;a<rr.length;a++)for(let b=a+1;b<rr.length;b++){need((rr[a]&rr[b])!==rr[a]&&(rr[a]&rr[b])!==rr[b],'minimal family');need(meets(g.ids.filter((_,j)=>rr[a]&(1<<j)).map(i=>m.pts[i]),g.ids.filter((_,j)=>rr[b]&(1<<j)).map(i=>m.pts[i])),'geometric hull disjoint');if(!(rr[a]&rr[b]))stats.disjoint_geometric_pairs++;}
   for(let v=0;v<(1<<n);v++){let a=fires(old,v),b=fires(g,v);need(!a||b,'loss of old winning pattern');stats.truth_states++;if(b&&!a)stats.strict_abstract_states++;}stats.upgraded_images++;
  }
  let original=gg.map(g=>canonical(g)).sort().join('|');for(let tr of trs)need(gg.map(g=>canonical(g,tr)).sort().join('|')===original,'D4 function multiset');stats.upgraded_orbits++;
 }
 let terms=m.pw.filter(w=>w!==0n).length,mass=m.pw.reduce((a,b)=>a+b,0n);
 for(let gg of m.groups)for(let g of gg){if(g.weight===0n)continue;let nn=1<<g.ids.length,a=Array.from({length:nn},(_,v)=>fires(g,v)?1:0);for(let j=0;j<g.ids.length;j++)for(let v=0;v<nn;v++)if(v&(1<<j))a[v]-=a[v^(1<<j)];for(let v=1;v<nn;v++)if(a[v]){terms++;mass+=abs(BigInt(a[v])*g.weight);}}
 need(mass<1n<<50n,'signed accumulator safety');stats.signed_terms=terms;return stats;
}
function captures(m,pose,A){let t=parse(pose.t),x=parse(pose.cx),y=parse(pose.cy);need(A[0]>0n&&le(Q(0),t)&&le(t,Q(1)),'parent/angle');const C=t[1]*t[1]-t[0]*t[0],S=2n*t[0]*t[1],T=t[1]*t[1]+t[0]*t[0],rad=mul(A,Q(abs(C)+abs(S),2n*T));need(le(rad,x)&&le(x,sub(m.L,rad))&&le(rad,y)&&le(y,sub(m.L,rad)),'illegal parent');let hit=[],closed=[];let lim=A[0]*T*m.D*x[1]*y[1],fac=2n*A[1];for(let p of m.pts){let dx=(p[0]*x[1]-x[0]*m.D)*y[1],dy=(p[1]*y[1]-y[0]*m.D)*x[1],u=abs(C*dx+S*dy)*fac,v=abs(C*dy-S*dx)*fac;hit.push(u<lim&&v<lim);closed.push(u<=lim&&v<=lim);}return{hit,closed};}
function counts(m,hit){let row=[];for(let gg of m.groups){let v=0;for(let g of gg){let mask=0;for(let j=0;j<g.ids.length;j++)if(hit[g.ids[j]])mask|=1<<j;if(fires(g,mask))v++;}row.push(v);}let i=0;for(let sz of m.sizes){let s=0;for(let j=0;j<sz;j++)if(hit[i++])s++;row.push(s);}return row;}
const fee=(m,row)=>row.reduce((s,c,i)=>s+BigInt(c)*m.weights[i],0n);
module.exports={fs,need,sha,abs,gcd,Q,parse,add,sub,mul,div,le,str,int,cross,on,seg,inConv,meets,fires,loadModel,overlay,captures,counts,fee};
