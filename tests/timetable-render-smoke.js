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
        refreshTimetableGeminiModelLabel() {},
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
    assert.deepEqual([...vm.runInContext("periodsForTimetableSession('afternoon', { afternoon: { '2': { '7': { subject: 'Toán' } } } })", context)], [1, 2, 3, 4, 7], 'an imported period 7 adds its own afternoon row');
}

{
    let workspaceRenders = 0;
    let listRenders = 0;
    const context = vm.createContext({
        state: { info: {}, teachers: [{ id: 1, name: 'Hồ Đăng Danh' }, { id: 2, name: 'Hoàng Xuân Ánh' }, { id: 123, name: 'Cô An' }] },
        selectedTimetableTeacherId: null,
        TT_DAYS: ['mon', 'tue', 'wed', 'thu', 'fri', 'sat'],
        emptyTimetable,
        getSessionPeriods: () => [],
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
    vm.runInContext([declaration('alignSessionPeriods'), declaration('matchTeacherByName'), declaration('applyAiTimetableResult')].join('\n'), context);
    vm.runInContext("applyAiTimetableResult({ teacher_name: 'Cô An' })", context);
    assert.equal(workspaceRenders, 1, 'the timetable workspace renders even when assignment sync fails');
    assert.equal(listRenders, 1, 'the timetable teacher list refreshes after AI recognition');
    vm.runInContext("applyAiTimetableResult({ teacher_name: 'Giáo viên: Ánh' })", context);
    assert.equal(vm.runInContext('selectedTimetableTeacherId', context), 2, 'AI timetable import assigns Ánh to Hoàng Xuân Ánh instead of Hồ Đăng Danh');
}

{
    const teachers = [
        { id: 1, name: 'Hồ Đăng Danh' },
        { id: 2, name: 'Hoàng Xuân Ánh' }
    ];
    const context = vm.createContext({
        teachers, String, Set, Math,
        foldText: value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/gi, 'd').toLowerCase()
    });
    vm.runInContext(declaration('matchTeacherByName'), context);
    assert.equal(vm.runInContext("matchTeacherByName('Giáo viên: Ánh', teachers, null)?.id", context), 2, 'terminal given name Ánh matches Hoàng Xuân Ánh, not Hồ Đăng Danh');
    assert.equal(vm.runInContext("matchTeacherByName('Hoàng Xuân Ánh', teachers, null)?.id", context), 2, 'the full normalized name matches exactly');
    assert.equal(vm.runInContext("matchTeacherByName('Ánh', [{ id: 1, name: 'Hồ Đăng Danh' }], null)", context), null, 'a name token never matches a substring inside another token');
    assert.equal(vm.runInContext("matchTeacherByName('Ánh', [{ id: 2, name: 'Hoàng Xuân Ánh' }, { id: 3, name: 'Nguyễn Thị Ánh' }], 3)?.id", context), 3, 'a selected teacher with the same terminal given name is retained');
    assert.equal(vm.runInContext("matchTeacherByName('Ánh', [{ id: 2, name: 'Hoàng Xuân Ánh' }, { id: 3, name: 'Nguyễn Thị Ánh' }], null)", context), null, 'ambiguous given names do not select the wrong teacher');
}

{
    const days = ['2', '3', '4', '5', '6', '7'];
    const context = vm.createContext({
        state: { info: {}, teachers: [] },
        selectedTimetableTeacherId: null,
        TT_DAYS: days,
        emptyTimetable: () => ({
            morning: Object.fromEntries(days.map(day => [day, {}])),
            afternoon: Object.fromEntries(days.map(day => [day, {}]))
        }),
        getSessionPeriods: session => session === 'afternoon' ? [7, 8, 9] : [1, 2, 3, 4],
        parseTimetableCell: value => value,
        foldText: value => String(value).toLowerCase(),
        document: { getElementById: () => null },
        persistAndSaveTimetableLocal() {}, renderTimetableWorkspace() {}, renderTimetableTeacherList() {},
        showToast() {}, Date, Object, Set, Map, String, Number, parseInt
    });
    vm.runInContext([declaration('alignSessionPeriods'), declaration('matchTeacherByName'), declaration('applyAiTimetableResult')].join('\n'), context);
    vm.runInContext(`applyAiTimetableResult({ afternoon: { '2': {
        '6': 'Toán - 61', '7': 'Toán - 62', '8': 'Toán - 63'
    } } })`, context);
    const afternoon = JSON.parse(JSON.stringify(context.editingTimetable.afternoon['2']));
    assert.deepEqual(afternoon, { '7': 'Toán - 61', '8': 'Toán - 62', '9': 'Toán - 63' }, 'AI periods 6–8 align to the configured afternoon periods 7–9');
    assert.equal(afternoon['6'], undefined, 'period 6 is not created when the afternoon begins at period 7');
    const alreadyAligned = JSON.parse(JSON.stringify(vm.runInContext(`alignSessionPeriods({ '2': {
        '7': 'Toán - 71', '8': 'Toán - 72', '9': 'Toán - 73'
    } }, [7, 8, 9])`, context)));
    assert.deepEqual(alreadyAligned, { '2': { '7': 'Toán - 71', '8': 'Toán - 72', '9': 'Toán - 73' } }, 'already configured AI periods remain unchanged');
}

{
    const days = ['2', '3', '4', '5', '6', '7'];
    const context = vm.createContext({
        Object, Set, Map, String, Number, parseInt
    });
    vm.runInContext(declaration('alignSessionPeriods'), context);
    const onlySeven = JSON.parse(JSON.stringify(vm.runInContext(`alignSessionPeriods({ '2': { '7': 'Toán - 71' } }, [1, 2, 3, 4])`, context)));
    assert.deepEqual(onlySeven, { '2': { '7': 'Toán - 71' } }, 'a lone period 7 stays period 7 against the default afternoon frame');
    const sixAndSeven = JSON.parse(JSON.stringify(vm.runInContext(`alignSessionPeriods({ '3': { '6': 'Toán - 61', '7': 'Toán - 62' } }, [1, 2, 3, 4])`, context)));
    assert.deepEqual(sixAndSeven, { '3': { '6': 'Toán - 61', '7': 'Toán - 62' } }, 'afternoon periods 6 and 7 are not compressed onto periods 1 and 2');
    const gaps = JSON.parse(JSON.stringify(vm.runInContext(`alignSessionPeriods({ '4': { '1': 'Toán - 41', '3': 'Toán - 43', '5': 'Toán - 45' } }, [1, 2, 3, 4, 5])`, context)));
    assert.deepEqual(gaps, { '4': { '1': 'Toán - 41', '3': 'Toán - 43', '5': 'Toán - 45' } }, 'gapped periods 1, 3 and 5 stay on their printed numbers');
    const afternoonSpan = JSON.parse(JSON.stringify(vm.runInContext(`alignSessionPeriods({ '5': { '6': 'A', '7': 'B', '8': 'C', '9': 'D' } }, [1, 2, 3, 4])`, context)));
    assert.deepEqual(afternoonSpan, { '5': { '6': 'A', '7': 'B', '8': 'C', '9': 'D' } }, 'afternoon span 6–9 is preserved when the frame is still 1–4');
    const sevenToNine = JSON.parse(JSON.stringify(vm.runInContext(`alignSessionPeriods({ '6': { '7': 'A', '8': 'B', '9': 'C' } }, [1, 2, 3, 4])`, context)));
    assert.deepEqual(sevenToNine, { '6': { '7': 'A', '8': 'B', '9': 'C' } }, 'afternoon span 7–9 is preserved when the frame is still 1–4');
    const vnEduRows = JSON.parse(JSON.stringify(vm.runInContext(`alignSessionPeriods({ '3': { '9': 'Toán - 61', '10': 'Toán - 61' } }, [6, 7, 8, 9, 10])`, context)));
    assert.deepEqual(vnEduRows, { '3': { '8': 'Toán - 61', '9': 'Toán - 61' } }, 'afternoon rows read as periods 9 and 10 shift to 8 and 9 when the frame is 6–10');
    const vnEduFromSeven = JSON.parse(JSON.stringify(vm.runInContext(`alignSessionPeriods({ '3': { '7': 'A', '8': 'B', '9': 'C', '10': 'D' } }, [6, 7, 8, 9, 10])`, context)));
    assert.deepEqual(vnEduFromSeven, { '3': { '6': 'A', '7': 'B', '8': 'C', '9': 'D' } }, 'a continuous afternoon span starting at 7 shifts back by one when the frame starts at 6');
    const alreadyEightNine = JSON.parse(JSON.stringify(vm.runInContext(`alignSessionPeriods({ '3': { '8': 'Toán - 61', '9': 'Toán - 61' } }, [6, 7, 8, 9, 10])`, context)));
    assert.deepEqual(alreadyEightNine, { '3': { '8': 'Toán - 61', '9': 'Toán - 61' } }, 'periods 8 and 9 stay put on a 6–10 frame');
}

assert.match(html, /applyPeriodPreset\('1-5','6-10'\)/, 'period modal includes the morning 1-5, afternoon 6-10 preset');
assert.match(html, /applyPeriodPreset\('1-5','1-5'\)/, 'period modal includes the morning 1-5, afternoon 1-5 preset');

assert.match(html, /id="tt-import-details"[\s\S]*openQuickPeriodsConfig\(\)[\s\S]*Khung tiết[\s\S]*btn-ai-scan-tt/, 'the timetable tab exposes the period-frame button beside AI scan');
assert.match(html, /id="gemini-model-modal"/, 'the page includes the Gemini model modal');
assert.match(html, /function openGeminiModelModal\(/, 'the timetable tab can open the Gemini model modal');
assert.match(html, /function getTimetableGeminiModel\(/, 'the timetable scan reads the saved Gemini model');
{
    const scanStart = html.indexOf('async function scanTimetableWithAI');
    const scanEnd = html.indexOf('function alignSessionPeriods', scanStart);
    const scanBody = html.slice(scanStart, scanEnd);
    assert.match(scanBody, /getTimetableGeminiModel\(\)/, 'AI timetable scan uses the selected Gemini model');
    assert.doesNotMatch(scanBody, /model:\s*'gemini-2\.5-flash'/, 'AI timetable scan no longer hardcodes gemini-2.5-flash');
}
{
    const store = new Map();
    const context = vm.createContext({
        state: { info: {} },
        localStorage: {
            getItem: key => store.has(key) ? store.get(key) : null,
            setItem: (key, value) => store.set(key, String(value))
        }
    });
    vm.runInContext([declaration('getTimetableGeminiModel'), declaration('formatGeminiModelShortLabel')].join('\n'), context);
    assert.equal(vm.runInContext('getTimetableGeminiModel()', context), 'gemini-2.5-flash', 'timetable AI defaults to gemini-2.5-flash');
    context.localStorage.setItem('phancong_gemini_model', 'gemini-3.7-flash');
    assert.equal(vm.runInContext('getTimetableGeminiModel()', context), 'gemini-3.7-flash', 'saved phancong_gemini_model overrides the default');
    assert.equal(vm.runInContext("formatGeminiModelShortLabel('gemini-3.7-flash')", context), '3.7 Flash', 'Flash models use a short button label');
}
assert.doesNotMatch(html, /gemini-2\.5-pro|gemini-1\.5-flash/, 'the timetable model picker no longer offers Pro or 1.5 Flash');
assert.match(html, /id="top-nav-ai-model-label"/, 'the top navbar shows the active Gemini model');
assert.match(html, /id="tt-toolbar-model-label"/, 'the timetable toolbar shows the active Gemini model');
assert.match(html, /function updateAiModelLabels\(/, 'saving a model updates every visible label');
{
    const api = fs.readFileSync(path.join(__dirname, '../api/khbd_gemini.php'), 'utf8');
    assert.match(api, /in_array\(\$status, \[403, 429, 503\], true\)/, 'HTTP 503 rotates to the next free Gemini key');
    assert.match(api, /high demand/, 'a high-demand message rotates to the next free Gemini key');
}
assert.doesNotMatch(html, /Key tiết trong "morning" BẮT BUỘC chỉ là một trong/, 'the scan prompt no longer drops periods outside the default frame');
assert.match(html, /tuyệt đối không bỏ sót bất kỳ tiết nào có phân công dạy/, 'the scan prompt requires every printed period, including period 7');

assert.match(html, /<details class="tt-import-card" id="tt-import-details">/, 'timetable import controls are collapsible');
assert.match(html, /<div class="tt-sessions-container">[\s\S]*id="tt-morning-wrap"[\s\S]*id="tt-afternoon-wrap"/, 'morning and afternoon grids share the sessions container');
assert.match(html, /\.tt-sessions-container\s*\{\s*display:\s*grid;\s*grid-template-columns:\s*1fr 1fr;/, 'desktop timetable layout uses two columns');
assert.match(html, /@media \(max-width: 1024px\)\s*\{\s*\.tt-sessions-container\s*\{\s*grid-template-columns:\s*1fr;/, 'small screens collapse timetable sessions to one column');

{
    const source = ['emptyDayMap', 'emptyTimetable', 'splitSubjectAndClass', 'parseTimetableCell', 'normalizeTeacherTimetable', 'timetableHasLessons', 'countTimetableLessons', 'periodsForTimetableSession', 'timetableEmailSessionTable', 'calendarSubscribeButtonsHtml', 'buildSelectedTeachersTimetableEmail', 'buildTeacherIndividualTimetableEmail'].map(declaration).join('\n');
    const timetable = {
        morning: { 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {} },
        afternoon: { 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {} }
    };
    timetable.morning['2']['1'] = { subject: 'Toán', class_name: '71' };
    timetable.afternoon['7']['4'] = { subject: 'Toán', class_name: '72' };
    const context = vm.createContext({
        state: { info: { school_year: '2026-2027', semester: 'HK1' }, teachers: [
            { id: 1, name: 'Cô An', role: 'GV', email: 'an@example.edu.vn', timetable },
            { id: 2, name: 'Thầy Bình', role: 'TTCM', timetable }
        ] },
        TT_DAYS: ['2', '3', '4', '5', '6', '7'],
        TT_DAY_LABELS: { 2: 'Thứ 2', 3: 'Thứ 3', 4: 'Thứ 4', 5: 'Thứ 5', 6: 'Thứ 6', 7: 'Thứ 7' },
        getSessionPeriods: session => session === 'morning' ? [1, 2, 3, 4, 5] : [1, 2, 3, 4],
        escapeHtml: value => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;'),
        JSON, String, Object, Set, Number, parseInt, encodeURIComponent
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
    const individual = vm.runInContext(`buildTeacherIndividualTimetableEmail(state.teachers[0], undefined, true, 'webcal://example.test/api/calendar_feed.php?token=abc&teacher_id=1')`, context);
    assert.match(individual.html, /📱 Thêm vào Lịch iPhone/, 'email TKB có nút thêm vào Lịch iPhone');
    assert.match(individual.html, /webcal:\/\/example\.test\/api\/calendar_feed\.php/, 'nút iPhone dùng link webcal');
    assert.match(individual.html, /🌐 Thêm vào Google Calendar/, 'email TKB có nút Google Calendar');
    assert.match(individual.html, /calendar\.google\.com\/calendar\/r\?cid=/, 'nút Google Calendar dùng cid webcal');
    assert.equal(individual.to, 'an@example.edu.vn', 'individual timetable email targets the selected teacher');
    assert.match(individual.subject, /Cô An/, 'individual timetable subject identifies its teacher');
    assert.doesNotMatch(individual.html, /Thầy Bình/, 'individual timetable email must not include another teacher');
}

{
    const context = vm.createContext({
        state: { teachers: [{ id: 'u_12', name: 'Cô An' }, { id: 't_2', name: 'Thầy Bình' }] },
        systemData: { current_user: { id: 12, full_name: 'Tên không cần khớp' } },
        String,
        foldText: value => String(value).toLowerCase()
    });
    vm.runInContext(declaration('currentUserTeacher'), context);
    assert.equal(vm.runInContext('currentUserTeacher().name', context), 'Cô An', 'my timetable resolves the logged-in user by u_id before name matching');
}

['view-email', 'switchEmailTab', 'sendMyTimetableEmail', 'currentUserTeacher', 'renderEmailRecipientList', 'sendSelectedTeachersTimetableEmail', 'sendBaoGiangSelectedWeekToTeachers', 'Email nhận', 'TKB của tôi', 'TKB tất cả GV → email tôi', 'LBG cá nhân từng GV', 'Gửi TKB của tôi về email cá nhân', 'Gửi TKB đã chọn về email tôi', 'Gửi lịch cho GV đã chọn'].forEach(token => {
    assert(html.includes(token), `missing centralized email control: ${token}`);
});
['email-mail-status', 'loadBaoGiangMailStatus', 'email-bg-send-teachers', 'buildTeacherBaoGiangWeekHtml', 'directButton.disabled = !directAllowed'].forEach(token => {
    assert(html.includes(token), `missing safe direct-email control: ${token}`);
});

assert.doesNotMatch(html, /onclick="sendSelectedTeachersIndividualTimetableEmail\(\)"/, 'individual timetable sending is not duplicated outside the centralized email flow');

{
    const feed = fs.readFileSync(path.join(__dirname, '../api/calendar_feed.php'), 'utf8');
    assert.match(feed, /text\/calendar; charset=utf-8/, 'calendar feed trả chuẩn iCalendar');
    assert.match(feed, /function calendar_feed_token/, 'calendar feed ký token theo giáo viên');
    assert.match(feed, /hash_equals\(\$expected, \$token\)/, 'calendar feed từ chối token sai');
    assert.match(feed, /DTSTART;VALUE=DATE:/, 'calendar feed mặc định là sự kiện cả ngày');
    assert.match(feed, /\[Tiết /, 'calendar feed đưa số tiết lên đầu tiêu đề');
    assert.match(html, /Đồng bộ Lịch \(iPhone \/ Google Calendar\)/, 'tab lịch có nút đồng bộ Webcal');
    assert.match(html, /id="bg-calendar-feed-iphone"/, 'modal có nút 1 chạm vào Lịch iPhone');
    assert.match(html, /Thêm ngay vào Lịch iPhone/, 'nút iPhone dùng webcal một chạm');
    assert.match(html, /Thêm ngay vào Google Calendar/, 'nút Google Calendar một chạm');
    assert.match(html, /calendar\.google\.com\/calendar\/r\?cid=/, 'link Google dùng cid webcal');
    assert.match(html, /iPhone 16 Pro \(iOS 18\)/, 'hướng dẫn nêu iOS 18');
    assert.match(html, /Thêm lịch đăng ký/, 'hướng dẫn cách A trong app Lịch');
    assert.match(html, /Cài đặt → Ứng dụng → Lịch/, 'hướng dẫn cách B trong Cài đặt iOS 18');
    assert.match(html, /calendarSubscribeButtonsHtml\(webcalUrl\)/, 'email lịch báo giảng chèn nút webcal dưới bảng');
    assert.match(html, /await baoGiangCalendarFeedWebcal\(teacher\.id\)/, 'gửi email lấy link webcal trước khi đính nội dung');
    assert.match(html, /id="bg-ics-format"/, 'tab lịch có hộp chọn định dạng');
    assert.match(html, /Tiết 1, 2, 3\.\.\. không gán giờ/, 'mặc định không gán khung giờ giả định');
    assert.match(html, /api\/calendar_feed\.php\?action=link/, 'nút link gọi endpoint Webcal');
    const start = html.indexOf('const BAOGIANG_PERIOD_TIMES');
    const end = html.indexOf('function syncBaoGiangIcsFormat');
    assert(start >= 0 && end > start, 'khối tạo .ics phải tách được');
    const context = vm.createContext({ formatBaoGiangLessonDisplay: row => row.lesson?.lesson || '' });
    vm.runInContext(html.slice(start, end), context);
    const allDay = vm.runInContext(`buildTeacherBaoGiangIcs({ id: 'gv1', name: 'Cô An' }, { start: '2026-09-28', end: '2026-10-04' }, [
        { date: '2026-09-28', session: 'morning', period: 1, subject: 'Toán', class_name: '63', lesson: { name: 'Số tự nhiên' } }
    ])`, context);
    assert.match(allDay, /SUMMARY:\[Tiết 1\] Toán 63 - Số tự nhiên/);
    assert.match(allDay, /DTSTART;VALUE=DATE:20260928/);
    assert.match(allDay, /DTEND;VALUE=DATE:20260929/);
    assert.doesNotMatch(allDay, /T071500/);
    const timed = vm.runInContext(`buildTeacherBaoGiangIcs({ id: 'gv1', name: 'Cô An' }, { start: '2026-09-28', end: '2026-10-04' }, [
        { date: '2026-09-28', session: 'morning', period: 1, subject: 'Toán', class_name: '63', lesson: { name: 'Số tự nhiên' } }
    ], false)`, context);
    assert.match(timed, /DTSTART;TZID=Asia\/Ho_Chi_Minh:20260928T071500/);
    assert.match(timed, /SUMMARY:\[Tiết 1\] Toán 63 - Số tự nhiên/);
}

console.log('PASS: timetable view loads numeric IDs and JSON data, uses a compact responsive layout, aligns AI periods, renders after AI sync errors, and builds selected-teacher timetable email.');
