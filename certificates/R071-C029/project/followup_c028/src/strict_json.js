'use strict';
// JSON parser wrapper rejecting duplicate object keys and unsafe numeric literals.
function strictParse(text){
 let i=0; const n=text.length,need=(v,s)=>{if(!v)throw Error(s);};
 function ws(){while(i<n&&/\s/.test(text[i]))i++;}
 function str(){need(text[i]==='"','JSON_STRING');const start=i++;let escape=false;while(i<n){const c=text[i++];if(escape){escape=false;continue;}if(c==='\\'){escape=true;continue;}if(c==='"')return JSON.parse(text.slice(start,i));}throw Error('JSON_UNTERMINATED_STRING');}
 function val(depth){need(depth<100,'JSON_DEPTH');ws();const c=text[i];if(c==='"')return str();if(c==='{'){i++;ws();const o=Object.create(null),keys=new Set();if(text[i]==='}'){i++;return o;}while(true){ws();const k=str();need(!keys.has(k),'DUPLICATE_JSON_KEY');keys.add(k);ws();need(text[i++]===':','JSON_COLON');o[k]=val(depth+1);ws();const z=text[i++];if(z==='}')return o;need(z===',','JSON_OBJECT');}}
 if(c==='['){i++;ws();const a=[];if(text[i]===']'){i++;return a;}while(true){a.push(val(depth+1));ws();const z=text[i++];if(z===']')return a;need(z===',','JSON_ARRAY');}}
 for(const[s,v]of[['true',true],['false',false],['null',null]])if(text.startsWith(s,i)){i+=s.length;return v;}
 const m=/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/.exec(text.slice(i));need(m,'JSON_VALUE');i+=m[0].length;const x=Number(m[0]);need(Number.isSafeInteger(x),'UNSAFE_JSON_NUMBER');return x;}
 const out=val(0);ws();need(i===n,'JSON_TRAILING_DATA');return out;
}
module.exports={strictParse};
