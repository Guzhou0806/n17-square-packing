'use strict';
// Independent checker: quadratic positivity for full angle intervals,
// and distance-to-polygon (not local-coordinate clipping) for anchor overlap.
const fs=require('fs');const {Q,q}=require('../../followup_c021/src/bigq.js');const {strictParse}=require('./strict_json.js');
const P=Q.parse,lt=(a,b)=>a.cmp(b)<0,le=(a,b)=>a.cmp(b)<=0,eq=(a,b)=>a.cmp(b)===0;
const need=(v,s)=>{if(!v)throw Error(s);},min=(a,b)=>lt(a,b)?a:b,max=(a,b)=>lt(a,b)?b:a;
const add=(a,b)=>a.map((x,i)=>x.add(b[i])),sub=(a,b)=>a.map((x,i)=>x.sub(b[i])),mul=(a,b)=>b.map(x=>x.mul(a));
const dot=(a,b)=>a[0].mul(b[0]).add(a[1].mul(b[1])),cross=(a,b)=>a[0].mul(b[1]).sub(a[1].mul(b[0]));
function frame(t){const d=q(1).add(t.mul(t));return[q(1).sub(t.mul(t)).div(d),t.mul(2).div(d)];}
function verts(c,t,A){const u=frame(t),v=[u[1].neg(),u[0]];return[[-1,-1],[1,-1],[1,1],[-1,1]].map(([a,b])=>add(c,mul(A.div(2),add(mul(q(a),u),mul(q(b),v)))));}
function strictInside(poly,p){return poly.every((a,i)=>lt(q(0),cross(sub(poly[(i+1)%4],a),sub(p,a))));}
function readSpec(j){
 need(j.schema==='n17.c028.second-anchor-atlas.v2','SCHEMA');need(j.parent_count===17&&j.grid_order===4,'GRID_DIMENSION');
 const L=P(j.L),T=P(j.cap),nt=P(j.near_t),eps=P(j.epsilon),depth=j.max_depth;
 need(lt(q(0),L)&&lt(q(4),T)&&lt(T,q(5))&&lt(q(0),nt)&&lt(nt,q(2).div(5)),'PARAMETER_DOMAIN');need(lt(q(0),eps)&&lt(eps,q(1).div(100)),'ENDPOINT_STRICTNESS');need(Number.isInteger(depth)&&depth>=0&&depth<=21,'DEPTH_RANGE');
 const A=L.div(T),half=A.div(2),alpha=q(1).sub(eps),gap=T.sub(alpha.mul(2)).div(3),uv=frame(nt);
 need(lt(q(0),gap)&&lt(gap.mul(uv[0].add(uv[1])),q(1)),'GRID_GAP');const grid=[];
 for(let y=0;y<4;y++)for(let x=0;x<4;x++)grid.push([A.mul(alpha.add(gap.mul(x))),A.mul(alpha.add(gap.mul(y)))]);
 const a=j.anchor,t=P(a.t),et=P(a.et);let C=[P(a.cx),P(a.cy)],ex=P(a.ex),ey=P(a.ey);need(lt(q(0),ex)&&lt(q(0),ey)&&lt(q(0),et),'POSITIVE_ANCHOR_WIDTH');need(le(q(0),t.sub(et))&&le(t.add(et),q(1)),'ANCHOR_ANGLE_RANGE');
 const rawPoly=verts(C,t,A.mul(q(1).add(et.mul(2))).add(ex.add(ey).mul(2)));
 const ua=frame(t.sub(et)),ub=frame(t.add(et)),ar=half.mul(min(ua[0].add(ua[1]),ub[0].add(ub[1]))),ax0=max(C[0].sub(ex),ar),ax1=min(C[0].add(ex),L.sub(ar)),ay0=max(C[1].sub(ey),ar),ay1=min(C[1].add(ey),L.sub(ar));
 need(le(ax0,ax1)&&le(ay0,ay1),'ANCHOR_WALL_BOX_EMPTY');C=[ax0.add(ax1).div(2),ay0.add(ay1).div(2)];ex=ax1.sub(ax0).div(2);ey=ay1.sub(ay0).div(2);
 const core=A.sub(ex.add(ey).mul(2)).div(q(1).add(et.mul(2)));need(lt(q(0),core),'ANCHOR_CORE');const k=j.anchor_point_index;need(Number.isInteger(k)&&k>=0&&k<16,'ANCHOR_POINT_INDEX');const poly=verts(C,t,core);need(strictInside(poly,grid[k]),'ANCHOR_GRID_CAPTURE');for(let z=0;z<16;z++)if(z!==k)need(rawPoly.some((a,i)=>lt(cross(sub(rawPoly[(i+1)%4],a),sub(grid[z],a)),q(0))),'ANCHOR_MULTIPLE_GRID_POSSIBLE');
 return{L,T,A,half,core,grid,depth,poly,anchor:{C,t,ex,ey,et},root:[[half,L.sub(half)],[half,L.sub(half)],[nt,q(1).sub(nt).div(q(1).add(nt))]]};
}
function quadraticPositive(a,b,c,lo,hi){const f=t=>a.mul(t).add(b).mul(t).add(c);if(!lt(q(0),f(lo))||!lt(q(0),f(hi)))return false;if(lt(q(0),a)){const t=b.neg().div(a.mul(2));if(lt(lo,t)&&lt(t,hi)&&!lt(q(0),f(t)))return false;}return true;}
function captured(s,b,k){if(k<0||k>=16)return false;const p=s.grid[k],r=s.half,lo=b[2][0],hi=b[2][1];for(let i=0;i<2;i++)for(let j=0;j<2;j++){
 const dx=p[0].sub(b[0][i]),dy=p[1].sub(b[1][j]);
 for(const[a,b,c]of[[r.add(dx),dy.mul(-2),r.sub(dx)],[r.sub(dx),dy.mul(2),r.add(dx)],[r.add(dy),dx.mul(2),r.sub(dy)],[r.sub(dy),dx.mul(-2),r.add(dy)]])if(!quadraticPositive(a,b,c,lo,hi))return false;
 }return true;}
function wall(s,b,k){const p=frame(b[2][0]),v=frame(b[2][1]),r=s.half.mul(min(p[0].add(p[1]),v[0].add(v[1])));return k===0?lt(b[0][1],r):k===1?lt(s.L.sub(r),b[0][0]):k===2?lt(b[1][1],r):k===3?lt(s.L.sub(r),b[1][0]):false;}
function cornerCapture(s,b,k){if(k<0||k>3)return false;const edge=s.grid[0][0];return (k&1?le(s.L.sub(edge),b[0][0]):le(b[0][1],edge))&&(k&2?le(s.L.sub(edge),b[1][0]):le(b[1][1],edge));}
function polygonDistanceSquared(poly,p){
 if(poly.every((a,i)=>le(q(0),cross(sub(poly[(i+1)%4],a),sub(p,a)))))return q(0);
 let best=null;for(let i=0;i<4;i++){const a=poly[i],edge=sub(poly[(i+1)%4],a),d=sub(p,a),t=max(q(0),min(q(1),dot(d,edge).div(dot(edge,edge)))),e=sub(d,mul(t,edge)),dist=dot(e,e);best=best===null?dist:min(best,dist);}return best;
}
function overlaps(s,b){for(let i=0;i<2;i++)for(let j=0;j<2;j++)if(!lt(polygonDistanceSquared(s.poly,[b[0][i],b[1][j]]),s.half.mul(s.half)))return false;return true;}
function strictOverlap(a,b){for(const p of[a,b])for(let k=0;k<4;k++){const edge=sub(p[(k+1)%4],p[k]),n=[edge[1].neg(),edge[0]],ra=a.map(x=>dot(n,x)),rb=b.map(x=>dot(n,x));if(le(ra.reduce(max),rb.reduce(min))||le(rb.reduce(max),ra.reduce(min)))return false;}return true;}
function kernelOverlap(s,b){const ex=b[0][1].sub(b[0][0]).div(2),ey=b[1][1].sub(b[1][0]).div(2),et=b[2][1].sub(b[2][0]).div(2),side=s.A.sub(ex.add(ey).mul(2)).div(q(1).add(et.mul(2)));if(le(side,q(0)))return false;const C=b.slice(0,2).map(x=>x[0].add(x[1]).div(2)),t=b[2][0].add(b[2][1]).div(2);return strictOverlap(verts(C,t,side),s.poly);}
function projectionsBelow(dx0,dx1,dy0,dy1,t0,t1,r){for(const dx of[dx0,dx1])for(const dy of[dy0,dy1])for(const[a,b,c]of[[r.add(dx),dy.mul(-2),r.sub(dx)],[r.sub(dx),dy.mul(2),r.add(dx)],[r.add(dy),dx.mul(2),r.sub(dy)],[r.sub(dy),dx.mul(-2),r.add(dy)]])if(!quadraticPositive(a,b,c,t0,t1))return false;return true;}
function jointOverlap(s,b){const a=s.anchor,a0=a.t.sub(a.et),a1=a.t.add(a.et);let rel=q(1);if(lt(b[2][1],a0)||lt(a1,b[2][0])){const x0=frame(a0),x1=frame(a1),y0=frame(b[2][0]),y1=frame(b[2][1]);rel=min(dot(x1,y0).add(cross(x1,y0).abs()),dot(x0,y1).add(cross(x0,y1).abs()));}const bound=s.A.mul(q(1).add(rel)).div(2),dx0=b[0][0].sub(a.C[0]).sub(a.ex),dx1=b[0][1].sub(a.C[0]).add(a.ex),dy0=b[1][0].sub(a.C[1]).sub(a.ey),dy1=b[1][1].sub(a.C[1]).add(a.ey);return projectionsBelow(dx0,dx1,dy0,dy1,a0,a1,bound)&&projectionsBelow(dx0,dx1,dy0,dy1,b[2][0],b[2][1],bound);}
function main(j,text){const s=readSpec(j),tokens=text.trim().split(/\s+/);let at=0;need(tokens[at++]==='C028_ATLAS_V2','TREE_HEADER');const counts={split:0,wall:0,grid_capture:0,corner_capture:0,anchor_overlap:0,kernel_overlap:0,joint_overlap:0,unresolved:0},vol=[0,0,0,0,0,0,0],pc=Array(16).fill(0),frontier=[];let nodes=0;
 function visit(b,depth,path){need(depth<=s.depth,'TREE_TOO_DEEP');need(++nodes<=5000000,'TREE_SIZE');need(at<tokens.length,'TREE_TRUNCATED');const op=tokens[at++];let k=-1;if(['S','W','P','C'].includes(op)){need(at<tokens.length&&/^\d+$/.test(tokens[at]),'TREE_MISSING_INDEX');k=Number(tokens[at++]);need(Number.isSafeInteger(k),'TREE_MISSING_INDEX');}
 if(op==='S'){need(k>=0&&k<3&&depth<s.depth,'INVALID_SPLIT');need(k===depth%3,'SPLIT_SCHEDULE');counts.split++;const m=b[k][0].add(b[k][1]).div(2),a=b.map(x=>x.slice()),c=b.map(x=>x.slice());a[k][1]=m;c[k][0]=m;visit(a,depth+1,path+'0');visit(c,depth+1,path+'1');return;}
 const w=2**(s.depth-depth);if(op==='W'){need(k>=0&&k<4&&wall(s,b,k),'UNPROVED_WALL_LEAF');counts.wall++;vol[0]+=w;}
 else if(op==='P'){need(k>=0&&k<16&&captured(s,b,k),'UNPROVED_POINT_LEAF');counts.grid_capture++;pc[k]++;vol[1]+=w;}
 else if(op==='C'){need(k>=0&&k<4&&cornerCapture(s,b,k),'UNPROVED_CORNER_LEAF');counts.corner_capture++;vol[2]+=w;}
 else if(op==='A'){need(overlaps(s,b),'UNPROVED_ANCHOR_LEAF');counts.anchor_overlap++;vol[3]+=w;}
 else if(op==='K'){need(kernelOverlap(s,b),'UNPROVED_KERNEL_LEAF');counts.kernel_overlap++;vol[4]+=w;}
 else if(op==='J'){need(jointOverlap(s,b),'UNPROVED_JOINT_LEAF');counts.joint_overlap++;vol[5]+=w;}
 else if(op==='U'){need(depth===s.depth,'PREMATURE_FRONTIER');counts.unresolved++;frontier.push(path);vol[6]+=w;}
 else throw Error('UNKNOWN_LEAF_OPCODE');
 }
 visit(s.root,0,'');need(at===tokens.length,'TREE_EXTRA_TOKENS');need(vol.reduce((a,b)=>a+b,0)===2**s.depth,'INCOMPLETE_ROOT_VOLUME');return{schema:'n17.c028.atlas-result.v2',scope:'complete outer cover of a forced grid-avoiding second parent; unresolved leaves are not feasible packings',new_lower_bound:false,cap:String(s.T),parent_side:String(s.A),anchor_core_side:String(s.core),anchor_grid_capture_count:1,max_depth:s.depth,root:s.root.map(x=>x.map(String)),nodes,counts,dyadic_volume_units:vol,volume_denominator:2**s.depth,point_leaf_counts:pc,frontier_paths:frontier};
}
if(require.main===module)try{need(process.argv.length===5,'USAGE_INPUT_TREE_FRESH_OUTPUT');const[ip,tp,op]=process.argv.slice(2);need(!fs.existsSync(op),'FRESH_OUTPUT_REQUIRED');const out=main(strictParse(fs.readFileSync(ip,'utf8')),fs.readFileSync(tp,'utf8'));fs.writeFileSync(op,JSON.stringify(out)+'\n',{flag:'wx'});console.log('PASS_COMPLETE_OUTER_ATLAS nodes='+out.nodes+' unresolved='+out.counts.unresolved);}catch(e){console.error('REJECT '+e.message);process.exit(1);}
module.exports={main,readSpec,captured,wall,overlaps,quadraticPositive,polygonDistanceSquared,projectionsBelow,jointOverlap,kernelOverlap};
