'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
for(const [p,v] of Object.entries(JSON.parse(fs.readFileSync(path.join(__dirname,'MANIFEST.json'))).files)){const b=fs.readFileSync(path.join(__dirname,p));if(b.length!==v.bytes||crypto.createHash('sha256').update(b).digest('hex')!==v.sha256)throw Error('IDENTITY / 身份 '+p);}console.log('PASS_BYTES_ONLY / 仅字节身份通过');
