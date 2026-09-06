const fs=require('fs'),vm=require('vm'),assert=require('assert');

const source=fs.readFileSync('xaydungphuluc.html','utf8');
const target=fs.readFileSync('backupcode viettailieu/canvas_xaydungphuluc.html','utf8');
const endpoint='https://hoangthiencm.id.vn/api/canvas_gemini.php';
const ids=html=>[...html.matchAll(/\bid=["']([^"']+)["']/g)].map(match=>match[1]);
const functions=html=>[...html.matchAll(/(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(/g)].map(match=>match[1]);
const sourceIds=new Set(ids(source)),targetIds=new Set(ids(target));
const sourceFunctions=new Set(functions(source)),targetFunctions=new Set(functions(target));

// Canvas only replaces the model/key controls. Every other original DOM hook and
// function must remain available so this page continues to be a 1:1 copy.
for(const id of sourceIds){if(!['selectModel','keyBadge'].includes(id))assert(targetIds.has(id),`missing original DOM id #${id}`)}
for(const name of sourceFunctions)assert(targetFunctions.has(name),`missing original function ${name}`);
assert(targetIds.has('canvasHostBanner'),'missing Canvas connection banner');

for(const text of [
  '<script src="https://hoangthiencm.id.vn/js/khbd-yccd.js"></script>',
  '<script src="https://hoangthiencm.id.vn/js/khbd-standards.js"></script>',
  endpoint,
  "fetch(CANVAS_ENDPOINT,{method:'OPTIONS',credentials:'omit'})",
  'Đã kết nối Gemini Canvas · gemini-3-flash-preview',
  'Gemini Canvas · gemini-3-flash-preview (Hệ thống cấp)',
  "apiKeys=['canvas-session']",'mistralKeys=[]',
  "method:'POST'","credentials:'omit'",'body:JSON.stringify({payload,timeout:75})',
  'envelope?.body','width:11906,height:16838','orientation:PageOrientation.LANDSCAPE',
  'Biểu hiện năng lực số','Biểu hiện năng lực AI','0070C0','7030A0'
])assert(target.includes(text),`missing Canvas requirement: ${text}`);
assert(!/src=["'][^"']*(?:security-guard|access-control)\.js/.test(target),'Canvas must not load access/security scripts');
assert(!/(?:generativelanguage\.googleapis\.com|api\.mistral\.ai|api\/user_gemini_keys\.php)/.test(target),'Canvas must not call direct provider or user-key services');

function sliceFunction(name){
  const start=target.indexOf(`async function ${name}(`);
  assert(start>=0,`missing ${name}`);
  return target.slice(start,target.indexOf('\n',start));
}
const calls=[];
const sandbox={console,AbortController,clearTimeout,setTimeout,fetch:async(url,init)=>{
  calls.push({url,init});
  return {ok:true,status:200,json:async()=>({ok:true,status:200,body:{candidates:[{content:{parts:[{text:'{"ok":true,"source":"canvas"}'}]}}]}})};
}};
vm.createContext(sandbox);
vm.runInContext(
  `const CANVAS_ENDPOINT=${JSON.stringify(endpoint)},GEMINI_TIMEOUT_MS=75000,DEFAULT_GEMINI_MODEL='gemini-3-flash-preview';let aborter=null;function isUserAbort(){return false};`+
  sliceFunction('fetchWithGeminiTimeout')+'\n'+sliceFunction('requestGemini')+'\n'+sliceFunction('readGeminiResponse')+'\n'+sliceFunction('callGemini'),sandbox
);
(async()=>{
  const result=await vm.runInContext("callGemini('kiểm tra Canvas')",sandbox);
  assert.deepEqual(JSON.parse(JSON.stringify(result)),{ok:true,source:'canvas'});
  assert.equal(calls.length,1);
  assert.equal(calls[0].url,endpoint);
  assert.equal(calls[0].init.method,'POST');
  assert.equal(calls[0].init.credentials,'omit');
  assert.equal(calls[0].init.headers['content-type'],'application/json');
  const body=JSON.parse(calls[0].init.body);
  assert.equal(body.timeout,75);
  assert.equal(body.payload.contents[0].parts[0].text,'kiểm tra Canvas');
  console.log('canvas-xaydungphuluc-smoke: PASS');
})().catch(error=>{console.error(error);process.exit(1)});
