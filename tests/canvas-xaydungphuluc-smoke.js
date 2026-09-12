const fs=require('fs'),vm=require('vm'),assert=require('assert');

const source=fs.readFileSync('xaydungphuluc.html','utf8');
const target=fs.readFileSync('canvas_xaydungphuluc.html','utf8');
const endpoint='https://hoangthiencm.id.vn/api/canvas_gemini.php';
const ids=html=>[...html.matchAll(/\bid=["']([^"']+)["']/g)].map(match=>match[1]);
const functions=html=>[...html.matchAll(/(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(/g)].map(match=>match[1]);
const sourceIds=new Set(ids(source)),targetIds=new Set(ids(target));
const sourceFunctions=new Set(functions(source)),targetFunctions=new Set(functions(target));
const defaultSchoolInfo={schoolYear:'2026-2027',school:'THCS Trần Phú',department:'Tổ Toán - Tin',teacher:'Hoàng Tấn Thiên'};
for(const [id,value] of Object.entries(defaultSchoolInfo)){
  const input=target.match(new RegExp(`<input[^>]*\\bid="${id}"[^>]*>`));
  assert(input,`Canvas missing default school-info input #${id}`);
  assert(input[0].includes(`value="${value}"`),`Canvas #${id} must have its editable default value`);
  assert(!/\\b(?:readonly|disabled)\\b/.test(input[0]),`Canvas #${id} must remain editable`);
}
['Theo tổng số tiết PPCT','Theo tổng số bài PPCT','AI tự đề xuất bài/tiết phù hợp dựa trên PPCT và ngữ cảnh SGK'].forEach(label=>assert(target.includes(label),`Canvas missing updated allocation wording: ${label}`));
assert(!target.includes('dạy bài mới'),'Canvas allocation wording must not imply that only new-teaching lessons count');

for(const id of ['nlsUnit','nlsCountInput','aiUnit','aiCountInput'])assert.equal(ids(target).filter(value=>value===id).length,1,`Canvas must keep exactly one #${id}`);
assert(!target.includes('aria-label="Phân bổ linh hoạt NLS và AI"'),'Canvas must not retain the duplicate flexible-allocation card');
for(const [control,cardTitle,rateControl] of [['nlsUnit','Năng lực số (CV 3456 / TT 02)','nlsRate'],['aiUnit','Trí tuệ nhân tạo (QĐ 2422)','aiRate']]){
  const controlIndex=target.indexOf(`id="${control}"`),cardIndex=target.indexOf(cardTitle),rateIndex=target.indexOf(`id="${rateControl}"`,cardIndex);
  assert(controlIndex>cardIndex&&controlIndex<rateIndex,`Canvas #${control} must appear in its Mục 1 card before its rate slider`);
}

// Canvas only replaces the model/key controls. Every other original DOM hook and
// function must remain available so this page continues to be a 1:1 copy.
for(const id of sourceIds){if(!['selectModel','keyBadge'].includes(id))assert(targetIds.has(id),`missing original DOM id #${id}`)}
for(const name of sourceFunctions)assert(targetFunctions.has(name),`missing original function ${name}`);
assert(targetIds.has('canvasHostBanner'),'missing Canvas connection banner');
assert(target.indexOf('<meta charset="utf-8">')<target.indexOf('<title>'),'charset must be declared before other document resources');
assert(target.indexOf('<meta name="viewport"')<target.indexOf('<title>'),'viewport must be declared before other document resources');
assert(!target.includes('cdn.tailwindcss.com'),'Canvas must not load runtime Tailwind CDN to avoid CSP worker blocks');
assert(!target.includes('AI_SELECTION_LIMIT'),'Canvas source must not retain the legacy AI hard-cap constant');
assert(!target.includes('tối đa 12 tiết AI'),'Canvas source must not tell users that AI selection is capped at 12 periods');
assert(target.includes('html,body{display:block!important;visibility:visible!important'),'Canvas must force-visible html/body against Tailwind FOUC');
assert(target.includes("setProperty('display','block','important')"),'Canvas must keep html/body visible if the host injects a hide style');
assert(target.indexOf('html,body{display:block!important')<target.indexOf('https://hoangthiencm.id.vn/css/khbd-styles.css'),'first-paint CSS must precede external stylesheets');
assert(target.includes('https://hoangthiencm.id.vn/css/khbd-styles.css'),'Canvas must load the static KHBD stylesheet');
assert(!target.includes('pdfjsLib'),'Canvas must not load PDF.js in the CSP-restricted Gemini sandbox');
assert(!target.includes('pdf.worker'),'Canvas must not configure a remote PDF Worker');
assert(!target.includes('GlobalWorkerOptions.workerSrc'),'Canvas must not configure a PDF Worker');
assert(!target.includes('new Worker('),'Canvas app must not create a Worker in Gemini');
assert(!target.includes('importScripts('),'Canvas app must not load worker scripts');
assert(target.includes('function documentImportUnavailable('),'Canvas must detect unsupported document import dependencies');
assert(target.includes('Gemini Canvas không thể đọc PDF trực tiếp vì môi trường này chặn PDF Worker.'),'Canvas must explain the PDF fallback to users');
assert(target.includes('const memoryStorage=Object.create(null);'),'Canvas must provide in-memory storage when sandbox storage is blocked');
assert(target.includes('function getCanvasStorage()'),'Canvas must safely probe browser storage');
assert(target.includes("document.readyState==='loading'"),'Canvas bootstrap must handle an already-complete document');
assert(target.includes("window.addEventListener('error'"),'Canvas must surface script errors in the host banner');
assert(target.includes("window.addEventListener('unhandledrejection'"),'Canvas must surface rejected promises in the host banner');
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
const sourceSafeParse=source.slice(source.indexOf('function safeParseAiJson('),source.indexOf('\n',source.indexOf('function safeParseAiJson(')));
const targetSafeParse=sliceNamedFunction('safeParseAiJson');
assert.equal(targetSafeParse,sourceSafeParse,'Canvas and standard interfaces must use the same safe AI JSON parser');
const parserSandbox={JSON,Error,String,RegExp};
vm.createContext(parserSandbox);
vm.runInContext(targetSafeParse,parserSandbox);
const rawControl=code=>`{"note":"Dòng một${String.fromCharCode(code)}Dòng hai"}`;
assert.deepEqual(JSON.parse(JSON.stringify(parserSandbox.safeParseAiJson('{"ok":true,"escaped":"\\\\n"}'))),{ok:true,escaped:'\\n'},'valid JSON and escaped sequences must remain unchanged');
assert.equal(parserSandbox.safeParseAiJson(rawControl(10)).note,'Dòng một\nDòng hai','raw newlines inside AI strings must be escaped before parsing');
assert.equal(parserSandbox.safeParseAiJson(rawControl(9)).note,'Dòng một\tDòng hai','raw tabs inside AI strings must be escaped before parsing');
assert.equal(parserSandbox.safeParseAiJson(rawControl(1)).note,`Dòng một${String.fromCharCode(1)}Dòng hai`,'other raw control characters must be preserved through Unicode escaping');
assert.deepEqual(JSON.parse(JSON.stringify(parserSandbox.safeParseAiJson('Lời dẫn\n```json\n{"items":[1,2,],}\n```\nLời kết'))),{items:[1,2]},'parser must extract fenced JSON from prose and recover trailing commas');
assert.equal(parserSandbox.safeParseAiJson(String.raw`{"formula":"\alpha"}`).formula,'\\alpha','a bare LaTex backslash must be converted into a JSON-safe literal backslash');
assert.throws(()=>parserSandbox.safeParseAiJson('không phải JSON'),/AI trả về JSON không hợp lệ/,'unrepairable AI output must report a useful parser error');
['function initCanvasEventBridge','function captureCanvasInlineHandlers','function parseCanvasInlineActions','function runCanvasInlineActions','removeAttribute(attribute)','new MutationObserver','addEventListener(type,event=>','Tương tác Canvas đã sẵn sàng.'].forEach(value=>assert(target.includes(value),`missing CSP-safe Canvas event bridge: ${value}`));
assert(!target.includes('eval(')&&!target.includes('Function('),'Canvas event bridge must not execute inline handlers dynamically');
const bridgeCalls=[];
const bridgeSandbox={
  window:{refreshSubjects(){bridgeCalls.push('subjects')},stageFiles(files,kind){bridgeCalls.push([files,kind])},print(){bridgeCalls.push('print')}},
  document:{querySelector(selector){return {click(){bridgeCalls.push(['click',selector])}}}}
};
vm.createContext(bridgeSandbox);
vm.runInContext(['splitCanvasActionParts','parseCanvasString','parseCanvasActionArgument','parseCanvasInlineActions','resolveCanvasActionArgument','runCanvasInlineActions'].map(sliceNamedFunction).join('\n'),bridgeSandbox);
const bridgeElement={value:'7',files:['ppct.docx'],checked:true,textContent:'Bài 1'};
const bridgeActions=bridgeSandbox.parseCanvasInlineActions("refreshSubjects();stageFiles(this.files,'ppct');document.querySelector('#draftJsonInput').click();window.print()");
assert.equal(bridgeActions.length,4,'event bridge must parse approved handler statements');
bridgeSandbox.runCanvasInlineActions(bridgeActions,bridgeElement,{type:'change'});
assert.deepEqual(JSON.parse(JSON.stringify(bridgeCalls)),['subjects',[['ppct.docx'],'ppct'],['click','#draftJsonInput'],'print'],'event bridge must dispatch approved calls without eval');
assert.equal(bridgeSandbox.parseCanvasInlineActions('refreshSubjects();alert(document.cookie)'),null,'event bridge must reject arbitrary expressions');
const bootstrapCalls=[];
const lifecycleSandbox={
  window:{},
  refreshSubjects(){bootstrapCalls.push('subjects')},loadDefaultPpctStructure(value){bootstrapCalls.push(['ppct',value])},checkSharedSgkKnowledge(value){bootstrapCalls.push(['knowledge',value])},syncRanges(){bootstrapCalls.push('ranges')},prefillTeacherIdentity(){bootstrapCalls.push('identity')},readCanvasStorage(){return 'dark'},
  document:{documentElement:{classList:{add:value=>bootstrapCalls.push(['theme',value])}}},initCanvasEventBridge(){bootstrapCalls.push('bridge')},bindFlexibleAllocationControls(){bootstrapCalls.push('allocation-controls')},restoreLayoutPrefs(){bootstrapCalls.push('layout')},updateKeyBadge(){bootstrapCalls.push('badge')},renderPreview(){bootstrapCalls.push('preview')},loadDraftFromServer(value){bootstrapCalls.push(['draft',value])},checkCanvasHostConnection(){bootstrapCalls.push('connection')},reportCanvasError(error){throw error}
};
vm.createContext(lifecycleSandbox);
vm.runInContext(sliceNamedFunction('initApp'),lifecycleSandbox);
lifecycleSandbox.initApp();
assert.deepEqual(JSON.parse(JSON.stringify(bootstrapCalls)),['bridge','allocation-controls','subjects',['ppct',true],['knowledge',true],'ranges','identity',['theme','dark'],'layout','badge','preview',['draft',{silent:true}],'connection'],'initApp must initialize a document that is already complete');
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
assert(target.includes('let _isGettingConfig=false;')&&target.includes('finally{_isGettingConfig=wasGettingConfig}'),
  'getConfig must restore its re-entrancy guard after every call');
assert(target.includes('defaultPpctRows(getConfig({includeAiSelection:false}))'),
  'empty PPCT fallbacks must not recursively read AI selection');

// With no recognized PPCT, reading AI selection used to call aiCandidates(),
// which asked getConfig() for default rows and entered the same path again.
// The bootstrap config must avoid those selection helpers and still create rows.
const bootstrapSandbox={
  sourcePpctRows:[],sourcePpctTable:null,
  grade:{value:'6'},subject:{value:'Toán học'},schoolYear:{value:'2026-2027'},
  school:{value:'THCS Trần Phú'},department:{value:'Tổ Toán - Tin'},teacher:{value:'Hoàng Tấn Thiên'},
  classCount:{value:''},studentCount:{value:''},teacherCount:{value:''},
  nlsEnabled:{checked:false},nlsRate:{value:'0'},nlsDensity:{value:'1'},
  aiEnabled:{checked:true},aiRate:{value:'0'},aiDensity:{value:'1'},
  clil:{checked:false},inclusive:{checked:false},instructions:{value:''},sgkCompactContext:'',allocationUnit(){return 'period'},
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
vm.runInContext('let _isGettingConfig=false;\n'+sliceNamedFunction('getConfig'),bootstrapSandbox);
assert.equal(vm.runInContext('defaultPpctRows(getConfig({includeAiSelection:false})).length',bootstrapSandbox),1,
  'empty PPCT must create its default rows without recursively reading AI selection');
assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext('getConfig({includeAiSelection:false})',bootstrapSandbox))),{
  capHoc:'THCS',lop:'6',monHoc:'Toán học',boSach:'Sách giáo khoa dùng chung (từ 2026-2027)',namHoc:'2026-2027',truong:'THCS Trần Phú',toChuyenMon:'Tổ Toán - Tin',giaoVien:'Hoàng Tấn Thiên',thongKe:{classes:'',students:'',teachers:''},nls:{enabled:false,rate:0,unit:'period',density:'1',noAiDensity:'2-3'},ai:{enabled:true,rate:0,unit:'period',density:'1',selectedLessons:[],selectedPeriods:[]},clil:false,hoaNhap:false,chiDao:'',sgkContext:''
},'Canvas getConfig must read the default school information');
bootstrapSandbox.school.value='THCS Tự Chọn';
assert.equal(vm.runInContext('getConfig({includeAiSelection:false}).truong',bootstrapSandbox),'THCS Tự Chọn','Canvas getConfig must retain manual school edits');
const sliderNodes={'#nlsRate':{value:'0'},'#nlsRateOut':{value:''},'#nlsUnit':{value:'period'},'#aiUnit':{value:'period'},'#nlsCountInput':{value:''},'#aiCountInput':{value:''}};
const sliderSandbox={
  document:{querySelector:selector=>sliderNodes[selector]||null},
  foldText:value=>String(value||'').toUpperCase(),cleanLessonDescription:value=>String(value||''),
  selectedAiLessons:()=>[],getSharedSgkLessonKnowledge:()=>null,
  SUBJECTS:[['Toán học',140]],
  getConfig:()=>({monHoc:'Toán học'}),
  nlsCandidates:()=>sliderSandbox.candidates,aiCandidates:()=>sliderSandbox.candidates,
  validPeriodCount:value=>Number(value)||1,updateAiPicker:()=>{},
  candidates:Array.from({length:10},(_,index)=>({id:`ppct:${index}`,lesson:index===0?'Ôn tập chương I':index===1?'Kiểm tra giữa kỳ I':`Bài slider ${index+1}`,periods:'1',tietCT:String(index+1),week:'1'})),
  nlsSelectedLessonIds:new Set(),aiSelectedLessonIds:new Set(),
  nlsRate:sliderNodes['#nlsRate'],nlsRateOut:sliderNodes['#nlsRateOut'],
  aiRate:{value:'0',min:'0',max:'100',disabled:false},aiRateOut:{value:''}
};
vm.createContext(sliderSandbox);
vm.runInContext(['nlsLessonPriorityScore','prioritizedNlsLessons','allocationUnit','aiPeriodCandidates','allocationTotals','nlsSelectedPeriodCount','chooseNlsLessonsForPeriods','selectedAiPeriodIds','allocationSummary','syncNlsRateFromSelection','syncNlsSelectionFromRate','syncNlsSelectionFromCount','prioritizedAiPeriods','syncAiRateFromSelection','syncAiSelectionFromRate','syncAiSelectionFromCount'].map(name=>extractNamed(target,name)).join('\n'),sliderSandbox);
sliderSandbox.syncNlsSelectionFromRate();
assert(sliderNodes['#nlsRateOut'].value.startsWith('0%'),'Canvas NLS slider must update at 0% without RangeError');
sliderNodes['#nlsRate'].value='80';sliderSandbox.syncNlsSelectionFromRate();
assert(sliderNodes['#nlsRateOut'].value.startsWith('80%'),'Canvas NLS slider must update at 80% without RangeError');
assert.equal(sliderNodes['#nlsRate'].value,'80','Canvas NLS slider must preserve the active drag value');
sliderSandbox.syncAiSelectionFromRate();
assert(sliderSandbox.aiRateOut.value.startsWith('0%'),'Canvas AI slider must update at 0% without RangeError');
sliderSandbox.aiRate.value='50';sliderSandbox.syncAiSelectionFromRate();
assert(sliderSandbox.aiRateOut.value.startsWith('50%'),'Canvas AI slider must update at 50% without RangeError');
assert(sliderSandbox.aiRateOut.value.includes('tiết PPCT'),'Canvas AI slider label must identify new-lesson periods after picker rendering');
assert.equal(sliderSandbox.aiRate.value,'50','Canvas AI slider must preserve the active drag value');
assert.equal(sliderSandbox.aiRate.max,'100','Canvas AI slider must retain the full 0–100 range');
assert.equal(sliderSandbox.aiSelectedLessonIds.size,5,'Canvas AI slider must not retain the old 12-period cap');
assert.equal(vm.runInContext('allocationTotals().totalLessons',sliderSandbox),10,'Canvas totals must include non-header review and test lessons');
assert.equal(vm.runInContext('allocationTotals().totalPeriods',sliderSandbox),10,'Canvas period totals must include non-header review and test lessons');
sliderSandbox.aiRate.value='100';sliderSandbox.syncAiSelectionFromRate();
assert.equal(sliderSandbox.aiSelectedLessonIds.size,10,'Canvas AI slider must select every available period at 100%');
sliderNodes['#nlsUnit'].value='lesson';sliderSandbox.syncNlsSelectionFromCount(3);
assert(sliderNodes['#nlsRateOut'].value.includes('bài PPCT'),'Canvas NLS count input must support the lesson unit');
sliderNodes['#aiUnit'].value='lesson';sliderSandbox.syncAiSelectionFromCount(4);
assert(sliderSandbox.aiRateOut.value.includes('bài PPCT'),'Canvas AI count input must support the lesson unit');
const calls=[];
const sandbox={console,AbortController,clearTimeout,setTimeout,fetch:async(url,init)=>{
  calls.push({url,init});
  return {ok:true,status:200,json:async()=>({ok:true,status:200,body:{candidates:[{content:{parts:[{text:'{"ok":true,"source":"canvas"}'}]}}]}})};
}};
vm.createContext(sandbox);
vm.runInContext(
  `const CANVAS_ENDPOINT=${JSON.stringify(endpoint)},GEMINI_TIMEOUT_MS=120000,DEFAULT_GEMINI_MODEL='gemini-3-flash-preview';let aborter=null;function isUserAbort(){return false};`+
  sliceFunction('fetchWithGeminiTimeout')+'\n'+sliceFunction('requestGemini')+'\n'+sliceNamedFunction('safeParseAiJson')+'\n'+sliceFunction('readGeminiResponse')+'\n'+sliceFunction('callGemini'),sandbox
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
  window:{localStorage:{getItem:key=>storage.get(key)||null,setItem:(key,value)=>storage.set(key,value),removeItem:key=>storage.delete(key)}},
  document:{querySelector:()=>null},
  notify:message=>messages.push(message),
  buildDraftPayload:()=>draftPayload,draftDefaultTitle:()=> 'Kế hoạch mẫu',
  applyDraftPayload:value=>{restored=value},setDraftStatus(){},closeSaveDraftModal(){},closeLoadDraftModal(){},
  saveAs:(blob,name)=>{download={blob,name}},
  fetch:async(url,init)=>{draftCalls.push({url,init});return {ok:true}},
};
vm.createContext(draftSandbox);
vm.runInContext(`const DRAFT_API_ENDPOINT=${JSON.stringify(draftEndpoint)};let currentDraftId=42,currentDraftTitle='';async function canvasConfirm(){return allowRestore;}`+
  "\nconst memoryStorage=Object.create(null);\n"+sliceNamedFunction('getCanvasStorage')+"\nconst canvasStorage=getCanvasStorage();\n"+sliceNamedFunction('readCanvasStorage')+"\nlet canvasDraftAccount=readCanvasStorage('canvas_xdpl_user');\n"+
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
  draftSandbox.window.localStorage.getItem=()=>{throw new Error('SecurityError')};
  draftSandbox.window.localStorage.setItem=()=>{throw new Error('QuotaExceededError')};
  assert.equal(draftSandbox.readCanvasStorage('canvas_xdpl_user'),'teacher1');
  draftSandbox.saveDraftLocally();
  assert(messages.at(-1).includes('Đã lưu bản nháp'));
  assert.equal(JSON.parse(vm.runInContext("canvasStorage.getItem('canvas_xdpl_draft')",draftSandbox)).format,'canvas-xdpl-draft');
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
const canvasComplianceSandbox={
  SUBJECTS:[['Toán học',140]],
  ppctTableFromRows(){return {columns:[],rows:[]}},
  normalizeIntegrationTable:model=>model,
  isIntegrationColumn:label=>/Mã NLS/.test(label),
  isNlsColumn:label=>/Mã NLS/.test(label),
  appendixAiCoverage(){return {covered:0,expected:0,pass:true}}
};
vm.createContext(canvasComplianceSandbox);
vm.runInContext(extractNamed(target,'parsePeriodCount')+'\n'+extractNamed(target,'calculateComplianceReport'),canvasComplianceSandbox);
const canvasNlsPeriodRows=Array.from({length:87},(_,index)=>({cells:[String(index+1),`Bài ${index+1}`,index<13?'2':index<16?'1':index===16?'111':'','Đạt',index<16?'1.1.TC1a':'-','-'],isHeader:false}));
const canvasNlsPeriodData={'1':{scheduleTable:{columns:['STT','Bài học','Số tiết','Yêu cầu cần đạt','Mã NLS','Mã AI'],rows:canvasNlsPeriodRows},schedule:[],assessments:[]}};
const canvasNlsPeriodReport=canvasComplianceSandbox.calculateComplianceReport({monHoc:'Toán học',nls:{enabled:true,unit:'period',rate:21},ai:{enabled:false}},canvasNlsPeriodData).criteria[2];
assert.equal(canvasNlsPeriodReport.pass,true,'Canvas must assess NLS period allocations by PPCT periods, not lesson count');
assert.equal(canvasNlsPeriodReport.detail,'29/140 tiết (16/87 bài), mục tiêu 29 tiết','Canvas must show the exact NLS period-unit detail');
const canvasNlsLessonReport=canvasComplianceSandbox.calculateComplianceReport({monHoc:'Toán học',nls:{enabled:true,unit:'lesson',rate:21},ai:{enabled:false}},canvasNlsPeriodData).criteria[2];
assert.equal(canvasNlsLessonReport.pass,false,'Canvas lesson-unit NLS compliance must preserve the ceil lesson target');
assert.equal(canvasNlsLessonReport.detail,'16/87 bài, mục tiêu 19 bài','Canvas must keep the exact NLS lesson-unit label');
const canvasNlsInvalidPeriodData=JSON.parse(JSON.stringify(canvasNlsPeriodData));canvasNlsInvalidPeriodData['1'].scheduleTable.rows[17].cells[4]='1.1.TC1a';
assert.equal(canvasComplianceSandbox.calculateComplianceReport({monHoc:'Toán học',nls:{enabled:true,unit:'period',rate:21},ai:{enabled:false}},canvasNlsInvalidPeriodData).criteria[2].detail,'29/140 tiết (17/87 bài), mục tiêu 29 tiết','Canvas must not invent periods for an NLS row without a valid period');
const importGuardSandbox={window:{}};
vm.createContext(importGuardSandbox);
vm.runInContext(extractNamed(target,'documentImportUnavailable'),importGuardSandbox);
assert.match(importGuardSandbox.documentImportUnavailable('PPCT.pdf'),/không thể đọc PDF trực tiếp/,'PDF imports must fail with a visible Canvas-safe explanation');
assert.match(importGuardSandbox.documentImportUnavailable('PPCT.docx'),/Thư viện đọc DOCX chưa tải được/,'DOCX imports must be guarded when their optional library is unavailable');
assert.match(importGuardSandbox.documentImportUnavailable('PPCT.xlsx'),/Thư viện đọc XLSX chưa tải được/,'XLSX imports must be guarded when their optional library is unavailable');
assert.equal(importGuardSandbox.documentImportUnavailable('PPCT.txt'),'','text imports must remain available without optional libraries');
const canvasInitCode=extractNamed(target,'initApp');
assert(!/mammoth|XLSX|pdfjsLib|documentImportUnavailable/.test(canvasInitCode),'initial Canvas UI must not depend on optional document-import libraries');
const pickerSandbox={
  foldText(s){return String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toUpperCase().replace(/\s+/g,' ').trim()},
  cleanLessonDescription(s){return String(s||'')},
  selectedAiLessons(){return []},
  getSharedSgkLessonKnowledge(){return null},
  SUBJECTS:[['Toán học',140],['Ngữ văn',140],['Tiếng Anh (Ngoại ngữ 1)',105],['Khoa học tự nhiên',140],['Tin học',35],['Giáo dục công dân',35]],
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
assert.ok(firstTwo.some(w=>Number(w)<19)&&firstTwo.some(w=>Number(w)>=19),'AI suggestions must mix both semesters');
console.log('canvas responsive layout and multi-subject picker: PASS');
