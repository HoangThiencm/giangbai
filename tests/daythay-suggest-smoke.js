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

    fields['new-sub-date'].value = '2026-09-15';
    vm.runInContext('renderDayThaySuggestions()', context);
    assert.equal(panel.hidden, false, 'replacement panel remains visible when the absent teacher has no lessons');
    assert.match(panel.innerHTML, /không có tiết dạy/, 'visible panel explains that no replacement is needed');
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
    assert.match(preview.innerHTML, /Không có tiết cần phân công dạy thay/, 'preview explicitly warns when the absent teacher has no schedule');
    assert.match(preview.innerHTML, /disabled/, 'quick session buttons are disabled when their session has zero lessons');

    fields['new-sub-type'].value = 'makeup';
    vm.runInContext('renderAbsentTeacherSchedulePreview()', context);
    assert.equal(preview.hidden, true, 'makeup records hide the absent-teacher schedule preview');
    assert.ok(suggestions >= 1, 'preview refresh keeps substitute suggestions synchronized');
}

{
    const source = ['getPeriodsDetail', 'dayThaySessionSortRank', 'firstDayThayPeriod', 'compareDayThayJournalRecords', 'sortDayThayJournalByDate', 'reorderDayThayJournalRecords'].map(declaration).join('\n');
    let saves = 0;
    let autosaves = 0;
    const records = [
        { id: 'late', date: '2026-09-17', session: 'morning', periods_detail: [{ period_num: 2 }] },
        { id: 'afternoon', date: '2026-09-16', session: 'afternoon', periods_detail: [{ period_num: 1 }] },
        { id: 'morning2', date: '2026-09-16', session: 'morning', periods_detail: [{ period_num: 2 }] },
        { id: 'morning1', date: '2026-09-16', session: 'morning', periods_detail: [{ period_num: 1 }] }
    ];
    const context = vm.createContext({
        state: { attendance: { substitutes: { m_9: records } } }, daythayJournalManualOrderMonths: new Set(),
        getPeriodsDetail: item => item.periods_detail || [], Number, String, Math,
        saveToLocal: () => { saves++; }, triggerAutoSave: () => { autosaves++; },
        getMonthKey: () => 'm_9', renderDayThayJournal() {}, showToast() {}
    });
    vm.runInContext(source, context);
    const chronological = vm.runInContext("state.attendance.substitutes.m_9.slice().sort(compareDayThayJournalRecords).map(item => item.id)", context);
    assert.deepEqual(JSON.parse(JSON.stringify(chronological)), ['morning1', 'morning2', 'afternoon', 'late'], 'journal comparator orders date, morning/afternoon, then first period');
    assert.equal(vm.runInContext("reorderDayThayJournalRecords('m_9', 'morning1', 'late')", context), true, 'drag reorder mutates the actual stored list by record id');
    assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext("state.attendance.substitutes.m_9.map(item => item.id)", context))), ['morning1', 'late', 'afternoon', 'morning2'], 'manual order is persisted in the underlying array and remains displayable');
    assert.equal(vm.runInContext("daythayJournalManualOrderMonths.has('m_9')", context), true, 'drag switches the month to its visible manual ordering mode');
    assert.equal(saves, 1, 'drag reorder saves immediately');
    assert.equal(autosaves, 1, 'drag reorder requests the normal autosave path');
    vm.runInContext('sortDayThayJournalByDate()', context);
    assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext("state.attendance.substitutes.m_9.map(item => item.id)", context))), ['morning1', 'morning2', 'afternoon', 'late'], 'sort button resets the actual array to chronological order');
    assert.equal(vm.runInContext("daythayJournalManualOrderMonths.has('m_9')", context), false, 'sort button resets visible manual ordering mode');
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
assert.match(html, /Sắp xếp theo ngày/, 'journal has a chronological sort toolbar button');
assert.match(html, /draggable="true"/, 'journal rows support HTML5 drag and drop');

// Regression: a dated substitute record must use the timetable effective on that
// date, not the currently displayed timetable after a later-week change.
{
    const historic = { morning: { '2': { '1': 'Toán - 7/9' } }, afternoon: {} };
    const current = { morning: { '2': { '3': 'Toán - 7/10' } }, afternoon: {} };
    const datedTeachers = [
        { id: 'a', name: 'A', timetable: current },
        { id: 'b', name: 'B', timetable: { morning: { '2': { '1': 'Tin - 8A1' } }, afternoon: {} } }
    ];
    const source = ['weekdayNumberFromDate', 'getTimetableDaySlots', 'computeDayThayTeacherAvailability'].map(declaration).join('\n');
    const context = vm.createContext({
        state: { teachers: datedTeachers },
        getTeacherTimetableForDate: (teacher, date) => date < '2026-11-23' ? (teacher.id === 'a' ? historic : { morning: { '2': {} }, afternoon: {} }) : teacher.timetable,
        parseTimetableCell: value => typeof value === 'string' ? { subject: value.split(' - ')[0], class_name: value.split(' - ')[1] } : value,
        Date, String, Object, Set, Map, Number, parseInt
    });
    vm.runInContext(source, context);
    assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext("getTimetableDaySlots(state.teachers[0], 'morning', 2, '2026-11-16').map(x => x.period_num)", context))), [1], 'week 11 reads the historic period 1 timetable');
    assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext("getTimetableDaySlots(state.teachers[0], 'morning', 2, '2026-11-23').map(x => x.period_num)", context))), [3], 'week 12 reads the replacement period 3 timetable');
    const availability = vm.runInContext("computeDayThayTeacherAvailability('2026-11-16', 'morning', 'a', [1])", context);
    assert.deepEqual(JSON.parse(JSON.stringify(availability.freeSessionTeachers.map(x => x.teacher.id))), ['b'], 'availability also resolves each teacher by the selected date');
}

// End-to-end Week 12 -> Week 11 switch in DayThay:
// 1. Same morning session across Week 12 and Week 11 must reload #period-slots-builder with Week 11 lessons (never keep Week 12 slots).
// 2. Switching to a Week 11 date with zero lessons clears stale Week 12 ticked slots.
// 3. Preview shows exact CSDL week badge when saved, or fallback warning + phase source override when missing.
{
    const ttWeek11A = { morning: { '2': { '1': { subject: 'Toán', class_name: '7/9' } }, '3': {} }, afternoon: {} };
    const ttWeek12A = { morning: { '2': { '1': { subject: 'Toán', class_name: '7/10' }, '3': { subject: 'Toán', class_name: '8/1' } }, '3': {} }, afternoon: {} };
    const ttWeek11B = { morning: { '2': {}, '3': {} }, afternoon: {} };
    const ttWeek12B = { morning: { '2': { '1': { subject: 'Tin', class_name: '9/1' } }, '3': {} }, afternoon: {} };

    const preview = { hidden: true, innerHTML: '' };
    const panel = { hidden: true, innerHTML: '' };
    const weekdayHint = { textContent: '' };
    const teacherSelect = { value: 'b', options: [] };
    Object.defineProperty(teacherSelect, 'innerHTML', {
        set(value) {
            this._html = value;
            this.options = [...String(value).matchAll(/<option value="([^"]+)"/g)].map(match => ({ value: match[1] }));
        },
        get() { return this._html || ''; }
    });

    let activeSlots = [];
    const fields = {
        'daythay-absent-schedule-preview': preview,
        'daythay-suggestion-panel': panel,
        'new-sub-weekday': weekdayHint,
        'new-sub-teacher': teacherSelect,
        'new-sub-type': { value: 'replacement' },
        'new-sub-date': { value: '2026-11-23' }, // Monday of Week 12
        'new-sub-for-teacher': { value: 'a' },
        'new-sub-session': { value: 'morning' }
    };

    const fnNames = [
        'emptyDayMap', 'emptyTimetable', 'splitSubjectAndClass', 'parseTimetableCell', 'normalizeTeacherTimetable',
        'timetableHasLessons', 'effectiveSchoolStartDate', 'baoGiangDate', 'baoGiangIso', 'baoGiangTeachingWeek',
        'baoGiangSchoolWeekRange', 'timetableWeekKeyForDate', 'weeklyTimetableSaved', 'resolvePhaseDateRanges',
        'resolvePhaseTimetableInfoForDate', 'phaseTimetableForDate', 'resolveTeacherTimetableForDate', 'getTeacherTimetableForDate',
        'weekdayLabel', 'updateDateWeekday', 'getSessionLabel', 'weekdayNumberFromDate', 'getTimetableDaySlots',
        'getDayThayAbsentContextKey', 'onDayThayAbsentContextChange', 'onDayThaySessionChange', 'onDayThaySourceOverrideChange',
        'renderAbsentTeacherSchedulePreview', 'autoSuggestSlotsFromTimetable', 'maybeAutoSuggestSlotsFromTimetable',
        'computeDayThayTeacherAvailability', 'renderDayThaySuggestions'
    ];

    const context = vm.createContext({
        state: {
            info: { school_year: '2026 - 2027', morning_periods: '1-5', afternoon_periods: '1-4' },
            bao_giang: { start_date: '2026-09-07' },
            phases: [{ id: 'phase_hk1_d1', name: 'Đợt 1', date_start: '2026-09-07', date_end: '2026-11-22' }],
            phase_assignments: {
                phase_hk1_d1: { teachers: [{ id: 'a', timetable: { morning: { '2': { '2': 'Toán - 6/1' } }, afternoon: {} } }] }
            },
            teachers: [
                { id: 'a', name: 'Cô Lan', role: 'GV', timetable: JSON.parse(JSON.stringify(ttWeek12A)) },
                { id: 'b', name: 'Thầy Minh', role: 'GV', timetable: JSON.parse(JSON.stringify(ttWeek12B)) }
            ],
            weekly_timetables: {
                W11: { a: JSON.parse(JSON.stringify(ttWeek11A)), b: JSON.parse(JSON.stringify(ttWeek11B)) },
                W12: { a: JSON.parse(JSON.stringify(ttWeek12A)), b: JSON.parse(JSON.stringify(ttWeek12B)) }
            }
        },
        TT_DAYS: ['2', '3', '4', '5', '6', '7'],
        TT_DAY_LABELS: { 2: 'Thứ 2', 3: 'Thứ 3', 4: 'Thứ 4', 5: 'Thứ 5', 6: 'Thứ 6', 7: 'Thứ 7' },
        daythaySessionAuto: { scope: '', manual: false, applied: false },
        daythayTimetableSourceOverride: '',
        editingSubId: null,
        extraPeriodSlots: [],
        hiddenPeriodSlots: new Set(),
        document: { getElementById: id => fields[id] || null },
        initPeriodSlotsBuilder(slots = []) {
            activeSlots = (slots || []).map(s => ({ ...s, enabled: true }));
            context.renderDayThaySuggestions();
        },
        snapshotPeriodSlots: () => activeSlots,
        formatVnDate: iso => iso.split('-').reverse().join('/'),
        escapeHtml: v => String(v ?? ''),
        showToast() {},
        Date, String, Object, Array, Set, Map, Number, Math, JSON, Boolean, parseInt, encodeURIComponent
    });
    vm.runInContext(fnNames.map(declaration).join('\n'), context);

    // Step 1: Select Week 12 Monday (2026-11-23) -> loads Week 12 slots [1 (7/10), 3 (8/1)], teacher B conflicts on period 1
    vm.runInContext('onDayThayAbsentContextChange()', context);
    assert.deepEqual(JSON.parse(JSON.stringify(activeSlots.map(s => `${s.period_num}:${s.class_name}`))), ['1:7/10', '3:8/1'], 'Week 12 loads periods 1 and 3 from W12');
    assert.match(preview.innerHTML, /CSDL TKB Tuần 12/, 'Week 12 preview badge confirms W12 CSDL source');
    assert.match(teacherSelect.innerHTML, /Thầy Minh[\s\S]*Trùng lịch/, 'Teacher B conflicts in Week 12 period 1');

    // Step 2: Switch back to Week 11 Monday (2026-11-16, ALSO morning!) -> must reload W11 slot [1 (7/9)] and free Teacher B
    fields['new-sub-date'].value = '2026-11-16';
    vm.runInContext('onDayThayAbsentContextChange()', context);
    assert.match(weekdayHint.textContent, /Tuần 11/, 'date weekday hint displays Week 11 range');
    assert.deepEqual(JSON.parse(JSON.stringify(activeSlots.map(s => `${s.period_num}:${s.class_name}`))), ['1:7/9'], 'switching to Week 11 replaces Week 12 slots even when session stays morning');
    assert.match(preview.innerHTML, /✓ Đang lấy CSDL: CSDL TKB Tuần 11/, 'Week 11 preview shows exact W11 CSDL badge');
    assert.doesNotMatch(preview.innerHTML, /7\/10|8\/1/, 'Week 11 preview does not leak Week 12 classes');
    assert.match(teacherSelect.innerHTML, /Thầy Minh[\s\S]*Trống cả buổi/, 'Teacher B is free in Week 11 according to W11 CSDL');

    // Step 3: Switch to Week 11 Tuesday (2026-11-17, zero lessons) -> must wipe activeSlots clean
    fields['new-sub-date'].value = '2026-11-17';
    vm.runInContext('onDayThayAbsentContextChange()', context);
    assert.deepEqual(JSON.parse(JSON.stringify(activeSlots)), [], 'switching to a lesson-free day in Week 11 clears stale Week 12/Monday slots');

    // Step 4: Fallback warning when W11 & Phase have no timetable while W12 exists, plus manual source override
    delete context.state.weekly_timetables.W11;
    const savedPhase = context.state.phase_assignments.phase_hk1_d1;
    context.state.phase_assignments = {};
    fields['new-sub-date'].value = '2026-11-16';
    vm.runInContext('onDayThayAbsentContextChange()', context);
    assert.match(preview.innerHTML, /CSDL chưa có bản TKB lưu riêng cho Tuần 11/, 'warns clearly when W11 has no saved CSDL snapshot and falls back to W12');
    assert.match(preview.innerHTML, /Nhập \/ Sửa TKB Tuần 11/, 'provides 1-click button to enter/restore Week 11 TKB');

    context.state.phase_assignments = { phase_hk1_d1: savedPhase };
    vm.runInContext("onDayThaySourceOverrideChange('phase:phase_hk1_d1')", context);
    assert.deepEqual(JSON.parse(JSON.stringify(activeSlots.map(s => `${s.period_num}:${s.class_name}`))), ['2:6/1'], 'selecting phase override reloads slots from Đợt 1');
}

console.log('PASS: daythay suggestions classify availability, select a substitute teacher, and hide for makeup.');
