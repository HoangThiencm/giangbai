(function () {
    const ROUTES = {
        lotrinh: { url: 'lotrinhtoan6.html', label: 'Toán 6' },
        lotrinhtoan4: { url: 'lotrinhtoan4.html', label: 'Toán 4' },
        lotrinhtoan5: { url: 'lotrinhtoan5.html', label: 'Toán 5' },
        lotrinhtoan6: { url: 'lotrinhtoan6.html', label: 'Toán 6' },
        lotrinhtoan7: { url: 'lotrinhtoan7.html', label: 'Toán 7' },
        lotrinhtoan8: { url: 'lotrinhtoan8.html', label: 'Toán 8' },
        lotrinhtoan9: { url: 'lotrinhtoan9.html', label: 'Toán 9' }
    };

    function storageKeyFromSubject(subject) {
        return String(subject || '')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .toLowerCase()
            .replace(/đ/g, 'd')
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-+|-+$/g, '');
    }

    function previewStorageKey(subject) {
        return `lotrinh_teacher_preview_${storageKeyFromSubject(subject)}`;
    }

    function getAllowedLotrinhPages() {
        let allowed = [];
        try {
            allowed = JSON.parse(localStorage.getItem('allowedPages') || '[]');
        } catch {
            allowed = [];
        }
        const pages = [];
        allowed.forEach(page => {
            const key = page === 'lotrinh' ? 'lotrinhtoan6' : page;
            if (ROUTES[key] && !pages.some(item => item.key === key)) {
                pages.push({ key, ...ROUTES[key] });
            }
        });
        return pages;
    }

    function isTeacher() {
        return localStorage.getItem('userRole') === 'teacher';
    }

    function currentFile() {
        return (window.location.pathname.split('/').pop() || '').toLowerCase();
    }

    function teacherTabEnabled(flagKey) {
        return localStorage.getItem(flagKey) !== '0';
    }

    function getAllowedPagesList() {
        try {
            return JSON.parse(localStorage.getItem('allowedPages') || '[]');
        } catch {
            return [];
        }
    }

    function teacherCanViewDesign() {
        return teacherTabEnabled('teacher_design_enabled') && getAllowedLotrinhPages().length > 0;
    }

    function teacherCanViewStats() {
        return teacherTabEnabled('teacher_progress_stats_enabled') && getAllowedPagesList().includes('thongketientrinh');
    }

    function teacherCanViewDocuments() {
        return getAllowedPagesList().includes('quanlyvanban');
    }

    function teacherCanViewAiStats() {
        return teacherTabEnabled('teacher_ai_stats_enabled') && getAllowedPagesList().includes('theodoiai');
    }

    function teacherHasWorkspaceNav() {
        return teacherCanViewDesign()
            || teacherCanViewStats()
            || teacherCanViewDocuments()
            || teacherCanViewAiStats();
    }

    function isVanbanPage() {
        const file = currentFile();
        return file === 'quanlyvanban.html'
            || file === 'quanlyvanban-hanhchinh.html'
            || file === 'quanlyvanban-dang.html';
    }

    function detectMode() {
        const file = currentFile();
        if (file === 'theodoi-ai.html') return 'ai-stats';
        if (file === 'thongketientrinh.html') return 'stats';
        if (file.startsWith('lotrinhtoan')) return 'design';
        return 'hub';
    }

    function navLinkClass(active) {
        return active
            ? 'inline-flex items-center gap-2 rounded-lg bg-teal-700 px-3 py-2 text-sm font-bold text-white shadow-sm'
            : 'inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-bold text-slate-700 hover:bg-slate-50';
    }

    function ensureStyles() {
        if (document.getElementById('teacherLotrinhNavStyles')) return;
        const style = document.createElement('style');
        style.id = 'teacherLotrinhNavStyles';
        style.textContent = `
            .teacher-workspace-nav {
                border-bottom: 1px solid #e2e8f0;
                background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
            }
            .teacher-workspace-nav-inner {
                max-width: 80rem;
                margin: 0 auto;
                padding: 0.75rem 1rem 1rem;
                display: flex;
                flex-direction: column;
                gap: 0.75rem;
            }
            .teacher-workspace-nav-title {
                font-size: 0.72rem;
                font-weight: 800;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: #0f766e;
            }
            .teacher-workspace-nav-actions {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                align-items: center;
            }
            .teacher-workspace-subject-links {
                display: flex;
                flex-wrap: wrap;
                gap: 0.4rem;
            }
            .teacher-workspace-subject-link {
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                border-radius: 999px;
                border: 1px solid #cbd5e1;
                background: #fff;
                padding: 0.35rem 0.75rem;
                font-size: 0.78rem;
                font-weight: 700;
                color: #334155;
                text-decoration: none;
            }
            .teacher-workspace-subject-link.active {
                border-color: #0f766e;
                background: #ecfdf5;
                color: #0f766e;
            }
            .teacher-document-reminder-badge {
                min-width: 1.25rem;
                height: 1.25rem;
                display: inline-grid;
                place-items: center;
                border-radius: 999px;
                background: #e11d48;
                padding: 0 0.35rem;
                font-size: 0.68rem;
                font-weight: 800;
                color: #fff;
            }
        `;
        document.head.appendChild(style);
    }

    function buildNavHtml(options) {
        const mode = options.mode || detectMode();
        const subject = options.subject || window.LOTRINH_SUBJECT || '';
        const pages = getAllowedLotrinhPages();
        const current = currentFile();
        const subjectLinks = pages.map(page => {
            const active = current === page.url.toLowerCase();
            return `<a href="${page.url}" class="teacher-workspace-subject-link${active ? ' active' : ''}"><i class="fas fa-pen-to-square"></i> Soạn ${page.label}</a>`;
        }).join('');

        const previewBtn = mode === 'design' && subject
            ? `<button type="button" id="teacherPreviewStudentBtn" class="${navLinkClass(false)}"><i class="fas fa-eye"></i> Xem thử như học sinh</button>`
            : '';

        const statsActive = mode === 'stats';
        const aiStatsActive = mode === 'ai-stats';
        const documentsActive = mode === 'documents';
        const designActive = mode === 'design' || mode === 'preview';
        const showDesign = teacherCanViewDesign();
        const showStats = teacherCanViewStats();
        const showDocuments = teacherCanViewDocuments();
        const showAiStats = teacherCanViewAiStats();

        const designLink = showDesign
            ? (mode === 'design' || mode === 'preview'
                ? `<span class="${navLinkClass(true)}"><i class="fas fa-pen-ruler"></i> Soạn bài</span>`
                : `<a href="${pages[0]?.url || 'lotrinhtoan6.html'}" class="${navLinkClass(false)}"><i class="fas fa-pen-ruler"></i> Soạn bài</a>`)
            : '';
        const statsLink = showStats
            ? `<a href="thongketientrinh.html" class="${navLinkClass(statsActive)}"><i class="fas fa-chart-line"></i> Thống kê lớp</a>`
            : '';
        const aiStatsLink = showAiStats
            ? `<a href="theodoi-ai.html" class="${navLinkClass(aiStatsActive)}"><i class="fas fa-robot"></i> Theo dõi AI</a>`
            : '';
        const documentsLink = showDocuments
            ? `<a href="quanlyvanban.html" class="${navLinkClass(documentsActive)}"><i class="fas fa-folder-open"></i> Quản lý văn bản <span id="teacherDocumentReminderBadge" class="teacher-document-reminder-badge hidden" title="Văn bản gần hoặc quá hạn báo cáo"></span></a>`
            : '';

        return `
            <div class="teacher-workspace-nav">
                <div class="teacher-workspace-nav-inner">
                    <div>
                        <div class="teacher-workspace-nav-title">Không gian giáo viên · Lộ trình Toán</div>
                        <p class="mt-1 text-sm text-slate-600">Soạn bài, theo dõi tiến độ học sinh và mức sử dụng AI lộ trình.</p>
                    </div>
                    <div class="teacher-workspace-nav-actions">
                        <a href="index.html" class="${navLinkClass(false)}"><i class="fas fa-home"></i> Trang chính</a>
                        ${designLink}
                        ${statsLink}
                        ${documentsLink}
                        ${aiStatsLink}
                        ${previewBtn}
                    </div>
                    ${pages.length > 1 ? `<div class="teacher-workspace-subject-links">${subjectLinks}</div>` : ''}
                </div>
            </div>
        `;
    }

    function bindPreviewButton(subject) {
        const btn = document.getElementById('teacherPreviewStudentBtn');
        if (!btn || !subject) return;
        btn.addEventListener('click', () => {
            localStorage.setItem(previewStorageKey(subject), '1');
            window.location.reload();
        });
    }

    function reminderCount(documents) {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        return (documents || []).filter(document => {
            if (!Number(document.report_required) || document.effective_status === 'completed' || document.effective_status === 'aware' || !document.report_due_at) return false;
            const due = new Date(`${document.report_due_at}T00:00:00`);
            if (Number.isNaN(due.getTime())) return false;
            return Math.round((due - today) / 86400000) <= 7;
        }).length;
    }

    async function updateDocumentReminderBadge() {
        const badge = document.getElementById('teacherDocumentReminderBadge');
        if (!badge) return;
        const cacheKey = 'teacher_vanban_reminder_v1';
        try {
            const cached = sessionStorage.getItem(cacheKey);
            if (cached) {
                const parsed = JSON.parse(cached);
                if (parsed?.expiresAt > Date.now()) {
                    if (parsed.count > 0) {
                        badge.textContent = parsed.count > 99 ? '99+' : String(parsed.count);
                        badge.classList.remove('hidden');
                    }
                    return;
                }
            }
            const response = await fetch('api/vanban.php?action=reminder_count', { credentials: 'include', cache: 'no-store' });
            if (!response.ok) return;
            const data = await response.json();
            const count = Number(data.count || 0);
            sessionStorage.setItem(cacheKey, JSON.stringify({ count, expiresAt: Date.now() + 300000 }));
            if (!count) return;
            badge.textContent = count > 99 ? '99+' : String(count);
            badge.classList.remove('hidden');
        } catch (_) {
            // Không làm gián đoạn trang học nếu dịch vụ văn bản tạm thời không phản hồi.
        }
    }

    function mountTeacherLotrinhNav(options = {}) {
        if (!isTeacher()) return null;
        if (isVanbanPage()) return null;
        if (!teacherHasWorkspaceNav()) return null;

        ensureStyles();
        const html = buildNavHtml(options);
        let host = document.getElementById('teacherWorkspaceNav');
        if (!host) {
            host = document.createElement('div');
            host.id = 'teacherWorkspaceNav';
            const header = document.querySelector('.app-shell > header, body > header, .page-shell > nav');
            if (header) {
                header.insertAdjacentElement('afterend', host);
            } else {
                document.body.prepend(host);
            }
        }
        host.innerHTML = html;
        host.classList.remove('hidden');
        bindPreviewButton(options.subject || window.LOTRINH_SUBJECT || '');
        window.setTimeout(() => { void updateDocumentReminderBadge(); }, 1200);
        return host;
    }

    window.mountTeacherLotrinhNav = mountTeacherLotrinhNav;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => mountTeacherLotrinhNav());
    } else {
        mountTeacherLotrinhNav();
    }
})();
