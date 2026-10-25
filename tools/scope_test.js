// Simulate KubeJS shared global scope: concatenate all server scripts and check for redeclaration errors
const fs=require('fs'),vm=require('vm'),dir=process.argv[2];
const stub=new Proxy(function(){},{get:(t,k)=>k==='prototype'?{}:stub,apply:()=>stub,construct:()=>stub});
const ctx=vm.createContext({ServerEvents:stub,LevelEvents:stub,BlockEvents:stub,ItemEvents:stub,PlayerEvents:stub,Item:stub,BlockPos:stub,console});
for(const f of fs.readdirSync(dir).sort()){vm.runInContext(fs.readFileSync(dir+'/'+f,'utf8'),ctx,{filename:f});console.log('loaded',f)}
