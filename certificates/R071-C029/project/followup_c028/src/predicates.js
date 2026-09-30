'use strict';
const fs=require('fs'),{Q,q}=require('../../followup_c021/src/bigq.js'),{strictParse}=require('./strict_json.js'),{projectionsBelow}=require('./atlas.js');
const need=(v,s)=>{if(!v)throw Error(s);};
function main(j){need(j.schema==='n17.c028.angular-predicates.v1','SCHEMA');const cases=j.cases.map(c=>{need(c.dx.length===2&&c.dy.length===2&&c.t.length===2,'INTERVAL_SHAPE');const[x0,x1]=c.dx.map(Q.parse),[y0,y1]=c.dy.map(Q.parse),[t0,t1]=c.t.map(Q.parse),b=Q.parse(c.bound);need(x0.cmp(x1)<=0&&y0.cmp(y1)<=0&&q(0).cmp(t0)<=0&&t0.cmp(t1)<=0&&t1.cmp(q(1))<=0&&b.cmp(q(0))>0,'PREDICATE_DOMAIN');const v=projectionsBelow(x0,x1,y0,y1,t0,t1,b);need(v===c.expected,'PREDICATE_EXPECTATION');return{id:c.id,all_strictly_below:v};});return{schema:'n17.c028.angular-predicate-result.v1',cases};}
if(require.main===module)try{need(process.argv.length===4,'USAGE_INPUT_FRESH_OUTPUT');const[ip,op]=process.argv.slice(2);need(!fs.existsSync(op),'FRESH_OUTPUT_REQUIRED');fs.writeFileSync(op,JSON.stringify(main(strictParse(fs.readFileSync(ip,'utf8'))))+'\n',{flag:'wx'});console.log('PASS_ANGULAR_PREDICATES');}catch(e){console.error('REJECT '+e.message);process.exit(1);}
module.exports={main};
