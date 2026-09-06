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
function sliceNamedFunction(name){
  const start=target.indexOf(`function ${name}(`);
  assert(start>=0,`missing ${name}`);
  return target.slice(start,target.indexOf('\n',start));
}
assert(target.includes('function getConfig({includeAiSelection=true}={})'),
  'getConfig must support suppressing AI selection while bootstrapping PPCT');
assert(target.includes('defaultPpctRows(getConfig({includeAiSelection:false}))'),
  'empty PPCT fallbacks must not recursively read AI selection');

// With no recognized PPCT, reading AI selection used to call aiCandidates(),
// which asked getConfig() for default rows and entered the same path again.
// The bootstrap config must avoid those selection helpers and still create rows.
const bootstrapSandbox={
  sourcePpctRows:[],sourcePpctTable:null,
  grade:{value:'6'},subject:{value:'Toán học'},schoolYear:{value:'2026-2027'},
  school:{value:''},department:{value:''},teacher:{value:''},
  classCount:{value:''},studentCount:{value:''},teacherCount:{value:''},
  nlsEnabled:{checked:false},nlsRate:{value:'0'},nlsDensity:{value:'1'},
  aiEnabled:{checked:true},aiRate:{value:'0'},aiDensity:{value:'1'},
  clil:{checked:false},inclusive:{checked:false},instructions:{value:''},sgkCompactContext:'',
  defaultPpctRows(config){
    assert.deepEqual(JSON.parse(JSON.stringify(config.ai.selectedLessons)),[]);
    assert.deepEqual(JSON.parse(JSON.stringify(config.ai.selectedPeriods)),[]);
    return [{lesson:'PPCT mẫu',periods:'1',tietCT:'1',week:'1',devices:'',location:'',isHeader:false}];
  },
  extractLessonPeriods(){return 1},isAdminLesson(){return false},
  selectedAiLessons(){throw new RangeError('AI selection must not run while PPCT is bootstrapping')},
  selectedAiPeriods(){throw new RangeError('AI selection must not run while PPCT is bootstrapping')}
};
vm.createContext(bootstrapSandbox);
vm.runInContext(sliceNamedFunction('getConfig'),bootstrapSandbox);
assert.equal(vm.runInContext('defaultPpctRows(getConfig({includeAiSelection:false})).length',bootstrapSandbox),1,
  'empty PPCT must create its default rows without recursively reading AI selection');
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
