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
    const LS_STUDY_MINUTES_KEY = `lotrinh_study_minutes_${PAGE_STORAGE_KEY}`;
    const LS_LESSON_NAV_VIEW_KEY = `lotrinh_lesson_nav_view_${PAGE_STORAGE_KEY}`;
    const LS_MOTIVATION_KEY_PREFIX = `lotrinh_motivation_${PAGE_STORAGE_KEY}`;
    const REVIEW_STALE_DAYS = 7;

    const BADGE_DEFS = [
        { id: 'streak_3', label: '3 ngày học liên tiếp', icon: 'fa-fire', tone: 'text-orange-600 bg-orange-50 border-orange-200' },
        { id: 'mastered_5', label: 'Hoàn thành 5 bài', icon: 'fa-medal', tone: 'text-amber-700 bg-amber-50 border-amber-200' },
        { id: 'perfect_100', label: 'Lần đầu đạt 100%', icon: 'fa-star', tone: 'text-teal-700 bg-teal-50 border-teal-200' }
    ];

    const state = {
        user: null,
        lessons: [],
        progress: {},
        selectedLessonId: localStorage.getItem(LS_LESSON_KEY) || '',
        activeTab: localStorage.getItem(LS_TAB_KEY) || 'learn',
        studyMinutes: Number(localStorage.getItem(LS_STUDY_MINUTES_KEY)) || 30,
        teacherPreviewUi: { answers: {}, essayAnswers: {}, practiceDone: false },
        lessonListUi: {
            chapter: '',
            search: '',
            view: localStorage.getItem(LS_LESSON_NAV_VIEW_KEY) || 'list'
        },
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
            .replace(/[ \t]+/g, ' ')
            .replace(/\n{3,}/g, '\n\n')
            .trim();
    }

    function decodeBasicEntities(value) {
        return String(value ?? '')
            .replace(/&quot;/g, '"')
            .replace(/&lt;/g, '<')
            .replace(/&gt;/g, '>')
            .replace(/&amp;/g, '&')
            .replace(/&nbsp;/g, ' ');
    }

    function normalizeMathContent(value) {
        return decodeBasicEntities(value)
            .replace(/\r\n?/g, '\n')
            .split('\n')
            .map(line => line.replace(/[ \t]+$/g, ''))
            .join('\n')
            .replace(/\n{3,}/g, '\n\n')
            .trim();
    }

    function isMathPart(part) {
        return (
            (part.startsWith('$$') && part.endsWith('$$')) ||
            (part.startsWith('\\[') && part.endsWith('\\]')) ||
            (part.startsWith('\\(') && part.endsWith('\\)')) ||
            (part.startsWith('$') && part.endsWith('$'))
        );
    }

    function mathText(value) {
        const source = normalizeMathContent(value);
        const parts = source.split(/(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\$[^\n$]*?\$|\\\([\s\S]*?\\\))/g);
        return parts.map(part => {
            if (!part) return '';
            if (isMathPart(part)) {
                return escapeHtml(part.replace(/[ \t]*\n[ \t]*/g, ' '));
            }
            return escapeHtml(part).replace(/\n/g, '<br>');
        }).join('');
    }

    function sanitizeLessonImageUrl(url) {
        const value = String(url || '').trim();
        if (!/^https?:\/\//i.test(value)) return '';
        return value.replace(/[\s"'<>]/g, '');
    }

    function applyLessonInlineMarkup(text) {
        return escapeHtml(text)
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>')
            .replace(/\+\+([^+]+)\+\+/g, '<u>$1</u>');
    }

    function formatLessonTextBlock(text) {
        const parts = text.split(/(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\$[^\n$]*?\$|\\\([\s\S]*?\\\))/g);
        return parts.map(part => {
            if (!part) return '';
            if (isMathPart(part)) {
                return escapeHtml(part.replace(/[ \t]*\n[ \t]*/g, ' '));
            }
            return applyLessonInlineMarkup(part).replace(/\n/g, '<br>');
        }).join('');
    }

    function lessonRichText(value) {
        const source = normalizeMathContent(value);
        const lines = source.split('\n');
        const chunks = [];
        let textBuffer = [];

        const flushText = () => {
            if (!textBuffer.length) return;
            chunks.push(formatLessonTextBlock(textBuffer.join('\n')));
            textBuffer = [];
        };

        lines.forEach(line => {
            const img = line.trim().match(/^!\[([^\]]*)\]\((\S+)\)$/);
            if (img) {
                flushText();
                const url = sanitizeLessonImageUrl(img[2]);
                if (!url) return;
                const alt = escapeHtml(img[1]);
                chunks.push(
                    `<figure class="lesson-inline-image"><img src="${escapeHtml(url)}" alt="${alt}" loading="lazy">${img[1] ? `<figcaption>${alt}</figcaption>` : ''}</figure>`
                );
                return;
            }
            textBuffer.push(line);
        });
        flushText();
        return chunks.join('<br>');
    }

    function richText(value) {
        return lessonRichText(value);
    }

    function cleanAiAnswer(value) {
        return String(value ?? '')
            .replace(/\r\n?/g, '\n')
            .replace(/^\s*[-*_]{3,}\s*$/gm, '')
            .replace(/\*\*([^*\n]+)\*\*/g, '$1')
            .replace(/__([^_\n]+)__/g, '$1')
            .replace(/^\s*#{1,6}\s+/gm, '')
            .replace(/^\s*[-*]\s+/gm, '')
            .replace(/\n{3,}/g, '\n\n')
            .trim();
    }

    function renderAiAnswer(value) {
        return mathText(cleanAiAnswer(value));
    }

    function practiceItems(lesson) {
        return [
            ...(Array.isArray(lesson.questions) ? lesson.questions.map(item => ({ type: 'choice', item })) : []),
            ...(Array.isArray(lesson.essay_exercises) ? lesson.essay_exercises.map((item, index) => ({ type: 'essay', item, index })) : []),
            ...(Array.isArray(lesson.fill_exercises) ? lesson.fill_exercises.map((item, index) => ({ type: 'fill', item, index })) : []),
            ...(Array.isArray(lesson.drag_exercises) ? lesson.drag_exercises.map((item, index) => ({ type: 'drag', item, index })) : []),
        ];
    }

    function practiceProgress(lesson, ui = currentUiState(lesson)) {
        const items = practiceItems(lesson);
        if (!items.length) return { answered: 0, total: 0, percent: 0 };
        const answered = items.filter(({ type, item, index }) => {
            if (type === 'choice') return ui.answers?.[item.id] !== undefined && ui.answers?.[item.id] !== null;
            const key = item.id || `${type}_${index + 1}`;
            if (type === 'essay') return String(ui.essayAnswers?.[key] || '').trim() !== '';
            if (type === 'fill') return String(ui.fillAnswers?.[key] || '').trim() !== '';
            if (type === 'drag') return Array.isArray(ui.dragAnswers?.[key]) && ui.dragAnswers[key].length > 0;
            return false;
        }).length;
        return { answered, total: items.length, percent: Math.round((answered / items.length) * 100) };
    }

    function lessonCompletionPercent(lesson, uiOverride = null, statusOverride = null) {
        const progress = currentLessonProgress(lesson);
        const ui = uiOverride || currentUiState(lesson);
        const status = statusOverride || progress.status;
        if (status === 'mastered') return 100;
        const practice = practiceProgress(lesson, ui);
        const theory = ui.theoryDone ? 30 : 0;
        const examples = ui.examplesDone ? 20 : 0;
        const practicePart = ui.practiceDone ? 50 : Math.round(practice.percent * 0.5);
        return Math.max(0, Math.min(100, theory + examples + practicePart));
    }

    function lessonProgressSkillScores(lesson, percent) {
        const scores = {};
        (lesson.skills || []).forEach(skill => {
            scores[skill.id] = percent;
        });
        return scores;
    }

    const AI_MARKER_LINE_RE = /^\s*(\[\[AI\]\]|\[AI\])\s*$/i;
    const AI_MARKER_INLINE_RE = /\s*(\[\[AI\]\]|\[AI\])\s*$/i;

    function parseContentWithAiMarker(text) {
        let ai = false;
        const lines = String(text || '').replace(/\r/g, '').split('\n');
        while (lines.length && AI_MARKER_LINE_RE.test(lines[lines.length - 1])) {
            ai = true;
            lines.pop();
        }
        const cleaned = lines
            .map(line => line.replace(/[ \t]+$/g, '').replace(AI_MARKER_INLINE_RE, () => {
                ai = true;
                return '';
            }))
            .join('\n')
            .trim();
        return { text: cleaned, ai };
    }

    function normalizeTheoryItem(item) {
        let text = '';
        let ai = false;
        if (typeof item === 'string') {
            text = item.trim();
        } else if (item && typeof item === 'object') {
            text = String(item.text ?? item.content ?? '').trim();
            ai = !!item.ai;
        }
        const parsed = parseContentWithAiMarker(text);
        return { text: parsed.text, ai: ai || parsed.ai };
    }

    function normalizeExampleItem(item) {
        const title = String(item?.title ?? '').trim();
        const parsed = parseContentWithAiMarker(String(item?.body ?? ''));
        const hasAiField = item && typeof item === 'object' && Object.prototype.hasOwnProperty.call(item, 'ai');
        return {
            title: title || 'Ví dụ',
            body: parsed.text,
            ai: hasAiField ? !!item.ai : (parsed.ai || true)
        };
    }

    function renderParagraphs(items, emptyText, aiType = 'theory') {
        const parts = (Array.isArray(items) ? items : [])
            .map(item => {
                const block = normalizeTheoryItem(item);
                return { ...block, text: normalizeMathContent(block.text) };
            })
            .filter(part => part.text);
        if (!parts.length) {
            return `<div class="rounded border border-slate-200 bg-white p-4 muted-note">${emptyText}</div>`;
        }
        if (parts.length === 1 && !parts[0].ai) {
            return `
                <article class="lesson-document rounded border border-slate-200 bg-white p-5">
                    <div class="lesson-theory-flow lesson-paragraph">${lessonRichText(parts[0].text)}</div>
                </article>
            `;
        }
        return `
            <article class="lesson-document rounded border border-slate-200 bg-white p-5">
                <div class="lesson-theory-flow">
                    ${parts.map((part, index) => `
                        <div class="lesson-paragraph">${lessonRichText(part.text)}</div>
                        ${part.ai ? `
                        <button type="button" class="ai-explain-btn" data-ai-type="${aiType}" data-ai-index="${index}" data-ai-text="${escapeHtml(normalizeDisplayText(part.text))}">
                            <i class="fas fa-wand-magic-sparkles"></i> AI giải thích
                        </button>
                        ` : ''}
                    `).join('')}
                </div>
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
            const base = data && (data.error || data.message) ? (data.error || data.message) : `HTTP ${res.status}`;
            const detail = data && data.detail ? String(data.detail) : '';
            const message = detail && detail !== base ? `${base} (${detail})` : (detail || base);
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
        renderStudyPlanner();
        renderMotivationPanel();
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

    function getLessonRightAside() {
        return document.querySelector('#studentLearningMain section.grid > aside');
    }

    function ensureStudyPlannerPanel() {
        const rightAside = getLessonRightAside();
        if (!rightAside) return null;

        let panel = document.getElementById('studyPlannerPanel');
        if (!panel) {
            panel = document.createElement('section');
            panel.id = 'studyPlannerPanel';
            panel.className = 'panel p-5 study-planner-panel';
            rightAside.insertBefore(panel, rightAside.firstChild);
        } else if (panel.parentElement !== rightAside) {
            rightAside.insertBefore(panel, rightAside.firstChild);
        }
        return panel;
    }

    function injectLessonListStyles() {
        if (document.getElementById('lessonListStyles')) return;
        const style = document.createElement('style');
        style.id = 'lessonListStyles';
        style.textContent = `
            .lesson-list-scroll {
                max-height: min(68vh, 520px);
                overflow-y: auto;
                padding-right: 4px;
                scroll-behavior: smooth;
            }
            .lesson-list-scroll::-webkit-scrollbar { width: 6px; }
            .lesson-list-scroll::-webkit-scrollbar-thumb {
                background: #cbd5e1;
                border-radius: 999px;
            }
            .lesson-item-compact { padding: 8px 10px; }
            .lesson-item-compact .lesson-item-title {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
            .lesson-chapter-group[open] .lesson-chapter-head {
                position: sticky;
                top: 0;
                z-index: 2;
                background: #f8fafc;
                border-bottom: 1px solid #e2e8f0;
            }
            .chapter-map-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 8px;
            }
            .chapter-map-card {
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                background: #fff;
                padding: 10px;
                text-align: left;
                transition: border-color 0.16s ease, box-shadow 0.16s ease;
            }
            .chapter-map-card:hover {
                border-color: #94a3b8;
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
            }
            .chapter-map-card.is-active {
                border-color: #0f766e;
                box-shadow: 0 6px 16px rgba(15, 118, 110, 0.12);
            }
            .chapter-map-dot {
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 999px;
                margin-right: 6px;
            }
            .chapter-map-legend {
                display: flex;
                flex-wrap: wrap;
                gap: 6px 10px;
                font-size: 0.72rem;
                font-weight: 700;
                color: #64748b;
            }
            .motivation-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                border-radius: 999px;
                border: 1px solid;
                padding: 4px 10px;
                font-size: 0.72rem;
                font-weight: 700;
            }
            .motivation-badge.is-locked { opacity: 0.45; filter: grayscale(0.2); }
            .smart-review-item { border-color: #fcd34d; background: #fffbeb; }
            .smart-review-item:hover { border-color: #f59e0b; background: #fef3c7; }
        `;
        document.head.appendChild(style);
    }

    function todayKey(date = new Date()) {
        return date.toISOString().slice(0, 10);
    }

    function motivationStorageKey() {
        const userId = state.user?.id || state.user?.username || 'guest';
        return `${LS_MOTIVATION_KEY_PREFIX}_${userId}`;
    }

    function loadMotivation() {
        return safeJson(localStorage.getItem(motivationStorageKey()), {
            studyDays: [],
            badges: [],
            firstPerfectLessonId: null
        });
    }

    function saveMotivation(data) {
        localStorage.setItem(motivationStorageKey(), JSON.stringify(data));
    }

    function computeStreak(studyDays) {
        if (!studyDays.length) return 0;
        const set = new Set(studyDays);
        let streak = 0;
        const cursor = new Date();
        while (set.has(todayKey(cursor))) {
            streak += 1;
            cursor.setDate(cursor.getDate() - 1);
        }
        return streak;
    }

    function masteredLessonCount() {
        return state.lessons.filter(lesson => currentLessonProgress(lesson).status === 'mastered').length;
    }

    function evaluateMotivationBadges(data) {
        const streak = computeStreak(data.studyDays);
        const earned = new Set(data.badges || []);
        if (streak >= 3) earned.add('streak_3');
        if (masteredLessonCount() >= 5) earned.add('mastered_5');
        if (data.firstPerfectLessonId) earned.add('perfect_100');
        data.badges = [...earned];
        return data;
    }

    function recordStudyActivity() {
        if (isTeacher() && !isTeacherPreview()) return loadMotivation();
        const data = evaluateMotivationBadges(loadMotivation());
        const today = todayKey();
        if (!data.studyDays.includes(today)) {
            data.studyDays = [...data.studyDays, today].sort();
        }
        evaluateMotivationBadges(data);
        saveMotivation(data);
        return data;
    }

    function markPerfectLesson(lesson) {
        if (!lesson || (isTeacher() && !isTeacherPreview())) return;
        const data = loadMotivation();
        if (!data.firstPerfectLessonId) {
            data.firstPerfectLessonId = String(lesson.id);
            evaluateMotivationBadges(data);
            saveMotivation(data);
        }
    }

    function daysSince(isoDate) {
        if (!isoDate) return Infinity;
        const then = new Date(isoDate).getTime();
        if (Number.isNaN(then)) return Infinity;
        return (Date.now() - then) / (1000 * 60 * 60 * 24);
    }

    function smartReviewReason(lesson) {
        const progress = currentLessonProgress(lesson);
        const score = Number(progress.score || 0);
        const completedAt = progress.completedAt || progress.state?.completedAt || null;

        if (progress.status === 'needs_practice') {
            return { priority: 100, reason: `Điểm ${score}% — cần luyện thêm`, tab: 'practice', minutes: 15, title: 'Ôn lại bài yếu' };
        }
        if (progress.status !== 'not_started' && score > 0 && score < 80) {
            return { priority: 90, reason: `Điểm ${score}% — dưới mục tiêu 80%`, tab: 'practice', minutes: 15, title: 'Củng cố điểm thấp' };
        }
        if (progress.status === 'mastered' && daysSince(completedAt) >= REVIEW_STALE_DAYS) {
            const days = Math.floor(daysSince(completedAt));
            return { priority: 65, reason: `Đã học xong ${days} ngày trước — nên ôn lại`, tab: 'practice', minutes: 10, title: 'Ôn lại kiến thức cũ' };
        }
        return null;
    }

    function buildSmartReviewSuggestions(limit = 4) {
        return state.lessons
            .map(lesson => {
                const hint = smartReviewReason(lesson);
                if (!hint) return null;
                return {
                    lesson,
                    tab: hint.tab,
                    minutes: hint.minutes,
                    title: hint.title,
                    body: hint.reason,
                    priority: hint.priority,
                    isReview: true
                };
            })
            .filter(Boolean)
            .sort((a, b) => b.priority - a.priority)
            .slice(0, limit);
    }

    function chapterAggregateStatus(lessons) {
        const statuses = lessons.map(lesson => currentLessonProgress(lesson).status);
        const percents = lessons.map(lesson => lessonCompletionPercent(lesson));
        if (statuses.length && statuses.every(status => status === 'mastered')) return 'mastered';
        if (statuses.some(status => status === 'needs_practice')) return 'needs_practice';
        if (statuses.some(status => status === 'in_progress') || percents.some(percent => percent > 0)) return 'in_progress';
        return 'not_started';
    }

    function shortChapterLabel(chapter) {
        const text = String(chapter || '').trim();
        const match = text.match(/^(Chương\s*\d+)/i);
        return match ? match[1] : (text.length > 22 ? `${text.slice(0, 22)}…` : text);
    }

    function bindStudyActionButtons(root) {
        if (!root) return;
        root.querySelectorAll('[data-study-lesson-id]').forEach(button => {
            button.onclick = async () => {
                state.selectedLessonId = button.getAttribute('data-study-lesson-id') || state.selectedLessonId;
                state.activeTab = button.getAttribute('data-study-tab') || state.activeTab;
                localStorage.setItem(LS_LESSON_KEY, state.selectedLessonId);
                localStorage.setItem(LS_TAB_KEY, state.activeTab);
                render();
                if (!isTeacher()) await markLessonStarted(currentLesson());
            };
        });
    }

    function ensureMotivationPanel() {
        const rightAside = getLessonRightAside();
        if (!rightAside) return null;
        let panel = document.getElementById('motivationPanel');
        if (!panel) {
            panel = document.createElement('section');
            panel.id = 'motivationPanel';
            panel.className = 'panel p-5';
            const studyPanel = document.getElementById('studyPlannerPanel');
            if (studyPanel?.nextSibling) {
                rightAside.insertBefore(panel, studyPanel.nextSibling);
            } else {
                rightAside.appendChild(panel);
            }
        }
        return panel;
    }

    function renderMotivationPanel() {
        if (isTeacher() && !isTeacherPreview()) {
            document.getElementById('motivationPanel')?.remove();
            return;
        }
        const panel = ensureMotivationPanel();
        if (!panel) return;
        const data = evaluateMotivationBadges(loadMotivation());
        const streak = computeStreak(data.studyDays);
        const earned = new Set(data.badges || []);
        panel.innerHTML = `
            <div class="flex items-center justify-between gap-3">
                <div>
                    <h2 class="text-sm font-bold uppercase tracking-widest text-slate-500">Động lực học</h2>
                    <p class="mt-1 text-xs font-semibold text-slate-500">${streak > 0 ? `${streak} ngày học liên tiếp` : 'Bắt đầu chuỗi học hôm nay'}</p>
                </div>
                <div class="rounded-full border border-orange-200 bg-orange-50 px-3 py-1 text-sm font-bold text-orange-700">
                    <i class="fas fa-fire mr-1"></i>${streak}
                </div>
            </div>
            <div class="mt-4 flex flex-wrap gap-2">
                ${BADGE_DEFS.map(badge => {
                    const active = earned.has(badge.id);
                    return `
                        <span class="motivation-badge border ${badge.tone} ${active ? '' : 'is-locked'}">
                            <i class="fas ${badge.icon}"></i>${escapeHtml(badge.label)}
                        </span>
                    `;
                }).join('')}
            </div>
        `;
    }

    function ensureLessonListShell() {
        if (!els.lessonList || els.lessonList.dataset.shellReady === '1') return;
        injectLessonListStyles();
        const section = els.lessonList.closest('section');
        if (!section) return;

        const toolbar = document.createElement('div');
        toolbar.id = 'lessonListToolbar';
        toolbar.className = 'mb-3 space-y-2';
        section.insertBefore(toolbar, els.lessonList);

        els.lessonList.classList.add('lesson-list-scroll');

        const meta = document.createElement('p');
        meta.id = 'lessonListMeta';
        meta.className = 'mt-2 text-xs font-semibold text-slate-400';
        section.appendChild(meta);

        els.lessonList.dataset.shellReady = '1';
    }

    function lessonStudyTasks(lesson, includeReview = false) {
        if (!lesson) return [];
        const progress = currentLessonProgress(lesson);
        const ui = currentUiState(lesson);
        const tasks = [];

        if (!ui.theoryDone) {
            tasks.push({
                lesson,
                tab: 'learn',
                minutes: 10,
                title: 'Đọc lý thuyết',
                body: 'Nắm khái niệm và công thức cốt lõi.'
            });
        }
        if (ui.theoryDone && !ui.examplesDone) {
            tasks.push({
                lesson,
                tab: 'examples',
                minutes: 8,
                title: 'Xem ví dụ mẫu',
                body: 'Theo dõi cách biến đổi từng bước.'
            });
        }
        if (ui.theoryDone && ui.examplesDone && !ui.practiceDone) {
            const practice = practiceProgress(lesson, ui);
            tasks.push({
                lesson,
                tab: 'practice',
                minutes: practice.total > 8 ? 20 : 15,
                title: practice.answered ? 'Làm tiếp bài luyện' : 'Làm bài luyện tập',
                body: practice.total
                    ? `${practice.answered}/${practice.total} câu đã có đáp án.`
                    : 'Kiểm tra lại kiến thức vừa học.'
            });
        }
        if (progress.status === 'needs_practice') {
            tasks.push({
                lesson,
                tab: 'practice',
                minutes: 15,
                title: 'Luyện lại phần còn yếu',
                body: `Điểm hiện tại ${progress.score || 0}%, mục tiêu là 80%.`
            });
        }
        if (!tasks.length && includeReview) {
            tasks.push({
                lesson,
                tab: 'practice',
                minutes: 8,
                title: 'Ôn nhanh',
                body: 'Đọc lại lời giải hoặc làm lại vài câu khó.'
            });
        }

        return tasks;
    }

    function orderedStudyLessons() {
        const current = currentLesson();
        const seen = new Set();
        const buckets = [
            current ? [current] : [],
            state.lessons.filter(lesson => currentLessonProgress(lesson).status === 'needs_practice'),
            state.lessons.filter(lesson => {
                const status = currentLessonProgress(lesson).status;
                return status === 'in_progress' || lessonCompletionPercent(lesson) > 0;
            }),
            state.lessons.filter(lesson => currentLessonProgress(lesson).status === 'not_started'),
            state.lessons.filter(lesson => currentLessonProgress(lesson).status === 'mastered'),
        ];

        return buckets.flat().filter(lesson => {
            const id = String(lesson.id);
            if (!id || seen.has(id)) return false;
            seen.add(id);
            return true;
        });
    }

    function buildStudyPlan(minutes) {
        const budget = Math.max(10, Number(minutes) || 30);
        const smartReview = buildSmartReviewSuggestions(3);
        const reviewLessonIds = new Set(smartReview.map(task => String(task.lesson.id)));
        const lessons = orderedStudyLessons().filter(lesson => !reviewLessonIds.has(String(lesson.id)));
        const primaryTasks = lessons.flatMap(lesson => lessonStudyTasks(lesson, false));
        const reviewTasks = lessons.flatMap(lesson => lessonStudyTasks(lesson, true))
            .filter(task => !primaryTasks.some(item => String(item.lesson.id) === String(task.lesson.id) && item.tab === task.tab));
        const candidates = [...primaryTasks, ...reviewTasks];
        const plan = [];
        let total = 0;

        smartReview.forEach(task => {
            if (plan.length >= 5) return;
            if (total + task.minutes <= budget || !plan.length) {
                plan.push(task);
                total += task.minutes;
            }
        });

        candidates.some(task => {
            if (plan.length >= 5) return true;
            if (total + task.minutes <= budget || !plan.length) {
                plan.push(task);
                total += task.minutes;
            }
            return total >= budget;
        });

        return { plan, total, budget, smartReview };
    }

    function renderStudyPlanner() {
        const panel = ensureStudyPlannerPanel();
        if (!panel) return;

        if (!state.lessons.length) {
            panel.innerHTML = `
                <div class="flex items-center justify-between">
                    <h2 class="text-sm font-bold uppercase tracking-widest text-slate-500">Kế hoạch tự học</h2>
                    <i class="fas fa-calendar-check text-xl text-teal-700"></i>
                </div>
                <p class="mt-3 text-sm leading-6 text-slate-500">Chưa có bài học để lập kế hoạch.</p>
            `;
            return;
        }

        const { plan, total, budget, smartReview } = buildStudyPlan(state.studyMinutes);
        const reviewBlock = smartReview.length ? `
            <div class="mt-4">
                <div class="mb-2 flex items-center justify-between gap-2">
                    <h3 class="text-xs font-bold uppercase tracking-widest text-amber-700">Ôn tập thông minh</h3>
                    <i class="fas fa-brain text-amber-600"></i>
                </div>
                <div class="space-y-2">
                    ${smartReview.map(task => `
                        <button type="button" class="smart-review-item study-plan-item w-full rounded border p-3 text-left" data-study-lesson-id="${escapeHtml(task.lesson.id)}" data-study-tab="${escapeHtml(task.tab)}">
                            <p class="text-xs font-bold uppercase tracking-widest text-amber-800">${task.minutes} phút · ${escapeHtml(task.title)}</p>
                            <p class="mt-1 truncate text-sm font-bold text-slate-900">${escapeHtml(task.lesson.title)}</p>
                            <p class="mt-1 text-xs leading-5 text-amber-900/80">${escapeHtml(task.body)}</p>
                        </button>
                    `).join('')}
                </div>
            </div>
        ` : `
            <div class="mt-4 rounded border border-slate-200 bg-slate-50 p-3 text-sm leading-6 text-slate-500">
                Chưa có bài cần ôn gấp. Tiếp tục kế hoạch học mới bên dưới.
            </div>
        `;

        panel.innerHTML = `
            <div class="flex items-center justify-between gap-3">
                <div>
                    <h2 class="text-sm font-bold uppercase tracking-widest text-slate-500">Kế hoạch tự học</h2>
                    <p class="mt-1 text-xs font-semibold text-slate-500">${total}/${budget} phút dự kiến</p>
                </div>
                <select id="studyMinutesSelect" class="rounded border border-slate-300 bg-white px-2 py-1 text-sm font-bold text-slate-700">
                    ${[15, 30, 45, 60].map(value => `<option value="${value}" ${Number(state.studyMinutes) === value ? 'selected' : ''}>${value} phút</option>`).join('')}
                </select>
            </div>
            ${reviewBlock}
            <div class="mt-5">
                <h3 class="mb-2 text-xs font-bold uppercase tracking-widest text-teal-700">Lộ trình hôm nay</h3>
                <div class="space-y-2">
                    ${plan.length ? plan.map((task, index) => `
                        <button type="button" class="study-plan-item w-full rounded border border-slate-200 bg-white p-3 text-left hover:border-teal-300 hover:bg-teal-50 ${task.isReview ? 'smart-review-item' : ''}" data-study-lesson-id="${escapeHtml(task.lesson.id)}" data-study-tab="${escapeHtml(task.tab)}">
                            <div class="flex items-start justify-between gap-3">
                                <div class="min-w-0">
                                    <p class="text-xs font-bold uppercase tracking-widest ${task.isReview ? 'text-amber-800' : 'text-teal-700'}">Bước ${index + 1} - ${task.minutes} phút</p>
                                    <p class="mt-1 text-sm font-bold text-slate-900">${escapeHtml(task.title)}</p>
                                    <p class="mt-1 truncate text-xs font-semibold text-slate-500">${escapeHtml(task.lesson.title)}</p>
                                    <p class="mt-1 text-xs leading-5 text-slate-600">${escapeHtml(task.body)}</p>
                                </div>
                                <i class="fas fa-arrow-right mt-1 text-slate-400"></i>
                            </div>
                        </button>
                    `).join('') : '<p class="rounded border border-slate-200 bg-white p-3 text-sm leading-6 text-slate-500">Tất cả bài học đã hoàn thành. Hãy chọn 15 phút ôn nhanh để giữ nhịp.</p>'}
                </div>
            </div>
        `;

        const select = document.getElementById('studyMinutesSelect');
        if (select) {
            select.onchange = () => {
                state.studyMinutes = Number(select.value) || 30;
                localStorage.setItem(LS_STUDY_MINUTES_KEY, String(state.studyMinutes));
                renderStudyPlanner();
            };
        }

        bindStudyActionButtons(panel);
    }

    function renderOverallProgress() {
        const masteredCount = state.lessons.filter(lesson => currentLessonProgress(lesson).status === 'mastered').length;
        const publishedLessons = state.lessons.filter(lesson => lesson.is_published);
        const visibleLessons = publishedLessons.length ? publishedLessons : state.lessons;
        const total = visibleLessons.length || state.lessons.length;
        const percent = total ? Math.round(visibleLessons.reduce((sum, lesson) => sum + lessonCompletionPercent(lesson), 0) / total) : 0;
        const lesson = currentLesson();
        const currentPercent = lesson ? lessonCompletionPercent(lesson) : 0;
        els.overallProgress.innerHTML = `
            <div class="flex items-center justify-between text-sm">
                <span class="font-semibold text-slate-600">Tiến độ chương</span>
                <span class="font-bold text-slate-900">${percent}%</span>
            </div>
            <div class="skill-bar mt-3"><span style="width:${percent}%"></span></div>
            <p class="mt-2 text-xs font-semibold text-slate-500">${masteredCount}/${total} bài đã học xong</p>
            <div class="mt-4 flex items-center justify-between text-sm">
                <span class="font-semibold text-slate-600">Tiến độ bài hiện tại</span>
                <span class="font-bold text-teal-700">${currentPercent}%</span>
            </div>
            <div class="skill-bar mt-2"><span style="width:${currentPercent}%"></span></div>
        `;
    }

    function statusInfo(status) {
        const map = {
            mastered: { text: 'Đã học xong', color: 'bg-teal-600', tone: 'text-teal-700' },
            needs_practice: { text: 'Cần luyện thêm', color: 'bg-amber-500', tone: 'text-amber-700' },
            in_progress: { text: 'Đang học', color: 'bg-sky-500', tone: 'text-sky-700' },
            not_started: { text: 'Chưa bắt đầu', color: 'bg-slate-400', tone: 'text-slate-600' },
        };
        return map[status] || map.not_started;
    }

    function groupLessonsByChapter(lessons) {
        const groups = [];
        const indexByChapter = new Map();
        lessons.forEach(lesson => {
            const chapter = String(lesson.chapter || '').trim() || 'Chưa phân chương';
            if (!indexByChapter.has(chapter)) {
                indexByChapter.set(chapter, groups.length);
                groups.push({ chapter, lessons: [] });
            }
            groups[indexByChapter.get(chapter)].lessons.push(lesson);
        });
        return groups;
    }

    function lessonMatchesSearch(lesson, search) {
        if (!search) return true;
        const haystack = `${lesson.title || ''} ${lesson.chapter || ''}`.toLowerCase();
        return haystack.includes(search.toLowerCase());
    }

    function renderLessonListToolbar(chapterGroups) {
        const toolbar = document.getElementById('lessonListToolbar');
        if (!toolbar) return;
        const chapters = chapterGroups.map(group => group.chapter);
        const { chapter, search, view } = state.lessonListUi;
        const listFilters = view === 'list' ? `
            <input id="lessonListSearch" type="search" value="${escapeHtml(search)}" placeholder="Tìm bài học..." class="w-full rounded border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-teal-500">
            <select id="lessonListChapterFilter" class="w-full rounded border border-slate-300 bg-white px-3 py-2 text-sm font-semibold text-slate-700 outline-none focus:ring-2 focus:ring-teal-500">
                <option value="">Tất cả chương (${state.lessons.length} bài)</option>
                ${chapters.map(name => `<option value="${escapeHtml(name)}" ${chapter === name ? 'selected' : ''}>${escapeHtml(name)}</option>`).join('')}
            </select>
        ` : `
            <div class="chapter-map-legend">
                <span><span class="chapter-map-dot bg-slate-400"></span>Chưa học</span>
                <span><span class="chapter-map-dot bg-sky-500"></span>Đang học</span>
                <span><span class="chapter-map-dot bg-amber-500"></span>Cần luyện</span>
                <span><span class="chapter-map-dot bg-teal-600"></span>Đã xong</span>
            </div>
        `;
        toolbar.innerHTML = `
            <div class="flex rounded-lg border border-slate-200 bg-slate-50 p-1 text-xs font-bold">
                <button type="button" data-lesson-view="list" class="lesson-nav-view-btn flex-1 rounded px-2 py-1.5 ${view === 'list' ? 'bg-white text-teal-800 shadow-sm' : 'text-slate-600'}">Danh sách</button>
                <button type="button" data-lesson-view="map" class="lesson-nav-view-btn flex-1 rounded px-2 py-1.5 ${view === 'map' ? 'bg-white text-teal-800 shadow-sm' : 'text-slate-600'}">Bản đồ chương</button>
            </div>
            ${listFilters}
        `;
        toolbar.querySelectorAll('[data-lesson-view]').forEach(button => {
            button.onclick = () => {
                state.lessonListUi.view = button.getAttribute('data-lesson-view') || 'list';
                localStorage.setItem(LS_LESSON_NAV_VIEW_KEY, state.lessonListUi.view);
                renderLessonList();
            };
        });
        const searchInput = document.getElementById('lessonListSearch');
        const chapterSelect = document.getElementById('lessonListChapterFilter');
        if (searchInput) {
            searchInput.oninput = () => {
                state.lessonListUi.search = searchInput.value.trim();
                renderLessonList();
            };
        }
        if (chapterSelect) {
            chapterSelect.onchange = () => {
                state.lessonListUi.chapter = chapterSelect.value || '';
                renderLessonList();
            };
        }
    }

    function renderChapterMap(chapterGroups) {
        const activeLesson = currentLesson();
        const activeChapter = activeLesson?.chapter || '';
        els.lessonList.innerHTML = `
            <div class="chapter-map-grid">
                ${chapterGroups.map(group => {
                    const status = chapterAggregateStatus(group.lessons);
                    const info = statusInfo(status);
                    const masteredCount = group.lessons.filter(lesson => currentLessonProgress(lesson).status === 'mastered').length;
                    const isActive = group.chapter === activeChapter;
                    return `
                        <button type="button" class="chapter-map-card ${isActive ? 'is-active' : ''}" data-chapter-map="${escapeHtml(group.chapter)}">
                            <div class="flex items-center">
                                <span class="chapter-map-dot ${info.color}"></span>
                                <span class="text-sm font-bold text-slate-900">${escapeHtml(shortChapterLabel(group.chapter))}</span>
                            </div>
                            <p class="mt-2 line-clamp-2 text-xs font-semibold text-slate-600">${escapeHtml(group.chapter)}</p>
                            <p class="mt-2 text-xs font-bold ${info.tone}">${info.text}</p>
                            <p class="mt-1 text-xs text-slate-500">${masteredCount}/${group.lessons.length} bài</p>
                        </button>
                    `;
                }).join('')}
            </div>
        `;
        els.lessonList.querySelectorAll('[data-chapter-map]').forEach(button => {
            button.onclick = () => {
                const chapterName = button.getAttribute('data-chapter-map') || '';
                const group = chapterGroups.find(item => item.chapter === chapterName);
                const targetLesson = group?.lessons.find(lesson => String(lesson.id) === String(state.selectedLessonId)) || group?.lessons[0];
                state.lessonListUi.chapter = chapterName;
                state.lessonListUi.view = 'list';
                localStorage.setItem(LS_LESSON_NAV_VIEW_KEY, 'list');
                if (targetLesson) {
                    state.selectedLessonId = targetLesson.id;
                    localStorage.setItem(LS_LESSON_KEY, state.selectedLessonId);
                }
                render();
            };
        });
    }

    function renderLessonListMeta(visibleCount, chapterCount) {
        const meta = document.getElementById('lessonListMeta');
        if (!meta) return;
        const { chapter, search } = state.lessonListUi;
        if (search || chapter) {
            meta.textContent = `Đang hiển thị ${visibleCount} bài${chapter ? ` · ${chapter}` : ''}${search ? ` · "${search}"` : ''}`;
            return;
        }
        meta.textContent = `${visibleCount} bài · ${chapterCount} chương`;
    }

    function renderLessonList() {
        ensureLessonListShell();

        if (!state.lessons.length) {
            document.getElementById('lessonListToolbar')?.replaceChildren();
            document.getElementById('lessonListMeta')?.replaceChildren();
            els.lessonList.innerHTML = '<div class="text-sm text-slate-500">Chưa có bài học nào được giáo viên mở.</div>';
            return;
        }

        const activeLessonId = String(state.selectedLessonId || state.lessons[0]?.id || '');
        const chapterGroups = groupLessonsByChapter(state.lessons);
        renderLessonListToolbar(chapterGroups);

        if (state.lessonListUi.view === 'map') {
            renderLessonListMeta(state.lessons.length, chapterGroups.length);
            renderChapterMap(chapterGroups);
            return;
        }

        const { chapter, search } = state.lessonListUi;
        const filteredGroups = chapterGroups
            .filter(group => !chapter || group.chapter === chapter)
            .map(group => ({
                ...group,
                lessons: group.lessons.filter(lesson => lessonMatchesSearch(lesson, search))
            }))
            .filter(group => group.lessons.length);

        const visibleCount = filteredGroups.reduce((sum, group) => sum + group.lessons.length, 0);
        renderLessonListMeta(visibleCount, chapterGroups.length);

        if (!visibleCount) {
            els.lessonList.innerHTML = '<div class="rounded border border-dashed border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">Không có bài phù hợp bộ lọc.</div>';
            return;
        }

        els.lessonList.innerHTML = filteredGroups.map(group => {
            const containsActive = group.lessons.some(lesson => String(lesson.id) === activeLessonId);
            const masteredCount = group.lessons.filter(lesson => currentLessonProgress(lesson).status === 'mastered').length;
            return `
                <details class="lesson-chapter-group" ${containsActive ? 'open' : ''}>
                    <summary class="lesson-chapter-head">
                        <span class="lesson-chapter-title">${escapeHtml(group.chapter)}</span>
                        <span class="lesson-chapter-meta">${masteredCount}/${group.lessons.length}</span>
                    </summary>
                    <div class="lesson-chapter-items space-y-1.5">
                        ${group.lessons.map(lesson => {
                            const active = String(lesson.id) === activeLessonId;
                            const status = statusInfo(currentLessonProgress(lesson).status);
                            const percent = lessonCompletionPercent(lesson);
                            return `
                                <button type="button" class="lesson-item lesson-item-compact ${active ? 'active' : ''} w-full bg-white text-left" data-lesson-id="${lesson.id}" title="${escapeHtml(lesson.title)} · ${status.text} · ${percent}%">
                                    <div class="flex items-center gap-2">
                                        <span class="status-dot ${status.color} flex-shrink-0"></span>
                                        <span class="lesson-item-title flex-1 min-w-0 text-sm font-bold text-slate-900">${escapeHtml(lesson.title)}</span>
                                        <span class="flex-shrink-0 text-xs font-bold ${status.tone}">${percent}%</span>
                                    </div>
                                </button>
                            `;
                        }).join('')}
                    </div>
                </details>
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

        const activeItem = els.lessonList.querySelector('.lesson-item.active');
        if (activeItem) {
            window.requestAnimationFrame(() => activeItem.scrollIntoView({ block: 'nearest' }));
        }
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
        const lessonPercent = lessonCompletionPercent(lesson);
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
                    <i class="fas ${progress.status === 'mastered' ? 'fa-rotate-left' : 'fa-check'}"></i>${progress.status === 'mastered' ? 'Học lại' : 'Đã học'}
                </button>
            </div>
            <div class="mt-2 flex items-center justify-between text-xs font-semibold text-slate-600">
                <span>Tiến trình học</span>
                <span>${lessonPercent}%</span>
            </div>
            <div class="skill-bar mt-2"><span style="width:${lessonPercent}%"></span></div>
        `;
        const markBtn = document.getElementById('markLessonDoneBtn');
        if (markBtn) {
            markBtn.onclick = async () => {
                if (progress.status === 'mastered') {
                    await resetLesson(lesson);
                    delete state.progress[lesson.id];
                    await markLessonStarted(lesson);
                    state.activeTab = 'learn';
                    render();
                    return;
                }
                const ui = currentUiState(lesson);
                const completedAt = new Date().toISOString();
                const nextUi = {
                    ...ui,
                    theoryDone: true,
                    examplesDone: true,
                    practiceDone: true,
                    completedAt,
                    startedAt: ui.startedAt || completedAt
                };
                const nextPercent = lessonCompletionPercent(lesson, nextUi, 'mastered');
                await syncLessonState(lesson, {
                    ...nextUi
                }, {
                    status: 'mastered',
                    score: nextPercent,
                    skillScores: lessonProgressSkillScores(lesson, nextPercent),
                    completedAt
                });
                render();
            };
        }
    }

    function setActiveTab(tab) {
        state.activeTab = tab;
        localStorage.setItem(LS_TAB_KEY, tab);
        renderTabs();
        renderNextAction(currentLesson());
        renderTasks(currentLesson());
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
                state.activeTab = 'examples';
                render();
                return;
            }
            try {
                const nextUi = { ...ui, theoryDone: true, startedAt: ui.startedAt || new Date().toISOString() };
                const nextPercent = lessonCompletionPercent(lesson, nextUi, 'in_progress');
                await syncLessonState(lesson, nextUi, {
                    status: 'in_progress',
                    score: nextPercent,
                    skillScores: lessonProgressSkillScores(lesson, nextPercent)
                });
                state.activeTab = 'examples';
                render();
            } catch (err) {
                console.error('markTheoryDone error:', err);
                alert('Không lưu được tiến độ: ' + (err.message || 'Lỗi không xác định'));
            }
        };
        bindAiExplainButtons(lesson);
    }

    function renderEssayExercises(lesson) {
        const items = Array.isArray(lesson.essay_exercises) ? lesson.essay_exercises : [];
        if (!items.length) {
            return '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa thêm bài tập tự luận cho bài này.</div>';
        }
        const practiceDone = !!currentUiState(lesson).practiceDone;
        return items.map((item, index) => {
            const key = item.id || `essay_${index + 1}`;
            const saved = currentUiState(lesson).essayAnswers?.[key] || '';
            const ok = practiceDone && normalizeAnswerText(saved) === normalizeAnswerText(item.answer || '');
            const feedback = practiceDone
                ? (ok
                    ? '<span class="font-bold text-teal-700">Đúng.</span> Em đang đi đúng hướng.'
                    : `<span class="font-bold text-rose-700">Chưa đúng.</span> Gợi ý: ${escapeHtml(item.hint || 'Hãy thử so sánh với đáp án mẫu.')}`)
                : '';
            return `
                <article class="practice-card">
                    <div class="question-head">
                        <p class="text-xs font-bold uppercase tracking-widest text-teal-700">Tự luận ${index + 1}</p>
                        <h3 class="question-text mt-1 text-base font-bold text-slate-950">${mathText(item.prompt || '')}</h3>
                    </div>
                    <textarea class="essay-input" data-essay-key="${escapeHtml(key)}" rows="5" placeholder="Nhập đáp án của em..." ${practiceDone ? 'disabled' : ''}>${escapeHtml(saved)}</textarea>
                    ${practiceDone ? '' : renderMathSymbolToolbar('essay', key)}
                    <div class="mt-3 flex flex-wrap gap-2">
                        <button type="button" class="essay-ai-btn inline-flex items-center gap-2 rounded border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:bg-slate-50" data-ai-text="${escapeHtml(item.prompt || '')}">
                            <i class="fas fa-wand-magic-sparkles"></i>Hỏi AI
                        </button>
                    </div>
                    <div class="essay-feedback mt-3 ${practiceDone ? '' : 'hidden'} rounded border border-slate-200 bg-slate-50 p-3 text-sm leading-7">${feedback}</div>
                </article>
            `;
        }).join('');
    }

    function renderFillExercises(lesson) {
        const items = Array.isArray(lesson.fill_exercises) ? lesson.fill_exercises : [];
        if (!items.length) {
            return '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa thêm bài điền khuyết cho bài này.</div>';
        }
        const ui = currentUiState(lesson);
        const practiceDone = !!ui.practiceDone;
        const savedAnswers = ui.fillAnswers || {};
        return items.map((item, index) => {
            const key = item.id || `fill_${index + 1}`;
            const saved = savedAnswers[key] || '';
            const ok = practiceDone && normalizeAnswerText(saved) === normalizeAnswerText(item.answer || '');
            const feedback = practiceDone
                ? (ok
                    ? '<span class="font-bold text-teal-700">Đúng.</span> Em đã điền khớp đáp án.'
                    : `<span class="font-bold text-rose-700">Chưa đúng.</span> Đáp án mẫu: ${mathText(item.answer || '')}`)
                : '';
            return `
                <article class="practice-card">
                    <div class="question-head">
                        <p class="text-xs font-bold uppercase tracking-widest text-teal-700">Điền khuyết ${index + 1}</p>
                        <h3 class="question-text mt-1 text-base font-bold text-slate-950">${mathText(item.prompt || '')}</h3>
                    </div>
                    <input class="fill-input" type="text" data-fill-key="${escapeHtml(key)}" value="${escapeHtml(saved)}" placeholder="Nhập đáp án hoặc bấm ký hiệu bên dưới..." ${practiceDone ? 'disabled' : ''}>
                    ${practiceDone ? '' : renderMathSymbolToolbar('fill', key)}
                    <div class="mt-3 flex flex-wrap gap-2">
                        <button type="button" class="fill-ai-btn inline-flex items-center gap-2 rounded border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:bg-slate-50" data-ai-text="${escapeHtml(item.prompt || '')}">
                            <i class="fas fa-wand-magic-sparkles"></i>Hỏi AI
                        </button>
                    </div>
                    <div class="fill-feedback mt-3 ${practiceDone ? '' : 'hidden'} rounded border border-slate-200 bg-slate-50 p-3 text-sm leading-7">${feedback}</div>
                </article>
            `;
        }).join('');
    }

    function renderDragExercises(lesson) {
        const items = Array.isArray(lesson.drag_exercises) ? lesson.drag_exercises : [];
        if (!items.length) {
            return '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa thêm bài kéo thả cho bài này.</div>';
        }
        const practiceDone = !!currentUiState(lesson).practiceDone;
        return items.map((item, index) => {
            const dragItems = Array.isArray(item.items) ? item.items : [];
            const answer = Array.isArray(item.answer) ? item.answer : [];
            const key = item.id || `drag_${index + 1}`;
            const savedOrder = currentUiState(lesson).dragAnswers?.[key] || [];
            const poolItems = dragItems.filter(piece => !savedOrder.includes(piece));
            const ok = practiceDone && savedOrder.map(normalizeAnswerText).join('|') === answer.map(normalizeAnswerText).join('|');
            const feedback = practiceDone
                ? (ok
                    ? '<span class="font-bold text-teal-700">Đúng.</span> Thứ tự đã khớp.'
                    : `<span class="font-bold text-rose-700">Chưa đúng.</span> Thứ tự đúng: ${escapeHtml(answer.join(' → '))}`)
                : '';
            const dragDisabled = practiceDone ? 'pointer-events-none opacity-80' : '';
            return `
                <article class="practice-card ${dragDisabled}" data-drag-key="${escapeHtml(key)}" data-drag-answer="${escapeHtml(JSON.stringify(answer))}">
                    <div class="question-head">
                        <p class="text-xs font-bold uppercase tracking-widest text-teal-700">Kéo thả ${index + 1}</p>
                        <h3 class="question-text mt-1 text-base font-bold text-slate-950">${mathText(item.prompt || '')}</h3>
                    </div>
                    <div class="drag-pool" data-drag-pool="${escapeHtml(key)}">
                        ${poolItems.map((piece, pieceIndex) => `<button type="button" draggable="${practiceDone ? 'false' : 'true'}" class="drag-chip" data-piece="${pieceIndex}" ${practiceDone ? 'disabled' : ''}>${escapeHtml(piece)}</button>`).join('')}
                    </div>
                    <div class="drag-slot-row" data-drop-zone="${escapeHtml(key)}">
                        ${savedOrder.map((piece, pieceIndex) => `<button type="button" draggable="${practiceDone ? 'false' : 'true'}" class="drag-chip" data-piece="saved-${pieceIndex}" ${practiceDone ? 'disabled' : ''}>${escapeHtml(piece)}</button>`).join('')}
                    </div>
                    <div class="mt-3 flex flex-wrap gap-2">
                        <button type="button" class="drag-ai-btn inline-flex items-center gap-2 rounded border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:bg-slate-50" data-ai-text="${escapeHtml(item.prompt || '')}">
                            <i class="fas fa-wand-magic-sparkles"></i>Hỏi AI
                        </button>
                    </div>
                    <div class="drag-feedback mt-3 ${practiceDone ? '' : 'hidden'} rounded border border-slate-200 bg-slate-50 p-3 text-sm leading-7">${feedback}</div>
                </article>
            `;
        }).join('');
    }

    function renderExamples(lesson) {
        const ui = currentUiState(lesson);
        const examples = Array.isArray(lesson.examples) ? lesson.examples : [];
        els.tabContent.innerHTML = `
            <div class="space-y-4">
                ${examples.length ? examples.map((example, index) => {
                    const item = normalizeExampleItem(example);
                    return `
                    <div class="lesson-document rounded border border-slate-200 bg-white p-4">
                        <h3 class="font-bold text-slate-900">${richText(item.title)}</h3>
                        <div class="lesson-paragraph mt-2 text-base leading-7 text-slate-700">${richText(item.body)}</div>
                        ${item.ai ? `
                        <button type="button" class="ai-explain-btn mt-3" data-ai-type="example" data-ai-index="${index}" data-ai-text="${escapeHtml(normalizeDisplayText(`${item.title}\n${item.body}`))}">
                            <i class="fas fa-wand-magic-sparkles"></i> AI giải thích
                        </button>
                        ` : ''}
                    </div>
                `;
                }).join('') : '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa nhập ví dụ cho bài này.</div>'}
                <button id="markExamplesDone" class="inline-flex items-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800">
                    <i class="fas fa-check"></i>${ui.examplesDone ? 'Đã xem ví dụ' : 'Đánh dấu đã xem ví dụ'}
                </button>
            </div>
        `;
        document.getElementById('markExamplesDone').onclick = async () => {
            if (isTeacherPreview()) {
                state.teacherPreviewUi = { ...state.teacherPreviewUi, examplesDone: true };
                state.activeTab = 'practice';
                render();
                return;
            }
            try {
                const nextUi = { ...ui, examplesDone: true, startedAt: ui.startedAt || new Date().toISOString() };
                const nextPercent = lessonCompletionPercent(lesson, nextUi, 'in_progress');
                await syncLessonState(lesson, nextUi, {
                    status: 'in_progress',
                    score: nextPercent,
                    skillScores: lessonProgressSkillScores(lesson, nextPercent)
                });
                state.activeTab = 'practice';
                render();
            } catch (err) {
                console.error('markExamplesDone error:', err);
                alert('Không lưu được tiến độ: ' + (err.message || 'Lỗi không xác định'));
            }
        };
        bindAiExplainButtons(lesson);
    }

    function showAiModal(htmlContent, anchorButton = null) {
        document.getElementById('aiExplainBubble')?.remove();

        const bubble = document.createElement('div');
        bubble.id = 'aiExplainBubble';
        bubble.className = 'ai-chat-bubble';
        bubble.innerHTML = `
            <div class="ai-chat-bubble-head">
                <span><i class="fas fa-wand-magic-sparkles"></i> AI giải thích</span>
                <button type="button" class="ai-chat-bubble-close" aria-label="Đóng">&times;</button>
            </div>
            <div class="ai-chat-bubble-body">${htmlContent}</div>
        `;
        bubble.querySelector('.ai-chat-bubble-close').onclick = () => bubble.remove();

        const host = anchorButton?.closest('.lesson-theory-flow, .lesson-explain-block, .practice-card, .lesson-document') || anchorButton?.parentElement;
        if (host) {
            host.appendChild(bubble);
        } else {
            document.body.appendChild(bubble);
        }
        typesetMath();
    }

    function bindAiExplainButtons(lesson) {
        document.querySelectorAll('.ai-explain-btn').forEach(button => {
            button.onclick = async () => {
                const text = button.dataset.aiText || '';
                const old = button.innerHTML;
                button.disabled = true;
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> AI đang giải thích...';
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
                    showAiModal(renderAiAnswer(data.answer || ''), button);
                } catch (err) {
                    showAiModal(`<p style="color:#dc2626">${escapeHtml(err.message || 'Chưa gọi được AI.')}</p>`, button);
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
        const practiceDone = !!ui.practiceDone;
        const questions = Array.isArray(lesson.questions) ? lesson.questions : [];
        const essayExercises = Array.isArray(lesson.essay_exercises) ? lesson.essay_exercises : [];
        const fillExercises = Array.isArray(lesson.fill_exercises) ? lesson.fill_exercises : [];
        const dragExercises = Array.isArray(lesson.drag_exercises) ? lesson.drag_exercises : [];
        const answers = ui.answers || {};
        const practiceScore = typeof progress.score === 'number' ? progress.score : null;

        els.tabContent.innerHTML = `
            <form id="practiceForm" class="space-y-5">
                ${practiceDone ? `
                    <div class="rounded border border-teal-200 bg-teal-50 p-4 text-sm leading-7 text-teal-900">
                        <p class="font-bold">Đã nộp bài luyện tập.</p>
                        <p class="mt-1">${practiceScore !== null ? `Điểm luyện tập: <strong>${practiceScore}%</strong>. ` : ''}Các đáp án đúng/sai được hiển thị bên dưới. Bấm <strong>Làm lại bài luyện</strong> nếu muốn làm vòng mới.</p>
                    </div>
                ` : ''}
                ${essayExercises.length ? `<section class="space-y-4">${renderEssayExercises(lesson)}</section>` : ''}
                ${fillExercises.length ? `<section class="space-y-4">${renderFillExercises(lesson)}</section>` : ''}
                ${dragExercises.length ? `<section class="space-y-4">${renderDragExercises(lesson)}</section>` : ''}
                ${questions.length ? `<section class="space-y-4">${questions.map((question, index) => `
                    <article class="practice-card">
                        <div class="question-head">
                            <p class="text-xs font-bold uppercase tracking-widest text-teal-700">Câu ${index + 1}</p>
                            <h3 class="question-text mt-1 text-base font-bold text-slate-950">${mathText(question.prompt)}</h3>
                        </div>
                        <div class="answer-grid">
                            ${(question.options || []).map((option, optionIndex) => {
                                const checked = normalizeOptionIndex(answers[question.id]) === normalizeOptionIndex(optionIndex) ? 'checked' : '';
                                const mark = renderAnswerMark(question, optionIndex, answers, practiceDone);
                                const letter = 'ABCD'[optionIndex] || '';
                                const disabled = practiceDone ? 'disabled' : '';
                                return `
                                    <label class="answer-option flex items-center justify-between gap-3 px-3 py-2.5 text-sm ${practiceDone ? 'cursor-default' : 'cursor-pointer'}">
                                        <span class="flex min-w-0 items-center gap-3">
                                            <input type="radio" name="${question.id}" value="${optionIndex}" ${checked} ${disabled} class="sr-only">
                                            <span class="answer-letter">${letter}</span>
                                            <span class="min-w-0 flex-1 leading-7 text-slate-800">${mathText(option)}</span>
                                        </span>
                                        ${mark}
                                    </label>
                                `;
                            }).join('')}
                        </div>
                    </article>
                `).join('')}</section>` : '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa nhập câu hỏi trắc nghiệm cho bài này.</div>'}
                <div class="flex flex-wrap gap-3">
                    ${practiceDone ? '' : `
                        <button type="submit" class="inline-flex items-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800">
                            <i class="fas fa-paper-plane"></i>Nộp bài luyện
                        </button>
                    `}
                    ${practiceDone ? `
                        <button id="clearAnswersBtn" type="button" class="inline-flex items-center gap-2 rounded border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:bg-slate-50">
                            <i class="fas fa-rotate-left"></i>Làm lại bài luyện
                        </button>
                    ` : ''}
                </div>
            </form>
        `;

        const form = document.getElementById('practiceForm');
        if (form && !practiceDone) {
            form.querySelectorAll("input[type='radio']").forEach(input => {
                input.addEventListener('change', async event => {
                    const nextAnswers = { ...answers, [event.target.name]: Number(event.target.value) };
                    try {
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
                        render();
                    } catch (err) {
                        console.error('save answer error:', err);
                        alert('Không lưu được câu trả lời: ' + (err.message || 'Lỗi không xác định'));
                    }
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
                try {
                    const nextUi = {
                        ...ui,
                        practiceDone: true,
                        completedAt,
                        startedAt: ui.startedAt || completedAt,
                        answers: submittedAnswers,
                        essayAnswers: essayData.answers,
                        fillAnswers: fillData.answers,
                        dragAnswers: dragData.answers
                    };
                    await syncLessonState(lesson, nextUi, {
                        status,
                        score: mergedScore,
                        skillScores: scoreData.skillScores,
                        completedAt
                    });
                    render();
                } catch (err) {
                    console.error('submit practice error:', err);
                    alert('Không nộp được bài luyện tập: ' + (err.message || 'Lỗi không xác định'));
                }
            };
        }

        const clearBtn = document.getElementById('clearAnswersBtn');
        if (clearBtn) {
            clearBtn.onclick = async () => {
                const baseUi = currentUiState(lesson);
                const nextState = {
                    ...baseUi,
                    answers: {},
                    essayAnswers: {},
                    fillAnswers: {},
                    dragAnswers: {},
                    practiceDone: false,
                    completedAt: null,
                    startedAt: baseUi.startedAt || new Date().toISOString()
                };
                const nextPercent = lessonCompletionPercent(lesson, nextState, 'in_progress');
                try {
                    await syncLessonState(lesson, nextState, {
                        status: 'in_progress',
                        score: nextPercent,
                        skillScores: lessonProgressSkillScores(lesson, nextPercent),
                        startedAt: nextState.startedAt
                    });
                    render();
                } catch (err) {
                    console.error('clear practice error:', err);
                    alert('Không xóa được đáp án nháp: ' + (err.message || 'Lỗi không xác định'));
                }
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

    const MATH_SYMBOL_GROUPS = [
        {
            title: 'Tập hợp',
            symbols: [
                { label: '∈', insert: '\\in', title: 'Thuộc' },
                { label: '∉', insert: '\\notin', title: 'Không thuộc' },
                { label: '⊂', insert: '\\subset', title: 'Tập con' },
                { label: '⊆', insert: '\\subseteq', title: 'Tập con hoặc bằng' },
                { label: '∪', insert: '\\cup', title: 'Hợp' },
                { label: '∩', insert: '\\cap', title: 'Giao' },
                { label: '∅', insert: '\\emptyset', title: 'Tập rỗng' },
            ]
        },
        {
            title: 'Phép tính',
            symbols: [
                { label: '+', insert: '+', title: 'Cộng' },
                { label: '−', insert: '-', title: 'Trừ' },
                { label: '×', insert: '\\times', title: 'Nhân' },
                { label: '÷', insert: '\\div', title: 'Chia' },
                { label: '=', insert: '=', title: 'Bằng' },
                { label: '≠', insert: '\\neq', title: 'Khác' },
                { label: '<', insert: '<', title: 'Nhỏ hơn' },
                { label: '>', insert: '>', title: 'Lớn hơn' },
                { label: '≤', insert: '\\leq', title: 'Nhỏ hơn hoặc bằng' },
                { label: '≥', insert: '\\geq', title: 'Lớn hơn hoặc bằng' },
            ]
        },
        {
            title: 'Công thức',
            symbols: [
                { label: '√', insert: '\\sqrt{}', title: 'Căn bậc hai' },
                { label: 'x²', insert: '^2', title: 'Bình phương' },
                { label: 'x³', insert: '^3', title: 'Lập phương' },
                { label: 'a/b', insert: '\\frac{}{}', title: 'Phân số' },
                { label: '|x|', insert: '\\left| \\right|', title: 'Giá trị tuyệt đối' },
                { label: 'π', insert: '\\pi', title: 'Pi' },
                { label: '∞', insert: '\\infty', title: 'Vô cực' },
            ]
        }
    ];

    const ANSWER_ALIASES = {
        'thuoc': '\\in',
        'thuộc': '\\in',
        'khong thuoc': '\\notin',
        'không thuộc': '\\notin',
        'tap rong': '\\emptyset',
        'tập rỗng': '\\emptyset',
        'khac': '\\neq',
        'khác': '\\neq',
        'nho hon hoac bang': '\\leq',
        'nhỏ hơn hoặc bằng': '\\leq',
        'lon hon hoac bang': '\\geq',
        'lớn hơn hoặc bằng': '\\geq',
    };

    function normalizeAnswerText(value) {
        let text = String(value ?? '').trim();
        text = text
            .replace(/∈/g, '\\in')
            .replace(/∉/g, '\\notin')
            .replace(/⊂/g, '\\subset')
            .replace(/⊆/g, '\\subseteq')
            .replace(/∪/g, '\\cup')
            .replace(/∩/g, '\\cap')
            .replace(/∅/g, '\\emptyset')
            .replace(/×/g, '\\times')
            .replace(/÷/g, '\\div')
            .replace(/≤/g, '\\leq')
            .replace(/≥/g, '\\geq')
            .replace(/≠/g, '\\neq')
            .replace(/π/g, '\\pi')
            .replace(/∞/g, '\\infty')
            .replace(/√/g, '\\sqrt');
        text = text.toLowerCase().replace(/\s+/g, ' ');
        if (ANSWER_ALIASES[text]) text = ANSWER_ALIASES[text];
        return text.replace(/\s+/g, '');
    }

    function renderMathSymbolToolbar(inputKind, inputKey) {
        return `
            <div class="math-symbol-toolbar" data-input-kind="${escapeHtml(inputKind)}" data-input-key="${escapeHtml(inputKey)}">
                <p class="math-symbol-toolbar-title">Chèn ký hiệu toán (bấm để thêm vào ô đáp án):</p>
                ${MATH_SYMBOL_GROUPS.map(group => `
                    <div class="math-symbol-group">
                        <span class="math-symbol-group-label">${escapeHtml(group.title)}</span>
                        <div class="math-symbol-row">
                            ${group.symbols.map(symbol => `
                                <button type="button" class="math-symbol-btn" data-insert="${escapeHtml(symbol.insert)}" title="${escapeHtml(symbol.title)}">${escapeHtml(symbol.label)}</button>
                            `).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    function insertIntoInput(input, text) {
        if (!input || input.disabled) return;
        const start = typeof input.selectionStart === 'number' ? input.selectionStart : input.value.length;
        const end = typeof input.selectionEnd === 'number' ? input.selectionEnd : input.value.length;
        input.value = `${input.value.slice(0, start)}${text}${input.value.slice(end)}`;
        const pos = start + text.length;
        input.setSelectionRange(pos, pos);
        input.focus();
    }

    function bindMathSymbolToolbars(root = document) {
        root.querySelectorAll('.math-symbol-toolbar').forEach(toolbar => {
            if (toolbar.dataset.boundMathToolbar === '1') return;
            toolbar.dataset.boundMathToolbar = '1';
            const kind = toolbar.dataset.inputKind || '';
            const key = toolbar.dataset.inputKey || '';
            const attr = kind === 'essay' ? 'data-essay-key' : 'data-fill-key';
            const input = key ? root.querySelector(`[${attr}="${escapeSelector(key)}"]`) : null;
            if (!input) return;
            toolbar.querySelectorAll('.math-symbol-btn').forEach(button => {
                button.onclick = () => insertIntoInput(input, button.dataset.insert || '');
            });
        });
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

    function normalizeOptionIndex(value) {
        const index = Number(value);
        return Number.isFinite(index) ? index : -1;
    }

    function renderAnswerMark(question, optionIndexValue, answers, practiceDone = false) {
        if (!practiceDone) return '';
        const selected = answers[question.id];
        if (selected === undefined || selected === null) return '';
        const selectedIndex = normalizeOptionIndex(selected);
        const correctIndex = normalizeOptionIndex(question.answer);
        const currentIndex = normalizeOptionIndex(optionIndexValue);
        if (currentIndex === correctIndex) return '<i class="fas fa-check text-teal-700"></i>';
        if (selectedIndex === currentIndex && selectedIndex !== correctIndex) return '<i class="fas fa-xmark text-rose-600"></i>';
        return '';
    }

    function calculateScore(lesson, answers) {
        const questions = Array.isArray(lesson.questions) ? lesson.questions : [];
        if (!questions.length) return { score: null, skillScores: {} };

        const correct = questions.filter(question => normalizeOptionIndex(answers[question.id]) === normalizeOptionIndex(question.answer)).length;
        const score = Math.round((correct / questions.length) * 100);

        const totals = {};
        (lesson.skills || []).forEach(skill => {
            totals[skill.id] = { correct: 0, total: 0 };
        });
        questions.forEach(question => {
            if (!totals[question.skill]) totals[question.skill] = { correct: 0, total: 0 };
            totals[question.skill].total += 1;
            if (normalizeOptionIndex(answers[question.id]) === normalizeOptionIndex(question.answer)) totals[question.skill].correct += 1;
        });

        const skillScores = {};
        Object.entries(totals).forEach(([skillId, data]) => {
            skillScores[skillId] = data.total ? Math.round((data.correct / data.total) * 100) : 0;
        });
        return { score, skillScores };
    }

    function renderSkills(lesson) {
        const progress = currentLessonProgress(lesson);
        const ui = currentUiState(lesson);
        const liveScoreData = calculateScore(lesson, ui.answers || {});
        const scores = Object.keys(progress.skillScores || {}).length ? progress.skillScores : liveScoreData.skillScores;
        const completionPercent = lessonCompletionPercent(lesson);
        const skills = Array.isArray(lesson.skills) ? lesson.skills : [];
        els.skillPanel.innerHTML = skills.length ? skills.map(skill => {
            const score = Math.max(scores[skill.id] || 0, completionPercent);
            return `
                <div>
                    <div class="flex items-start justify-between gap-3 text-sm">
                        <span class="font-semibold text-slate-700">${skill.name || skill.id}</span>
                        <span class="font-bold">${score}%</span>
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
            { done: ui.practiceDone, text: tasks[2] || 'Làm bài luyện tập' }
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

    function nextLessonAfter(lesson) {
        if (!lesson) return null;
        const index = state.lessons.findIndex(item => String(item.id) === String(lesson.id));
        return index >= 0 ? state.lessons[index + 1] || null : null;
    }

    function lessonHasVideos(lesson) {
        return Array.isArray(lesson?.videos) && lesson.videos.some(video => String(video.url || '').trim());
    }

    function applyNextActionSuggestion({ title, body, tab = null }) {
        if (!els.nextActionTitle || !els.nextActionBody) return;
        els.nextActionTitle.textContent = title;
        els.nextActionBody.textContent = body;
        const panel = els.nextActionTitle.closest('section.panel');
        if (!panel) return;
        panel.classList.toggle('next-action-clickable', !!tab);
        panel.onclick = tab ? () => setActiveTab(tab) : null;
    }

    function renderNextAction(lesson) {
        if (!lesson) {
            applyNextActionSuggestion({
                title: 'Chọn bài học',
                body: 'Chọn một bài trong danh sách bên trái để bắt đầu.'
            });
            return;
        }

        const progress = currentLessonProgress(lesson);
        const ui = currentUiState(lesson);
        const tab = state.activeTab;
        const practice = practiceProgress(lesson, ui);
        const tasks = Array.isArray(lesson.tasks) && lesson.tasks.length ? lesson.tasks : [
            'Đọc lý thuyết ngắn',
            'Xem ví dụ mẫu',
            'Làm bài luyện tập'
        ];
        const scoreData = calculateScore(lesson, ui.answers || {});
        const weakSkills = (lesson.skills || []).filter(skill => (scoreData.skillScores[skill.id] || 0) < (skill.target || 80));
        const nextLesson = nextLessonAfter(lesson);

        if (progress.status === 'mastered' && weakSkills.length === 0) {
            applyNextActionSuggestion({
                title: 'Đã hoàn thành bài này',
                body: nextLesson
                    ? `Có thể chuyển sang "${nextLesson.title}".`
                    : 'Đã đạt mục tiêu của bài này.'
            });
            return;
        }

        if (!ui.theoryDone) {
            if (tab === 'learn') {
                applyNextActionSuggestion({
                    title: 'Đang đọc lý thuyết',
                    body: 'Đọc xong thì bấm "Đánh dấu đã học" để mở phần ví dụ.'
                });
                return;
            }
            applyNextActionSuggestion({
                title: tasks[0] || 'Bắt đầu bằng lý thuyết',
                body: 'Quay lại tab Lý thuyết để nắm khái niệm và ký hiệu của bài.',
                tab: 'learn'
            });
            return;
        }

        if (!ui.examplesDone) {
            if (tab === 'examples') {
                applyNextActionSuggestion({
                    title: 'Đang xem ví dụ',
                    body: 'Xem xong thì bấm "Đánh dấu đã xem ví dụ" để sang luyện tập.'
                });
                return;
            }
            if (tab === 'videos') {
                applyNextActionSuggestion({
                    title: lessonHasVideos(lesson) ? 'Đang xem bài giảng' : 'Bài chưa có video',
                    body: lessonHasVideos(lesson)
                        ? 'Sau video, chuyển sang tab Ví dụ rồi làm luyện tập.'
                        : 'Chuyển sang tab Ví dụ để xem cách giải mẫu.',
                    tab: lessonHasVideos(lesson) ? null : 'examples'
                });
                return;
            }
            applyNextActionSuggestion({
                title: tasks[1] || 'Xem ví dụ mẫu',
                body: 'Ví dụ giúp em thấy cách áp dụng lý thuyết vào bài cụ thể.',
                tab: 'examples'
            });
            return;
        }

        if (!ui.practiceDone) {
            if (tab === 'practice') {
                if (!practice.total) {
                    applyNextActionSuggestion({
                        title: 'Chưa có bài luyện tập',
                        body: 'Giáo viên chưa thêm câu hỏi cho bài này.'
                    });
                    return;
                }
                if (!practice.answered) {
                    applyNextActionSuggestion({
                        title: 'Làm bài luyện tập',
                        body: `Có ${practice.total} câu/bài. Làm xong rồi bấm "Nộp bài" để nhận điểm.`
                    });
                    return;
                }
                if (practice.answered < practice.total) {
                    applyNextActionSuggestion({
                        title: `Tiếp tục luyện tập (${practice.answered}/${practice.total})`,
                        body: 'Hoàn thành các câu còn lại, sau đó nộp bài.'
                    });
                    return;
                }
                applyNextActionSuggestion({
                    title: 'Sẵn sàng nộp bài',
                    body: 'Đã làm hết — bấm "Nộp bài" để hệ thống chấm điểm.'
                });
                return;
            }
            applyNextActionSuggestion({
                title: tasks[2] || 'Làm bài luyện tập',
                body: practice.total
                    ? `Chuyển sang tab Luyện tập — còn ${Math.max(practice.total - practice.answered, practice.total)} bài cần làm.`
                    : 'Chuyển sang tab Luyện tập để kiểm tra kiến thức.',
                tab: 'practice'
            });
            return;
        }

        if (weakSkills.length) {
            const weakest = weakSkills[0];
            const weakestScore = scoreData.skillScores[weakest.id] || progress.score || 0;
            applyNextActionSuggestion({
                title: `Luyện thêm: ${weakest.name}`,
                body: `Hiện ${weakestScore}% — mục tiêu ${weakest.target || 80}%. Làm lại bài luyện để cải thiện.`,
                tab: 'practice'
            });
            return;
        }

        applyNextActionSuggestion({
            title: 'Đã làm xong các bước học',
            body: nextLesson
                ? `Có thể chuyển sang bài "${nextLesson.title}" hoặc ôn lại phần luyện tập.`
                : 'Có thể ôn lại lý thuyết hoặc làm thêm bài luyện.'
        });
    }

    async function syncLessonState(lesson, uiState, extra = {}) {
        const current = currentLessonProgress(lesson);
        const payload = {
            action: 'save_progress',
            lesson_id: lesson.id,
            status: extra.status || current.status || 'in_progress',
            score: typeof extra.score === 'number' ? extra.score : current.score || 0,
            skill_scores: extra.skillScores || current.skillScores || {},
            state: uiState,
            started_at: extra.startedAt || uiState.startedAt || null,
            completed_at: extra.completedAt || uiState.completedAt || null,
        };
        await api('api/lessons.php?action=save_progress&debug=1', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        state.progress[lesson.id] = {
            ...current,
            status: payload.status,
            score: payload.score,
            skillScores: payload.skill_scores,
            state: uiState,
            startedAt: payload.started_at || current.startedAt || null,
            completedAt: payload.completed_at || null,
        };
        if (!isTeacher() || isTeacherPreview()) {
            recordStudyActivity();
            if (payload.status === 'mastered' || payload.score >= 100 || lessonCompletionPercent(lesson, uiState, payload.status) >= 100) {
                markPerfectLesson(lesson);
            }
        }
        return state.progress[lesson.id];
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
            if (!isTeacher()) recordStudyActivity();
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
        if ((state.user?.role || data.user?.role) === 'student') {
            state.lessons = state.lessons.filter(lesson => !!lesson.is_published);
        }
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
                const old = button.innerHTML;
                button.disabled = true;
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> AI đang giải thích...';
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
                    showAiModal(renderAiAnswer(data.answer || ''), button);
                } catch (err) {
                    showAiModal(`<p style="color:#dc2626">${escapeHtml(err.message || 'Chưa gọi được AI.')}</p>`, button);
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

        bindMathSymbolToolbars();
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
