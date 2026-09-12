const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const html = fs.readFileSync(path.join(__dirname, '../phancongtochuyenmon.html'), 'utf8');

for (const match of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)) new vm.Script(match[1]);

function declaration(name) {
    const start = html.lastIndexOf(`function ${name}(`);
    assert(start >= 0, `Missing ${name}`);
    const next = html.indexOf('\n        function ', start + 1);
    return html.slice(start, next < 0 ? html.length : next);
}

function emptyTimetable() {
    return {
        morning: { mon: {}, tue: {}, wed: {}, thu: {}, fri: {}, sat: {} },
        afternoon: { mon: {}, tue: {}, wed: {}, thu: {}, fri: {}, sat: {} }
    };
}

{
    let selected = null;
    const context = vm.createContext({
        state: { teachers: [{ id: 123 }] },
        selectedTimetableTeacherId: null,
        bindTimetableInputEvents() {},
        selectTimetableTeacher: id => { selected = id; },
        renderTimetableTeacherList() { throw new Error('should use select'); },
        renderTimetableWorkspace() { throw new Error('should use select'); }
    });
    vm.runInContext(declaration('renderTimetableView'), context);
    vm.runInContext('renderTimetableView()', context);
    assert.equal(selected, 123, 'opening the view loads the first teacher timetable');
}

{
    const elements = {
        'tt-preview': { src: 'old', style: {} },
        'tt-clear-preview': { style: {} }
    };
    const context = vm.createContext({
        state: { info: {}, teachers: [{ id: 123, timetable: { marker: 'saved' } }] },
        document: { getElementById: id => elements[id] },
        normalizeTeacherTimetable: timetable => ({ ...emptyTimetable(), ...timetable }),
        renderTimetableTeacherList() {}, renderTimetableWorkspace() {}
    });
    vm.runInContext(declaration('selectTimetableTeacher'), context);
    vm.runInContext("selectTimetableTeacher('123')", context);
    assert.equal(context.editingTimetable.marker, 'saved', 'string HTML IDs resolve numeric teacher IDs');
}

{
    const source = ['emptyDayMap', 'emptyTimetable', 'splitSubjectAndClass', 'parseTimetableCell', 'normalizeTeacherTimetable'].map(declaration).join('\n');
    const context = vm.createContext({ TT_DAYS: ['mon', 'tue', 'wed', 'thu', 'fri', 'sat'], JSON, String, Object });
    vm.runInContext(source, context);
    const normalized = vm.runInContext(`normalizeTeacherTimetable(JSON.stringify({
        school_year: '2026-2027',
        morning: { mon: { 1: { subject: 'Toán', class_name: '9A1' } } }
    }))`, context);
    assert.equal(normalized.school_year, '2026-2027', 'JSON-string timetables retain metadata');
    assert.deepEqual(JSON.parse(JSON.stringify(normalized.morning.mon['1'])), { subject: 'Toán', class_name: '9A1' }, 'JSON-string timetables retain lessons');
}

{
    const context = vm.createContext({
        getSessionPeriods: () => [],
        Object, Set, parseInt
    });
    vm.runInContext(declaration('periodsForTimetableSession'), context);
    assert.deepEqual([...vm.runInContext("periodsForTimetableSession('morning', {})", context)], [1, 2, 3, 4, 5]);
    assert.deepEqual([...vm.runInContext("periodsForTimetableSession('afternoon', {})", context)], [1, 2, 3, 4]);
}

{
    let workspaceRenders = 0;
    let listRenders = 0;
    const context = vm.createContext({
        state: { info: {}, teachers: [{ id: 123, name: 'Cô An' }] },
        TT_DAYS: ['mon', 'tue', 'wed', 'thu', 'fri', 'sat'],
        emptyTimetable,
        parseTimetableCell: value => value,
        foldText: value => String(value).toLowerCase(),
        document: { getElementById: id => id === 'tt-auto-apply-assign' ? { checked: true } : null },
        persistAndSaveTimetableLocal() {},
        applyTimetableToAssignments() { throw new Error('assignment mismatch'); },
        renderLiveStatsBanner() {}, renderPool() {}, renderTeachers() {},
        renderTimetableWorkspace() { workspaceRenders++; },
        renderTimetableTeacherList() { listRenders++; },
        showToast() {}, console: { error() {} }, Date
    });
    vm.runInContext(declaration('applyAiTimetableResult'), context);
    vm.runInContext("applyAiTimetableResult({ teacher_name: 'Cô An' })", context);
    assert.equal(workspaceRenders, 1, 'the timetable workspace renders even when assignment sync fails');
    assert.equal(listRenders, 1, 'the timetable teacher list refreshes after AI recognition');
}

{
    const source = ['emptyDayMap', 'emptyTimetable', 'splitSubjectAndClass', 'parseTimetableCell', 'normalizeTeacherTimetable', 'timetableHasLessons', 'countTimetableLessons', 'periodsForTimetableSession', 'timetableEmailSessionTable', 'buildSelectedTeachersTimetableEmail'].map(declaration).join('\n');
    const timetable = {
        morning: { 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {} },
        afternoon: { 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {} }
    };
    timetable.morning['2']['1'] = { subject: 'Toán', class_name: '71' };
    timetable.afternoon['7']['4'] = { subject: 'Toán', class_name: '72' };
    const context = vm.createContext({
        state: { info: { school_year: '2026-2027', semester: 'HK1' }, teachers: [
            { id: 1, name: 'Cô An', role: 'GV', timetable },
            { id: 2, name: 'Thầy Bình', role: 'TTCM', timetable }
        ] },
        TT_DAYS: ['2', '3', '4', '5', '6', '7'],
        TT_DAY_LABELS: { 2: 'Thứ 2', 3: 'Thứ 3', 4: 'Thứ 4', 5: 'Thứ 5', 6: 'Thứ 6', 7: 'Thứ 7' },
        getSessionPeriods: session => session === 'morning' ? [1, 2, 3, 4, 5] : [1, 2, 3, 4],
        escapeHtml: value => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;'),
        JSON, String, Object, Set, Number, parseInt
    });
    vm.runInContext(source, context);
    const email = vm.runInContext('buildSelectedTeachersTimetableEmail([1, 2])', context);
    assert.match(email.subject, /Thời khóa biểu 2 giáo viên/, 'email subject identifies selected teachers');
    assert.match(email.html, /Cô An/, 'email includes first selected teacher');
    assert.match(email.html, /Thầy Bình/, 'email includes second selected teacher');
    assert.match(email.html, /Buổi sáng/, 'email has a morning timetable grid');
    assert.match(email.html, /Buổi chiều/, 'email has an afternoon timetable grid');
    assert.match(email.html, /Thứ 2/, 'email grid has Monday through Saturday headers');
    assert.match(email.html, /Toán/, 'email retains subject data');
    assert.match(email.html, /71/, 'email retains class data');
    assert.doesNotMatch(email.html, /báo giảng|PPCT/i, 'timetable email contains no lesson-plan content');
}

['selectedTimetableTeacherIds', 'selectAllTimetableTeachers', 'clearTimetableTeacherSelection', 'buildSelectedTeachersTimetableEmail', 'sendSelectedTeachersTimetableEmail', 'Chọn tất cả GV có TKB', 'Gửi TKB các GV đã chọn qua email'].forEach(token => {
    assert(html.includes(token), `missing selected-teacher timetable email control: ${token}`);
});

console.log('PASS: timetable view loads numeric IDs and JSON data, preserves grid fallbacks, renders after AI sync errors, and builds selected-teacher timetable email.');
