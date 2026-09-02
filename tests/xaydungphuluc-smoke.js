/* Smoke test for the standalone THCS Appendix Builder. Run: node tests/xaydungphuluc-smoke.js */
const fs=require('fs'),path=require('path'),assert=require('assert'),vm=require('vm');
const {getCleanOfficialYccd,generatePedagogicalOutcome,KHBD_YCCD}=require('../js/khbd-yccd.js');
const {recommendOfficialStandards}=require('../js/khbd-standards.js');
async function run(){
const file=path.join(__dirname,'..','xaydungphuluc.html');
const html=fs.readFileSync(file,'utf8');
const draftApi=fs.readFileSync(path.join(__dirname,'..','api','user_phuluc_draft.php'),'utf8');
function has(value,label=value){assert(html.includes(value),`Missing: ${label}`)}
assert(/^<!doctype html>/i.test(html),'not a standalone HTML document');
['tailwindcss','mammoth','pdf.js','xlsx.full.min.js','docx@8.5.0','JSZip','FileSaver'].forEach(x=>has(x));
['Lớp 6','Lớp 7','Lớp 8','Lớp 9','Toán học','Ngữ văn','Khoa học tự nhiên','Giáo dục địa phương'].forEach(has);
['js/security-guard.js','access-control.js','LEGACY_API_KEY_STORAGE_KEYS','khbd_user_gemini_keys_default','khbd_gemini_api_keys','gemini_api_keys','xdpl_gemini_api_keys','global_gemini_keys','clearLegacyApiKeyStorage','ensureKeysLoaded','syncUserKeysPromise','saveKeys','checkKeys','429','403','mistralKeys','mistralKeyInput','mistral_keys','syncUserKeysFromServer','api/user_gemini_keys.php','credentials:\'include\'','cache:\'no-store\''].forEach(has);
['saveDraftToServer','loadDraftFromServer','buildDraftPayload','applyDraftPayload','openSaveDraftModal','openLoadDraftModal','fetchAndRenderDraftList','buildDraftSummary','loadDraftById','deleteDraftFromServer','api/user_phuluc_draft.php','💾 Lưu lên CSDL','📂 Tải từ CSDL','id="draftStatus"','id="saveDraftModal"','id="loadDraftModal"','id="draftTitleInput"','id="draftListContainer"','aiSelectedLessonIds','sgkCompactContext','sgkKnowledgeBase'].forEach(has);
['user_phuluc_drafts','LONGTEXT','$_SESSION[\'user_id\']','DROP INDEX uniq_user_phuluc_draft_user','idx_user_phuluc_drafts_user','idx_user_phuluc_drafts_mon_lop','action===\'list\'','action===\'delete\'','draft_data','updated_at','save_mode'].forEach(value=>assert(draftApi.includes(value),`draft API missing ${value}`));
assert(!draftApi.includes('UNIQUE KEY uniq_user_phuluc_draft_user'),'draft API must not create a single-draft unique key');
assert(!/localStorage\.setItem\([^\n]*(?:gemini|mistral|api_keys)/i.test(html.replace(/localStorage\.setItem\('khbd_gemini_model',[\s\S]*?\);/g,'')),'API keys must never be persisted in localStorage');
assert(!/sessionStorage\.(?:setItem|getItem)/i.test(html),'API keys must never use sessionStorage');
assert(!html.includes('readStoredKeyList')&&!html.includes('cacheUserKeys'),'legacy API-key cache helpers must be removed');
['Đang đọc tệp dữ liệu PPCT…','Đang gửi ngữ cảnh lên AI (Gemini/Mistral)…','AI đang phân tích và trích xuất bảng PPCT…','Đang khởi tạo Bảng PPCT 8 cột…','Đã nhận diện hoàn tất bảng PPCT!','await ensureKeysLoaded()'].forEach(has);
['nlsRate','nlsDensity','aiRate','aiDensity','NLS và AI ĐỘC LẬP','1–2 mã/bài','2–3 mã/bài','3–4 mã/bài'].forEach(has);
['appendixPrompt','NGUYÊN TẮC BẢO TOÀN PPCT NGUỒN','giữ nguyên 100%','Tuần 1 đến Tuần 35','Phụ lục 1','Phụ lục 2','Phụ lục 3','Công văn 5512','TT 38/2021','TT 14/2020'].forEach(has);
['parseFiles','extractPpctRows','extractDocxTables','ingestSourceTables','preserveSourceSchedule','mammoth.extractRawText','pdfjsLib','XLSX.read','generateSelected','exportDocx','contenteditable','exportAll'].forEach(has);
has('max-w-[98%]');
has('min-width:900px');
has('overflow-x-auto');
has('id="aiLessonPickerCard" class="card p-5 w-full"');
has('id="aiLessonPicker" class="w-full mt-3 overflow-x-auto"');
assert(!html.includes('id="aiLessonPicker" class="grid md:grid-cols-2 gap-2 mt-3"'),'AI picker must not use a two-column grid');
has('id="generateAll" class="btn primary" onclick="generateSelected(\'all\')"');
assert(!html.includes('word-break: break-word'),'table text must not be forcibly broken');
['js/khbd-standards.js','KHBD_STANDARDS','recommendOfficialStandards','getOfficialYccd','getStandardCompetenciesForLesson','normalizeIntegrationTable','stageFiles','recognizeStagedPpct','readStagedSgk','🔍 Nhận diện PPCT','📖 Đọc SGK','Đã hiểu thông tin SGK','sgkKnowledgeBase'].forEach(has);
['getCleanOfficialYccd','densityLowerBound','cleanAppendixOutcome','formatOutcomeLines','formatTietCT','formatWeek','PageOrientation.LANDSCAPE','width:16838,height:11906','top:1134,right:1134,bottom:1134,left:1134','LineRuleType.AUTO','line:312,lineRule:LineRuleType.AUTO','size:26'].forEach(has);
['progressContainer','progressPercent','progressBarInner','setProgress','hideProgress','progressTimerId','SCHEDULE_COLUMNS','PLAN_COLUMNS','CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM','organizationHeading'].forEach(has);
assert(!html.includes('UBND XÃ/PHƯỜNG ...<br>'),'Appendix 1 HTML heading must not render a commune/ward line');
assert(!html.includes('UBND XÃ/PHƯỜNG ...\\n${school.value'),'Appendix 1 DOCX heading must not render a commune/ward line');
has('onclick="hideProgress()"');
has('setTimeout(()=>hideProgress(),hideMs??1500)');
has('progress-done');
has('class="text-xs opacity-75 hover:opacity-100 ml-2"');
['APPENDIX_1_COLUMNS','Bài học','Số tiết','Yêu cầu cần đạt','Tiết CT','Tuần','Thiết bị dạy học (*)','Địa điểm dạy học (**)','Mã NLS & AI (CV 3456 & QĐ 2422)'].forEach(has);
has('(*) Tên thiết bị/học liệu số theo Thông tư 38/2021/TT-BGDĐT');
has('(**) Lớp học/Phòng học bộ môn theo Thông tư 14/2020/TT-BGDĐT');
has('GIÁO VIÊN (Ký và ghi rõ họ tên)');
has('TỔ TRƯỞNG DUYỆT (Ký và ghi rõ họ tên)');
has('isHeader');
has('tietCT');
has('PPCT_COLUMN_WIDTHS');
assert(!html.includes('Phương pháp & kĩ thuật dạy học'),'legacy methods section must be removed');
has('tuyệt đối không dùng Huyện, Phòng GD&ĐT hoặc Phòng Giáo dục','two-tier local-government safeguard');

const script=html.match(/<script>\s*(\/\* Client-side[\s\S]*?)<\/script>/);
assert(script,'inline application script missing');
const sandbox={
  window:{},
  KHBD_YCCD:{toan:{'6':Array.from({length:43},(_,i)=>({lesson:`Bài ${i+1}. Toán 6`})),'7':Array.from({length:37},(_,i)=>({lesson:`Bài ${i+1}. Toán 7`})),'8':Array.from({length:39},(_,i)=>({lesson:`Bài ${i+1}. Toán 8`})),'9':Array.from({length:32},(_,i)=>({lesson:`Bài ${i+1}. Toán 9`}))}},
  document:{querySelector(){return null},querySelectorAll(){return []},addEventListener(){},createElement(){return {className:'',textContent:'',append(){},remove(){}}}},
  localStorage:{getItem(){return null},setItem(){}},
  console,
  getCleanOfficialYccd,generatePedagogicalOutcome,
  JSON,Math,Set,Array,String,Number,Boolean,RegExp,Date,Error,Promise,Map,AbortController,setTimeout,clearTimeout,
  DOMParser:class{parseFromString(){return {querySelectorAll(){return []}}}},
};
vm.createContext(sandbox);
try{vm.runInContext(script[1].replace(/document\.addEventListener\('DOMContentLoaded'[\s\S]*\);\s*$/,''),sandbox);}
catch(e){assert.fail('inline JavaScript failed to parse: '+e.message)}
assert.equal(typeof sandbox.extractPpctRows,'function','extractPpctRows must be defined');
assert.equal(sandbox.htmlMultiline('STT'),'STT','ordinary HTML table labels must not gain a bullet');
assert.equal(sandbox.htmlMultiline('4'),'4','ordinary HTML table values must not gain a bullet');
assert.equal(sandbox.outcomeHtml('Nhận biết được số tự nhiên').startsWith('- '),true,'only outcomes must retain pedagogical bullets');
assert(html.includes('const outcomeCell=')&&!html.includes('children:formatOutcomeLines(integrationText(text))'),'DOCX must use a dedicated outcome cell instead of formatting every cell as an outcome');
assert.equal(typeof sandbox.calculateComplianceReport,'function','compliance calculation must be defined');
assert.equal(typeof sandbox.renderComplianceCard,'function','compliance summary renderer must be defined');
assert(html.includes('id="complianceSummaryCard"')&&html.includes('id="complianceModal"'),'compliance card and modal must be present');
const incompleteCompliance=vm.runInContext("calculateComplianceReport({monHoc:'Toán học',nls:{enabled:false,rate:0},ai:{selectedPeriods:[]}}, {'1':{schedule:[],assessments:[]}})",sandbox);
assert.equal(incompleteCompliance.isCompliant,false,'incomplete source data must never be reported as 100% compliant');
assert.equal(typeof sandbox.recognizePpctWithAi,'function','stage-one PPCT recognizer must be defined');
assert.equal(typeof sandbox.callAiJson,'function','AI provider fallback must be defined');
vm.runInContext("getConfig=()=>({lop:'6',monHoc:'Toán học',namHoc:'2026-2027'});sourcePpctRows=[{lesson:'Bài nháp'}];sourcePpctTable={columns:['Bài học'],rows:[]};aiSelectedLessonIds=new Set(['ppct:0:period:1']);sgkCompactContext='Ngữ cảnh SGK';sgkKnowledgeBase='{}';results={'1':{title:'PL1'},'2':{title:'PL2'},'3':{title:'PL3'}}",sandbox);
const draftPayload=vm.runInContext('buildDraftPayload()',sandbox);
assert.deepEqual(JSON.parse(JSON.stringify(draftPayload.config)),{lop:'6',monHoc:'Toán học',namHoc:'2026-2027'},'draft payload must retain pedagogical configuration');
assert.deepEqual(Array.from(draftPayload.aiSelectedLessonIds),['ppct:0:period:1'],'draft payload must retain selected AI periods');
assert.equal(draftPayload.sgkCompactContext,'Ngữ cảnh SGK','draft payload must retain compact SGK context');
assert.deepEqual(Object.keys(draftPayload.results).sort(),['1','2','3'],'draft payload must retain all appendix results');
const bai14Yccd=getCleanOfficialYccd({subjectId:'toan',grade:'6',topic:'Bài 14. Phép cộng và phép trừ số nguyên'});
assert(/phép cộng|số nguyên/i.test(bai14Yccd),'clean YCCĐ must match Bài 14 by its lesson number');
assert(!/ước chung lớn nhất|bội chung nhỏ nhất/i.test(bai14Yccd),'Bài 14 YCCĐ must not leak ƯCLN/BCNN from another lesson');
assert(!/nguồn bắt buộc|căn cứ|bài sgk|nội dung ctgdpt/i.test(bai14Yccd),'clean YCCĐ must contain outcomes only, without metadata');
const bai5Yccd=getCleanOfficialYccd({subjectId:'toan',grade:'6',topic:'Bài 5: Phép nhân và phép chia số tự nhiên'});
assert(/phép.*nhân|phép.*chia|luỹ thừa/i.test(bai5Yccd),'Bài 5 must receive the arithmetic YCCĐ');
assert(!/chữ số la mã|thuật ngữ tập hợp/i.test(bai5Yccd),'Bài 5 must not receive the Tập hợp YCCĐ');
const bai1Yccd=getCleanOfficialYccd({subjectId:'toan',grade:'6',topic:'Bài 1. Tập hợp'});
const bai2Yccd=getCleanOfficialYccd({subjectId:'toan',grade:'6',topic:'Bài 2. Cách ghi số tự nhiên'});
const bai3Yccd=getCleanOfficialYccd({subjectId:'toan',grade:'6',topic:'Bài 3. Thứ tự trong tập hợp các số tự nhiên'});
const bai4Yccd=getCleanOfficialYccd({subjectId:'toan',grade:'6',topic:'Bài 4. Phép cộng và phép trừ số tự nhiên'});
assert(/tập hợp|phần tử/i.test(bai1Yccd)&&!/la mã|hệ thập phân|so sánh/i.test(bai1Yccd),'Bài 1 must only retain its tập hợp YCCĐ');
assert(/hệ thập phân|la mã/i.test(bai2Yccd)&&!/phần tử thuộc/i.test(bai2Yccd),'Bài 2 must only retain number notation YCCĐ');
assert(/thứ tự|so sánh/i.test(bai3Yccd)&&!/la mã|hệ thập phân/i.test(bai3Yccd),'Bài 3 must only retain order YCCĐ');
assert(/phép cộng|phép trừ/i.test(bai4Yccd)&&!/luỹ thừa|phép chia/i.test(bai4Yccd),'Bài 4 must not inherit multiplication, division, or power YCCĐ');
assert.notEqual(bai1Yccd,bai2Yccd,'adjacent lessons must not share a topic-wide YCCĐ block');
const practiceYccd=getCleanOfficialYccd({subjectId:'toan',grade:'6',topic:'Luyện tập chung',contextTopic:'Bài 5. Phép nhân và phép chia số tự nhiên'});
assert(/phép.*nhân|phép.*chia|luỹ thừa/i.test(practiceYccd),'practice lessons must inherit the preceding topic context');
assert(!/chia hết|ước chung|bội chung|số nguyên tố/i.test(practiceYccd),'practice after Bài 5 must not inherit divisibility or factor outcomes from later Chapter I lessons');
const chapterOneReview=getCleanOfficialYccd({subjectId:'toan',grade:'6',topic:'Bài tập cuối chương I',chapterTopic:'CHƯƠNG I. TẬP HỢP SỐ TỰ NHIÊN'});
assert(/số tự nhiên|tập hợp|phép tính|chia hết|ước/i.test(chapterOneReview),'chapter I review must remain in the natural-number domain');
assert(!/điểm|đường thẳng|tia|góc|tam giác|phân số/i.test(chapterOneReview),'chapter I review must never leak geometry or fractions');
const chapterOnePractice=getCleanOfficialYccd({subjectId:'toan',grade:'6',topic:'Luyện tập chung',chapterTopic:'CHƯƠNG I. TẬP HỢP SỐ TỰ NHIÊN',contextTopic:'Bài 5. Phép nhân và phép chia số tự nhiên'});
assert(/số tự nhiên|phép tính|chia hết/i.test(chapterOnePractice),'chapter I practice must stay within its chapter domain');
assert(!/chia hết|ước chung|bội chung|số nguyên tố/i.test(chapterOnePractice),'chapter I practice after Bài 5 must prioritize its preceding calculation topic');
assert(/Củng cố, hệ thống hóa/i.test(generatePedagogicalOutcome('Luyện tập chung','Toán học','6')),'practice fallback must use the pedagogical review frame');
assert(/Vận dụng kiến thức liên môn/i.test(generatePedagogicalOutcome('Chuyên đề STEM mô hình toán học','Toán học','6')),'STEM fallback must use the pedagogical project frame');
['DOCX_WIDTHS','appendixOne:[5,22,6,47,20]','appendixThree:[22,6,8,6,18,16,24]','tableHeader:true,cantSplit:true','contenteditable="true" onblur="editAppendixOneOutcome','sgkOutcomeForLesson','generatePedagogicalOutcome'].forEach(has);
['selectModel','gemini-3.7-flash','gemini-3.6-flash','gemini-3.5-flash','gemini-3.5-flash-lite','gemini-2.5-flash','gemini-2.5-flash-lite','gemini-3-flash-preview','getSelectedModel','onModelChange','khbd_gemini_model','thinkingConfig:{thinkingBudget:0}','api/khbd_gemini.php','GEMINI_FALLBACK_MODEL','fetchWithGeminiTimeout','Không thể trích xuất dòng PPCT nào từ tệp','Tệp không có văn bản hoặc là PDF scan cần OCR.'].forEach(has);
assert(html.includes('Giai đoạn 1 chỉ nhận diện PPCT'),'upload flow must document stage separation');
assert(html.includes('AI chưa khả dụng')&&html.includes('đang dùng bảng PPCT đọc trực tiếp từ tệp'),'upload must provide a visible parser fallback');
assert(html.includes('await recognizePpctWithAi(recognitionInput)'),'PPCT upload must invoke recognition after structured extraction');
assert(vm.runInContext("ppctRecognitionPrompt('Bài 1').includes('Không suy diễn Yêu cầu cần đạt')",sandbox),'stage-one prompt must explicitly forbid outcome generation');
assert(!vm.runInContext("ppctRecognitionPrompt('Bài 1').includes('schema {title')",sandbox),'stage-one prompt must not use an appendix-generation schema');
const recognizedRows=vm.runInContext("normalizeRecognizedPpct({ppct:[{lesson:'HỌC KÌ I',isHeader:true},{lesson:'Bài 1. Tập hợp',periods:'1, 2',tietCT:'1-2',week:'Tuần 1',devices:'Máy chiếu',location:'Lớp học'}]})",sandbox);
assert.equal(recognizedRows.length,2,'recognizer must retain PPCT headers and lesson rows');
assert.equal(recognizedRows[1].periods,'2','recognizer must normalize listed periods for picker checkboxes');
const recognizedVariants=vm.runInContext("normalizeRecognizedPpct([{ten_bai:'HỌC KÌ II'},{bai_hoc:'Bài biến thể',so_tiet:'2',tiet_ct:'3-4',tuan:'Tuần 2',thiet_bi:'Máy chiếu',dia_diem:'Lớp học'}])",sandbox);
assert.equal(recognizedVariants.length,2,'recognizer must accept a direct JSON array');
assert.equal(recognizedVariants[0].isHeader,true,'recognizer must infer PPCT headers');
assert.deepEqual(Array.from(vm.runInContext("normalizeRecognizedPpct({schedule:[{ten_bai:'Bài wrapped',so_tiet:'1',tiet_ct:'5'}]})",sandbox)),[{lesson:'Bài wrapped',periods:'1',tietCT:'5',week:'',devices:'',location:'',integration:'',isHeader:false}],'recognizer must accept wrapped Vietnamese snake_case rows');
const recognizedTable=vm.runInContext("ppctTableFromRows(normalizeRecognizedPpct({items:[{lesson:'Bài đồng bộ',periods:'1',tietCT:'1'}]}))",sandbox);
assert.equal(recognizedTable.rows[0].cells[0],'Bài đồng bộ','AI rows must synchronize into the PPCT table model');
assert(html.includes('const recognitionInput=tableText||text'),'table uploads must prefer TSV input for recognition');
assert(html.includes("results['1']=normalizeAppendix(fallback('1',config),'1',config)")&&html.includes('activeTab=\'1\';renderPreview()'),'recognized PPCT must render immediately in the preview');
[['(2 tiết)',2],['3 tiết',3],['[3 tiết]',3],['4 tiết/tuần',4],['1-2',2],['1, 2',2],['Tiết 1-3',3],['tiết 6 đến 8',3],['hai tiết',2],['bốn tiết',4]].forEach(([value,expected])=>assert.equal(vm.runInContext(`parsePeriodCount(${JSON.stringify(value)})`,sandbox),expected,`must parse ${value}`));
assert.equal(vm.runInContext("parsePeriodCount('3-1')",sandbox),null,'reversed ranges must be rejected');
const sample=[
  'Bài học\tSố tiết\tTiết CT\tTuần\tThiết bị dạy học (*)\tĐịa điểm dạy học (**)',
  'HỌC KÌ I',
  '1. SỐ HỌC 6',
  'CHƯƠNG I. TẬP HỢP SỐ TỰ NHIÊN (13 tiết)',
  'Tập hợp\t1\t1\t1\tTi vi, thước\tLớp học',
  'Bài 2. Quan hệ giữa phần tử và tập hợp\t2\t2\t1\tBảng phụ\tPhòng bộ môn',
  'HỌC KÌ II'
].join('\n');
const rows=sandbox.extractPpctRows(sample);
assert(rows.some(r=>r.isHeader&&r.lesson.includes('HỌC KÌ I')),'must keep HỌC KÌ I spanning header');
assert(rows.some(r=>r.isHeader&&r.lesson.includes('CHƯƠNG I')),'must keep CHƯƠNG spanning header');
const lesson=rows.find(r=>r.lesson.includes('Tập hợp')&&!r.isHeader);
assert(lesson,'must parse lesson row');
assert.equal(String(lesson.periods),'1');
assert.equal(String(lesson.tietCT),'1');
assert.equal(String(lesson.week),'1');
assert.equal(lesson.devices,'Ti vi, thước');
assert.equal(lesson.location,'Lớp học');
assert(html.includes('✓'),'complete-state checkmark missing');
assert(sandbox.setProgress.toString().includes('safe>=100')||sandbox.setProgress.toString().includes('safe >= 100'),'setProgress must stop spinner at 100%');
assert(typeof sandbox.hideProgress==='function','hideProgress must be defined');
assert.equal(typeof sandbox.extractDocxTables,'function');
assert.equal(typeof sandbox.ingestSourceTables,'function');
['aiLessonPickerCard','aiLessonPicker','aiSelectionCount','toggleAiLesson','toggleAiLessonRow','suggestAiLessons','AI_SELECTION_LIMIT','aiPeriodCandidates','updatePpctLessonPeriods','syncAiSelectionFromRate','validPeriodCount','compactSgkText','isSgkFile','looksLikeSgkText','selectedAiLessons','sgkCompactContext'].forEach(has);
['ppctFiles','sgkFiles',"stageFiles(this.files,'ppct')","stageFiles(this.files,'sgk')",'Nhận diện PPCT','Đọc SGK','recognizeStagedPpct','readStagedSgk','loadDefaultPpctStructure','clearAiLessons','Bỏ chọn tất cả','Đã chọn: 0/12 tiết AI'].forEach(has);
['recalculatePpctSequences','periodsPerWeekForSubject','onclick="recalculatePpctSequences()"','🔄 Tính lại Tiết CT &amp; Tuần tự động'].forEach(has);
['schedulePreviewUpdate','officialYccdCache','standardCompetenciesCache','periodsByLesson'].forEach(has);
assert(!html.includes('id="aiLessonPickerCard" class="card p-5 hidden"'),'AI lesson picker must be visible on initial load');
['sourcePpctRowsForAppendixOne','appendixOneTable','appendixOneFallbackOutcome','outcomes (Yêu cầu cần đạt) chuẩn Chương trình GDPT 2018'].forEach(has);
['DANH SÁCH BÀI HỌC BẮT BUỘC','NGỮ CẢNH CTGDPT 2018 THEO TỪNG BÀI','ghép 1-kèm-1 theo index và lesson','classCount','studentCount','teacherCount'].forEach(has);
has('slice(0,aiSelectionLimit())','AI suggestion must cap the selection at 12 periods');
has(':period:','AI selections must use stable per-period identifiers');
['NLS: mã - mô tả','AI TUYỆT ĐỐI chỉ được xuất','[AI: mã - mô tả]','0070C0','7030A0','nls-code','ai-code','integrationHtml','integrationCell'].forEach(has);
assert.equal(typeof sandbox.compactSgkText,'function','compact SGK index must be defined');
const compact=vm.runInContext("compactSgkText('BÀI 1. Tập hợp\\nMục tiêu cần đạt: nhận biết tập hợp.\\nNội dung giới thiệu dài không giữ lại.\\nHoạt động khám phá: lập tập hợp.\\nLuyện tập: viết tập hợp.')",sandbox);
assert(compact.includes('BÀI 1. Tập hợp')&&compact.includes('Mục tiêu cần đạt')&&compact.includes('Hoạt động khám phá'),'SGK compact index must retain lesson, objective and activity');
assert(!compact.includes('Nội dung giới thiệu dài'),'SGK compact index must omit unrelated prose');
const compactTechnology=vm.runInContext("compactSgkText('MỤC LỤC\\nChương I. Hình học\\nBài 1. Tam giác\\nThực hành với phần mềm GeoGebra\\nĐoạn văn kể chuyện không liên quan.')",sandbox);
assert(compactTechnology.includes('MỤC LỤC')&&compactTechnology.includes('Chương I')&&compactTechnology.includes('GeoGebra'),'SGK compact index must retain table of contents, chapter and digital practice');
assert(vm.runInContext("looksLikeSgkText('Bài 1. Tập hợp. Mục tiêu cần đạt. Hoạt động khám phá.',[])",sandbox),'content signature must recognize SGK even when its filename is generic');
const codesFor=topic=>recommendOfficialStandards('digital',{grade:6,topic,vision:'Hoạt động thực hành với công nghệ số',subjectName:'Toán học',facilities:{devices:true},aiOn:false}).map(item=>item.officialCode);
assert(codesFor('Bài toán về số nguyên và phân số').some(code=>code.startsWith('5.3.TC1a')),'algebra must prioritize 5.3.TC1a');
assert(codesFor('Tam giác, đo góc và vẽ hình với GeoGebra').some(code=>code.startsWith('3.1.TC1a')),'geometry must prioritize 3.1.TC1a');
assert(codesFor('Bảng số liệu và biểu đồ cột').some(code=>code.startsWith('1.1.TC1a')||code.startsWith('1.2.TC1a')),'statistics must prioritize data standards');
assert.equal(vm.runInContext("selectedIntegration('[NLS: 1.1.6a - Khai thác học liệu.] [AI: 6.A1.1 - Hỗ trợ bài tập.]',false,0,{ai:{enabled:true},lop:'6'})",sandbox),'[NLS: 1.1.6a - Khai thác học liệu.]','unselected lesson must not retain AI integration');
assert(vm.runInContext("selectedIntegration('[NLS: 1.1.6a - Khai thác học liệu.]',true,0,{ai:{enabled:true},lop:'6'})",sandbox).includes('[AI:'),'selected lesson must receive an AI integration when AI is enabled');
assert(vm.runInContext("integrationHtml('[NLS: 1.1.6a - Khai thác học liệu.] [AI: 6.A1.1 - Hỗ trợ bài tập.]')",sandbox).includes('nls-code')&&vm.runInContext("integrationHtml('[NLS: 1.1.6a - Khai thác học liệu.] [AI: 6.A1.1 - Hỗ trợ bài tập.]')",sandbox).includes('ai-code'),'preview must distinguish NLS and AI integration colors');
assert.equal(vm.runInContext("integrationText([{text:'[NLS: 1.1.TC1a - Học liệu số]',ai:false},{label:'[AI: 6.A1.1 - Hỗ trợ]',ai:true}])",sandbox),'[NLS: 1.1.TC1a - Học liệu số]\n[AI: 6.A1.1 - Hỗ trợ]','integration objects must be converted to text before rendering');
assert(!vm.runInContext("selectedIntegration([{text:'[NLS: 1.1.TC1a - Học liệu số]',ai:false}],false,0,{ai:{enabled:false},lop:'6'}).includes('[object Object]')",sandbox),'selected integration must never stringify raw objects');
assert.equal(vm.runInContext("cleanAppendixOutcome('- Phân tích được nhân vật và chi tiết tiêu biểu trong truyện.', 'Bài 3. Nhân vật trong truyện', {lop:'6',monHoc:'Ngữ văn',sgkContext:''})",sandbox),'- Phân tích được nhân vật và chi tiết tiêu biểu trong truyện.','a valid AI outcome for a non-math lesson must be preserved');
assert(vm.runInContext("appendixPrompt('1',{lop:'6',monHoc:'Ngữ văn',ai:{enabled:false,selectedPeriods:[]},nls:{}}).includes('DANH SÁCH BÀI HỌC BẮT BUỘC')",sandbox),'Appendix 1 prompt must transmit the ordered PPCT lesson list');
assert.equal(vm.runInContext("formatOutcomeLines('Mô tả được nội dung., Nhận biết được khái niệm; Vận dụng được kiến thức.')",sandbox),'- Mô tả được nội dung.\n- Nhận biết được khái niệm\n- Vận dụng được kiến thức.','outcomes must normalize compact outcomes into separate bullets');
const toan6Overrides=KHBD_YCCD.toan['6'];
assert.equal(toan6Overrides.length,43,'Toán 6 must contain all 43 lesson rows');
assert(toan6Overrides.every(row=>row.items.length>0),'every Toán 6 lesson must have a focused YCCĐ');
assert.notDeepEqual(toan6Overrides[12].items,toan6Overrides[13].items,'adjacent Toán 6 lessons must not share a topic-wide YCCĐ block');
assert.equal(vm.runInContext("formatTietCT('8 9')",sandbox),'8, 9','Tiết CT must use comma-separated integers');
assert.equal(vm.runInContext("formatWeek('Tuần 3 3')",sandbox),'3','week display must remove duplicate weeks');
const scopedIntegration=vm.runInContext("selectedIntegration('[NLS: 1.1.6a - Khai thác học liệu.] [AI: 6.A1.1 - Hỗ trợ.] Áp dụng: tiết 1, 2. Áp dụng: tiết 1, 2.',[1,2],0,{ai:{enabled:true},lop:'6'})",sandbox);
assert.equal((scopedIntegration.match(/Áp dụng:/g)||[]).length,1,'selected AI integration must keep exactly one scope');
assert(scopedIntegration.includes('[NLS:')&&scopedIntegration.includes('[AI:'),'selected AI integration must retain NLS alongside AI');

const zlib=require('zlib');
function zipRead(buf,entryName){
  const nameBuf=Buffer.from(entryName);
  let idx=0;
  while((idx=buf.indexOf(nameBuf,idx))!==-1){
    const header=idx-30;
    if(header>=0&&buf.readUInt32LE(header)===0x04034b50){
      const method=buf.readUInt16LE(header+8);
      const compSize=buf.readUInt32LE(header+18);
      const extraLen=buf.readUInt16LE(header+28);
      const data=buf.slice(idx+entryName.length+extraLen, idx+entryName.length+extraLen+compSize);
      if(method===0)return data.toString('utf8');
      if(method===8)return zlib.inflateRawSync(data).toString('utf8');
    }
    idx+=1;
  }
  throw new Error('missing zip entry '+entryName);
}
function xmlTablesToHtml(xml){
  function cellText(cell){return (cell.match(/<w:t[^>]*>([\s\S]*?)<\/w:t>/g)||[]).map(t=>t.replace(/<[^>]+>/g,'')).join('').replace(/\s+/g,' ').trim()}
  const chunks=[];
  xml.replace(/<w:tbl\b[\s\S]*?<\/w:tbl>/g,tbl=>{
    let h='<table>';
    tbl.replace(/<w:tr\b[\s\S]*?<\/w:tr>/g,tr=>{
      h+='<tr>';
      tr.replace(/<w:tc\b[\s\S]*?<\/w:tc>/g,tc=>{h+=`<td>${cellText(tc)}</td>`});
      h+='</tr>';
    });
    chunks.push(h+'</table>');
    return '';
  });
  return chunks.join('');
}
const sampleDocx=path.join(__dirname,'..','GIAO AN','XAYDUNGPHULUC','Phụ lục 1 - Lớp 6 - Toán.docx');
assert(fs.existsSync(sampleDocx),'sample PPCT docx missing');
const ingested=sandbox.ingestSourceTables(sandbox.extractDocxTables(xmlTablesToHtml(zipRead(fs.readFileSync(sampleDocx),'word/document.xml'))));
assert(ingested.ppct.length>=2,'sample docx must yield PPCT rows');
assert(!ingested.ppct.some(r=>/TRƯỜNG THCS|CỘNG HÒA XÃ HỘI|UBND/i.test(r.lesson||'')),'administrative header must not leak into PPCT rows');
assert(ingested.ppct.some(r=>/Bài 1\. Tập hợp/.test(r.lesson)),'must recognize Bài 1. Tập hợp');
assert(ingested.ppct.some(r=>/Bài 2\. Cách ghi số tự nhiên/.test(r.lesson)),'must recognize Bài 2. Cách ghi số tự nhiên');
const bai1=ingested.ppct.find(r=>/Bài 1\. Tập hợp/.test(r.lesson));
assert.equal(String(bai1.periods),'1');
assert.equal(String(bai1.tietCT),'1');
const arbitrary=sandbox.sourcePpctFromTable([
  ['STT','Bài học','Số tiết','Yêu cầu cần đạt','Thiết bị','Địa điểm'],
  ['HỌC KÌ I','','','','',''],
  ['1','Bài 1. Tập hợp','1','Nhận biết tập hợp','Bảng phụ','Lớp học']
]);
assert.deepEqual(Array.from(arbitrary.columns),['STT','Bài học','Số tiết','Yêu cầu cần đạt','Thiết bị','Địa điểm'],'must preserve every source column verbatim');
const preserved=vm.runInContext(`sourcePpctTable=${JSON.stringify(arbitrary)};preservedPpctTable([{lesson:'Bài 1. Tập hợp',integration:'[1.1.6a] Khai thác học liệu số.'}],{lop:'6',nls:{enabled:true,rate:50,density:'1-2'},ai:{enabled:false,rate:0,density:'1-2'}})`,sandbox);
assert.equal(preserved.columns.length,7,'must add exactly one NLS/AI column');
assert.equal(preserved.columns[6],'Mã NLS & AI (CV 3456 & QĐ 2422)');
assert.equal(preserved.rows[1].cells[3],'Nhận biết tập hợp','must retain arbitrary source data');
const duplicateIntegration=vm.runInContext(`normalizeIntegrationTable({columns:['Bài học','Mã NLS','NLS & AI'],lessonIndex:0,rows:[{cells:['Bài 1','[NLS: 1.1.TC1a]','[AI: 6.A1.1]'],isHeader:false}]})`,sandbox);
assert.equal(duplicateIntegration.columns.filter(column=>/Mã NLS|NLS\s*&\s*AI|Tích hợp/i.test(column)).length,1,'adapter must collapse duplicate integration columns');
assert.equal(duplicateIntegration.rows[0].cells.length,2,'adapter must keep one integration cell');
assert(/\.TC1a|\.TC2a/.test('1.1.TC1a 1.1.TC2a'),'digital standards must use TC1a/TC2a');
assert(/^[6-9]\.A/.test('6.A1.1'),'AI standards must be grade-specific');
const appendixOne=vm.runInContext(`sourcePpctTable=${JSON.stringify({columns:['Bài học','Số tiết','Tiết CT','Tuần','Thiết bị','Địa điểm'],lessonIndex:0,rows:[{cells:['HỌC KÌ I','','','','',''],isHeader:true},{cells:['Bài 1. Tập hợp','1','1','1','Bảng phụ','Lớp học'],isHeader:false}]})};aiSelectedLessonIds=new Set(['source:1:period:1']);appendixOneTable([{lesson:'Bài 1. Tập hợp',periods:'99',outcomes:'Nhận biết và mô tả được tập hợp.',integration:'[NLS: 1.1.6a - Khai thác học liệu.] [AI: 6.A1.1 - Hỗ trợ bài tập.]'}],{lop:'6',monHoc:'Toán học',ai:{enabled:true}})`,sandbox);
assert.deepEqual(Array.from(appendixOne.columns),['STT','Bài học','Số tiết','Yêu cầu cần đạt','Mã NLS & AI (CV 3456 & QĐ 2422)'],'PL1 must use its five-column form');
assert.equal(appendixOne.rows[1].cells[2],'1','PL1 must retain periods from PL3, not generated schedule values');
assert.equal(appendixOne.rows[1].cells[3],'- Nhận biết và mô tả được tập hợp.','PL1 must use the AI-generated outcome as a bullet');
assert(appendixOne.rows[1].cells[4].includes('[AI:'),'selected PL3 lesson must retain its AI code in PL1');
assert(appendixOne.rows[1].cells[4].includes('Áp dụng: tiết 1'),'partial selected period must be scoped in PL1 AI integration');
sandbox.getCleanOfficialYccd=()=>'- Thực hiện được phép cộng và phép trừ số nguyên.';
const cleanAppendixOne=vm.runInContext(`sourcePpctTable={columns:['Bài học','Số tiết'],lessonIndex:0,rows:[{cells:['Bài 14. Phép cộng và phép trừ số nguyên','1'],isHeader:false}]};appendixOneTable([{lesson:'Bài 14. Phép cộng và phép trừ số nguyên',outcomes:'Nguồn bắt buộc: CTGDPT 2018. Bài SGK: Bài 14.'}],{lop:'6',monHoc:'Toán học',ai:{enabled:false}})`,sandbox);
assert.equal(cleanAppendixOne.rows[0].cells[3],'- Thực hiện được phép cộng và phép trừ số nguyên.','PL1 must replace metadata outcomes with clean YCCĐ');
const chapterScopedReview=vm.runInContext(`sourcePpctTable={columns:['Bài học','Số tiết'],lessonIndex:0,rows:[{cells:['CHƯƠNG II. SỐ NGUYÊN',''],isHeader:true},{cells:['Ôn tập chương II','1'],isHeader:false}]};appendixOneTable([{lesson:'Ôn tập chương II',outcomes:'Củng cố được kiến thức số nguyên và phép tính với số nguyên.'}],{lop:'6',monHoc:'Toán học',ai:{enabled:false}})`,sandbox);
assert(chapterScopedReview.rows[1].cells[3].includes('số nguyên'),'a chapter review must retain the outcome from its current chapter context');
const chapterOneIsolation=vm.runInContext(`sourcePpctTable=null;sourcePpctRows=[{lesson:'CHƯƠNG I. TẬP HỢP SỐ TỰ NHIÊN',isHeader:true},{lesson:'Bài tập cuối chương I',periods:'1',isHeader:false}];appendixOneTable([{lesson:'Bài tập cuối chương I',outcomes:'Nhận biết được điểm, đường thẳng và góc.'}],{lop:'6',monHoc:'Toán học',ai:{enabled:false}})`,sandbox);
assert(/số tự nhiên|tập hợp|phép tính|chia hết|ước/i.test(chapterOneIsolation.rows[1].cells[3]),'PL1 chapter I review must fall back to chapter-I outcomes');
assert(!/điểm|đường thẳng|góc/i.test(chapterOneIsolation.rows[1].cells[3]),'PL1 chapter I review must reject leaked geometry outcomes');
const chapterOnePracticeFallback=vm.runInContext(`officialYccdCache.clear();sourcePpctTable=null;sourcePpctRows=[{lesson:'CHƯƠNG I. TẬP HỢP SỐ TỰ NHIÊN',isHeader:true},{lesson:'Bài 5. Phép nhân và phép chia số tự nhiên',periods:'1',isHeader:false},{lesson:'Luyện tập chung',periods:'1',isHeader:false}];appendixOneTable([{lesson:'Bài 5. Phép nhân và phép chia số tự nhiên',outcomes:'Thực hiện phép nhân và phép chia số tự nhiên.'},{lesson:'Luyện tập chung',outcomes:'Nhận biết được điểm, đường thẳng và góc.'}],{lop:'6',monHoc:'Toán học',ai:{enabled:false}})`,sandbox);
assert(/phép.*nhân|phép.*chia|luỹ thừa/i.test(chapterOnePracticeFallback.rows[2].cells[3]),'PL1 practice fallback after Bài 5 must use the preceding calculation topic');
assert(!/chia hết|ước chung|bội chung|số nguyên tố/i.test(chapterOnePracticeFallback.rows[2].cells[3]),'PL1 practice fallback after Bài 5 must not use whole-chapter review outcomes');
assert.equal(vm.runInContext("densityLowerBound('1-2')",sandbox),1,'NLS density 1-2 must select one digital standard');
assert.equal(vm.runInContext("densityLowerBound('2-3')",sandbox),2,'NLS density 2-3 must select two digital standards');
assert.equal(vm.runInContext("densityLowerBound('3-4')",sandbox),3,'NLS density 3-4 must select three digital standards');

const periodFixture=`getConfig=()=>({lop:'6',monHoc:'Toán học',nls:{enabled:false,rate:0,density:'1-2'},ai:{enabled:false,rate:0,density:'1-2'}});sourcePpctTable={columns:['Bài học','Số tiết'],lessonIndex:0,rows:[{cells:['Bài A','2'],isHeader:false},{cells:['Bài B','3'],isHeader:false}]};sourcePpctRows=[{lesson:'Bài A',periods:'2',isHeader:false},{lesson:'Bài B',periods:'3',isHeader:false}];aiSelectedLessonIds=new Set(['source:0:period:1','source:1:period:2']);results={1:{},2:null,3:{}};activeTab='2';`;
assert.equal(vm.runInContext(`${periodFixture}aiPeriodCandidates().length`,sandbox),5,'period candidates must flatten the lesson durations');
assert.equal(vm.runInContext(`${periodFixture}aiSelectionPercentage()`,sandbox),40,'two selected periods out of five must report 40%');
vm.runInContext(`${periodFixture}updatePpctLessonPeriods('source:0','1')`,sandbox);
assert.equal(vm.runInContext(`sourcePpctTable.rows[0].cells[1]`,sandbox),'1','editing periods must update the raw PPCT table');
assert.equal(vm.runInContext(`sourcePpctRows[0].periods`,sandbox),'1','editing periods must update canonical PPCT rows');
assert.equal(vm.runInContext(`aiSelectedLessonIds.has('source:0:period:2')`,sandbox),false,'reducing periods must discard invalid period selections');
assert.equal(vm.runInContext(`!!results['1']&&!!results['3']`,sandbox),true,'editing periods must immediately synchronize PL1 and PL3');
assert(vm.runInContext(`appendixOneTable([{lesson:'Bài A',outcomes:'Đạt yêu cầu.',integration:'[AI: 6.A1.1 - Hỗ trợ.]'}],{lop:'6',monHoc:'Toán học',ai:{enabled:true}}).rows[0].cells[4]`,sandbox).includes('Áp dụng: tiết 1'),'PL1 must keep a selected partial-period scope');
assert.equal(vm.runInContext(`preservedPpctTable([{lesson:'Bài A',integration:'[AI: 6.A1.1 - Hỗ trợ.]'}],{lop:'6',ai:{enabled:true}}).rows[0].cells[1]`,sandbox),'1','PL3 must keep the edited source period count');
assert.equal(vm.runInContext(`sourcePpctTable=null;sourcePpctRows=[{lesson:'Bài dài',periods:'13',isHeader:false}];aiSelectedLessonIds=new Set(aiPeriodCandidates().map(x=>x.id));selectedAiPeriodIds().size`,sandbox),12,'the thirteenth period must not remain selected');
assert.equal(vm.runInContext(`aiRate={value:'100',min:'0',max:'100',disabled:false};aiRateOut={value:''};syncAiSelectionFromRate();aiSelectedLessonIds.size`,sandbox),12,'the slider must cap its selection at 12 periods');
assert.equal(vm.runInContext(`aiRate.value`,sandbox),'92','the slider must snap to the practical 12-of-13 rate');
assert.equal(vm.runInContext(`sourcePpctTable={columns:['Bài học','Số tiết','Tiết CT'],lessonIndex:0,rows:[{cells:['Bài từ Tiết CT','','3-5'],isHeader:false}]};sourcePpctRows=[];aiPeriodCandidates().length`,sandbox),3,'blank Số tiết must derive period candidates from Tiết CT');
assert.equal(vm.runInContext(`sourcePpctRowsForAppendixOne()[0].periods`,sandbox),'3','PL1 must derive its period count from raw Tiết CT');
const ppctEditing=vm.runInContext(`getConfig=()=>({lop:'6',monHoc:'Toán học',nls:{enabled:false,rate:0,density:'1-2'},ai:{enabled:false,rate:0,density:'1-2'}});results={'1':null,'2':null,'3':null};activeTab='2';sourcePpctTable={columns:['Bài học','Số tiết','Tiết CT','Tuần','Thiết bị dạy học','Địa điểm dạy học'],lessonIndex:0,rows:[{cells:['Bài A','2','8-9','Tuần 9','Bảng phụ','Lớp học'],isHeader:false},{cells:['Bài B','3','1-3','Tuần 1','Máy chiếu','Phòng bộ môn'],isHeader:false}]};sourcePpctRows=[{lesson:'Bài A',periods:'2',tietCT:'8-9',week:'Tuần 9',devices:'Bảng phụ',location:'Lớp học',isHeader:false},{lesson:'Bài B',periods:'3',tietCT:'1-3',week:'Tuần 1',devices:'Máy chiếu',location:'Phòng bộ môn',isHeader:false}];aiSelectedLessonIds=new Set(['source:0:period:1']);const moved=movePpctRow(0,1),editedTiet=updatePpctField(1,'tietCT','20-21'),manualTietCT=sourcePpctTable.rows[1].cells[2],edited=updatePpctField(1,'week','Tuần 10'),manualWeek=sourcePpctTable.rows[1].cells[3],reordered=reorderPpctRow(1,0);({moved,editedTiet,edited,reordered,manualTietCT,manualWeek,table:sourcePpctTable.rows.map(row=>row.cells),rows:sourcePpctRows,selected:[...aiSelectedLessonIds],periodsPerWeek:periodsPerWeekForSubject()})`,sandbox);
assert(ppctEditing.moved&&ppctEditing.editedTiet&&ppctEditing.edited&&ppctEditing.reordered,'PPCT move, edit and reorder helpers must report success');
assert.equal(ppctEditing.table[0][0],'Bài A','reorderPpctRow must update sourcePpctTable');
assert.equal(ppctEditing.rows[0].lesson,'Bài A','reorderPpctRow must update sourcePpctRows');
assert.equal(ppctEditing.manualTietCT,'20, 21','updatePpctField must normalize a direct Tiết CT override with commas');
assert.equal(ppctEditing.manualWeek,'10','updatePpctField must still allow a direct week override');
assert.equal(ppctEditing.periodsPerWeek,4,'Toán học must use its four-period weekly norm');
assert.equal(ppctEditing.table[0][2],'20, 21','reordering must preserve a manually edited Tiết CT');
assert.equal(ppctEditing.table[1][2],'1-3','reordering must preserve source Tiết CT values');
assert.equal(ppctEditing.table[0][3],'10','reordering must preserve a manually edited week');
assert.equal(ppctEditing.table[1][3],'Tuần 1','reordering must preserve source week values');
assert.equal(ppctEditing.rows[1].week,'Tuần 1','manual/source weeks must remain synchronized after reordering');
assert(ppctEditing.selected.includes('source:0:period:1'),'reordering must keep the AI selection attached to its lesson');
const inPlaceEditing=vm.runInContext(`const pickerCalls=[];const previewFrames=[],originalUpdateAiPicker=updateAiPicker;requestAnimationFrame=callback=>{previewFrames.push(callback);return previewFrames.length};updateAiPicker=()=>pickerCalls.push('rebuilt');renderPreview=()=>pickerCalls.push('preview');ppctPreviewFrameId=null;results={'1':null,'2':null,'3':null};sourcePpctTable={columns:['Bài học','Số tiết','Tiết CT','Tuần','Thiết bị dạy học','Địa điểm dạy học'],lessonIndex:0,rows:[{cells:['Bài tại chỗ','1','1','1','Bảng','Lớp'],isHeader:false}]};sourcePpctRows=[{lesson:'Bài tại chỗ',periods:'1',tietCT:'1',week:'1',devices:'Bảng',location:'Lớp',isHeader:false}];const changed=updatePpctField(0,'devices','Máy chiếu');updateAiPicker=originalUpdateAiPicker;({changed,device:sourcePpctTable.rows[0].cells[4],mirror:sourcePpctRows[0].devices,pickerCalls,frames:previewFrames.length})`,sandbox);
assert(inPlaceEditing.changed,'in-place edit must report success');
assert.equal(inPlaceEditing.device,'Máy chiếu','in-place edit must update source PPCT table');
assert.equal(inPlaceEditing.mirror,'Máy chiếu','in-place edit must update source PPCT rows');
assert.deepEqual(Array.from(inPlaceEditing.pickerCalls),[],'text edits must not rebuild the PPCT picker DOM');
assert.equal(inPlaceEditing.frames,1,'text edits must schedule a deferred preview refresh');
const pickerComplexity=vm.runInContext(`(()=>{const pickerNodes={'#aiLessonPickerCard':{classList:{remove(){}}},'#aiLessonPicker':{innerHTML:''},'#aiSelectionCount':{textContent:''}};document.querySelector=selector=>pickerNodes[selector]||null;sourcePpctTable={columns:['Bài học','Số tiết'],lessonIndex:0,rows:Array.from({length:120},(_,index)=>({cells:[\`Bài \${index+1}\`,'1'],isHeader:false}))};sourcePpctRows=[];let candidateCalls=0;const originalCandidates=aiPeriodCandidates;aiPeriodCandidates=()=>{candidateCalls++;return originalCandidates()};updateAiPicker();return {candidateCalls,html:pickerNodes['#aiLessonPicker'].innerHTML}})()`,sandbox);
assert.equal(pickerComplexity.candidateCalls,1,'picker must compute AI period candidates once per full render');
assert(pickerComplexity.html.includes('Bài 120'),'optimized picker must retain every PPCT row');
const cacheBehavior=vm.runInContext(`officialYccdCache.clear();standardCompetenciesCache.clear();let yccdCalls=0,standardCalls=0;getCleanOfficialYccd=()=>{yccdCalls++;return 'YCCĐ cache'};KHBD_STANDARDS={};recommendOfficialStandards=()=>{standardCalls++;return []};getStandardCompetenciesForLesson('Bài cache','6','Toán học','',true);getStandardCompetenciesForLesson('Bài cache','6','Toán học','',true);({yccdCalls,standardCalls})`,sandbox);
assert.deepEqual(JSON.parse(JSON.stringify(cacheBehavior)),{yccdCalls:1,standardCalls:2},'standard lookup cache must avoid repeated YCCĐ and standards searches for one lesson');
const parallelPpct=vm.runInContext(`getConfig=()=>({lop:'6',monHoc:'Toán học',nls:{enabled:false,rate:0,density:'1-2'},ai:{enabled:false,rate:0,density:'1-2'}});results={'1':null,'2':null,'3':null};activeTab='2';sourcePpctTable={columns:['Bài học','Số tiết','Tiết CT','Tuần'],lessonIndex:0,rows:[{cells:['HỌC KÌ I','','',''],isHeader:true},{cells:['1. SỐ HỌC 6','','',''],isHeader:true},{cells:['Bài Số 1','4','',''],isHeader:false},{cells:['2. HÌNH HỌC 6','','',''],isHeader:true},{cells:['Bài Hình 1','2','',''],isHeader:false},{cells:['HỌC KÌ II','','',''],isHeader:true},{cells:['PHÂN SỐ VÀ SỐ THẬP PHÂN','','',''],isHeader:true},{cells:['Bài Số 2','3','',''],isHeader:false},{cells:['HÌNH HỌC CƠ BẢN','','',''],isHeader:true},{cells:['Bài Hình 2','1','',''],isHeader:false}]};sourcePpctRows=sourcePpctTable.rows.map(row=>({lesson:row.cells[0],periods:row.cells[1],tietCT:row.cells[2],week:row.cells[3],isHeader:row.isHeader}));recalculatePpctSequences();sourcePpctTable.rows.map(row=>row.cells.slice(0,4))`,sandbox);
assert.deepEqual(Array.from(parallelPpct[2]),['Bài Số 1','4','1, 2, 3, 4','1, 2'],'number branch must calculate with three periods per week');
assert.deepEqual(Array.from(parallelPpct[4]),['Bài Hình 1','2','1, 2','1, 2'],'geometry branch must begin in week 1 in parallel with number branch');
assert.deepEqual(Array.from(parallelPpct[7]),['Bài Số 2','3','5, 6, 7','19'],'number branch must continue its Tiết CT in semester II');
assert.deepEqual(Array.from(parallelPpct[9]),['Bài Hình 2','1','3','19'],'geometry branch must continue independently in semester II');
const ppctInsertDelete=vm.runInContext(`getConfig=()=>({lop:'6',monHoc:'Toán học',nls:{enabled:false,rate:0,density:'1-2'},ai:{enabled:false,rate:0,density:'1-2'}});results={'1':{},'2':null,'3':{}};activeTab='2';sourcePpctTable={columns:['Bài học','Số tiết','Tiết CT','Tuần','Thiết bị dạy học','Địa điểm dạy học'],lessonIndex:0,rows:[{cells:['Bài A','2','1-2','1','Bảng phụ','Lớp học'],isHeader:false},{cells:['Bài B','1','3','1','Máy chiếu','Phòng bộ môn'],isHeader:false}]};sourcePpctRows=[{lesson:'Bài A',periods:'2',tietCT:'1-2',week:'1',devices:'Bảng phụ',location:'Lớp học',isHeader:false},{lesson:'Bài B',periods:'1',tietCT:'3',week:'1',devices:'Máy chiếu',location:'Phòng bộ môn',isHeader:false}];aiSelectedLessonIds=new Set(['source:1:period:1']);const inserted=insertPpctRowAt(0),afterInsert={table:sourcePpctTable.rows.map(row=>[...row.cells]),rows:sourcePpctRows.map(row=>({...row})),selected:[...aiSelectedLessonIds]},headerInserted=insertPpctRowAt(1,true),afterHeader={lesson:sourcePpctTable.rows[2].cells[0],isHeader:sourcePpctTable.rows[2].isHeader,tiet:sourcePpctTable.rows[3].cells[2]},headerDeleted=deletePpctRowAt(2,false),deleted=deletePpctRowAt(1,false);({inserted,headerInserted,headerDeleted,deleted,afterInsert,afterHeader,table:sourcePpctTable.rows.map(row=>row.cells),rows:sourcePpctRows,selected:[...aiSelectedLessonIds]})`,sandbox);
assert(ppctInsertDelete.inserted&&ppctInsertDelete.headerInserted&&ppctInsertDelete.headerDeleted&&ppctInsertDelete.deleted,'PPCT insert/delete helpers must report success');
assert.equal(ppctInsertDelete.afterInsert.table[1][0],'Bài học mới','insertPpctRowAt must insert the safe default lesson directly below the selected row');
assert.equal(ppctInsertDelete.afterInsert.table[1][1],'1','a new lesson must default to one period');
assert.equal(ppctInsertDelete.afterInsert.table[1][2],'','inserting must not overwrite a new row Tiết CT');
assert.equal(ppctInsertDelete.afterInsert.table[2][2],'3','inserting must preserve later source Tiết CT values');
assert.deepEqual(ppctInsertDelete.afterInsert.selected,['source:2:period:1'],'inserting must keep AI selection attached to the original lesson');
assert.equal(ppctInsertDelete.afterHeader.lesson,'HỌC KÌ / CHƯƠNG MỚI','header insertion must use a safe default header name');
assert.equal(ppctInsertDelete.afterHeader.isHeader,true,'header insertion must preserve header semantics');
assert.equal(ppctInsertDelete.afterHeader.tiet,'3','a header must not alter preserved curriculum periods');
assert.equal(ppctInsertDelete.table.length,2,'deleting an inserted PPCT row must restore the source table length');
assert.equal(ppctInsertDelete.table[1][0],'Bài B','deleting an inserted PPCT row must retain later source rows');
assert.deepEqual(ppctInsertDelete.selected,['source:1:period:1'],'deleting must remap AI selection back to its lesson');
['insertPpctRowAt','deletePpctRowAt','appendPpctRow','➕ Thêm bài học mới','➕ Thêm tiêu đề','title="Chèn dòng dưới"','title="Xóa dòng"'].forEach(value=>has(value,`PPCT row management control ${value}`));
const pickerMetadata=vm.runInContext(`const pickerNodes={'#aiLessonPickerCard':{classList:{remove(){}}},'#aiLessonPicker':{innerHTML:''},'#aiSelectionCount':{textContent:''}};document.querySelector=selector=>pickerNodes[selector]||null;sourcePpctTable={columns:['Bài học','Số tiết','Tiết CT','Tuần','Thiết bị dạy học','Địa điểm dạy học'],lessonIndex:0,rows:[{cells:['Bài hiển thị','1','1','Tuần 1','Máy chiếu','Lớp học'],isHeader:false}]};updateAiPicker();pickerNodes['#aiLessonPicker'].innerHTML`,sandbox);
assert(pickerMetadata.includes('Máy chiếu')&&pickerMetadata.includes('Lớp học'),'PPCT picker must show the complete source lesson metadata');
const pickerTable=vm.runInContext(`const pickerTableNodes={'#aiLessonPickerCard':{classList:{remove(){}}},'#aiLessonPicker':{innerHTML:''},'#aiSelectionCount':{textContent:''}};document.querySelector=selector=>pickerTableNodes[selector]||null;sourcePpctTable={columns:['Bài học','Số tiết','Tiết CT','Tuần','Thiết bị dạy học','Địa điểm dạy học'],lessonIndex:0,rows:[{cells:['HỌC KÌ I','','','','',''],isHeader:true},{cells:['Bài bảng','2','1-2','Tuần 1','Máy chiếu','Lớp học'],isHeader:false}]};updateAiPicker();pickerTableNodes['#aiLessonPicker'].innerHTML`,sandbox);
['overflow-x-auto','<table','STT','Bài học','Số tiết','Tiết CT','Tuần','Thiết bị dạy học','Địa điểm','Tích hợp AI (QĐ 2422)','colspan="8"','Tiết 1','Tiết 2'].forEach(value=>assert(pickerTable.includes(value),`PPCT table picker must include ${value}`));
assert(pickerTable.includes('HỌC KÌ I'),'PPCT table picker must preserve and merge source header rows');
const fallbackPicker=vm.runInContext(`const fallbackPickerNodes={'#aiLessonPickerCard':{classList:{remove(){}}},'#aiLessonPicker':{innerHTML:''},'#aiSelectionCount':{textContent:''}};document.querySelector=selector=>fallbackPickerNodes[selector]||null;sourcePpctTable=null;sourcePpctRows=[];getConfig=()=>({monHoc:'Toán học',lop:'6',nls:{enabled:false,rate:0,density:'1-2'},ai:{enabled:false,rate:0,density:'1-2'}});updateAiPicker();fallbackPickerNodes['#aiLessonPicker'].innerHTML`,sandbox);
assert(fallbackPicker.includes('Bài 1. Tập hợp')&&fallbackPicker.includes('Bài 5. Phép nhân và phép chia số tự nhiên'),'PPCT table picker must show the Toán 6 sample before source upload');
const defaultMath=vm.runInContext(`defaultPpctRows({monHoc:'Toán học',lop:'6',nls:{enabled:false,rate:0,density:'1-2'},ai:{enabled:false,rate:0,density:'1-2'}})`,sandbox);
const defaultLessons=defaultMath.filter(row=>!row.isHeader);
assert.equal(defaultLessons.length,47,'Toán 6 catalog must retain all 47 lessons from the verified sample document');
assert.equal(defaultLessons[0].periods,'1','Toán 6 Bài 1 must retain its verified one-period allocation');
assert.equal(defaultLessons[4].periods,'2','Toán 6 Bài 5 must retain its verified two-period allocation');
assert.equal(defaultLessons.find(row=>row.lesson.includes('Ôn tập và Bài tập cuối chương II')).periods,'5','Toán 6 review must retain its verified five-period allocation');
assert(defaultLessons.some(row=>Number(row.periods)!==4),'Toán 6 PPCT must not be allocated as uniform four-period cards');

let recognitionRequest;
sandbox.fetch=async(url,options)=>{recognitionRequest={url,options};return {ok:true,status:200,json:async()=>({candidates:[{content:{parts:[{text:JSON.stringify({ppct:[{lesson:'Bài AI nhận diện',periods:'2',tietCT:'1-2',week:'Tuần 1',devices:'Máy chiếu',location:'Lớp học'}]})}]}}]})}};
vm.runInContext("apiKeys=['AIza-stage-one'];mistralKeys=[];aborter=null",sandbox);
const recognizedByApi=await sandbox.recognizePpctWithAi('Bài học\\tSố tiết\\nBài AI nhận diện\\t2');
assert.equal(recognizedByApi[0].lesson,'Bài AI nhận diện','recognizer must use the provider JSON PPCT result');
assert(recognitionRequest.url.includes('generativelanguage.googleapis.com'),'recognizer must reuse the existing Gemini provider');
assert(JSON.parse(recognitionRequest.options.body).contents[0].parts[0].text.includes('Không suy diễn Yêu cầu cần đạt'),'stage one provider prompt must forbid early appendix generation');

const modelStorage=new Map([['khbd_gemini_model','gemini-3.6-flash']]);
const modelSelect={value:'',options:[...['gemini-3.7-flash','gemini-3.6-flash','gemini-3.5-flash','gemini-3.5-flash-lite','gemini-2.5-flash','gemini-2.5-flash-lite','gemini-3-flash-preview'].map(value=>({value}))]};
sandbox.localStorage={getItem:key=>modelStorage.get(key)||null,setItem:(key,value)=>modelStorage.set(key,value),removeItem:key=>modelStorage.delete(key),key:index=>Array.from(modelStorage.keys())[index]||null,get length(){return modelStorage.size}};
sandbox.document.querySelector=selector=>selector==='#selectModel'?modelSelect:selector==='#log'?{textContent:'',scrollTop:0}:null;
sandbox.document.body={append(){}};
assert.equal(sandbox.getSelectedModel(),'gemini-3.6-flash','saved model selection must be restored');
sandbox.onModelChange('gemini-3.5-flash');
assert.equal(modelStorage.get('khbd_gemini_model'),'gemini-3.5-flash','only the selected model id may be persisted');
let geminiCalls=[];
sandbox.fetch=async(url,options)=>{geminiCalls.push({url,options});return {ok:true,status:200,json:async()=>({candidates:[{content:{parts:[{text:'{"ok":true}'}]}}]})}};
vm.runInContext("apiKeys=['AIza-direct'];mistralKeys=[];aborter=null",sandbox);
await sandbox.callGemini('payload test');
assert(geminiCalls[0].url.includes('/gemini-3.5-flash:generateContent'),'direct request must use the selected model');
assert.equal(JSON.parse(geminiCalls[0].options.body).generationConfig.thinkingConfig.thinkingBudget,0,'Gemini request must disable thinking budget');
geminiCalls=[];
sandbox.fetch=async(url,options)=>{geminiCalls.push({url,options});if(url.includes('generativelanguage.googleapis.com'))throw new TypeError('network/CORS');return {ok:true,status:200,json:async()=>({ok:true,status:200,body:{candidates:[{content:{parts:[{text:'{"proxy":true}'}]}}]}})}};
assert.deepEqual(await sandbox.callGemini('proxy test'),{proxy:true},'network failure must retry through proxy');
assert(geminiCalls.some(call=>call.url==='api/khbd_gemini.php'),'proxy fallback must call khbd proxy');
geminiCalls=[];modelStorage.set('khbd_gemini_model','gemini-3.7-flash');
sandbox.fetch=async(url,options)=>{geminiCalls.push({url,options});if(url.includes('gemini-3.7-flash'))return {ok:false,status:503,json:async()=>({error:{message:'high demand'}})};return {ok:true,status:200,json:async()=>({candidates:[{content:{parts:[{text:'{"fallback":true}'}]}}]})}};
assert.deepEqual(await sandbox.callGemini('fallback test'),{fallback:true},'3.7 transient failures must retry with 2.5');
assert(geminiCalls.some(call=>call.url.includes('gemini-2.5-flash')),'fallback must use Gemini 2.5 Flash without changing saved model');
assert.equal(modelStorage.get('khbd_gemini_model'),'gemini-3.7-flash','temporary fallback must not overwrite selected model');

const keyElements={
  '#keyBadge':{textContent:''},'#keyInput':{value:'AIza-manual\nAIza-manual'},'#mistralKeyInput':{value:'mistral-manual\nmistral-manual'},
  '#keyModal':{classList:{add(){},remove(){}}},'#keyResults':{textContent:'',innerHTML:''}
};
const keyStorage=new Map();
sandbox.localStorage.getItem=key=>keyStorage.get(key)||null;
sandbox.localStorage.removeItem=key=>keyStorage.delete(key);
sandbox.localStorage.key=index=>Array.from(keyStorage.keys())[index]||null;
Object.defineProperty(sandbox.localStorage,'length',{get:()=>keyStorage.size});
sandbox.setTimeout=()=>0;
sandbox.document.querySelector=selector=>keyElements[selector]||null;
sandbox.document.body={append(){}};
let serverRequests=[];
sandbox.fetch=async(url,options={})=>{serverRequests.push({url,options});if(options.method==='POST')return {ok:true,json:async()=>({ok:true,keys:['AIza-saved'],mistral_keys:['mistral-saved']})};return {ok:true,json:async()=>({ok:true,keys:['AIza-server','AIza-server'],mistral_keys:['mistral-server','mistral-server']})}};
assert.equal(await sandbox.syncUserKeysFromServer(),true,'server key sync must succeed without exposing key contents');
assert.deepEqual(Array.from(vm.runInContext('apiKeys',sandbox)),['AIza-server'],'GET sync must apply normalized Gemini keys');
assert.deepEqual(Array.from(vm.runInContext('mistralKeys',sandbox)),['mistral-server'],'GET sync must apply normalized Mistral keys');
await sandbox.saveKeys();
const saveRequest=serverRequests.find(request=>request.options.method==='POST');
assert(saveRequest,'saving keys must POST to the key API');
assert.deepEqual(JSON.parse(saveRequest.options.body),{keys:['AIza-manual'],mistral_keys:['mistral-manual']},'POST body must include both normalized key arrays');
keyStorage.set('khbd_gemini_api_keys','legacy-key');keyStorage.set('xdpl_mistral_api_keys','legacy-key');keyStorage.set('teacherName','Giáo viên');
sandbox.clearLegacyApiKeyStorage();
assert.equal(keyStorage.has('khbd_gemini_api_keys'),false,'legacy Gemini storage must be cleared');
assert.equal(keyStorage.has('xdpl_mistral_api_keys'),false,'legacy Mistral storage must be cleared');
assert.equal(keyStorage.get('teacherName'),'Giáo viên','non-key preferences must not be removed');
serverRequests=[];vm.runInContext('syncUserKeysPromise=null',sandbox);
assert.deepEqual(await Promise.all([sandbox.ensureKeysLoaded(),sandbox.ensureKeysLoaded()]),[true,true],'recognition must await the shared eager key-load promise');
assert.equal(serverRequests.filter(request=>request.options.method==='GET').length,1,'concurrent key checks must share one eager GET request');
assert.equal(keyElements['#keyBadge'].textContent,'🔑 1 Gemini · 1 Mistral','badge must report provider-specific counts');
const allRadio={checked:false};
sandbox.generateAll={disabled:false};
sandbox.document.querySelector=selector=>selector==='input[value="all"]'?allRadio:null;
vm.runInContext("apiKeys=['mock-key'];mistralKeys=[];results={};getConfig=()=>({});callAiJson=async prompt=>({appendix:prompt});normalizeAppendix=value=>value;appendixPrompt=no=>no;setStep=()=>{};setProgress=()=>{};log=()=>{};showTab=()=>{};notify=()=>{};openKeyModal=()=>{};aborter=null",sandbox);
await sandbox.generateSelected('all');
assert.deepEqual(Array.from(vm.runInContext('Object.keys(results).sort()',sandbox)),['1','2','3'],'generateSelected(all) must generate all three appendices');
assert.equal(allRadio.checked,true,'generateSelected(all) must synchronize the all radio button');
console.log('PASS xaydungphuluc smoke: PPCT 7-column form, independent table ingest, no admin-header leak, density ranges and auto-hiding progress UI are present.');
}
run().catch(error=>{console.error(error);process.exitCode=1});
