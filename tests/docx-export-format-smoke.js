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
console.log('✓ exportFullLessonPlan dùng header/footer Word và truyền tiết dạy.');

console.log('\n================================================================================');
console.log('TẤT CẢ KIỂM THỬ XUẤT WORD KHBD ĐÃ PASS 100%!');
console.log('================================================================================');
