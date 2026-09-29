'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
if(process.argv[2]==='global'){
 const t=read('.recheck/global/THEOREM.json');assert.equal(t.status,'PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION');assert.equal(t.target,'46604427/10000000');assert.equal(t.intervals,5107);assert.equal(String(t.minimum_units),'1000026844');assert.equal(String(t.budget_units),'17000448944');assert.equal(String(t.surplus),'7404');
}else if(process.argv[2]==='geometry'){
 const t=read('.recheck/all-bigint.json'),b=read('.recheck/barrier-bigint.json');
 assert.equal(t.status,'PASS_INDEPENDENT_BIGINT_SAME_BUDGET_MONOTONE_GEOMETRIC_RULE_OVERLAY');assert.equal(t.upgraded_orbits,319);assert.equal(t.upgraded_images,2552);assert.equal(t.truth_states,206976);assert.equal(String(t.budget_units),'17000448944');
 assert.equal(b.status,'PASS_INDEPENDENT_BIGINT_PARENT_SEPARATION_COMPLETION_OBSTRUCTION');assert.equal(b.blocked_losing_images,6574);assert.equal(b.fired_images,474);assert.equal(b.open_fee,'999880603');assert.equal(b.surplus,'-2478693');
 const c=read('project/followup_c016/results/target_4.6604427/certificate.json'),m=read('project/followup_c015/data/lifted_accepted_model.json');
 assert.equal(m.L,c.L);assert.equal(m.coordinate_denominator,c.coordinate_denominator);assert.equal(String(m.budget_units),String(c.budget_units));assert.deepEqual(m.point_orbits.slice(0,c.point_orbits.length),c.point_orbits);assert(m.point_orbits.slice(c.point_orbits.length).every(x=>x[2]===0));assert.deepEqual(m.threshold_orbits.slice(0,c.threshold_orbits.length),c.threshold_orbits);assert(m.threshold_orbits.slice(c.threshold_orbits.length).every(x=>x.weight===0));
}else throw Error('global or geometry / 需要global或geometry');
console.log('PASS_FRESH_SCOPED_RESULTS / 新运行范围内结果通过');
