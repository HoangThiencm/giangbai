const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const html = fs.readFileSync(path.join(__dirname, '../phancongtochuyenmon.html'), 'utf8');
for (const source of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)) new vm.Script(source[1]);

function declaration(name) {
    const start = html.lastIndexOf(`function ${name}(`);
    assert(start >= 0, `Không tìm thấy ${name}`);
    const next = html.indexOf('\n        function ', start + 1);
    return html.slice(start, next < 0 ? html.length : next);
}

const source = ['baoGiangDate', 'baoGiangWeekdayLabel', 'baoGiangSubjectKey', 'baoGiangKey', 'parseBaoGiangCurriculumEntries', 'baoGiangExpandPeriodNumbers', 'parseBaoGiangCurriculum', 'normalizeBaoGiangLessonTitle'].map(declaration).join('\n');
const context = vm.createContext({ Map, Date, String, Number, Array, foldText: value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase().replace(/\s+/g, ' ').trim() });
vm.runInContext(source, context);

const plan = vm.runInContext(`parseBaoGiangCurriculum([
    '9 | Toán | 1 | 1 | Hình học | Bài 11. Tỉ số lượng giác của góc nhọn | 1',
    '9 | Toán | 2 | 2-3 | Hình học | Bài 11. Tỉ số lượng giác của góc nhọn (tiếp theo) | 2'
].join('\\n')).get(baoGiangKey('9', 'Toán')).all`, context);
assert.deepEqual(JSON.parse(JSON.stringify(plan.map(item => [item.ppct, item.segment]))), [['1', '1/3'], ['2', '2/3'], ['3', '3/3']]);
const interleavedPlan = vm.runInContext(`parseBaoGiangCurriculum([
    '9 | Toán | 1 | 1-2 | Đại số | Bài 1. Căn bậc hai | 2',
    '9 | Toán | 1 | 1 | Hình học | Bài 11. Tỉ số lượng giác của góc nhọn | 1',
    '9 | Toán | 2 | 3-4 | Đại số | Bài 2. Hàm số | 2',
    '9 | Toán | 2 | 2-3 | Hình học | Bài 11. Tỉ số lượng giác của góc nhọn (tiếp theo) | 2'
].join('\\n')).get(baoGiangKey('9', 'Toán')).all
    .filter(item => item.strand === 'Hình học')`, context);
assert.deepEqual(JSON.parse(JSON.stringify(interleavedPlan.map(item => [item.week, item.ppct, item.segment]))), [[1, '1', '1/3'], [2, '2', '2/3'], [2, '3', '3/3']]);
assert.equal(vm.runInContext("baoGiangWeekdayLabel('2026-09-09')", context), 'Thứ Tư');
assert.match(html, /id="qp-inherit-assignments"(?! checked)/);
assert.match(html, /assignments: \{\}, timetable: emptyTimetable\(\)/);
assert.match(html, /baoGiangWeekdayLabel\(row\.date\)\}, \$\{formatVnDate\(row\.date\)\}/);
console.log('PASS: PPCT đa tuần, kể cả khi Đại số và Hình học xen kẽ, có phân đoạn 1/3, 2/3, 3/3.');
