const fs=require('fs'),vm=require('vm'),assert=require('assert');

const source=fs.readFileSync('xaydungphuluc.html','utf8');
const target=fs.readFileSync('canvas_xaydungphuluc.html','utf8');
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
['function enrichNlsCode','function cleanNlsColumnText','function cleanAiColumnText','hasCode:hasAiCode(value)','return lines.length?lines.join(\'\\n\'):\'\''].forEach(value=>assert(target.includes(value),`missing clean Appendix 1 integration behavior: ${value}`));
['nlsAdaptiveOptions','nlsNoAiDensity','Tự động theo tiết &amp; AI (Khuyên dùng)','function toggleNlsCustomDensity','function getExpectedNlsCount','noAiDensity','row.lesson,row.periods','QUY TẮC PHÂN BỔ NLS'].forEach(value=>assert(target.includes(value),`missing adaptive NLS behavior: ${value}`));
const adaptiveOptionsMarkup=target.match(/<div id="nlsAdaptiveOptions"[\s\S]*?<\/div><\/div><div class="border rounded-xl p-4">/);
assert(adaptiveOptionsMarkup,'Canvas adaptive NLS options markup missing');
assert(!adaptiveOptionsMarkup[0].includes('dark:bg-slate-800'),'Canvas adaptive NLS options must not use Tailwind dark background');
['background:var(--paper)','border-color:var(--line)','color:var(--ink)','color:var(--brand)','id="nlsNoAiDensity"','background:var(--card)'].forEach(value=>assert(adaptiveOptionsMarkup[0].includes(value),`Canvas adaptive NLS theme missing: ${value}`));

for(const text of [
  '<script src="https://hoangthiencm.id.vn/js/khbd-yccd.js"></script>',
  '<script src="https://hoangthiencm.id.vn/js/khbd-standards.js"></script>',
  endpoint,
  "fetch(CANVAS_ENDPOINT,{method:'OPTIONS',credentials:'omit'})",
  'Đã kết nối Gemini Canvas · gemini-3-flash-preview',
  'Gemini Canvas · gemini-3-flash-preview (Hệ thống cấp)',
  "apiKeys=['canvas-session']",'mistralKeys=[]',
  "method:'POST'","credentials:'omit'",'body:JSON.stringify({payload,timeout:120})','GEMINI_TIMEOUT_MS=120000',
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
  const start=[target.indexOf(`function ${name}(`),target.indexOf(`async function ${name}(`)].filter(index=>index>=0).sort((a,b)=>a-b)[0];
  assert(start>=0,`missing ${name}`);
  return target.slice(start,target.indexOf('\n',start));
}
const adaptiveNlsSandbox={};vm.createContext(adaptiveNlsSandbox);vm.runInContext(sliceNamedFunction('getExpectedNlsCount')+'\n'+sliceNamedFunction('getExpectedNlsMaxCount'),adaptiveNlsSandbox);
const adaptiveNlsConfig={nls:{density:'adaptive',noAiDensity:'2-3'}};
assert.equal(adaptiveNlsSandbox.getExpectedNlsCount(1,false,adaptiveNlsConfig),2,'one-period lessons must use two NLS codes');
assert.equal(adaptiveNlsSandbox.getExpectedNlsCount(2,true,adaptiveNlsConfig),2,'AI-selected multi-period lessons must use two NLS codes');
assert.equal(adaptiveNlsSandbox.getExpectedNlsCount(2,false,adaptiveNlsConfig),2,'the 2–3 setting must permit a two-code fallback');
assert.equal(adaptiveNlsSandbox.getExpectedNlsMaxCount(2,false,{nls:{density:'adaptive',noAiDensity:'2'}}),2,'the two-code option must cap a multi-period lesson without AI at two NLS codes');
assert.equal(adaptiveNlsSandbox.getExpectedNlsMaxCount(2,false,adaptiveNlsConfig),3,'the 2–3 option must cap a multi-period lesson without AI at three NLS codes');
assert.equal(adaptiveNlsSandbox.getExpectedNlsMaxCount(1,false,adaptiveNlsConfig),2,'one-period lessons must cap NLS at two codes');
assert.equal(adaptiveNlsSandbox.getExpectedNlsMaxCount(2,true,adaptiveNlsConfig),2,'AI-selected multi-period lessons must cap NLS at two codes');
const cleanIntegrationSandbox={};vm.createContext(cleanIntegrationSandbox);
vm.runInContext(sliceNamedFunction('foldText')+'\n'+sliceNamedFunction('cleanLessonDescription')+'\n'+sliceNamedFunction('lessonAppliedNlsDescription')+'\n'+sliceNamedFunction('lessonAppliedAiDescription')+'\n'+sliceNamedFunction('enrichNlsCode')+'\n'+sliceNamedFunction('cleanNlsColumnText')+'\n'+sliceNamedFunction('cleanAiColumnText'),cleanIntegrationSandbox);
assert.equal(cleanIntegrationSandbox.cleanNlsColumnText('[NLS: 5.3.TC2a - Sử dụng GeoGebra].'),'5.3.TC2a - Sử dụng GeoGebra.','Canvas must remove a bracket before a final NLS period');
assert.equal(cleanIntegrationSandbox.cleanNlsColumnText('[NLS: 5.3.TC2a - Sử dụng GeoGebra],'),'5.3.TC2a - Sử dụng GeoGebra','Canvas must remove a bracket before a final NLS comma');
assert.equal(cleanIntegrationSandbox.cleanNlsColumnText('[NLS: 5.3.TC2a - Sử dụng GeoGebra] .'),'5.3.TC2a - Sử dụng GeoGebra.','Canvas must remove a spaced NLS bracket before a period');
assert.equal(cleanIntegrationSandbox.cleanAiColumnText('[AI: 6.A1.1 - Hỗ trợ bài tập]. (Áp dụng: tiết 1).'),'6.A1.1 - Hỗ trợ bài tập. (Áp dụng: tiết 1).','Canvas must retain AI scope while removing its stray bracket');
assert.equal(cleanIntegrationSandbox.cleanAiColumnText(''),'','Canvas must preserve the blank Appendix 1 AI cell');
const canvasBareAi = cleanIntegrationSandbox.cleanAiColumnText('9.B2.1 - (Áp dụng: tiết 1, 2).', 'Bài 1: Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn');
assert(!canvasBareAi.includes('9.B2.1 - (Áp dụng:'), 'Canvas: bare AI code without description must be enriched');
assert(canvasBareAi.includes('9.B2.1 - Ứng dụng công cụ AI') && canvasBareAi.includes('(Áp dụng: tiết 1, 2).'), 'Canvas: AI code 9.B2.1 must have pedagogical description and retain scope');
const canvasUnpedagogicalNls = cleanIntegrationSandbox.cleanNlsColumnText('[NLS: 5.3.TC2a - Sử dụng chatbot AI để tìm hiểu lịch sử ra đời của hệ phương trình bậc nhất.;]', 'Bài 1: Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn');
assert(!canvasUnpedagogicalNls.includes('chatbot') && !canvasUnpedagogicalNls.includes('lịch sử ra đời'), 'Canvas: unpedagogical chatbot history NLS must be filtered out');
assert(canvasUnpedagogicalNls.includes('5.3.TC2a'), 'Canvas: NLS code must keep a valid Miền 1–5 code after rewrite');
assert.equal(cleanIntegrationSandbox.cleanNlsColumnText('[NLS: 6.1.TC2a - Hiểu biết về hệ thống trí tuệ nhân tạo]', 'Bài 1: Tập hợp'), '-', 'Canvas: legacy NLS miền 6 must be dropped');
assert(target.includes('function canvasConfirm(message)'), 'Canvas must provide an in-DOM confirmation modal');
assert(!/\bconfirm\(/.test(target), 'Canvas must not call the browser confirm() API in a sandbox');
for(const name of ['loadDraftById','deleteDraftFromServer','restoreCanvasDraft','resetData','deletePpctRowAt'])assert(target.includes(`await canvasConfirm(`),`${name} must await the Canvas confirmation modal`);

// Gemini Canvas does not grant allow-modals, so confirmation must be rendered
// in the document and resolved only by its own buttons or backdrop.
let renderedConfirmModal;
const confirmSandbox={
  esc:value=>String(value).replace(/</g,'&lt;'),
  document:{
    createElement(){
      const actions={cancel:{},ok:{}};
      return {className:'',style:{},innerHTML:'',removed:false,
        querySelector(selector){return actions[selector.includes('cancel')?'cancel':'ok']},
        addEventListener(_event,handler){this.backdropHandler=handler},
        remove(){this.removed=true}
      };
    },
    body:{appendChild(modal){renderedConfirmModal=modal}}
  }
};
vm.createContext(confirmSandbox);
vm.runInContext(sliceNamedFunction('canvasConfirm'),confirmSandbox);
(async()=>{
  const accepted=confirmSandbox.canvasConfirm('Mở <b>nháp</b>?');
  assert.equal(renderedConfirmModal.className,'modal');
  assert(renderedConfirmModal.innerHTML.includes('Mở &lt;b>nháp&lt;/b>?'));
  renderedConfirmModal.querySelector('[data-action="ok"]').onclick();
  assert.equal(await accepted,true);
  assert.equal(renderedConfirmModal.removed,true);
  const cancelled=confirmSandbox.canvasConfirm('Xóa?');
  renderedConfirmModal.backdropHandler({target:renderedConfirmModal});
  assert.equal(await cancelled,false);
  console.log('canvas in-DOM confirmation: PASS');
})().catch(error=>{console.error(error);process.exitCode=1});
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
  `const CANVAS_ENDPOINT=${JSON.stringify(endpoint)},GEMINI_TIMEOUT_MS=120000,DEFAULT_GEMINI_MODEL='gemini-3-flash-preview';let aborter=null;function isUserAbort(){return false};`+
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
  assert.equal(body.timeout,120);
  assert.equal(body.payload.contents[0].parts[0].text,'kiểm tra Canvas');
  console.log('canvas-xaydungphuluc-smoke: PASS');
})().catch(error=>{console.error(error);process.exit(1)});


// Draft transport must work with an opaque Canvas origin and no cookies.
const draftEndpoint='https://hoangthiencm.id.vn/api/user_phuluc_draft.php';
assert(target.includes(`const DRAFT_API_ENDPOINT = '${draftEndpoint}';`));
assert(!target.includes("fetch('api/user_phuluc_draft.php"));
for(const id of ['saveDraftAccount','loadDraftAccount','draftJsonInput'])assert(targetIds.has(id));
for(const name of ['submitSaveDraft','fetchAndRenderDraftList','loadDraftById','deleteDraftFromServer'])assert(sliceFunction(name).includes('requestCanvasDraft('));
const storage=new Map(),draftCalls=[],messages=[];
const draftPayload={version:1,config:{giaoVien:'Giáo viên',monHoc:'Toán học'},sourcePpctRows:[{lesson:'Bài 1'}],results:{'1':{title:'Phụ lục'}}};
let restored=null,download=null;
const draftSandbox={URLSearchParams,Blob,console,
  allowRestore:true,
  localStorage:{getItem:key=>storage.get(key)||null,setItem:(key,value)=>storage.set(key,value)},
  document:{querySelector:()=>null},
  notify:message=>messages.push(message),
  buildDraftPayload:()=>draftPayload,draftDefaultTitle:()=> 'Kế hoạch mẫu',
  applyDraftPayload:value=>{restored=value},setDraftStatus(){},closeSaveDraftModal(){},closeLoadDraftModal(){},
  saveAs:(blob,name)=>{download={blob,name}},
  fetch:async(url,init)=>{draftCalls.push({url,init});return {ok:true}},
};
vm.createContext(draftSandbox);
vm.runInContext(`const DRAFT_API_ENDPOINT=${JSON.stringify(draftEndpoint)};let currentDraftId=42,currentDraftTitle='';async function canvasConfirm(){return allowRestore;}`+
  sliceNamedFunction('readCanvasStorage')+"\nlet canvasDraftAccount=readCanvasStorage('canvas_xdpl_user');\n"+
  ['setCanvasDraftAccount','savedCanvasDraft','restoreCanvasDraft','saveDraftLocally','loadDraftLocally','exportDraftJson'].map(sliceNamedFunction).join('\n')+'\n'+
  sliceFunction('requestCanvasDraft')+'\n'+sliceFunction('importDraftJson'),draftSandbox);
(async()=>{
  await assert.rejects(()=>draftSandbox.requestCanvasDraft({action:'list'}),/tài khoản/);
  assert.equal(draftCalls.length,0);
  draftSandbox.setCanvasDraftAccount(' teacher1 ');
  assert.equal(storage.get('canvas_xdpl_user'),'teacher1');
  assert.equal(vm.runInContext('currentDraftId',draftSandbox),null,'changing account must detach existing draft');
  for(const [params,options] of [[{action:'list'},{}],[{id:12},{}],[{},{method:'POST',body:JSON.stringify({draft:draftPayload})}],[{action:'delete'},{method:'POST',body:'{"id":12}'}]]){
    await draftSandbox.requestCanvasDraft(params,options);
    const call=draftCalls.at(-1),url=new URL(call.url);
    assert.equal(url.origin+url.pathname,draftEndpoint);
    assert.equal(url.searchParams.get('user_account'),'teacher1');
    assert.equal(call.init.headers['X-User-Account'],'teacher1');
    assert.equal(call.init.credentials,'omit');
    if(options.body)assert.equal(JSON.parse(call.init.body).user_account,'teacher1');
  }
  vm.runInContext(sliceFunction('loadDraftById'),draftSandbox);
  restored=null;
  draftSandbox.fetch=async()=>({ok:true,json:async()=>({ok:true,id:19,title:'Mở từ CSDL',draft:draftPayload})});
  assert.equal(await draftSandbox.loadDraftById(19),true,'opening a draft must proceed after the in-DOM confirmation');
  assert.deepEqual(JSON.parse(JSON.stringify(restored)),draftPayload);
  draftSandbox.saveDraftLocally();
  await draftSandbox.loadDraftLocally();
  assert.deepEqual(JSON.parse(JSON.stringify(restored)),draftPayload);
  restored=null;
  await assert.rejects(()=>draftSandbox.restoreCanvasDraft({unrelated:true}),/hợp lệ/);
  assert.equal(restored,null,'invalid JSON must not erase current work');
  draftSandbox.allowRestore=false;
  await draftSandbox.restoreCanvasDraft(JSON.parse(storage.get('canvas_xdpl_draft')));
  assert.equal(restored,null,'cancel must preserve current work');
  draftSandbox.allowRestore=true;
  draftSandbox.exportDraftJson();
  assert.equal(download.name,'ke-hoach-phu-luc.json');
  const exported=await download.blob.text();
  const input={files:[{text:async()=>exported}],value:'draft.json'};
  await draftSandbox.importDraftJson(input);
  assert.deepEqual(JSON.parse(JSON.stringify(restored)),draftPayload);
  assert.equal(input.value,'');
  draftSandbox.localStorage={getItem(){throw new Error('SecurityError')},setItem(){throw new Error('QuotaExceededError')}};
  assert.equal(draftSandbox.readCanvasStorage('canvas_xdpl_user'),'');
  draftSandbox.saveDraftLocally();
  assert(messages.at(-1).includes('Xuất file JSON'));
  draftSandbox.exportDraftJson();
  assert.equal(JSON.parse(await download.blob.text()).format,'canvas-xdpl-draft');
  console.log('canvas draft transport and offline recovery: PASS');
})().catch(error=>{console.error(error);process.exitCode=1});

assert(target.includes('grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5'),'Mục 1 form must stay at least 2 columns on a narrow Canvas');
assert(target.includes('py-1.5'),'header padding must be compact');
assert(target.includes('ppct-sticky-lesson'),'lesson column must be sticky while scrolling horizontally');
assert(target.includes('function toggleCompactMode('),'compact layout toggle must exist');
assert(target.includes('function toggleHeroBanner('),'hero banner must be collapsible');
assert(target.includes('function defaultPpctRows('),'defaultPpctRows must be defined');
assert(target.includes('SUBJECT_SAMPLE_TOPICS'),'non-math subjects must have sample PPCT topics');
assert(target.includes('annual>0&&annual<70'),'low-period subjects must cap AI periods at 20%');
assert(target.includes('title="Gemini Canvas · gemini-3-flash-preview (Hệ thống cấp)"'),'model badge must keep the Canvas model identity');
assert(target.includes('>Gemini Canvas<'),'model badge label must be shortened for narrow screens');
assert(target.includes('PPCT:')&&target.includes('NLS/AI:'),'Mục 4 actions must be grouped');

function extractNamed(src,name){
  const start=src.indexOf(`function ${name}(`);
  assert(start>=0,name+' missing');
  let depth=0,end=src.indexOf('{',start);
  for(let i=end;i<src.length;i++){
    if(src[i]==='{')depth++;
    else if(src[i]==='}'){depth--;if(depth===0)return src.slice(start,i+1)}
  }
  throw new Error('unterminated '+name);
}
const pickerSandbox={
  foldText(s){return String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toUpperCase().replace(/\s+/g,' ').trim()},
  cleanLessonDescription(s){return String(s||'')},
  selectedAiLessons(){return []},
  getSharedSgkLessonKnowledge(){return null},
  SUBJECTS:[['Toán học',140],['Ngữ văn',140],['Tiếng Anh (Ngoại ngữ 1)',105],['Khoa học tự nhiên',140],['Tin học',35],['Giáo dục công dân',35]],
  AI_SELECTION_LIMIT:12,
  getConfig(){return {monHoc:pickerSandbox.monHoc||'Toán học',lop:'7'}},
  nlsCandidates(){return pickerSandbox._cands},
  aiCandidates(){return pickerSandbox._cands},
  validPeriodCount(periods,tietCT){return Number(periods)||(String(tietCT||'').match(/\d+/g)||[]).length||1},
  _cands:[]
};
vm.createContext(pickerSandbox);
vm.runInContext(
  extractNamed(target,'nlsLessonPriorityScore')+'\n'+
  extractNamed(target,'prioritizedNlsLessons')+'\n'+
  extractNamed(target,'aiPeriodCandidates')+'\n'+
  extractNamed(target,'aiSelectionLimit')+'\n'+
  extractNamed(target,'prioritizedAiPeriods'),
  pickerSandbox
);
pickerSandbox.monHoc='Toán học';
assert.ok(pickerSandbox.nlsLessonPriorityScore('Bài 18. Tam giác đều, hình vuông')>pickerSandbox.nlsLessonPriorityScore('Kiểm tra giữa kỳ I'),'Toán geometry must outrank tests');
assert.ok(pickerSandbox.nlsLessonPriorityScore('Bài 38. Dữ liệu và thu thập dữ liệu')>pickerSandbox.nlsLessonPriorityScore('Ôn tập và Bài tập cuối chương II'),'Toán statistics must outrank review');
pickerSandbox.monHoc='Ngữ văn';
assert.ok(pickerSandbox.nlsLessonPriorityScore('Viết: Viết bài văn nghị luận','Ngữ văn')>pickerSandbox.nlsLessonPriorityScore('Đọc hiểu: Thơ trữ tình','Ngữ văn'),'Ngữ văn writing must outrank pure poetry');
pickerSandbox.monHoc='Tiếng Anh (Ngoại ngữ 1)';
assert.ok(pickerSandbox.nlsLessonPriorityScore('Unit Project: Digital poster','Tiếng Anh (Ngoại ngữ 1)')>pickerSandbox.nlsLessonPriorityScore('Pronunciation and language focus','Tiếng Anh (Ngoại ngữ 1)'),'English projects must outrank pronunciation drills');
pickerSandbox.monHoc='Khoa học tự nhiên';
assert.ok(pickerSandbox.nlsLessonPriorityScore('Bài thực hành thí nghiệm đo lường','Khoa học tự nhiên')>pickerSandbox.nlsLessonPriorityScore('Ôn tập học kì I','Khoa học tự nhiên'),'KHTN labs must outrank review');
pickerSandbox.getSharedSgkLessonKnowledge=()=>({digital_evidence:'Excel',ai_pedagogy_hint:'AI gợi ý'});
assert.ok(pickerSandbox.nlsLessonPriorityScore('Bài thường','Ngữ văn')>5,'SGK digital evidence must boost NLS priority');
pickerSandbox.getSharedSgkLessonKnowledge=()=>null;
pickerSandbox._cands=[
  {id:'ppct:0',lesson:'Viết: Viết bài văn nghị luận',periods:'1',tietCT:'1',week:'2'},
  {id:'ppct:1',lesson:'Đọc hiểu: Thơ trữ tình',periods:'1',tietCT:'2',week:'3'},
  {id:'ppct:2',lesson:'Nói và nghe: Thuyết trình',periods:'1',tietCT:'80',week:'20'},
  {id:'ppct:3',lesson:'Dự án đọc sách',periods:'1',tietCT:'81',week:'21'},
  {id:'ppct:4',lesson:'Ôn tập học kì II',periods:'1',tietCT:'90',week:'30'}
];
pickerSandbox.monHoc='Ngữ văn';
const ranked=pickerSandbox.prioritizedAiPeriods();
assert.equal(ranked.length,5,'all periods remain available after ranking');
const firstTwo=ranked.slice(0,2).map(x=>x.week);
assert.ok(firstTwo.some(w=>Number(w)<19)&&firstTwo.some(w=>Number(w)>=19),'12-period AI suggestions must mix both semesters');
pickerSandbox.getConfig=()=>({monHoc:'Tin học',lop:'8'});
assert.equal(pickerSandbox.aiSelectionLimit(Array.from({length:35},(_,i)=>({id:i}))),7,'35-period subjects cap AI at 20%');
pickerSandbox.getConfig=()=>({monHoc:'Toán học',lop:'6'});
assert.equal(pickerSandbox.aiSelectionLimit(Array.from({length:13},(_,i)=>({id:i}))),12,'Toán still allows 12 AI periods');
console.log('canvas responsive layout and multi-subject picker: PASS');
