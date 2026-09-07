const fs = require('fs');
const path = require('path');
const assert = require('assert');
const vm = require('vm');
const zlib = require('zlib');

function loadDocx() {
  try {
    return require('docx');
  } catch (e) {
    const runtimeModule = path.join(
      process.env.USERPROFILE || '',
      '.cache', 'codex-runtimes', 'codex-primary-runtime',
      'dependencies', 'node', 'node_modules', 'docx'
    );
    if (fs.existsSync(runtimeModule)) return require(runtimeModule);
    throw e;
  }
}

const docx = loadDocx();
global.window = { docx };
const { DocxGenerator, docxGenerator } = require('../js/khbd-docx.js');
global.docxGenerator = docxGenerator;

function readZipEntry(buffer, entryName) {
  const endSignature = 0x06054b50;
  let endOffset = -1;
  for (let offset = buffer.length - 22; offset >= 0; offset--) {
    if (buffer.readUInt32LE(offset) === endSignature) {
      endOffset = offset;
      break;
    }
  }
  assert.notStrictEqual(endOffset, -1, 'DOCX phải là gói ZIP hợp lệ');

  const entryCount = buffer.readUInt16LE(endOffset + 10);
  let offset = buffer.readUInt32LE(endOffset + 16);
  for (let index = 0; index < entryCount; index++) {
    const compression = buffer.readUInt16LE(offset + 10);
    const compressedSize = buffer.readUInt32LE(offset + 20);
    const nameLength = buffer.readUInt16LE(offset + 28);
    const extraLength = buffer.readUInt16LE(offset + 30);
    const commentLength = buffer.readUInt16LE(offset + 32);
    const localOffset = buffer.readUInt32LE(offset + 42);
    const name = buffer.subarray(offset + 46, offset + 46 + nameLength).toString('utf8');
    if (name === entryName) {
      const localNameLength = buffer.readUInt16LE(localOffset + 26);
      const localExtraLength = buffer.readUInt16LE(localOffset + 28);
      const payloadOffset = localOffset + 30 + localNameLength + localExtraLength;
      const payload = buffer.subarray(payloadOffset, payloadOffset + compressedSize);
      return compression === 0 ? payload : zlib.inflateRawSync(payload);
    }
    offset += 46 + nameLength + extraLength + commentLength;
  }
  throw new Error(`Không tìm thấy ${entryName} trong DOCX`);
}

async function main() {
  console.log('==================================================');
  console.log('KIỂM THỬ CÔNG THỨC EQUATION TRONG PHỤ LỤC (SMOKE TEST)');
  console.log('==================================================');

  const files = [
    'xaydungphuluc.html',
    'canvas_xaydungphuluc.html',
    'backupcode viettailieu/canvas_xaydungphuluc.html'
  ];

  // 1. Kiểm tra sự hiện diện của các hàm và quy chuẩn trong mã nguồn
  console.log('-> 1. Kiểm tra hooks & functions trong các file...');
  for (const rel of files) {
    const content = fs.readFileSync(path.join(__dirname, '..', rel), 'utf8');
    assert.ok(content.includes('function autoWrapMathInDelimiters'), `${rel} thiếu autoWrapMathInDelimiters`);
    assert.ok(content.includes('function renderMathHtml'), `${rel} thiếu renderMathHtml`);
    assert.ok(content.includes('function parseDocxMathRuns'), `${rel} thiếu parseDocxMathRuns`);
    assert.ok(content.includes('QUY TẮC CÔNG THỨC TOÁN HỌC (BẮT BUỘC ĐẶT TRONG EQUATION)'), `${rel} thiếu quy tắc công thức toán trong standards`);
    assert.ok(content.includes('children:parseDocxMathRuns('), `${rel} thiếu parseDocxMathRuns trong para/exportDocx`);
    assert.ok(content.includes('katex.min.js'), `${rel} thiếu thư viện KaTeX`);
    console.log(`  ✓ ${rel}: PASS`);
  }

  // 2. Kiểm tra autoWrapMathInDelimiters trong VM sandbox
  console.log('-> 2. Kiểm tra autoWrapMathInDelimiters với các dạng công thức...');
  const canvasSrc = fs.readFileSync(path.join(__dirname, '..', 'canvas_xaydungphuluc.html'), 'utf8');
  const sandbox = {
    esc: s => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;'),
    docx,
    docxGenerator,
    DocxGenerator,
    window: { docx, docxGenerator, DocxGenerator }
  };
  vm.createContext(sandbox);

  const extractFn = name => {
    const start = canvasSrc.indexOf(`function ${name}(`);
    assert.ok(start >= 0, `Không tìm thấy ${name}`);
    return canvasSrc.slice(start, canvasSrc.indexOf('\n', start));
  };

  vm.runInContext(
    extractFn('autoWrapMathInDelimiters') + '\n' +
    extractFn('renderMathHtml') + '\n' +
    extractFn('parseDocxMathRuns'),
    sandbox
  );

  // Test auto-wrap
  const w1 = sandbox.autoWrapMathInDelimiters('Giải phương trình ax + b = 0 trong tập R');
  assert.ok(w1.includes('$ax + b = 0$'), 'Phải bọc phương trình ax + b = 0 trong $');

  const w2 = sandbox.autoWrapMathInDelimiters('Hệ hai phương trình \\begin{cases} x + y = 3 \\\\ 2x - y = 1 \\end{cases} có nghiệm');
  assert.ok(w2.includes('$\\begin{cases}'), 'Phải bọc hệ phương trình trong $');

  const w3 = sandbox.autoWrapMathInDelimiters('Tính phân số \\frac{a}{b} + \\frac{c}{d} và căn \\sqrt{x^2 + 1}');
  assert.ok(w3.includes('$\\frac{a}{b}$'), 'Phải bọc phân số trong $');
  assert.ok(w3.includes('$\\sqrt{x^2 + 1}$'), 'Phải bọc căn thức trong $');

  const w4 = sandbox.autoWrapMathInDelimiters('Quan hệ a ∈ A và b ∉ A, x ≤ 5 và y ≥ 0');
  assert.ok(w4.includes('$\\in') || w4.includes('$a \\in'), 'Phải chuyển ký hiệu thuộc về LaTeX');
  assert.ok(w4.includes('$\\notin') || w4.includes('$b \\notin'), 'Phải chuyển ký hiệu không thuộc về LaTeX');
  assert.ok(w4.includes('\\le'), 'Phải chuyển ký hiệu nhỏ hơn hoặc bằng về LaTeX');
  assert.ok(w4.includes('\\ge'), 'Phải chuyển ký hiệu lớn hơn hoặc bằng về LaTeX');

  const w5 = sandbox.autoWrapMathInDelimiters('Đã bọc sẵn $x^2 - 1 = 0$ không được bọc lặp');
  assert.ok(!w5.includes('$$x^2') && w5.includes('$x^2 - 1 = 0$'), 'Không được bọc 2 lần');
  console.log('  ✓ autoWrapMathInDelimiters: PASS');

  // 3. Kiểm tra Word export sinh OMML <m:oMath> thực chất cho tất cả các công thức
  console.log('-> 3. Kiểm tra OMML Equation sinh ra trong DOCX...');
  const testText = `Bài 1. Phương trình bậc nhất hai ẩn ax + by = c (với a ≠ 0 hoặc b ≠ 0).
YCCĐ:
- Nhận biết nghiệm của hệ phương trình \\begin{cases} x + y = 17 \\\\ 10x + 3y = 100 \\end{cases}.
- Vận dụng phân số \\frac{a + b}{c} và căn bậc hai \\sqrt{x^2 + 4} để giải bài toán.
- So sánh x_1, x_2 và quan hệ a \\notin A.`;

  const lines = testText.split('\n').filter(Boolean);
  const runsList = lines.map(line => sandbox.parseDocxMathRuns(line, { size: 26 }, docx));
  
  const paragraphs = runsList.map(runs => new docx.Paragraph({ children: runs }));
  const testDoc = new docx.Document({
    sections: [{ children: paragraphs }]
  });

  const buffer = await docx.Packer.toBuffer(testDoc);
  const xml = readZipEntry(buffer, 'word/document.xml').toString('utf8');

  assert.match(xml, /<m:oMath>/, 'Word export bắt buộc phải chứa thẻ Equation OMML <m:oMath>');
  assert.match(xml, /<m:f>/, 'Phân số phải tạo OMML fraction <m:f>');
  assert.match(xml, /<m:rad>/, 'Căn thức phải tạo OMML radical <m:rad>');
  assert.match(xml, /<m:eqArr>/, 'Hệ phương trình cases phải tạo Equation Array <m:eqArr>');
  assert.ok(xml.includes('∉') || xml.includes('notin'), 'Ký hiệu notin phải xuất hiện trong Math');
  assert.ok(xml.includes('≠') || xml.includes('ne'), 'Ký hiệu khác phải xuất hiện trong Math');
  assert.ok(!xml.includes('\\begin{cases}') && !xml.includes('\\end{cases}'), 'XML Word không được chứa cú pháp LaTeX thô');

  const mathCount = (xml.match(/<m:oMath>/g) || []).length;
  console.log(`  ✓ Đã sinh thành công ${mathCount} Equation (<m:oMath>) trong file Word!`);
  assert.ok(mathCount >= 5, `Phải sinh ít nhất 5 Equation, thực tế sinh ${mathCount}`);

  console.log('==================================================');
  console.log('🎉 TẤT CẢ KIỂM THỬ CÔNG THỨC EQUATION ĐÃ ĐẠT 100%!');
  console.log('==================================================');
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
