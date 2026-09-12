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
    const allDayTeachers = [
        { id: 'absent', name: 'Cô Nghỉ', timetable: { morning: { '2': { '1': 'Toán - 8A1' } }, afternoon: { '2': { '6': 'Toán - 8A1' } } } },
        { id: 'whole', name: 'Thầy Rảnh Cả Ngày', timetable: { morning: { '2': {} }, afternoon: { '2': {} } } },
        { id: 'slots', name: 'Cô Rảnh Tiết', timetable: { morning: { '2': { '3': 'Tin - 8A2' } }, afternoon: { '2': { '8': 'Tin - 8A2' } } } },
        { id: 'busy', name: 'Thầy Trùng Lịch', timetable: { morning: { '2': { '1': 'Toán - 9A1' } }, afternoon: { '2': { '6': 'Toán - 9A1' } } } }
    ];
    const source = ['parsePeriodsConfig', 'getSessionPeriods', 'weekdayNumberFromDate', 'getTimetableDaySlots', 'computeDayThayTeacherAvailability'].map(declaration).join('\n');
    const context = vm.createContext({
        state: { teachers: allDayTeachers, info: { morning_periods: '1, 2, 3', afternoon_periods: '6, 7, 8' } },
        parseTimetableCell: value => typeof value === 'string' ? { subject: value.split(' - ')[0], class_name: value.split(' - ')[1] } : value,
        Date, String, Object, Set, Map, Number, parseInt
    });
    vm.runInContext(source, context);
    assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext("getSessionPeriods('all_day')", context))), [1, 2, 3, 6, 7, 8], 'all-day periods merge the configured morning and afternoon frames');
    assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext("getTimetableDaySlots(state.teachers[0], 'all_day', 2).map(slot => slot.period_num)", context))), [1, 6], 'all-day timetable slots merge both sessions');
    const availability = vm.runInContext("computeDayThayTeacherAvailability('2026-09-14', 'all_day', 'absent', [1, 6])", context);
    assert.deepEqual(JSON.parse(JSON.stringify(availability.freeSessionTeachers.map(item => item.teacher.id))), ['whole'], 'a teacher with no lessons all day is free for the whole day');
    assert.deepEqual(JSON.parse(JSON.stringify(availability.freeSlotTeachers.map(item => item.teacher.id))), ['slots'], 'a teacher teaching only other all-day periods is available');
    assert.deepEqual(JSON.parse(JSON.stringify(availability.busyConflictTeachers.map(item => item.teacher.id))), ['busy'], 'all-day collisions are marked as conflicts');
}

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
    const source = ['getSessionLabel', 'weekdayNumberFromDate', 'getTimetableDaySlots', 'computeDayThayTeacherAvailability', 'renderDayThaySuggestions'].map(declaration).join('\n');
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

{
    const preview = { hidden: true, innerHTML: '' };
    const fields = {
        'daythay-absent-schedule-preview': preview,
        'new-sub-type': { value: 'replacement' },
        'new-sub-date': { value: '2026-09-14' },
        'new-sub-for-teacher': { value: 'absent' },
        'new-sub-session': { value: 'afternoon' }
    };
    let sessionChanges = 0;
    let suggestions = 0;
    const source = ['weekdayNumberFromDate', 'getTimetableDaySlots', 'getDayThayAbsentContextKey', 'renderAbsentTeacherSchedulePreview'].map(declaration).join('\n');
    const context = vm.createContext({
        state: { teachers },
        daythaySessionAuto: { scope: '2026-09-14|absent', manual: false, applied: false },
        editingSubId: null,
        document: { getElementById: id => fields[id] || null },
        parseTimetableCell: value => typeof value === 'string' ? { subject: value.split(' - ')[0], class_name: value.split(' - ')[1] } : value,
        escapeHtml: value => String(value), TT_DAY_LABELS: { 2: 'Thứ 2' },
        onDayThaySessionChange: options => { assert.equal(options.auto, true); sessionChanges++; },
        renderDayThaySuggestions: () => { suggestions++; },
        Date, String, Object, Set, Map, Number, parseInt
    });
    vm.runInContext(source, context);
    vm.runInContext('renderAbsentTeacherSchedulePreview()', context);
    assert.equal(preview.hidden, false, 'absent teacher preview is shown after valid date and teacher selection');
    assert.match(preview.innerHTML, /Tiết 1[\s\S]*8A1[\s\S]*Toán/, 'preview renders actual timetable period, class and subject data');
    assert.match(preview.innerHTML, /Buổi sáng[\s\S]*Buổi chiều/, 'preview always shows both morning and afternoon sections');
    assert.equal(fields['new-sub-session'].value, 'morning', 'morning-only teacher auto-selects morning');
    assert.equal(sessionChanges, 1, 'auto session load happens exactly once for a context');
    vm.runInContext('renderAbsentTeacherSchedulePreview()', context);
    assert.equal(sessionChanges, 1, 'harmless preview rerender does not reload the automatically selected session');

    context.daythaySessionAuto = { scope: '2026-09-14|absent', manual: true, applied: true };
    fields['new-sub-session'].value = 'afternoon';
    vm.runInContext('renderAbsentTeacherSchedulePreview()', context);
    assert.equal(fields['new-sub-session'].value, 'afternoon', 'a manual session choice survives harmless preview rerendering');

    fields['new-sub-date'].value = '2026-09-15';
    context.daythaySessionAuto = { scope: '2026-09-15|absent', manual: false, applied: false };
    vm.runInContext('renderAbsentTeacherSchedulePreview()', context);
    assert.equal(fields['new-sub-session'].value, 'afternoon', 'no automatic session is chosen when the newly selected day has no lessons');

    fields['new-sub-type'].value = 'makeup';
    vm.runInContext('renderAbsentTeacherSchedulePreview()', context);
    assert.equal(preview.hidden, true, 'makeup records hide the absent-teacher schedule preview');
    assert.ok(suggestions >= 1, 'preview refresh keeps substitute suggestions synchronized');
}

{
    const preview = { hidden: true, innerHTML: '' };
    const afternoonTeacher = { id: 'afternoon', name: 'Cô Chiều', timetable: { morning: {}, afternoon: { '2': { '6': 'Tin - 9A1' } } } };
    const bothTeacher = { id: 'both', name: 'Thầy Cả Ngày', timetable: { morning: { '2': { '1': 'Toán - 9A2' } }, afternoon: { '2': { '6': 'Toán - 9A2' } } } };
    const fields = {
        'daythay-absent-schedule-preview': preview,
        'new-sub-type': { value: 'replacement' },
        'new-sub-date': { value: '2026-09-14' },
        'new-sub-for-teacher': { value: 'afternoon' },
        'new-sub-session': { value: 'morning' }
    };
    const source = ['weekdayNumberFromDate', 'getTimetableDaySlots', 'getDayThayAbsentContextKey', 'renderAbsentTeacherSchedulePreview'].map(declaration).join('\n');
    const context = vm.createContext({
        state: { teachers: [afternoonTeacher, bothTeacher] }, daythaySessionAuto: { scope: '2026-09-14|afternoon', manual: false, applied: false }, editingSubId: null,
        document: { getElementById: id => fields[id] || null }, parseTimetableCell: value => ({ subject: value.split(' - ')[0], class_name: value.split(' - ')[1] }),
        escapeHtml: value => String(value), TT_DAY_LABELS: { 2: 'Thứ 2' }, onDayThaySessionChange() {}, renderDayThaySuggestions() {},
        Date, String, Object, Set, Map, Number, parseInt
    });
    vm.runInContext(source, context);
    vm.runInContext('renderAbsentTeacherSchedulePreview()', context);
    assert.equal(fields['new-sub-session'].value, 'afternoon', 'afternoon-only teacher auto-selects afternoon');
    fields['new-sub-for-teacher'].value = 'both';
    context.daythaySessionAuto = { scope: '2026-09-14|both', manual: false, applied: false };
    vm.runInContext('renderAbsentTeacherSchedulePreview()', context);
    assert.equal(fields['new-sub-session'].value, 'all_day', 'teacher with morning and afternoon lessons auto-selects all day');
}

{
    const fields = {
        'new-sub-date': { value: '2026-09-14' },
        'new-sub-for-teacher': { value: 'absent' },
        'new-sub-session': { value: 'morning' }
    };
    let previewRenders = 0;
    let sessionCalls = 0;
    const source = ['getDayThayAbsentContextKey', 'onDayThayAbsentContextChange', 'chooseDayThayPreviewSession'].map(declaration).join('\n');
    const context = vm.createContext({
        daythaySessionAuto: { scope: '2026-09-14|absent', manual: true, applied: true },
        document: { getElementById: id => fields[id] || null },
        updateDateWeekday() {}, renderAbsentTeacherSchedulePreview() { previewRenders++; },
        onDayThaySessionChange(options) { assert.equal(options.manual, true); sessionCalls++; },
        String
    });
    vm.runInContext(source, context);
    vm.runInContext("chooseDayThayPreviewSession('afternoon')", context);
    assert.equal(fields['new-sub-session'].value, 'afternoon', 'preview quick action changes session in one click');
    assert.equal(context.daythaySessionAuto.manual, true, 'preview quick action is treated as a manual override');
    assert.equal(sessionCalls, 1, 'preview quick action uses the existing session-change flow once');
    fields['new-sub-date'].value = '2026-09-15';
    vm.runInContext('onDayThayAbsentContextChange()', context);
    assert.deepEqual(JSON.parse(JSON.stringify(context.daythaySessionAuto)), { scope: '2026-09-15|absent', manual: false, applied: false }, 'changing absent date re-enables automatic session detection');
    assert.equal(previewRenders, 1, 'absent context change renders the schedule preview once');
}

assert.match(html, /id="daythay-suggestion-panel"/, 'daythay suggestion panel exists');
assert.match(html, /id="daythay-absent-schedule-preview"/, 'absent-teacher schedule preview exists');
assert.ok(html.indexOf('id="new-sub-for-teacher"') < html.indexOf('id="new-sub-session"'), 'absent teacher is selected before session in visible form order');
assert.ok(html.indexOf('id="daythay-absent-schedule-preview"') < html.indexOf('id="daythay-suggestion-panel"'), 'absent preview appears before suggestion panel');
assert.match(html, /<option value="all_day">Cả ngày/, 'session dropdown offers an all-day choice');
assert.match(html, /Trống cả buổi[\s\S]*Có mặt, trống tiết cần thay/, 'suggestion panel has exactly the two user-facing availability columns');
assert.match(html, /Trống cả buổi[\s\S]*Trống tiết[\s\S]*⚠️ Trùng lịch/, 'teacher dropdown status labels include availability and conflict safely');

console.log('PASS: daythay suggestions classify availability, select a substitute teacher, and hide for makeup.');
