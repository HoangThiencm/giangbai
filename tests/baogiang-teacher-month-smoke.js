const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(path.join(__dirname, '../phancongtochuyenmon.html'), 'utf8');
function declaration(name) { const start = html.lastIndexOf(`function ${name}(`); assert(start >= 0, name); const next = html.indexOf('\n        function ', start + 1); return html.slice(start, next < 0 ? html.length : next); }
const source = ['baoGiangDate','baoGiangIso','baoGiangMonthRange','baoGiangMonthTable','renderBaoGiangCalendarByDay','renderBaoGiangWeekGrid'].map(declaration).join('\n');
const context = vm.createContext({Date, String, Number, Array, Map, escapeHtml: value => String(value), baoGiangWeekdayLabel: () => 'Thứ Hai', formatVnDate: value => value});
vm.runInContext(source, context);
assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext("baoGiangMonthRange('2026-02')", context))), {start:'2026-02-01',end:'2026-02-28',month:'2026-02'});
const rows = [{date:'2026-09-07',session:'morning',period:1,class_name:'9A1',subject:'Toán',teacher_id:'gv-a',lesson:{ppct:'1',lesson:'Bài 1',segment:'1/1'}}];
assert.match(vm.runInContext('renderBaoGiangCalendarByDay(' + JSON.stringify(rows) + ')', context), /Buổi sáng/);
assert.match(vm.runInContext('renderBaoGiangWeekGrid(' + JSON.stringify(rows) + ')', context), /9A1/);
assert.match(html, /id="bg-filter-teacher"/);
assert.match(html, /id="bg-filter-month"/);
assert.match(html, /id="bg-view-mode"/);
assert.match(html, /function exportBaoGiangMonth\(/);
assert.match(html, /function getBaoGiangTeacherList\(/);
assert.match(html, /Tất cả giáo viên \(\$\{teachers\.length\} GV\)/);
assert.match(html, /Sang Tab Thời khóa biểu GV để nhập TKB cho thầy\/cô này/);
console.log('PASS: lọc GV, phạm vi tháng, lịch theo ngày và lưới tuần.');

function sliceFrom(name, untilMarker) {
    const start = html.lastIndexOf(`function ${name}(`);
    assert(start >= 0, name);
    const end = untilMarker ? html.indexOf(untilMarker, start) : html.indexOf('\n        function ', start + 1);
    assert(end > start, `Không cắt được ${name}`);
    return html.slice(start, end < 0 ? html.length : end);
}

const teacherHelpers = sliceFrom('getBaoGiangTeacherList', '\n        const baoGiangMonthRenderCore');
const phaseTeacher = { id: 'gv1', name: 'Nguyễn Văn A', role: 'GV', assignments: { toan: ['8A1'] }, timetable: {} };
const listCtx = vm.createContext({
    state: {
        teachers: [],
        subjects: [{ key: 'toan', name: 'Toán' }],
        info: { current_phase_id: 'phase_hk1_d1' },
        phase_assignments: { phase_hk1_d1: { teachers: [phaseTeacher] } }
    },
    systemData: { teachers: [] },
    JSON, Object, Array, String, Set, Map
});
vm.runInContext(teacherHelpers, listCtx);
const fallbackList = vm.runInContext('getBaoGiangTeacherList()', listCtx);
assert.equal(fallbackList.length, 1, 'Fallback đợt phân công phải ra 1 GV');
assert.equal(fallbackList[0].name, 'Nguyễn Văn A');
assert.equal(listCtx.state.teachers.length, 1, 'Phải đồng bộ ngược state.teachers từ đợt hiện tại');
assert.match(vm.runInContext('baoGiangTeacherOptionLabel(getBaoGiangTeacherList()[0])', listCtx), /Nguyễn Văn A \(GV \/ 1 lớp\)/);

const emptyRootOtherPhaseCtx = vm.createContext({
    state: {
        teachers: [],
        subjects: [],
        info: { current_phase_id: '' },
        phase_assignments: {
            phase_hk2_d1: { teachers: [{ id: 'gv2', name: 'Trần Thị B', role: 'TTCM', assignments: { van: ['9A1', '9A2'] } }] }
        }
    },
    systemData: { teachers: [] },
    JSON, Object, Array, String, Set, Map
});
vm.runInContext(teacherHelpers, emptyRootOtherPhaseCtx);
assert.equal(vm.runInContext('getBaoGiangTeacherList().length', emptyRootOtherPhaseCtx), 1);
assert.equal(emptyRootOtherPhaseCtx.state.teachers[0].name, 'Trần Thị B');

const systemFallbackCtx = vm.createContext({
    state: { teachers: [], subjects: [], info: {}, phase_assignments: {} },
    systemData: { teachers: [{ id: 'sys1', name: 'Lê Văn C', role: 'GV' }] },
    JSON, Object, Array, String, Set, Map
});
vm.runInContext(teacherHelpers, systemFallbackCtx);
assert.equal(vm.runInContext('getBaoGiangTeacherList()[0].id', systemFallbackCtx), 'sys1');
console.log('PASS: getBaoGiangTeacherList fallback từ phase_assignments và systemData.');

function makeEl(init = {}) {
    return { value: init.value || '', innerHTML: init.innerHTML || '', disabled: false, readOnly: false, style: {} };
}
function mockDocument(map) {
    return { getElementById: id => map[id] || null };
}
function monthViewContext(overrides) {
    const els = {
        'bg-start-date': makeEl({ value: '2026-09-01' }),
        'bg-curriculum': makeEl(),
        'bg-filter-month': makeEl({ value: '2026-09' }),
        'bg-view-date': makeEl(),
        'bg-days': makeEl(),
        'bg-filter-teacher': makeEl({ value: overrides.selectedTeacher || '' }),
        'bg-view-mode': makeEl({ value: 'day' }),
        'bg-schedule': makeEl()
    };
    const ctx = vm.createContext({
        Date, String, Number, Array, Map, Set, JSON, Object, window: {},
        escapeHtml: value => String(value ?? ''),
        baoGiangWeekdayLabel: () => 'Thứ Hai',
        formatVnDate: value => value,
        state: overrides.state,
        systemData: overrides.systemData || { teachers: [] },
        document: mockDocument(els),
        decorateBaoGiangRows: overrides.decorateBaoGiangRows,
        selectedTimetableTeacherId: '',
        switchAppView: () => {},
        selectTimetableTeacher: () => {},
        els
    });
    vm.runInContext(source + '\n' + teacherHelpers, ctx);
    return { ctx, els };
}

const noTkbState = {
    bao_giang: { start_date: '2026-09-01', curriculum_text: '', exceptions: [], recipient_ids: [] },
    teachers: [],
    subjects: [{ key: 'toan', name: 'Toán' }],
    info: { current_phase_id: 'phase_hk1_d1' },
    phase_assignments: {
        phase_hk1_d1: {
            teachers: [{ id: 'gv1', name: 'Nguyễn Văn A', role: 'GV', assignments: { toan: ['8A1'] }, timetable: {} }]
        }
    }
};
const noTkb = monthViewContext({
    state: noTkbState,
    selectedTeacher: 'gv1',
    decorateBaoGiangRows: () => ({ rows: [], warnings: [] })
});
vm.runInContext('renderBaoGiangMonthView()', noTkb.ctx);
assert.match(noTkb.els['bg-filter-teacher'].innerHTML, /Tất cả giáo viên \(1 GV\)/);
assert.match(noTkb.els['bg-filter-teacher'].innerHTML, /Nguyễn Văn A \(GV \/ 1 lớp\)/);
assert.match(noTkb.els['bg-schedule'].innerHTML, /đã có phân công chuyên môn \(Toán lớp 8A1\)/);
assert.match(noTkb.els['bg-schedule'].innerHTML, /Sang Tab Thời khóa biểu GV để nhập TKB cho thầy\/cô này/);
assert.doesNotMatch(noTkb.els['bg-schedule'].innerHTML, /undefined/);
assert.equal(noTkb.ctx.state.teachers.length, 1);
console.log('PASS: có PCCM chưa có TKB thì hiện hướng dẫn, dropdown vẫn đủ GV.');

const tkbRows = [{
    date: '2026-09-07', session: 'morning', period: 1, class_name: '8A1', subject: 'Toán',
    teacher_id: 'gv1', teacher_name: 'Nguyễn Văn A', teaching_week: 1,
    lesson: { ppct: '1', lesson: 'Bài 1. Đơn thức', segment: '1/1', strand: 'Đại số' }
}];
const withTkb = monthViewContext({
    state: {
        bao_giang: { start_date: '2026-09-01', curriculum_text: '', exceptions: [], recipient_ids: [] },
        teachers: [{
            id: 'gv1', name: 'Nguyễn Văn A', role: 'GV', assignments: { toan: ['8A1'] },
            timetable: { morning: { T2: { 1: { subject: 'Toán', class_name: '8A1' } } }, afternoon: {} }
        }],
        subjects: [{ key: 'toan', name: 'Toán' }],
        info: { current_phase_id: 'phase_hk1_d1' },
        phase_assignments: {}
    },
    selectedTeacher: 'gv1',
    decorateBaoGiangRows: () => ({ rows: tkbRows, warnings: [] })
});
vm.runInContext('renderBaoGiangMonthView()', withTkb.ctx);
assert.match(withTkb.els['bg-filter-teacher'].innerHTML, /Nguyễn Văn A \(GV \/ 1 lớp\)/);
assert.match(withTkb.els['bg-schedule'].innerHTML, /Buổi sáng/);
assert.match(withTkb.els['bg-schedule'].innerHTML, /8A1/);
assert.match(withTkb.els['bg-schedule'].innerHTML, /Bài 1\. Đơn thức/);
assert.doesNotMatch(withTkb.els['bg-schedule'].innerHTML, /đã có phân công chuyên môn/);
assert.equal(withTkb.ctx.window.__baoGiangVisibleRows.length, 1);
console.log('PASS: có GV và TKB thì hiện lịch báo giảng theo tháng.');

assert.match(html, /id="baogiang-config-modal"/);
assert.match(html, /onclick="openBaoGiangConfigModal\(\)"/);
assert.match(html, /function openBaoGiangConfigModal\(/);
assert.match(html, /function closeBaoGiangConfigModal\(/);
assert.match(html, /function baoGiangWarningsHtml\(/);
const modalStart = html.indexOf('id="baogiang-config-modal"');
assert(modalStart >= 0, 'Thiếu modal cấu hình báo giảng');
const modalChunk = html.slice(modalStart, modalStart + 8000);
assert.match(modalChunk, /id="bg-curriculum"/);
assert.match(modalChunk, /id="bg-ppct-grade"/);
assert.match(modalChunk, /id="bg-ppct-subject"/);
assert.match(modalChunk, /id="bg-ppct-file"/);
assert.match(modalChunk, /id="bg-exceptions"/);
assert.equal((html.match(/id="bg-curriculum"/g) || []).length, 1, 'bg-curriculum phải còn đúng 1 ID');
assert.equal((html.match(/id="bg-ppct-grade"/g) || []).length, 1, 'bg-ppct-grade phải còn đúng 1 ID');
assert.doesNotMatch(html.slice(html.indexOf('id="view-baogiang"'), html.indexOf('id="view-daythay"')), /id="bg-curriculum"/);
assert.match(html, /class="bg-warning-box"/);
assert.match(html, /max-height:180px;overflow-y:auto/);
assert.match(html, /\$\{warnings\.length\} cảnh báo — Bấm để xem\/ẩn/);
assert.doesNotMatch(declaration('baoGiangWarningsHtml'), /\bopen\b/);
const warnCtx = vm.createContext({ escapeHtml: value => String(value ?? '') });
vm.runInContext(declaration('baoGiangWarningsHtml'), warnCtx);
const warnHtml = vm.runInContext("baoGiangWarningsHtml(['Lệch tiết lớp 8A1', 'Thiếu PPCT tuần 2'])", warnCtx);
assert.match(warnHtml, /<details class="bg-warning-box"/);
assert.match(warnHtml, /2 cảnh báo — Bấm để xem\/ẩn/);
assert.match(warnHtml, /max-height:180px/);
assert.doesNotMatch(warnHtml, /<details[^>]*\sopen[\s>]/);
assert.equal(vm.runInContext('baoGiangWarningsHtml([])', warnCtx), '');
console.log('PASS: modal PPCT/lịch nghỉ và cảnh báo PPCT thu gọn <details>.');