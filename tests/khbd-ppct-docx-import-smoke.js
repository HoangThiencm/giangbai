const fs=require('fs'),assert=require('assert'),path=require('path');
const app=require('../js/khbd-app.js');
const source=fs.readFileSync(path.join(__dirname,'..','js','khbd-app.js'),'utf8');
const main=fs.readFileSync(path.join(__dirname,'..','soankhbd.html'),'utf8');
const canvas=fs.readFileSync(path.join(__dirname,'..','canvas_soankhbd.html'),'utf8');
const backup=fs.readFileSync(path.join(__dirname,'..','backupcode viettailieu','canvas_soankhbd.html'),'utf8');

// Minimal OOXML fixture: a PPCT header with seven columns, merged chapter and
// both modern OMML and legacy MathType objects. It guards the source contract
// without uploading a document or invoking Gemini.
const OOXML=`<w:document xmlns:w="w" xmlns:m="m"><w:body><w:tbl>
<w:tr><w:tc><w:p><w:r><w:t>Nội dung</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Số tiết</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Tiết CT</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Tuần</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Thiết bị</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Năng lực số</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>AI</w:t></w:r></w:p></w:tc></w:tr>
<w:tr><w:tc><w:tcPr><w:gridSpan w:val="7"/></w:tcPr><w:p><w:r><w:t>CHƯƠNG I</w:t></w:r></w:p></w:tc></w:tr>
<w:tr><w:tc><w:p><w:r><w:t>Bài 1: Tập hợp</w:t></w:r><m:oMath><m:r><m:t>x</m:t></m:r></m:oMath></w:p></w:tc><w:tc><w:p><w:r><w:t>2</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>1, 2</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>1</w:t></w:r></w:p></w:tc><w:tc><w:p><w:object><o:OLEObject/></w:object></w:p></w:tc><w:tc><w:p><w:r><w:t>1.1.TC1a</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>6.A1</w:t></w:r></w:p></w:tc></w:tr>
</w:tbl></w:body></w:document>`;
assert.match(OOXML,/gridSpan/);assert.match(OOXML,/m:oMath/);assert.match(OOXML,/OLEObject/);assert.strictEqual((OOXML.match(/<w:tc>/g)||[]).length,15);
['readPpctDocx','docxTableGrid','gridSpan','vMerge','findPpctDocxTable','ppctHeaderIndex','[CÔNG THỨC]','[CÔNG THỨC MathType]','docx-table','Không tìm thấy bảng PPCT'].forEach(token=>assert(source.includes(token),token));
assert.deepStrictEqual(app.ppctCellCodes('NLS: 1.1.TC1a; AI 6.A1'),['1.1.TC1a','6.A1']);
const candidate=app.findPpctDocxTable([[['Thủ tục','Người ký'],['x','y'],['z','q']], [['Nội dung bài học','Số tiết','Tiết CT','Tuần','Năng lực số','AI'],['Bài 1','2','1,2','1','1.1.TC1a','6.A1'],['Bài 2','1','3','2','','']]]);
assert(candidate&&candidate.index===1&&candidate.map.title===0&&candidate.map.nls===4&&candidate.map.ai===5);
for(const html of [main,canvas,backup]){assert.match(html,/jszip\/3\.10\.1\/jszip\.min\.js/);assert.match(html,/mammoth\/1\.6\.0\/mammoth\.browser\.min\.js/);assert.match(html,/\.docx/);}
assert.match(main,/Word được đọc trực tiếp trên máy/);assert.match(source,/Không gửi file lên AI/);
console.log('PASS khbd PPCT DOCX import smoke');
