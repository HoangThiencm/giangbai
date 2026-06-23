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
        lessonAiChatAside: document.getElementById('lessonAiChatAside'),
        tabs: Array.from(document.querySelectorAll('.tab-btn')),
    };

    const LOTRINH_PAGE_SUBJECTS = {
        lotrinhtoan4: 'Toán 4',
        lotrinhtoan5: 'Toán 5',
        lotrinhtoan6: 'Toán 6',
        lotrinhtoan7: 'Toán 7',
        lotrinhtoan8: 'Toán 8',
        lotrinhtoan9: 'Toán 9',
    };
    const LOTRINH_ROUTE_ORDER = ['lotrinhtoan4', 'lotrinhtoan5', 'lotrinhtoan6', 'lotrinhtoan7', 'lotrinhtoan8', 'lotrinhtoan9'];
    const LOTRINH_PAGE_URLS = {
        lotrinhtoan4: 'lotrinhtoan4.html',
        lotrinhtoan5: 'lotrinhtoan5.html',
        lotrinhtoan6: 'lotrinhtoan6.html',
        lotrinhtoan7: 'lotrinhtoan7.html',
        lotrinhtoan8: 'lotrinhtoan8.html',
        lotrinhtoan9: 'lotrinhtoan9.html',
    };
    const PAGE_KEY = String(window.LOTRINH_PAGE_KEY || '').trim();
    const PAGE_SUBJECT = LOTRINH_PAGE_SUBJECTS[PAGE_KEY]
        || String(window.LOTRINH_SUBJECT || '').trim()
        || 'Toán 6';
    const PAGE_TITLE = window.LOTRINH_PAGE_TITLE || `Lộ trình tự học ${PAGE_SUBJECT}`;

    function normalizeSubjectName(value) {
        return String(value || '').trim().normalize('NFC');
    }

    function lessonMatchesPageSubject(lesson) {
        return normalizeSubjectName(lesson?.subject) === normalizeSubjectName(PAGE_SUBJECT);
    }

    function studentAllowedPages(user) {
        const pages = user?.allowed_pages;
        return Array.isArray(pages) ? pages : [];
    }

    function studentCanOpenPageKey(pageKey, allowedPages) {
        const pages = Array.isArray(allowedPages) ? allowedPages : [];
        return pages.includes(pageKey)
            || (pageKey === 'lotrinhtoan6' && pages.includes('lotrinh'));
    }

    function primaryLotrinhUrl(allowedPages) {
        const pages = Array.isArray(allowedPages) ? allowedPages : [];
        for (const pageKey of LOTRINH_ROUTE_ORDER) {
            if (studentCanOpenPageKey(pageKey, pages) && LOTRINH_PAGE_URLS[pageKey]) {
                return LOTRINH_PAGE_URLS[pageKey];
            }
        }
        return null;
    }

    function ensureStudentOnAllowedLotrinhPage(user) {
        if (!PAGE_KEY || (user?.role || '') !== 'student') return;
        const allowedPages = studentAllowedPages(user);
        localStorage.setItem('allowedPages', JSON.stringify(allowedPages));
        if (!studentCanOpenPageKey(PAGE_KEY, allowedPages)) {
            const fallback = primaryLotrinhUrl(allowedPages) || 'login.html';
            window.location.replace(fallback);
        }
    }
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

    let lessonListLastScrollId = null;

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

    function renderMarkdownTable(htmlStr) {
        const lines = String(htmlStr || '').split(/(?:<br\s*\/?>|\n)/i);
        const out = [];
        let inTable = false;
        let tableLines = [];

        const flushTable = () => {
            if (!inTable) return;
            out.push(renderHtmlTable(tableLines));
            inTable = false;
            tableLines = [];
        };

        lines.forEach((line) => {
            const trimmed = line.trim();
            if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
                inTable = true;
                tableLines.push(trimmed);
                return;
            }
            flushTable();
            out.push(line);
        });
        flushTable();
        return out.join('<br>');

        function renderHtmlTable(tLines) {
            if (tLines.length < 2 || !tLines[1].replace(/\s/g, '').match(/^\|[\-\:|]+\|$/)) {
                return tLines.join('<br>');
            }
            let tbl = '<table class="lesson-markdown-table"><thead><tr>';
            const headerCells = tLines[0].slice(1, -1).split('|');
            headerCells.forEach(cell => {
                tbl += `<th>${cell.trim()}</th>`;
            });
            tbl += '</tr></thead><tbody>';
            tLines.slice(2).forEach(rowLine => {
                const cells = rowLine.slice(1, -1).split('|');
                tbl += '<tr>';
                cells.forEach(cell => {
                    tbl += `<td>${cell.trim()}</td>`;
                });
                tbl += '</tr>';
            });
            return `${tbl}</tbody></table>`;
        }
    }

    (function injectLessonMarkdownTableStyles() {
        if (document.getElementById('lotrinh-md-table-style')) return;
        const style = document.createElement('style');
        style.id = 'lotrinh-md-table-style';
        style.textContent = `
            .lesson-markdown-table {
                border-collapse: collapse;
                width: 100%;
                max-width: 100%;
                margin: 0.75rem 0;
                font-size: 0.95rem;
            }
            .lesson-markdown-table th,
            .lesson-markdown-table td {
                border: 1px solid #cbd5e1;
                padding: 0.45rem 0.65rem;
                text-align: center;
                vertical-align: middle;
            }
            .lesson-markdown-table th {
                background: #f1f5f9;
                font-weight: 700;
                color: #334155;
            }
            .lesson-markdown-table td { background: #fff; }
            .practice-q-text .lesson-markdown-table,
            .fill-prompt-line .lesson-markdown-table {
                margin-top: 0.5rem;
            }
        `;
        document.head.appendChild(style);
    })();

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
        const html = parts.map(part => {
            if (!part) return '';
            if (isMathPart(part)) {
                return escapeHtml(part.replace(/[ \t]*\n[ \t]*/g, ' '));
            }
            return escapeHtml(part).replace(/\n/g, '<br>');
        }).join('');
        return renderMarkdownTable(html);
    }

    function extractDriveFileId(url) {
        const value = String(url || '').trim();
        const patterns = [
            /drive\.google\.com\/thumbnail\?[^#]*\bid=([a-zA-Z0-9_-]+)/i,
            /drive\.google\.com\/uc\?[^#]*\bid=([a-zA-Z0-9_-]+)/i,
            /drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)/i,
            /drive\.google\.com\/open\?[^#]*\bid=([a-zA-Z0-9_-]+)/i,
        ];
        for (const pattern of patterns) {
            const match = value.match(pattern);
            if (match) return match[1];
        }
        return '';
    }

    function sanitizeLessonImageUrl(url) {
        const value = String(url || '').trim();
        if (!/^https?:\/\//i.test(value)) return '';
        return value.replace(/[\s"'<>]/g, '');
    }

    function normalizeLessonImageDisplayUrl(url) {
        const value = sanitizeLessonImageUrl(url);
        if (!value) return '';
        const fileId = extractDriveFileId(value);
        if (fileId) return `https://drive.google.com/thumbnail?id=${fileId}&sz=w1600`;
        return value;
    }

    function isPendingLessonImageLine(line) {
        const trimmed = String(line || '').trim();
        return /^!\[(?:Đang tải ảnh|ĐANG_TAI:)/i.test(trimmed) && /\(\s*\)$/.test(trimmed);
    }

    function isGenericLessonImageLabel(label) {
        const value = String(label || '').trim();
        if (!value) return true;
        const lower = value.toLowerCase();
        if (/^(ảnh|anh)(\s+screenshot|\s+minh\s*họa)?$/iu.test(value)) return true;
        if (/^image\.(png|jpe?g|webp|gif|bmp)$/i.test(lower)) return true;
        if (/^pasted-image\.(png|jpe?g|webp)$/i.test(lower)) return true;
        if (/^anh-minh-hoa(\.[a-z0-9]+)?$/i.test(lower)) return true;
        if (/^screenshot/i.test(lower)) return true;
        return false;
    }

    function shouldShowLessonImageCaption(label) {
        return !isGenericLessonImageLabel(label);
    }

    function applyLessonInlineMarkup(text) {
        return escapeHtml(text)
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>')
            .replace(/\+\+([^+]+)\+\+/g, '<u>$1</u>');
    }

    function formatLessonTextBlock(text) {
        const parts = text.split(/(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\$[^\n$]*?\$|\\\([\s\S]*?\\\))/g);
        const html = parts.map(part => {
            if (!part) return '';
            if (isMathPart(part)) {
                return escapeHtml(part.replace(/[ \t]*\n[ \t]*/g, ' '));
            }
            return applyLessonInlineMarkup(part).replace(/\n/g, '<br>');
        }).join('');
        return renderMarkdownTable(html);
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
            if (isPendingLessonImageLine(line)) {
                flushText();
                chunks.push(
                    '<figure class="lesson-inline-image lesson-inline-image--pending"><span class="text-sm text-slate-500"><i class="fas fa-spinner fa-spin mr-1"></i>Ảnh chưa tải xong — giáo viên cần dán lại và lưu bài.</span></figure>'
                );
                return;
            }
            const img = line.trim().match(/^!\[([^\]]*)\]\((\S+)\)$/);
            if (img) {
                flushText();
                const url = normalizeLessonImageDisplayUrl(img[2]);
                if (!url) return;
                const altRaw = String(img[1] || '').trim();
                const alt = escapeHtml(altRaw);
                const caption = shouldShowLessonImageCaption(altRaw) ? `<figcaption>${alt}</figcaption>` : '';
                chunks.push(
                    `<figure class="lesson-inline-image"><img src="${escapeHtml(url)}" alt="${alt || 'Ảnh minh họa'}" loading="lazy">${caption}</figure>`
                );
                return;
            }
            if (/^!\[[^\]]*\]\([^)]*\)$/.test(line.trim())) {
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

    function formatAiCacheNote(data) {
        if (!data?.cached) return '';
        const hits = Number(data.cache_hits) > 1 ? ` · dùng lại lần ${data.cache_hits}` : '';
        return `<p class="mt-2 text-xs font-semibold text-sky-700"><i class="fas fa-database mr-1"></i>Đã lưu từ trước${hits} — không tốn quota AI.</p>`;
    }

    function practiceItems(lesson) {
        return [
            ...(Array.isArray(lesson.questions) ? lesson.questions.map(item => ({ type: 'choice', item })) : []),
            ...(Array.isArray(lesson.essay_exercises) ? lesson.essay_exercises.map((item, index) => ({ type: 'essay', item, index })) : []),
            ...(Array.isArray(lesson.fill_exercises) ? lesson.fill_exercises.map((item, index) => ({ type: 'fill', item, index })) : []),
            ...(Array.isArray(lesson.drag_exercises) ? lesson.drag_exercises.map((item, index) => ({ type: 'drag', item, index })) : []),
        ];
    }

    const BLANK_TOKEN_RE = /_{3,}|\[\.\.\.\]|\[\s*\]/g;
    const POOL_ITEM_JOINER = ' » ';
    const POOL_ITEM_SEP_RE = /\s*»\s*/u;
    // Chỉ tách khi dấu phẩy có khoảng trắng (7, 2, 8) — không tách số thập phân 7,2 hay 70,208
    const FILL_COMMA_LIST_RE = /\s*,\s+|\s+,\s*/;

    function splitPoolTextByGt(value) {
        const source = String(value || '');
        if (!source) return [];
        const parts = [];
        let current = '';
        let inInlineMath = false;
        let inDisplayMath = false;
        for (let i = 0; i < source.length; i += 1) {
            if (!inInlineMath && source.startsWith('$$', i)) {
                inDisplayMath = !inDisplayMath;
                current += '$$';
                i += 1;
                continue;
            }
            if (!inDisplayMath && source[i] === '$') {
                inInlineMath = !inInlineMath;
                current += '$';
                continue;
            }
            if (source[i] === '>' && !inInlineMath && !inDisplayMath) {
                const trimmed = current.trim();
                if (trimmed) parts.push(trimmed);
                current = '';
                continue;
            }
            current += source[i];
        }
        const trimmed = current.trim();
        if (trimmed) parts.push(trimmed);
        return parts;
    }

    function splitPoolText(value) {
        const source = String(value || '');
        if (!source) return [];
        if (POOL_ITEM_SEP_RE.test(source)) {
            return source.split(POOL_ITEM_SEP_RE).map(part => part.trim()).filter(Boolean);
        }
        return splitPoolTextByGt(source);
    }

    function splitFillAnswerList(value, blankCount = 0) {
        if (Array.isArray(value)) {
            return value.map(part => String(part || '').trim()).filter(Boolean);
        }
        const source = String(value || '').trim();
        if (!source) return [];
        if (POOL_ITEM_SEP_RE.test(source)) return splitPoolText(source);
        if (FILL_COMMA_LIST_RE.test(source)) {
            const parts = source.split(FILL_COMMA_LIST_RE).map(part => part.trim()).filter(Boolean);
            if (parts.length > 1) return parts;
        }
        if (source.includes(';')) {
            const parts = source.split(/\s*;\s*/).map(part => part.trim()).filter(Boolean);
            if (parts.length > 1) return parts;
        }
        if (source.includes('>')) {
            const gtParts = splitPoolTextByGt(source);
            if (gtParts.length > 1) return gtParts;
        }
        if (blankCount > 1 && source.length === 1 && blankCount === source.length) {
            return source.split('');
        }
        return [source];
    }

    function joinPoolText(items) {
        return (items || []).map(item => String(item || '').trim()).filter(Boolean).join(POOL_ITEM_JOINER);
    }

    function repairPoolPieces(pieces, expectedCount = 0) {
        if (!Array.isArray(pieces) || pieces.length <= 1) return pieces || [];
        const repaired = splitPoolText(pieces.join(' > '));
        if (repaired.length >= pieces.length) return pieces;
        if (expectedCount > 0 && repaired.length === expectedCount) return repaired;
        if (!expectedCount && repaired.length < pieces.length) return repaired;
        return pieces;
    }

    function countBlankTokens(prompt) {
        const matches = String(prompt || '').match(BLANK_TOKEN_RE);
        return matches?.length || 1;
    }

    function normalizeFillSlots(saved, blankCount) {
        if (Array.isArray(saved)) return saved.slice(0, blankCount);
        if (typeof saved === 'string' && saved.trim()) return [saved.trim()];
        return Array.from({ length: blankCount }, () => '');
    }

    function normalizeFillExercise(item) {
        const prompt = String(item?.prompt || '');
        const blankCount = countBlankTokens(prompt);
        let pool = Array.isArray(item?.items) ? [...item.items] : splitPoolText(item?.pool);
        let answers = splitFillAnswerList(item?.answer, blankCount);
        if (answers.length === 1 && blankCount > 1) {
            const expanded = splitFillAnswerList(answers[0], blankCount);
            if (expanded.length > 1) answers = expanded;
        }
        if (!pool.length && answers.length) pool = [...answers];
        if (!answers.length && pool.length) answers = blankCount > 1 ? pool.slice(0, blankCount) : [pool[0]];
        return {
            ...item,
            prompt,
            blankCount,
            pool,
            answers: answers.slice(0, blankCount),
            hint: item?.hint || ''
        };
    }

    function parseMatchPairs(spec) {
        return String(spec || '').split(',').map(part => part.trim()).filter(Boolean).map(part => {
            const [left, right] = part.split('-').map(value => Number.parseInt(value, 10));
            if (!Number.isFinite(left) || !Number.isFinite(right)) return null;
            return { left, right };
        }).filter(Boolean);
    }

    function normalizeDragExercise(item) {
        if (item?.mode === 'match' || (Array.isArray(item?.left) && Array.isArray(item?.right))) {
            const pairs = Array.isArray(item.pairs) && item.pairs.length
                ? item.pairs
                : parseMatchPairs(item.pair_spec || item.pairs_text || '');
            const pairCount = pairs.length || 0;
            const left = repairPoolPieces(Array.isArray(item.left) ? item.left : [], pairCount);
            const right = repairPoolPieces(Array.isArray(item.right) ? item.right : [], pairCount);
            return {
                ...item,
                mode: 'match',
                left,
                right,
                pairs,
                hint: item?.hint || ''
            };
        }
        const items = Array.isArray(item?.items) ? item.items : splitPoolText(item?.items_text);
        const answer = Array.isArray(item?.answer) ? item.answer : splitPoolText(item?.answer_text || item?.answer);
        return {
            ...item,
            mode: 'sort',
            items,
            answer,
            hint: item?.hint || ''
        };
    }

    function isDragMatchAnswer(value) {
        return value && typeof value === 'object' && !Array.isArray(value);
    }

    function shuffleSeed(text) {
        let hash = 0;
        const value = String(text || '');
        for (let i = 0; i < value.length; i += 1) {
            hash = ((hash << 5) - hash) + value.charCodeAt(i);
            hash |= 0;
        }
        return Math.abs(hash) || 1;
    }

    function seededShuffle(items, seed) {
        const arr = [...items];
        let state = seed >>> 0;
        const random = () => {
            state = (state * 1664525 + 1013904223) >>> 0;
            return state / 0x100000000;
        };
        for (let i = arr.length - 1; i > 0; i -= 1) {
            const j = Math.floor(random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    function shuffledIndices(length, seed) {
        return seededShuffle(Array.from({ length }, (_, index) => index), seed);
    }

    function renderPracticeCheckButton(className, attrName, attrValue, practiceDone) {
        if (practiceDone) return '';
        return `
            <button type="button" class="${className} practice-btn practice-btn--primary" ${attrName}="${escapeHtml(attrValue)}">
                <i class="fas fa-check"></i>Kiểm tra đáp án
            </button>
        `;
    }

    function renderPracticeAiButton(aiText) {
        return `
            <button type="button" class="practice-btn practice-btn--ghost drag-ai-btn fill-ai-btn essay-ai-btn" data-ai-text="${escapeHtml(aiText)}">
                <i class="fas fa-wand-magic-sparkles"></i>Hỏi AI
            </button>
        `;
    }

    function renderPracticeQuestionMeta(index, typeLabel, theme) {
        return `
            <div class="practice-card-meta">
                <span class="practice-q-badge practice-q-badge--${theme}">Câu ${index + 1}</span>
                ${typeLabel ? `<span class="practice-type-chip practice-type-chip--${theme}">${escapeHtml(typeLabel)}</span>` : ''}
            </div>
        `;
    }

    function renderPracticeHint(html) {
        return `<div class="practice-hint"><i class="fas fa-lightbulb" aria-hidden="true"></i><span>${html}</span></div>`;
    }

    function renderPracticeActions(buttonsHtml) {
        return `<div class="practice-card-actions">${buttonsHtml}</div>`;
    }

    function renderPracticeFeedback(className, content, visible = true) {
        return `<div class="${className} practice-feedback ${visible ? '' : 'hidden'}">${content}</div>`;
    }

    function buildFillCheckFeedback(normalized, slots) {
        const filledCount = slots.filter(slot => String(slot || '').trim()).length;
        if (filledCount < normalized.blankCount) {
            return '<span class="font-bold text-slate-600">Hãy kéo đủ mảnh vào tất cả ô trống trước khi kiểm tra.</span>';
        }
        const ok = normalized.answers.length > 0
            && normalized.answers.every((answer, slotIndex) => essayAnswersEqual(slots[slotIndex], answer));
        return ok
            ? '<span class="font-bold text-teal-700">Đúng.</span> Em đã kéo đúng vào các ô trống.'
            : `<span class="font-bold text-rose-700">Chưa đúng.</span> Đáp án mẫu: ${normalized.answers.map(part => mathText(part)).join(' · ')}${normalized.blankCount > 1 ? ` <span class="text-slate-600">(${normalized.blankCount} ô trống)</span>` : ''}`;
    }

    function sortPieceIndex(piece, items) {
        const key = normalizeAnswerText(piece);
        return items.findIndex(item => normalizeAnswerText(item) === key);
    }

    function isSortAnswerCorrect(normalized, savedOrder) {
        if (!savedOrder.length || savedOrder.length < normalized.items.length) return false;
        const expectedIndexes = normalized.answer.map(answer => sortPieceIndex(answer, normalized.items));
        const givenIndexes = savedOrder.map(piece => sortPieceIndex(piece, normalized.items));
        if (expectedIndexes.every(index => index >= 0) && givenIndexes.every(index => index >= 0)) {
            return expectedIndexes.join('|') === givenIndexes.join('|');
        }
        return savedOrder.map(normalizeAnswerText).join('|') === normalized.answer.map(normalizeAnswerText).join('|');
    }

    function buildSortCheckFeedback(normalized, savedOrder, poolRemaining = 0) {
        if (!savedOrder.length) {
            if (poolRemaining > 0) {
                return '<span class="font-bold text-slate-600">Các mảnh vẫn đang ở khay phía trên. Hãy <strong>kéo xuống hàng trả lời bên dưới</strong> theo thứ tự đúng, rồi bấm kiểm tra.</span>';
            }
            return '<span class="font-bold text-slate-600">Hãy kéo các mảnh xuống hàng trả lời bên dưới theo thứ tự đúng trước khi kiểm tra.</span>';
        }
        if (savedOrder.length < normalized.items.length) {
            return '<span class="font-bold text-slate-600">Hãy kéo đủ tất cả mảnh xuống hàng trả lời bên dưới theo thứ tự trước khi kiểm tra.</span>';
        }
        const ok = isSortAnswerCorrect(normalized, savedOrder);
        return ok
            ? '<span class="font-bold text-teal-700">Đúng.</span> Thứ tự đã khớp.'
            : `<span class="font-bold text-rose-700">Chưa đúng.</span> Thứ tự đúng: ${escapeHtml(normalized.answer.join(' → '))}`;
    }

    function getMatchPairValue(matches, leftIndex) {
        if (!matches || typeof matches !== 'object' || Array.isArray(matches)) return undefined;
        const leftKey = Number(leftIndex);
        if (!Number.isFinite(leftKey) || leftKey < 0) return undefined;
        if (matches[leftKey] !== undefined) return Number(matches[leftKey]);
        if (matches[String(leftKey)] !== undefined) return Number(matches[String(leftKey)]);
        return undefined;
    }

    function normalizeMatchAnswers(raw) {
        if (!isDragMatchAnswer(raw)) return {};
        const savedMatches = {};
        Object.entries(raw).forEach(([left, right]) => {
            const leftIndex = Number.parseInt(left, 10);
            const rightIndex = Number.parseInt(right, 10);
            if (Number.isFinite(leftIndex) && leftIndex >= 0 && Number.isFinite(rightIndex) && rightIndex >= 0) {
                savedMatches[leftIndex] = rightIndex;
            }
        });
        return savedMatches;
    }

    function collectMatchAnswersFromCard(card) {
        const savedMatches = {};
        if (!card) return savedMatches;
        card.querySelectorAll('.match-item[data-match-side="left"]').forEach(leftBtn => {
            const leftIndex = Number.parseInt(leftBtn.dataset.matchIndex || '-1', 10);
            if (!Number.isFinite(leftIndex) || leftIndex < 0) return;

            const pairedRight = leftBtn.dataset.pairedRight;
            if (pairedRight !== undefined && pairedRight !== '') {
                const rightIndex = Number.parseInt(pairedRight, 10);
                if (Number.isFinite(rightIndex) && rightIndex >= 0) {
                    savedMatches[leftIndex] = rightIndex;
                    return;
                }
            }

            const pairOrder = Number.parseInt(leftBtn.querySelector('.match-pair-badge')?.textContent?.trim() || '', 10);
            if (!Number.isFinite(pairOrder) || pairOrder < 1) return;
            const rightBtn = Array.from(card.querySelectorAll('.match-item[data-match-side="right"]'))
                .find(node => Number.parseInt(node.querySelector('.match-pair-badge')?.textContent?.trim() || '', 10) === pairOrder);
            const rightIndex = Number.parseInt(rightBtn?.dataset.matchIndex || '-1', 10);
            if (Number.isFinite(rightIndex) && rightIndex >= 0) savedMatches[leftIndex] = rightIndex;
        });
        return savedMatches;
    }

    function resolveMatchAnswers(lesson, key, card = null) {
        const fromState = normalizeMatchAnswers(currentUiState(lesson).dragAnswers?.[key]);
        const matchCard = card || document.querySelector(`[data-match-card="${escapeSelector(key)}"]`);
        const fromDom = collectMatchAnswersFromCard(matchCard);
        return { ...fromState, ...fromDom };
    }

    function syncLocalLessonUiState(lesson, nextUi) {
        const current = currentLessonProgress(lesson);
        state.progress[lesson.id] = {
            ...current,
            state: nextUi
        };
    }

    function isMatchAnswerCorrect(normalized, savedMatches) {
        if (!normalized?.pairs?.length || !normalized.left?.length) return false;
        const pairedCount = Object.keys(savedMatches || {}).length;
        if (pairedCount < normalized.left.length) return false;
        return normalized.pairs.every(pair => getMatchPairValue(savedMatches, pair.left) === Number(pair.right));
    }

    function buildMatchCheckFeedback(normalized, savedMatches) {
        const totalPairs = normalized.left.length;
        const pairedCount = Object.keys(savedMatches || {}).length;
        if (!totalPairs) {
            return '<span class="font-bold text-slate-600">Chưa có dữ liệu nối cặp để kiểm tra.</span>';
        }
        if (pairedCount < totalPairs) {
            return '<span class="font-bold text-slate-600">Hãy nối đủ tất cả các cặp trước khi kiểm tra.</span>';
        }
        const ok = isMatchAnswerCorrect(normalized, savedMatches);
        return ok
            ? '<span class="font-bold text-teal-700">Đúng.</span> Em đã nối đủ các cặp.'
            : `<span class="font-bold text-rose-700">Chưa đúng.</span> ${escapeHtml(normalized.hint || 'Hãy kiểm tra lại các cặp chưa khớp.')}`;
    }

    function practiceProgress(lesson, ui = currentUiState(lesson)) {
        const items = practiceItems(lesson);
        if (!items.length) return { answered: 0, total: 0, percent: 0 };
        const answered = items.filter(({ type, item, index }) => {
            if (type === 'choice') return ui.answers?.[item.id] !== undefined && ui.answers?.[item.id] !== null;
            const key = item.id || `${type}_${index + 1}`;
            if (type === 'essay') return String(ui.essayAnswers?.[key] || '').trim() !== '';
            if (type === 'fill') {
                const normalized = normalizeFillExercise(item);
                const slots = normalizeFillSlots(ui.fillAnswers?.[key], normalized.blankCount);
                return slots.filter(slot => String(slot || '').trim() !== '').length >= normalized.blankCount;
            }
            if (type === 'drag') {
                const normalized = normalizeDragExercise(item);
                const saved = ui.dragAnswers?.[key];
                if (normalized.mode === 'match') {
                    const matches = normalizeMatchAnswers(saved);
                    return normalized.left.length > 0 && Object.keys(matches).length >= normalized.left.length;
                }
                return Array.isArray(saved) && saved.length > 0;
            }
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

    function practiceScorePercent(lesson, progressOverride = null) {
        const progress = progressOverride || currentLessonProgress(lesson);
        const score = Number(progress?.score);
        return Number.isFinite(score) ? Math.max(0, Math.min(100, Math.round(score))) : null;
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

    const API_TIMEOUT_MS = 25000;

    async function api(url, options = {}) {
        const controller = new AbortController();
        const timer = window.setTimeout(() => controller.abort(), API_TIMEOUT_MS);
        try {
            const res = await fetch(url, {
                cache: 'no-store',
                credentials: 'include',
                ...options,
                signal: options.signal || controller.signal,
            });
            const text = await res.text();
            let data = null;
            try { data = text ? JSON.parse(text) : null; } catch { data = { error: text }; }
            if (!res.ok) {
                const base = data && (data.error || data.message) ? (data.error || data.message) : `HTTP ${res.status}`;
                const detail = data && data.detail ? String(data.detail) : '';
                const message = detail && detail !== base ? `${base} (${detail})` : (detail || base);
                const err = new Error(message);
                err.code = data?.code || '';
                err.quota = data?.quota || null;
                throw err;
            }
            return data;
        } catch (err) {
            if (err?.name === 'AbortError') {
                throw new Error('Mạng chậm hoặc máy chủ không phản hồi. Vui lòng thử lại.');
            }
            throw err;
        } finally {
            window.clearTimeout(timer);
        }
    }

    function formatAiErrorMessage(err) {
        if (err?.code === 'student_quota_exhausted') {
            return err?.message || 'Hôm nay em đã hết lượt hỏi AI. Mai hỏi tiếp hoặc xem lại phần đã giải thích nhé.';
        }
        if (err?.code === 'quota_exhausted_block') {
            return 'Hôm nay đã hết quota AI miễn phí, vui lòng thử lại ngày mai.';
        }
        return err?.message || 'Chưa gọi được AI.';
    }

    function formatAiErrorHtml(err) {
        return `<p style="color:#dc2626">${escapeHtml(formatAiErrorMessage(err))}</p>`;
    }

    async function refreshTeacherQuotaBanner() {
        if (!isTeacher() || isTeacherPreview()) {
            document.getElementById('teacherQuotaBanner')?.remove();
            return;
        }
        try {
            const res = await fetch('api/ai_quota.php', { credentials: 'include', cache: 'no-store' });
            const data = await res.json();
            if (!res.ok) return;
            renderTeacherQuotaBanner(data.smart_quota);
        } catch (err) {
            console.warn('Không tải quota AI:', err);
        }
    }

    function renderTeacherQuotaBanner(sq) {
        const host = els.teacherLessonDesigner;
        if (!host) return;
        document.getElementById('teacherQuotaBanner')?.remove();
        if (!sq?.enabled || !sq.teacher_notice || sq.level === 'normal' || sq.level === 'disabled') return;

        const levelClass = ({
            warn: 'border-amber-300 bg-amber-50 text-amber-950',
            critical: 'border-orange-300 bg-orange-50 text-orange-950',
            exhausted: 'border-rose-300 bg-rose-50 text-rose-950',
        })[sq.level] || 'border-sky-300 bg-sky-50 text-sky-950';
        const icon = ({
            warn: 'fa-triangle-exclamation text-amber-600',
            critical: 'fa-circle-exclamation text-orange-600',
            exhausted: 'fa-ban text-rose-600',
        })[sq.level] || 'fa-robot text-sky-600';

        const banner = document.createElement('section');
        banner.id = 'teacherQuotaBanner';
        banner.className = `mb-4 rounded-lg border px-4 py-3 text-sm leading-6 ${levelClass}`;
        banner.innerHTML = `
            <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <p><i class="fas ${icon} mr-2"></i><strong>Smart Quota:</strong> ${escapeHtml(sq.teacher_notice)}</p>
                <a href="theodoi-ai.html" class="inline-flex shrink-0 items-center gap-1 text-xs font-bold underline opacity-90 hover:opacity-100">
                    <i class="fas fa-chart-line"></i> Theo dõi AI
                </a>
            </div>
            <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-white/70">
                <div class="h-full rounded-full bg-current opacity-60" style="width:${Math.max(0, Math.min(100, Number(sq.used_pct) || 0))}%"></div>
            </div>
        `;
        host.prepend(banner);
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
        els.resetBtn?.classList.toggle('hidden', teacher || preview);
        if (els.accountRoleLabel) {
            els.accountRoleLabel.textContent = teacher ? 'Giáo viên' : 'Học sinh';
        }
        if (els.routeTitle) {
            els.routeTitle.textContent = teacher
                ? (preview ? `Xem thử · ${PAGE_SUBJECT}` : `Soạn bài · ${PAGE_SUBJECT}`)
                : PAGE_TITLE;
        }
        if (els.routeSubject) {
            els.routeSubject.textContent = teacher
                ? (preview ? 'Giao diện học sinh' : 'Không gian soạn bài')
                : PAGE_SUBJECT;
        }
        if (teacher && typeof window.mountTeacherLotrinhNav === 'function') {
            window.mountTeacherLotrinhNav({ mode: preview ? 'preview' : 'design', subject: PAGE_SUBJECT });
        }
        if (teacher && !preview) {
            refreshTeacherQuotaBanner();
        } else {
            document.getElementById('teacherQuotaBanner')?.remove();
        }
    }

    function render() {
        ensurePracticeStyles();
        const lesson = currentLesson();
        if (state.loading) {
            els.studentName.textContent = 'Đang tải...';
            if (els.routeTitle) els.routeTitle.textContent = PAGE_TITLE;
            if (els.routeSubject) els.routeSubject.textContent = PAGE_SUBJECT;
            if (els.routeChapter) els.routeChapter.textContent = 'Đang tải bài học...';
            els.lessonTitle.textContent = 'Đang tải dữ liệu';
            els.lessonGoal.textContent = '';
            els.lessonList.innerHTML = '<div class="text-sm text-slate-500">Đang tải bài học...</div>';
            return;
        }

        if (state.error) {
            els.studentName.textContent = 'Lỗi tải dữ liệu';
            if (els.routeTitle) els.routeTitle.textContent = PAGE_TITLE;
            if (els.routeSubject) els.routeSubject.textContent = PAGE_SUBJECT;
            if (els.routeChapter) els.routeChapter.textContent = 'Không tải được dữ liệu';
            els.lessonTitle.textContent = 'Không thể mở lộ trình';
            els.lessonGoal.textContent = state.error;
            els.lessonList.innerHTML = `
                <div class="space-y-3 text-sm">
                    <p class="leading-6 text-rose-700">${escapeHtml(state.error)}</p>
                    <div class="flex flex-wrap gap-2">
                        <button type="button" id="lotrinhRetryBtn" class="inline-flex items-center gap-2 rounded border border-teal-300 bg-teal-50 px-3 py-2 text-xs font-bold text-teal-800 hover:bg-teal-100">
                            <i class="fas fa-rotate-right"></i>Thử lại
                        </button>
                        <button type="button" id="lotrinhReloginBtn" class="inline-flex items-center gap-2 rounded border border-rose-200 bg-white px-3 py-2 text-xs font-bold text-rose-700 hover:bg-rose-50">
                            <i class="fas fa-right-from-bracket"></i>Đăng nhập lại
                        </button>
                    </div>
                </div>`;
            document.getElementById('lotrinhRetryBtn')?.addEventListener('click', () => { void bootstrapLotrinhPage(); });
            document.getElementById('lotrinhReloginBtn')?.addEventListener('click', logout);
            return;
        }

        els.studentName.textContent = state.user?.full_name || state.user?.username || 'Tài khoản';
        applyRoleView();
        if (isTeacher() && !isTeacherPreview()) return;

        renderTeacherPreviewBanner();
        renderOverallProgress();
        cleanupVerboseRightPanels();
        renderLessonList();
        renderHeader(lesson);
        renderTabs();
        renderSkills(lesson);
        bindPracticeInteractions(lesson);
        refreshStudentAiAssist(lesson);
        typesetMath();
    }

    function refreshLearningChrome(lesson) {
        if (!lesson) return;
        renderOverallProgress();
        renderLessonList({ scrollToActive: false });
        renderHeader(lesson);
        renderSkills(lesson);
    }

    function cleanupVerboseRightPanels() {
        document.getElementById('studyPlannerPanel')?.remove();
        document.getElementById('motivationPanel')?.remove();
        document.getElementById('lessonAiChatRoot')?.remove();
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
        return document.getElementById('lessonRightAside')
            || document.querySelector('#studentLearningMain section.grid > aside');
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
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
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
        if (!isoDate) return null;
        const then = new Date(isoDate).getTime();
        if (Number.isNaN(then)) return null;
        return (Date.now() - then) / (1000 * 60 * 60 * 24);
    }

    function staleMasteredDays(completedAt) {
        const elapsed = daysSince(completedAt);
        if (elapsed === null || !Number.isFinite(elapsed)) return null;
        return Math.floor(elapsed);
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
        if (progress.status === 'mastered') {
            const days = staleMasteredDays(completedAt);
            if (days !== null && days >= REVIEW_STALE_DAYS) {
                return { priority: 65, reason: `Đã học xong ${days} ngày trước — nên ôn lại`, tab: 'practice', minutes: 10, title: 'Ôn lại kiến thức cũ' };
            }
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
                title: 'Đọc kiến thức cần nhớ',
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
        const term = String(search || '').trim().toLowerCase();
        if (!term) return true;
        const haystack = `${lesson.title || ''} ${lesson.chapter || ''}`.toLowerCase();
        return haystack.includes(term);
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
                state.lessonListUi.search = searchInput.value;
                renderLessonList({ updateToolbar: false });
            };
        }
        if (chapterSelect) {
            chapterSelect.onchange = () => {
                state.lessonListUi.chapter = chapterSelect.value || '';
                renderLessonList({ updateToolbar: false });
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

    function renderLessonList(options = {}) {
        const { updateToolbar = true, scrollToActive } = options;
        ensureLessonListShell();

        if (!state.lessons.length) {
            document.getElementById('lessonListToolbar')?.replaceChildren();
            document.getElementById('lessonListMeta')?.replaceChildren();
            els.lessonList.innerHTML = '<div class="text-sm text-slate-500">Chưa có bài học nào được giáo viên mở.</div>';
            return;
        }

        const activeLessonId = String(state.selectedLessonId || state.lessons[0]?.id || '');
        const chapterGroups = groupLessonsByChapter(state.lessons);
        if (updateToolbar) renderLessonListToolbar(chapterGroups);

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
        const shouldScrollActive = scrollToActive ?? (activeLessonId !== lessonListLastScrollId);
        if (activeItem && shouldScrollActive) {
            window.requestAnimationFrame(() => activeItem.scrollIntoView({ block: 'nearest' }));
            lessonListLastScrollId = activeLessonId;
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
            if (els.lessonStatus) els.lessonStatus.innerHTML = '';
            return;
        }

        const progress = currentLessonProgress(lesson);
        const status = statusInfo(progress.status);
        const lessonPercent = lessonCompletionPercent(lesson);
        const ui = currentUiState(lesson);
        const submittedPracticeScore = ui.practiceDone ? practiceScorePercent(lesson, progress) : null;
        if (els.routeTitle) els.routeTitle.textContent = PAGE_TITLE;
        if (els.routeSubject) els.routeSubject.textContent = lesson.subject || 'Lộ trình';
        if (els.routeChapter) els.routeChapter.textContent = lesson.chapter || 'Danh sách bài học';
        els.lessonPath.textContent = `${lesson.subject} · ${lesson.chapter}`;
        els.lessonTitle.textContent = lesson.title;
        els.lessonGoal.textContent = lesson.goal || '';
        if (!els.lessonStatus) return;
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
            ${submittedPracticeScore !== null ? `
            <div class="mt-2 flex items-center justify-between text-xs font-semibold text-slate-600">
                <span>Điểm luyện tập (GV xem)</span>
                <span class="${submittedPracticeScore >= 80 ? 'text-teal-700' : 'text-amber-700'}">${submittedPracticeScore}%</span>
            </div>
            ` : ''}
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
                    practiceScore: Number.isFinite(Number(ui.practiceScore))
                        ? Math.round(Number(ui.practiceScore))
                        : (Number.isFinite(Number(progress.score)) ? Math.round(Number(progress.score)) : 100),
                    completedAt,
                    startedAt: ui.startedAt || completedAt
                };
                const practiceScore = nextUi.practiceScore;
                await syncLessonState(lesson, {
                    ...nextUi
                }, {
                    status: 'mastered',
                    score: practiceScore,
                    skillScores: lessonProgressSkillScores(lesson, practiceScore),
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
        if (state.activeTab === 'self_practice') renderSelfPractice(lesson);
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
                ${renderParagraphs(theory, 'Giáo viên chưa nhập kiến thức cần nhớ cho bài này.')}
                <button id="markTheoryDone" class="inline-flex items-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800">
                    <i class="fas fa-check"></i>${ui.theoryDone ? 'Đã hoàn thành kiến thức cần nhớ' : 'Đánh dấu đã học'}
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

    function renderPracticePart(title, icon, bodyHtml, count = 0, note = '', theme = 'choice') {
        const countLabel = count === 1 ? '1 câu' : `${count} câu`;
        return `
            <section class="practice-part practice-part--${theme}">
                <header class="practice-part-head">
                    <div class="practice-part-icon"><i class="fas ${icon}" aria-hidden="true"></i></div>
                    <div class="practice-part-intro">
                        <div class="practice-part-title-row">
                            <h2 class="practice-part-title">${escapeHtml(title)}</h2>
                            <span class="practice-part-count">${countLabel}</span>
                        </div>
                        ${note ? `<p class="practice-part-note">${note}</p>` : ''}
                    </div>
                </header>
                <div class="practice-part-body">${bodyHtml}</div>
            </section>
        `;
    }

    function preprocessEssayAnswerExpression(raw) {
        let text = String(raw ?? '').trim();
        if (!text) return '';
        text = text
            .replace(/,/g, '.')
            .replace(/÷/g, '/')
            .replace(/×/g, '*')
            .replace(/−/g, '-')
            .replace(/√\(([^)]+)\)/g, 'sqrt($1)')
            .replace(/√\{([^}]+)\}/g, 'sqrt($1)')
            .replace(/√(-?(?:\d+\.\d+|\d+|\.\d+))/g, 'sqrt($1)')
            .replace(/\\sqrt\{([^}]*)\}/g, 'sqrt($1)')
            .replace(/\\sqrt\(([^)]*)\)/g, 'sqrt($1)')
            .replace(/\\sqrt\s*(-?(?:\d+\.\d+|\d+|\.\d+))/g, 'sqrt($1)')
            .replace(/\\frac\{([^}]*)\}\{([^}]*)\}/g, '($1)/($2)')
            .replace(/\s+/g, '');
        return text;
    }

    function parseEssayNumericToken(token) {
        const text = String(token ?? '').trim();
        if (!text) return { ok: false };
        if (/^-?(?:\d+\.\d+|\d+|\.\d+)$/.test(text)) {
            const value = Number.parseFloat(text);
            return Number.isFinite(value) ? { ok: true, value } : { ok: false };
        }
        const fraction = text.match(/^(-?(?:\d+\.\d+|\d+|\.\d+))\/(-?(?:\d+\.\d+|\d+|\.\d+))$/);
        if (fraction) {
            const numerator = Number.parseFloat(fraction[1]);
            const denominator = Number.parseFloat(fraction[2]);
            if (!Number.isFinite(numerator) || !Number.isFinite(denominator) || denominator === 0) return { ok: false };
            return { ok: true, value: numerator / denominator };
        }
        const sqrtMatch = text.match(/^sqrt\((.+)\)$/i);
        if (sqrtMatch) {
            const inner = parseEssayNumericToken(preprocessEssayAnswerExpression(sqrtMatch[1]));
            if (!inner.ok || inner.value < 0) return { ok: false };
            const value = Math.sqrt(inner.value);
            return Number.isFinite(value) ? { ok: true, value } : { ok: false };
        }
        return { ok: false };
    }

    function tryEvaluateEssayAnswer(raw) {
        const normalized = preprocessEssayAnswerExpression(raw);
        if (!normalized) return { ok: false };
        return parseEssayNumericToken(normalized);
    }

    function essayAnswersEqual(given, expected) {
        const left = String(given ?? '').trim();
        const right = String(expected ?? '').trim();
        if (!left || !right) return false;
        if (normalizeAnswerText(left) === normalizeAnswerText(right)) return true;

        const givenEval = tryEvaluateEssayAnswer(left);
        const expectedEval = tryEvaluateEssayAnswer(right);
        if (givenEval.ok && expectedEval.ok) {
            return Math.abs(givenEval.value - expectedEval.value) < 1e-9;
        }
        return false;
    }

    function isEssayNumericAnswer(value) {
        const text = String(value ?? '').trim();
        if (!text) return false;
        if (tryEvaluateEssayAnswer(text).ok) return true;
        const normalized = preprocessEssayAnswerExpression(text);
        return /^-?(?:\d+(?:\.\d+)?|\d*\.\d+)(?:\/-?(?:\d+(?:\.\d+)?|\d*\.\d+))?$/.test(normalized)
            || /^sqrt\(.+\)$/i.test(normalized)
            || /^\\frac\{[^}]+\}\{[^}]+\}$/.test(text.replace(/\s+/g, ''))
            || /^√/.test(text);
    }

    function buildEssayCheckFeedback(item, value) {
        const trimmed = String(value || '').trim();
        if (!trimmed) {
            return '<span class="font-bold text-slate-600">Hãy nhập đáp án trước khi kiểm tra.</span>';
        }
        if (!isEssayNumericAnswer(trimmed)) {
            return '<span class="font-bold text-amber-700">Chỉ nhập kết quả cuối cùng.</span> Dùng số, phân số (<strong>1/2</strong>), hoặc căn (<strong>√16</strong>, <strong>4</strong>). Không nhập lời giải hay đơn vị.';
        }
        const ok = essayAnswersEqual(trimmed, item?.answer || '');
        return ok
            ? '<span class="font-bold text-teal-700">Đúng.</span> Em đang đi đúng hướng.'
            : `<span class="font-bold text-rose-700">Chưa đúng.</span> Gợi ý: ${escapeHtml(item?.hint || 'Hãy thử so sánh với đáp án mẫu.')}`;
    }

    function renderEssayExercises(lesson) {
        const items = Array.isArray(lesson.essay_exercises) ? lesson.essay_exercises : [];
        if (!items.length) return '';
        const ui = currentUiState(lesson);
        const practiceDone = !!ui.practiceDone;
        return items.map((item, index) => {
            const key = item.id || `essay_${index + 1}`;
            const saved = ui.essayAnswers?.[key] || '';
            const ok = practiceDone && essayAnswersEqual(saved, item.answer || '');
            const feedback = practiceDone
                ? (ok
                    ? '<span class="font-bold text-teal-700">Đúng.</span> Em đang đi đúng hướng.'
                    : `<span class="font-bold text-rose-700">Chưa đúng.</span> Gợi ý: ${escapeHtml(item.hint || 'Hãy thử so sánh với đáp án mẫu.')}`)
                : '';
            return `
                <article class="practice-card practice-card--essay">
                    <div class="question-head practice-card-head">
                        ${renderPracticeQuestionMeta(index, 'Tự luận', 'essay')}
                        <h3 class="question-text practice-q-text">${mathText(item.prompt || '')}</h3>
                    </div>
                    <div class="practice-card-content">
                        ${renderPracticeHint('Nhập <strong>kết quả cuối</strong>: số (<strong>4</strong>), phân số (<strong>1/2</strong>), hoặc căn (<strong>√16</strong>). Có thể dùng các nút ký hiệu bên dưới.')}
                        <input type="text" class="essay-input" data-essay-key="${escapeHtml(key)}" inputmode="text" autocomplete="off" placeholder="Ví dụ: 4, -3, 1/2, √16" value="${escapeHtml(saved)}" ${practiceDone ? 'disabled' : ''}>
                        ${practiceDone ? '' : renderMathSymbolToolbar('essay', key)}
                        ${renderPracticeActions(`
                            ${practiceDone ? '' : `<button type="button" class="essay-check-btn practice-btn practice-btn--primary" data-essay-key="${escapeHtml(key)}"><i class="fas fa-check"></i>Kiểm tra đáp án</button>`}
                            ${renderPracticeAiButton(item.prompt || '')}
                        `)}
                        ${renderPracticeFeedback('essay-feedback', feedback, practiceDone)}
                    </div>
                </article>
            `;
        }).join('');
    }

    function renderPromptWithFillSlots(prompt, key, slots, practiceDone) {
        const parts = String(prompt || '').split(BLANK_TOKEN_RE);
        const markers = String(prompt || '').match(BLANK_TOKEN_RE) || [];
        let slotIndex = 0;
        let html = '';
        parts.forEach((part, partIndex) => {
            if (part) html += `<span class="fill-prompt-text">${mathText(part)}</span>`;
            if (partIndex < markers.length) {
                const value = String(slots[slotIndex] || '').trim();
                const chipHtml = value
                    ? `<button type="button" class="drag-chip fill-slot-chip" data-chip-value="${escapeHtml(value)}" data-chip-id="${escapeHtml(`${key}-slot-${slotIndex}`)}" ${practiceDone ? 'disabled' : ''}>${escapeHtml(value)}</button>`
                    : '<span class="fill-slot-placeholder">nhấn để điền</span>';
                const slotAttrs = practiceDone ? '' : ' role="button" tabindex="0"';
                html += `<span class="fill-drop-slot" data-fill-key="${escapeHtml(key)}" data-slot-index="${slotIndex}" data-drop-slot="1"${slotAttrs}>${chipHtml}</span>`;
                slotIndex += 1;
            }
        });
        return html;
    }

    function renderFillExercises(lesson) {
        const items = Array.isArray(lesson.fill_exercises) ? lesson.fill_exercises : [];
        if (!items.length) return '';
        const ui = currentUiState(lesson);
        const practiceDone = !!ui.practiceDone;
        const savedAnswers = ui.fillAnswers || {};
        return items.map((item, index) => {
            const normalized = normalizeFillExercise(item);
            const key = normalized.id || item.id || `fill_${index + 1}`;
            const slots = normalizeFillSlots(savedAnswers[key], normalized.blankCount);
            const usedValues = slots.map(slot => normalizeAnswerText(slot)).filter(Boolean);
            const poolItems = seededShuffle(
                normalized.pool.filter(piece => !usedValues.includes(normalizeAnswerText(piece))),
                shuffleSeed(`${lesson.id}-fill-${key}`)
            );
            const ok = practiceDone && normalized.answers.length > 0
                && normalized.answers.every((answer, slotIndex) => essayAnswersEqual(slots[slotIndex], answer));
            const feedback = practiceDone
                ? (ok
                    ? '<span class="font-bold text-teal-700">Đúng.</span> Em đã kéo đúng vào các ô trống.'
                    : `<span class="font-bold text-rose-700">Chưa đúng.</span> Đáp án mẫu: ${normalized.answers.map(part => mathText(part)).join(' · ')}`)
                : '';
            const dragDisabled = practiceDone ? 'pointer-events-none opacity-80' : '';
            return `
                <article class="practice-card practice-card--fill fill-drag-card ${dragDisabled}" data-fill-card="${escapeHtml(key)}">
                    <div class="question-head practice-card-head">
                        ${renderPracticeQuestionMeta(index, 'Điền khuyết', 'fill')}
                        <div class="question-text practice-q-text fill-prompt-line">${renderPromptWithFillSlots(normalized.prompt, key, slots, practiceDone)}</div>
                    </div>
                    <div class="practice-card-content">
                        <p class="fill-pool-label practice-zone-label"><i class="fas fa-hand-pointer" aria-hidden="true"></i> Chọn mảnh rồi nhấn vào ô trống để điền</p>
                        <div class="drag-pool fill-chip-pool practice-chip-pool" data-fill-pool="${escapeHtml(key)}">
                            ${poolItems.map((piece, pieceIndex) => `<button type="button" class="drag-chip" data-chip-value="${escapeHtml(piece)}" data-chip-id="${escapeHtml(`${key}-pool-${pieceIndex}`)}" ${practiceDone ? 'disabled' : ''}>${escapeHtml(piece)}</button>`).join('')}
                        </div>
                        ${renderPracticeActions(`
                            ${renderPracticeCheckButton('fill-check-btn', 'data-fill-key', key, practiceDone)}
                            ${renderPracticeAiButton(normalized.prompt || '')}
                        `)}
                        ${renderPracticeFeedback('fill-feedback', feedback, practiceDone)}
                    </div>
                </article>
            `;
        }).join('');
    }

    function renderDragExercises(lesson) {
        const items = Array.isArray(lesson.drag_exercises) ? lesson.drag_exercises : [];
        if (!items.length) return '';
        const ui = currentUiState(lesson);
        const practiceDone = !!ui.practiceDone;
        return items.map((item, index) => {
            const normalized = normalizeDragExercise(item);
            const key = normalized.id || item.id || `drag_${index + 1}`;
            if (normalized.mode === 'match') {
                const savedMatches = normalizeMatchAnswers(ui.dragAnswers?.[key]);
                const pairedRight = new Set(Object.values(savedMatches).map(value => Number(value)));
                const ok = practiceDone && isMatchAnswerCorrect(normalized, savedMatches);
                const feedback = practiceDone
                    ? (ok
                        ? '<span class="font-bold text-teal-700">Đúng.</span> Em đã nối đủ các cặp.'
                        : `<span class="font-bold text-rose-700">Chưa đúng.</span> Hãy kiểm tra lại các cặp chưa khớp.`)
                    : '';
                const dragDisabled = practiceDone ? 'pointer-events-none opacity-80' : '';
                const matchSeed = shuffleSeed(`${lesson.id}-match-${key}`);
                const leftOrder = shuffledIndices(normalized.left.length, matchSeed);
                const rightOrder = shuffledIndices(normalized.right.length, matchSeed + 97);
                return `
                    <article class="practice-card practice-card--drag match-card ${dragDisabled}" data-match-card="${escapeHtml(key)}">
                        <div class="question-head practice-card-head">
                            ${renderPracticeQuestionMeta(index, 'Nối cặp', 'drag')}
                            <h3 class="question-text practice-q-text">${mathText(normalized.prompt || '')}</h3>
                        </div>
                        <div class="practice-card-content">
                        ${renderPracticeHint('Bấm mục bên trái, rồi bấm mục bên phải để nối cặp. Bấm lại để gỡ. Các mục hai bên được xáo trộn.')}
                        <div class="match-board" data-match-key="${escapeHtml(key)}">
                            <div class="match-col" data-match-side="left">
                                ${leftOrder.map(leftIndex => {
                                    const text = normalized.left[leftIndex];
                                    const rightIndex = savedMatches[leftIndex];
                                    const paired = Number.isFinite(Number(rightIndex));
                                    const pairNumber = paired ? Object.entries(savedMatches).findIndex(([left]) => Number(left) === leftIndex) + 1 : '';
                                    return `<button type="button" class="match-item ${paired ? 'is-paired' : ''}" data-match-side="left" data-match-index="${leftIndex}"${paired ? ` data-paired-right="${rightIndex}"` : ''} ${practiceDone ? 'disabled' : ''}>${pairNumber ? `<span class="match-pair-badge">${pairNumber}</span>` : ''}<span class="match-item-text">${mathText(text)}</span></button>`;
                                }).join('')}
                            </div>
                            <div class="match-col" data-match-side="right">
                                ${rightOrder.map(rightIndex => {
                                    const text = normalized.right[rightIndex];
                                    const paired = pairedRight.has(rightIndex);
                                    const pairNumber = paired ? Object.entries(savedMatches).findIndex(([, right]) => Number(right) === rightIndex) + 1 : '';
                                    return `<button type="button" class="match-item ${paired ? 'is-paired' : ''}" data-match-side="right" data-match-index="${rightIndex}" ${practiceDone ? 'disabled' : ''}>${pairNumber ? `<span class="match-pair-badge">${pairNumber}</span>` : ''}<span class="match-item-text">${mathText(text)}</span></button>`;
                                }).join('')}
                            </div>
                        </div>
                        ${renderPracticeActions(`
                            ${renderPracticeCheckButton('match-check-btn', 'data-match-key', key, practiceDone)}
                            ${renderPracticeAiButton(normalized.prompt || '')}
                        `)}
                        ${renderPracticeFeedback('drag-feedback', feedback, practiceDone)}
                        </div>
                    </article>
                `;
            }

            const savedOrder = Array.isArray(ui.dragAnswers?.[key]) ? ui.dragAnswers[key] : [];
            const poolItems = seededShuffle(
                normalized.items.filter(piece => !savedOrder.includes(piece)),
                shuffleSeed(`${lesson.id}-sort-${key}`)
            );
            const ok = practiceDone && isSortAnswerCorrect(normalized, savedOrder);
            const feedback = practiceDone
                ? (ok
                    ? '<span class="font-bold text-teal-700">Đúng.</span> Thứ tự đã khớp.'
                    : `<span class="font-bold text-rose-700">Chưa đúng.</span> Thứ tự đúng: ${escapeHtml(normalized.answer.join(' → '))}`)
                : '';
            const dragDisabled = practiceDone ? 'pointer-events-none opacity-80' : '';
            return `
                <article class="practice-card practice-card--drag sort-card ${dragDisabled}" data-sort-card="${escapeHtml(key)}">
                    <div class="question-head practice-card-head">
                        ${renderPracticeQuestionMeta(index, 'Sắp xếp', 'drag')}
                        <h3 class="question-text practice-q-text">${mathText(normalized.prompt || '')}</h3>
                    </div>
                    <div class="practice-card-content">
                        <p class="fill-pool-label sort-pool-label practice-zone-label"><i class="fas fa-layer-group" aria-hidden="true"></i> Kéo các mảnh vào hàng bên dưới theo thứ tự đúng</p>
                        <div class="drag-pool sort-chip-pool practice-chip-pool" data-sort-pool="${escapeHtml(key)}">
                            ${poolItems.map((piece, pieceIndex) => `<button type="button" class="drag-chip" data-chip-value="${escapeHtml(piece)}" data-chip-id="${escapeHtml(`${key}-pool-${pieceIndex}`)}" ${practiceDone ? 'disabled' : ''}>${escapeHtml(piece)}</button>`).join('')}
                        </div>
                        <p class="fill-pool-label sort-zone-label practice-zone-label practice-zone-label--answer"><i class="fas fa-arrow-down" aria-hidden="true"></i> Hàng trả lời</p>
                        <div class="drag-slot-row sort-slot-row sort-answer-zone practice-answer-zone" data-sort-zone="${escapeHtml(key)}">
                            ${savedOrder.length ? savedOrder.map((piece, pieceIndex) => `<button type="button" class="drag-chip" data-chip-value="${escapeHtml(piece)}" data-chip-id="${escapeHtml(`${key}-zone-${pieceIndex}`)}" ${practiceDone ? 'disabled' : ''}>${escapeHtml(piece)}</button>`).join('') : '<span class="sort-zone-placeholder">Kéo các mảnh từ khay phía trên xuống đây...</span>'}
                        </div>
                        ${renderPracticeActions(`
                            ${renderPracticeCheckButton('sort-check-btn', 'data-sort-key', key, practiceDone)}
                            ${renderPracticeAiButton(normalized.prompt || '')}
                        `)}
                        ${renderPracticeFeedback('drag-feedback', feedback, practiceDone)}
                    </div>
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

    const selfPracticeState = {
        lessonId: '',
        submissions: [],
        loading: false,
        loaded: false,
    };

    function normalizeSelfPracticeItem(item) {
        return normalizeExampleItem(item);
    }

    function ensureSelfPracticeStyles() {
        if (document.getElementById('lotrinhSelfPracticeStyles')) return;
        const style = document.createElement('style');
        style.id = 'lotrinhSelfPracticeStyles';
        style.textContent = `
            .self-practice-card { border-radius: 16px; border: 1px solid #e2e8f0; background: #fff; padding: 16px; box-shadow: 0 8px 24px rgba(15,23,42,.04); }
            .self-practice-upload { margin-top: 14px; border-radius: 14px; border: 2px dashed #cbd5e1; background: #f8fafc; padding: 14px; }
            .self-practice-upload.is-drag { border-color: #0f766e; background: #f0fdfa; }
            .self-practice-file-list { margin-top: 10px; display: flex; flex-direction: column; gap: 8px; }
            .self-practice-file-item { display: flex; align-items: center; gap: 10px; border: 1px solid #e2e8f0; border-radius: 10px; background: #fff; padding: 8px 10px; font-size: 12px; }
            .self-practice-history { margin-top: 12px; border-top: 1px solid #e2e8f0; padding-top: 10px; }
            .self-practice-history a { color: #0f766e; font-weight: 700; text-decoration: underline; }
        `;
        document.head.appendChild(style);
    }

    const SELF_PRACTICE_WHOLE_INDEX = -1;

    function submissionsForLessonSelfPractice() {
        return selfPracticeState.submissions.filter(row => Number(row.item_index) === SELF_PRACTICE_WHOLE_INDEX);
    }

    async function loadSelfPracticeSubmissions(lesson, force = false) {
        if (!lesson?.id) return;
        const lessonId = String(lesson.id);
        if (!force && selfPracticeState.loaded && selfPracticeState.lessonId === lessonId) return;
        selfPracticeState.loading = true;
        selfPracticeState.lessonId = lessonId;
        try {
            const data = await api(`api/lesson_self_practice.php?action=list&lesson_id=${encodeURIComponent(lessonId)}`);
            selfPracticeState.submissions = Array.isArray(data.submissions) ? data.submissions : [];
            selfPracticeState.loaded = true;
        } catch (err) {
            console.warn('Không tải bài tập:', err);
            selfPracticeState.submissions = [];
        } finally {
            selfPracticeState.loading = false;
        }
    }

    function renderSelfPracticeSubmissionHistory() {
        const rows = submissionsForLessonSelfPractice();
        if (!rows.length) return '';
        const row = rows[0];
        return `
            <div class="self-practice-history">
                <div class="text-xs font-bold uppercase tracking-wide text-slate-500 mb-2">Bài đã nộp</div>
                <div class="mb-2 text-sm text-slate-700">
                    <div class="text-xs text-slate-500">${escapeHtml(String(row.submitted_at || '').replace('T', ' ').slice(0, 16))}</div>
                    ${(row.files || []).map(file => `
                        <a href="${escapeHtml(file.view_url)}" target="_blank" rel="noopener" class="mr-3 inline-flex items-center gap-1">
                            <i class="fas fa-file"></i>${escapeHtml(file.original_name)}
                        </a>
                    `).join('')}
                    ${row.note ? `<div class="text-xs text-slate-500 mt-1">${escapeHtml(row.note)}</div>` : ''}
                </div>
            </div>
        `;
    }

    function renderSelfPracticeUploadForm(lesson, options = {}) {
        const canSubmit = !!options.canSubmit;
        const showForm = !!options.showForm;
        const alreadySubmitted = !!options.alreadySubmitted;
        if (!showForm) {
            return `<p class="text-sm text-slate-500"><i class="fab fa-google-drive mr-1"></i>Học sinh đăng nhập sẽ nộp bài làm lên Google Drive tại đây.</p>`;
        }
        if (!canSubmit) {
            return `<p class="text-sm text-amber-800"><i class="fab fa-google-drive mr-1"></i>Chế độ xem thử — học sinh mới nộp được bài làm thật.</p>`;
        }
        if (alreadySubmitted) {
            return `
                <div class="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-900">
                    <i class="fas fa-circle-check mr-1"></i>Em đã nộp bài cho bài học này. Giáo viên sẽ xem trên Google Drive.
                </div>
                ${renderSelfPracticeSubmissionHistory()}
            `;
        }
        const key = 'self_practice_whole';
        return `
            <div class="self-practice-upload" data-self-practice-drop="${key}">
                <label class="block cursor-pointer text-center">
                    <input type="file" class="hidden" data-self-practice-input="${key}" multiple accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.jpg,.jpeg,.png,.zip,.rar,.txt">
                    <div class="mx-auto grid h-10 w-10 place-items-center rounded-lg bg-teal-50 text-teal-700"><i class="fas fa-cloud-arrow-up"></i></div>
                    <p class="mt-2 text-sm font-bold text-slate-800">Chọn tệp bài làm hoặc kéo thả vào đây</p>
                    <p class="mt-1 text-xs text-slate-500">Gộp tất cả dạng vào một lần nộp · tối đa 10 tệp · 25 MB/tệp · lưu Google Drive</p>
                </label>
                <div class="self-practice-file-list" data-self-practice-file-list="${key}"></div>
                <label class="mt-3 block text-xs font-bold text-slate-600">Ghi chú (không bắt buộc)
                    <textarea rows="2" class="mt-1 w-full rounded border border-slate-300 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-teal-500" data-self-practice-note="${key}" placeholder="Ví dụ: Em nộp bài làm đầy đủ các dạng"></textarea>
                </label>
                <button type="button" class="mt-3 inline-flex items-center gap-2 rounded bg-teal-700 px-4 py-2 text-sm font-bold text-white hover:bg-teal-800" data-self-practice-submit="${key}">
                    <i class="fas fa-paper-plane"></i> Nộp bài cho giáo viên
                </button>
                <div class="mt-2 hidden text-sm font-semibold text-rose-700" data-self-practice-error="${key}"></div>
            </div>
        `;
    }

    function bindSelfPracticeUploads(lesson) {
        if (!lesson || (isTeacher() && !isTeacherPreview())) return;
        const canSubmit = !isTeacher();
        document.querySelectorAll('[data-self-practice-input]').forEach(input => {
            const key = input.dataset.selfPracticeInput;
            const list = document.querySelector(`[data-self-practice-file-list="${key}"]`);
            const renderFiles = () => {
                if (!list) return;
                const files = [...input.files];
                list.innerHTML = files.map(file => `
                    <div class="self-practice-file-item">
                        <span class="grid h-8 w-8 place-items-center rounded bg-teal-50 text-teal-700"><i class="fas fa-file"></i></span>
                        <span class="min-w-0 flex-1 truncate font-semibold text-slate-800">${escapeHtml(file.name)}</span>
                        <span class="text-slate-400">${(file.size / 1024 / 1024).toFixed(2)} MB</span>
                    </div>
                `).join('');
            };
            input.onchange = renderFiles;
            const drop = document.querySelector(`[data-self-practice-drop="${key}"]`);
            if (drop) {
                ['dragenter', 'dragover'].forEach(name => drop.addEventListener(name, e => {
                    e.preventDefault();
                    drop.classList.add('is-drag');
                }));
                ['dragleave', 'drop'].forEach(name => drop.addEventListener(name, e => {
                    e.preventDefault();
                    drop.classList.remove('is-drag');
                }));
                drop.addEventListener('drop', e => {
                    if (!canSubmit) return;
                    input.files = e.dataTransfer.files;
                    renderFiles();
                });
            }
        });

        document.querySelectorAll('[data-self-practice-submit]').forEach(button => {
            button.onclick = async () => {
                if (!canSubmit) return;
                const key = button.dataset.selfPracticeSubmit;
                const input = document.querySelector(`[data-self-practice-input="${key}"]`);
                const noteEl = document.querySelector(`[data-self-practice-note="${key}"]`);
                const errorEl = document.querySelector(`[data-self-practice-error="${key}"]`);
                const files = input?.files ? [...input.files] : [];
                if (!files.length) {
                    if (errorEl) {
                        errorEl.textContent = 'Vui lòng chọn ít nhất một tệp.';
                        errorEl.classList.remove('hidden');
                    }
                    return;
                }
                const old = button.innerHTML;
                button.disabled = true;
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang gửi...';
                if (errorEl) errorEl.classList.add('hidden');
                const form = new FormData();
                form.append('action', 'submit');
                form.append('lesson_id', String(lesson.id));
                form.append('item_index', String(SELF_PRACTICE_WHOLE_INDEX));
                form.append('note', String(noteEl?.value || '').trim());
                files.forEach(file => form.append('files[]', file));
                try {
                    const res = await fetch('api/lesson_self_practice.php', { method: 'POST', body: form, credentials: 'include', cache: 'no-store' });
                    const data = await res.json().catch(() => ({}));
                    if (!res.ok) throw new Error(data.error || 'Không nộp được bài.');
                    selfPracticeState.loaded = false;
                    await loadSelfPracticeSubmissions(lesson, true);
                    renderSelfPractice(lesson);
                } catch (err) {
                    if (errorEl) {
                        errorEl.textContent = err.message || 'Không nộp được bài.';
                        errorEl.classList.remove('hidden');
                    }
                } finally {
                    button.disabled = false;
                    button.innerHTML = old;
                }
            };
        });
    }

    async function renderSelfPractice(lesson) {
        ensureSelfPracticeStyles();
        const items = Array.isArray(lesson.self_practice) ? lesson.self_practice : [];
        const canSubmit = !isTeacher();
        const showForm = canSubmit || isTeacherPreview();
        if (canSubmit) {
            els.tabContent.innerHTML = '<div class="rounded border border-dashed border-slate-200 bg-slate-50 p-6 text-sm text-slate-500"><i class="fas fa-circle-notch fa-spin mr-2"></i>Đang tải bài tập...</div>';
            await loadSelfPracticeSubmissions(lesson);
        }
        const alreadySubmitted = canSubmit && submissionsForLessonSelfPractice().length > 0;
        els.tabContent.innerHTML = `
            <div class="space-y-4">
                <div class="rounded-lg border border-sky-100 bg-sky-50 px-4 py-3 text-sm text-sky-900">
                    <i class="fas fa-cloud-arrow-up mr-1"></i> Đọc các dạng bài bên dưới, làm xong rồi <strong>nộp chung một lần</strong> — tệp được lưu lên Google Drive để giáo viên xem.
                </div>
                ${items.length ? items.map((raw, index) => {
                    const item = normalizeSelfPracticeItem(raw);
                    return `
                    <article class="self-practice-card lesson-document">
                        <h3 class="font-bold text-slate-900">${richText(item.title)}</h3>
                        <div class="lesson-paragraph mt-2 text-base leading-7 text-slate-700">${richText(item.body)}</div>
                        ${item.ai ? `
                        <button type="button" class="ai-explain-btn mt-3" data-ai-type="self_practice" data-ai-index="${index}" data-ai-text="${escapeHtml(normalizeDisplayText(`${item.title}\n${item.body}`))}">
                            <i class="fas fa-wand-magic-sparkles"></i> AI giải thích
                        </button>
                        ` : ''}
                    </article>
                `;
                }).join('') : '<div class="rounded border border-slate-200 bg-white p-4 muted-note">Giáo viên chưa nhập bài tập nộp cho bài này.</div>'}
                ${items.length ? `
                <section class="self-practice-card">
                    <h3 class="font-bold text-slate-900"><i class="fas fa-paper-plane text-teal-700 mr-1"></i> Nộp bài cho giáo viên</h3>
                    <p class="mt-1 text-sm text-slate-600">Chọn một hoặc nhiều tệp chứa toàn bộ bài làm (mỗi bài học chỉ nộp một lần).</p>
                    ${renderSelfPracticeUploadForm(lesson, { canSubmit, showForm, alreadySubmitted })}
                </section>
                ` : ''}
            </div>
        `;
        bindAiExplainButtons(lesson);
        bindSelfPracticeUploads(lesson);
        typesetMath();
    }

    const aiAssistState = {
        selectionToolbar: null,
        selectionTimer: null,
        chatHistory: [],
        chatLessonId: '',
        chatBusy: false,
        bound: false
    };

    function canUseStudentAiAssist() {
        return !isTeacher() || isTeacherPreview();
    }

    function lessonAiPayload(lesson, extra = {}) {
        return {
            lesson_id: lesson?.id ? Number(lesson.id) : 0,
            subject: lesson?.subject || PAGE_SUBJECT,
            lesson_title: lesson?.title || PAGE_TITLE,
            ...extra
        };
    }

    function lessonContextText(lesson) {
        if (!lesson) return '';
        const theory = Array.isArray(lesson.theory) ? lesson.theory.join('\n') : '';
        const examples = Array.isArray(lesson.examples)
            ? lesson.examples.map(item => `${item.title || ''}\n${item.body || ''}`).join('\n')
            : '';
        return [lesson.goal_text || '', theory, examples]
            .filter(Boolean)
            .join('\n\n')
            .replace(/\[\[?AI\]\]?/g, '')
            .slice(0, 2200);
    }

    async function requestAiExplain(lesson, text) {
        return api('api/ai_explain.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(lessonAiPayload(lesson, {
                text,
                lesson_context: lessonContextText(lesson)
            }))
        });
    }

    async function requestAiChat(lesson, question, history = []) {
        return api('api/ai_explain.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(lessonAiPayload(lesson, {
                mode: 'chat',
                question,
                lesson_context: lessonContextText(lesson),
                history
            }))
        });
    }

    function ensurePracticeStyles() {
        if (document.getElementById('lotrinhPracticeStyles')) return;
        const style = document.createElement('style');
        style.id = 'lotrinhPracticeStyles';
        style.textContent = `
            .practice-workspace { display: flex; flex-direction: column; gap: 18px; }
            .practice-parts-stack { display: flex; flex-direction: column; gap: 22px; }
            .practice-part {
                border-radius: 20px;
                border: 1px solid #e2e8f0;
                background: #fff;
                box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
                overflow: hidden;
            }
            .practice-part-head {
                display: flex;
                gap: 14px;
                align-items: flex-start;
                padding: 18px 20px;
                border-bottom: 1px solid rgba(148, 163, 184, 0.25);
            }
            .practice-part--essay .practice-part-head { background: linear-gradient(135deg, #fffbeb 0%, #fff 72%); }
            .practice-part--fill .practice-part-head { background: linear-gradient(135deg, #f5f3ff 0%, #fff 72%); }
            .practice-part--drag .practice-part-head { background: linear-gradient(135deg, #f0f9ff 0%, #fff 72%); }
            .practice-part--choice .practice-part-head { background: linear-gradient(135deg, #f0fdfa 0%, #fff 72%); }
            .practice-part-icon {
                width: 46px;
                height: 46px;
                flex: 0 0 46px;
                display: grid;
                place-items: center;
                border-radius: 14px;
                font-size: 1.05rem;
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.65);
            }
            .practice-part--essay .practice-part-icon { background: #fde68a; color: #b45309; }
            .practice-part--fill .practice-part-icon { background: #ddd6fe; color: #6d28d9; }
            .practice-part--drag .practice-part-icon { background: #bae6fd; color: #0369a1; }
            .practice-part--choice .practice-part-icon { background: #99f6e4; color: #0f766e; }
            .practice-part-intro { min-width: 0; flex: 1; }
            .practice-part-title-row {
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                gap: 10px;
            }
            .practice-part-title {
                margin: 0;
                font-size: 0.95rem;
                font-weight: 800;
                letter-spacing: 0.03em;
                text-transform: uppercase;
                color: #0f172a;
            }
            .practice-part-count {
                display: inline-flex;
                align-items: center;
                padding: 4px 10px;
                border-radius: 999px;
                background: rgba(255,255,255,0.85);
                border: 1px solid rgba(148,163,184,0.35);
                font-size: 0.72rem;
                font-weight: 800;
                color: #475569;
            }
            .practice-part-note {
                margin: 8px 0 0;
                font-size: 0.8rem;
                line-height: 1.55;
                color: #92400e;
            }
            .practice-part-body {
                display: flex;
                flex-direction: column;
                gap: 16px;
                padding: 16px;
                background: linear-gradient(180deg, #fafbfc 0%, #fff 100%);
            }
            .practice-card {
                border-radius: 16px;
                border: 1px solid #dbe3ef;
                background: #fff;
                overflow: hidden;
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
                transition: transform 0.18s ease, box-shadow 0.18s ease;
            }
            .practice-card:hover {
                transform: translateY(-1px);
                box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
            }
            .practice-card--essay { border-top: 3px solid #f59e0b; }
            .practice-card--fill { border-top: 3px solid #8b5cf6; }
            .practice-card--drag { border-top: 3px solid #0ea5e9; }
            .practice-card--choice { border-top: 3px solid #0f766e; }
            .practice-card-head {
                padding: 16px 18px 14px;
                border-bottom: 1px solid #e8edf3;
                background: linear-gradient(180deg, #f8fafc 0%, #fff 100%);
            }
            .practice-card-meta {
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                gap: 8px;
                margin-bottom: 10px;
            }
            .practice-q-badge,
            .practice-type-chip {
                display: inline-flex;
                align-items: center;
                padding: 5px 11px;
                border-radius: 999px;
                font-size: 0.72rem;
                font-weight: 800;
                letter-spacing: 0.02em;
            }
            .practice-q-badge--essay { background: #fef3c7; color: #b45309; }
            .practice-q-badge--fill { background: #ede9fe; color: #6d28d9; }
            .practice-q-badge--drag { background: #e0f2fe; color: #0369a1; }
            .practice-q-badge--choice { background: #ccfbf1; color: #0f766e; }
            .practice-type-chip {
                border: 1px solid rgba(148,163,184,0.28);
                background: #fff;
                color: #475569;
            }
            .practice-q-text {
                margin: 0;
                font-size: 1rem;
                font-weight: 700;
                line-height: 1.75;
                color: #0f172a;
            }
            .practice-card-content { padding-bottom: 2px; }
            .practice-hint {
                display: flex;
                gap: 10px;
                align-items: flex-start;
                margin: 14px 18px 0;
                padding: 12px 14px;
                border-radius: 12px;
                border: 1px solid #fde68a;
                background: #fffbeb;
                font-size: 0.84rem;
                line-height: 1.55;
                color: #78350f;
            }
            .practice-hint i {
                margin-top: 2px;
                color: #d97706;
            }
            .practice-zone-label {
                display: flex;
                align-items: center;
                gap: 8px;
                margin: 14px 18px 8px !important;
                font-size: 0.82rem !important;
                font-weight: 800 !important;
                color: #475569 !important;
            }
            .practice-zone-label--answer { color: #0f766e !important; }
            .practice-chip-pool,
            .practice-answer-zone {
                margin-left: 18px !important;
                margin-right: 18px !important;
            }
            .practice-answer-zone {
                border-width: 2px;
                border-style: dashed;
                border-color: #5eead4;
                background: linear-gradient(180deg, #f0fdfa 0%, #fff 100%);
            }
            .practice-card-actions {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 14px;
                padding: 14px 18px 16px;
                border-top: 1px solid #e8edf3;
                background: #f8fafc;
            }
            .practice-btn {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 0.86rem;
                font-weight: 800;
                line-height: 1;
                cursor: pointer;
                transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease, border-color 0.15s ease;
            }
            .practice-btn:hover { transform: translateY(-1px); }
            .practice-btn--primary,
            .practice-btn--submit {
                border: 0;
                background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
                color: #fff;
                box-shadow: 0 8px 18px rgba(15, 118, 110, 0.22);
            }
            .practice-btn--primary:hover,
            .practice-btn--submit:hover {
                box-shadow: 0 10px 22px rgba(15, 118, 110, 0.28);
            }
            .practice-btn--ghost {
                border: 1px solid #cbd5e1;
                background: #fff;
                color: #334155;
            }
            .practice-btn--ghost:hover {
                border-color: #94a3b8;
                background: #f8fafc;
            }
            .practice-feedback {
                margin: 0 18px 16px;
                padding: 14px 16px;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                border-left: 4px solid #0f766e;
                background: #f8fafc;
                font-size: 0.88rem;
                line-height: 1.65;
            }
            .practice-answer-grid { padding: 14px 16px 18px !important; }
            .practice-status-banner {
                display: flex;
                gap: 14px;
                align-items: flex-start;
                padding: 16px 18px;
                border-radius: 16px;
                border: 1px solid #99f6e4;
                background: linear-gradient(135deg, #f0fdfa 0%, #fff 70%);
                box-shadow: 0 8px 20px rgba(15, 118, 110, 0.08);
            }
            .practice-status-banner--done {
                border-color: #5eead4;
            }
            .practice-status-banner--active {
                border-color: #fcd34d;
                background: linear-gradient(135deg, #fffbeb 0%, #fff 70%);
            }
            .practice-status-icon {
                width: 40px;
                height: 40px;
                flex: 0 0 40px;
                display: grid;
                place-items: center;
                border-radius: 12px;
                background: #ccfbf1;
                color: #0f766e;
                font-size: 1rem;
            }
            .practice-status-banner--active .practice-status-icon {
                background: #fde68a;
                color: #b45309;
            }
            .practice-status-title {
                margin: 0;
                font-size: 0.95rem;
                font-weight: 800;
                color: #0f172a;
            }
            .practice-status-text {
                margin: 4px 0 0;
                font-size: 0.86rem;
                line-height: 1.6;
                color: #475569;
            }
            .practice-submit-bar {
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                position: sticky;
                bottom: 12px;
                z-index: 5;
                padding: 14px 16px;
                border-radius: 16px;
                border: 1px solid #dbe3ef;
                background: rgba(255,255,255,0.96);
                backdrop-filter: blur(8px);
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.1);
            }
            .practice-empty-note {
                padding: 18px;
                border-radius: 14px;
                border: 1px dashed #cbd5e1;
                background: #f8fafc;
                color: #64748b;
                font-size: 0.9rem;
                line-height: 1.6;
            }
            .essay-input {
                width: calc(100% - 36px) !important;
                margin: 14px 18px 0 !important;
                border-radius: 12px !important;
                font-size: 1.05rem !important;
                font-weight: 700 !important;
            }
            .fill-prompt-line { margin: 0 !important; }
            .drag-chip.chip-selected {
                outline: 3px solid #0f766e;
                background: #ecfdf5 !important;
                box-shadow: 0 0 0 4px rgba(15, 118, 110, 0.18);
            }
            .fill-drop-slot.is-drop-ready,
            .drag-pool.is-drop-ready,
            .drag-slot-row.is-drop-ready {
                border-color: #0f766e;
                background: #ecfdf5;
                box-shadow: inset 0 0 0 2px rgba(15, 118, 110, 0.12);
            }
            .touch-placement .drag-chip,
            .touch-placement .fill-drop-slot,
            .touch-placement .drag-pool,
            .touch-placement .drag-slot-row {
                touch-action: manipulation;
                -webkit-tap-highlight-color: rgba(15, 118, 110, 0.12);
                -webkit-user-select: none;
                user-select: none;
            }
            .touch-placement .drag-chip {
                min-height: 44px;
                padding: 10px 16px;
                cursor: pointer;
            }
            .touch-placement .fill-drop-slot,
            .touch-placement .drag-pool,
            .touch-placement .drag-slot-row {
                min-height: 52px;
            }
            .touch-placement .fill-drop-slot:not(:has(.fill-slot-chip)),
            .touch-placement .drag-slot-row:has(.sort-zone-placeholder) {
                cursor: pointer;
            }
            @media (pointer: coarse), (hover: none) {
                .drag-chip {
                    min-height: 44px;
                    padding: 10px 16px;
                    touch-action: manipulation;
                    -webkit-user-select: none;
                    user-select: none;
                }
                .fill-drop-slot,
                .drag-pool,
                .drag-slot-row {
                    min-height: 52px;
                    touch-action: manipulation;
                }
                .fill-drop-slot:not(:has(.fill-slot-chip)),
                .drag-slot-row:has(.sort-zone-placeholder) {
                    cursor: pointer;
                }
            }
            @media (max-width: 640px) {
                .practice-part-head,
                .practice-card-head,
                .practice-card-actions,
                .practice-submit-bar { padding-left: 14px; padding-right: 14px; }
                .practice-hint,
                .practice-feedback,
                .practice-chip-pool,
                .practice-answer-zone { margin-left: 14px !important; margin-right: 14px !important; }
            }
        `;
        document.head.appendChild(style);
    }

    function ensureStudentAiAssistStyles() {
        if (document.getElementById('lotrinhStudentAiAssistStyles')) return;
        const style = document.createElement('style');
        style.id = 'lotrinhStudentAiAssistStyles';
        style.textContent = `
            .ai-selection-toolbar {
                position: fixed;
                z-index: 9999;
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 10px;
                border: 1px solid #fcd34d;
                border-radius: 999px;
                background: #fffbeb;
                box-shadow: 0 10px 24px rgba(146, 64, 14, 0.18);
                animation: aiBubbleIn 0.16s ease;
                user-select: none;
            }
            .ai-selection-toolbar button {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                border: 0;
                border-radius: 999px;
                background: #fde68a;
                color: #92400e;
                font-size: 0.78rem;
                font-weight: 700;
                padding: 6px 12px;
                cursor: pointer;
            }
            .ai-selection-toolbar button:hover { background: #fcd34d; }
            .ai-selection-toolbar button:disabled { opacity: 0.7; cursor: wait; }
            #lessonRightAside {
                align-self: start;
            }
            .lesson-ai-chat-aside {
                display: flex;
                flex-direction: column;
                min-height: 420px;
                max-height: min(82vh, 680px);
                border-color: #99f6e4;
                background: linear-gradient(180deg, #f0fdfa 0%, #fff 28%);
            }
            .lesson-ai-chat-aside.is-hidden { display: none !important; }
            .lesson-ai-chat-head {
                padding-bottom: 8px;
                border-bottom: 1px solid #ccfbf1;
            }
            .lesson-ai-chat-head strong {
                display: block;
                color: #115e59;
                font-size: 0.88rem;
            }
            .lesson-ai-chat-head p {
                color: #0f766e;
                font-size: 0.72rem;
                margin-top: 4px;
                line-height: 1.4;
            }
            .lesson-ai-chat-hint {
                margin-top: 6px;
                font-size: 0.68rem;
                line-height: 1.45;
                color: #64748b;
            }
            .lesson-ai-chat-messages {
                flex: 1;
                min-height: 180px;
                overflow-y: auto;
                margin-top: 10px;
                padding: 8px 4px;
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .lesson-ai-chat-msg {
                max-width: 100%;
                padding: 8px 10px;
                border-radius: 10px;
                font-size: 0.82rem;
                line-height: 1.65;
                word-break: break-word;
            }
            .lesson-ai-chat-msg.user {
                align-self: flex-end;
                max-width: 92%;
                background: #dbeafe;
                color: #1e3a8a;
                border: 1px solid #bfdbfe;
            }
            .lesson-ai-chat-msg.assistant {
                align-self: flex-start;
                background: #fffbeb;
                color: #334155;
                border: 1px solid #fde68a;
            }
            .lesson-ai-chat-msg.error {
                background: #fef2f2;
                color: #b91c1c;
                border: 1px solid #fecaca;
            }
            .lesson-ai-chat-compose {
                display: flex;
                flex-direction: column;
                gap: 8px;
                margin-top: 10px;
                padding-top: 10px;
                border-top: 1px solid #e2e8f0;
            }
            .lesson-ai-chat-compose textarea {
                width: 100%;
                min-height: 56px;
                max-height: 120px;
                resize: vertical;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                padding: 8px 10px;
                font-size: 0.84rem;
                outline: none;
            }
            .lesson-ai-chat-compose textarea:focus {
                border-color: #14b8a6;
                box-shadow: 0 0 0 2px rgba(20, 184, 166, 0.15);
            }
            .lesson-ai-chat-send {
                border: 0;
                border-radius: 10px;
                background: #0f766e;
                color: #fff;
                font-weight: 700;
                font-size: 0.82rem;
                padding: 10px 12px;
                cursor: pointer;
            }
            .lesson-ai-chat-send:disabled { opacity: 0.6; cursor: wait; }
        `;
        document.head.appendChild(style);
    }

    function hideAiSelectionToolbar() {
        aiAssistState.selectionToolbar?.remove();
        aiAssistState.selectionToolbar = null;
    }

    function positionAiSelectionToolbar(toolbar, rect) {
        const margin = 8;
        toolbar.style.position = 'fixed';
        toolbar.style.display = 'inline-flex';
        toolbar.style.visibility = 'hidden';
        document.body.appendChild(toolbar);
        const width = toolbar.offsetWidth;
        const height = toolbar.offsetHeight;
        let top = rect.top - height - margin;
        let left = rect.left + rect.width / 2 - width / 2;
        if (top < margin) top = rect.bottom + margin;
        left = Math.max(margin, Math.min(left, window.innerWidth - width - margin));
        toolbar.style.top = `${top}px`;
        toolbar.style.left = `${left}px`;
        toolbar.style.visibility = 'visible';
    }

    async function runAiExplainFromSelection(selectedText, anchorHost) {
        const lesson = currentLesson();
        if (!lesson || !selectedText) return;
        hideAiSelectionToolbar();
        window.getSelection()?.removeAllRanges();

        const anchor = document.createElement('div');
        anchor.className = 'ai-selection-anchor';
        anchor.style.marginTop = '12px';
        (anchorHost || els.tabContent)?.appendChild(anchor);

        showAiModal('<p class="text-slate-500"><i class="fas fa-spinner fa-spin"></i> AI đang giải thích...</p>', anchor);
        try {
            const data = await requestAiExplain(lesson, selectedText);
            showAiModal(renderAiAnswer(data.answer || '') + formatAiCacheNote(data), anchor);
            anchor.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        } catch (err) {
            showAiModal(formatAiErrorHtml(err), anchor);
            anchor.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }
    }

    function showAiSelectionToolbar(selectedText, rect, anchorHost) {
        hideAiSelectionToolbar();
        const toolbar = document.createElement('div');
        toolbar.className = 'ai-selection-toolbar';
        toolbar.innerHTML = '<button type="button"><i class="fas fa-wand-magic-sparkles"></i> AI giải thích</button>';
        const button = toolbar.querySelector('button');
        toolbar.addEventListener('mousedown', event => event.preventDefault());
        button.onclick = async event => {
            event.preventDefault();
            event.stopPropagation();
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang hỏi...';
            await runAiExplainFromSelection(selectedText, anchorHost);
        };
        positionAiSelectionToolbar(toolbar, rect);
        aiAssistState.selectionToolbar = toolbar;
    }

    function isSelectableAiRegion(node) {
        return !!node?.closest?.('#tabContent');
    }

    function handleLessonTextSelection() {
        if (!canUseStudentAiAssist()) return hideAiSelectionToolbar();
        const active = document.activeElement;
        if (active?.matches('.essay-input, #lessonAiChatInput, input, textarea, select, [contenteditable="true"]')) {
            return hideAiSelectionToolbar();
        }
        const selection = window.getSelection();
        if (!selection || selection.isCollapsed || selection.rangeCount === 0) return hideAiSelectionToolbar();

        const selectedText = String(selection.toString() || '').replace(/\s+/g, ' ').trim();
        if (selectedText.length < 2) return hideAiSelectionToolbar();

        const range = selection.getRangeAt(0);
        const anchorNode = range.commonAncestorContainer.nodeType === Node.TEXT_NODE
            ? range.commonAncestorContainer.parentElement
            : range.commonAncestorContainer;
        if (!isSelectableAiRegion(anchorNode)) return hideAiSelectionToolbar();
        if (anchorNode.closest('.lesson-ai-chat-aside, .ai-selection-toolbar, .ai-chat-bubble, button, input, textarea, select, .tab-btn')) {
            return hideAiSelectionToolbar();
        }

        const rect = range.getBoundingClientRect();
        if (!rect.width && !rect.height) return hideAiSelectionToolbar();
        const anchorHost = anchorNode.closest('.lesson-theory-flow, .lesson-explain-block, .practice-card, .lesson-document') || els.tabContent;
        showAiSelectionToolbar(selectedText, rect, anchorHost);
    }

    function renderLessonChatMessages() {
        const box = document.getElementById('lessonAiChatMessages');
        if (!box) return;
        if (!aiAssistState.chatHistory.length) {
            box.innerHTML = '<div class="lesson-ai-chat-msg assistant">Em có thể hỏi về khái niệm, công thức hoặc cách làm bài trong bài học này.</div>';
            return;
        }
        box.innerHTML = aiAssistState.chatHistory.map(msg => `
            <div class="lesson-ai-chat-msg ${msg.role === 'error' ? 'error' : msg.role}">
                ${msg.role === 'assistant' ? renderAiAnswer(msg.content) : escapeHtml(msg.content)}
                ${msg.role === 'assistant' && msg.cached ? '<div class="mt-1 text-[11px] font-semibold text-sky-700"><i class="fas fa-database mr-1"></i>Đã lưu từ trước</div>' : ''}
            </div>
        `).join('');
        box.scrollTop = box.scrollHeight;
        typesetMath();
    }

    function bindLessonChatForm() {
        const form = document.getElementById('lessonAiChatForm');
        if (!form || form.dataset.bound === '1') return;
        form.dataset.bound = '1';
        form.addEventListener('submit', async event => {
            event.preventDefault();
            if (aiAssistState.chatBusy) return;
            const lesson = currentLesson();
            const input = document.getElementById('lessonAiChatInput');
            const sendBtn = document.getElementById('lessonAiChatSend');
            const question = String(input?.value || '').trim();
            if (!lesson || !question) return;

            aiAssistState.chatBusy = true;
            sendBtn.disabled = true;
            aiAssistState.chatHistory.push({ role: 'user', content: question });
            input.value = '';
            renderLessonChatMessages();
            aiAssistState.chatHistory.push({ role: 'assistant', content: 'Đang suy nghĩ...' });
            renderLessonChatMessages();

            try {
                const history = aiAssistState.chatHistory.slice(0, -2);
                const data = await requestAiChat(lesson, question, history);
                aiAssistState.chatHistory.pop();
                aiAssistState.chatHistory.push({
                    role: 'assistant',
                    content: data.answer || '',
                    cached: !!data.cached,
                });
            } catch (err) {
                aiAssistState.chatHistory.pop();
                aiAssistState.chatHistory.push({ role: 'error', content: formatAiErrorMessage(err) });
            } finally {
                aiAssistState.chatBusy = false;
                sendBtn.disabled = false;
                renderLessonChatMessages();
                input.focus();
            }
        });
    }

    function ensureLessonChatbot() {
        ensureStudentAiAssistStyles();
        const mount = els.lessonAiChatAside || document.getElementById('lessonAiChatAside');
        if (!mount) return;

        if (!document.getElementById('lessonAiChatForm')) {
            mount.innerHTML = `
                <div class="lesson-ai-chat-head">
                    <strong><i class="fas fa-comments text-teal-700 mr-1"></i> Hỏi đáp cùng AI</strong>
                    <p id="lessonAiChatLessonLabel">Đang tải bài...</p>
                    <p class="lesson-ai-chat-hint">Bôi đen đoạn → <strong>AI giải thích</strong>, hoặc hỏi bên dưới.</p>
                </div>
                <div id="lessonAiChatMessages" class="lesson-ai-chat-messages"></div>
                <form id="lessonAiChatForm" class="lesson-ai-chat-compose">
                    <textarea id="lessonAiChatInput" rows="3" placeholder="Ví dụ: Tập hợp là gì?"></textarea>
                    <button type="submit" id="lessonAiChatSend" class="lesson-ai-chat-send"><i class="fas fa-paper-plane mr-1"></i> Gửi câu hỏi</button>
                </form>
            `;
        }
        mount.dataset.ready = '1';
        bindLessonChatForm();
        renderLessonChatMessages();
    }

    function refreshStudentAiAssist(lesson) {
        const enabled = canUseStudentAiAssist();
        ensureLessonChatbot();
        const mount = els.lessonAiChatAside || document.getElementById('lessonAiChatAside');
        if (mount) mount.classList.toggle('is-hidden', !enabled);
        const label = document.getElementById('lessonAiChatLessonLabel');
        if (label) label.textContent = lesson?.title || PAGE_TITLE;
        const lessonId = String(lesson?.id || '');
        if (lessonId && lessonId !== aiAssistState.chatLessonId) {
            aiAssistState.chatLessonId = lessonId;
            aiAssistState.chatHistory = [];
            renderLessonChatMessages();
        }
        if (!enabled) hideAiSelectionToolbar();
    }

    function initStudentAiAssist() {
        if (aiAssistState.bound) return;
        aiAssistState.bound = true;
        ensureStudentAiAssistStyles();
        const scheduleSelectionCheck = () => {
            const active = document.activeElement;
            if (active?.matches('.essay-input, #lessonAiChatInput, input, textarea, select, [contenteditable="true"]')) {
                return hideAiSelectionToolbar();
            }
            window.clearTimeout(aiAssistState.selectionTimer);
            aiAssistState.selectionTimer = window.setTimeout(handleLessonTextSelection, 30);
        };
        document.addEventListener('mouseup', scheduleSelectionCheck);
        document.addEventListener('touchend', scheduleSelectionCheck);
        document.addEventListener('selectionchange', scheduleSelectionCheck);
        document.addEventListener('keydown', event => {
            if (event.key === 'Escape') hideAiSelectionToolbar();
        });
        document.addEventListener('mousedown', event => {
            if (event.target.closest('.ai-selection-toolbar, #tabContent')) return;
            window.setTimeout(() => {
                const selection = window.getSelection();
                if (!selection || selection.isCollapsed) hideAiSelectionToolbar();
            }, 120);
        });

        // Tránh menu copy/paste đè lên toolbar AI trên Android/iOS
        if (els.tabContent) {
            els.tabContent.addEventListener('contextmenu', e => {
                if (isSelectableAiRegion(e.target)) {
                    e.preventDefault();
                }
            });
        }

        // Trên thiết bị chạm, toolbar AI nổi bật hơn và tránh xung đột
        if (prefersTouchPlacement()) {
            const style = document.createElement('style');
            style.textContent = `
                .ai-selection-toolbar {
                    font-size: 1rem;
                    padding: 8px 14px;
                    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
                }
                .ai-selection-toolbar button {
                    padding: 8px 16px;
                    font-size: 0.9rem;
                }
            `;
            document.head.appendChild(style);
        }
        ensureLessonChatbot();
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

        const host = anchorButton?.closest('.lesson-theory-flow, .lesson-explain-block, .practice-card, .lesson-document, .ai-selection-anchor') || anchorButton?.parentElement;
        if (host) {
            host.appendChild(bubble);
        } else {
            document.body.appendChild(bubble);
        }
        typesetMath();
    }

    async function triggerAiExplainButton(button, lesson, text) {
        const old = button.innerHTML;
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> AI đang giải thích...';
        try {
            const data = await requestAiExplain(lesson, text);
            showAiModal(renderAiAnswer(data.answer || '') + formatAiCacheNote(data), button);
        } catch (err) {
            showAiModal(formatAiErrorHtml(err), button);
        } finally {
            button.disabled = false;
            button.innerHTML = old;
        }
    }

    function bindAiExplainButtons(lesson) {
        document.querySelectorAll('.ai-explain-btn').forEach(button => {
            button.onclick = () => triggerAiExplainButton(button, lesson, button.dataset.aiText || '');
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
            await fetch('api/logout.php', { method: 'POST', cache: 'no-store', credentials: 'include' });
        } catch {
            // Still clear local state below.
        }
        localStorage.removeItem('authToken');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('userName');
        localStorage.removeItem('userRole');
        localStorage.removeItem('allowedPages');
        localStorage.removeItem('userClassName');
        localStorage.removeItem(LS_TAB_KEY);
        localStorage.removeItem(LS_LESSON_KEY);
        window.location.href = 'login.html';
    }

    if (els.logoutBtn) {
        els.logoutBtn.onclick = logout;
    }

    function renderMultipleChoiceExercises(lesson) {
        const questions = Array.isArray(lesson.questions) ? lesson.questions : [];
        if (!questions.length) return '';
        const ui = currentUiState(lesson);
        const practiceDone = !!ui.practiceDone;
        const answers = ui.answers || {};
        return questions.map((question, index) => `
            <article class="practice-card practice-card--choice">
                <div class="question-head practice-card-head">
                    ${renderPracticeQuestionMeta(index, 'Trắc nghiệm', 'choice')}
                    <h3 class="question-text practice-q-text">${mathText(question.prompt)}</h3>
                </div>
                <div class="answer-grid practice-answer-grid">
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
        `).join('');
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
        const hasAnyPractice = essayExercises.length || fillExercises.length || dragExercises.length || questions.length;

        const practiceParts = [
            essayExercises.length
                ? renderPracticePart(
                    'Phần Bài tập tự luận',
                    'fa-pen-nib',
                    renderEssayExercises(lesson),
                    essayExercises.length,
                    'Mỗi câu chỉ nhập <strong>kết quả là số</strong>. Không nhập lời giải, công thức hay đáp án dạng chữ.',
                    'essay'
                )
                : '',
            fillExercises.length
                ? renderPracticePart('Phần Bài tập điền khuyết', 'fa-i-cursor', renderFillExercises(lesson), fillExercises.length, '', 'fill')
                : '',
            dragExercises.length
                ? renderPracticePart('Phần Bài tập kéo thả', 'fa-hand-pointer', renderDragExercises(lesson), dragExercises.length, '', 'drag')
                : '',
            questions.length
                ? renderPracticePart('Phần Bài tập trắc nghiệm', 'fa-list-check', renderMultipleChoiceExercises(lesson), questions.length, '', 'choice')
                : ''
        ].filter(Boolean).join('');

        els.tabContent.innerHTML = `
            <form id="practiceForm" class="practice-workspace">
                ${practiceDone ? `
                    <div class="practice-status-banner practice-status-banner--done">
                        <div class="practice-status-icon"><i class="fas fa-circle-check" aria-hidden="true"></i></div>
                        <div>
                            <p class="practice-status-title">Đã nộp bài luyện tập</p>
                            <p class="practice-status-text">${practiceScore !== null ? `Điểm luyện tập: <strong>${practiceScore}%</strong>. ` : ''}Các đáp án đúng/sai được hiển thị bên dưới. Bấm <strong>Làm lại bài luyện</strong> nếu muốn làm vòng mới.</p>
                        </div>
                    </div>
                ` : `
                    <div class="practice-status-banner practice-status-banner--active">
                        <div class="practice-status-icon"><i class="fas fa-dumbbell" aria-hidden="true"></i></div>
                        <div>
                            <p class="practice-status-title">Luyện tập bài học</p>
                            <p class="practice-status-text">Làm lần lượt từng dạng bài bên dưới. Có thể bấm <strong>Kiểm tra đáp án</strong> trước khi nộp.</p>
                        </div>
                    </div>
                `}
                ${hasAnyPractice
                    ? `<div class="practice-parts-stack">${practiceParts}</div>`
                    : '<div class="practice-empty-note">Giáo viên chưa nhập bài luyện tập cho bài này.</div>'}
                <div class="practice-submit-bar">
                    ${practiceDone ? '' : `
                        <button type="submit" class="practice-btn practice-btn--submit">
                            <i class="fas fa-paper-plane"></i>Nộp bài luyện
                        </button>
                    `}
                    ${practiceDone ? `
                        <button id="clearAnswersBtn" type="button" class="practice-btn practice-btn--ghost">
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
                        refreshLearningChrome(lesson);
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
                        practiceScore: mergedScore,
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
                        skillScores: lessonProgressSkillScores(lesson, mergedScore),
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
                try {
                    await syncLessonState(lesson, nextState, {
                        status: 'in_progress',
                        score: progress.score || 0,
                        skillScores: progress.skillScores || {},
                        startedAt: nextState.startedAt,
                        completedAt: null
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
                { label: '√', insert: '√', title: 'Căn bậc hai (gõ thêm số, ví dụ √16)' },
                { label: 'x²', insert: '^2', title: 'Bình phương' },
                { label: 'x³', insert: '^3', title: 'Lập phương' },
                { label: 'a/b', insert: '/', title: 'Phân số (ví dụ 1/2)' },
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
            const attr = 'data-essay-key';
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
            const value = field?.value || '';
            answers[key] = value;
            if (essayAnswersEqual(value, item.answer || '')) correct += 1;
        });
        return { score: Math.round((correct / items.length) * 100), answers };
    }

    function collectFillSlotsFromCard(card, blankCount) {
        const slots = Array.from({ length: blankCount }, () => '');
        card?.querySelectorAll('.fill-drop-slot').forEach(slot => {
            const index = Number.parseInt(slot.dataset.slotIndex || '0', 10);
            const chip = slot.querySelector('.fill-slot-chip');
            if (Number.isFinite(index) && index >= 0 && index < blankCount) {
                slots[index] = chip?.dataset.chipValue || chip?.textContent?.trim() || '';
            }
        });
        return slots;
    }

    function evaluateFillExercises(lesson) {
        const items = Array.isArray(lesson.fill_exercises) ? lesson.fill_exercises : [];
        if (!items.length) return { score: null, answers: {} };
        const answers = {};
        let correct = 0;
        items.forEach((item, itemIndex) => {
            const normalized = normalizeFillExercise(item);
            const key = normalized.id || item.id || `fill_${itemIndex + 1}`;
            const card = document.querySelector(`[data-fill-card="${escapeSelector(key)}"]`);
            const slots = collectFillSlotsFromCard(card, normalized.blankCount);
            answers[key] = slots;
            const given = slots;
            const expected = normalized.answers;
            if (expected.length && expected.every((answer, slotIndex) => essayAnswersEqual(given[slotIndex], answer))) correct += 1;
        });
        return { score: Math.round((correct / items.length) * 100), answers };
    }

    function evaluateDragExercises(lesson) {
        const items = Array.isArray(lesson.drag_exercises) ? lesson.drag_exercises : [];
        if (!items.length) return { score: null, answers: {} };
        const answers = {};
        let correct = 0;
        items.forEach((item, itemIndex) => {
            const normalized = normalizeDragExercise(item);
            const key = normalized.id || item.id || `drag_${itemIndex + 1}`;
            if (normalized.mode === 'match') {
                const card = document.querySelector(`[data-match-card="${escapeSelector(key)}"]`);
                const matches = resolveMatchAnswers(lesson, key, card);
                answers[key] = matches;
                if (isMatchAnswerCorrect(normalized, matches)) correct += 1;
                return;
            }
            const zone = document.querySelector(`[data-sort-zone="${escapeSelector(key)}"]`);
            const current = Array.from(zone?.querySelectorAll('.drag-chip') || []).map(node => node.dataset.chipValue || node.textContent?.trim() || '');
            answers[key] = current;
            if (isSortAnswerCorrect(normalized, current)) correct += 1;
        });
        return { score: Math.round((correct / items.length) * 100), answers };
    }

    async function persistPracticeUi(lesson, nextUi) {
        const progress = currentLessonProgress(lesson);
        await syncLessonState(lesson, {
            ...nextUi,
            practiceDone: false,
            startedAt: nextUi.startedAt || currentUiState(lesson).startedAt || new Date().toISOString()
        }, {
            status: 'in_progress',
            score: progress.score || 0,
            skillScores: progress.skillScores || {}
        });
        refreshLearningChrome(lesson);
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

    function resolveSkillDisplayScores(lesson) {
        const progress = currentLessonProgress(lesson);
        const ui = currentUiState(lesson);
        const storedScores = progress.skillScores || {};
        if (ui.practiceDone && Object.keys(storedScores).length) {
            return storedScores;
        }

        const liveScoreData = calculateScore(lesson, ui.answers || {});
        const liveScores = liveScoreData.skillScores || {};
        const completionPercent = lessonCompletionPercent(lesson);
        const questions = Array.isArray(lesson.questions) ? lesson.questions : [];
        const skillQuestionCounts = {};
        questions.forEach(question => {
            const skillId = question.skill;
            if (skillId) skillQuestionCounts[skillId] = (skillQuestionCounts[skillId] || 0) + 1;
        });

        const result = {};
        (lesson.skills || []).forEach(skill => {
            const id = skill.id;
            const stored = Number(storedScores[id]);
            const baseline = Number.isFinite(stored) ? stored : completionPercent;
            const live = Number(liveScores[id]);
            const hasMcq = !!skillQuestionCounts[id];
            const answeredMcq = hasMcq && questions.some(question => (
                question.skill === id
                && ui.answers?.[question.id] !== undefined
                && ui.answers?.[question.id] !== null
            ));
            if (answeredMcq && Number.isFinite(live)) {
                result[id] = Math.max(baseline, live);
            } else {
                result[id] = baseline;
            }
        });
        return result;
    }

    function renderSkills(lesson) {
        const scores = resolveSkillDisplayScores(lesson);
        const skills = Array.isArray(lesson.skills) ? lesson.skills : [];
        els.skillPanel.innerHTML = skills.length ? skills.map(skill => {
            const score = scores[skill.id] || 0;
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
            'Đọc kiến thức cần nhớ',
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
                    title: 'Đang đọc kiến thức cần nhớ',
                    body: 'Đọc xong thì bấm "Đánh dấu đã học" để mở phần ví dụ.'
                });
                return;
            }
            applyNextActionSuggestion({
                title: tasks[0] || 'Bắt đầu bằng kiến thức cần nhớ',
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
                : 'Có thể ôn lại kiến thức cần nhớ hoặc làm thêm bài luyện.'
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
            completed_at: 'completedAt' in extra ? extra.completedAt : (uiState.completedAt ?? null),
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
            if (Number(payload.score) >= 100) {
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
        const data = await api(`api/lessons.php?debug=1&subject=${encodeURIComponent(PAGE_SUBJECT)}`, { method: 'GET' });
        state.user = data.user;
        ensureStudentOnAllowedLotrinhPage(state.user);
        state.lessons = (data.lessons || []).filter(lesson => lessonMatchesPageSubject(lesson));
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

    function bindEssayInputs(lesson) {
        document.querySelectorAll('.essay-input').forEach(field => {
            if (field.dataset.boundEssayInput === '1' || field.disabled) return;
            field.dataset.boundEssayInput = '1';
            const key = field.dataset.essayKey || '';
            let saveTimer = null;

            const applyLocalEssayAnswer = value => {
                if (isTeacherPreview()) {
                    state.teacherPreviewUi = {
                        ...state.teacherPreviewUi,
                        essayAnswers: { ...(state.teacherPreviewUi.essayAnswers || {}), [key]: value }
                    };
                    return;
                }
                const progress = currentLessonProgress(lesson);
                const ui = progress.state || {};
                state.progress[lesson.id] = {
                    ...progress,
                    state: {
                        ...ui,
                        essayAnswers: { ...(ui.essayAnswers || {}), [key]: value }
                    }
                };
            };

            field.addEventListener('input', () => {
                applyLocalEssayAnswer(field.value);
                window.clearTimeout(saveTimer);
                saveTimer = window.setTimeout(async () => {
                    try {
                        const ui = currentUiState(lesson);
                        const progress = currentLessonProgress(lesson);
                        await syncLessonState(lesson, {
                            ...ui,
                            essayAnswers: { ...(ui.essayAnswers || {}), [key]: field.value },
                            startedAt: ui.startedAt || new Date().toISOString()
                        }, {
                            status: progress.status || 'in_progress',
                            score: progress.score || 0,
                            skillScores: progress.skillScores || {}
                        });
                    } catch (err) {
                        console.warn('save essay answer error:', err);
                    }
                }, 500);
            });
        });
    }

    function prefersTouchPlacement() {
        try {
            if (window.matchMedia('(pointer: coarse)').matches) return true;
            if (window.matchMedia('(hover: none)').matches) return true;
            if (window.matchMedia('(any-pointer: coarse)').matches) return true;
            if (window.matchMedia('(any-hover: none)').matches) return true;
        } catch {}
        if ((navigator.maxTouchPoints || 0) > 0) return true;
        if ('ontouchstart' in window) return true;
        return /Android|webOS|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent || '');
    }

    function bindTouchTap(element, handler, options = {}) {
        if (!element || element.dataset.boundTouchTap === '1') return;
        element.dataset.boundTouchTap = '1';

        const isDisabled = () => (typeof options.disabled === 'function' ? options.disabled() : false);
        const tapSlop = options.tapSlop ?? 16;
        let activePointer = null;
        let startX = 0;
        let startY = 0;
        let suppressClick = false;

        const run = event => {
            if (isDisabled()) return;
            void handler(event);
        };

        const onPointerDown = event => {
            if (isDisabled()) return;
            if (event.pointerType === 'mouse' && event.button !== 0) return;
            activePointer = event.pointerId;
            startX = event.clientX;
            startY = event.clientY;
        };

        const onPointerUp = event => {
            if (isDisabled() || event.pointerId !== activePointer) return;
            activePointer = null;

            if (event.pointerType === 'mouse') {
                run(event);
                return;
            }

            const dx = Math.abs(event.clientX - startX);
            const dy = Math.abs(event.clientY - startY);
            if (dx > tapSlop || dy > tapSlop) return;

            suppressClick = true;
            event.preventDefault();
            run(event);
            window.setTimeout(() => { suppressClick = false; }, 500);
        };

        const onPointerCancel = event => {
            if (event.pointerId === activePointer) activePointer = null;
        };

        if (window.PointerEvent) {
            element.addEventListener('pointerdown', onPointerDown);
            element.addEventListener('pointerup', onPointerUp);
            element.addEventListener('pointercancel', onPointerCancel);
            element.addEventListener('click', event => {
                if (!suppressClick) return;
                event.preventDefault();
                event.stopPropagation();
            });
            return;
        }

        let touchActive = false;
        element.addEventListener('touchstart', event => {
            if (isDisabled() || event.touches.length !== 1) return;
            touchActive = true;
            startX = event.touches[0].clientX;
            startY = event.touches[0].clientY;
        }, { passive: true });

        element.addEventListener('touchend', event => {
            if (!touchActive) return;
            touchActive = false;
            const touch = event.changedTouches[0];
            if (!touch) return;
            const dx = Math.abs(touch.clientX - startX);
            const dy = Math.abs(touch.clientY - startY);
            if (dx > tapSlop || dy > tapSlop) return;
            suppressClick = true;
            event.preventDefault();
            run(event);
            window.setTimeout(() => { suppressClick = false; }, 500);
        }, { passive: false });

        element.addEventListener('click', event => {
            if (suppressClick) {
                event.preventDefault();
                event.stopPropagation();
                return;
            }
            run(event);
        });
    }

    function configureChipDrag(chip, enabled) {
        if (!chip || chip.disabled) return;
        if (prefersTouchPlacement() || !enabled) {
            chip.draggable = false;
            chip.removeAttribute('draggable');
        } else {
            chip.setAttribute('draggable', 'true');
        }
    }

    function clearSelectedChips(root) {
        root?.querySelectorAll('.drag-chip.chip-selected').forEach(node => node.classList.remove('chip-selected'));
        root?.querySelectorAll('.is-drop-ready').forEach(node => node.classList.remove('is-drop-ready'));
    }

    function toggleSelectedChip(chip, root) {
        if (!chip) return false;
        if (chip.classList.contains('chip-selected')) {
            chip.classList.remove('chip-selected');
            root?.querySelectorAll('.is-drop-ready').forEach(node => node.classList.remove('is-drop-ready'));
            return false;
        }
        clearSelectedChips(root);
        chip.classList.add('chip-selected');
        root?.querySelectorAll('.fill-drop-slot, .drag-pool, .drag-slot-row').forEach(node => {
            if (!node.querySelector('.fill-slot-chip') || node.classList.contains('fill-drop-slot')) {
                node.classList.add('is-drop-ready');
            }
        });
        return true;
    }

    function getSelectedChip(root) {
        return root?.querySelector('.drag-chip.chip-selected') || null;
    }

    function fillSlotPlaceholderText() {
        // Prefer tap-to-place for fill (even on desktop)
        return 'nhấn để điền';
    }

    function updateTouchDragHints(card, mode) {
        if (mode === 'fill') {
            // Always use tap hint for fill (including desktop)
            const poolLabel = card.querySelector('.fill-pool-label');
            if (poolLabel) {
                poolLabel.innerHTML = '<i class="fas fa-hand-pointer" aria-hidden="true"></i> Chọn một mảnh rồi nhấn vào ô trống';
            }
            card.querySelectorAll('.fill-slot-placeholder').forEach(node => {
                node.textContent = fillSlotPlaceholderText();
            });
            if (!prefersTouchPlacement()) return;
        }
        if (!prefersTouchPlacement()) return;
        if (mode === 'sort') {
            const poolLabel = card.querySelector('.sort-pool-label');
            const zoneLabel = card.querySelector('.sort-zone-label');
            if (poolLabel) {
                poolLabel.innerHTML = '<i class="fas fa-hand-pointer" aria-hidden="true"></i> Chạm mảnh ở khay trên để thêm vào hàng trả lời';
            }
            if (zoneLabel) {
                zoneLabel.innerHTML = '<i class="fas fa-hand-pointer" aria-hidden="true"></i> Chạm mảnh ở hàng trả lời để gỡ ra';
            }
            const placeholder = card.querySelector('.sort-zone-placeholder');
            if (placeholder) placeholder.textContent = 'Chạm mảnh phía trên để thêm vào đây...';
        }
    }

    function bindPracticeInteractions(lesson) {
        bindEssayInputs(lesson);
        document.querySelectorAll('[data-ai-text]').forEach(button => {
            if (button.dataset.boundAi === '1') return;
            button.dataset.boundAi = '1';
            button.onclick = () => triggerAiExplainButton(button, lesson, button.dataset.aiText || '');
        });

        const touchPlacement = prefersTouchPlacement();

        document.querySelectorAll('.fill-drag-card').forEach(card => {
            if (card.dataset.boundFillDrag === '1') return;
            card.dataset.boundFillDrag = '1';
            const key = card.dataset.fillCard || '';
            const pool = card.querySelector(`[data-fill-pool="${escapeSelector(key)}"]`);
            if (!pool) return;
            const item = (lesson.fill_exercises || []).map(normalizeFillExercise).find((entry, index) => String(entry.id || `fill_${index + 1}`) === key);
            const blankCount = item?.blankCount || 1;
            const practiceDone = !!currentUiState(lesson).practiceDone;
            // Force tap-to-place on desktop too (preferred over drag for fill blanks)
            card.classList.add('touch-placement');
            const useTapPlacement = true;
            updateTouchDragHints(card, 'fill');

            const getSlots = () => collectFillSlotsFromCard(card, blankCount);

            const persistSlots = async () => {
                const ui = currentUiState(lesson);
                await persistPracticeUi(lesson, {
                    ...ui,
                    fillAnswers: {
                        ...(ui.fillAnswers || {}),
                        [key]: getSlots()
                    }
                });
            };

            const emptySlotMarkup = () => `<span class="fill-slot-placeholder">${fillSlotPlaceholderText()}</span>`;

            const dropIntoSlot = async (slot, chip) => {
                if (!slot || !chip) return;
                const existing = slot.querySelector('.fill-slot-chip');
                if (existing && existing !== chip) pool.appendChild(existing);
                chip.classList.add('fill-slot-chip');
                slot.innerHTML = '';
                slot.appendChild(chip);
                configureChipDrag(chip, !practiceDone);
                bindFillChip(chip);
                clearSelectedChips(card);
                await persistSlots();
            };

            const returnChipToPool = async (chip, slot) => {
                if (!chip || !slot) return;
                pool.appendChild(chip);
                chip.classList.remove('fill-slot-chip');
                slot.innerHTML = emptySlotMarkup();
                clearSelectedChips(card);
                await persistSlots();
            };

            const bindFillChip = chip => {
                if (chip.dataset.boundFillChip === '1') return;
                chip.dataset.boundFillChip = '1';
                configureChipDrag(chip, !practiceDone);

                if (useTapPlacement) {
                    chip.draggable = false;
                    chip.removeAttribute('draggable');
                }

                if (!useTapPlacement) {
                    chip.addEventListener('dragstart', e => {
                        e.dataTransfer?.setData('application/x-lotrinh-chip', chip.dataset.chipId || '');
                        e.dataTransfer?.setData('text/plain', chip.dataset.chipValue || chip.textContent || '');
                        chip.classList.add('opacity-60');
                    });
                    chip.addEventListener('dragend', () => chip.classList.remove('opacity-60'));
                }

                const onFillChipTap = async () => {
                    if (practiceDone) return;
                    const slot = chip.closest('.fill-drop-slot');
                    if (useTapPlacement) {
                        if (slot) {
                            await returnChipToPool(chip, slot);
                            return;
                        }
                        toggleSelectedChip(chip, card);
                        return;
                    }
                    if (slot) {
                        await returnChipToPool(chip, slot);
                    }
                };

                if (useTapPlacement) {
                    bindTouchTap(chip, onFillChipTap, { disabled: () => practiceDone });
                } else {
                    chip.addEventListener('click', onFillChipTap);
                }
            };

            const allowDrop = target => {
                if (useTapPlacement) return;
                target?.addEventListener('dragover', e => {
                    e.preventDefault();
                    target.classList.add('drag-over');
                });
                target?.addEventListener('dragleave', () => target.classList.remove('drag-over'));
            };

            allowDrop(pool);
            card.querySelectorAll('.fill-drop-slot').forEach(allowDrop);

            if (useTapPlacement) {
                card.querySelectorAll('.fill-drop-slot').forEach(slot => {
                    bindTouchTap(slot, async () => {
                        if (practiceDone || slot.querySelector('.fill-slot-chip')) return;
                        const selected = getSelectedChip(card);
                        if (!selected || selected.closest('.fill-drop-slot')) return;
                        await dropIntoSlot(slot, selected);
                    }, {
                        disabled: () => practiceDone || !!slot.querySelector('.fill-slot-chip')
                    });
                });
            } else {
                pool.addEventListener('drop', async e => {
                    e.preventDefault();
                    pool.classList.remove('drag-over');
                    const chipId = e.dataTransfer?.getData('application/x-lotrinh-chip');
                    const chip = chipId ? card.querySelector(`[data-chip-id="${escapeSelector(chipId)}"]`) : null;
                    if (!chip) return;
                    const fromSlot = chip.closest('.fill-drop-slot');
                    if (fromSlot) fromSlot.innerHTML = emptySlotMarkup();
                    pool.appendChild(chip);
                    chip.classList.remove('fill-slot-chip');
                    await persistSlots();
                });

                card.querySelectorAll('.fill-drop-slot').forEach(slot => {
                    slot.addEventListener('drop', async e => {
                        e.preventDefault();
                        slot.classList.remove('drag-over');
                        const chipId = e.dataTransfer?.getData('application/x-lotrinh-chip');
                        const chip = chipId ? card.querySelector(`[data-chip-id="${escapeSelector(chipId)}"]`) : null;
                        await dropIntoSlot(slot, chip);
                    });
                });
            }

            pool.querySelectorAll('.drag-chip').forEach(bindFillChip);
            card.querySelectorAll('.fill-drop-slot .drag-chip').forEach(bindFillChip);
        });

        document.querySelectorAll('.sort-card').forEach(card => {
            if (card.dataset.boundSortDrag === '1') return;
            card.dataset.boundSortDrag = '1';
            const key = card.dataset.sortCard || '';
            const pool = card.querySelector(`[data-sort-pool="${escapeSelector(key)}"]`);
            const zone = card.querySelector(`[data-sort-zone="${escapeSelector(key)}"]`);
            if (!pool || !zone) return;
            const practiceDone = !!currentUiState(lesson).practiceDone;
            if (touchPlacement) card.classList.add('touch-placement');
            updateTouchDragHints(card, 'sort');

            const sortZonePlaceholderText = () => (
                touchPlacement
                    ? 'Chạm mảnh phía trên để thêm vào đây...'
                    : 'Kéo các mảnh từ khay phía trên xuống đây...'
            );

            const syncSortZonePlaceholder = () => {
                const chips = zone.querySelectorAll('.drag-chip');
                let placeholder = zone.querySelector('.sort-zone-placeholder');
                if (chips.length) {
                    placeholder?.remove();
                    return;
                }
                if (!placeholder) {
                    placeholder = document.createElement('span');
                    placeholder.className = 'sort-zone-placeholder';
                    zone.appendChild(placeholder);
                }
                placeholder.textContent = sortZonePlaceholderText();
            };

            const persistOrder = async () => {
                syncSortZonePlaceholder();
                const ui = currentUiState(lesson);
                const current = Array.from(zone.querySelectorAll('.drag-chip')).map(node => node.dataset.chipValue || node.textContent?.trim() || '');
                await persistPracticeUi(lesson, {
                    ...ui,
                    dragAnswers: {
                        ...(ui.dragAnswers || {}),
                        [key]: current
                    }
                });
            };

            const moveChipToZone = async (chip, beforeNode = null) => {
                if (!chip) return;
                if (beforeNode && beforeNode.parentElement === zone) zone.insertBefore(chip, beforeNode);
                else zone.appendChild(chip);
                configureChipDrag(chip, !practiceDone);
                bindSortChip(chip);
                clearSelectedChips(card);
                await persistOrder();
            };

            const bindSortChip = chip => {
                if (chip.dataset.boundSortChip === '1') return;
                chip.dataset.boundSortChip = '1';
                configureChipDrag(chip, !practiceDone);

                if (!touchPlacement) {
                    chip.addEventListener('dragstart', e => {
                        e.dataTransfer?.setData('application/x-lotrinh-chip', chip.dataset.chipId || '');
                        e.dataTransfer?.setData('text/plain', chip.dataset.chipValue || chip.textContent || '');
                        chip.classList.add('opacity-60');
                    });
                    chip.addEventListener('dragend', () => chip.classList.remove('opacity-60'));
                }

                const onSortChipTap = async () => {
                    if (practiceDone) return;
                    if (touchPlacement) {
                        if (chip.parentElement === zone) {
                            pool.appendChild(chip);
                            clearSelectedChips(card);
                            await persistOrder();
                            return;
                        }
                        await moveChipToZone(chip);
                        return;
                    }
                    if (chip.parentElement === zone) {
                        pool.appendChild(chip);
                    } else {
                        zone.appendChild(chip);
                    }
                    await persistOrder();
                };

                if (touchPlacement) {
                    bindTouchTap(chip, onSortChipTap, { disabled: () => practiceDone });
                } else {
                    chip.addEventListener('click', onSortChipTap);
                }
            };

            const allowDrop = target => {
                if (touchPlacement) return;
                target?.addEventListener('dragover', e => {
                    e.preventDefault();
                    target.classList.add('drag-over');
                });
                target?.addEventListener('dragleave', () => target.classList.remove('drag-over'));
            };
            allowDrop(pool);
            allowDrop(zone);

            if (!touchPlacement) {
                zone.addEventListener('drop', async e => {
                    e.preventDefault();
                    zone.classList.remove('drag-over');
                    const chipId = e.dataTransfer?.getData('application/x-lotrinh-chip');
                    const chip = chipId ? card.querySelector(`[data-chip-id="${escapeSelector(chipId)}"]`) : null;
                    if (!chip) return;
                    const target = e.target.closest('.drag-chip');
                    await moveChipToZone(chip, target && target !== chip ? target : null);
                });

                pool.addEventListener('drop', async e => {
                    e.preventDefault();
                    pool.classList.remove('drag-over');
                    const chipId = e.dataTransfer?.getData('application/x-lotrinh-chip');
                    const chip = chipId ? card.querySelector(`[data-chip-id="${escapeSelector(chipId)}"]`) : null;
                    if (!chip) return;
                    pool.appendChild(chip);
                    await persistOrder();
                });
            } else {
                bindTouchTap(zone, async event => {
                    if (practiceDone || event.target.closest('.drag-chip')) return;
                    const selected = getSelectedChip(card);
                    if (!selected || selected.parentElement !== pool) return;
                    await moveChipToZone(selected);
                }, { disabled: () => practiceDone });
            }

            pool.querySelectorAll('.drag-chip').forEach(bindSortChip);
            zone.querySelectorAll('.drag-chip').forEach(bindSortChip);
            syncSortZonePlaceholder();
        });

        document.querySelectorAll('.match-card').forEach(card => {
            if (card.dataset.boundMatch === '1') return;
            card.dataset.boundMatch = '1';
            const key = card.dataset.matchCard || '';
            let selectedLeft = null;

            let localMatches = normalizeMatchAnswers(currentUiState(lesson).dragAnswers?.[key]);

            const readMatches = () => ({ ...localMatches });

            const paintMatchState = matches => {
                const entries = Object.entries(matches).map(([left, right]) => [Number(left), Number(right)]);
                const rightToPair = new Map(entries.map(([left, right], order) => [right, { left, order: order + 1 }]));
                const leftToPair = new Map(entries.map(([left, right], order) => [left, { right, order: order + 1 }]));

                card.querySelectorAll('.match-item[data-match-side="left"]').forEach(button => {
                    const index = Number.parseInt(button.dataset.matchIndex || '-1', 10);
                    const pair = leftToPair.get(index);
                    button.classList.toggle('is-paired', !!pair);
                    button.classList.toggle('is-selected', selectedLeft === index);
                    if (pair) button.dataset.pairedRight = String(pair.right);
                    else delete button.dataset.pairedRight;
                    let badge = button.querySelector('.match-pair-badge');
                    if (pair) {
                        if (!badge) {
                            badge = document.createElement('span');
                            badge.className = 'match-pair-badge';
                            button.prepend(badge);
                        }
                        badge.textContent = String(pair.order);
                    } else if (badge) {
                        badge.remove();
                    }
                });

                card.querySelectorAll('.match-item[data-match-side="right"]').forEach(button => {
                    const index = Number.parseInt(button.dataset.matchIndex || '-1', 10);
                    const pair = rightToPair.get(index);
                    button.classList.toggle('is-paired', !!pair);
                    button.classList.remove('is-selected');
                    let badge = button.querySelector('.match-pair-badge');
                    if (pair) {
                        if (!badge) {
                            badge = document.createElement('span');
                            badge.className = 'match-pair-badge';
                            button.prepend(badge);
                        }
                        badge.textContent = String(pair.order);
                    } else if (badge) {
                        badge.remove();
                    }
                });
            };

            const saveMatches = async matches => {
                localMatches = normalizeMatchAnswers(matches);
                paintMatchState(localMatches);
                const ui = currentUiState(lesson);
                const nextUi = {
                    ...ui,
                    dragAnswers: {
                        ...(ui.dragAnswers || {}),
                        [key]: localMatches
                    }
                };
                syncLocalLessonUiState(lesson, nextUi);
                await persistPracticeUi(lesson, nextUi);
            };

            paintMatchState(localMatches);

            card.querySelectorAll('.match-item').forEach(button => {
                button.addEventListener('click', async () => {
                    const side = button.dataset.matchSide;
                    const index = Number.parseInt(button.dataset.matchIndex || '-1', 10);
                    if (!Number.isFinite(index) || index < 0) return;
                    const matches = readMatches();

                    if (side === 'left') {
                        if (matches[index] !== undefined) {
                            delete matches[index];
                            selectedLeft = null;
                            await saveMatches(matches);
                        } else {
                            selectedLeft = index;
                            paintMatchState(matches);
                        }
                        return;
                    }

                    if (selectedLeft === null) return;
                    Object.keys(matches).forEach(leftKey => {
                        if (Number(matches[leftKey]) === index) delete matches[leftKey];
                    });
                    matches[selectedLeft] = index;
                    selectedLeft = null;
                    await saveMatches(matches);
                });
            });
        });

        document.querySelectorAll('.fill-check-btn').forEach(button => {
            if (button.dataset.boundFillCheck === '1') return;
            button.dataset.boundFillCheck = '1';
            button.onclick = () => {
                const key = button.dataset.fillKey || '';
                const card = document.querySelector(`[data-fill-card="${escapeSelector(key)}"]`);
                const feedback = card?.querySelector('.fill-feedback');
                if (!feedback || !card) return;
                const item = (lesson.fill_exercises || []).map(normalizeFillExercise).find((entry, index) => String(entry.id || `fill_${index + 1}`) === key);
                if (!item) return;
                const slots = collectFillSlotsFromCard(card, item.blankCount);
                feedback.classList.remove('hidden');
                feedback.innerHTML = buildFillCheckFeedback(item, slots);
                typesetMath();
            };
        });

        document.querySelectorAll('.sort-check-btn').forEach(button => {
            if (button.dataset.boundSortCheck === '1') return;
            button.dataset.boundSortCheck = '1';
            button.onclick = () => {
                const key = button.dataset.sortKey || '';
                const card = document.querySelector(`[data-sort-card="${escapeSelector(key)}"]`);
                const feedback = card?.querySelector('.drag-feedback');
                const zone = card?.querySelector(`[data-sort-zone="${escapeSelector(key)}"]`);
                if (!feedback || !card || !zone) return;
                const item = (lesson.drag_exercises || []).map(normalizeDragExercise).find((entry, index) => String(entry.id || `drag_${index + 1}`) === key);
                if (!item || item.mode !== 'sort') return;
                const pool = card?.querySelector(`[data-sort-pool="${escapeSelector(key)}"]`);
                const savedOrder = Array.from(zone.querySelectorAll('.drag-chip')).map(node => node.dataset.chipValue || node.textContent?.trim() || '');
                const poolRemaining = pool?.querySelectorAll('.drag-chip').length || 0;
                feedback.classList.remove('hidden');
                feedback.innerHTML = buildSortCheckFeedback(item, savedOrder, poolRemaining);
            };
        });

        document.querySelectorAll('.match-check-btn').forEach(button => {
            if (button.dataset.boundMatchCheck === '1') return;
            button.dataset.boundMatchCheck = '1';
            button.onclick = () => {
                const key = button.dataset.matchKey || '';
                const card = document.querySelector(`[data-match-card="${escapeSelector(key)}"]`);
                const feedback = card?.querySelector('.drag-feedback');
                if (!feedback || !card) return;
                const item = (lesson.drag_exercises || []).map(normalizeDragExercise).find((entry, index) => String(entry.id || `drag_${index + 1}`) === key);
                if (!item || item.mode !== 'match') return;
                const savedMatches = resolveMatchAnswers(lesson, key, card);
                feedback.classList.remove('hidden');
                feedback.innerHTML = buildMatchCheckFeedback(item, savedMatches);
            };
        });

        document.querySelectorAll('.essay-check-btn').forEach(button => {
            if (button.dataset.boundEssay === '1') return;
            button.dataset.boundEssay = '1';
            button.onclick = () => {
                const key = button.dataset.essayKey || '';
                const card = button.closest('.practice-card');
                const input = card?.querySelector(`[data-essay-key="${escapeSelector(key)}"]`);
                const feedback = card?.querySelector('.essay-feedback');
                if (!feedback || !input) return;
                const item = (lesson.essay_exercises || []).find((entry, index) => String(entry.id || `essay_${index + 1}`) === key);
                const value = String(input.value || '').trim();
                feedback.classList.remove('hidden');
                feedback.innerHTML = buildEssayCheckFeedback(item, value);
                if (!value || !isEssayNumericAnswer(value)) input.focus();
            };
        });

        bindMathSymbolToolbars();
    }

    initStudentAiAssist();

    function handleAuthLoadError(err) {
        const message = String(err?.message || 'Không tải được lộ trình.');
        if (message.toLowerCase().includes('chưa đăng nhập') || message.toLowerCase().includes('not logged in')) {
            localStorage.removeItem('authToken');
            localStorage.removeItem('userEmail');
            localStorage.removeItem('userName');
            localStorage.removeItem('userRole');
            localStorage.removeItem('allowedPages');
            localStorage.removeItem('userClassName');
            window.location.href = 'login.html';
            return true;
        }
        state.error = message;
        return false;
    }

    async function bootstrapLotrinhPage() {
        state.loading = true;
        state.error = '';
        render();
        let lessonToStart = null;
        try {
            await reloadLessons(true);
            if (!state.selectedLessonId && state.lessons[0]) {
                state.selectedLessonId = state.lessons[0].id;
                localStorage.setItem(LS_LESSON_KEY, state.selectedLessonId);
            }
            if (!state.selectedLessonId && state.lessons[0]) {
                state.selectedLessonId = state.lessons[0].id;
            }
            if (!isTeacher()) {
                lessonToStart = currentLesson();
            }
        } catch (err) {
            if (handleAuthLoadError(err)) return;
        } finally {
            state.loading = false;
            render();
        }
        if (lessonToStart) {
            markLessonStarted(lessonToStart).catch(console.warn);
        }
    }

    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState !== 'visible' || isTeacher()) return;
        reloadLessons(false).then(() => render()).catch(console.warn);
    });

    await bootstrapLotrinhPage();

    els.resetBtn.onclick = async () => {
        const lesson = currentLesson();
        if (!lesson) return;
        if (!confirm('Làm lại toàn bộ tiến độ của bài hiện tại?')) return;
        await resetLesson(lesson);
        await reloadLessons(false);
        render();
    };
})();
