'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,'.recheck',p),'utf8'));
if(process.argv[2]==='global'){
 const t=read('global/THEOREM.json');
 assert.equal(t.status,'PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION');assert.equal(t.target,'116511/25000');
 assert.equal(t.intervals,4991);assert.equal(String(t.budget_units),'17000448944');
 assert.equal(String(t.minimum_units),'1000026844');assert.equal(String(t.surplus),'7404');
}else if(process.argv[2]==='local'){
 const t=read('strip-independent.json');assert.equal(t.status,'PASS_PAIRED_LOCAL_CONTINUOUS_ANGLE_WALL_STRIP_MINIMA');
 assert.equal(t.rows.length,17);assert.equal(String(t.budget_units),'17000401055');
 for(const r of t.rows)assert.equal(String(r.minimum_open_fee),'1000026908');
 const a=read('failure-cpp.json'),b=read('failure-bigint.json');
 assert.equal(b.status,'PASS_EXACT_ACTUAL_PARENT_COUNTEREXAMPLE');assert.equal(a.rows.length,1);assert.equal(b.rows.length,1);
 assert.equal(String(a.rows[0].open_fee),'999975439');assert.equal(String(b.rows[0].open_fee),'999975439');
 assert.equal(String(a.rows[0].open_surplus),'-818592');assert.equal(String(b.rows[0].open_surplus),'-818592');
}else throw Error('expected global or local / 需要global或local');
console.log('PASS_FRESH_EXPECTED_RESULTS / 新运行结果符合预期');
