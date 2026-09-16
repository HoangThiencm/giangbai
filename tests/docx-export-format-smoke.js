/** Smoke: header/footer/lề/spacing Word KHBD. Node 18+. */
'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

function loadDocx() {
  try { return require('docx'); } catch (projectDependencyError) {
    const runtimeModule = path.join(process.env.USERPROFILE || '', '.cache', 'codex-runtimes', 'codex-primary-runtime', 'dependencies', 'node', 'node_modules', 'docx');
    if (fs.existsSync(runtimeModule)) return require(runtimeModule);
    throw projectDependencyError;
  }
}

const docx = loadDocx();
global.window = { docx };
const { DocxGenerator } = require('../js/khbd-docx.js');
const generator = new DocxGenerator();

console.log('================================================================================');
console.log('KIỂM THỬ XUẤT WORD KHBD: LỀ, HEADER, FOOTER, TIẾT DẠY');
console.log('================================================================================');

assert.strictEqual(generator.pageMargins.top, 850);
assert.strictEqual(generator.pageMargins.bottom, 850);
assert.strictEqual(generator.pageMargins.left, 1134);
assert.strictEqual(generator.pageMargins.right, 850);
assert.strictEqual(generator.lineSpacing, 240);
assert.strictEqual(generator.spaceAfter, 60);
assert.strictEqual(generator.spaceBefore, 0);
assert.strictEqual(generator.tableWidth, 9922);
assert.deepStrictEqual(generator.columnWidths, [4961, 4961]);
console.log('✓ Lề 1.5/1.5/2.0/1.5 cm, spacing After 3pt, Single, bảng 9922.');

const header = generator.createDocumentHeader({
  school: 'THCS Trần Phú',
  teacher: 'Hoàng Tấn Thiên',
  chapter: 'Chương I: Tập hợp các số tự nhiên',
  topic: 'Bài 1: Tập hợp',
  lessonScope: 'Tiết 1',
  duration: '2 tiết (90 phút)',
  subject: 'Toán',
  academicYear: '2026-2027'
});
const headerDump = JSON.stringify(header);
assert.match(headerDump, /Trường THCS Trần Phú/);
assert.match(headerDump, /Giáo viên: Hoàng Tấn Thiên/);
assert.match(headerDump, /CHƯƠNG I: TẬP HỢP CÁC SỐ TỰ NHIÊN/);
assert.match(headerDump, /TIẾT 1/);
assert.match(headerDump, /BÀI 1/);
assert.match(headerDump, /TẬP HỢP/);
assert.match(headerDump, /Thời lượng thực hiện: 2 tiết \(90 phút\)/);

const noChapter = JSON.stringify(generator.createDocumentHeader({
  school: 'THCS Trần Phú',
  teacher: 'Hoàng Tấn Thiên',
  topic: 'Tập hợp',
  duration: '01 tiết (45 phút)'
}));
assert.doesNotMatch(noChapter, /CHƯƠNG/);
assert.match(noChapter, /BÀI: TẬP HỢP/);
console.log('✓ Header 2 cột Trường/GV, Chương, TIẾT-BÀI, thời lượng; ẩn Chương khi thiếu.');

const footer = generator.createDocumentFooter({
  subject: 'Toán',
  academicYear: '2026-2027'
});
const footerDump = JSON.stringify(footer);
assert.match(footerDump, /Môn: Toán/);
assert.match(footerDump, /Năm học: 2026-2027/);
assert.match(footerDump, /Trang/);
console.log('✓ Footer Môn / Trang / Năm học.');

const src = fs.readFileSync(path.join(__dirname, '..', 'js', 'khbd-docx.js'), 'utf8');
assert.match(src, /headers = \{ default: new Header/);
assert.match(src, /footers = \{ default: new Footer/);
assert.match(src, /AlignmentType\?\.JUSTIFIED/);
const app = fs.readFileSync(path.join(__dirname, '..', 'js', 'khbd-app.js'), 'utf8');
assert.match(app, /lessonScope:\s*appState\.teachingContext\.lessonScope/);
assert.match(src, /parseInlineTextToRuns\(headingText, runColor, \{ size: this\.fontSizeH3/);
assert.match(src, /parseInlineTextToRuns\(headingText, runColor, \{ size: this\.fontSizeH2/);
assert.match(src, /parseInlineTextToRuns\(headingText, runColor \|\| "111111"/);
console.log('✓ exportFullLessonPlan dùng header/footer Word và truyền tiết dạy.');

function collectRuns(node, acc = []) {
  if (!node) return acc;
  if (Array.isArray(node)) {
    node.forEach(item => collectRuns(item, acc));
    return acc;
  }
  if (node.rootKey === 'w:r') acc.push(node);
  if (node.root) collectRuns(node.root, acc);
  return acc;
}
function runText(run) {
  const parts = [];
  (function walk(node) {
    if (!node) return;
    if (Array.isArray(node)) return node.forEach(walk);
    if (node.rootKey === 'w:t' && Array.isArray(node.root)) {
      node.root.forEach(item => { if (typeof item === 'string') parts.push(item); });
    }
    if (node.root) walk(node.root);
  })(run);
  return parts.join('');
}
function hasFormatting(run, tag) {
  const dump = JSON.stringify(run);
  return dump.includes(`"rootKey":"${tag}"`);
}
const nlsHeadingMd = '### c) Năng lực số: ***[5.3.TC2a]:*** Sử dụng máy tính cầm tay (phím CALC) để kiểm tra cặp số (x; y) có là nghiệm của hệ phương trình hay không.';
const aiHeadingMd = '### d) Năng lực AI: ***[9.B2.1]:*** Sử dụng trợ lý AI tạo các ví dụ ngẫu nhiên về phương trình để luyện tập nhận biết khái niệm và chịu trách nhiệm kiểm chứng kết quả (Áp dụng: tiết 1, 2).';
const headingElements = generator.parseMarkdownToDocxElements(`${nlsHeadingMd}\n${aiHeadingMd}`);
const headingDump = JSON.stringify(headingElements);
const headingRuns = collectRuns(headingElements);
const headingPlain = headingRuns.map(runText).join('');
assert.ok(!headingPlain.includes('***') && !headingDump.includes('***['), 'Tiêu đề Word không còn ký tự thô ***');
assert.ok(headingPlain.includes('[5.3.TC2a]'), 'Word phải giữ mã NLS 5.3.TC2a');
assert.ok(headingPlain.includes('[9.B2.1]'), 'Word phải giữ mã AI 9.B2.1');
const nlsCodeRun = headingRuns.find(run => runText(run).includes('[5.3.TC2a]'));
const aiCodeRun = headingRuns.find(run => runText(run).includes('[9.B2.1]'));
assert.ok(nlsCodeRun, 'Phải có TextRun chứa [5.3.TC2a]');
assert.ok(aiCodeRun, 'Phải có TextRun chứa [9.B2.1]');
assert.ok(hasFormatting(nlsCodeRun, 'w:b') && hasFormatting(nlsCodeRun, 'w:i'), '[5.3.TC2a] phải in đậm và in nghiêng');
assert.ok(hasFormatting(aiCodeRun, 'w:b') && hasFormatting(aiCodeRun, 'w:i'), '[9.B2.1] phải in đậm và in nghiêng');
assert.match(JSON.stringify(nlsCodeRun), /0369A1/i, '[5.3.TC2a] phải màu xanh 0369A1');
assert.match(JSON.stringify(aiCodeRun), /6D28D9/i, '[9.B2.1] phải màu tím 6D28D9');
console.log('✓ Tiêu đề NLS/AI trong Word bóc *** và giữ in đậm/nghiêng đúng màu.');

console.log('\n================================================================================');
console.log('TẤT CẢ KIỂM THỬ XUẤT WORD KHBD ĐÃ PASS 100%!');
console.log('================================================================================');
