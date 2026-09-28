'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=__dirname,m=JSON.parse(fs.readFileSync(path.join(root,'MANIFEST.json'),'utf8'));
for(const [name,item] of Object.entries(m.files)){
 const raw=fs.readFileSync(path.join(root,name));
 if(raw.length!==item.bytes||crypto.createHash('sha256').update(raw).digest('hex')!==item.sha256)throw Error('identity / 身份: '+name);
}
console.log('PASS_PACKAGE_BYTES_ONLY / 仅文件身份通过');
