const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const html = fs.readFileSync(path.join(__dirname, '../phancongtochuyenmon.html'), 'utf8');

function declaration(name) {
    const start = html.lastIndexOf(`function ${name}(`);
    assert(start >= 0, `Missing ${name}`);
    const next = html.indexOf('\n        function ', start + 1);
    return html.slice(start, next < 0 ? html.length : next);
}

const teachers = [
    { id: 'absent', name: 'Cô Nghỉ', role: 'GV', timetable: { morning: { '2': { '1': 'Toán - 8A1', '2': 'Toán - 8A1' } }, afternoon: {} } },
    { id: 'whole', name: 'Thầy Rảnh Buổi', role: 'GV', timetable: { morning: { '2': {} }, afternoon: {} } },
    { id: 'slots', name: 'Cô Rảnh Tiết', role: 'GV', timetable: { morning: { '2': { '3': 'Tin - 8A2', '4': 'Tin - 8A2' } }, afternoon: {} } },
    { id: 'busy', name: 'Thầy Trùng Lịch', role: 'GV', timetable: { morning: { '2': { '2': 'Toán - 9A1' } }, afternoon: {} } }
];

{
    const source = ['weekdayNumberFromDate', 'getTimetableDaySlots', 'computeDayThayTeacherAvailability'].map(declaration).join('\n');
    const context = vm.createContext({
        state: { teachers },
        parseTimetableCell: value => typeof value === 'string' ? { subject: value.split(' - ')[0], class_name: value.split(' - ')[1] } : value,
        Date, String, Object, Set, Map, Number, parseInt
    });
    vm.runInContext(source, context);
    const availability = vm.runInContext("computeDayThayTeacherAvailability('2026-09-14', 'morning', 'absent', [1, 2])", context);
    assert.deepEqual(JSON.parse(JSON.stringify(availability.freeSessionTeachers.map(item => item.teacher.id))), ['whole'], 'teacher with no lessons is free for the whole session');
    assert.deepEqual(JSON.parse(JSON.stringify(availability.freeSlotTeachers.map(item => item.teacher.id))), ['slots'], 'teacher teaching only other periods is free for every needed period');
    assert.deepEqual(JSON.parse(JSON.stringify(availability.busyConflictTeachers.map(item => item.teacher.id))), ['busy'], 'teacher colliding with a needed period is marked as conflict');
    const weekend = vm.runInContext("computeDayThayTeacherAvailability('2026-09-13', 'morning', 'absent', [1])", context);
    assert.equal(weekend.dayNum, 0, 'Sunday has no substitute suggestion availability');
}

{
    let rendered = 0;
    let toast = '';
    const select = { value: '' };
    const context = vm.createContext({
        state: { teachers },
        document: { getElementById: id => id === 'new-sub-teacher' ? select : null },
        renderDayThaySuggestions() { rendered++; },
        showToast: message => { toast = message; },
        String
    });
    vm.runInContext(declaration('selectDayThaySuggestedTeacher'), context);
    vm.runInContext("selectDayThaySuggestedTeacher('slots')", context);
    assert.equal(select.value, 'slots', 'one-click suggestion selects the substitute teacher dropdown');
    assert.equal(rendered, 1, 'one-click selection re-renders cards so the active card is highlighted');
    assert.match(toast, /Cô Rảnh Tiết/, 'one-click selection confirms the selected teacher');
}

{
    const panel = { hidden: false, innerHTML: '' };
    const teacherSelect = { value: '', options: [] };
    Object.defineProperty(teacherSelect, 'innerHTML', {
        set(value) {
            this._html = value;
            this.options = [...String(value).matchAll(/<option value="([^"]+)"/g)].map(match => ({ value: match[1] }));
        },
        get() { return this._html || ''; }
    });
    const fields = {
        'daythay-suggestion-panel': panel,
        'new-sub-teacher': teacherSelect,
        'new-sub-type': { value: 'makeup' },
        'new-sub-date': { value: '2026-09-14' },
        'new-sub-session': { value: 'morning' },
        'new-sub-for-teacher': { value: 'absent' }
    };
    const source = ['weekdayNumberFromDate', 'getTimetableDaySlots', 'computeDayThayTeacherAvailability', 'renderDayThaySuggestions'].map(declaration).join('\n');
    const context = vm.createContext({
        state: { teachers },
        document: { getElementById: id => fields[id] || null },
        snapshotPeriodSlots: () => [{ period_num: 1, enabled: true }, { period_num: 2, enabled: true }],
        parseTimetableCell: value => typeof value === 'string' ? { subject: value.split(' - ')[0], class_name: value.split(' - ')[1] } : value,
        escapeHtml: value => String(value), TT_DAY_LABELS: { 2: 'Thứ 2' },
        Date, String, Object, Set, Map, Number, parseInt, encodeURIComponent
    });
    vm.runInContext(source, context);
    vm.runInContext('renderDayThaySuggestions()', context);
    assert.equal(panel.hidden, true, 'makeup records hide the substitute suggestion panel');
    fields['new-sub-type'].value = 'replacement';
    vm.runInContext('renderDayThaySuggestions()', context);
    assert.equal(panel.hidden, false, 'replacement records show suggestions when inputs are complete');
    assert.match(panel.innerHTML, /Trống cả buổi[\s\S]*Có mặt, trống tiết cần thay/, 'shown panel contains two availability columns');
    assert.doesNotMatch(panel.innerHTML, /Bị trùng tiết/, 'conflicts are not rendered as a third user-facing panel');
}

assert.match(html, /id="daythay-suggestion-panel"/, 'daythay suggestion panel exists');
assert.match(html, /Trống cả buổi[\s\S]*Có mặt, trống tiết cần thay/, 'suggestion panel has exactly the two user-facing availability columns');
assert.match(html, /Trống cả buổi[\s\S]*Trống tiết[\s\S]*⚠️ Trùng lịch/, 'teacher dropdown status labels include availability and conflict safely');

console.log('PASS: daythay suggestions classify availability, select a substitute teacher, and hide for makeup.');
