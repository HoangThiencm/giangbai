/* Smoke test for the standalone THCS Appendix Builder. Run: node tests/xaydungphuluc-smoke.js */
const fs=require('fs'),path=require('path'),assert=require('assert');
const file=path.join(__dirname,'..','xaydungphuluc.html');
const html=fs.readFileSync(file,'utf8');
function has(value,label=value){assert(html.includes(value),`Missing: ${label}`)}
assert(/^<!doctype html>/i.test(html),'not a standalone HTML document');
['tailwindcss','mammoth','pdf.js','docx@8.5.0','JSZip','FileSaver'].forEach(x=>has(x));
['Lớp 6','Lớp 7','Lớp 8','Lớp 9','Toán học','Ngữ văn','Khoa học tự nhiên','Giáo dục địa phương'].forEach(has);
['js/security-guard.js','access-control.js','khbd_user_gemini_keys_${userEmail}','khbd_user_gemini_keys_default','khbd_gemini_api_keys','gemini_api_keys','xdpl_gemini_api_keys','global_gemini_keys','loadKeys','saveKeys','checkKeys','429','403'].forEach(has);
['nlsRate','nlsDensity','aiRate','aiDensity','NLS và AI ĐỘC LẬP'].forEach(has);
['appendixPrompt','Phụ lục 1','Phụ lục 2','Phụ lục 3','Công văn 5512','TT 38/2021','TT 14/2020'].forEach(has);
['parseFiles','mammoth.extractRawText','pdfjsLib','generateSelected','exportDocx','contenteditable','exportAll'].forEach(has);
has('tuyệt đối không dùng Huyện, Phòng GD&ĐT hoặc Phòng Giáo dục','two-tier local-government safeguard');
console.log('PASS xaydungphuluc smoke: HTML, THCS data, API rotation, independent NLS/AI, prompts, parsers and DOCX export are present.');
