'use strict';
// Independent vertex-based check; inherited BigInt arithmetic only.
const fs=require('fs');
const {Q,q}=require('../../followup_c021/src/bigq.js');
const P=Q.parse,eq=(a,b)=>a.cmp(b)===0,lt=(a,b)=>a.cmp(b)<0,le=(a,b)=>a.cmp(b)<=0;
const need=(b,s)=>{if(!b)throw Error(s);},mn=(a,b)=>lt(a,b)?a:b,mx=(a,b)=>lt(a,b)?b:a;
const add=(a,b)=>a.map((x,i)=>x.add(b[i])),sub=(a,b)=>a.map((x,i)=>x.sub(b[i])),scale=(c,a)=>a.map(x=>x.mul(c));
const cr=(a,b)=>a[0].mul(b[1]).sub(a[1].mul(b[0]));
function frame(t){const d=q(1).add(t.mul(t));return[q(1).sub(t.mul(t)).div(d),t.mul(2).div(d)];}
function verts(c,t,A){const u=frame(t),v=[u[1].neg(),u[0]];return [[-1,-1],[1,-1],[1,1],[-1,1]].map(([a,b])=>add(c,scale(A.div(2),add(scale(q(a),u),scale(q(b),v)))));}
function margin(poly,p,A){const orient=cr(sub(poly[1],poly[0]),sub(poly[2],poly[1])).cmp(0);need(orient!==0,'DEGENERATE_CORE');return poly.map((a,i)=>cr(sub(poly[(i+1)%4],a),sub(p,a)).mul(orient).div(A)).reduce(mn);}
function main(j){
 need(j.schema==='n17.c028.stabbing.v1','SCHEMA');need(j.grid_order===4&&j.parent_count===17,'GRID_CARDINALITY');
 const L=P(j.L),eps=P(j.endpoint_epsilon),loss=P(j.spacing_loss);
 need(lt(q(0),L)&&lt(q(0),eps)&&lt(eps,q(1).div(100))&&lt(q(0),loss)&&lt(loss,q(1).div(100)),'STRICT_ENDPOINT_AND_SPACING');
 need(j.seeds.length===3&&j.targets.length>0&&j.targets.length<=16,'INPUT_COUNT');const targets=[];
 for(const sp of j.targets){
  const T=P(sp.cap),t=P(sp.near_t),t2=P(sp.two_t);need(lt(q(4),T)&&lt(T,q(5))&&lt(q(0),t2)&&lt(t2,t)&&lt(t,q(2).div(5)),'PARAMETER_DOMAIN');
  const A=L.div(T),alpha=q(1).sub(eps),step=T.sub(alpha.mul(2)).div(3),cs=frame(t),b=q(1).div(cs[0].add(cs[1]));need(lt(q(0),step)&&lt(step,b),'NEAR_GRID_GAP');
  const axis=Array.from({length:4},(_,i)=>A.mul(alpha.add(step.mul(i))));need(lt(axis[0],A)&&lt(L.sub(A),axis[3])&&eq(axis[0].add(axis[3]),L)&&eq(axis[1].add(axis[2]),L),'GRID_ENDPOINTS_SYMMETRY');
  const c2=frame(t2),b2=q(1).div(c2[0].add(c2[1])),w=b2.sub(loss),lo=T.sub(alpha).sub(w.mul(3)),hi=alpha;
  need(lt(q(0),w)&&lt(w,b2)&&le(lo,hi),'MOVABLE_GRID_PHASE');
  const bands=Array.from({length:4},(_,i)=>[lo.add(w.mul(i)),hi.add(w.mul(i))]);
  let rho=mx(q(0),mx(bands[0][0].sub(q(1).div(2)),T.sub(q(1).div(2)).sub(bands[3][1])));
  for(let i=0;i<3;i++)rho=mx(rho,bands[i+1][0].sub(bands[i][1]).div(2));
  const disk=q(1).div(4).sub(rho.mul(rho).mul(2));need(lt(q(0),disk),'MOVABLE_DISK_MARGIN');
  const boxes=[];
  for(const seed of j.seeds){
   const tt=P(seed.t),ex=P(seed.ex),ey=P(seed.ey),et=P(seed.et),top=q(1).add(tt).add(et);
   need(lt(q(0),ex)&&lt(q(0),ey)&&lt(q(0),et)&&lt(t,tt.sub(et))&&lt(top.mul(top),q(2)),'SEED_DOMAIN');
   const inner=A.sub(ex.add(ey).mul(2)).div(q(1).add(et.mul(2)));need(lt(q(0),inner),'POSITIVE_CORE');
   const poly=verts([P(seed.cx),P(seed.cy)],tt,inner);
   for(let sw=0;sw<2;sw++)for(let fx=0;fx<2;fx++)for(let fy=0;fy<2;fy++){
    const vs=poly.map(p=>{let a=p.slice();if(sw)a.reverse();if(fx)a[0]=L.sub(a[0]);if(fy)a[1]=L.sub(a[1]);return a;});
    let chosen=-1,pm=q(0);for(let y=0;y<4;y++)for(let x=0;x<4;x++){const m=margin(vs,[axis[x],axis[y]],inner);if(lt(q(0),m)&&chosen<0){chosen=4*y+x;pm=m;}}
    need(chosen>=0,'BOX_WITHOUT_COMMON_GRID_POINT');boxes.push({seed:seed.id,transform:4*sw+2*fx+fy,point_index:chosen,core_side:String(inner),point_margin:String(pm)});
   }
  }
  targets.push({cap:String(T),near_t:String(t),two_t:String(t2),canonical_upper_t:String(q(1).sub(t).div(q(1).add(t))),grid_gap_margin:String(b.sub(step)),moving_rho:String(rho),moving_disk_margin:String(disk),axis_points:axis.map(String),boxes,union_capacity:16,remaining_restricted_capacity:15});
 }
 return {schema:'n17.c028.stabbing-result.v1',new_lower_bound:false,targets};
}
if(require.main===module)try{need(process.argv.length===4,'USAGE_INPUT_FRESH_OUTPUT');const[ip,op]=process.argv.slice(2);need(!fs.existsSync(op),'FRESH_OUTPUT_REQUIRED');const out=main(JSON.parse(fs.readFileSync(ip,'utf8')));fs.writeFileSync(op,JSON.stringify(out)+'\n',{flag:'wx'});console.log('PASS_STABBING_AND_CONTINUOUS_CAPACITY');}catch(e){console.error('REJECT '+e.message);process.exit(1);}
module.exports={main};
