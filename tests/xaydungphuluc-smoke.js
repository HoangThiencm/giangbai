/* Smoke test for the standalone THCS Appendix Builder. Run: node tests/xaydungphuluc-smoke.js */
const fs=require('fs'),path=require('path'),assert=require('assert');
const file=path.join(__dirname,'..','xaydungphuluc.html');
const html=fs.readFileSync(file,'utf8');
function has(value,label=value){assert(html.includes(value),`Missing: ${label}`)}
assert(/^<!doctype html>/i.test(html),'not a standalone HTML document');
['tailwindcss','mammoth','pdf.js','xlsx.full.min.js','docx@8.5.0','JSZip','FileSaver'].forEach(x=>has(x));
['Lớp 6','Lớp 7','Lớp 8','Lớp 9','Toán học','Ngữ văn','Khoa học tự nhiên','Giáo dục địa phương'].forEach(has);
['js/security-guard.js','access-control.js','khbd_user_gemini_keys_${userEmail}','khbd_user_gemini_keys_default','khbd_gemini_api_keys','gemini_api_keys','xdpl_gemini_api_keys','global_gemini_keys','loadKeys','saveKeys','checkKeys','429','403'].forEach(has);
['nlsRate','nlsDensity','aiRate','aiDensity','NLS và AI ĐỘC LẬP','1–2 mã/bài','2–3 mã/bài','3–4 mã/bài'].forEach(has);
['appendixPrompt','NGUYÊN TẮC BẢO TOÀN PPCT NGUỒN','giữ nguyên 100%','Tuần 1 đến Tuần 35','Phụ lục 1','Phụ lục 2','Phụ lục 3','Công văn 5512','TT 38/2021','TT 14/2020'].forEach(has);
['parseFiles','extractPpctRows','preserveSourceSchedule','mammoth.extractRawText','pdfjsLib','XLSX.read','generateSelected','exportDocx','contenteditable','exportAll'].forEach(has);
['progressContainer','progressPercent','progressBarInner','setProgress','SCHEDULE_COLUMNS','PLAN_COLUMNS','UBND XÃ/PHƯỜNG','CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM'].forEach(has);
assert(!html.includes('Phương pháp & kĩ thuật dạy học'),'legacy methods section must be removed');
has('tuyệt đối không dùng Huyện, Phòng GD&ĐT hoặc Phòng Giáo dục','two-tier local-government safeguard');
console.log('PASS xaydungphuluc smoke: PPCT preservation, Tuan columns, standard DOCX tables, density ranges and floating progress UI are present.');
