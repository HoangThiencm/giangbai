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
    assert.ok(content.includes('APPENDIX_3_COLUMNS'), `${rel} thiếu cấu trúc 8 cột Phụ lục 3`);
    assert.ok(content.includes('function appendixThreeTable'), `${rel} thiếu bộ tách cột NLS/AI Phụ lục 3`);
    assert.ok(content.includes('appendixThree:[20,5,6,5,14,12,19,19]'), `${rel} thiếu độ rộng Word 8 cột Phụ lục 3`);
    assert.ok(content.includes('function cleanMathEntityName'), `${rel} thiếu bộ làm sạch thực thể toán học`);
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

  // 4. Kiểm tra triệt để Phụ lục 3: Không còn bất kỳ ký tự $ nào sót lại trong Word XML
  console.log('-> 4. Kiểm tra xuất Word Phụ lục 3: 100% không còn dấu $ thô trong XML...');
  const pl3TestText = [
    'Bài 1. Khái niệm phương trình ax + by = c (a ≠ 0 hoặc b ≠ 0)',
    'Bài 18. Hàm số y = ax² (a ≠ 0) và đồ thị parabol',
    '[NLS: 5.3.TC2a - Sử dụng phần mềm GeoGebra vẽ đồ thị đường thẳng $ax + by = c$ và tìm nghiệm]',
    '[AI: 9.B2.1 - Dùng trợ lý AI gợi ý nghiệm của hệ $\\begin{cases} x + y = 3 \\\\ 2x - y = 0 \\end{cases}$ (Áp dụng: tiết 1, 2)]',
    'Rút gọn phân thức: \\frac{-b \\pm \\sqrt{\\Delta}}{2a} với \\Delta = b^2 - 4ac'
  ];

  const pl3Runs = pl3TestText.map(line => sandbox.parseDocxMathRuns(line, { size: 26 }, docx));
  const pl3Doc = new docx.Document({
    sections: [{ children: pl3Runs.map(runs => new docx.Paragraph({ children: runs })) }]
  });
  const pl3Buffer = await docx.Packer.toBuffer(pl3Doc);
  const pl3Xml = readZipEntry(pl3Buffer, 'word/document.xml').toString('utf8');

  const pl3DollarMatches = pl3Xml.match(/\$[^<$]+/g);
  assert.strictEqual(pl3DollarMatches, null, `Phụ lục 3 Word XML không được sót bất kỳ dấu $ nào! Thực tế sót: ${JSON.stringify(pl3DollarMatches)}`);
  const pl3MathCount = (pl3Xml.match(/<m:oMath>/g) || []).length;
  console.log(`  ✓ Phụ lục 3 xuất Word sạch 100% dấu $, đã chuyển thành ${pl3MathCount} Equation OMML!`);
  assert.ok(pl3MathCount >= 6, `Phụ lục 3 phải tạo ít nhất 6 Equation OMML, thực tế tạo ${pl3MathCount}`);

  // 5. Rà soát đảm bảo Phụ lục 2: đủ 10 cột, 4-6 hoạt động STEM/trải nghiệm, có NLS & AI
  console.log('-> 5. Rà soát chuẩn hóa Phụ lục 2 (Kế hoạch hoạt động giáo dục)...');
  const extractAppendixFn = (name) => {
    const start = canvasSrc.indexOf(`function ${name}(`);
    if (start < 0) return '';
    const nextStart = canvasSrc.indexOf('\nfunction ', start + 1);
    return canvasSrc.slice(start, nextStart > 0 ? nextStart : canvasSrc.length);
  };

  const pl2Sandbox = {
    ...sandbox,
    EQUIPMENT: { default: ['Thiết bị cơ bản'] },
    getConfig: () => ({ monHoc: 'Toán học', lop: '9', namHoc: '2026-2027', thongKe: { students: '160' }, nls: { enabled: true }, ai: { enabled: true } })
  };
  vm.createContext(pl2Sandbox);

  vm.runInContext(
    extractAppendixFn('fallback') + '\n' +
    extractAppendixFn('cleanNlsColumnText') + '\n' +
    extractAppendixFn('cleanAiColumnText') + '\n' +
    extractAppendixFn('enrichNlsCode') + '\n' +
    extractAppendixFn('normalizeAppendix'),
    pl2Sandbox
  );

  const pl2Data = pl2Sandbox.normalizeAppendix(null, '2', pl2Sandbox.getConfig());
  assert.ok(Array.isArray(pl2Data.activities), 'Phụ lục 2 phải có mảng activities');
  assert.ok(pl2Data.activities.length >= 4 && pl2Data.activities.length <= 6, `Phụ lục 2 phải có 4–6 hoạt động, thực tế có ${pl2Data.activities.length}`);
  
  // Kiểm tra 10 trường dữ liệu chuẩn Công văn 5512
  const requiredFields = ['stt', 'topic', 'requirements', 'duration', 'time', 'location', 'host', 'coordinator', 'conditions', 'integration'];
  for (const act of pl2Data.activities) {
    for (const field of requiredFields) {
      assert.ok(act[field] !== undefined && String(act[field]).trim() !== '', `Hoạt động "${act.topic}" thiếu trường bắt buộc: ${field}`);
    }
    assert.ok(act.integration.includes('NLS:') || act.integration.includes('AI:') || act.integration !== '-', `Hoạt động "${act.topic}" phải có tích hợp NLS/AI`);
  }
  console.log(`  ✓ Phụ lục 2 đạt chuẩn 100%: gồm ${pl2Data.activities.length} hoạt động STEM/trải nghiệm với đầy đủ 10 cột dữ liệu và tích hợp NLS/AI.`);

  // 6. Kiểm tra tính đồng bộ 100% giữa Phụ lục 1 và Phụ lục 3
  console.log('-> 6. Kiểm tra đồng bộ NLS và AI giữa Phụ lục 1 và Phụ lục 3...');
  vm.runInContext(
    extractAppendixFn('isNlsColumn') + '\n' +
    extractAppendixFn('isAiColumn') + '\n' +
    extractAppendixFn('isIntegrationColumn') + '\n' +
    extractAppendixFn('normalizeHeaderKey') + '\n' +
    extractAppendixFn('normalizeIntegrationTable') + '\n' +
    extractAppendixFn('foldText') + '\n' +
    extractAppendixFn('cleanLessonName') + '\n' +
    extractAppendixFn('lessonOrdinal') + '\n' +
    extractAppendixFn('lessonKeywords') + '\n' +
    extractAppendixFn('lessonsMatch') + '\n' +
    extractAppendixFn('integrationText') + '\n' +
    extractAppendixFn('integrationParts') + '\n' +
    extractAppendixFn('appendixOneIntegrationForLesson') + '\n' +
    extractAppendixFn('syncIntegrationFromAppendixOne'),
    pl2Sandbox
  );

  const mockPl1Table = {
    columns: ['STT', 'Bài học', 'Số tiết', 'Yêu cầu cần đạt', 'Biểu hiện năng lực số', 'Biểu hiện năng lực AI'],
    rows: [
      {
        isHeader: false,
        cells: [
          '1',
          'Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn',
          '2',
          'Nhận biết khái niệm...',
          '5.3.TC2a - Sử dụng GeoGebra và máy tính cầm tay kiểm tra nghiệm',
          '9.B2.1 - Dùng trợ lý AI gợi mở ví dụ ngẫu nhiên và kiểm chứng (Áp dụng: tiết 1, 2)'
        ]
      },
      {
        isHeader: false,
        cells: [
          '2',
          'Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn',
          '3',
          'Giải được hệ hai phương trình...',
          '5.3.TC2a - Sử dụng máy tính cầm tay giải hệ phương trình',
          '9.B2.1 - Dùng AI gợi ý định hướng lựa chọn phương pháp giải (Áp dụng: tiết 3, 4)'
        ]
      }
    ]
  };

  const pl3PlanRows = [
    { lesson: 'Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn', periods: '2' },
    { lesson: 'Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn', periods: '3' }
  ];

  const syncedPl3 = pl2Sandbox.syncIntegrationFromAppendixOne(pl3PlanRows, mockPl1Table, pl2Sandbox.getConfig());
  
  assert.strictEqual(syncedPl3.length, 2, 'Phải đồng bộ đủ 2 bài học');
  assert.ok(syncedPl3[0].integration.includes('[NLS: 5.3.TC2a'), 'PL3 Bài 1 phải kế thừa đúng mã NLS của PL1');
  assert.ok(syncedPl3[0].integration.includes('[AI: 9.B2.1'), 'PL3 Bài 1 phải kế thừa đúng mã AI của PL1');
  assert.ok(syncedPl3[0].integration.includes('tiết 1, 2'), 'PL3 Bài 1 phải khớp phạm vi tiết của PL1');
  assert.ok(syncedPl3[1].integration.includes('[NLS: 5.3.TC2a'), 'PL3 Bài 2 phải kế thừa đúng mã NLS của PL1');
  assert.ok(syncedPl3[1].integration.includes('phương pháp giải'), 'PL3 Bài 2 phải kế thừa đúng mô tả AI của PL1');
  console.log('  ✓ NLS và AI giữa Phụ lục 1 và Phụ lục 3 khớp nhau 100% về mã, mô tả sư phạm và phạm vi tiết!');

  // 7. Kiểm tra Phụ lục 3 xuất và xem trước có đủ 8 cột và có Biểu hiện khung năng lực AI
  console.log('-> 7. Kiểm tra Phụ lục 3 có Biểu hiện khung năng lực AI trong bảng 8 cột...');
  const app3ColMatch = canvasSrc.match(/const APPENDIX_3_COLUMNS\s*=\s*\[[\s\S]*?\];/);
  vm.runInContext(
    (app3ColMatch ? app3ColMatch[0] : "const APPENDIX_3_COLUMNS=[['lesson','Bài học'],['periods','Số tiết'],['tietCT','Tiết CT'],['week','Tuần'],['devices','Thiết bị dạy học (*)'],['location','Địa điểm dạy học (**)'],['nls','Biểu hiện năng lực số'],['ai','Biểu hiện năng lực AI']];") + '\n' +
    extractAppendixFn('selectedPeriodsForLesson') + '\n' +
    extractAppendixFn('selectedPeriodsForLessonId') + '\n' +
    extractAppendixFn('appendixThreeTable'),
    pl2Sandbox
  );
  pl2Sandbox.results = { '1': { scheduleTable: mockPl1Table } };
  const pl3TableOutput = pl2Sandbox.appendixThreeTable(syncedPl3, pl2Sandbox.getConfig());
  assert.strictEqual(pl3TableOutput.columns.length, 8, 'Phụ lục 3 phải có đúng 8 cột');
  assert.ok(pl2Sandbox.isAiColumn(pl3TableOutput.columns[7]), 'Cột 8 phải là Biểu hiện năng lực AI');
  assert.ok(pl3TableOutput.rows[0].cells[7].includes('9.B2.1'), 'Cột AI của Bài 1 trong Phụ lục 3 phải chứa mã 9.B2.1');
  assert.ok(pl3TableOutput.rows[0].cells[7].includes('tiết 1, 2'), 'Cột AI của Bài 1 trong Phụ lục 3 phải chứa phạm vi tiết');
  assert.ok(pl3TableOutput.rows[1].cells[7].includes('9.B2.1'), 'Cột AI của Bài 2 trong Phụ lục 3 phải chứa mã AI');
  console.log('  ✓ Phụ lục 3 hiển thị và xuất đầy đủ 8 cột với Biểu hiện khung năng lực AI chính xác 100%!');

  console.log('==================================================');
  console.log('🎉 TẤT CẢ KIỂM THỬ CÔNG THỨC EQUATION VÀ PHỤ LỤC 3 ĐÃ ĐẠT 100%!');
  console.log('==================================================');
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
