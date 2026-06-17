(function () {
    const SUBJECTS = [
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

    let lessons = [];
    let currentSlug = defaults.slug;
    let selectedSubject = 'Toán 6';

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

    function parseExamples(text) {
        return parseLines(text).map(line => {
            const parts = line.includes('||') ? line.split('||') : line.split('|');
            const [title, ...bodyParts] = parts;
            return { title: (title || '').trim(), body: bodyParts.join(parts.length > 2 ? '|' : '').trim() };
        });
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

    function formatExamples(items) {
        return (items || []).map(item => `${item.title || ''} | ${item.body || ''}`).join('\n');
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
            });
            ['copy', 'cut', 'paste'].forEach(type => {
                field.addEventListener(type, event => event.stopPropagation());
            });
        });
    }

    function ensurePanel() {
        if (el('lessonEditorPanel')) return;
        const dashboard = el('dashboardSection');
        if (!dashboard) return;

        const panel = document.createElement('section');
        panel.id = 'lessonEditorPanel';
        panel.className = 'bg-white rounded-xl shadow-lg border border-slate-200 mb-8 p-6';
        panel.innerHTML = `
            <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                <div>
                    <h3 class="font-bold text-slate-800 text-lg">
                        <i class="fas fa-book-open text-teal-600 mr-2"></i>Tạo bài học cho lộ trình
                    </h3>
                    <p class="text-sm text-slate-500 mt-1">Nhập nội dung theo từng mục. Công thức viết bằng LaTeX trong dấu <code>$...$</code>.</p>
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
                    <button id="lessonReloadBtn" type="button" class="w-full bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-rotate-right mr-1"></i>Tải lại dữ liệu
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
                            <input id="lessonChapter" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Chương 1: Số tự nhiên">
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

                    <label class="flex items-center gap-2 text-sm font-bold text-slate-700">
                        <input id="lessonPublished" type="checkbox" class="w-4 h-4 text-teal-600 rounded">
                        Mở bài này cho học sinh
                    </label>

                    <label class="block text-sm font-bold text-slate-700">Mục tiêu bài học
                        <textarea id="lessonGoal" rows="2" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Sau bài này học sinh cần nắm được..."></textarea>
                    </label>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        <label class="block text-sm font-bold text-slate-700">Lý thuyết
                            <span class="block text-xs font-medium text-slate-500 mb-1">Mỗi dòng là một ý. Có thể dùng $...$.</span>
                            <textarea id="lessonTheory" rows="8" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                        </label>
                        <label class="block text-sm font-bold text-slate-700">Ví dụ
                            <span class="block text-xs font-medium text-slate-500 mb-1">Mỗi dòng: Tiêu đề | Nội dung</span>
                            <textarea id="lessonExamples" rows="8" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                        </label>
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

                    <label class="block text-sm font-bold text-slate-700">Câu hỏi trắc nghiệm
                        <span class="block text-xs font-medium text-slate-500 mb-1">Mỗi dòng: Câu hỏi | A | B | C | D | đáp án. Đáp án nhập A/B/C/D hoặc 1/2/3/4.</span>
                        <textarea id="lessonQuestions" rows="8" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none font-mono text-xs" placeholder="Tập hợp là gì? | Một nhóm đối tượng xác định rõ ràng | Một phép cộng | Một số bất kỳ | Một hình vẽ | A"></textarea>
                    </label>

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
        el('saveLessonBtn').onclick = saveLesson;
        el('seedLessonBtn').onclick = fillSeed;
        el('lessonTitleInput').addEventListener('blur', suggestSlug);
        el('lessonChapter').addEventListener('blur', suggestSlug);
        el('lessonSubject').addEventListener('change', event => {
            selectedSubject = event.target.value;
            renderSubjectPills();
            suggestSlug();
        });
        ['lessonGoal', 'lessonTheory', 'lessonExamples', 'lessonSkills', 'lessonTasks', 'lessonVideos', 'lessonQuestions'].forEach(id => {
            el(id).addEventListener('input', renderPreview);
        });
        setupEditorFieldShortcuts();

        renderSubjectPills();
    }

    function renderSubjectPills() {
        const box = el('subjectPills');
        if (!box) return;
        box.innerHTML = SUBJECTS.map(item => {
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
        const filtered = lessons.filter(lesson => lesson.subject === selectedSubject);
        const items = filtered.length ? filtered : lessons;
        select.innerHTML = items.map(lesson => `<option value="${escapeHtml(lesson.slug)}">${escapeHtml(lesson.title)} (${escapeHtml(lesson.subject)})</option>`).join('');
        if (items.some(item => item.slug === currentSlug)) select.value = currentSlug;
    }

    function fillForm(slug) {
        const lesson = lessons.find(item => item.slug === slug) || lessons.find(item => item.subject === selectedSubject) || lessons[0] || defaults;
        currentSlug = lesson.slug;
        selectedSubject = lesson.subject || selectedSubject;
        if (el('lessonSelect')) el('lessonSelect').value = lesson.slug;
        el('lessonSubject').value = selectedSubject;
        el('lessonSlug').value = lesson.slug || '';
        el('lessonChapter').value = lesson.chapter || '';
        el('lessonTitleInput').value = lesson.title || '';
        el('lessonOrder').value = lesson.order_index || 1;
        el('lessonPublished').checked = !!lesson.is_published;
        el('lessonGoal').value = lesson.goal || lesson.goal_text || '';
        el('lessonTheory').value = Array.isArray(lesson.theory) ? lesson.theory.join('\n') : '';
        el('lessonExamples').value = formatExamples(lesson.examples);
        el('lessonVideos').value = formatVideos(lesson.videos);
        el('lessonSkills').value = formatSkills(lesson.skills);
        el('lessonTasks').value = Array.isArray(lesson.tasks) ? lesson.tasks.join('\n') : '';
        el('lessonQuestions').value = formatQuestions(lesson.questions);
        renderSubjectPills();
        renderPreview();
    }

    function fillSeed() {
        selectedSubject = defaults.subject;
        el('lessonSubject').value = defaults.subject;
        el('lessonSlug').value = defaults.slug;
        el('lessonChapter').value = defaults.chapter;
        el('lessonTitleInput').value = defaults.title;
        el('lessonOrder').value = defaults.order_index;
        el('lessonPublished').checked = true;
        el('lessonGoal').value = defaults.goal_text;
        el('lessonTheory').value = defaults.theory.join('\n');
        el('lessonExamples').value = formatExamples(defaults.examples);
        el('lessonVideos').value = formatVideos(defaults.videos);
        el('lessonSkills').value = formatSkills(defaults.skills);
        el('lessonTasks').value = defaults.tasks.join('\n');
        el('lessonQuestions').value = formatQuestions(defaults.questions);
        renderSubjectPills();
        renderPreview();
    }

    function newLesson() {
        const order = lessons.filter(lesson => lesson.subject === selectedSubject).length + 1;
        el('lessonSubject').value = selectedSubject;
        el('lessonChapter').value = '';
        el('lessonTitleInput').value = '';
        el('lessonSlug').value = '';
        el('lessonOrder').value = order;
        el('lessonPublished').checked = false;
        el('lessonGoal').value = '';
        el('lessonTheory').value = '';
        el('lessonExamples').value = '';
        el('lessonVideos').value = '';
        el('lessonSkills').value = 'nhan_biet | Nhan biet kien thuc | 80';
        el('lessonTasks').value = 'Đọc lý thuyết\nXem ví dụ\nLàm bài luyện tập';
        el('lessonQuestions').value = '';
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
        preview.innerHTML = `
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div><div class="text-xs text-slate-500">Lý thuyết</div><div class="font-bold">${parseLines(el('lessonTheory').value).length} ý</div></div>
                <div><div class="text-xs text-slate-500">Ví dụ</div><div class="font-bold">${parseExamples(el('lessonExamples').value).length} mục</div></div>
                <div><div class="text-xs text-slate-500">Kỹ năng</div><div class="font-bold">${parseSkills(el('lessonSkills').value).length} kỹ năng</div></div>
                <div><div class="text-xs text-slate-500">Video / câu hỏi</div><div class="font-bold">${parseVideos(el('lessonVideos').value).length} / ${questionCount}</div></div>
            </div>
        `;
    }

    async function saveLesson(event) {
        event.preventDefault();
        suggestSlug();
        const skills = parseSkills(el('lessonSkills').value);
        const payload = {
            action: 'save_content',
            slug: el('lessonSlug').value.trim(),
            subject: el('lessonSubject').value.trim(),
            chapter: el('lessonChapter').value.trim(),
            title: el('lessonTitleInput').value.trim(),
            order_index: Number(el('lessonOrder').value) || 0,
            is_published: el('lessonPublished').checked,
            goal_text: el('lessonGoal').value.trim(),
            theory: parseLines(el('lessonTheory').value),
            examples: parseExamples(el('lessonExamples').value),
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
                headers: { 'Content-Type': 'application/json', 'X-Admin-Key': getAdminKey() },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Không lưu được bài học.');
            currentSlug = payload.slug;
            selectedSubject = payload.subject;
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

    async function refreshLessons() {
        const adminKey = getAdminKey();
        if (!adminKey) return;

        const res = await fetch('api/lessons.php?admin=1&debug=1', {
            headers: { 'X-Admin-Key': adminKey },
            cache: 'no-store'
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Không tải được bài học.');
        lessons = data.lessons || [];
        if (!lessons.some(item => item.slug === currentSlug)) {
            currentSlug = lessons.find(item => item.subject === selectedSubject)?.slug || lessons[0]?.slug || defaults.slug;
        }
        renderSubjectPills();
        renderSelect();
        fillForm(currentSlug);
        document.dispatchEvent(new CustomEvent('adminLessonsChanged', { detail: { lessons } }));
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
        if (getAdminKey()) refreshLessons().catch(console.warn);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootIfReady);
    } else {
        bootIfReady();
    }
})();
