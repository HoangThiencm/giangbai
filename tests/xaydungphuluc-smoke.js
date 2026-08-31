/* Smoke test for the standalone THCS Appendix Builder. Run: node tests/xaydungphuluc-smoke.js */
const fs=require('fs'),path=require('path'),assert=require('assert'),vm=require('vm');
const file=path.join(__dirname,'..','xaydungphuluc.html');
const html=fs.readFileSync(file,'utf8');
function has(value,label=value){assert(html.includes(value),`Missing: ${label}`)}
assert(/^<!doctype html>/i.test(html),'not a standalone HTML document');
['tailwindcss','mammoth','pdf.js','xlsx.full.min.js','docx@8.5.0','JSZip','FileSaver'].forEach(x=>has(x));
['Lớp 6','Lớp 7','Lớp 8','Lớp 9','Toán học','Ngữ văn','Khoa học tự nhiên','Giáo dục địa phương'].forEach(has);
['js/security-guard.js','access-control.js','khbd_user_gemini_keys_${userEmail}','khbd_user_gemini_keys_default','khbd_gemini_api_keys','gemini_api_keys','xdpl_gemini_api_keys','global_gemini_keys','loadKeys','saveKeys','checkKeys','429','403'].forEach(has);
['nlsRate','nlsDensity','aiRate','aiDensity','NLS và AI ĐỘC LẬP','1–2 mã/bài','2–3 mã/bài','3–4 mã/bài'].forEach(has);
['appendixPrompt','NGUYÊN TẮC BẢO TOÀN PPCT NGUỒN','giữ nguyên 100%','Tuần 1 đến Tuần 35','Phụ lục 1','Phụ lục 2','Phụ lục 3','Công văn 5512','TT 38/2021','TT 14/2020'].forEach(has);
['parseFiles','extractPpctRows','extractDocxTables','ingestSourceTables','preserveSourceSchedule','mammoth.extractRawText','pdfjsLib','XLSX.read','generateSelected','exportDocx','contenteditable','exportAll'].forEach(has);
has('table-layout: fixed');
has('word-break: break-word');
['progressContainer','progressPercent','progressBarInner','setProgress','hideProgress','progressTimerId','SCHEDULE_COLUMNS','PLAN_COLUMNS','UBND XÃ/PHƯỜNG','CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM'].forEach(has);
has('onclick="hideProgress()"');
has('setTimeout(()=>hideProgress(),hideMs??1500)');
has('progress-done');
has('class="text-xs opacity-75 hover:opacity-100 ml-2"');
['Bài học','Số tiết','Tiết CT','Tuần','Thiết bị dạy học (*)','Địa điểm dạy học (**)','Mã NLS & AI (CV 3456 & QĐ 2422)'].forEach(has);
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
  document:{querySelector(){return null},querySelectorAll(){return []},addEventListener(){},createElement(){return {className:'',textContent:'',append(){},remove(){}}}},
  localStorage:{getItem(){return null},setItem(){}},
  console,
  JSON,Math,Set,Array,String,Number,Boolean,RegExp,Date,Error,Promise,Map,
  DOMParser:class{parseFromString(){return {querySelectorAll(){return []}}}},
};
vm.createContext(sandbox);
try{vm.runInContext(script[1].replace(/document\.addEventListener\('DOMContentLoaded'[\s\S]*\);\s*$/,''),sandbox);}
catch(e){assert.fail('inline JavaScript failed to parse: '+e.message)}
assert.equal(typeof sandbox.extractPpctRows,'function','extractPpctRows must be defined');
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
console.log('PASS xaydungphuluc smoke: PPCT 7-column form, independent table ingest, no admin-header leak, density ranges and auto-hiding progress UI are present.');
