'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

class DocxValue { constructor(options) { this.options = options; } }
global.window = {
  docx: {
    Table: DocxValue, TableRow: DocxValue, TableCell: DocxValue, Paragraph: DocxValue, TextRun: DocxValue,
    WidthType: { DXA: 'dxa' }, BorderStyle: { SINGLE: 'single' }, VerticalAlign: { TOP: 'top' }, TableLayoutType: { FIXED: 'fixed' }
  }
};

const { DocxGenerator } = require('../js/khbd-docx.js');
const generator = new DocxGenerator();
const table = generator.createDocxTableFromMarkdown([
  '| Hoạt động của GV và HS | Nội dung |',
  '| :--- | :--- |',
  '| **GV:** Nêu nhiệm vụ | $|-5| = 5$ | Ghi nhớ |'
]);

assert.deepStrictEqual(table.options.columnWidths, [6426, 3213]);
const styles = fs.readFileSync(path.join(__dirname, '..', 'css', 'khbd-styles.css'), 'utf8');
assert.match(styles, /th:first-child:nth-last-child\(2\)[\s\S]*?width:\s*66\.67%/, 'Preview left column must be 66.67%');
assert.match(styles, /th:last-child:nth-child\(2\)[\s\S]*?width:\s*33\.33%/, 'Preview right column must be 33.33%');
assert.strictEqual(table.options.rows[0].options.children.length, 2, 'Header phải có đúng 2 cột');
assert.strictEqual(table.options.rows[1].options.children.length, 2, 'Dữ liệu phải có đúng 2 cột');
const rightCell = table.options.rows[1].options.children[1];
const rightText = rightCell.options.children.map(p => p.options.children.map(run => run.options.text || '').join('')).join('');
assert.match(rightText, /\|-5\| = 5/, 'Công thức trị tuyệt đối nằm cột Nội dung');
assert.match(rightText, /Ghi nhớ/, 'Ghi nhớ nằm cột Nội dung');

const leftCell0 = table.options.rows[1].options.children[0];
const leftText0 = leftCell0.options.children.map(p => p.options.children.map(run => run.options.text || '').join('')).join('');
assert.match(leftText0, /GV/, 'Cột trái giữ kịch bản GV');

const pipeInLeft = [
  '+ Bước 1: Chuyển giao. **GV:** Giao việc. **HS:** Nhận nhiệm vụ.',
  '+ Bước 2: Thực hiện (Số luống',
  'Số cây/luống',
  'Tổng số cây) **GV:** Hướng dẫn lập bảng. **HS:** Điền số liệu.<br>+ Bước 3: Báo cáo. **HS:** Trình bày.<br>+ Bước 4: Kết luận. **GV:** Chốt kiến thức.',
  '**Hệ phương trình**<br>Định nghĩa: nghiệm của hệ.'
];
const [leftPipe, rightPipe] = generator.semanticSplitActivityRow(pipeInLeft);
assert.match(leftPipe, /Bước 2/, 'Bước 2 ở cột trái');
assert.match(leftPipe, /Bước 3/, 'Bước 3 ở cột trái dù có dấu | nội dung');
assert.match(leftPipe, /Bước 4/, 'Bước 4 ở cột trái');
assert.match(leftPipe, /Số cây\/luống/, 'Mảnh bảng nháp còn ở cột trái');
assert.doesNotMatch(rightPipe, /Bước 3/, 'Cột phải không chứa Bước 3');
assert.doesNotMatch(rightPipe, /Bước 4/, 'Cột phải không chứa Bước 4');
assert.match(rightPipe, /Hệ phương trình/, 'Cột phải là kiến thức ghi bảng');

const activityTable = generator.createDocxTableFromMarkdown([
  '| Hoạt động của GV và HS | Nội dung |',
  '| :--- | :--- |',
  `| ${pipeInLeft[0]} ${pipeInLeft.slice(1, 4).join(' | ')} | ${pipeInLeft[4]} |`
]);
function cellText(row, col) {
  return activityTable.options.rows[row].options.children[col].options.children
    .map(p => p.options.children.map(run => run.options.text || '').join('')).join('');
}
assert.match(cellText(1, 0), /Bước 3/, 'Word: Bước 3 cột trái');
assert.match(cellText(1, 0), /Bước 4/, 'Word: Bước 4 cột trái');
assert.doesNotMatch(cellText(1, 1), /Bước 3/, 'Word: cột phải không có Bước 3');
assert.match(cellText(1, 1), /Hệ phương trình|Định nghĩa/, 'Word: cột phải là kiến thức');
console.log('khbd-table-columns-smoke: passed');
