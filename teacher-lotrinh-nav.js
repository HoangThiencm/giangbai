(function () {
    const ROUTES = {
        lotrinh: { url: 'lotrinhtoan6.html', label: 'Toán 6' },
        lotrinhtoan4: { url: 'lotrinhtoan4.html', label: 'Toán 4' },
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

    function teacherCanViewAiStats() {
        if (!teacherTabEnabled('teacher_ai_stats_enabled')) return false;
        try {
            return JSON.parse(localStorage.getItem('allowedPages') || '[]').includes('theodoiai');
        } catch {
            return false;
        }
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
        const designActive = mode === 'design' || mode === 'preview';
        const showDesign = teacherTabEnabled('teacher_design_enabled');
        const showStats = teacherTabEnabled('teacher_progress_stats_enabled');
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

    function mountTeacherLotrinhNav(options = {}) {
        if (!isTeacher()) return null;
        if (!getAllowedLotrinhPages().length) return null;

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
        return host;
    }

    window.mountTeacherLotrinhNav = mountTeacherLotrinhNav;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => mountTeacherLotrinhNav());
    } else {
        mountTeacherLotrinhNav();
    }
})();