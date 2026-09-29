'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),root=__dirname;
for(const [p,v] of Object.entries(JSON.parse(fs.readFileSync(path.join(root,'MANIFEST.json'))).files)){
 const b=fs.readFileSync(path.join(root,p));if(b.length!==v.bytes||crypto.createHash('sha256').update(b).digest('hex')!==v.sha256)throw Error('identity / 身份: '+p);
}console.log('PASS_PACKAGE_BYTES_ONLY / 仅文件身份通过');
