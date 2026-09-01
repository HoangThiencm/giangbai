/* Smoke test for the standalone THCS Appendix Builder. Run: node tests/xaydungphuluc-smoke.js */
const fs=require('fs'),path=require('path'),assert=require('assert'),vm=require('vm');
const {getCleanOfficialYccd}=require('../js/khbd-yccd.js');
const {recommendOfficialStandards}=require('../js/khbd-standards.js');
async function run(){
const file=path.join(__dirname,'..','xaydungphuluc.html');
const html=fs.readFileSync(file,'utf8');
function has(value,label=value){assert(html.includes(value),`Missing: ${label}`)}
assert(/^<!doctype html>/i.test(html),'not a standalone HTML document');
['tailwindcss','mammoth','pdf.js','xlsx.full.min.js','docx@8.5.0','JSZip','FileSaver'].forEach(x=>has(x));
['Lớp 6','Lớp 7','Lớp 8','Lớp 9','Toán học','Ngữ văn','Khoa học tự nhiên','Giáo dục địa phương'].forEach(has);
['js/security-guard.js','access-control.js','LEGACY_API_KEY_STORAGE_KEYS','khbd_user_gemini_keys_default','khbd_gemini_api_keys','gemini_api_keys','xdpl_gemini_api_keys','global_gemini_keys','clearLegacyApiKeyStorage','ensureKeysLoaded','syncUserKeysPromise','saveKeys','checkKeys','429','403','mistralKeys','mistralKeyInput','mistral_keys','syncUserKeysFromServer','api/user_gemini_keys.php','credentials:\'include\'','cache:\'no-store\''].forEach(has);
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
  JSON,Math,Set,Array,String,Number,Boolean,RegExp,Date,Error,Promise,Map,AbortController,setTimeout,clearTimeout,
  DOMParser:class{parseFromString(){return {querySelectorAll(){return []}}}},
};
vm.createContext(sandbox);
try{vm.runInContext(script[1].replace(/document\.addEventListener\('DOMContentLoaded'[\s\S]*\);\s*$/,''),sandbox);}
catch(e){assert.fail('inline JavaScript failed to parse: '+e.message)}
assert.equal(typeof sandbox.extractPpctRows,'function','extractPpctRows must be defined');
assert.equal(typeof sandbox.recognizePpctWithAi,'function','stage-one PPCT recognizer must be defined');
assert.equal(typeof sandbox.callAiJson,'function','AI provider fallback must be defined');
const bai14Yccd=getCleanOfficialYccd({subjectId:'toan',grade:'6',topic:'Bài 14. Phép cộng và phép trừ số nguyên'});
assert(/phép cộng|số nguyên/i.test(bai14Yccd),'clean YCCĐ must match Bài 14 by its lesson number');
assert(!/ước chung lớn nhất|bội chung nhỏ nhất/i.test(bai14Yccd),'Bài 14 YCCĐ must not leak ƯCLN/BCNN from another lesson');
assert(!/nguồn bắt buộc|căn cứ|bài sgk|nội dung ctgdpt/i.test(bai14Yccd),'clean YCCĐ must contain outcomes only, without metadata');
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
assert(!html.includes('id="aiLessonPickerCard" class="card p-5 hidden"'),'AI lesson picker must be visible on initial load');
['sourcePpctRowsForAppendixOne','appendixOneTable','appendixOneFallbackOutcome','outcomes (Yêu cầu cần đạt) chuẩn Chương trình GDPT 2018'].forEach(has);
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
assert.equal(vm.runInContext("formatOutcomeLines('Mô tả được nội dung.,- Nhận biết được khái niệm; - Vận dụng được kiến thức.')",sandbox),'Mô tả được nội dung.\n- Nhận biết được khái niệm\n- Vận dụng được kiến thức.','outcomes must normalize compact bullets into separate lines');
assert.equal(vm.runInContext("formatTietCT('8 9')",sandbox),'8\n9','Tiết CT must display each curriculum period on its own line');
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
assert.equal(appendixOne.rows[1].cells[3],'Nhận biết và mô tả được tập hợp.','PL1 must use the AI-generated outcome');
assert(appendixOne.rows[1].cells[4].includes('[AI:'),'selected PL3 lesson must retain its AI code in PL1');
assert(appendixOne.rows[1].cells[4].includes('Áp dụng: tiết 1'),'partial selected period must be scoped in PL1 AI integration');
sandbox.getCleanOfficialYccd=()=>'- Thực hiện được phép cộng và phép trừ số nguyên.';
const cleanAppendixOne=vm.runInContext(`sourcePpctTable={columns:['Bài học','Số tiết'],lessonIndex:0,rows:[{cells:['Bài 14. Phép cộng và phép trừ số nguyên','1'],isHeader:false}]};appendixOneTable([{lesson:'Bài 14. Phép cộng và phép trừ số nguyên',outcomes:'Nguồn bắt buộc: CTGDPT 2018. Bài SGK: Bài 14.'}],{lop:'6',monHoc:'Toán học',ai:{enabled:false}})`,sandbox);
assert.equal(cleanAppendixOne.rows[0].cells[3],'- Thực hiện được phép cộng và phép trừ số nguyên.','PL1 must replace metadata outcomes with clean YCCĐ');
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
const ppctEditing=vm.runInContext(`getConfig=()=>({lop:'6',monHoc:'Toán học',nls:{enabled:false,rate:0,density:'1-2'},ai:{enabled:false,rate:0,density:'1-2'}});results={'1':null,'2':null,'3':null};activeTab='2';sourcePpctTable={columns:['Bài học','Số tiết','Tiết CT','Tuần','Thiết bị dạy học','Địa điểm dạy học'],lessonIndex:0,rows:[{cells:['Bài A','1','1','Tuần 1','Bảng phụ','Lớp học'],isHeader:false},{cells:['Bài B','1','2','Tuần 2','Máy chiếu','Phòng bộ môn'],isHeader:false}]};sourcePpctRows=[{lesson:'Bài A',periods:'1',tietCT:'1',week:'Tuần 1',devices:'Bảng phụ',location:'Lớp học',isHeader:false},{lesson:'Bài B',periods:'1',tietCT:'2',week:'Tuần 2',devices:'Máy chiếu',location:'Phòng bộ môn',isHeader:false}];aiSelectedLessonIds=new Set(['source:0:period:1']);const moved=movePpctRow(0,1),edited=updatePpctField(1,'week','Tuần 10'),reordered=reorderPpctRow(1,0);({moved,edited,reordered,table:sourcePpctTable.rows.map(row=>row.cells),rows:sourcePpctRows,selected:[...aiSelectedLessonIds]})`,sandbox);
assert(ppctEditing.moved&&ppctEditing.edited&&ppctEditing.reordered,'PPCT move, edit and reorder helpers must report success');
assert.equal(ppctEditing.table[0][0],'Bài A','reorderPpctRow must update sourcePpctTable');
assert.equal(ppctEditing.rows[0].lesson,'Bài A','reorderPpctRow must update sourcePpctRows');
assert.equal(ppctEditing.table[0][3],'10','updatePpctField must normalize and update sourcePpctTable');
assert.equal(ppctEditing.rows[0].week,'10','updatePpctField must normalize and update sourcePpctRows');
assert(ppctEditing.selected.includes('source:0:period:1'),'reordering must keep the AI selection attached to its lesson');
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
