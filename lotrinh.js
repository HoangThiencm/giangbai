(async function () {
    const els = {
        studentName: document.getElementById('studentNameDisplay'),
        accountRoleLabel: document.getElementById('accountRoleLabel'),
        studentLearningMain: document.getElementById('studentLearningMain'),
        teacherLessonDesigner: document.getElementById('teacherLessonDesigner'),
        routeTitle: document.getElementById('routeTitle'),
        routeSubject: document.getElementById('routeSubject'),
        routeChapter: document.getElementById('routeChapter'),
        resetBtn: document.getElementById('resetBtn'),
        logoutBtn: document.getElementById('logoutBtn'),
        overallProgress: document.getElementById('overallProgress'),
        lessonList: document.getElementById('lessonList'),
        lessonPath: document.getElementById('lessonPath'),
        lessonTitle: document.getElementById('lessonTitle'),
        lessonGoal: document.getElementById('lessonGoal'),
        lessonStatus: document.getElementById('lessonStatus'),
        tabContent: document.getElementById('tabContent'),
        nextActionTitle: document.getElementById('nextActionTitle'),
        nextActionBody: document.getElementById('nextActionBody'),
        skillPanel: document.getElementById('skillPanel'),
        dailyTasks: document.getElementById('dailyTasks'),
        tabs: Array.from(document.querySelectorAll('.tab-btn')),
    };

    const PAGE_SUBJECT = window.LOTRINH_SUBJECT || 'Toán 6';
    const PAGE_TITLE = window.LOTRINH_PAGE_TITLE || `Lộ trình tự học ${PAGE_SUBJECT}`;
    const PAGE_STORAGE_KEY = PAGE_SUBJECT.normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
        .replace(/đ/g, 'd')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '');
    const LS_TAB_KEY = `lotrinh_active_tab_${PAGE_STORAGE_KEY}`;
    const LS_LESSON_KEY = `lotrinh_selected_lesson_${PAGE_STORAGE_KEY}`;
    const LS_TEACHER_PREVIEW_KEY = `lotrinh_teacher_preview_${PAGE_STORAGE_KEY}`;

    const state = {
        user: null,
        lessons: [],
        progress: {},
        selectedLessonId: localStorage.getItem(LS_LESSON_KEY) || '',
        activeTab: localStorage.getItem(LS_TAB_KEY) || 'learn',
        teacherPreviewUi: { answers: {}, essayAnswers: {}, practiceDone: false },
        loading: true,
        error: ''
    };

    function safeJson(value, fallback) {
        try {
            return value ? JSON.parse(value) : fallback;
        } catch {
            return fallback;
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

    function normalizeDisplayText(value) {
        return String(value ?? '')
            .replace(/&quot;/g, '"')
            .replace(/&lt;/g, '<')
            .replace(/&gt;/g, '>')
            .replace(/&amp;/g, '&')
            .replace(/&nbsp;/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
    }

    function preserveMathSegments(value) {
        return String(value ?? '')
            .replace(/\r/g, '')
            .replace(/\$\$(.+?)\$\$/gs, (_, expr) => `\n$${expr.trim()}$\n`)
            .replace(/\$(.+?)\$/g, (_, expr) => ` $${expr.trim()} `)
            .replace(/\n{3,}/g, '\n\n')
            .trim();
    }

    function richText(value) {
        return escapeHtml(preserveMathSegments(value))
            .replace(/\n/g, '<br>')
            .replace(/ {2,}/g, ' ');
    }

    function renderParagraphs(items, emptyText, aiType = 'theory') {
        const parts = (Array.isArray(items) ? items : [])
            .map(preserveMathSegments)
            .filter(Boolean);
        if (!parts.length) {
            return `<div class="rounded border border-slate-200 bg-white p-4 muted-note">${emptyText}</div>`;
        }
        return `
            <article class="lesson-document rounded border border-slate-200 bg-white p-5">
                ${parts.map((part, index) => `
                    <section class="lesson-explain-block">
                        <p>${escapeHtml(part).replace(/\n/g, '<br>')}</p>
                        <button type="button" class="ai-explain-btn" data-ai-type="${aiType}" data-ai-index="${index}" data-ai-text="${escapeHtml(normalizeDisplayText(part))}">
                            <i class="fas fa-wand-magic-sparkles"></i> AI giải thích
                        </button>
                    </section>
                `).join('')}
            </article>
        `;
    }

    function typesetMath() {
        if (window.MathJax && typeof window.MathJax.typesetPromise === 'function') {
            window.MathJax.typesetPromise([document.body]).catch(() => {});
        }
    }

    function youtubeEmbedUrl(url) {
        const value = String(url || '').trim();
        if (!value) return '';
        const patterns = [
            /drive\.google\.com\/file\/d\/([A-Za-z0-9_-]+)/,
            /drive\.google\.com\/open\?id=([A-Za-z0-9_-]+)/,
            /docs\.google\.com\/uc\?id=([A-Za-z0-9_-]+)/,
            /youtu\.be\/([A-Za-z0-9_-]{6,})/,
            /youtube\.com\/watch\?v=([A-Za-z0-9_-]{6,})/,
            /youtube\.com\/embed\/([A-Za-z0-9_-]{6,})/,
            /youtube\.com\/shorts\/([A-Za-z0-9_-]{6,})/
        ];
        for (const pattern of patterns) {
            const match = value.match(pattern);
            if (match) {
                if (pattern.source.includes('drive\\.google\\.com') || pattern.source.includes('docs\\.google\\.com')) {
                    return `https://drive.google.com/file/d/${match[1]}/preview`;
                }
                return `https://www.youtube.com/embed/${match[1]}`;
            }
        }
        return '';
    }

    async function api(url, options = {}) {
        const res = await fetch(url, { cache: 'no-store', ...options });
        const text = await res.text();
        let data = null;
        try { data = text ? JSON.parse(text) : null; } catch { data = { error: text }; }
        if (!res.ok) {
            const message = data && (data.detail || data.error || data.message) ? (data.detail || data.error || data.message) : `HTTP ${res.status}`;
            throw new Error(message);
        }
        return data;
    }

    function currentLesson() {
        return state.lessons.find(item => String(item.id) === String(state.selectedLessonId)) || state.lessons[0] || null;
    }

    function currentLessonProgress(lesson) {
        if (isTeacherPreview()) return { status: 'not_started', score: 0, skillScores: {}, state: state.teacherPreviewUi };
        if (!lesson) return { status: 'not_started', score: 0, skillScores: {}, state: {} };
        return state.progress[lesson.id] || { status: 'not_started', score: 0, skillScores: {}, state: {} };
    }

    function currentUiState(lesson) {
        const progress = currentLessonProgress(lesson);
        const ui = progress.state || {};
        return {
            theoryDone: !!ui.theoryDone,
            examplesDone: !!ui.examplesDone,
            practiceDone: !!ui.practiceDone,
            answers: ui.answers || {},
            essayAnswers: ui.essayAnswers || {},
            fillAnswers: ui.fillAnswers || {},
            dragAnswers: ui.dragAnswers || {},
            startedAt: ui.startedAt || progress.startedAt || null,
            completedAt: ui.completedAt || progress.completedAt || null,
        };
    }

    function isTeacher() {
        return state.user?.role === 'teacher';
    }

    function isTeacherPreview() {
        return isTeacher() && localStorage.getItem(LS_TEACHER_PREVIEW_KEY) === '1';
    }

    function applyRoleView() {
        const teacher = isTeacher();
        const preview = isTeacherPreview();
        els.studentLearningMain?.classList.toggle('hidden', teacher && !preview);
        els.teacherLessonDesigner?.classList.toggle('hidden', !teacher || preview);
        els.resetBtn?.classList.toggle('hidden', preview);
        if (els.accountRoleLabel) {
            els.accountRoleLabel.textContent = teacher ? 'Giáo viên' : 'Học sinh';
        }
        if (els.routeTitle) els.routeTitle.textContent = PAGE_TITLE;
        if (els.routeSubject) els.routeSubject.textContent = PAGE_SUBJECT;
    }

    function render() {
        const lesson = currentLesson();
        if (state.loading) {
            els.studentName.textContent = 'Đang tải...';
            if (els.routeTitle) els.routeTitle.textContent = PAGE_TITLE;
            if (els.routeSubject) els.routeSubject.textContent = PAGE_SUBJECT;
            els.lessonTitle.textContent = 'Đang tải dữ liệu';
            els.lessonGoal.textContent = '';
            els.lessonList.innerHTML = '<div class="text-sm text-slate-500">Đang tải bài học...</div>';
            return;
        }

        if (state.error) {
            els.studentName.textContent = 'Lỗi tải dữ liệu';
            if (els.routeTitle) els.routeTitle.textContent = PAGE_TITLE;
            if (els.routeSubject) els.routeSubject.textContent = PAGE_SUBJECT;
            els.lessonTitle.textContent = 'Không thể mở lộ trình';
            els.lessonGoal.textContent = state.error;
            return;
        }

        els.studentName.textContent = state.user?.full_name || state.user?.username || 'Tài khoản';
        applyRoleView();
        if (isTeacher() && !isTeacherPreview()) return;

        renderTeacherPreviewBanner();
        renderOverallProgress();
        renderLessonList();
        renderHeader(lesson);
        renderTabs();
        renderSkills(lesson);
        renderTasks(lesson);
        renderNextAction(lesson);
        bindPracticeInteractions(lesson);
        typesetMath();
    }

    function renderTeacherPreviewBanner() {
        if (!els.studentLearningMain) return;
        const existing = document.getElementById('teacherPreviewBanner');
        if (!isTeacherPreview()) {
            existing?.remove();
            return;
        }
        if (existing) return;
        const banner = document.createElement('section');
        banner.id = 'teacherPreviewBanner';
        banner.className = 'panel p-4 lg:col-span-2 flex flex-col gap-3 md:flex-row md:items-center md:justify-between';
        banner.innerHTML = `
            <div>
                <p class="text-xs font-bold uppercase tracking-widest text-amber-600">Giáo viên đang xem thử</p>
                <h2 class="text-lg font-bold text-slate-950">Giao diện bên dưới là cách học sinh nhìn thấy lộ trình.</h2>
            </div>
            <button id="backToLessonEditorBtn" type="button" class="inline-flex items-center justify-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800">
                <i class="fas fa-pen-to-square"></i> Quay lại soạn bài
            </button>
        `;
        els.studentLearningMain.prepend(banner);
        document.getElementById('backToLessonEditorBtn').onclick = () => {
            localStorage.removeItem(LS_TEACHER_PREVIEW_KEY);
            window.location.reload();
        };
    }

    function renderOverallProgress() {
        const masteredCount = state.lessons.filter(lesson => currentLessonProgress(lesson).status === 'mastered').length;
        const total = state.lessons.filter(lesson => lesson.is_published).length || state.lessons.length;
        const percent = total ? Math.round((masteredCount / total) * 100) : 0;
        els.overallProgress.innerHTML = `
            <div class="flex items-center justify-between text-sm">
                <span class="font-semibold text-slate-600">Tiến độ chương</span>
                <span class="font-bold text-slate-900">${masteredCount}/${total} bài đã vững</span>
            </div>
            <div class="skill-bar mt-3"><span style="width:${percent}%"></span></div>
        `;
    }

    function statusInfo(status) {
        const map = {
            mastered: { text: 'Đã vững', color: 'bg-teal-600', tone: 'text-teal-700' },
            needs_practice: { text: 'Cần luyện thêm', color: 'bg-amber-500', tone: 'text-amber-700' },
            in_progress: { text: 'Đang học', color: 'bg-sky-500', tone: 'text-sky-700' },
            not_started: { text: 'Chưa bắt đầu', color: 'bg-slate-400', tone: 'text-slate-600' },
        };
        return map[status] || map.not_started;
    }

    function renderLessonList() {
        if (!state.lessons.length) {
            els.lessonList.innerHTML = '<div class="text-sm text-slate-500">Chưa có bài học nào được giáo viên mở.</div>';
            return;
        }

        els.lessonList.innerHTML = state.lessons.map(lesson => {
            const progress = currentLessonProgress(lesson);
            const active = String(lesson.id) === String(state.selectedLessonId) || (!state.selectedLessonId && lesson === state.lessons[0]);
            const status = statusInfo(progress.status);
            return `
                <button class="lesson-item ${active ? 'active' : ''} w-full bg-white p-3 text-left" data-lesson-id="${lesson.id}">
                    <div class="flex items-start justify-between gap-3">
                        <div>
                            <p class="text-sm font-bold text-slate-900">${lesson.title}</p>
                            <p class="mt-1 text-xs text-slate-500">${lesson.subject} · ${lesson.chapter}</p>
                        </div>
                        <span class="status-dot ${status.color} mt-1"></span>
                    </div>
                    <p class="mt-2 text-xs font-semibold ${status.tone}">${status.text}</p>
                </button>
            `;
        }).join('');

        els.lessonList.querySelectorAll('[data-lesson-id]').forEach(button => {
            button.addEventListener('click', async () => {
                state.selectedLessonId = button.getAttribute('data-lesson-id');
                localStorage.setItem(LS_LESSON_KEY, state.selectedLessonId);
                render();
                if (!isTeacher()) await markLessonStarted(currentLesson());
            });
        });
    }

    function renderHeader(lesson) {
        if (!lesson) {
            if (els.routeTitle) els.routeTitle.textContent = PAGE_TITLE;
            if (els.routeSubject) els.routeSubject.textContent = PAGE_SUBJECT;
            if (els.routeChapter) els.routeChapter.textContent = 'Chưa có bài học được mở';
            els.lessonPath.textContent = '';
            els.lessonTitle.textContent = 'Chưa có bài học';
            els.lessonGoal.textContent = '';
            els.lessonStatus.innerHTML = '';
            return;
        }

        const progress = currentLessonProgress(lesson);
        const status = statusInfo(progress.status);
        if (els.routeTitle) els.routeTitle.textContent = PAGE_TITLE;
        if (els.routeSubject) els.routeSubject.textContent = lesson.subject || 'Lộ trình';
        if (els.routeChapter) els.routeChapter.textContent = lesson.chapter || 'Danh sách bài học';
        els.lessonPath.textContent = `${lesson.subject} · ${lesson.chapter}`;
        els.lessonTitle.textContent = lesson.title;
        els.lessonGoal.textContent = lesson.goal || '';
        els.lessonStatus.innerHTML = `
            <div class="flex items-center justify-between gap-3">
                <span class="inline-flex items-center gap-2 text-sm font-bold ${status.tone}">
                    <span class="status-dot ${status.color}"></span>${status.text}
                </span>
                <button type="button" id="markLessonDoneBtn" class="inline-flex items-center gap-2 rounded border border-teal-200 bg-teal-50 px-3 py-1 text-xs font-bold text-teal-700 hover:bg-teal-100">
                    <i class="fas fa-check"></i>Đã học
                </button>
            </div>
            <div class="skill-bar mt-2"><span style="width:${progress.score || 0}%"></span></div>
        `;
        const markBtn = document.getElementById('markLessonDoneBtn');
        if (markBtn) {
            markBtn.onclick = async () => {
                const ui = currentUiState(lesson);
                const completedAt = new Date().toISOString();
                await syncLessonState(lesson, {
                    ...ui,
                    theoryDone: true,
                    examplesDone: true,
                    practiceDone: true,
                    completedAt,
                    startedAt: ui.startedAt || completedAt
                }, {
                    status: 'mastered',
                    score: Math.max(progress.score || 0, 80),
                    skillScores: progress.skillScores || {},
                    completedAt
                });
                await reloadLessons();
                render();
            };
        }
    }

    function setActiveTab(tab) {
        state.activeTab = tab;
        localStorage.setItem(LS_TAB_KEY, tab);
        renderTabs();
    }

    function renderTabs() {
        els.tabs.forEach(button => {
            const active = button.dataset.tab === state.activeTab;
            button.classList.toggle('bg-teal-700', active);
            button.classList.toggle('text-white', active);
            button.classList.toggle('text-slate-700', !active);
            button.onclick = () => setActiveTab(button.dataset.tab);
        });

        const lesson = currentLesson();
        if (!lesson) {
            els.tabContent.innerHTML = '<div class="rounded border border-dashed border-slate-300 bg-slate-50 p-5"><p class="text-sm text-slate-600">Chưa có bài học để hiển thị.</p></div>';
            return;
        }

        if (state.activeTab === 'learn') renderTheory(lesson);
        if (state.activeTab === 'examples') renderExamples(lesson);
        if (state.activeTab === 'videos') renderVideos(lesson);
        if (state.activeTab === 'practice') {
            renderPractice(lesson);
            bindPracticeInteractions(lesson);
        }
        typesetMath();
    }

    function renderTheory(lesson) {
        const ui = currentUiState(lesson);
        const theory = Array.isArray(lesson.theory) ? lesson.theory : [];
        els.tabContent.innerHTML = `
            <div class="space-y-4">
                ${renderParagraphs(theory, 'Giáo viên chưa nhập lý thuyết cho bài này.')}
                <button id="markTheoryDone" class="inline-flex items-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800">
                    <i class="fas fa-check"></i>${ui.theoryDone ? 'Đã hoàn thành lý thuyết' : 'Đánh dấu đã học'}
                </button>
            </div>
        `;
        document.getElementById('markTheoryDone').onclick = async () => {
            if (isTeacherPreview()) {
                state.teacherPreviewUi = { ...state.teacherPreviewUi, theoryDone: true };
                setActiveTab('examples');
                return;
            }
            await syncLessonState(lesson, { ...ui, theoryDone: true, startedAt: ui.startedAt || new Date().toISOString() }, { status: 'in_progress' });
            await reloadLessons();
            setActiveTab('examples');
        };
        bindAiExplainButtons(lesson);
    }

    function renderEssayExercises(lesson) {
        const items = Array.isArray(lesson.essay_exercises) ? lesson.essay_exercises : [];
        if (!items.length) {
            return '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa thêm bài tập tự luận cho bài này.</div>';
        }
        return items.map((item, index) => {
            const key = item.id || `essay_${index + 1}`;
            const saved = currentUiState(lesson).essayAnswers?.[key] || '';
            return `
                <article class="practice-card">
                    <div class="question-head">
                        <p class="text-xs font-bold uppercase tracking-widest text-teal-700">Tự luận ${index + 1}</p>
                        <h3 class="question-text mt-1 text-base font-bold text-slate-950">${escapeHtml(normalizeDisplayText(item.prompt || ''))}</h3>
                    </div>
                    <textarea class="essay-input" data-essay-key="${escapeHtml(key)}" rows="5" placeholder="Nhập đáp án của em...">${escapeHtml(saved)}</textarea>
                    <div class="mt-3 flex flex-wrap gap-2">
                        <button type="button" class="essay-check-btn inline-flex items-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800" data-essay-key="${escapeHtml(key)}">
                            <i class="fas fa-check"></i>Kiểm tra
                        </button>
                        <button type="button" class="essay-ai-btn inline-flex items-center gap-2 rounded border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:bg-slate-50" data-ai-text="${escapeHtml(item.prompt || '')}">
                            <i class="fas fa-wand-magic-sparkles"></i>Hỏi AI
                        </button>
                    </div>
                    <div class="essay-feedback mt-3 hidden rounded border border-slate-200 bg-slate-50 p-3 text-sm leading-7"></div>
                </article>
            `;
        }).join('');
    }

    function renderFillExercises(lesson) {
        const items = Array.isArray(lesson.fill_exercises) ? lesson.fill_exercises : [];
        if (!items.length) {
            return '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa thêm bài điền khuyết cho bài này.</div>';
        }
        const savedAnswers = currentUiState(lesson).fillAnswers || {};
        return items.map((item, index) => `
            <article class="practice-card">
                <div class="question-head">
                    <p class="text-xs font-bold uppercase tracking-widest text-teal-700">Điền khuyết ${index + 1}</p>
                    <h3 class="question-text mt-1 text-base font-bold text-slate-950">${escapeHtml(normalizeDisplayText(item.prompt || ''))}</h3>
                </div>
                <input class="fill-input" type="text" data-fill-key="${escapeHtml(item.id || `fill_${index + 1}`)}" value="${escapeHtml(savedAnswers[item.id || `fill_${index + 1}`] || '')}" placeholder="Nhập đáp án...">
                <div class="mt-3 flex flex-wrap gap-2">
                    <button type="button" class="fill-check-btn inline-flex items-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800" data-fill-key="${escapeHtml(item.id || `fill_${index + 1}`)}">
                        <i class="fas fa-check"></i>Kiểm tra
                    </button>
                    <button type="button" class="fill-ai-btn inline-flex items-center gap-2 rounded border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:bg-slate-50" data-ai-text="${escapeHtml(item.prompt || '')}">
                        <i class="fas fa-wand-magic-sparkles"></i>Hỏi AI
                    </button>
                </div>
                <div class="fill-feedback mt-3 hidden rounded border border-slate-200 bg-slate-50 p-3 text-sm leading-7"></div>
            </article>
        `).join('');
    }

    function renderDragExercises(lesson) {
        const items = Array.isArray(lesson.drag_exercises) ? lesson.drag_exercises : [];
        if (!items.length) {
            return '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa thêm bài kéo thả cho bài này.</div>';
        }
        return items.map((item, index) => {
            const dragItems = Array.isArray(item.items) ? item.items : [];
            const answer = Array.isArray(item.answer) ? item.answer : [];
            const key = item.id || `drag_${index + 1}`;
            const savedOrder = currentUiState(lesson).dragAnswers?.[key] || [];
            const poolItems = dragItems.filter(piece => !savedOrder.includes(piece));
            return `
                <article class="practice-card" data-drag-key="${escapeHtml(key)}" data-drag-answer="${escapeHtml(JSON.stringify(answer))}">
                    <div class="question-head">
                        <p class="text-xs font-bold uppercase tracking-widest text-teal-700">Kéo thả ${index + 1}</p>
                        <h3 class="question-text mt-1 text-base font-bold text-slate-950">${escapeHtml(normalizeDisplayText(item.prompt || ''))}</h3>
                    </div>
                    <div class="drag-pool" data-drag-pool="${escapeHtml(key)}">
                        ${poolItems.map((piece, pieceIndex) => `<button type="button" draggable="true" class="drag-chip" data-piece="${pieceIndex}">${escapeHtml(piece)}</button>`).join('')}
                    </div>
                    <div class="drag-slot-row" data-drop-zone="${escapeHtml(key)}">
                        ${savedOrder.map((piece, pieceIndex) => `<button type="button" draggable="true" class="drag-chip" data-piece="saved-${pieceIndex}">${escapeHtml(piece)}</button>`).join('')}
                    </div>
                    <div class="mt-3 flex flex-wrap gap-2">
                        <button type="button" class="drag-check-btn inline-flex items-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800" data-drag-key="${escapeHtml(key)}">
                            <i class="fas fa-check"></i>Kiểm tra
                        </button>
                        <button type="button" class="drag-ai-btn inline-flex items-center gap-2 rounded border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:bg-slate-50" data-ai-text="${escapeHtml(item.prompt || '')}">
                            <i class="fas fa-wand-magic-sparkles"></i>Hỏi AI
                        </button>
                    </div>
                    <div class="drag-feedback mt-3 hidden rounded border border-slate-200 bg-slate-50 p-3 text-sm leading-7"></div>
                </article>
            `;
        }).join('');
    }

    function renderExamples(lesson) {
        const ui = currentUiState(lesson);
        const examples = Array.isArray(lesson.examples) ? lesson.examples : [];
        els.tabContent.innerHTML = `
            <div class="space-y-4">
                ${examples.length ? examples.map(example => `
                    <div class="rounded border border-slate-200 bg-white p-4">
                        <h3 class="font-bold text-slate-900">${richText(example.title || 'Ví dụ')}</h3>
                        <p class="mt-2 text-base leading-7 text-slate-700">${richText(example.body || '')}</p>
                        <button type="button" class="ai-explain-btn mt-3" data-ai-type="example" data-ai-index="0" data-ai-text="${escapeHtml(`${example.title || 'Ví dụ'}\n${example.body || ''}`)}">
                            <i class="fas fa-wand-magic-sparkles"></i> AI giải thích
                        </button>
                    </div>
                `).join('') : '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa nhập ví dụ cho bài này.</div>'}
                <button id="markExamplesDone" class="inline-flex items-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800">
                    <i class="fas fa-check"></i>${ui.examplesDone ? 'Đã xem ví dụ' : 'Đánh dấu đã xem ví dụ'}
                </button>
            </div>
        `;
        document.getElementById('markExamplesDone').onclick = async () => {
            if (isTeacherPreview()) {
                state.teacherPreviewUi = { ...state.teacherPreviewUi, examplesDone: true };
                setActiveTab('practice');
                return;
            }
            await syncLessonState(lesson, { ...ui, examplesDone: true, startedAt: ui.startedAt || new Date().toISOString() }, { status: 'in_progress' });
            await reloadLessons();
            setActiveTab('practice');
        };
        bindAiExplainButtons(lesson);
    }

    function bindAiExplainButtons(lesson) {
        document.querySelectorAll('.ai-explain-btn').forEach(button => {
            button.onclick = async () => {
                const text = button.dataset.aiText || '';
                const block = button.closest('.lesson-explain-block') || button.parentElement;
                let output = block.querySelector('.ai-explain-output');
                if (!output) {
                    output = document.createElement('div');
                    output.className = 'ai-explain-output mt-3 rounded border border-amber-200 bg-amber-50 p-3 text-sm leading-7 text-slate-800';
                    block.appendChild(output);
                }
                const old = button.innerHTML;
                button.disabled = true;
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> AI đang giải thích...';
                output.textContent = 'Đang gọi AI...';
                try {
                    const data = await api('api/ai_explain.php', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            subject: lesson.subject || PAGE_SUBJECT,
                            lesson_title: lesson.title || PAGE_TITLE,
                            text
                        })
                    });
                    output.innerHTML = escapeHtml(data.answer || '').replace(/\n/g, '<br>');
                } catch (err) {
                    output.textContent = err.message || 'Chưa gọi được AI.';
                } finally {
                    button.disabled = false;
                    button.innerHTML = old;
                }
            };
        });
    }

    function renderVideos(lesson) {
        const videos = Array.isArray(lesson.videos) ? lesson.videos.filter(item => youtubeEmbedUrl(item.url)) : [];
        els.tabContent.innerHTML = `
            <div class="space-y-4">
                ${videos.length ? videos.map(video => {
                    const embedUrl = youtubeEmbedUrl(video.url);
                    return `
                        <div class="rounded border border-slate-200 bg-white p-4">
                            <h3 class="font-bold text-slate-900">${escapeHtml(video.title || 'Bài giảng')}</h3>
                            <div class="mt-3 aspect-video overflow-hidden rounded border border-slate-200 bg-slate-100">
                                <iframe class="h-full w-full" src="${embedUrl}" title="${escapeHtml(video.title || 'Bài giảng')}" allowfullscreen loading="lazy"></iframe>
                            </div>
                        </div>
                    `;
                }).join('') : '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa gắn video YouTube cho bài này.</div>'}
            </div>
        `;
    }

    async function logout() {
        try {
            await fetch('api/logout.php', { method: 'POST', cache: 'no-store' });
        } catch {
            // Still clear local state below.
        }
        localStorage.removeItem('authToken');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('userName');
        localStorage.removeItem('userRole');
        localStorage.removeItem('allowedPages');
        localStorage.removeItem(LS_TAB_KEY);
        localStorage.removeItem(LS_LESSON_KEY);
        window.location.href = 'login.html';
    }

    if (els.logoutBtn) {
        els.logoutBtn.onclick = logout;
    }

    function renderPractice(lesson) {
        const progress = currentLessonProgress(lesson);
        const ui = currentUiState(lesson);
        const questions = Array.isArray(lesson.questions) ? lesson.questions : [];
        const essayExercises = Array.isArray(lesson.essay_exercises) ? lesson.essay_exercises : [];
        const fillExercises = Array.isArray(lesson.fill_exercises) ? lesson.fill_exercises : [];
        const dragExercises = Array.isArray(lesson.drag_exercises) ? lesson.drag_exercises : [];
        const answers = ui.answers || {};

        els.tabContent.innerHTML = `
            <form id="practiceForm" class="space-y-5">
                ${essayExercises.length ? `<section class="space-y-4">${renderEssayExercises(lesson)}</section>` : ''}
                ${fillExercises.length ? `<section class="space-y-4">${renderFillExercises(lesson)}</section>` : ''}
                ${dragExercises.length ? `<section class="space-y-4">${renderDragExercises(lesson)}</section>` : ''}
                ${questions.length ? `<section class="space-y-4">${questions.map((question, index) => `
                    <article class="practice-card">
                        <div class="question-head">
                            <p class="text-xs font-bold uppercase tracking-widest text-teal-700">Câu ${index + 1}</p>
                            <h3 class="question-text mt-1 text-base font-bold text-slate-950">${escapeHtml(normalizeDisplayText(question.prompt))}</h3>
                        </div>
                        <div class="answer-grid">
                            ${(question.options || []).map((option, optionIndex) => {
                                const checked = answers[question.id] === optionIndex ? 'checked' : '';
                                const mark = progress.status !== 'not_started' ? renderAnswerMark(question, optionIndex, answers) : '';
                                const letter = 'ABCD'[optionIndex] || '';
                                return `
                                    <label class="answer-option flex cursor-pointer items-center justify-between gap-3 px-3 py-2.5 text-sm">
                                        <span class="flex min-w-0 items-center gap-3">
                                            <input type="radio" name="${question.id}" value="${optionIndex}" ${checked} class="sr-only">
                                            <span class="answer-letter">${letter}</span>
                                            <span class="min-w-0 flex-1 leading-7 text-slate-800">${escapeHtml(normalizeDisplayText(option))}</span>
                                        </span>
                                        ${mark}
                                    </label>
                                `;
                            }).join('')}
                        </div>
                    </article>
                `).join('')}</section>` : '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa nhập câu hỏi trắc nghiệm cho bài này.</div>'}
                <div class="flex flex-wrap gap-3">
                    <button type="submit" class="inline-flex items-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800">
                        <i class="fas fa-paper-plane"></i>Nộp bài luyện
                    </button>
                    <button id="clearAnswersBtn" type="button" class="inline-flex items-center gap-2 rounded border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:bg-slate-50">
                        <i class="fas fa-eraser"></i>Xóa đáp án nháp
                    </button>
                </div>
            </form>
        `;

        const form = document.getElementById('practiceForm');
        if (form) {
            form.querySelectorAll("input[type='radio']").forEach(input => {
                input.addEventListener('change', async event => {
                    const nextAnswers = { ...answers, [event.target.name]: Number(event.target.value) };
                    await syncLessonState(lesson, {
                        ...ui,
                        answers: nextAnswers,
                        practiceDone: false,
                        startedAt: ui.startedAt || new Date().toISOString()
                    }, {
                        status: 'in_progress',
                        score: progress.score || 0,
                        skillScores: progress.skillScores || {}
                    });
                    await reloadLessons(false);
                    render();
                });
            });

            form.onsubmit = async event => {
                event.preventDefault();
                const submittedAnswers = collectFormAnswers(form, questions);
                const scoreData = calculateScore(lesson, submittedAnswers);
                const essayData = evaluateEssayExercises(lesson);
                const fillData = evaluateFillExercises(lesson);
                const dragData = evaluateDragExercises(lesson);
                const parts = [scoreData.score, essayData.score, fillData.score, dragData.score].filter(score => score !== null);
                const mergedScore = parts.length ? Math.round(parts.reduce((sum, value) => sum + value, 0) / parts.length) : 0;
                const completedAt = new Date().toISOString();
                const status = mergedScore >= 80 ? 'mastered' : (mergedScore >= 50 ? 'needs_practice' : 'in_progress');
                await syncLessonState(lesson, {
                    ...ui,
                    practiceDone: true,
                    completedAt,
                    startedAt: ui.startedAt || completedAt,
                    answers: submittedAnswers,
                    essayAnswers: essayData.answers,
                    fillAnswers: fillData.answers,
                    dragAnswers: dragData.answers
                }, {
                    status,
                    score: mergedScore,
                    skillScores: scoreData.skillScores,
                    completedAt
                });
                await reloadLessons();
                render();
            };
        }

        const clearBtn = document.getElementById('clearAnswersBtn');
        if (clearBtn) {
            clearBtn.onclick = async () => {
                await resetLesson(lesson);
                await reloadLessons();
                render();
            };
        }
    }

    function collectFormAnswers(form, questions) {
        const result = {};
        questions.forEach(question => {
            const checked = Array.from(form.querySelectorAll("input[type='radio']:checked"))
                .find(input => input.name === question.id);
            if (checked) result[question.id] = Number(checked.value);
        });
        return result;
    }

    function normalizeAnswerText(value) {
        return String(value ?? '').trim().toLowerCase().replace(/\s+/g, ' ');
    }

    function evaluateEssayExercises(lesson) {
        const items = Array.isArray(lesson.essay_exercises) ? lesson.essay_exercises : [];
        if (!items.length) return { score: null, answers: {} };
        const answers = {};
        let correct = 0;
        items.forEach(item => {
            const key = item.id || `essay_${items.indexOf(item) + 1}`;
            const field = document.querySelector(`[data-essay-key="${escapeSelector(key)}"]`);
            const value = normalizeAnswerText(field?.value || '');
            answers[key] = field?.value || '';
            const expected = normalizeAnswerText(item.answer || '');
            if (expected && value === expected) correct += 1;
        });
        return { score: Math.round((correct / items.length) * 100), answers };
    }

    function evaluateFillExercises(lesson) {
        const items = Array.isArray(lesson.fill_exercises) ? lesson.fill_exercises : [];
        if (!items.length) return { score: null, answers: {} };
        const answers = {};
        let correct = 0;
        items.forEach(item => {
            const key = item.id || `fill_${items.indexOf(item) + 1}`;
            const field = document.querySelector(`[data-fill-key="${escapeSelector(key)}"]`);
            const value = normalizeAnswerText(field?.value || '');
            answers[key] = field?.value || '';
            const expected = normalizeAnswerText(item.answer || '');
            if (expected && value === expected) correct += 1;
        });
        return { score: Math.round((correct / items.length) * 100), answers };
    }

    function evaluateDragExercises(lesson) {
        const items = Array.isArray(lesson.drag_exercises) ? lesson.drag_exercises : [];
        if (!items.length) return { score: null, answers: {} };
        const answers = {};
        let correct = 0;
        items.forEach(item => {
            const key = item.id || `drag_${items.indexOf(item) + 1}`;
            const zone = document.querySelector(`[data-drop-zone="${escapeSelector(key)}"]`);
            const current = Array.from(zone?.querySelectorAll('.drag-chip') || []).map(node => node.textContent || '');
            answers[key] = current;
            const expected = (item.answer || []).map(normalizeAnswerText);
            const given = current.map(normalizeAnswerText);
            if (expected.length && expected.join('|') === given.join('|')) correct += 1;
        });
        return { score: Math.round((correct / items.length) * 100), answers };
    }

    function escapeSelector(value) {
        return String(value ?? '').replace(/["\\]/g, '\\$&');
    }

    function renderAnswerMark(question, optionIndex, answers) {
        const selected = answers[question.id];
        if (optionIndex === question.answer) return '<i class="fas fa-check text-teal-700"></i>';
        if (selected === optionIndex && selected !== question.answer) return '<i class="fas fa-xmark text-rose-600"></i>';
        return '';
    }

    function calculateScore(lesson, answers) {
        const questions = Array.isArray(lesson.questions) ? lesson.questions : [];
        if (!questions.length) return { score: null, skillScores: {} };

        const correct = questions.filter(question => answers[question.id] === question.answer).length;
        const score = Math.round((correct / questions.length) * 100);

        const totals = {};
        (lesson.skills || []).forEach(skill => {
            totals[skill.id] = { correct: 0, total: 0 };
        });
        questions.forEach(question => {
            if (!totals[question.skill]) totals[question.skill] = { correct: 0, total: 0 };
            totals[question.skill].total += 1;
            if (answers[question.id] === question.answer) totals[question.skill].correct += 1;
        });

        const skillScores = {};
        Object.entries(totals).forEach(([skillId, data]) => {
            skillScores[skillId] = data.total ? Math.round((data.correct / data.total) * 100) : 0;
        });
        return { score, skillScores };
    }

    function renderSkills(lesson) {
        const progress = currentLessonProgress(lesson);
        const scores = progress.skillScores || {};
        const skills = Array.isArray(lesson.skills) ? lesson.skills : [];
        els.skillPanel.innerHTML = skills.length ? skills.map(skill => {
            const score = progress.status === 'not_started' ? 0 : (scores[skill.id] || 0);
            return `
                <div>
                    <div class="flex items-start justify-between gap-3 text-sm">
                        <span class="font-semibold text-slate-700">${skill.name || skill.id}</span>
                        <span class="font-bold">${progress.status === 'not_started' ? '--' : `${score}%`}</span>
                    </div>
                    <div class="skill-bar mt-2"><span style="width:${score}%"></span></div>
                </div>
            `;
        }).join('') : '<p class="muted-note">Giáo viên chưa nhập kỹ năng cho bài này.</p>';
    }

    function renderTasks(lesson) {
        const ui = currentUiState(lesson);
        const tasks = Array.isArray(lesson.tasks) && lesson.tasks.length ? lesson.tasks : ['Đọc lý thuyết ngắn', 'Xem 3 ví dụ mẫu', 'Làm 8 câu luyện tập'];
        const statusList = [
            { done: ui.theoryDone, text: tasks[0] || 'Đọc lý thuyết ngắn' },
            { done: ui.examplesDone, text: tasks[1] || 'Xem ví dụ mẫu' },
            { done: currentLessonProgress(lesson).status === 'mastered' || currentLessonProgress(lesson).status === 'needs_practice', text: tasks[2] || 'Làm bài luyện tập' }
        ];
        els.dailyTasks.innerHTML = statusList.map(task => `
            <div class="flex items-center gap-3 rounded border border-slate-200 bg-white px-3 py-2">
                <span class="grid h-7 w-7 place-items-center rounded ${task.done ? 'bg-teal-700 text-white' : 'bg-slate-100 text-slate-400'}">
                    <i class="fas ${task.done ? 'fa-check' : 'fa-circle'} text-xs"></i>
                </span>
                <span class="text-sm font-semibold text-slate-700">${task.text}</span>
            </div>
        `).join('');
    }

    function renderNextAction(lesson) {
        const progress = currentLessonProgress(lesson);
        const ui = currentUiState(lesson);
        const scoreData = calculateScore(lesson, ui.answers || {});
        const weakSkills = (lesson.skills || []).filter(skill => (scoreData.skillScores[skill.id] || 0) < (skill.target || 80));

        if (!ui.theoryDone) {
            els.nextActionTitle.textContent = 'Bắt đầu bằng lý thuyết ngắn';
            els.nextActionBody.textContent = 'Đọc phần lý thuyết trước để nắm khái niệm và ký hiệu của bài.';
            return;
        }
        if (!ui.examplesDone) {
            els.nextActionTitle.textContent = 'Xem ví dụ mẫu';
            els.nextActionBody.textContent = 'Ví dụ giúp học sinh nhận ra cách áp dụng lý thuyết vào bài cụ thể.';
            return;
        }
        if (progress.status === 'not_started') {
            els.nextActionTitle.textContent = 'Làm bài luyện để hệ thống chấm tự động';
            els.nextActionBody.textContent = 'Sau khi nộp, hệ thống sẽ chấm điểm và gợi ý phần cần luyện thêm.';
            return;
        }
        if (progress.status === 'mastered' && weakSkills.length === 0) {
            els.nextActionTitle.textContent = 'Có thể chuyển sang bài tiếp theo';
            els.nextActionBody.textContent = 'Đã đạt mục tiêu của bài này.';
            return;
        }

        const weakest = weakSkills[0];
        els.nextActionTitle.textContent = weakest ? `Luyện thêm: ${weakest.name}` : 'Luyện thêm một vòng nữa';
        els.nextActionBody.textContent = weakest ? `Kỹ năng này hiện chưa chạm mốc mục tiêu. Có thể luyện thêm 3-5 câu cùng dạng.` : 'Nên làm lại bài luyện để ổn định kết quả.';
    }

    async function syncLessonState(lesson, uiState, extra = {}) {
        const payload = {
            action: 'save_progress',
            lesson_id: lesson.id,
            status: extra.status || currentLessonProgress(lesson).status || 'in_progress',
            score: typeof extra.score === 'number' ? extra.score : currentLessonProgress(lesson).score || 0,
            skill_scores: extra.skillScores || currentLessonProgress(lesson).skillScores || {},
            state: uiState,
            started_at: extra.startedAt || uiState.startedAt || null,
            completed_at: extra.completedAt || uiState.completedAt || null,
        };
        await api('api/lessons.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
    }

    async function markLessonStarted(lesson) {
        if (!lesson) return;
        const progress = currentLessonProgress(lesson);
        if (progress.status !== 'not_started') return;

        const startedAt = new Date().toISOString();
        const nextState = {
            ...(progress.state || {}),
            startedAt: progress.startedAt || startedAt
        };
        state.progress[lesson.id] = {
            ...progress,
            status: 'in_progress',
            state: nextState,
            startedAt: nextState.startedAt
        };
        render();

        try {
            await syncLessonState(lesson, nextState, {
                status: 'in_progress',
                score: progress.score || 0,
                skillScores: progress.skillScores || {},
                startedAt: nextState.startedAt
            });
            await reloadLessons(false);
            render();
        } catch (err) {
            console.warn('Không lưu được trạng thái bắt đầu bài học', err);
        }
    }

    async function resetLesson(lesson) {
        await api('api/lessons.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'reset_progress', lesson_id: lesson.id })
        });
    }

    async function reloadLessons(reselect = true) {
        const data = await api('api/lessons.php?debug=1', { method: 'GET' });
        state.user = data.user;
        state.lessons = (data.lessons || []).filter(lesson => String(lesson.subject || '').trim() === PAGE_SUBJECT);
        state.progress = data.progress || {};
        if (reselect && !state.selectedLessonId && state.lessons[0]) {
            state.selectedLessonId = state.lessons[0].id;
            localStorage.setItem(LS_LESSON_KEY, state.selectedLessonId);
        }
        if (reselect && state.selectedLessonId && !state.lessons.some(lesson => String(lesson.id) === String(state.selectedLessonId))) {
            state.selectedLessonId = state.lessons[0]?.id || '';
            if (state.selectedLessonId) localStorage.setItem(LS_LESSON_KEY, state.selectedLessonId);
        }
    }

    function bindPracticeInteractions(lesson) {
        document.querySelectorAll('[data-ai-text]').forEach(button => {
            if (button.dataset.boundAi === '1') return;
            button.dataset.boundAi = '1';
            button.onclick = async () => {
                const text = button.dataset.aiText || '';
                const block = button.closest('.practice-card, .lesson-explain-block, article, div') || button.parentElement;
                let output = block.querySelector('.ai-output');
                if (!output) {
                    output = document.createElement('div');
                    output.className = 'ai-output mt-3 rounded border border-amber-200 bg-amber-50 p-3 text-sm leading-7 text-slate-800';
                    block.appendChild(output);
                }
                const old = button.innerHTML;
                button.disabled = true;
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> AI đang giải thích...';
                output.textContent = 'Đang gọi AI...';
                try {
                    const data = await api('api/ai_explain.php', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            subject: lesson.subject || PAGE_SUBJECT,
                            lesson_title: lesson.title || PAGE_TITLE,
                            text
                        })
                    });
                    output.innerHTML = escapeHtml(data.answer || '').replace(/\n/g, '<br>');
                } catch (err) {
                    output.textContent = err.message || 'Chưa gọi được AI.';
                } finally {
                    button.disabled = false;
                    button.innerHTML = old;
                }
            };
        });

        document.querySelectorAll('.drag-pool').forEach(pool => {
            if (pool.dataset.boundDrag === '1') return;
            pool.dataset.boundDrag = '1';
            const zoneId = pool.dataset.dragPool;
            const zone = document.querySelector(`[data-drop-zone="${escapeSelector(zoneId)}"]`);
            if (!zone) return;

            const bindChip = chip => {
                chip.addEventListener('dragstart', e => {
                    e.dataTransfer?.setData('text/plain', chip.textContent || '');
                    e.dataTransfer?.setData('source', chip.parentElement === zone ? 'zone' : 'pool');
                    chip.classList.add('opacity-60');
                });
                chip.addEventListener('dragend', () => chip.classList.remove('opacity-60'));
                chip.addEventListener('click', () => {
                    if (chip.parentElement === zone) {
                        pool.appendChild(chip);
                    } else {
                        zone.appendChild(chip);
                    }
                });
            };

            pool.querySelectorAll('.drag-chip').forEach(bindChip);
            zone.querySelectorAll('.drag-chip').forEach(bindChip);

            zone.addEventListener('dragover', e => e.preventDefault());
            zone.addEventListener('drop', e => {
                e.preventDefault();
                const text = e.dataTransfer?.getData('text/plain');
                const chip = Array.from(document.querySelectorAll('.drag-chip')).find(node => node.classList.contains('opacity-60') && node.textContent === text);
                if (!chip) return;
                const target = e.target.closest('.drag-chip');
                if (target && target.parentElement === zone && target !== chip) {
                    zone.insertBefore(chip, target);
                } else {
                    zone.appendChild(chip);
                }
            });
        });

        document.querySelectorAll('.essay-check-btn').forEach(button => {
            if (button.dataset.boundEssay === '1') return;
            button.dataset.boundEssay = '1';
            button.onclick = () => {
                const key = button.dataset.essayKey || '';
                const card = button.closest('.practice-card');
                const input = card?.querySelector(`[data-essay-key="${escapeSelector(key)}"]`);
                const feedback = card?.querySelector('.essay-feedback');
                if (!feedback) return;
                const item = (lesson.essay_exercises || []).find((entry, index) => String(entry.id || `essay_${index + 1}`) === key);
                const ok = normalizeAnswerText(input?.value || '') === normalizeAnswerText(item?.answer || '');
                feedback.classList.remove('hidden');
                feedback.innerHTML = ok
                    ? '<span class="font-bold text-teal-700">Đúng.</span> Em đang đi đúng hướng.'
                    : `<span class="font-bold text-rose-700">Chưa đúng.</span> Gợi ý: ${escapeHtml(item?.hint || 'Hãy thử so sánh với đáp án mẫu.')}`;
            };
        });

        document.querySelectorAll('.fill-check-btn').forEach(button => {
            if (button.dataset.boundFill === '1') return;
            button.dataset.boundFill = '1';
            button.onclick = () => {
                const key = button.dataset.fillKey || '';
                const card = button.closest('.practice-card');
                const input = card?.querySelector(`[data-fill-key="${escapeSelector(key)}"]`);
                const feedback = card?.querySelector('.fill-feedback');
                const item = (lesson.fill_exercises || []).find((entry, index) => String(entry.id || `fill_${index + 1}`) === key);
                const ok = normalizeAnswerText(input?.value || '') === normalizeAnswerText(item?.answer || '');
                if (feedback) {
                    feedback.classList.remove('hidden');
                    feedback.innerHTML = ok
                        ? '<span class="font-bold text-teal-700">Đúng.</span> Em đã điền khớp đáp án.'
                        : `<span class="font-bold text-rose-700">Chưa đúng.</span> Đáp án mẫu: ${escapeHtml(item?.answer || '')}`;
                }
            };
        });

        document.querySelectorAll('.drag-check-btn').forEach(button => {
            if (button.dataset.boundDragCheck === '1') return;
            button.dataset.boundDragCheck = '1';
            button.onclick = () => {
                const key = button.dataset.dragKey || '';
                const card = button.closest('.practice-card');
                const zone = card?.querySelector(`[data-drop-zone="${escapeSelector(key)}"]`);
                const feedback = card?.querySelector('.drag-feedback');
                const item = (lesson.drag_exercises || []).find((entry, index) => String(entry.id || `drag_${index + 1}`) === key);
                const current = Array.from(zone?.querySelectorAll('.drag-chip') || []).map(node => node.textContent || '');
                const ok = current.map(normalizeAnswerText).join('|') === (item?.answer || []).map(normalizeAnswerText).join('|');
                if (feedback) {
                    feedback.classList.remove('hidden');
                    feedback.innerHTML = ok
                        ? '<span class="font-bold text-teal-700">Đúng.</span> Thứ tự đã khớp.'
                        : `<span class="font-bold text-rose-700">Chưa đúng.</span> Thứ tự đúng: ${escapeHtml((item?.answer || []).join(' → '))}`;
                }
            };
        });
    }

    try {
        await reloadLessons(true);
        if (!state.selectedLessonId && state.lessons[0]) {
            state.selectedLessonId = state.lessons[0].id;
            localStorage.setItem(LS_LESSON_KEY, state.selectedLessonId);
        }
        if (state.user?.full_name) {
            els.studentName.textContent = state.user.full_name;
        }
        if (!state.selectedLessonId && state.lessons[0]) state.selectedLessonId = state.lessons[0].id;
        if (!isTeacher()) await markLessonStarted(currentLesson());
    } catch (err) {
        state.error = err.message;
        if (err.message.toLowerCase().includes('chưa đăng nhập') || err.message.toLowerCase().includes('not logged in')) {
            localStorage.removeItem('authToken');
            localStorage.removeItem('userEmail');
            localStorage.removeItem('userName');
            localStorage.removeItem('userRole');
            localStorage.removeItem('allowedPages');
            window.location.href = 'login.html';
            return;
        }
    } finally {
        state.loading = false;
        render();
    }

    els.resetBtn.onclick = async () => {
        const lesson = currentLesson();
        if (!lesson) return;
        if (!confirm('Làm lại toàn bộ tiến độ của bài hiện tại?')) return;
        await resetLesson(lesson);
        await reloadLessons(false);
        render();
    };
})();
