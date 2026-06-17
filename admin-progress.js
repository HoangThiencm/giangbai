(function () {
    let lessons = [];
    let rows = [];
    let selectedLessonId = '';

    function el(id) { return document.getElementById(id); }

    function getAdminKey() {
        try {
            return typeof cachedKey !== 'undefined' ? cachedKey : window.cachedKey;
        } catch {
            return window.cachedKey;
        }
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

    function statusLabel(status) {
        const map = {
            not_started: ['Chưa bắt đầu', 'bg-slate-100 text-slate-700'],
            in_progress: ['Đang học', 'bg-sky-100 text-sky-700'],
            needs_practice: ['Cần luyện thêm', 'bg-amber-100 text-amber-800'],
            mastered: ['Đã vững', 'bg-teal-100 text-teal-800']
        };
        return map[status] || map.not_started;
    }

    function ensurePanel() {
        if (el('adminProgressPanel')) return;
        const dashboard = el('dashboardSection');
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
                    <p class="text-sm text-slate-500 mt-1">Xem học sinh nào đã làm bài, điểm hiện tại và ai cần luyện thêm.</p>
                </div>
                <button id="progressReloadBtn" class="bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 px-4 py-2.5 rounded font-bold text-sm">
                    <i class="fas fa-rotate-right mr-1"></i>Tải lại
                </button>
            </div>
            <div class="mt-5 grid grid-cols-1 md:grid-cols-[1fr_180px_180px] gap-3">
                <label class="block text-sm font-bold text-slate-700">Bài học
                    <select id="progressLessonSelect" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-amber-500 outline-none"></select>
                </label>
                <label class="block text-sm font-bold text-slate-700">Lọc trạng thái
                    <select id="progressStatusFilter" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-amber-500 outline-none">
                        <option value="">Tất cả</option>
                        <option value="needs">Cần luyện thêm</option>
                        <option value="mastered">Đã vững</option>
                        <option value="not_started">Chưa bắt đầu</option>
                    </select>
                </label>
                <label class="block text-sm font-bold text-slate-700">Tìm học sinh
                    <input id="progressSearch" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-amber-500 outline-none" placeholder="Tên, lớp...">
                </label>
            </div>
            <div id="progressSummary" class="mt-5 grid grid-cols-2 md:grid-cols-4 gap-3"></div>
            <div class="mt-5 overflow-x-auto rounded border border-slate-200">
                <table class="min-w-full divide-y divide-slate-200">
                    <thead class="bg-slate-50">
                        <tr>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Học sinh</th>
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
        el('progressStatusFilter').onchange = render;
        el('progressSearch').oninput = render;
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

    function renderSummary(filteredRows) {
        const total = rows.length;
        const done = rows.filter(row => ['needs_practice', 'mastered'].includes(row.status)).length;
        const mastered = rows.filter(row => row.status === 'mastered').length;
        const needs = rows.filter(row => row.needs_practice).length;
        const cards = [
            ['Tổng học sinh', total, 'text-slate-900'],
            ['Đã nộp bài', done, 'text-sky-700'],
            ['Đã vững', mastered, 'text-teal-700'],
            ['Cần luyện thêm', needs, 'text-amber-700']
        ];
        el('progressSummary').innerHTML = cards.map(card => `
            <div class="rounded border border-slate-200 bg-slate-50 p-4">
                <div class="text-xs font-bold uppercase text-slate-500">${card[0]}</div>
                <div class="mt-1 text-2xl font-bold ${card[2]}">${card[1]}</div>
            </div>
        `).join('');
    }

    function render() {
        const body = el('progressTableBody');
        if (!body) return;
        const statusFilter = el('progressStatusFilter')?.value || '';
        const search = (el('progressSearch')?.value || '').toLowerCase();
        let filtered = rows.filter(row => {
            const haystack = `${row.full_name} ${row.username} ${row.class_name}`.toLowerCase();
            if (search && !haystack.includes(search)) return false;
            if (statusFilter === 'needs') return row.needs_practice;
            if (statusFilter) return row.status === statusFilter;
            return true;
        });

        renderSummary(filtered);

        if (!filtered.length) {
            body.innerHTML = '<tr><td colspan="5" class="px-4 py-8 text-center text-slate-400 italic">Chưa có dữ liệu phù hợp.</td></tr>';
            return;
        }

        body.innerHTML = filtered.map(row => {
            const [label, tone] = statusLabel(row.status);
            const scoreTone = row.score >= 80 ? 'text-teal-700' : (row.score >= 50 ? 'text-amber-700' : 'text-rose-700');
            return `
                <tr class="hover:bg-slate-50">
                    <td class="px-4 py-3 text-sm">
                        <div class="font-bold text-slate-900">${escapeHtml(row.full_name)}</div>
                        <div class="text-xs text-slate-500">${escapeHtml(row.username)} · ${escapeHtml(row.class_name || 'Chưa xếp lớp')}</div>
                    </td>
                    <td class="px-4 py-3 text-sm">
                        <span class="inline-flex rounded-full px-3 py-1 text-xs font-bold ${tone}">${label}</span>
                    </td>
                    <td class="px-4 py-3 text-sm font-bold ${scoreTone}">${row.score}%</td>
                    <td class="px-4 py-3 text-sm text-slate-700">${escapeHtml(weakSkillText(row))}</td>
                    <td class="px-4 py-3 text-xs text-slate-500">${escapeHtml(row.updated_at || 'Chưa có')}</td>
                </tr>
            `;
        }).join('');
    }

    async function refresh() {
        const key = getAdminKey();
        if (!key) return;
        ensurePanel();
        const qs = selectedLessonId ? `?lesson_id=${encodeURIComponent(selectedLessonId)}` : '';
        const res = await fetch(`api/admin_progress.php${qs}`, {
            headers: { 'X-Admin-Key': key },
            cache: 'no-store'
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Không tải được tiến độ.');
        lessons = data.lessons || [];
        rows = data.rows || [];
        selectedLessonId = String(data.lesson_id || lessons[0]?.id || '');
        renderLessons();
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
        if (getAdminKey()) refresh().catch(console.warn);
    }

    document.addEventListener('adminLessonsChanged', () => refresh().catch(console.warn));

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
