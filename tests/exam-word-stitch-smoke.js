/** Smoke: lọc đề theo lớp + Word 20 câu không bị nuốt khi tổng hợp. Node 18+. */
'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'thitructuyen.html'), 'utf8');
const stitchSrc = fs.readFileSync(path.join(root, 'exam-stitch-client.js'), 'utf8');

console.log('================================================================================');
console.log('KIỂM THỬ LỌC THEO LỚP & GIỮ NGUYÊN 20 CÂU WORD Ở TỔNG HỢP');
console.log('================================================================================');

console.log('\n[TEST 1] Giao diện lọc theo lớp trên TeacherDashboard...');
assert.match(html, /const \[classFilter, setClassFilter\]/, 'Phải có state classFilter');
assert.match(html, /aria-label="Lọc theo lớp"/, 'Dropdown phải có nhãn Lọc theo lớp');
assert.match(html, /Tất cả các lớp/, 'Phải có lựa chọn Tất cả các lớp');
assert.match(html, /Thí sinh tự do/, 'Phải có lựa chọn Thí sinh tự do');
assert.match(html, /const matchesClassFilter/, 'Phải có hàm matchesClassFilter');
assert.match(html, /matchesClassFilter\(ex, classFilter\)/, 'filteredExams phải lọc theo lớp');
assert.match(html, /examUrl\("student-classes"\)/, 'Phải lấy danh sách lớp phân công');
assert.match(html, /classFilterOptions/, 'Phải gộp lớp từ đề đã tạo và lớp được phân công');
assert.doesNotMatch(html, /StudentView[\s\S]{0,200}classFilter/, 'Không đổi giao diện StudentView bằng classFilter');
console.log('✓ Dropdown lọc theo lớp có đủ lựa chọn và logic.');

console.log('\n[TEST 2] isDuplicate không còn so sánh index 0.85...');
assert.doesNotMatch(stitchSrc, /same \/ maxLen\) > 0\.85/, 'Đã bỏ ngưỡng 0.85 theo vị trí ký tự');
assert.match(stitchSrc, /pairSimilarity\(qA, qB\) > 0\.98/, 'Trùng câu hỏi phải > 98%');
assert.match(stitchSrc, /pairSimilarity\(oA, oB\) > 0\.98/, 'Trùng đáp án phải > 98%');
assert.match(stitchSrc, /skipDedupe = pages\.length <= 1/, 'Word 1 trang không chạy lọc trùng');
console.log('✓ Thuật toán dedupe đã siết chặt.');

console.log('\n[TEST 3] 20 câu Word toán có mở đầu giống nhau vẫn đủ 20/20...');
require(path.join(root, 'exam-stitch-client.js'));
const stitch = global.ExamStitch;
assert.ok(stitch && typeof stitch.isDuplicate === 'function', 'ExamStitch phải load được trong Node');

const makeQ = (n) => ({
    question: `Tính giá trị biểu thức sau: $${n} + ${n + 1}$`,
    options: [`${2 * n + 1}`, `${2 * n}`, `${n}`, `${n + 3}`],
    correct_index: 0
});
const twenty = Array.from({ length: 20 }, (_, i) => makeQ(i + 1));
const pageId = 'imported';
const pages = [{ id: pageId, page_index: 1 }];
const pageQuestions = { [pageId]: twenty };

assert.strictEqual(stitch.flattenStitchedQuestions(pageQuestions, pages).length, 20, 'Word 1 trang: Tổng hợp phải giữ 20/20');
assert.strictEqual(stitch.dedupeQuestions(twenty).length, 20, '20 câu khác đáp án không bị xóa vì tiền tố giống nhau');

const qA = makeQ(1);
const qB = makeQ(2);
assert.strictEqual(stitch.isDuplicate(qA, qB), false, 'Hai câu toán khác nhau không được coi là trùng');
assert.strictEqual(stitch.isDuplicate(qA, { ...qA, options: [...qA.options] }), true, 'Cùng câu và cùng 4 đáp án mới là trùng');
console.log('✓ 20 câu Word được giữ nguyên 20/20.');

console.log('\n================================================================================');
console.log('TẤT CẢ KIỂM THỬ LỌC LỚP & WORD 20 CÂU ĐÃ PASS 100%!');
console.log('================================================================================');
