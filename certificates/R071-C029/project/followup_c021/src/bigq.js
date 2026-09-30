'use strict';
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a;}
class Q{
 constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('ZERO_DENOMINATOR');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);this.n=n/g;this.d=d/g;}
 static parse(s){if(typeof s!=='string'||s.length>10000||!/^[-]?\d+\/\d+$/.test(s))throw Error('BAD_RATIONAL');const [n,d]=s.split('/');if(BigInt(d)<=0n)throw Error('NONPOSITIVE_DENOMINATOR');return new Q(n,d);}
 add(b){b=q(b);return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
 sub(b){return this.add(q(b).neg());}
 mul(b){b=q(b);return new Q(this.n*b.n,this.d*b.d);}
 div(b){b=q(b);return new Q(this.n*b.d,this.d*b.n);}
 neg(){return new Q(-this.n,this.d);}
 cmp(b){b=q(b);const x=this.n*b.d-b.n*this.d;return x<0n?-1:x>0n?1:0;}
 abs(){return this.n<0n?this.neg():this;}
 toString(){return `${this.n}/${this.d}`;}
}
function q(x){return x instanceof Q?x:new Q(x);}
module.exports={Q,q};
