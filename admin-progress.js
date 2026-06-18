(function () {
    let lessons = [];
    let rows = [];
    let classes = [];
    let selectedLessonId = '';
    let selectedClassName = localStorage.getItem('progress_class_filter') || '';

    function el(id) { return document.getElementById(id); }

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

    function ensurePanel() {
        if (el('adminProgressPanel')) return;
        const dashboard = isTeacherUser() ? el('lessonDesignerMount') : null;
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
                    <p class="text-sm text-slate-500 mt-1">Chọn lớp (vd. 6A, 6B, 6C) để xem nhanh tiến độ từng lớp — hoặc xem tất cả lớp được nhóm theo tên lớp.</p>
                </div>
                <button id="progressReloadBtn" class="bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 px-4 py-2.5 rounded font-bold text-sm">
                    <i class="fas fa-rotate-right mr-1"></i>Tải lại
                </button>
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
                <table class="min-w-full divide-y divide-slate-200">
                    <thead class="bg-slate-50">
                        <tr>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Học sinh / Lớp</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Trạng thái</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Điểm</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Cần lưu ý</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Cập nhật</th>
                        </tr>
                    </thead>
                    <tbody id="progressTableBody" class="divide-y divide-slate-100 bg-white"></tbody>
                </table>
            </div>
        `;
        dashboard.prepend(panel);

        el('progressReloadBtn').onclick = () => refresh();
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
        const options = ['<option value="">Tất cả lớp</option>']
            .concat(classes.map(className => `<option value="${escapeHtml(className)}">${escapeHtml(className)}</option>`));
        select.innerHTML = options.join('');
        if (selectedClassName && classes.includes(selectedClassName)) {
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

    function renderLessons() {
        const select = el('progressLessonSelect');
        if (!select) return;
        select.innerHTML = lessons.map(lesson => `
            <option value="${lesson.id}">${escapeHtml(lesson.subject)} - ${escapeHtml(lesson.title)}</option>
        `).join('');
        if (selectedLessonId) select.value = selectedLessonId;
    }

    function weakSkillText(row) {
        const lesson = lessons.find(item => String(item.id) === String(selectedLessonId)) || lessons[0];
        const skills = lesson?.skills || [];
        const weak = skills.filter(skill => Number(row.skill_scores?.[skill.id] || 0) < Number(skill.target || 80));
        if (row.status === 'not_started') return 'Chưa vào làm bài';
        if (!weak.length && !row.needs_practice) return 'Đạt mục tiêu';
        return weak.map(skill => skill.name || skill.id).join(', ') || 'Nên luyện thêm';
    }

    function renderSummary(viewRows) {
        const total = viewRows.length;
        const done = viewRows.filter(row => ['needs_practice', 'mastered'].includes(row.status)).length;
        const mastered = viewRows.filter(row => row.status === 'mastered').length;
        const needs = viewRows.filter(row => row.needs_practice).length;
        const scope = selectedClassName ? `Lớp ${selectedClassName}` : 'Tất cả lớp';
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
                <td class="px-4 py-3 text-sm font-bold ${scoreTone}">${row.score}%</td>
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
                <td colspan="5" class="px-4 py-2.5">
                    <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm">
                        <span class="font-bold text-amber-900">Lớp ${escapeHtml(className)}</span>
                        <span class="text-amber-800">${groupRows.length} học sinh</span>
                        <span class="text-teal-700">${mastered} đã học xong</span>
                        <span class="text-amber-700">${needs} cần luyện</span>
                    </div>
                </td>
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

    async function refresh() {
        const key = getAdminKey();
        if (!key && !isTeacherUser()) return;
        ensurePanel();
        const qs = selectedLessonId ? `?lesson_id=${encodeURIComponent(selectedLessonId)}` : '';
        const headers = key ? { 'X-Admin-Key': key } : {};
        const res = await fetch(`api/admin_progress.php${qs}`, {
            headers,
            cache: 'no-store'
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Không tải được tiến độ.');
        lessons = data.lessons || [];
        rows = data.rows || [];
        classes = Array.isArray(data.classes) ? data.classes : [];
        selectedLessonId = String(data.lesson_id || lessons[0]?.id || '');
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

    function boot() {
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
