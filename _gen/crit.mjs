import Beasties from 'beasties'; import fs from 'fs'; import path from 'path';
const root='/workspace/diler-consult';
const b=new Beasties({path:root,publicPath:'/',preload:'swap',pruneSource:false,reduceInlineStyles:false,logLevel:'warn',fonts:false,compress:true});
function walk(d){for(const f of fs.readdirSync(d)){const p=path.join(d,f);if(['assets','_gen'].includes(f))continue;const s=fs.statSync(p);if(s.isDirectory())walk(p);else if(f.endsWith('.html'))files.push(p);}}
const files=[];walk(root);
for(const f of files){const h=fs.readFileSync(f,'utf8');if(h.includes('data-beasties'))continue;const o=await b.process(h);fs.writeFileSync(f,o);}
console.log(files.length);
