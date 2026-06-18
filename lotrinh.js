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

    const state = {
        user: null,
        lessons: [],
        progress: {},
        selectedLessonId: localStorage.getItem(LS_LESSON_KEY) || '',
        activeTab: localStorage.getItem(LS_TAB_KEY) || 'learn',
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

    function richText(value) {
        return escapeHtml(normalizeDisplayText(value));
    }

    function renderParagraphs(items, emptyText) {
        const parts = (Array.isArray(items) ? items : [])
            .map(normalizeDisplayText)
            .filter(Boolean);
        if (!parts.length) {
            return `<div class="rounded border border-slate-200 bg-white p-4 muted-note">${emptyText}</div>`;
        }
        return `
            <article class="lesson-document rounded border border-slate-200 bg-white p-5">
                ${parts.map(part => `<p>${escapeHtml(part)}</p>`).join('')}
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
            /youtu\.be\/([A-Za-z0-9_-]{6,})/,
            /youtube\.com\/watch\?v=([A-Za-z0-9_-]{6,})/,
            /youtube\.com\/embed\/([A-Za-z0-9_-]{6,})/,
            /youtube\.com\/shorts\/([A-Za-z0-9_-]{6,})/
        ];
        for (const pattern of patterns) {
            const match = value.match(pattern);
            if (match) return `https://www.youtube.com/embed/${match[1]}`;
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
            startedAt: ui.startedAt || progress.startedAt || null,
            completedAt: ui.completedAt || progress.completedAt || null,
        };
    }

    function isTeacher() {
        return state.user?.role === 'teacher';
    }

    function applyRoleView() {
        const teacher = isTeacher();
        els.studentLearningMain?.classList.toggle('hidden', teacher);
        els.teacherLessonDesigner?.classList.toggle('hidden', !teacher);
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
        if (isTeacher()) return;

        renderOverallProgress();
        renderLessonList();
        renderHeader(lesson);
        renderTabs();
        renderSkills(lesson);
        renderTasks(lesson);
        renderNextAction(lesson);
        typesetMath();
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
            <div class="flex items-center justify-between">
                <span class="inline-flex items-center gap-2 text-sm font-bold ${status.tone}">
                    <span class="status-dot ${status.color}"></span>${status.text}
                </span>
                <span class="text-sm font-bold text-slate-900">${progress.score || 0}%</span>
            </div>
            <div class="skill-bar"><span style="width:${progress.score || 0}%"></span></div>
        `;
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
        if (state.activeTab === 'practice') renderPractice(lesson);
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
            await syncLessonState(lesson, { ...ui, theoryDone: true, startedAt: ui.startedAt || new Date().toISOString() }, { status: 'in_progress' });
            await reloadLessons();
            setActiveTab('examples');
        };
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
                    </div>
                `).join('') : '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa nhập ví dụ cho bài này.</div>'}
                <button id="markExamplesDone" class="inline-flex items-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800">
                    <i class="fas fa-check"></i>${ui.examplesDone ? 'Đã xem ví dụ' : 'Đánh dấu đã xem ví dụ'}
                </button>
            </div>
        `;
        document.getElementById('markExamplesDone').onclick = async () => {
            await syncLessonState(lesson, { ...ui, examplesDone: true, startedAt: ui.startedAt || new Date().toISOString() }, { status: 'in_progress' });
            await reloadLessons();
            setActiveTab('practice');
        };
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
        const answers = ui.answers || {};

        els.tabContent.innerHTML = `
            <form id="practiceForm" class="space-y-5">
                ${questions.length ? questions.map((question, index) => `
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
                `).join('') : '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa nhập câu hỏi trắc nghiệm cho bài này.</div>'}
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
                const completedAt = new Date().toISOString();
                const status = scoreData.score >= 80 ? 'mastered' : (scoreData.score >= 50 ? 'needs_practice' : 'in_progress');
                await syncLessonState(lesson, {
                    ...ui,
                    practiceDone: true,
                    completedAt,
                    startedAt: ui.startedAt || completedAt,
                    answers: submittedAnswers
                }, {
                    status,
                    score: scoreData.score,
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

    function renderAnswerMark(question, optionIndex, answers) {
        const selected = answers[question.id];
        if (optionIndex === question.answer) return '<i class="fas fa-check text-teal-700"></i>';
        if (selected === optionIndex && selected !== question.answer) return '<i class="fas fa-xmark text-rose-600"></i>';
        return '';
    }

    function calculateScore(lesson, answers) {
        const questions = Array.isArray(lesson.questions) ? lesson.questions : [];
        if (!questions.length) return { score: 0, skillScores: {} };

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
