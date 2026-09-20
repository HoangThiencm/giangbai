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

const dumpedLeft = [
  '+ Bước 1: Chuyển giao. **GV:** Giao việc. **HS:** Nhận nhiệm vụ.<br>+ Bước 2: Thực hiện. **HS:** Làm việc nhóm. **GV:** Quan sát.<br>+ Bước 3: Báo cáo. **HS:** Trình bày. **GV:** Chốt.<br>+ Bước 4: Kết luận. **GV:** Nhận xét. **HS:** Ghi nội dung cốt lõi. / 2. PHƯƠNG PHÁP CỘNG ĐẠI SỐ<br>Quy tắc giải: Cộng từng vế.<br>Ví dụ 4: Giải hệ.<br>Lời giải: x = 1; y = 2.',
  '---'
];
const [rescuedLeft, rescuedRight] = generator.semanticSplitActivityRow(dumpedLeft);
assert.match(rescuedLeft, /Bước 4/, 'Cột trái giữ Bước 4');
assert.doesNotMatch(rescuedLeft, /PHƯƠNG PHÁP CỘNG ĐẠI SỐ/, 'Kiến thức ghi bảng không còn ở cột trái');
assert.match(rescuedRight, /PHƯƠNG PHÁP CỘNG ĐẠI SỐ/, 'Cột 2 rỗng/--- được cứu bằng kiến thức từ cột 1');
assert.match(rescuedRight, /Quy tắc giải/, 'Quy tắc chuyển sang cột 2');

const numberedKnowledgeSplit = generator.semanticSplitActivityRow([
  '+ Bước 1: Chuyển giao.<br>+ Bước 2: Thực hiện.<br>+ Bước 3: Báo cáo.<br>+ Bước 4: Kết luận.',
  '1. Các bước giải bài toán bằng cách lập hệ phương trình<br>- Lập hệ phương trình.',
  'Ví dụ: Vòi I chảy riêng trong 2 giờ, vòi II trong 4 giờ.'
]);
assert.doesNotMatch(numberedKnowledgeSplit[0], /Các bước giải bài toán/, 'Tiêu đề kiến thức đánh số không được lẫn vào cột trái');
assert.match(numberedKnowledgeSplit[1], /Các bước giải bài toán/, 'Tiêu đề kiến thức đánh số phải ở cột phải');
assert.match(numberedKnowledgeSplit[1], /Vòi I chảy riêng/, 'Nội dung kiến thức tiếp theo phải ở cột phải');

const {
  ensureActivityFourPartStructure,
  repairActivityTablesRightColumn
} = require('../js/khbd-app.js');
const missingFour = `## D. HOẠT ĐỘNG 4: VẬN DỤNG (18 phút)
- Mục tiêu: Vận dụng giải quyết bài toán thực tế.
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: **GV:** "Các em giải bài vận dụng." **HS:** Nhận đề.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Làm việc nhóm. **GV:** Quan sát.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Trình bày nghiệm. **GV:** Nhận xét.<br>+ Bước 4: Kết luận, nhận định: **GV:** Chốt. **HS:** Ghi bài. | --- |`;
const restored = ensureActivityFourPartStructure(missingFour, 'D');
assert.match(restored, /#{3,4}\s*a\) Mục tiêu/, 'Chuẩn hóa heading mục tiêu');
assert.match(restored, /#{3,4}\s*b\) Nội dung/, 'Tự thêm b) Nội dung');
assert.match(restored, /#{3,4}\s*c\) Sản phẩm/, 'Tự thêm c) Sản phẩm');
assert.match(restored, /#{3,4}\s*d\) Tổ chức thực hiện/, 'Tự thêm d) Tổ chức thực hiện');
const repairedTable = repairActivityTablesRightColumn(restored);
const dataRow = repairedTable.split('\n').find(line => /Bước 1/.test(line));
assert.ok(dataRow, 'Còn hàng dữ liệu bảng sau rescue');
assert.ok(!/\|\s*---\s*\|$/.test(dataRow.trim()), 'Cột 2 của hàng dữ liệu không còn ---');

// Hoạt động B thiếu a) Mục tiêu: phải tự bổ sung; không slice(0,400); giữ đủ 4 bước.
const latexRight = '$-5x^2y$; $x^3 - \\frac{1}{2}$ — Bậc của đơn thức (cấp số nhân đầy đủ không bị cắt)';
const missingAOnB = `## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (45 phút)
### Hoạt động 2.1: Đơn thức (20 phút)
#### b) Nội dung:
- Học sinh khám phá khái niệm đơn thức trong SGK.
#### c) Sản phẩm:
- Định nghĩa và ví dụ đơn thức.
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: **GV:** "Các em đọc mục Đơn thức." **HS:** Nhận nhiệm vụ.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Làm việc cá nhân rồi thảo luận nhóm. **GV:** Quan sát.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Trình bày. **GV:** Nhận xét.<br>+ Bước 4: Kết luận, nhận định: **GV:** Chốt. **HS:** Ghi bài. | ${latexRight} |`;
const restoredB = ensureActivityFourPartStructure(missingAOnB, 'B');
assert.match(restoredB, /#### a\) Mục tiêu:/, 'Hoạt động B thiếu a) phải tự bổ sung #### a) Mục tiêu');
assert.match(restoredB, /#### b\) Nội dung:/, 'Hoạt động B giữ b) Nội dung');
assert.match(restoredB, /#### c\) Sản phẩm:/, 'Hoạt động B giữ c) Sản phẩm');
assert.match(restoredB, /#### d\) Tổ chức thực hiện:/, 'Hoạt động B có d) Tổ chức thực hiện trước bảng');
assert.match(restoredB, /Bước 1:[\s\S]*Bước 2:[\s\S]*Bước 3:[\s\S]*Bước 4:/, 'Bảng Cột 1 giữ nguyên đủ 4 bước');
assert.match(restoredB, /\$-5x\^2y\$/, 'Không cắt xén LaTeX cột phải bằng slice(0, 400)');
assert.match(restoredB, /Bậc của đơn thức \(cấp số nhân đầy đủ không bị cắt\)/, 'Không đứt cụt câu chữ cột phải');
assert.doesNotMatch(
  fs.readFileSync(path.join(__dirname, '..', 'js', 'khbd-app.js'), 'utf8').match(/function repairActivityBlockFourParts[\s\S]*?\nfunction ensureActivityFourPartStructure/)[0],
  /\.slice\(0,\s*400\)/,
  'repairActivityBlockFourParts không còn .slice(0, 400)'
);

const promptsSrc = fs.readFileSync(path.join(__dirname, '..', 'js', 'khbd-prompts.js'), 'utf8');
assert.match(promptsSrc, /ACTIVITY_TABLE_CONTRACT_COMPACT[\s\S]*?#### a\) Mục tiêu:/, 'COMPACT bắt buộc #### a) Mục tiêu');
assert.match(promptsSrc, /ACTIVITY_TABLE_CONTRACT_COMPACT[\s\S]*?\+ Bước 1: Chuyển giao nhiệm vụ:/, 'COMPACT bắt buộc Bước 1 quy chuẩn');
assert.match(promptsSrc, /ACTIVITY_TABLE_CONTRACT_COMPACT[\s\S]*?\+ Bước 4: Kết luận, nhận định:/, 'COMPACT bắt buộc Bước 4 quy chuẩn');

console.log('khbd-table-columns-smoke: passed');
