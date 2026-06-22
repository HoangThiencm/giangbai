(function () {
    const SUBJECTS = [
        { id: 'math4', label: 'Toán 4', title: 'Toán 4' },
        { id: 'math5', label: 'Toán 5', title: 'Toán 5' },
        { id: 'math6', label: 'Toán 6', title: 'Toán 6' },
        { id: 'math7', label: 'Toán 7', title: 'Toán 7' },
        { id: 'math8', label: 'Toán 8', title: 'Toán 8' },
        { id: 'math9', label: 'Toán 9', title: 'Toán 9' }
    ];

    const defaults = {
        slug: 'math6-c1-b1-tap-hop',
        subject: 'Toán 6',
        chapter: 'Chương 1: Số tự nhiên',
        title: 'Bài 1: Tập hợp',
        order_index: 1,
        is_published: true,
        goal_text: 'Học sinh hiểu tập hợp là gì, biết viết tập hợp bằng cách liệt kê phần tử và dùng ký hiệu thuộc, không thuộc.',
        theory: [
            'Tập hợp là một nhóm các đối tượng được xác định rõ ràng.',
            'Mỗi đối tượng trong một tập hợp được gọi là một phần tử.',
            'Ta thường đặt tên tập hợp bằng chữ cái in hoa.',
            'Có thể nhập công thức bằng LaTeX, ví dụ: $A=\\{1,2,3\\}$.'
        ],
        examples: [
            { title: 'Ví dụ 1', body: 'A = $\\{1,2,3,4\\}$ là tập hợp các số tự nhiên nhỏ hơn 5.' },
            { title: 'Ví dụ 2', body: 'Nếu B = $\\{a,b,c\\}$ thì $a \\in B$ và $d \\notin B$.' }
        ],
        videos: [
            { title: 'Bài giảng ôn lại', url: '' }
        ],
        skills: [
            { id: 'khai_niem', name: 'Hiểu khái niệm tập hợp', target: 80 },
            { id: 'liet_ke', name: 'Liệt kê phần tử của tập hợp', target: 80 },
            { id: 'ky_hieu', name: 'Dùng ký hiệu thuộc và không thuộc', target: 80 }
        ],
        tasks: ['Đọc lý thuyết ngắn', 'Xem ví dụ mẫu', 'Làm bài luyện tập'],
        questions: [
            {
                id: 'q1',
                skill: 'khai_niem',
                prompt: 'Câu nào mô tả đúng nhất về tập hợp?',
                options: ['Một nhóm các đối tượng được xác định rõ ràng', 'Một phép tính cộng', 'Một số tự nhiên bất kỳ', 'Một hình vẽ'],
                answer: 0
            },
            {
                id: 'q2',
                skill: 'ky_hieu',
                prompt: 'Cho $B=\\{2,4,6,8\\}$. Khẳng định nào đúng?',
                options: ['$3 \\in B$', '$6 \\in B$', '$8 \\notin B$', '$4 \\notin B$'],
                answer: 1
            }
        ]
    };

    const PAGE_SUBJECT = String(window.LOTRINH_SUBJECT || '').trim();
    const PAGE_TO_SUBJECT = {
        lotrinh: 'Toán 6',
        lotrinhtoan4: 'Toán 4',
        lotrinhtoan5: 'Toán 5',
        lotrinhtoan6: 'Toán 6',
        lotrinhtoan7: 'Toán 7',
        lotrinhtoan8: 'Toán 8',
        lotrinhtoan9: 'Toán 9'
    };

    let lessons = [];
    let currentSlug = defaults.slug;
    let currentLessonId = null;
    let selectedSubject = PAGE_SUBJECT || 'Toán 6';
    let essayItems = [];
    let fillItems = [];
    let dragItems = [];
    let questionItems = [];

    function el(id) { return document.getElementById(id); }

    function getAllowedPages() {
        try {
            return JSON.parse(localStorage.getItem('allowedPages') || '[]');
        } catch {
            return [];
        }
    }

    function getTeacherAllowedSubjects() {
        if (localStorage.getItem('userRole') !== 'teacher') {
            return SUBJECTS.map(item => item.title);
        }
        const subjects = getAllowedPages()
            .map(page => PAGE_TO_SUBJECT[page === 'lotrinh' ? 'lotrinhtoan6' : page])
            .filter(Boolean);
        return [...new Set(subjects)];
    }

    function scopedSubjects() {
        const allowed = new Set(getTeacherAllowedSubjects());
        if (localStorage.getItem('userRole') !== 'teacher') {
            return SUBJECTS;
        }
        return SUBJECTS.filter(item => allowed.has(item.title));
    }

    function teacherCanManageScope() {
        if (localStorage.getItem('userRole') !== 'teacher') return true;
        const allowed = getTeacherAllowedSubjects();
        if (!allowed.length) return false;
        if (isPageScopedEditor()) return allowed.includes(PAGE_SUBJECT);
        return scopedSubjects().length > 0;
    }

    function isPageScopedEditor() {
        return !!PAGE_SUBJECT && !!el('lessonDesignerMount') && localStorage.getItem('userRole') === 'teacher';
    }

    function normalizeSubjectName(value) {
        return String(value || '').trim();
    }

    function lessonsForScope() {
        if (!isPageScopedEditor()) {
            return lessons.filter(lesson => lesson.subject === selectedSubject);
        }
        return lessons.filter(lesson => normalizeSubjectName(lesson.subject) === PAGE_SUBJECT);
    }

    function chaptersForScope() {
        const seen = new Set();
        const items = [];
        lessonsForScope().forEach(lesson => {
            const chapter = String(lesson.chapter || '').trim();
            if (!chapter || seen.has(chapter)) return;
            seen.add(chapter);
            items.push(chapter);
        });
        return items.sort((a, b) => a.localeCompare(b, 'vi'));
    }

    function renderChapterOptions() {
        const datalist = el('lessonChapterOptions');
        if (!datalist) return;
        datalist.innerHTML = chaptersForScope()
            .map(chapter => `<option value="${escapeHtml(chapter)}"></option>`)
            .join('');
    }

    function getAdminKey() {
        try {
            return typeof cachedKey !== 'undefined' ? cachedKey : (window.cachedKey || '');
        } catch {
            return window.cachedKey || '';
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

    function slugify(value) {
        return String(value || '')
            .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
            .toLowerCase()
            .replace(/đ/g, 'd')
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-+|-+$/g, '')
            .slice(0, 110);
    }

    function parseLines(text) {
        return String(text || '').split('\n').map(line => line.trim()).filter(Boolean);
    }

    const AI_MARKER = '[AI]';
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

    function parseTheoryBlocks(text) {
        return String(text || '')
            .replace(/\r/g, '')
            .split(/\n\s*\n+/)
            .map(block => parseContentWithAiMarker(block))
            .filter(block => block.text);
    }

    function formatTheoryBlocks(blocks) {
        return (Array.isArray(blocks) ? blocks : [])
            .map(item => {
                const block = normalizeTheoryItem(item);
                if (!block.text) return '';
                return block.ai ? `${block.text}\n${AI_MARKER}` : block.text;
            })
            .filter(Boolean)
            .join('\n\n');
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

    function parseExamples(text) {
        const blocks = String(text || '').replace(/\r/g, '').split(/\n\s*\n+/).map(block => block.trim()).filter(Boolean);
        const source = blocks.length > 1 || !String(text || '').includes('|') ? blocks : parseLines(text);
        return source.map((block, index) => {
            const parts = block.includes('||') ? block.split('||') : block.split('|');
            if (parts.length >= 2) {
                const [title, ...bodyParts] = parts;
                const parsed = parseContentWithAiMarker(bodyParts.join(parts.length > 2 ? '|' : '').trim());
                return {
                    title: (title || `Ví dụ ${index + 1}`).trim(),
                    body: parsed.text,
                    ai: parsed.ai
                };
            }
            const lines = block.split('\n').map(line => line.replace(/[ \t]+$/g, ''));
            const title = (lines[0] || '').trim();
            const parsed = parseContentWithAiMarker(lines.slice(1).join('\n').trim());
            return {
                title: title || `Ví dụ ${index + 1}`,
                body: parsed.text,
                ai: parsed.ai
            };
        }).filter(example => example.title || example.body);
    }

    function parseSkills(text) {
        return parseLines(text).map((line, index) => {
            const [id, name, target] = line.split('|').map(part => part.trim());
            return {
                id: slugify(id || name || `skill-${index + 1}`),
                name: name || id || `Kỹ năng ${index + 1}`,
                target: Number(target) || 80
            };
        });
    }

    function parseVideos(text) {
        return parseLines(text).map(line => {
            const parts = line.includes('||') ? line.split('||') : line.split('|');
            const [title, ...urlParts] = parts;
            return { title: (title || 'Video bài giảng').trim(), url: urlParts.join('|').trim() };
        }).filter(video => video.url);
    }

    function answerToIndex(value, lineNumber) {
        const raw = String(value || '').trim().toUpperCase().replace(/^ĐÁP\s*ÁN\s*[:：-]?\s*/, '');
        const letter = raw.match(/^[ABCD]$/)?.[0] || raw.match(/(?:^|\s)([ABCD])(?:\s|$)/)?.[1];
        if (letter) return letter.charCodeAt(0) - 65;
        const number = raw.match(/^[1-4]$/)?.[0] || raw.match(/(?:^|\s)([1-4])(?:\s|$)/)?.[1];
        if (number) return Number(number) - 1;
        throw new Error(`Câu hỏi số ${lineNumber} chưa có đáp án đúng. Nhập A/B/C/D hoặc 1/2/3/4.`);
    }

    function decodePastedText(text) {
        return String(text || '')
            .replace(/\r/g, '')
            .replace(/&quot;/g, '"')
            .replace(/&lt;/g, '<')
            .replace(/&gt;/g, '>')
            .replace(/&amp;/g, '&')
            .replace(/&nbsp;/g, ' ');
    }

    function splitQuestionParts(line) {
        return (line.includes('||') ? line.split('||') : line.split('|'))
            .map(part => part.trim())
            .filter(Boolean);
    }

    function parseQuestionLine(line, index, fallbackSkill) {
        const parts = splitQuestionParts(line);
        if (parts.length < 6) {
            throw new Error(`Câu hỏi số ${index + 1} chưa đúng mẫu: Câu hỏi | A | B | C | D | đáp án`);
        }

        const hasSkill = parts.length >= 7;
        const skill = hasSkill ? parts[0] : fallbackSkill;
        const offset = hasSkill ? 1 : 0;
        const prompt = parts[offset];
        const options = parts.slice(offset + 1, offset + 5);
        const answer = parts[offset + 5];
        if (!prompt || options.length < 4 || options.some(option => !option)) {
            throw new Error(`Câu hỏi số ${index + 1} còn thiếu nội dung hoặc lựa chọn A/B/C/D.`);
        }

        return {
            id: `q${index + 1}`,
            skill: slugify(skill || fallbackSkill || 'tong_hop'),
            prompt,
            options,
            answer: answerToIndex(answer, index + 1)
        };
    }

    function canParseQuestionBlock(block, fallbackSkill) {
        try {
            parseQuestionLine(block, 0, fallbackSkill);
            return true;
        } catch {
            return false;
        }
    }

    function readQuestionBlocks(text, fallbackSkill) {
        const lines = decodePastedText(text).split('\n').map(line => line.trim()).filter(Boolean);
        const blocks = [];
        let buffer = '';

        lines.forEach(line => {
            buffer = buffer ? `${buffer} ${line}` : line;
            if (canParseQuestionBlock(buffer, fallbackSkill)) {
                blocks.push(buffer);
                buffer = '';
            }
        });

        if (buffer.trim()) {
            parseQuestionLine(buffer, blocks.length, fallbackSkill);
        }

        return blocks;
    }

    function parseQuestions(text, skills = []) {
        const fallbackSkill = skills[0]?.id || 'tong_hop';
        return readQuestionBlocks(text, fallbackSkill).map((line, index) => parseQuestionLine(line, index, fallbackSkill));
    }

    function parseEssayExercises(text) {
        return parseLines(text).map((line, index) => {
            const parts = splitQuestionParts(line);
            return { id: `essay_${index + 1}`, prompt: parts[0] || '', answer: parts[1] || '', hint: parts[2] || '' };
        }).filter(item => item.prompt);
    }

    const POOL_ITEM_JOINER = ' » ';
    const POOL_ITEM_SEP_RE = /\s*»\s*/u;

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

    function poolTextHasMultipleItems(value) {
        return splitPoolText(value).length > 1;
    }

    function parseMatchPairs(spec) {
        return String(spec || '').split(',').map(part => part.trim()).filter(Boolean).map(part => {
            const [left, right] = part.split('-').map(value => Number.parseInt(value, 10));
            if (!Number.isFinite(left) || !Number.isFinite(right)) return null;
            return { left, right };
        }).filter(Boolean);
    }

    function parseFillExercises(text) {
        return parseLines(text).map((line, index) => {
            const parts = splitQuestionParts(line);
            const prompt = parts[0] || '';
            let pool = [];
            let answer = parts[1] || '';
            let hint = parts[2] || '';
            if (poolTextHasMultipleItems(parts[1])) {
                pool = splitPoolText(parts[1]);
                answer = parts[2] || pool[0] || '';
                hint = parts[3] || '';
            } else if (answer) {
                pool = [String(answer).trim()];
            }
            const answers = poolTextHasMultipleItems(answer) ? splitPoolText(answer) : [String(answer || '').trim()].filter(Boolean);
            return {
                id: `fill_${index + 1}`,
                prompt,
                items: pool,
                pool,
                answer: answers.length <= 1 ? (answers[0] || '') : answers,
                hint
            };
        }).filter(item => item.prompt && (item.pool.length || item.answer));
    }

    function parseDragExercises(text) {
        return parseLines(text).map((line, index) => {
            const parts = splitQuestionParts(line);
            const prompt = parts[0] || '';
            const pairSpec = parts[3] || '';
            if (pairSpec && /\d+\s*-\s*\d+/.test(pairSpec)) {
                const pairs = parseMatchPairs(pairSpec);
                const left = repairPoolPieces(splitPoolText(parts[1]), pairs.length);
                const right = repairPoolPieces(splitPoolText(parts[2]), pairs.length);
                return {
                    id: `drag_${index + 1}`,
                    mode: 'match',
                    prompt,
                    left,
                    right,
                    pairs,
                    pair_spec: pairSpec,
                    hint: parts[4] || ''
                };
            }
            const items = splitPoolText(parts[1]);
            const answer = splitPoolText(parts[2] || parts[1]);
            return {
                id: `drag_${index + 1}`,
                mode: 'sort',
                prompt,
                items,
                answer,
                hint: parts[3] || ''
            };
        }).filter(item => {
            if (item.mode === 'match') return item.prompt && item.left?.length && item.right?.length && item.pairs?.length;
            return item.prompt && item.items?.length && item.answer?.length;
        });
    }

    function formatExamples(items) {
        return (items || []).map(item => {
            const normalized = normalizeExampleItem(item);
            const body = normalized.ai ? `${normalized.body}\n${AI_MARKER}` : normalized.body;
            return `${normalized.title}\n${body}`.trim();
        }).join('\n\n');
    }

    function formatSkills(items) {
        return (items || []).map(item => `${item.id || ''} | ${item.name || ''} | ${item.target || 80}`).join('\n');
    }

    function formatVideos(items) {
        return (items || []).map(item => `${item.title || 'Video bài giảng'} | ${item.url || ''}`).join('\n');
    }

    function formatQuestions(items) {
        return (items || []).map(item => {
            const options = item.options || [];
            const answer = 'ABCD'[Number(item.answer || 0)] || 'A';
            return [
                item.prompt || '',
                options[0] || '',
                options[1] || '',
                options[2] || '',
                options[3] || '',
                answer
            ].join(' | ');
        }).join('\n');
    }

    function formatEssayExercises(items) {
        return (items || []).map(item => [item.prompt || '', item.answer || '', item.hint || ''].join(' | ')).join('\n');
    }

    function formatFillExercises(items) {
        return (items || []).map(item => {
            const pool = joinPoolText(item.items || item.pool || []);
            const answer = Array.isArray(item.answer) ? joinPoolText(item.answer) : (item.answer || '');
            return [item.prompt || '', pool || answer, answer, item.hint || ''].filter((part, idx, arr) => !(idx === 1 && part === arr[2])).join(' | ');
        }).join('\n');
    }

    function formatDragExercises(items) {
        return (items || []).map(item => {
            if (item.mode === 'match' || (Array.isArray(item.left) && Array.isArray(item.right))) {
                const pairs = (item.pairs || []).map(pair => `${pair.left}-${pair.right}`).join(',');
                const pairCount = (item.pairs || []).length;
                const left = joinPoolText(repairPoolPieces(item.left || [], pairCount));
                const right = joinPoolText(repairPoolPieces(item.right || [], pairCount));
                return [item.prompt || '', left, right, pairs, item.hint || ''].join(' | ');
            }
            return [item.prompt || '', joinPoolText(item.items || []), joinPoolText(item.answer || []), item.hint || ''].join(' | ');
        }).join('\n');
    }

    function richToolbarHtml(targetId) {
        return `
            <div class="lesson-rich-toolbar" data-target="${targetId}">
                <button type="button" data-wrap="**" title="In đậm"><i class="fas fa-bold"></i></button>
                <button type="button" data-wrap="*" title="In nghiêng"><i class="fas fa-italic"></i></button>
                <button type="button" data-wrap="++" title="Gạch chân"><i class="fas fa-underline"></i></button>
                <button type="button" data-action="image" title="Chèn ảnh"><i class="fas fa-image"></i></button>
                <button type="button" data-action="ai" title="Thêm [AI] cho đoạn này"><i class="fas fa-wand-magic-sparkles"></i> [AI]</button>
            </div>
        `;
    }

    function insertEditorWrap(targetId, marker, placeholder = 'nội dung') {
        const field = el(targetId);
        if (!field) return;
        const start = field.selectionStart ?? 0;
        const end = field.selectionEnd ?? start;
        const selected = field.value.slice(start, end) || placeholder;
        const next = `${marker}${selected}${marker}`;
        field.setRangeText(next, start, end, 'end');
        const cursor = start + marker.length + selected.length + marker.length;
        field.setSelectionRange(cursor, cursor);
        field.focus();
        field.dispatchEvent(new Event('input', { bubbles: true }));
    }

    function insertEditorImage(targetId) {
        const field = el(targetId);
        if (!field) return;
        const url = window.prompt('Dán link ảnh (https://...)');
        if (!url) return;
        const alt = window.prompt('Mô tả ảnh (có thể để trống)', '') || '';
        const insert = `\n![${alt}](${url.trim()})\n`;
        const start = field.selectionStart ?? field.value.length;
        field.setRangeText(insert, start, start, 'end');
        field.focus();
        field.dispatchEvent(new Event('input', { bubbles: true }));
    }

    function insertEditorAiMarker(targetId) {
        const field = el(targetId);
        if (!field) return;
        const insert = `\n${AI_MARKER}\n`;
        const start = field.selectionStart ?? field.value.length;
        field.setRangeText(insert, start, start, 'end');
        field.focus();
        field.dispatchEvent(new Event('input', { bubbles: true }));
    }

    function setupRichToolbars() {
        document.querySelectorAll('.lesson-rich-toolbar').forEach(toolbar => {
            if (toolbar.dataset.ready) return;
            toolbar.dataset.ready = '1';
            const targetId = toolbar.dataset.target;
            toolbar.querySelectorAll('button[data-wrap]').forEach(button => {
                button.onclick = () => insertEditorWrap(targetId, button.dataset.wrap || '');
            });
            toolbar.querySelector('[data-action="image"]').onclick = () => insertEditorImage(targetId);
            toolbar.querySelector('[data-action="ai"]').onclick = () => insertEditorAiMarker(targetId);
        });
    }

    // Dynamic flexible items for structured sections (support paste image per item via rich toolbar)
    function syncEssayToTextarea() {
        const ta = el('lessonEssay');
        if (!ta) return;
        ta.value = essayItems.map(i => `${i.de}|${i.dap}|${i.goi}`).join('\n');
        ta.dispatchEvent(new Event('input', { bubbles: true }));
    }
    function renderEssayItems() {
        const cont = el('essayItems');
        if (!cont) return;
        cont.innerHTML = '';
        essayItems.forEach((it, i) => {
            const d = document.createElement('div');
            d.className = 'p-2 border rounded bg-white text-xs';
            d.innerHTML = `
                <div class="flex items-center mb-1">
                    <span class="font-bold">Bài ${i+1}</span>
                    <button type="button" class="ml-auto text-rose-600" onclick="removeEssayItem(${i})">×</button>
                </div>
                ${richToolbarHtml(`essay-de-${i}`)}
                <textarea id="essay-de-${i}" class="w-full p-1 border text-xs" placeholder="Đề bài (dán ảnh nếu cần)"></textarea>
                <div class="flex gap-1 mt-1">
                    <input id="essay-dap-${i}" class="flex-1 p-1 border text-xs" placeholder="Đáp án (số)">
                    <input id="essay-goi-${i}" class="flex-1 p-1 border text-xs" placeholder="Gợi ý">
                </div>
            `;
            cont.appendChild(d);
            const de = d.querySelector(`#essay-de-${i}`);
            de.value = it.de || '';
            de.oninput = () => { essayItems[i].de = de.value; syncEssayToTextarea(); };
            const dap = d.querySelector(`#essay-dap-${i}`);
            dap.value = it.dap || '';
            dap.oninput = () => { essayItems[i].dap = dap.value; syncEssayToTextarea(); };
            const goi = d.querySelector(`#essay-goi-${i}`);
            goi.value = it.goi || '';
            goi.oninput = () => { essayItems[i].goi = goi.value; syncEssayToTextarea(); };
        });
        setupRichToolbars();
    }
    function addEssayItem() { essayItems.push({de:'', dap:'', goi:''}); renderEssayItems(); syncEssayToTextarea(); }
    function removeEssayItem(i) { essayItems.splice(i,1); renderEssayItems(); syncEssayToTextarea(); }

    function syncFillToTextarea() {
        const ta = el('lessonFill');
        if (!ta) return;
        ta.value = fillItems.map(i => `${i.de}|${i.manh}|${i.dap}|${i.goi}`).join('\n');
        ta.dispatchEvent(new Event('input', { bubbles: true }));
    }
    function renderFillItems() {
        const cont = el('fillItems');
        if (!cont) return;
        cont.innerHTML = '';
        fillItems.forEach((it, i) => {
            const d = document.createElement('div');
            d.className = 'p-2 border rounded bg-white text-xs';
            d.innerHTML = `
                <div class="flex items-center mb-1"><span class="font-bold">Bài ${i+1}</span><button type="button" class="ml-auto text-rose-600" onclick="removeFillItem(${i})">×</button></div>
                ${richToolbarHtml(`fill-de-${i}`)}
                <textarea id="fill-de-${i}" class="w-full p-1 border text-xs" placeholder="Câu có ___ (dán ảnh)"></textarea>
                <div class="grid grid-cols-3 gap-1 mt-1">
                    <input id="fill-manh-${i}" class="p-1 border text-xs" placeholder="Mảnh » ...">
                    <input id="fill-dap-${i}" class="p-1 border text-xs" placeholder="Đáp án">
                    <input id="fill-goi-${i}" class="p-1 border text-xs" placeholder="Gợi ý">
                </div>
            `;
            cont.appendChild(d);
            const de = d.querySelector(`#fill-de-${i}`); de.value = it.de||''; de.oninput = ()=>{fillItems[i].de=de.value; syncFillToTextarea();};
            ['manh','dap','goi'].forEach(k=>{ const inp=d.querySelector(`#fill-${k}-${i}`); inp.value=it[k]||''; inp.oninput=()=>{fillItems[i][k]=inp.value; syncFillToTextarea();}; });
        });
        setupRichToolbars();
    }
    function addFillItem(){ fillItems.push({de:'',manh:'',dap:'',goi:''}); renderFillItems(); syncFillToTextarea(); }
    function removeFillItem(i){ fillItems.splice(i,1); renderFillItems(); syncFillToTextarea(); }

    function syncDragToTextarea() {
        const ta = el('lessonDrag');
        if (!ta) return;
        ta.value = dragItems.map(i => `${i.de}|${i.trai}|${i.phai}|${i.map}|${i.goi}`).join('\n');
        ta.dispatchEvent(new Event('input', { bubbles: true }));
    }
    function renderDragItems() {
        const cont = el('dragItems');
        if (!cont) return;
        cont.innerHTML = '';
        dragItems.forEach((it, i) => {
            const d = document.createElement('div');
            d.className = 'p-2 border rounded bg-white text-xs';
            d.innerHTML = `
                <div class="flex items-center mb-1"><span class="font-bold">Bài ${i+1}</span><button type="button" class="ml-auto text-rose-600" onclick="removeDragItem(${i})">×</button></div>
                ${richToolbarHtml(`drag-de-${i}`)}
                <textarea id="drag-de-${i}" class="w-full p-1 border text-xs" placeholder="Đề (dán ảnh)"></textarea>
                <div class="grid grid-cols-4 gap-1 mt-1">
                    <input id="drag-trai-${i}" class="p-1 border text-xs" placeholder="Trái »">
                    <input id="drag-phai-${i}" class="p-1 border text-xs" placeholder="Phải »">
                    <input id="drag-map-${i}" class="p-1 border text-xs" placeholder="0-0,1-1">
                    <input id="drag-goi-${i}" class="p-1 border text-xs" placeholder="Gợi ý">
                </div>
            `;
            cont.appendChild(d);
            const de = d.querySelector(`#drag-de-${i}`); de.value = it.de||''; de.oninput = ()=>{dragItems[i].de=de.value; syncDragToTextarea();};
            ['trai','phai','map','goi'].forEach(k=>{ const inp=d.querySelector(`#drag-${k}-${i}`); inp.value=it[k]||''; inp.oninput=()=>{dragItems[i][k]=inp.value; syncDragToTextarea();}; });
        });
        setupRichToolbars();
    }
    function addDragItem(){ dragItems.push({de:'',trai:'',phai:'',map:'',goi:''}); renderDragItems(); syncDragToTextarea(); }
    function removeDragItem(i){ dragItems.splice(i,1); renderDragItems(); syncDragToTextarea(); }

    function syncQuestionsToTextarea() {
        const ta = el('lessonQuestions');
        if (!ta) return;
        ta.value = questionItems.map(i => `${i.cau}|${i.a}|${i.b}|${i.c}|${i.d}|${i.dung}`).join('\n');
        ta.dispatchEvent(new Event('input', { bubbles: true }));
    }
    function renderQuestionItems() {
        const cont = el('questionItems');
        if (!cont) return;
        cont.innerHTML = '';
        questionItems.forEach((it, i) => {
            const d = document.createElement('div');
            d.className = 'p-2 border rounded bg-white text-xs';
            d.innerHTML = `
                <div class="flex items-center mb-1"><span class="font-bold">Câu ${i+1}</span><button type="button" class="ml-auto text-rose-600" onclick="removeQuestionItem(${i})">×</button></div>
                ${richToolbarHtml(`q-cau-${i}`)}
                <textarea id="q-cau-${i}" class="w-full p-1 border text-xs" placeholder="Câu hỏi (dán ảnh nếu cần)"></textarea>
                <div class="grid grid-cols-5 gap-1 mt-1">
                    <input id="q-a-${i}" class="p-1 border text-xs" placeholder="A">
                    <input id="q-b-${i}" class="p-1 border text-xs" placeholder="B">
                    <input id="q-c-${i}" class="p-1 border text-xs" placeholder="C">
                    <input id="q-d-${i}" class="p-1 border text-xs" placeholder="D">
                    <input id="q-dung-${i}" class="p-1 border text-xs" placeholder="Đúng (A/B/C/D)">
                </div>
            `;
            cont.appendChild(d);
            const cau = d.querySelector(`#q-cau-${i}`); cau.value=it.cau||''; cau.oninput=()=>{questionItems[i].cau=cau.value; syncQuestionsToTextarea();};
            ['a','b','c','d','dung'].forEach(k=>{ const inp=d.querySelector(`#q-${k}-${i}`); inp.value=it[k]||''; inp.oninput=()=>{questionItems[i][k]=inp.value; syncQuestionsToTextarea();}; });
        });
        setupRichToolbars();
    }
    function addQuestionItem(){ questionItems.push({cau:'',a:'',b:'',c:'',d:'',dung:''}); renderQuestionItems(); syncQuestionsToTextarea(); }
    function removeQuestionItem(i){ questionItems.splice(i,1); renderQuestionItems(); syncQuestionsToTextarea(); }

    // parse from | format to items (for load)
    function parseEssayToItems(str) {
        return (str || '').split('\n').filter(Boolean).map(line => {
            const p = line.split('|').map(s=>s.trim());
            return {de: p[0]||'', dap: p[1]||'', goi: p[2]||''};
        });
    }
    function parseFillToItems(str) {
        return (str || '').split('\n').filter(Boolean).map(line => {
            const p = line.split('|').map(s=>s.trim());
            return {de: p[0]||'', manh: p[1]||'', dap: p[2]||'', goi: p[3]||''};
        });
    }
    function parseDragToItems(str) {
        return (str || '').split('\n').filter(Boolean).map(line => {
            const p = line.split('|').map(s=>s.trim());
            return {de: p[0]||'', trai: p[1]||'', phai: p[2]||'', map: p[3]||'', goi: p[4]||''};
        });
    }
    function parseQuestionToItems(str) {
        return (str || '').split('\n').filter(Boolean).map(line => {
            const p = line.split('|').map(s=>s.trim());
            return {cau: p[0]||'', a: p[1]||'', b: p[2]||'', c: p[3]||'', d: p[4]||'', dung: p[5]||''};
        });
    }

    function setupEditorFieldShortcuts() {
        document.querySelectorAll('#lessonEditorPanel input, #lessonEditorPanel textarea').forEach(field => {
            if (field.dataset.editorShortcutsReady) return;
            field.dataset.editorShortcutsReady = '1';
            field.addEventListener('keydown', event => {
                if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'a') {
                    event.preventDefault();
                    event.stopPropagation();
                    field.select();
                }
            }, true);
            field.addEventListener('paste', event => {
                const text = event.clipboardData?.getData('text/plain');
                if (typeof text !== 'string') return;
                event.preventDefault();
                event.stopPropagation();
                const start = field.selectionStart ?? field.value.length;
                const end = field.selectionEnd ?? start;
                field.setRangeText(text, start, end, 'end');
                field.dispatchEvent(new Event('input', { bubbles: true }));
            }, true);
            ['copy', 'cut'].forEach(type => {
                field.addEventListener(type, event => event.stopPropagation(), true);
            });
        });
    }

    function ensurePanel() {
        if (el('lessonEditorPanel') || el('lessonEditorBlocked')) return;
        const teacherMount = el('lessonDesignerMount');
        if (!teacherMount) return;
        if (localStorage.getItem('userRole') !== 'teacher') return;
        if (!teacherCanManageScope()) {
            teacherMount.innerHTML = `
                <section id="lessonEditorBlocked" class="bg-amber-50 rounded-xl border border-amber-200 mb-8 p-6 text-sm text-amber-900">
                    <p class="font-bold text-base mb-2"><i class="fas fa-lock mr-2"></i>Chưa được mở quyền soạn bài</p>
                    <p>Admin cần tick lộ trình Toán 4/5/6/7/8/9 trong phần <strong>Lộ trình được phép soạn</strong> rồi giáo viên đăng nhập lại.</p>
                </section>
            `;
            return;
        }
        const dashboard = teacherMount;

        const panel = document.createElement('section');
        panel.id = 'lessonEditorPanel';
        panel.className = 'bg-white rounded-xl shadow-lg border border-slate-200 mb-8 p-6';
        panel.innerHTML = `
            <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                <div>
                    <h3 class="font-bold text-slate-800 text-lg">
                        <i class="fas fa-book-open text-teal-600 mr-2"></i>Tạo bài học cho lộ trình
                    </h3>
                    <p id="lessonEditorScopeHint" class="text-sm text-slate-500 mt-1">Nhập nội dung theo từng mục. Công thức viết bằng LaTeX trong dấu <code>$...$</code>.</p>
                </div>
                <div class="flex flex-wrap gap-2" id="subjectPills"></div>
            </div>

            <div class="mt-5 grid grid-cols-1 xl:grid-cols-[300px_1fr] gap-5">
                <aside class="space-y-4">
                    <div>
                        <label class="block text-sm font-bold text-slate-700 mb-1">Chọn bài học</label>
                        <select id="lessonSelect" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></select>
                    </div>
                    <button id="newLessonBtn" type="button" class="w-full bg-slate-100 hover:bg-slate-200 text-slate-800 px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-plus mr-1"></i>Tạo bài mới
                    </button>
                    <button id="duplicateLessonBtn" type="button" class="w-full bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-copy mr-1"></i>Nhân bản bài đang chọn
                    </button>
                    <button id="deleteLessonBtn" type="button" class="w-full bg-rose-50 hover:bg-rose-100 border border-rose-200 text-rose-700 px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-trash mr-1"></i>Xóa bài đang chọn
                    </button>
                    <button id="lessonReloadBtn" type="button" class="w-full bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-rotate-right mr-1"></i>Tải lại dữ liệu
                    </button>
                    <button id="viewSubmissionsBtn" type="button" class="w-full bg-sky-600 hover:bg-sky-700 text-white px-4 py-2.5 rounded font-bold text-sm shadow">
                        <i class="fas fa-cloud-arrow-down mr-1"></i>Xem bài nộp HS
                    </button>
                    <div class="rounded border border-teal-100 bg-teal-50 p-3 text-sm leading-6 text-teal-900">
                        Ví dụ công thức: <code>$A=\\{1,2,3\\}$</code>, <code>$x \\in A$</code>. Học sinh sẽ nhìn thấy công thức đã render.
                    </div>
                </aside>

                <form id="lessonForm" class="space-y-5">
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        <label class="block text-sm font-bold text-slate-700">Môn học
                            <select id="lessonSubject" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none">
                                ${SUBJECTS.map(item => `<option value="${item.title}">${item.label}</option>`).join('')}
                            </select>
                        </label>
                        <label class="block text-sm font-bold text-slate-700">Chương
                            <input id="lessonChapter" list="lessonChapterOptions" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Chương 1: Số tự nhiên">
                            <datalist id="lessonChapterOptions"></datalist>
                            <button id="renameChapterBtn" type="button" class="mt-2 text-xs font-bold text-teal-700 hover:text-teal-900 underline">
                                Đổi tên chương cho tất cả bài trong chương này
                            </button>
                        </label>
                        <label class="block text-sm font-bold text-slate-700">Tên bài
                            <input id="lessonTitleInput" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Bài 1: Tập hợp">
                        </label>
                        <div class="grid grid-cols-[1fr_110px] gap-3">
                            <label class="block text-sm font-bold text-slate-700">Slug
                                <input id="lessonSlug" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="math6-c1-b1-tap-hop">
                            </label>
                            <label class="block text-sm font-bold text-slate-700">Thứ tự
                                <input id="lessonOrder" type="number" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" value="1">
                            </label>
                        </div>
                    </div>

                    <label class="flex items-start gap-2 rounded border border-teal-200 bg-teal-50 px-3 py-2.5 text-sm font-bold text-teal-900">
                        <input id="lessonPublished" type="checkbox" class="mt-0.5 w-4 h-4 text-teal-600 rounded">
                        <span>Mở bài này cho học sinh <span class="block text-xs font-medium text-teal-800">Mặc định tắt — chỉ bật khi bạn sẵn sàng cho lớp học bài này.</span></span>
                    </label>

                    <label class="block text-sm font-bold text-slate-700">Mục tiêu bài học
                        <textarea id="lessonGoalInput" rows="2" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Sau bài này học sinh cần nắm được..."></textarea>
                    </label>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    <label class="block text-sm font-bold text-slate-700">Lý thuyết
                        <span class="block text-xs font-medium text-slate-500 mb-1">Enter 1 lần = xuống dòng. Enter 2 lần = tách đoạn (dùng với <code class="font-mono text-[11px]">[AI]</code>). Định dạng: <code class="font-mono text-[11px]">**đậm**</code>, <code class="font-mono text-[11px]">*nghiêng*</code>, <code class="font-mono text-[11px]">++gạch chân++</code>, ảnh: <code class="font-mono text-[11px]">![mô tả](link)</code>. Công thức: <code class="font-mono text-[11px]">$...$</code>.</span>
                        ${richToolbarHtml('lessonTheory')}
                        <textarea id="lessonTheory" rows="8" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Ví dụ
                        <span class="block text-xs font-medium text-slate-500 mb-1">Enter 2 lần = tách ví dụ. Dòng đầu là tiêu đề; Enter 1 lần trong lời giải = xuống dòng. Cùng quy tắc định dạng và <code class="font-mono text-[11px]">[AI]</code> như nội dung bài học.</span>
                        ${richToolbarHtml('lessonExamples')}
                        <textarea id="lessonExamples" rows="8" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                    </label>
                    </div>

                    <label class="block text-sm font-bold text-slate-700">Bài tập nộp giáo viên
                        <span class="block text-xs font-medium text-slate-500 mb-1">Cùng cấu trúc ví dụ — mỗi dạng một khối (Enter 2 lần). Học sinh làm xong tất cả dạng rồi <strong>nộp chung một lần</strong> lên Google Drive. Không cần <code class="font-mono text-[11px]">[AI]</code> trừ khi muốn nút giải thích.</span>
                        ${richToolbarHtml('lessonSelfPractice')}
                        <textarea id="lessonSelfPractice" rows="6" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                    </label>

                    <section id="selfPracticeSubmissionsPanel" class="rounded-xl border-2 border-sky-300 bg-sky-50 p-4 scroll-mt-24">
                        <div class="flex flex-wrap items-center justify-between gap-2">
                            <div>
                                <h4 class="text-base font-bold text-sky-950"><i class="fas fa-folder-open mr-1"></i> Bài nộp học sinh (Google Drive)</h4>
                                <p class="text-xs text-sky-800 mt-1">Học sinh lớp bạn dạy nộp ở tab <strong>Bài tập</strong> trong lộ trình. Bấm link tệp để xem trên Drive.</p>
                            </div>
                            <button type="button" id="reloadSelfPracticeSubmissionsBtn" class="rounded border border-sky-300 bg-white px-3 py-1.5 text-xs font-bold text-sky-800 hover:bg-sky-100">Tải lại</button>
                        </div>
                        <div id="selfPracticeSubmissionsBody" class="mt-3 text-sm text-sky-900">Chọn bài học để xem bài nộp.</div>
                    </section>

                    <div class="space-y-6">
                        <!-- Bài tập tự luận (linh hoạt, có thể dán hình vào Đề) -->
                        <div>
                            <label class="block text-sm font-bold text-slate-700">Bài tập tự luận
                                <span class="block text-xs font-medium text-slate-500 mb-1">Mỗi item: Đề (hỗ trợ ảnh) | Đáp án (số) | Gợi ý. Thêm từng bài một, dán hình vào phần Đề nếu cần.</span>
                            </label>
                            <div id="essayItems" class="space-y-3"></div>
                            <button type="button" onclick="addEssayItem()" class="mt-2 text-xs px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded">+ Thêm bài tập tự luận</button>
                            <textarea id="lessonEssay" class="hidden"></textarea>
                        </div>
                        <!-- Kéo vào ô trống -->
                        <div>
                            <label class="block text-sm font-bold text-slate-700">Kéo vào ô trống
                                <span class="block text-xs font-medium text-slate-500 mb-1">Mỗi item: Đề (hỗ trợ ảnh) | Mảnh » ... | Đáp án | Gợi ý</span>
                            </label>
                            <div id="fillItems" class="space-y-3"></div>
                            <button type="button" onclick="addFillItem()" class="mt-2 text-xs px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded">+ Thêm bài kéo thả</button>
                            <textarea id="lessonFill" class="hidden"></textarea>
                        </div>
                        <!-- Nối / sắp xếp -->
                        <div>
                            <label class="block text-sm font-bold text-slate-700">Nối ô / sắp xếp
                                <span class="block text-xs font-medium text-slate-500 mb-1">Mỗi item: Đề (hỗ trợ ảnh) | ... | ... | map | Gợi ý</span>
                            </label>
                            <div id="dragItems" class="space-y-3"></div>
                            <button type="button" onclick="addDragItem()" class="mt-2 text-xs px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded">+ Thêm bài nối/sắp xếp</button>
                            <textarea id="lessonDrag" class="hidden"></textarea>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        <label class="block text-sm font-bold text-slate-700">Kỹ năng cần đạt
                            <span class="block text-xs font-medium text-slate-500 mb-1">Mỗi dòng: id | Tên kỹ năng | target</span>
                            <textarea id="lessonSkills" rows="6" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                        </label>
                        <label class="block text-sm font-bold text-slate-700">Nhiệm vụ học sinh
                            <span class="block text-xs font-medium text-slate-500 mb-1">Mỗi dòng là một việc cần làm.</span>
                            <textarea id="lessonTasks" rows="6" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                        </label>
                    </div>

                    <label class="block text-sm font-bold text-slate-700">Video YouTube bài giảng
                        <span class="block text-xs font-medium text-slate-500 mb-1">Mỗi dòng: Tiêu đề | Link YouTube. Có thể để trống nếu bài chưa có video.</span>
                        <textarea id="lessonVideos" rows="4" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Bài giảng Tập hợp | https://www.youtube.com/watch?v=..."></textarea>
                    </label>

                    <div>
                        <label class="block text-sm font-bold text-slate-700">Câu hỏi trắc nghiệm
                            <span class="block text-xs font-medium text-slate-500 mb-1">Mỗi câu: Câu hỏi (hỗ trợ ảnh) | A | B | C | D | đáp án. Thêm từng câu, dán hình vào Câu hỏi nếu cần.</span>
                        </label>
                        <div id="questionItems" class="space-y-3"></div>
                        <button type="button" onclick="addQuestionItem()" class="mt-2 text-xs px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded">+ Thêm câu hỏi trắc nghiệm</button>
                        <textarea id="lessonQuestions" class="hidden"></textarea>
                    </div>

                    <div id="lessonPreview" class="rounded border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700"></div>

                    <div class="flex flex-wrap gap-3">
                        <button id="saveLessonBtn" class="bg-teal-600 hover:bg-teal-700 text-white px-5 py-2.5 rounded shadow font-bold text-sm transition flex items-center gap-2">
                            <i class="fas fa-save"></i>Lưu bài học
                        </button>
                        <button id="seedLessonBtn" type="button" class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-5 py-2.5 rounded shadow-sm font-bold text-sm transition">
                            Điền mẫu Bài 1
                        </button>
                    </div>
                </form>
            </div>
        `;
        dashboard.prepend(panel);

        el('lessonReloadBtn').onclick = refreshLessons;
        el('lessonSelect').onchange = () => fillForm(el('lessonSelect').value);
        el('newLessonBtn').onclick = newLesson;
        el('duplicateLessonBtn').onclick = duplicateLesson;
        el('deleteLessonBtn').onclick = deleteLesson;
        el('renameChapterBtn').onclick = renameChapter;
        el('saveLessonBtn').onclick = saveLesson;
        el('seedLessonBtn').onclick = fillSeed;
        el('lessonTitleInput').addEventListener('blur', suggestSlug);
        el('lessonChapter').addEventListener('blur', suggestSlug);
        el('lessonSubject').addEventListener('change', event => {
            if (isPageScopedEditor()) {
                event.target.value = PAGE_SUBJECT;
                return;
            }
            selectedSubject = event.target.value;
            renderSubjectPills();
            suggestSlug();
        });
        ['lessonGoalInput', 'lessonTheory', 'lessonExamples', 'lessonSelfPractice', 'lessonEssay', 'lessonFill', 'lessonDrag', 'lessonSkills', 'lessonTasks', 'lessonVideos', 'lessonQuestions'].forEach(id => {
            const field = el(id);
            if (field) field.addEventListener('input', renderPreview);
        });
        el('reloadSelfPracticeSubmissionsBtn')?.addEventListener('click', () => loadSelfPracticeSubmissions());
        el('viewSubmissionsBtn')?.addEventListener('click', () => {
            el('selfPracticeSubmissionsPanel')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
            loadSelfPracticeSubmissions();
        });
        setupEditorFieldShortcuts();
        setupRichToolbars();
        injectLessonEditorStyles();

        // init dynamic flexible lists (empty for new)
        essayItems = [];
        fillItems = [];
        dragItems = [];
        questionItems = [];
        renderEssayItems();
        renderFillItems();
        renderDragItems();
        renderQuestionItems();

        applyPageScopeUi();
        renderSubjectPills();
    }

    function applyPageScopeUi() {
        const scoped = isPageScopedEditor();
        const pills = el('subjectPills');
        const subjectSelect = el('lessonSubject');
        const hint = el('lessonEditorScopeHint');

        if (scoped) {
            selectedSubject = PAGE_SUBJECT;
        }

        if (pills) {
            pills.classList.toggle('hidden', scoped);
            if (scoped) pills.innerHTML = '';
        }

        if (subjectSelect) {
            if (scoped) {
                subjectSelect.innerHTML = `<option value="${escapeHtml(PAGE_SUBJECT)}">${escapeHtml(PAGE_SUBJECT)}</option>`;
                subjectSelect.value = PAGE_SUBJECT;
                subjectSelect.disabled = true;
            } else {
                const subjects = scopedSubjects();
                subjectSelect.disabled = subjects.length <= 1;
                subjectSelect.innerHTML = subjects.map(item => `<option value="${item.title}">${item.label}</option>`).join('');
                if (!subjects.some(item => item.title === selectedSubject)) {
                    selectedSubject = subjects[0]?.title || selectedSubject;
                }
                subjectSelect.value = selectedSubject;
            }
        }

        if (hint) {
            hint.innerHTML = scoped
                ? `Soạn bài cho <strong>${escapeHtml(PAGE_SUBJECT)}</strong>. Chỉ hiển thị bài học thuộc lộ trình này. Công thức viết bằng LaTeX trong dấu <code>$...$</code>.`
                : 'Nhập nội dung theo từng mục. Công thức viết bằng LaTeX trong dấu <code>$...$</code>.';
        }
    }

    function injectLessonEditorStyles() {
        if (document.getElementById('lessonEditorStyles')) return;
        const style = document.createElement('style');
        style.id = 'lessonEditorStyles';
        style.textContent = `
            .lesson-rich-toolbar { display: flex; flex-wrap: wrap; gap: 6px; margin: 6px 0; }
            .lesson-rich-toolbar button {
                display: inline-flex; align-items: center; gap: 4px;
                padding: 4px 10px; border: 1px solid #cbd5e1; border-radius: 6px;
                background: #fff; color: #334155; font-size: 0.78rem; font-weight: 700; cursor: pointer;
            }
            .lesson-rich-toolbar button:hover { background: #f8fafc; border-color: #94a3b8; }
        `;
        document.head.appendChild(style);
    }

    function renderSubjectPills() {
        const box = el('subjectPills');
        if (!box) return;
        if (isPageScopedEditor()) {
            applyPageScopeUi();
            return;
        }
        const subjects = scopedSubjects();
        if (!subjects.length) {
            box.classList.add('hidden');
            box.innerHTML = '';
            return;
        }
        box.classList.remove('hidden');
        box.innerHTML = subjects.map(item => {
            const active = selectedSubject === item.title;
            return `<button type="button" data-subject="${item.title}" class="subject-pill rounded px-3 py-2 text-sm font-bold ${active ? 'bg-teal-700 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}">${item.label}</button>`;
        }).join('');
        box.querySelectorAll('.subject-pill').forEach(button => {
            button.onclick = () => {
                selectedSubject = button.dataset.subject;
                if (el('lessonSubject')) el('lessonSubject').value = selectedSubject;
                renderSubjectPills();
                renderSelect();
            };
        });
    }

    function renderSelect() {
        const select = el('lessonSelect');
        if (!select) return;
        const items = lessonsForScope();
        if (!items.length) {
            select.innerHTML = '<option value="">Chưa có bài học</option>';
            return;
        }
        const scoped = isPageScopedEditor();
        select.innerHTML = items.map(lesson => {
            const chapter = String(lesson.chapter || '').trim();
            const prefix = chapter ? `${chapter} · ` : '';
            const label = scoped
                ? `${prefix}${lesson.title}`
                : `${prefix}${lesson.title} (${lesson.subject})`;
            return `<option value="${escapeHtml(lesson.slug)}">${escapeHtml(label)}</option>`;
        }).join('');
        if (items.some(item => item.slug === currentSlug)) select.value = currentSlug;
        renderChapterOptions();
    }

    function scopedEmptyLesson() {
        return {
            ...defaults,
            subject: PAGE_SUBJECT,
            slug: '',
            chapter: '',
            title: '',
            order_index: lessonsForScope().length + 1,
            is_published: false,
            goal_text: '',
            theory: [],
            examples: [],
            essay_exercises: [],
            fill_exercises: [],
            drag_exercises: [],
            videos: [],
            skills: [],
            tasks: [],
            questions: []
        };
    }

    function fillForm(slug) {
        const scopedLessons = lessonsForScope();
        const fallback = isPageScopedEditor() ? scopedEmptyLesson() : defaults;
        const lesson = scopedLessons.find(item => item.slug === slug) || scopedLessons[0] || fallback;
        currentSlug = lesson.slug || '';
        currentLessonId = lesson.id ? Number(lesson.id) : null;
        selectedSubject = isPageScopedEditor() ? PAGE_SUBJECT : (lesson.subject || selectedSubject);
        if (el('lessonSelect')) el('lessonSelect').value = lesson.slug;
        el('lessonSubject').value = selectedSubject;
        el('lessonSlug').value = lesson.slug || '';
        el('lessonChapter').value = lesson.chapter || '';
        if (el('lessonChapter')) el('lessonChapter').dataset.renameSource = lesson.chapter || '';
        el('lessonTitleInput').value = lesson.title || '';
        el('lessonOrder').value = lesson.order_index || 1;
        el('lessonPublished').checked = !!lesson.is_published;
        el('lessonGoalInput').value = lesson.goal || lesson.goal_text || '';
        el('lessonTheory').value = formatTheoryBlocks(lesson.theory);
        el('lessonExamples').value = formatExamples(lesson.examples);
        if (el('lessonSelfPractice')) el('lessonSelfPractice').value = formatExamples(lesson.self_practice || []);
        el('lessonEssay').value = formatEssayExercises(lesson.essay_exercises);
        el('lessonFill').value = formatFillExercises(lesson.fill_exercises);
        el('lessonDrag').value = formatDragExercises(lesson.drag_exercises);
        el('lessonVideos').value = formatVideos(lesson.videos);
        el('lessonSkills').value = formatSkills(lesson.skills);
        el('lessonTasks').value = Array.isArray(lesson.tasks) ? lesson.tasks.join('\n') : '';
        el('lessonQuestions').value = formatQuestions(lesson.questions);

        // populate dynamic items for flexible UI
        essayItems = parseEssayToItems(el('lessonEssay').value || '');
        fillItems = parseFillToItems(el('lessonFill').value || '');
        dragItems = parseDragToItems(el('lessonDrag').value || '');
        questionItems = parseQuestionToItems(el('lessonQuestions').value || '');
        renderEssayItems();
        renderFillItems();
        renderDragItems();
        renderQuestionItems();

        renderSubjectPills();
        renderPreview();
        loadSelfPracticeSubmissions();
    }

    async function loadSelfPracticeSubmissions() {
        const panel = el('selfPracticeSubmissionsPanel');
        const body = el('selfPracticeSubmissionsBody');
        if (!panel || !body) return;
        if (!currentLessonId) {
            body.innerHTML = '<p class="text-sky-800">Chọn hoặc lưu một bài học để xem bài nộp của học sinh.</p>';
            return;
        }
        body.innerHTML = '<span class="text-slate-500"><i class="fas fa-spinner fa-spin mr-1"></i>Đang tải bài nộp...</span>';
        try {
            const res = await fetch(`api/lesson_self_practice.php?action=list&lesson_id=${encodeURIComponent(currentLessonId)}`, {
                credentials: 'include',
                cache: 'no-store'
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Không tải được bài nộp.');
            const submissions = Array.isArray(data.submissions) ? data.submissions : [];
            if (!submissions.length) {
                body.innerHTML = '<p class="text-sky-800">Chưa có học sinh lớp bạn dạy nộp bài cho bài học này. (Kiểm tra Admin đã gán <strong>lớp</strong> cho tài khoản giáo viên chưa.)</p>';
                return;
            }
            body.innerHTML = `
                <div class="overflow-x-auto rounded-lg border border-sky-200 bg-white">
                    <table class="min-w-full text-left text-xs">
                        <thead class="bg-sky-100 font-bold uppercase text-sky-800">
                            <tr>
                                <th class="px-3 py-2">Thời gian</th>
                                <th class="px-3 py-2">Học sinh</th>
                                <th class="px-3 py-2">Loại</th>
                                <th class="px-3 py-2">Tệp</th>
                                <th class="px-3 py-2">Ghi chú</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${submissions.map(row => `
                                <tr class="border-t border-sky-100">
                                    <td class="px-3 py-2 whitespace-nowrap">${String(row.submitted_at || '').replace('T', ' ').slice(0, 16)}</td>
                                    <td class="px-3 py-2">
                                        <div class="font-semibold">${escapeHtml(row.student_name || '')}</div>
                                        <div class="text-sky-700">${escapeHtml(row.class_name || '')}</div>
                                    </td>
                                    <td class="px-3 py-2">${escapeHtml(row.item_title || ('Dạng ' + ((row.item_index || 0) + 1)))}</td>
                                    <td class="px-3 py-2">
                                        ${(row.files || []).map(file => `
                                            <a href="${escapeHtml(file.view_url)}" target="_blank" rel="noopener" class="block font-bold text-sky-800 underline">${escapeHtml(file.original_name)}</a>
                                        `).join('') || '—'}
                                    </td>
                                    <td class="px-3 py-2 text-slate-600">${escapeHtml(row.note || '')}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        } catch (err) {
            body.innerHTML = `<p class="text-rose-700">${escapeHtml(err.message || 'Không tải được bài nộp.')}</p>`;
        }
    }

    function fillSeed() {
        selectedSubject = isPageScopedEditor() ? PAGE_SUBJECT : defaults.subject;
        el('lessonSubject').value = selectedSubject;
        el('lessonSlug').value = defaults.slug;
        el('lessonChapter').value = defaults.chapter;
        el('lessonTitleInput').value = defaults.title;
        el('lessonOrder').value = defaults.order_index;
        el('lessonPublished').checked = true;
        el('lessonGoalInput').value = defaults.goal_text;
        el('lessonTheory').value = formatTheoryBlocks(defaults.theory.map((text, index) => (
            index === 1 ? { text, ai: true } : text
        )));
        el('lessonExamples').value = formatExamples(defaults.examples);
        if (el('lessonSelfPractice')) el('lessonSelfPractice').value = '';
        el('lessonEssay').value = 'Viết tập hợp A gồm các số tự nhiên nhỏ hơn 4 | A={0,1,2,3} | Các số tự nhiên bắt đầu từ 0.';
        el('lessonFill').value = 'Nếu A={1,2,3} thì 2 ___ A | thuộc > không thuộc > ∈ | thuộc | 2 là phần tử của A.';
        el('lessonDrag').value = 'Nối khái niệm | 1 » 2 » 3 | một » hai » ba | 0-0,1-1,2-2 | Ghép đúng từng cặp.';
        el('lessonVideos').value = formatVideos(defaults.videos);
        el('lessonSkills').value = formatSkills(defaults.skills);
        el('lessonTasks').value = defaults.tasks.join('\n');
        el('lessonQuestions').value = formatQuestions(defaults.questions);
        essayItems = parseEssayToItems(el('lessonEssay').value);
        fillItems = parseFillToItems(el('lessonFill').value);
        dragItems = parseDragToItems(el('lessonDrag').value);
        questionItems = parseQuestionToItems(el('lessonQuestions').value);
        renderEssayItems();
        renderFillItems();
        renderDragItems();
        renderQuestionItems();
        renderSubjectPills();
        renderPreview();
    }

    function newLesson() {
        currentLessonId = null;
        currentSlug = '';
        const order = lessons.filter(lesson => lesson.subject === selectedSubject).length + 1;
        el('lessonSubject').value = selectedSubject;
        el('lessonChapter').value = '';
        el('lessonChapter').dataset.renameSource = '';
        el('lessonTitleInput').value = '';
        el('lessonSlug').value = '';
        el('lessonOrder').value = order;
        el('lessonPublished').checked = false;
        el('lessonGoalInput').value = '';
        el('lessonTheory').value = '';
        el('lessonExamples').value = '';
        el('lessonEssay').value = '';
        el('lessonFill').value = '';
        el('lessonDrag').value = '';
        el('lessonVideos').value = '';
        el('lessonSkills').value = 'nhan_biet | Nhan biet kien thuc | 80';
        el('lessonTasks').value = 'Đọc lý thuyết\nXem ví dụ\nLàm bài luyện tập';
        el('lessonQuestions').value = '';
        essayItems = [];
        fillItems = [];
        dragItems = [];
        questionItems = [];
        renderEssayItems();
        renderFillItems();
        renderDragItems();
        renderQuestionItems();
        renderPreview();
    }

    function suggestSlug() {
        if (el('lessonSlug').value.trim()) return;
        const subjectCode = SUBJECTS.find(item => item.title === el('lessonSubject').value)?.id || 'lesson';
        const value = [subjectCode, el('lessonChapter').value, el('lessonTitleInput').value].join(' ');
        el('lessonSlug').value = slugify(value);
    }

    function renderPreview() {
        const preview = el('lessonPreview');
        if (!preview) return;
        let questionCount = 0;
        try { questionCount = parseQuestions(el('lessonQuestions').value, parseSkills(el('lessonSkills').value)).length; } catch { questionCount = 0; }
        const essayCount = parseEssayExercises(el('lessonEssay').value).length;
        const fillCount = parseFillExercises(el('lessonFill').value).length;
        const dragCount = parseDragExercises(el('lessonDrag').value).length;
        preview.innerHTML = `
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div><div class="text-xs text-slate-500">Nội dung</div><div class="font-bold">${(() => { const blocks = parseTheoryBlocks(el('lessonTheory').value); return `${blocks.length} đoạn · ${blocks.filter(block => block.ai).length} có AI`; })()}</div></div>
                <div><div class="text-xs text-slate-500">Ví dụ</div><div class="font-bold">${parseExamples(el('lessonExamples').value).length} mục</div></div>
                <div><div class="text-xs text-slate-500">Bài tập</div><div class="font-bold">${parseExamples(el('lessonSelfPractice')?.value || '').length} dạng</div></div>
                <div><div class="text-xs text-slate-500">Kỹ năng</div><div class="font-bold">${parseSkills(el('lessonSkills').value).length} kỹ năng</div></div>
                <div><div class="text-xs text-slate-500">Bài tập</div><div class="font-bold">${essayCount + fillCount + dragCount + questionCount}</div></div>
            </div>
        `;
    }

    async function saveLesson(event) {
        event.preventDefault();
        suggestSlug();
        // sync dynamic lists to hidden textareas (for save compatibility)
        syncEssayToTextarea();
        syncFillToTextarea();
        syncDragToTextarea();
        syncQuestionsToTextarea();
        const skills = parseSkills(el('lessonSkills').value);
        const payload = {
            action: 'save_content',
            id: currentLessonId || undefined,
            slug: el('lessonSlug').value.trim(),
            subject: (isPageScopedEditor() ? PAGE_SUBJECT : el('lessonSubject').value).trim(),
            chapter: el('lessonChapter').value.trim(),
            title: el('lessonTitleInput').value.trim(),
            order_index: Number(el('lessonOrder').value) || 0,
            is_published: el('lessonPublished').checked,
            goal_text: el('lessonGoalInput').value.trim(),
            theory: parseTheoryBlocks(el('lessonTheory').value),
            examples: parseExamples(el('lessonExamples').value),
            self_practice: parseExamples(el('lessonSelfPractice')?.value || ''),
            essay_exercises: parseEssayExercises(el('lessonEssay').value),
            fill_exercises: parseFillExercises(el('lessonFill').value),
            drag_exercises: parseDragExercises(el('lessonDrag').value),
            videos: parseVideos(el('lessonVideos').value),
            skills,
            tasks: parseLines(el('lessonTasks').value),
            questions: parseQuestions(el('lessonQuestions').value, skills)
        };
        if (!payload.slug || !payload.title) {
            alert('Cần nhập slug và tên bài.');
            return;
        }
        const btn = el('saveLessonBtn');
        const old = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>Đang lưu...';
        try {
            const res = await fetch('api/lessons.php', {
                method: 'POST',
                credentials: 'include',
                headers: lessonRequestHeaders(),
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Không lưu được bài học.');
            currentSlug = data.slug || payload.slug;
            currentLessonId = data.id ? Number(data.id) : currentLessonId;
            selectedSubject = payload.subject;
            if (el('lessonChapter')) el('lessonChapter').dataset.renameSource = payload.chapter;
            await refreshLessons();
            if (typeof window.refreshAdminProgress === 'function') window.refreshAdminProgress();
            alert('Đã lưu bài học.');
        } catch (e) {
            alert(e.message || 'Không lưu được bài học.');
        } finally {
            btn.disabled = false;
            btn.innerHTML = old;
        }
    }

    async function postLessonAction(action, body) {
        const res = await fetch('api/lessons.php', {
            method: 'POST',
            credentials: 'include',
            headers: lessonRequestHeaders(),
            body: JSON.stringify({ action, ...body })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Thao tác thất bại.');
        return data;
    }

    async function duplicateLesson() {
        const slug = el('lessonSlug').value.trim() || currentSlug;
        if (!slug && !currentLessonId) {
            alert('Chọn một bài học để nhân bản.');
            return;
        }
        const btn = el('duplicateLessonBtn');
        const old = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>Đang nhân bản...';
        try {
            const data = await postLessonAction('duplicate_lesson', {
                id: currentLessonId || undefined,
                slug: slug || undefined
            });
            currentSlug = data.slug;
            currentLessonId = data.id ? Number(data.id) : null;
            await refreshLessons();
            if (typeof window.refreshAdminProgress === 'function') window.refreshAdminProgress();
            alert(`Đã tạo bản sao: ${data.title || 'Bài mới'}. Bản sao mặc định chưa mở cho học sinh.`);
        } catch (e) {
            alert(e.message || 'Không nhân bản được bài học.');
        } finally {
            btn.disabled = false;
            btn.innerHTML = old;
        }
    }

    async function deleteLesson() {
        const slug = el('lessonSlug').value.trim() || currentSlug;
        const title = el('lessonTitleInput').value.trim() || 'bài học này';
        if (!slug && !currentLessonId) {
            alert('Chọn một bài học để xóa.');
            return;
        }
        const confirmed = confirm(
            `Xóa "${title}"?\n\nTiến độ học sinh của bài này cũng sẽ bị xóa. Thao tác không thể hoàn tác.`
        );
        if (!confirmed) return;

        const btn = el('deleteLessonBtn');
        const old = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>Đang xóa...';
        try {
            await postLessonAction('delete_lesson', {
                id: currentLessonId || undefined,
                slug: slug || undefined
            });
            currentLessonId = null;
            currentSlug = '';
            await refreshLessons();
            if (typeof window.refreshAdminProgress === 'function') window.refreshAdminProgress();
            alert('Đã xóa bài học.');
        } catch (e) {
            alert(e.message || 'Không xóa được bài học.');
        } finally {
            btn.disabled = false;
            btn.innerHTML = old;
        }
    }

    async function renameChapter() {
        const subject = (isPageScopedEditor() ? PAGE_SUBJECT : el('lessonSubject').value).trim();
        const oldChapter = String(el('lessonChapter').dataset.renameSource || '').trim();
        if (!oldChapter) {
            alert('Chọn một bài đã có chương, hoặc lưu bài với tên chương trước khi đổi tên hàng loạt.');
            return;
        }
        const newChapter = prompt(
            `Đổi tên "${oldChapter}" thành tên mới cho tất cả bài thuộc môn "${subject}":`,
            oldChapter
        );
        if (newChapter === null) return;
        const trimmed = newChapter.trim();
        if (!oldChapter || !trimmed) {
            alert('Cần tên chương cũ và tên chương mới.');
            return;
        }
        if (oldChapter === trimmed) return;

        try {
            const data = await postLessonAction('rename_chapter', {
                subject,
                old_chapter: oldChapter,
                new_chapter: trimmed
            });
            el('lessonChapter').value = trimmed;
            el('lessonChapter').dataset.renameSource = trimmed;
            await refreshLessons();
            alert(`Đã đổi tên chương cho ${data.updated || 0} bài.`);
        } catch (e) {
            alert(e.message || 'Không đổi tên chương được.');
        }
    }

    async function refreshLessons() {
        const res = await fetch('api/lessons.php?admin=1&debug=1', {
            credentials: 'include',
            headers: lessonRequestHeaders(false),
            cache: 'no-store'
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Không tải được bài học.');
        lessons = data.lessons || [];
        if (isPageScopedEditor()) {
            selectedSubject = PAGE_SUBJECT;
        }
        const scopedLessons = lessonsForScope();
        if (!scopedLessons.some(item => item.slug === currentSlug)) {
            currentSlug = scopedLessons[0]?.slug || (isPageScopedEditor() ? '' : defaults.slug);
        }
        applyPageScopeUi();
        renderSubjectPills();
        renderSelect();
        fillForm(currentSlug);
        document.dispatchEvent(new CustomEvent('adminLessonsChanged', { detail: { lessons } }));
    }

    function lessonRequestHeaders(hasBody = true) {
        const headers = hasBody ? { 'Content-Type': 'application/json' } : {};
        const adminKey = getAdminKey();
        if (adminKey) headers['X-Admin-Key'] = adminKey;
        return headers;
    }

    function wrapLoadUsers() {
        if (typeof window.loadUsers !== 'function' || window.loadUsers.__lessonWrapped) return;
        const original = window.loadUsers;
        const wrapped = async function (...args) {
            const result = await original.apply(this, args);
            ensurePanel();
            await refreshLessons();
            if (typeof window.ensureAdminTabs === 'function') window.ensureAdminTabs();
            return result;
        };
        wrapped.__lessonWrapped = true;
        window.loadUsers = wrapped;
    }

    function bootIfReady() {
        ensurePanel();
        wrapLoadUsers();
        const canLoadFromTeacherPage = !!el('lessonDesignerMount') && localStorage.getItem('userRole') === 'teacher';
        if (getAdminKey() || canLoadFromTeacherPage) refreshLessons().catch(console.warn);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootIfReady);
    } else {
        bootIfReady();
    }
})();
