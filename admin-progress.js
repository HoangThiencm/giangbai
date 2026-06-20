(function () {
    const PAGE_SUBJECT = String(window.LOTRINH_SUBJECT || '').trim();

    let lessons = [];
    let rows = [];
    let classes = [];
    let managedClasses = [];
    let selectedLessonId = '';
    let selectedClassName = localStorage.getItem('progress_class_filter') || '';

    function el(id) { return document.getElementById(id); }

    function lessonsForPage() {
        if (!PAGE_SUBJECT) return lessons;
        return lessons.filter(lesson => String(lesson.subject || '').trim() === PAGE_SUBJECT);
    }

    function getAdminKey() {
        try {
            return typeof cachedKey !== 'undefined' ? cachedKey : window.cachedKey;
        } catch {
            return window.cachedKey;
        }
    }

    function isTeacherUser() {
        return localStorage.getItem('userRole') === 'teacher';
    }

    function parseManagedClasses(value) {
        return String(value || '')
            .split(/[,;|]+/)
            .map(part => part.trim())
            .filter(Boolean);
    }

    function teacherManagedClasses() {
        if (!isTeacherUser()) return [];
        if (managedClasses.length) return managedClasses;
        return parseManagedClasses(localStorage.getItem('userClassName') || '');
    }

    function escapeHtml(value) {
        return String(value ?? '').replace(/[&<>"']/g, ch => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }[ch]));
    }

    function decodeBasicEntities(value) {
        return String(value ?? '')
            .replace(/&quot;/g, '"')
            .replace(/&lt;/g, '<')
            .replace(/&gt;/g, '>')
            .replace(/&amp;/g, '&')
            .replace(/&nbsp;/g, ' ');
    }

    function mathText(value) {
        const source = decodeBasicEntities(value).replace(/\r\n?/g, '\n').trim();
        const parts = source.split(/(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\$[^\n$]*?\$|\\\([\s\S]*?\\\))/g);
        return parts.map(part => {
            if (!part) return '';
            const isMath = (
                (part.startsWith('$$') && part.endsWith('$$')) ||
                (part.startsWith('\\[') && part.endsWith('\\]')) ||
                (part.startsWith('\\(') && part.endsWith('\\)')) ||
                (part.startsWith('$') && part.endsWith('$'))
            );
            if (isMath) return escapeHtml(part.replace(/[ \t]*\n[ \t]*/g, ' '));
            return escapeHtml(part).replace(/\n/g, '<br>');
        }).join('');
    }

    function typesetMath() {
        if (window.MathJax && typeof window.MathJax.typesetPromise === 'function') {
            window.MathJax.typesetPromise([el('adminProgressPanel') || document.body]).catch(() => {});
        }
    }

    function statusLabel(status) {
        const map = {
            not_started: ['Chưa bắt đầu', 'bg-slate-100 text-slate-700'],
            in_progress: ['Đang học', 'bg-sky-100 text-sky-700'],
            needs_practice: ['Cần luyện thêm', 'bg-amber-100 text-amber-800'],
            mastered: ['Đã học xong', 'bg-teal-100 text-teal-800']
        };
        return map[status] || map.not_started;
    }

    function bindProgressActionButtons() {
        const reloadBtn = el('progressReloadBtn');
        const syncBtn = el('progressSyncBtn');
        if (reloadBtn && reloadBtn.dataset.boundProgressReload !== '1') {
            reloadBtn.dataset.boundProgressReload = '1';
            reloadBtn.onclick = () => refresh();
        }
        if (syncBtn && syncBtn.dataset.boundProgressSync !== '1') {
            syncBtn.dataset.boundProgressSync = '1';
            syncBtn.onclick = () => syncProgress();
        }
    }

    function ensureProgressSyncButton() {
        if (el('progressSyncBtn')) return;
        const reloadBtn = el('progressReloadBtn');
        if (!reloadBtn || !reloadBtn.parentElement) return;
        const syncBtn = document.createElement('button');
        syncBtn.id = 'progressSyncBtn';
        syncBtn.type = 'button';
        syncBtn.className = 'bg-teal-700 hover:bg-teal-800 text-white px-4 py-2.5 rounded font-bold text-sm';
        syncBtn.innerHTML = '<i class="fas fa-arrows-rotate mr-1"></i>Cập nhật tiến trình';
        reloadBtn.parentElement.insertBefore(syncBtn, reloadBtn);
        bindProgressActionButtons();
    }

    function getProgressMount() {
        return el('progressDashboardMount');
    }

    function ensurePanel() {
        if (el('adminProgressPanel')) {
            ensureProgressSyncButton();
            bindProgressActionButtons();
            return;
        }
        const dashboard = getProgressMount();
        if (!dashboard) return;

        const panel = document.createElement('section');
        panel.id = 'adminProgressPanel';
        panel.className = 'bg-white rounded-xl shadow-lg border border-slate-200 mb-8 p-6';
        panel.innerHTML = `
            <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div>
                    <h3 class="font-bold text-slate-800 text-lg">
                        <i class="fas fa-chart-line text-amber-600 mr-2"></i>Theo dõi tiến độ học sinh
                    </h3>
                    <p id="progressScopeHint" class="text-sm text-slate-500 mt-1">Chọn lớp (vd. 6A, 6B, 6C) để xem nhanh tiến độ từng lớp. Bấm <strong>Cập nhật tiến trình</strong> để hệ thống tính lại điểm luyện tập từ đáp án đã lưu của học sinh.</p>
                </div>
                <div class="flex flex-wrap gap-2">
                    <button id="progressSyncBtn" type="button" class="bg-teal-700 hover:bg-teal-800 text-white px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-arrows-rotate mr-1"></i>Cập nhật tiến trình
                    </button>
                    <button id="progressReloadBtn" type="button" class="bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-rotate-right mr-1"></i>Tải lại
                    </button>
                </div>
            </div>
            <div class="mt-5 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
                <label class="block text-sm font-bold text-slate-700">Bài học
                    <select id="progressLessonSelect" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-amber-500 outline-none"></select>
                </label>
                <label class="block text-sm font-bold text-slate-700">Lớp
                    <select id="progressClassFilter" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-amber-500 outline-none">
                        <option value="">Tất cả lớp</option>
                    </select>
                </label>
                <label class="block text-sm font-bold text-slate-700">Lọc trạng thái
                    <select id="progressStatusFilter" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-amber-500 outline-none">
                        <option value="">Tất cả</option>
                        <option value="needs">Cần luyện thêm</option>
                        <option value="mastered">Đã học xong</option>
                        <option value="not_started">Chưa bắt đầu</option>
                    </select>
                </label>
                <label class="block text-sm font-bold text-slate-700">Tìm học sinh
                    <input id="progressSearch" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-amber-500 outline-none" placeholder="Tên, tài khoản...">
                </label>
            </div>
            <div id="progressSummary" class="mt-5 grid grid-cols-2 md:grid-cols-4 gap-3"></div>
            <div class="mt-5 overflow-x-auto rounded border border-slate-200">
                <table class="min-w-full table-fixed divide-y divide-slate-200">
                    <colgroup>
                        <col style="width:26%">
                        <col style="width:14%">
                        <col style="width:10%">
                        <col style="width:32%">
                        <col style="width:18%">
                    </colgroup>
                    <thead class="bg-slate-50">
                        <tr>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Học sinh / Lớp</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Trạng thái</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Điểm luyện tập</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Cần lưu ý</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Cập nhật</th>
                        </tr>
                    </thead>
                    <tbody id="progressTableBody" class="divide-y divide-slate-100 bg-white"></tbody>
                </table>
            </div>
        `;
        dashboard.prepend(panel);
        applyPageScopeUi();

        bindProgressActionButtons();
        el('progressLessonSelect').onchange = event => {
            selectedLessonId = event.target.value;
            refresh();
        };
        el('progressClassFilter').onchange = event => {
            selectedClassName = event.target.value || '';
            localStorage.setItem('progress_class_filter', selectedClassName);
            render();
        };
        el('progressStatusFilter').onchange = render;
        el('progressSearch').oninput = render;
    }

    function normalizeClassName(value) {
        return String(value || '').trim();
    }

    function renderClasses() {
        const select = el('progressClassFilter');
        if (!select) return;
        const teacherClasses = teacherManagedClasses();
        const visibleClasses = teacherClasses.length
            ? classes.filter(className => teacherClasses.includes(className))
            : classes;

        if (isTeacherUser() && teacherClasses.length) {
            const options = teacherClasses.length > 1
                ? ['<option value="">Tất cả lớp phụ trách</option>']
                : [];
            select.innerHTML = options
                .concat(teacherClasses.map(className => `<option value="${escapeHtml(className)}">${escapeHtml(className)}</option>`))
                .join('');
            select.disabled = teacherClasses.length === 1;
            if (!selectedClassName || !teacherClasses.includes(selectedClassName)) {
                selectedClassName = teacherClasses.length === 1 ? teacherClasses[0] : '';
            }
            select.value = selectedClassName;
            localStorage.setItem('progress_class_filter', selectedClassName);
            return;
        }

        const options = ['<option value="">Tất cả lớp</option>']
            .concat(visibleClasses.map(className => `<option value="${escapeHtml(className)}">${escapeHtml(className)}</option>`));
        select.innerHTML = options.join('');
        select.disabled = false;
        if (selectedClassName && visibleClasses.includes(selectedClassName)) {
            select.value = selectedClassName;
        } else {
            selectedClassName = '';
            select.value = '';
            localStorage.setItem('progress_class_filter', '');
        }
    }

    function filteredRows() {
        const statusFilter = el('progressStatusFilter')?.value || '';
        const search = (el('progressSearch')?.value || '').toLowerCase();
        return rows.filter(row => {
            if (selectedClassName && normalizeClassName(row.class_name) !== selectedClassName) return false;
            const haystack = `${row.full_name} ${row.username} ${row.class_name}`.toLowerCase();
            if (search && !haystack.includes(search)) return false;
            if (statusFilter === 'needs') return row.needs_practice;
            if (statusFilter) return row.status === statusFilter;
            return true;
        });
    }

    function applyPageScopeUi() {
        const hint = el('progressScopeHint');
        if (!hint) return;
        const teacherClasses = teacherManagedClasses();
        if (isTeacherUser() && teacherClasses.length) {
            const classLabel = teacherClasses.length === 1
                ? `lớp ${teacherClasses[0]}`
                : `các lớp ${teacherClasses.join(', ')}`;
            hint.textContent = PAGE_SUBJECT
                ? `Theo dõi tiến độ ${PAGE_SUBJECT} — ${classLabel}. Chỉ hiển thị học sinh thuộc lớp phụ trách của bạn.`
                : `Theo dõi tiến độ ${classLabel}. Chỉ hiển thị học sinh thuộc lớp phụ trách của bạn.`;
            return;
        }
        if (PAGE_SUBJECT) {
            hint.textContent = `Theo dõi tiến độ ${PAGE_SUBJECT}. Chọn lớp (vd. 6A, 6B, 6C) để xem nhanh học sinh cần hỗ trợ.`;
        }
    }

    function renderLessons() {
        const select = el('progressLessonSelect');
        if (!select) return;
        const items = lessonsForPage();
        if (!items.length) {
            select.innerHTML = '<option value="">Chưa có bài học</option>';
            return;
        }
        select.innerHTML = items.map(lesson => (
            PAGE_SUBJECT
                ? `<option value="${lesson.id}">${escapeHtml(lesson.title)}</option>`
                : `<option value="${lesson.id}">${escapeHtml(lesson.subject)} - ${escapeHtml(lesson.title)}</option>`
        )).join('');
        if (items.some(item => String(item.id) === String(selectedLessonId))) {
            select.value = selectedLessonId;
        } else {
            selectedLessonId = String(items[0].id);
            select.value = selectedLessonId;
        }
    }

    function lessonCompletionFromRow(row) {
        if (row.status === 'mastered') return 100;
        const state = row.state || {};
        const theory = state.theoryDone ? 30 : 0;
        const examples = state.examplesDone ? 20 : 0;
        const practicePart = state.practiceDone ? 50 : 0;
        return Math.max(0, Math.min(100, theory + examples + practicePart));
    }

    function weakSkillText(row) {
        const scopedLessons = lessonsForPage();
        const lesson = scopedLessons.find(item => String(item.id) === String(selectedLessonId)) || scopedLessons[0];
        const skills = lesson?.skills || [];
        const weak = skills.filter(skill => Number(row.skill_scores?.[skill.id] || 0) < Number(skill.target || 80));
        if (row.status === 'not_started') return 'Chưa vào làm bài';
        const lessonPercent = lessonCompletionFromRow(row);
        if (!weak.length && row.score >= 80) return `Đạt mục tiêu · Tiến trình ${lessonPercent}%`;
        if (!weak.length) return `Tiến trình ${lessonPercent}%`;
        return weak.map(skill => skill.name || skill.id).join(', ') || 'Nên luyện thêm';
    }

    function renderSummary(viewRows) {
        const total = viewRows.length;
        const done = viewRows.filter(row => ['needs_practice', 'mastered'].includes(row.status)).length;
        const mastered = viewRows.filter(row => row.status === 'mastered').length;
        const needs = viewRows.filter(row => row.needs_practice).length;
        const teacherClasses = teacherManagedClasses();
        const scope = selectedClassName
            ? `Lớp ${selectedClassName}`
            : (isTeacherUser() && teacherClasses.length ? 'Tất cả lớp phụ trách' : 'Tất cả lớp');
        const cards = [
            [`Học sinh (${scope})`, total, 'text-slate-900'],
            ['Đã nộp bài', done, 'text-sky-700'],
            ['Đã học xong', mastered, 'text-teal-700'],
            ['Cần luyện thêm', needs, 'text-amber-700']
        ];
        el('progressSummary').innerHTML = cards.map(card => `
            <div class="rounded border border-slate-200 bg-slate-50 p-4">
                <div class="text-xs font-bold uppercase text-slate-500">${card[0]}</div>
                <div class="mt-1 text-2xl font-bold ${card[2]}">${card[1]}</div>
            </div>
        `).join('');
    }

    function compareClassNames(a, b) {
        const left = normalizeClassName(a) || '\uffff';
        const right = normalizeClassName(b) || '\uffff';
        return left.localeCompare(right, 'vi', { numeric: true, sensitivity: 'base' });
    }

    function sortRowsForView(viewRows) {
        const sorted = viewRows.slice();
        sorted.sort((a, b) => {
            if (!selectedClassName) {
                const byClass = compareClassNames(a.class_name, b.class_name);
                if (byClass !== 0) return byClass;
            }
            return String(a.full_name || '').localeCompare(String(b.full_name || ''), 'vi', { sensitivity: 'base' });
        });
        return sorted;
    }

    function renderRow(row) {
        const [label, tone] = statusLabel(row.status);
        const scoreTone = row.score >= 80 ? 'text-teal-700' : (row.score >= 50 ? 'text-amber-700' : 'text-rose-700');
        return `
            <tr class="hover:bg-slate-50">
                <td class="px-4 py-3 text-sm">
                    <div class="font-bold text-slate-900">${escapeHtml(row.full_name)}</div>
                    <div class="text-xs text-slate-500">${escapeHtml(row.username)}${selectedClassName ? '' : ` · ${escapeHtml(row.class_name || 'Chưa xếp lớp')}`}</div>
                </td>
                <td class="px-4 py-3 text-sm">
                    <span class="inline-flex rounded-full px-3 py-1 text-xs font-bold ${tone}">${label}</span>
                </td>
                <td class="px-4 py-3 text-sm">
                    <div class="font-bold ${scoreTone}">${row.score}%</div>
                    ${row.status !== 'not_started' ? `<div class="text-xs text-slate-500 mt-0.5">Tiến trình ${lessonCompletionFromRow(row)}%</div>` : ''}
                    ${row.practice_score_state !== null && row.practice_score_state !== undefined && row.practice_score_state !== row.score
                        ? `<div class="text-xs text-amber-700 mt-0.5">HS nộp: ${row.practice_score_state}% · DB: ${row.score}%</div>`
                        : ''}
                </td>
                <td class="px-4 py-3 text-sm text-slate-700 leading-6">${mathText(weakSkillText(row))}</td>
                <td class="px-4 py-3 text-xs text-slate-500">${escapeHtml(row.updated_at || 'Chưa có')}</td>
            </tr>
        `;
    }

    function renderClassGroupHeader(className, groupRows) {
        const needs = groupRows.filter(row => row.needs_practice).length;
        const mastered = groupRows.filter(row => row.status === 'mastered').length;
        return `
            <tr class="bg-amber-50 border-t border-amber-100">
                <td class="px-4 py-2.5 text-sm font-bold text-amber-900">Lớp ${escapeHtml(className)}</td>
                <td class="px-4 py-2.5 text-sm text-amber-800">${groupRows.length} học sinh</td>
                <td class="px-4 py-2.5 text-sm font-semibold text-teal-700">${mastered} đã học xong</td>
                <td class="px-4 py-2.5 text-sm font-semibold text-amber-700">${needs} cần luyện</td>
                <td class="px-4 py-2.5 text-xs text-slate-400">—</td>
            </tr>
        `;
    }

    function render() {
        const body = el('progressTableBody');
        if (!body) return;
        const filtered = sortRowsForView(filteredRows());

        renderSummary(filtered);

        if (!filtered.length) {
            body.innerHTML = '<tr><td colspan="5" class="px-4 py-8 text-center text-slate-400 italic">Chưa có dữ liệu phù hợp.</td></tr>';
            return;
        }

        if (!selectedClassName) {
            const groups = new Map();
            filtered.forEach(row => {
                const key = normalizeClassName(row.class_name) || 'Chưa xếp lớp';
                if (!groups.has(key)) groups.set(key, []);
                groups.get(key).push(row);
            });
            body.innerHTML = [...groups.entries()].map(([className, groupRows]) => (
                renderClassGroupHeader(className, groupRows) + groupRows.map(renderRow).join('')
            )).join('');
        } else {
            body.innerHTML = filtered.map(renderRow).join('');
        }
        typesetMath();
    }

    async function syncProgress() {
        const key = getAdminKey();
        if (!key && !isTeacherUser()) return;
        if (!getProgressMount()) return;
        ensurePanel();
        const syncBtn = el('progressSyncBtn');
        const lessonId = selectedLessonId || el('progressLessonSelect')?.value || '';
        if (!lessonId) {
            alert('Chưa chọn bài học để cập nhật tiến độ.');
            return;
        }
        const oldHtml = syncBtn?.innerHTML || '';
        if (syncBtn) {
            syncBtn.disabled = true;
            syncBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-1"></i>Đang cập nhật...';
        }
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (key) headers['X-Admin-Key'] = key;
            const res = await fetch('api/admin_progress.php', {
                method: 'POST',
                credentials: 'include',
                headers,
                cache: 'no-store',
                body: JSON.stringify({
                    action: 'recalc_progress',
                    lesson_id: Number(lessonId)
                })
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Không cập nhật được tiến độ.');
            await refresh();
            alert(data.message || `Đã cập nhật tiến độ cho ${data.updated || 0} học sinh.`);
        } catch (err) {
            console.error('syncProgress error:', err);
            alert(err.message || 'Không cập nhật được tiến độ học sinh.');
        } finally {
            if (syncBtn) {
                syncBtn.disabled = false;
                syncBtn.innerHTML = oldHtml;
            }
        }
    }

    async function refresh() {
        const key = getAdminKey();
        if (!key && !isTeacherUser()) return;
        if (!getProgressMount()) return;
        ensurePanel();
        const qs = selectedLessonId ? `?lesson_id=${encodeURIComponent(selectedLessonId)}` : '';
        const headers = key ? { 'X-Admin-Key': key } : {};
        const res = await fetch(`api/admin_progress.php${qs}`, {
            credentials: 'include',
            headers,
            cache: 'no-store'
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Không tải được tiến độ.');
        lessons = data.lessons || [];
        rows = data.rows || [];
        classes = Array.isArray(data.classes) ? data.classes : [];
        managedClasses = Array.isArray(data.managed_classes) ? data.managed_classes : [];
        if (managedClasses.length) {
            localStorage.setItem('userClassName', managedClasses.join(', '));
        }
        const scopedLessons = lessonsForPage();
        const preferredLessonId = String(data.lesson_id || '');
        if (scopedLessons.some(item => String(item.id) === preferredLessonId)) {
            selectedLessonId = preferredLessonId;
        } else {
            selectedLessonId = String(scopedLessons[0]?.id || '');
        }
        renderLessons();
        renderClasses();
        render();
        if (typeof window.ensureAdminTabs === 'function') window.ensureAdminTabs();
    }

    function wrapLoadUsers() {
        if (typeof window.loadUsers !== 'function' || window.loadUsers.__progressWrapped) return;
        const original = window.loadUsers;
        const wrapped = async function (...args) {
            const result = await original.apply(this, args);
            await refresh().catch(console.warn);
            return result;
        };
        wrapped.__progressWrapped = true;
        window.loadUsers = wrapped;
    }

    window.refreshAdminProgress = refresh;
    window.syncAdminProgress = syncProgress;

    function boot() {
        if (!getProgressMount()) return;
        ensurePanel();
        wrapLoadUsers();
        if (isTeacherUser()) refresh().catch(console.warn);
    }

    document.addEventListener('adminLessonsChanged', () => refresh().catch(console.warn));

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
