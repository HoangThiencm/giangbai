(function () {
    const PAGE_SUBJECT = String(window.LOTRINH_SUBJECT || '').trim();

    let lessons = [];
    let rows = [];
    let classes = [];
    let managedClasses = [];
    let classSubjects = {};
    let submissions = [];
    let selectedLessonId = '';
    let selectedClassName = localStorage.getItem('progress_class_filter') || '';
    let weakThreshold = normalizeThreshold(localStorage.getItem('progress_weak_threshold') || 80);
    let inactiveDays = normalizeInactiveDays(localStorage.getItem('progress_inactive_days') || 7);

    const LOTRINH_SUBJECTS = ['Toán 9', 'Toán 8', 'Toán 7', 'Toán 6', 'Toán 5', 'Toán 4'];

    function el(id) { return document.getElementById(id); }

    function lessonsForPage() {
        if (!PAGE_SUBJECT) return lessons;
        return lessons.filter(lesson => String(lesson.subject || '').trim() === PAGE_SUBJECT);
    }

    function inferSubjectFromClassName(className) {
        const name = normalizeClassName(className);
        if (!name) return '';
        for (const subject of LOTRINH_SUBJECTS) {
            if (name.toLowerCase().includes(subject.toLowerCase())) return subject;
        }
        const match = name.match(/\b([4-9])[A-Za-z]{0,3}\b/);
        return match ? `Toán ${match[1]}` : '';
    }

    function subjectForClass(className) {
        const normalized = normalizeClassName(className);
        if (!normalized) return '';
        return classSubjects[normalized] || inferSubjectFromClassName(normalized);
    }

    function lessonsForClassFilter() {
        let items = lessonsForPage();
        if (!selectedClassName) return items;
        const subject = subjectForClass(selectedClassName);
        if (!subject) return items;
        const scoped = items.filter(lesson => String(lesson.subject || '').trim() === subject);
        return scoped.length ? scoped : items;
    }

    function syncLessonSelectionForClass() {
        const items = lessonsForClassFilter();
        if (!items.length) {
            selectedLessonId = '';
            return false;
        }
        const previous = selectedLessonId;
        if (!items.some(item => String(item.id) === String(selectedLessonId))) {
            selectedLessonId = String(items[0].id);
        }
        return selectedLessonId !== previous;
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
        const exportBtn = el('progressExportBtn');
        if (reloadBtn && reloadBtn.dataset.boundProgressReload !== '1') {
            reloadBtn.dataset.boundProgressReload = '1';
            reloadBtn.onclick = () => refresh();
        }
        if (syncBtn && syncBtn.dataset.boundProgressSync !== '1') {
            syncBtn.dataset.boundProgressSync = '1';
            syncBtn.onclick = () => syncProgress();
        }
        if (exportBtn && exportBtn.dataset.boundProgressExport !== '1') {
            exportBtn.dataset.boundProgressExport = '1';
            exportBtn.onclick = () => exportProgressExcel();
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
                    <button id="progressExportBtn" type="button" class="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-file-excel mr-1"></i>Xuất Excel
                    </button>
                    <button id="progressSyncBtn" type="button" class="bg-teal-700 hover:bg-teal-800 text-white px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-arrows-rotate mr-1"></i>Cập nhật tiến trình
                    </button>
                    <button id="progressReloadBtn" type="button" class="bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-rotate-right mr-1"></i>Tải lại
                    </button>
                </div>
            </div>
            <div class="mt-5 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-3">
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
                        <option value="weak">Điểm dưới ngưỡng</option>
                        <option value="inactive">Chưa vào học</option>
                        <option value="needs">Cần luyện thêm</option>
                        <option value="mastered">Đã học xong</option>
                        <option value="not_started">Chưa bắt đầu</option>
                    </select>
                </label>
                <label class="block text-sm font-bold text-slate-700">Ngưỡng điểm yếu
                    <input id="progressWeakThreshold" type="number" min="0" max="100" step="5" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-amber-500 outline-none" value="80">
                </label>
                <label class="block text-sm font-bold text-slate-700">Chưa vào học từ
                    <select id="progressInactiveDays" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-amber-500 outline-none">
                        <option value="3">3 ngày</option>
                        <option value="7">7 ngày</option>
                        <option value="14">14 ngày</option>
                        <option value="30">30 ngày</option>
                    </select>
                </label>
                <label class="block text-sm font-bold text-slate-700">Tìm học sinh
                    <input id="progressSearch" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-amber-500 outline-none" placeholder="Tên, tài khoản...">
                </label>
            </div>
            <section id="progressTodayActions" class="mt-5 rounded-lg border border-amber-200 bg-amber-50/70 p-4"></section>
            <div id="progressSummary" class="mt-5 grid grid-cols-2 md:grid-cols-5 gap-3"></div>
            <p class="mt-4 text-xs text-slate-500"><i class="fas fa-folder-open mr-1 text-sky-600"></i>Mỗi học sinh một dòng: tiến độ luyện tập và bài nộp Drive (tab <strong>Bài tập</strong> trong lộ trình).</p>
            <div class="mt-2 overflow-x-auto rounded border border-slate-200">
                <table class="min-w-full table-fixed divide-y divide-slate-200">
                    <colgroup>
                        <col style="width:20%">
                        <col style="width:22%">
                        <col style="width:22%">
                        <col style="width:24%">
                        <col style="width:12%">
                    </colgroup>
                    <thead class="bg-slate-50">
                        <tr>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Học sinh / Lớp</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Tiến độ học tập</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Bài nộp giáo viên</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Cần lưu ý</th>
                            <th class="px-4 py-3 text-left text-xs font-bold uppercase text-slate-500">Cập nhật</th>
                        </tr>
                    </thead>
                    <tbody id="progressTableBody" class="divide-y divide-slate-100 bg-white"></tbody>
                </table>
            </div>
            <div id="progressDrivePreviewModal" class="fixed inset-0 z-[80] hidden items-center justify-center bg-slate-900/60 p-3 sm:p-6" style="backdrop-filter:blur(2px)">
                <div class="flex h-full max-h-[92vh] w-full max-w-6xl flex-col overflow-hidden rounded-2xl bg-white shadow-2xl">
                    <div class="flex items-center justify-between border-b border-slate-200 px-5 py-3">
                        <div>
                            <p class="text-[11px] font-extrabold uppercase tracking-[.14em] text-sky-700">Xem bài nộp</p>
                            <h2 id="progressDrivePreviewTitle" class="text-base font-black text-slate-900">Tệp đính kèm</h2>
                        </div>
                        <button id="progressCloseDrivePreviewBtn" type="button" class="grid h-10 w-10 place-items-center rounded-full bg-slate-100 text-slate-600 hover:bg-slate-200">
                            <i class="fas fa-xmark"></i>
                        </button>
                    </div>
                    <iframe id="progressDrivePreviewFrame" class="min-h-0 flex-1 bg-slate-100" title="Xem bài nộp trong trang"></iframe>
                </div>
            </div>
        `;
        dashboard.prepend(panel);
        applyPageScopeUi();

        bindProgressActionButtons();
        el('progressCloseDrivePreviewBtn')?.addEventListener('click', closeDrivePreview);
        el('progressDrivePreviewModal')?.addEventListener('click', event => {
            if (event.target === el('progressDrivePreviewModal')) closeDrivePreview();
        });
        el('progressLessonSelect').onchange = event => {
            selectedLessonId = event.target.value;
            refresh();
        };
        el('progressClassFilter').onchange = async event => {
            selectedClassName = event.target.value || '';
            localStorage.setItem('progress_class_filter', selectedClassName);
            const lessonChanged = syncLessonSelectionForClass();
            renderLessons();
            if (lessonChanged && selectedLessonId) {
                try {
                    await refresh();
                } catch (err) {
                    console.warn(err);
                    render();
                }
                return;
            }
            render();
        };
        el('progressStatusFilter').onchange = render;
        const weakInput = el('progressWeakThreshold');
        if (weakInput) {
            weakInput.value = String(weakThreshold);
            weakInput.onchange = event => {
                weakThreshold = normalizeThreshold(event.target.value);
                event.target.value = String(weakThreshold);
                localStorage.setItem('progress_weak_threshold', String(weakThreshold));
                render();
            };
        }
        const inactiveSelect = el('progressInactiveDays');
        if (inactiveSelect) {
            inactiveSelect.value = String(inactiveDays);
            inactiveSelect.onchange = event => {
                inactiveDays = normalizeInactiveDays(event.target.value);
                event.target.value = String(inactiveDays);
                localStorage.setItem('progress_inactive_days', String(inactiveDays));
                render();
            };
        }
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

    function normalizeThreshold(value) {
        const parsed = Number(value);
        if (!Number.isFinite(parsed)) return 80;
        return Math.max(0, Math.min(100, Math.round(parsed)));
    }

    function normalizeInactiveDays(value) {
        const parsed = Number(value);
        return [3, 7, 14, 30].includes(parsed) ? parsed : 7;
    }

    function scopeRows() {
        return rows.filter(row => !selectedClassName || normalizeClassName(row.class_name) === selectedClassName);
    }

    function scopedSubmissions() {
        return submissions.filter(item => !selectedClassName || normalizeClassName(item.class_name) === selectedClassName);
    }

    function submissionByStudentId() {
        const map = new Map();
        scopedSubmissions().forEach(item => {
            const key = Number(item.student_id);
            if (!map.has(key)) map.set(key, item);
        });
        return map;
    }

    function driveFileIdFromUrl(url) {
        const value = String(url || '');
        const match = value.match(/\/d\/([A-Za-z0-9_-]+)/) || value.match(/[?&]id=([A-Za-z0-9_-]+)/);
        return match ? match[1] : '';
    }

    function openDrivePreview(fileUrl, title = 'Tệp đính kèm') {
        const fileId = driveFileIdFromUrl(fileUrl);
        const modal = el('progressDrivePreviewModal');
        const frame = el('progressDrivePreviewFrame');
        const titleEl = el('progressDrivePreviewTitle');
        if (!modal || !frame) {
            if (fileUrl) window.open(fileUrl, '_blank', 'noopener');
            return;
        }
        if (titleEl) titleEl.textContent = title;
        frame.src = fileId
            ? `https://drive.google.com/file/d/${encodeURIComponent(fileId)}/preview`
            : fileUrl;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.body.classList.add('overflow-hidden');
    }

    function closeDrivePreview() {
        const modal = el('progressDrivePreviewModal');
        const frame = el('progressDrivePreviewFrame');
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
        if (frame) frame.src = 'about:blank';
        document.body.classList.remove('overflow-hidden');
    }

    function renderSubmissionFiles(files) {
        const list = Array.isArray(files) ? files : [];
        if (!list.length) return '<span class="text-xs text-slate-400">Không có tệp</span>';
        return list.map(file => {
            const name = escapeHtml(file.original_name || 'Tệp');
            const url = String(file.view_url || '');
            const fileId = driveFileIdFromUrl(url);
            if (fileId || url) {
                return `<button type="button" data-preview-url="${escapeHtml(url)}" data-preview-title="${name}" class="mb-1 block max-w-full truncate rounded bg-sky-100 px-2 py-1 text-left text-xs font-bold text-sky-800 hover:bg-sky-200">
                    <i class="fas fa-paperclip mr-1"></i>${name}
                </button>`;
            }
            return `<span class="block text-xs text-slate-500">${name}</span>`;
        }).join('');
    }

    function renderProgressCell(row) {
        const [label, tone] = statusLabel(row.status);
        const scoreTone = row.score >= 80 ? 'text-teal-700' : (row.score >= 50 ? 'text-amber-700' : 'text-rose-700');
        return `
            <div class="space-y-1">
                <span class="inline-flex rounded-full px-3 py-1 text-xs font-bold ${tone}">${label}</span>
                <div class="font-bold ${scoreTone}">${row.score}%</div>
                ${row.status !== 'not_started' ? `<div class="text-xs text-slate-500">Tiến trình ${lessonCompletionFromRow(row)}%</div>` : ''}
                ${row.practice_score_state !== null && row.practice_score_state !== undefined && row.practice_score_state !== row.score
                    ? `<div class="text-xs text-amber-700">Làm bài: ${row.practice_score_state}% · DB: ${row.score}%</div>`
                    : ''}
            </div>
        `;
    }

    function renderSubmissionCell(row, submissionMap) {
        const submission = submissionMap.get(Number(row.student_id));
        if (!submission) {
            return '<span class="inline-flex rounded-full bg-slate-100 px-2.5 py-1 text-xs font-bold text-slate-500">Chưa nộp Drive</span>';
        }
        const when = String(submission.submitted_at || '').replace('T', ' ').slice(0, 16);
        const note = submission.note ? `<div class="mt-1 text-xs text-slate-600 italic">${escapeHtml(submission.note)}</div>` : '';
        return `
            <div>
                <span class="inline-flex rounded-full bg-sky-100 px-2.5 py-1 text-xs font-bold text-sky-800">Đã nộp · ${escapeHtml(when)}</span>
                <div class="mt-1.5">${renderSubmissionFiles(submission.files)}</div>
                ${note}
            </div>
        `;
    }

    function bindSubmissionPreviewButtons(root) {
        (root || document).querySelectorAll('[data-preview-url]').forEach(button => {
            if (button.dataset.boundPreview === '1') return;
            button.dataset.boundPreview = '1';
            button.addEventListener('click', () => {
                openDrivePreview(button.dataset.previewUrl || '', button.dataset.previewTitle || 'Tệp đính kèm');
            });
        });
    }

    async function loadSubmissions() {
        const lessonId = selectedLessonId || el('progressLessonSelect')?.value || '';
        if (!lessonId) {
            submissions = [];
            render();
            return;
        }
        try {
            const res = await fetch(`api/lesson_self_practice.php?action=list&lesson_id=${encodeURIComponent(lessonId)}`, {
                credentials: 'include',
                cache: 'no-store'
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Không tải được bài nộp.');
            submissions = Array.isArray(data.submissions) ? data.submissions : [];
            render();
        } catch (err) {
            submissions = [];
            console.warn('loadSubmissions:', err);
            render();
        }
    }

    function parseServerDate(value) {
        if (!value) return null;
        const normalized = String(value).includes('T') ? String(value) : String(value).replace(' ', 'T');
        const parsed = new Date(normalized);
        return Number.isNaN(parsed.getTime()) ? null : parsed;
    }

    function daysSince(value) {
        const date = parseServerDate(value);
        if (!date) return null;
        return Math.max(0, Math.floor((Date.now() - date.getTime()) / 86400000));
    }

    function isWeakRow(row) {
        return row.status !== 'not_started' && Number(row.score || 0) < weakThreshold;
    }

    function isInactiveRow(row) {
        const days = daysSince(row.last_login_at);
        return days === null || days >= inactiveDays;
    }

    function inactiveLabel(row) {
        const days = daysSince(row.last_login_at);
        if (days === null) return 'Chưa từng đăng nhập';
        return days === 0 ? 'Đã vào học hôm nay' : `${days} ngày chưa vào học`;
    }

    function filteredRows() {
        const statusFilter = el('progressStatusFilter')?.value || '';
        const search = (el('progressSearch')?.value || '').toLowerCase();
        return scopeRows().filter(row => {
            const haystack = `${row.full_name} ${row.username} ${row.class_name}`.toLowerCase();
            if (search && !haystack.includes(search)) return false;
            if (statusFilter === 'weak') return isWeakRow(row);
            if (statusFilter === 'inactive') return isInactiveRow(row);
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
        const items = lessonsForClassFilter();
        const subjectHint = selectedClassName ? subjectForClass(selectedClassName) : '';
        if (!items.length) {
            select.innerHTML = '<option value="">Chưa có bài học</option>';
            return;
        }
        const showSubjectPrefix = !PAGE_SUBJECT && !subjectHint;
        select.innerHTML = items.map(lesson => (
            showSubjectPrefix
                ? `<option value="${lesson.id}">${escapeHtml(lesson.subject)} - ${escapeHtml(lesson.title)}</option>`
                : `<option value="${lesson.id}">${escapeHtml(lesson.title)}</option>`
        )).join('');
        syncLessonSelectionForClass();
        if (selectedLessonId) {
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

    function currentLessonMeta() {
        const items = lessonsForClassFilter();
        return items.find(item => String(item.id) === String(selectedLessonId)) || items[0] || null;
    }

    function weakSkillText(row, lessonOverride = null) {
        const lesson = lessonOverride || currentLessonMeta();
        const skills = lesson?.skills || [];
        const weak = skills.filter(skill => Number(row.skill_scores?.[skill.id] || 0) < Number(skill.target || 80));
        if (row.status === 'not_started') return 'Chưa vào làm bài';
        const lessonPercent = lessonCompletionFromRow(row);
        if (!weak.length && row.score >= 80) return `Đạt mục tiêu · Tiến trình ${lessonPercent}%`;
        if (!weak.length) return `Tiến trình ${lessonPercent}%`;
        return weak.map(skill => skill.name || skill.id).join(', ') || 'Nên luyện thêm';
    }

    function plainText(value) {
        return decodeBasicEntities(String(value ?? ''))
            .replace(/\$\$?[^$]+\$\$?/g, ' ')
            .replace(/\\\[([\s\S]*?)\\\]/g, ' ')
            .replace(/\\\(([\s\S]*?)\\\)/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
    }

    function fileSlug(value, fallback = 'TienDo') {
        const slug = String(value || '').replace(/[^\w\-]+/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
        return slug || fallback;
    }

    function formatExportTimestamp() {
        const now = new Date();
        const pad = num => String(num).padStart(2, '0');
        return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}`;
    }

    function buildCurrentLessonSheetRows(viewRows) {
        const lesson = currentLessonMeta();
        const lessonTitle = lesson ? `${lesson.subject || ''} - ${lesson.title || ''}`.trim() : 'Chưa chọn bài';
        const classLabel = selectedClassName || (isTeacherUser() && teacherManagedClasses().length ? 'Tất cả lớp phụ trách' : 'Tất cả lớp');
        const statusFilter = el('progressStatusFilter')?.value || '';
        const statusLabels = {
            weak: `Điểm dưới ${weakThreshold}%`,
            inactive: `Chưa vào học từ ${inactiveDays} ngày`,
            needs: 'Cần luyện thêm',
            mastered: 'Đã học xong',
            not_started: 'Chưa bắt đầu'
        };
        const exportedAt = new Intl.DateTimeFormat('vi-VN', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date());
        const meta = [
            ['BÁO CÁO TIẾN ĐỘ HỌC SINH'],
            [`Bài học: ${lessonTitle}`],
            [`Lớp: ${classLabel}`],
            [`Lọc trạng thái: ${statusLabels[statusFilter] || 'Tất cả'}`],
            [`Xuất lúc: ${exportedAt}`],
            [],
            ['STT', 'Họ và tên', 'Tài khoản', 'Lớp', 'Trạng thái', 'Điểm luyện tập (%)', 'Tiến trình (%)', 'Cần lưu ý', 'Lần vào học gần nhất', 'Số ngày chưa vào học', 'Cập nhật tiến độ']
        ];
        const dataRows = viewRows.map((row, index) => {
            const [statusText] = statusLabel(row.status);
            return [
                index + 1,
                row.full_name || '',
                row.username || '',
                row.class_name || '',
                statusText,
                row.score ?? 0,
                row.status === 'not_started' ? 0 : lessonCompletionFromRow(row),
                plainText(weakSkillText(row)),
                row.last_login_at || 'Chưa từng đăng nhập',
                inactiveLabel(row),
                row.updated_at || 'Chưa có'
            ];
        });
        return meta.concat(dataRows);
    }

    function buildMatrixSheetRows(matrixData) {
        const lessonsList = matrixData.lessons || [];
        const matrixRows = matrixData.rows || [];
        const classLabel = matrixData.class_name || selectedClassName || 'Tất cả lớp';
        const subjectLabel = matrixData.subject || subjectForClass(classLabel) || '';
        const exportedAt = new Intl.DateTimeFormat('vi-VN', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date());
        const header = ['STT', 'Họ và tên', 'Tài khoản', 'Lớp'];
        lessonsList.forEach(lesson => {
            header.push(`${lesson.title || lesson.chapter || 'Bài'} (%)`);
            header.push(`${lesson.title || lesson.chapter || 'Bài'} - TT`);
        });
        const meta = [
            ['TỔNG HỢP TIẾN ĐỘ THEO LỚP'],
            [`Lớp: ${classLabel}`]
        ];
        if (subjectLabel) meta.push([`Môn: ${subjectLabel}`]);
        meta.push(
            [`Số bài: ${lessonsList.length}`],
            [`Xuất lúc: ${exportedAt}`],
            [],
            header
        );
        const dataRows = matrixRows.map((row, index) => {
            const line = [
                index + 1,
                row.full_name || '',
                row.username || '',
                row.class_name || ''
            ];
            (row.lessons || []).forEach(item => {
                line.push(item.score ?? 0);
                line.push(item.status_label || statusLabel(item.status || 'not_started')[0]);
            });
            return line;
        });
        return meta.concat(dataRows);
    }

    async function fetchProgressMatrix() {
        const key = getAdminKey();
        const params = new URLSearchParams({ matrix: '1' });
        if (selectedClassName) params.set('class_name', selectedClassName);
        const subject = subjectForClass(selectedClassName);
        if (subject) params.set('subject', subject);
        const headers = key ? { 'X-Admin-Key': key } : {};
        const res = await fetch(`api/admin_progress.php?${params.toString()}`, {
            credentials: 'include',
            headers,
            cache: 'no-store'
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Không tải được dữ liệu tổng hợp.');
        return data;
    }

    async function exportProgressExcel() {
        if (typeof window.XLSX === 'undefined') {
            alert('Thư viện Excel chưa tải. Vui lòng tải lại trang.');
            return;
        }
        const viewRows = sortRowsForView(filteredRows());
        if (!viewRows.length) {
            alert('Không có dữ liệu để xuất Excel.');
            return;
        }

        const exportBtn = el('progressExportBtn');
        const oldHtml = exportBtn?.innerHTML || '';
        if (exportBtn) {
            exportBtn.disabled = true;
            exportBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-1"></i>Đang xuất...';
        }

        try {
            const workbook = XLSX.utils.book_new();
            const currentSheet = XLSX.utils.aoa_to_sheet(buildCurrentLessonSheetRows(viewRows));
            currentSheet['!cols'] = [
                { wch: 5 }, { wch: 24 }, { wch: 16 }, { wch: 18 },
                { wch: 16 }, { wch: 12 }, { wch: 12 }, { wch: 34 }, { wch: 22 }, { wch: 22 }, { wch: 18 }
            ];
            XLSX.utils.book_append_sheet(workbook, currentSheet, 'Bai hien tai');

            const scopedLessons = lessonsForClassFilter();
            if (scopedLessons.length > 1) {
                const matrixData = await fetchProgressMatrix();
                if ((matrixData.rows || []).length && (matrixData.lessons || []).length) {
                    const matrixSheet = XLSX.utils.aoa_to_sheet(buildMatrixSheetRows(matrixData));
                    const widths = [{ wch: 5 }, { wch: 24 }, { wch: 16 }, { wch: 18 }];
                    (matrixData.lessons || []).forEach(() => {
                        widths.push({ wch: 10 }, { wch: 16 });
                    });
                    matrixSheet['!cols'] = widths;
                    XLSX.utils.book_append_sheet(workbook, matrixSheet, 'Tong hop lop');
                }
            }

            const lesson = currentLessonMeta();
            const stamp = formatExportTimestamp();
            const classPart = fileSlug(selectedClassName || 'TatCaLop');
            const lessonPart = fileSlug(lesson?.title || 'BaiHoc');
            XLSX.writeFile(workbook, `TienDo_${classPart}_${lessonPart}_${stamp}.xlsx`);
        } catch (err) {
            console.error('exportProgressExcel error:', err);
            alert(err.message || 'Không xuất được file Excel.');
        } finally {
            if (exportBtn) {
                exportBtn.disabled = false;
                exportBtn.innerHTML = oldHtml;
            }
        }
    }

    function renderSummary(viewRows) {
        const total = viewRows.length;
        const practiced = viewRows.filter(row => ['needs_practice', 'mastered'].includes(row.status)).length;
        const mastered = viewRows.filter(row => row.status === 'mastered').length;
        const needs = viewRows.filter(row => row.needs_practice).length;
        const submitted = scopedSubmissions().length;
        const teacherClasses = teacherManagedClasses();
        const scope = selectedClassName
            ? `Lớp ${selectedClassName}`
            : (isTeacherUser() && teacherClasses.length ? 'Tất cả lớp phụ trách' : 'Tất cả lớp');
        const cards = [
            [`Học sinh (${scope})`, total, 'text-slate-900'],
            ['Nộp Drive', submitted, 'text-sky-700'],
            ['Đã làm bài', practiced, 'text-indigo-700'],
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

    function applyQuickStatusFilter(value) {
        const select = el('progressStatusFilter');
        if (select) select.value = value;
        const search = el('progressSearch');
        if (search) search.value = '';
        render();
    }

    function renderTodayActions() {
        const container = el('progressTodayActions');
        if (!container) return;

        const scoped = scopeRows();
        const weakRows = scoped.filter(isWeakRow).sort((a, b) => Number(a.score || 0) - Number(b.score || 0));
        const inactiveRows = scoped.filter(isInactiveRow).sort((a, b) => {
            const left = daysSince(a.last_login_at);
            const right = daysSince(b.last_login_at);
            return (right ?? Number.MAX_SAFE_INTEGER) - (left ?? Number.MAX_SAFE_INTEGER);
        });
        const notStartedRows = scoped.filter(row => row.status === 'not_started');
        const lesson = currentLessonMeta();
        const lessonName = lesson?.title || 'bài đang chọn';

        const actions = new Map();
        weakRows.forEach(row => {
            actions.set(row.student_id, { row, tone: 'rose', reason: `Điểm ${row.score || 0}% dưới ngưỡng ${weakThreshold}%` });
        });
        inactiveRows.forEach(row => {
            if (!actions.has(row.student_id)) {
                actions.set(row.student_id, { row, tone: 'amber', reason: inactiveLabel(row) });
            }
        });
        notStartedRows.forEach(row => {
            if (!actions.has(row.student_id)) {
                actions.set(row.student_id, { row, tone: 'slate', reason: `Chưa bắt đầu ${lessonName}` });
            }
        });
        const priorityItems = [...actions.values()].slice(0, 6);

        container.innerHTML = `
            <div class="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                <div>
                    <h4 class="font-bold text-amber-950"><i class="fas fa-list-check mr-2 text-amber-600"></i>Việc cần xử lý hôm nay</h4>
                    <p class="mt-1 text-xs text-amber-900">Ưu tiên theo lớp đang chọn và bài <strong>${escapeHtml(lessonName)}</strong>. Ngưỡng điểm: ${weakThreshold}% · chưa vào học: ${inactiveDays} ngày.</p>
                </div>
                <div class="flex flex-wrap gap-2">
                    <button type="button" data-progress-filter="weak" class="rounded border border-rose-200 bg-white px-3 py-2 text-xs font-bold text-rose-700 hover:bg-rose-50">${weakRows.length} điểm yếu</button>
                    <button type="button" data-progress-filter="inactive" class="rounded border border-amber-200 bg-white px-3 py-2 text-xs font-bold text-amber-800 hover:bg-amber-100">${inactiveRows.length} chưa vào học</button>
                    <button type="button" data-progress-filter="not_started" class="rounded border border-slate-200 bg-white px-3 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50">${notStartedRows.length} chưa bắt đầu</button>
                </div>
            </div>
            <div class="mt-3 grid grid-cols-1 gap-2 md:grid-cols-2 xl:grid-cols-3">
                ${priorityItems.length ? priorityItems.map(item => {
                    const tone = item.tone === 'rose'
                        ? 'border-rose-200 bg-rose-50 text-rose-900'
                        : (item.tone === 'amber' ? 'border-amber-200 bg-amber-50 text-amber-900' : 'border-slate-200 bg-slate-50 text-slate-800');
                    return `<div class="rounded border p-3 ${tone}">
                        <div class="font-bold text-sm">${escapeHtml(item.row.full_name || item.row.username)}</div>
                        <div class="mt-1 text-xs">${escapeHtml(item.row.class_name || 'Chưa xếp lớp')} · ${escapeHtml(item.reason)}</div>
                    </div>`;
                }).join('') : '<div class="rounded border border-teal-200 bg-teal-50 px-3 py-3 text-sm font-semibold text-teal-800">Không có học sinh cần ưu tiên theo các ngưỡng hiện tại.</div>'}
            </div>
        `;
        container.querySelectorAll('[data-progress-filter]').forEach(button => {
            button.addEventListener('click', () => applyQuickStatusFilter(button.dataset.progressFilter || ''));
        });
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

    function renderRow(row, submissionMap) {
        return `
            <tr class="hover:bg-slate-50">
                <td class="px-4 py-3 text-sm">
                    <div class="font-bold text-slate-900">${escapeHtml(row.full_name)}</div>
                    <div class="text-xs text-slate-500">${escapeHtml(row.username)}${selectedClassName ? '' : ` · ${escapeHtml(row.class_name || 'Chưa xếp lớp')}`}</div>
                </td>
                <td class="px-4 py-3 text-sm">${renderProgressCell(row)}</td>
                <td class="px-4 py-3 text-sm">${renderSubmissionCell(row, submissionMap)}</td>
                <td class="px-4 py-3 text-sm text-slate-700 leading-6">${mathText(weakSkillText(row))}</td>
                <td class="px-4 py-3 text-xs text-slate-500">${escapeHtml(row.updated_at || 'Chưa có')}</td>
            </tr>
        `;
    }

    function renderClassGroupHeader(className, groupRows, submissionMap) {
        const needs = groupRows.filter(row => row.needs_practice).length;
        const mastered = groupRows.filter(row => row.status === 'mastered').length;
        const submitted = groupRows.filter(row => submissionMap.has(Number(row.student_id))).length;
        return `
            <tr class="bg-amber-50 border-t border-amber-100">
                <td class="px-4 py-2.5 text-sm font-bold text-amber-900">Lớp ${escapeHtml(className)}</td>
                <td class="px-4 py-2.5 text-sm text-amber-800">${groupRows.length} HS · ${mastered} xong · ${needs} cần luyện</td>
                <td class="px-4 py-2.5 text-sm font-semibold text-sky-700">${submitted} đã nộp Drive</td>
                <td class="px-4 py-2.5 text-xs text-slate-400">—</td>
                <td class="px-4 py-2.5 text-xs text-slate-400">—</td>
            </tr>
        `;
    }

    function render() {
        const body = el('progressTableBody');
        if (!body) return;
        const filtered = sortRowsForView(filteredRows());
        const submissionMap = submissionByStudentId();

        renderTodayActions();
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
                renderClassGroupHeader(className, groupRows, submissionMap) + groupRows.map(row => renderRow(row, submissionMap)).join('')
            )).join('');
        } else {
            body.innerHTML = filtered.map(row => renderRow(row, submissionMap)).join('');
        }
        bindSubmissionPreviewButtons(body);
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
        classSubjects = data.class_subjects && typeof data.class_subjects === 'object' ? data.class_subjects : {};
        if (managedClasses.length) {
            localStorage.setItem('userClassName', managedClasses.join(', '));
        }
        const preferredLessonId = String(data.lesson_id || '');
        if (preferredLessonId && lessonsForClassFilter().some(item => String(item.id) === preferredLessonId)) {
            selectedLessonId = preferredLessonId;
        } else {
            syncLessonSelectionForClass();
        }
        renderClasses();
        renderLessons();
        await loadSubmissions();
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
    window.exportAdminProgress = exportProgressExcel;

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
