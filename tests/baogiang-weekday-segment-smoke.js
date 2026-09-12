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

const source = ['baoGiangDate', 'baoGiangWeekdayLabel', 'baoGiangSubjectKey', 'baoGiangKey', 'parseBaoGiangCurriculumEntries', 'baoGiangExpandPeriodNumbers', 'parseBaoGiangCurriculum', 'normalizeBaoGiangLessonTitle', 'formatBaoGiangLessonDisplay'].map(declaration).join('\n');
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
const threeWeekPlan = vm.runInContext(`parseBaoGiangCurriculum([
    '9 | Toán | 4 | 6 | Hình học | Bài 11. Tỉ số lượng giác của góc nhọn | 1',
    '9 | Toán | 5 | 7 | Hình học | Bài 11. Tỉ số lượng giác của góc nhọn (tiếp theo) | 1',
    '9 | Toán | 6 | 8 | Hình học | Bài 11. Tỉ số lượng giác của góc nhọn (tiếp theo) | 1'
].join('\\n')).get(baoGiangKey('9', 'Toán')).all`, context);
assert.deepEqual(JSON.parse(JSON.stringify(threeWeekPlan.map(item => [item.week, item.ppct, item.segment]))), [[4, '6', '1/3'], [5, '7', '2/3'], [6, '8', '3/3']]);
assert.equal(vm.runInContext("formatBaoGiangLessonDisplay({ teaching_week: 4, lesson: { lesson: 'Bài 11. Tỉ số lượng giác của góc nhọn', ppct: '6', segment: '1/3' } })", context), 'Tuần 4  Bài 11. Tỉ số lượng giác của góc nhọn (tiết ppct: 6) 1/3');

const warningSource = ['baoGiangTeachingWeek', 'baoGiangGrade', 'baoGiangPlanFor', 'decorateBaoGiangRows'].map(declaration).join('\n');
const warningContext = vm.createContext({
    Map, Set, Date, String, Number, Array,
    foldText: value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase().replace(/\s+/g, ' ').trim(),
    baoGiangDate: value => { const date = new Date(`${value}T00:00:00`); return Number.isNaN(date.getTime()) ? null : date; },
    baoGiangIso: date => `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`,
    baoGiangKey: (className, subject) => `${String(className).toUpperCase()}|${String(subject).toUpperCase()}`,
    baoGiangSubjectKey: value => String(value).toUpperCase(),
    parseBaoGiangCurriculum: () => new Map([['7|TOÁN', { all: [], byWeek: new Map([[1, [{ ppct: '1' }]], [2, [{ ppct: '2' }]]]), usesWeek: true }]]),
    baoGiangRows: () => [
        { date: '2026-09-07', class_name: '71', subject: 'Toán', teacher_name: 'Thầy A' },
        { date: '2026-09-07', class_name: '71', subject: 'Toán', teacher_name: 'Cô B' },
        { date: '2026-09-14', class_name: '71', subject: 'Toán', teacher_name: 'Thầy A' }
    ],
    state: { bao_giang: { start_date: '2026-09-07', curriculum_text: '' } }
});
vm.runInContext(warningSource, warningContext);
const warnings = vm.runInContext("decorateBaoGiangRows('2026-09-14', '2026-09-14')", warningContext);
assert.equal(warnings.warnings.length, 0, 'Tuần đã qua không được đưa vào cảnh báo');
const currentWeekWarnings = vm.runInContext("decorateBaoGiangRows('2026-09-14', '2026-09-07')", warningContext);
assert.match(currentWeekWarnings.warnings[0], /Phát hiện 2 giáo viên cùng có TKB gồm Thầy A, Cô B/);
assert.equal(vm.runInContext("baoGiangWeekdayLabel('2026-09-09')", context), 'Thứ Tư');
assert.match(html, /id="qp-inherit-assignments"(?! checked)/);
assert.match(html, /assignments: \{\}, timetable: emptyTimetable\(\)/);
assert.match(html, /baoGiangWeekdayLabel\(row\.date\)\}, \$\{formatVnDate\(row\.date\)\}/);
assert.match(html, /const htmlRows = scheduleRows\.map\(row => .*formatBaoGiangLessonDisplay\(row\)/);

// Khóa mốc Tuần 1: kiểm tra đúng các hàm cuối cùng đang được trang sử dụng,
// không chỉ các khai báo cũ nằm trước đó trong file.
const lockSource = ['baoGiangDate', 'baoGiangIso', 'isBaoGiangStartDateValid', 'updateBaoGiangSettings', 'unlockBaoGiangStartDate', 'lockBaoGiangStartDate'].map(declaration).join('\n');
const elements = {
    'bg-start-date': { value: '2026-09-07', disabled: false, readOnly: false, style: {} },
    'bg-curriculum': { value: '', style: {} },
    'bg-ppct-grade': { value: '', style: {} },
    'bg-ppct-subject': { value: '', style: {} }
};
let saves = 0;
let renders = 0;
let confirms = [];
const lockContext = vm.createContext({
    Date, String, Number, Array, Object, RegExp,
    state: { bao_giang: { start_date: '2026-09-07', start_date_locked: true, curriculum_text: '', ppct_default_grade: '', ppct_default_subject: '' } },
    document: { getElementById: id => elements[id] || null },
    saveToLocal: () => { saves += 1; },
    renderBaoGiangView: () => { renders += 1; },
    renderBaoGiangCurriculumLibrary: () => {},
    showToast: () => {},
    confirm: message => { confirms.push(message); return false; }
});
vm.runInContext(lockSource, lockContext);
assert.equal(vm.runInContext("isBaoGiangStartDateValid('2026-09-07')", lockContext), true);
assert.equal(vm.runInContext("isBaoGiangStartDateValid('2026-02-31')", lockContext), false);

const normalizeContext = vm.createContext({
    Date, String, Number, Array, Object, RegExp, JSON, Set,
    defaultState: { info: { morning_periods: '1-5', afternoon_periods: '1-4', current_phase_id: '' } },
    ROLE_DEFAULTS: {},
    getSubjectDutyType: () => 'core',
    normalizeTeacherTimetable: value => value || {}
});
vm.runInContext(['baoGiangDate', 'baoGiangIso', 'isBaoGiangStartDateValid', 'normalizeState'].map(declaration).join('\n'), normalizeContext);
const hydrated = vm.runInContext("normalizeState({ bao_giang: { start_date: '2026-09-07' } })", normalizeContext);
assert.equal(hydrated.bao_giang.start_date_locked, true, 'Ngày đã lưu trước khi nâng cấp phải tự khóa');

// Kể cả DOM bị script khác sửa, trạng thái khóa không được update settings ghi đè.
elements['bg-start-date'].value = '2026-09-14';
vm.runInContext('updateBaoGiangSettings(\'start-date\')', lockContext);
assert.equal(lockContext.state.bao_giang.start_date, '2026-09-07');

// Cancel giữ nguyên khóa; OK mới mở khóa và hiển thị đúng cảnh báo nghiêm ngặt.
vm.runInContext('unlockBaoGiangStartDate()', lockContext);
assert.equal(lockContext.state.bao_giang.start_date_locked, true);
assert.match(confirms[0], /CẢNH BÁO QUAN TRỌNG/);
lockContext.confirm = message => { confirms.push(message); return true; };
vm.runInContext('unlockBaoGiangStartDate()', lockContext);
assert.equal(lockContext.state.bao_giang.start_date_locked, false);
assert.equal(renders, 1);

// Chọn ngày mới phải tự lưu và khóa lại ngay; nút Khóa lại cũng khóa được ngày không đổi.
elements['bg-start-date'].value = '2026-09-14';
vm.runInContext('updateBaoGiangSettings(\'start-date\')', lockContext);
assert.equal(lockContext.state.bao_giang.start_date, '2026-09-14');
assert.equal(lockContext.state.bao_giang.start_date_locked, true);
lockContext.state.bao_giang.start_date_locked = false;
vm.runInContext('lockBaoGiangStartDate()', lockContext);
assert.equal(lockContext.state.bao_giang.start_date_locked, true);
assert.ok(saves >= 3);

assert.match(html, /Ngày bắt đầu áp dụng \(Tuần 1\)/);
assert.match(html, /id="bg-start-date-lock-status"/);
assert.match(html, /startInput\.disabled = startDateLocked/);
assert.match(html, /if \(source === 'start-date' && !data\.start_date_locked\)/);
assert.doesNotMatch(declaration('renderBaoGiangView'), /fallbackStart/);
console.log('PASS: PPCT đa tuần, cảnh báo hai giáo viên, và khóa mốc Tuần 1.');
