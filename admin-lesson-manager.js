(function () {
    const defaults = {
        slug: 'math6-c1-b1-tap-hop',
        subject: 'Toán 6',
        chapter: 'Chương 1: Số tự nhiên',
        title: 'Bài 1: Tập hợp',
        goal_text: 'Học sinh hiểu tập hợp là gì, biết viết tập hợp bằng cách liệt kê phần tử và dùng đúng ký hiệu thuộc, không thuộc.',
        theory: [
            'Tập hợp là một nhóm các đối tượng được xác định rõ ràng.',
            'Mỗi đối tượng trong một tập hợp được gọi là một phần tử.',
            'Ta thường đặt tên tập hợp bằng các chữ cái in hoa.',
            'Các phần tử thường được viết trong dấu ngoặc nhọn { }.'
        ],
        examples: [
            { title: 'Ví dụ 1', body: 'A = {1, 2, 3, 4} là tập hợp các số tự nhiên nhỏ hơn 5.' },
            { title: 'Ví dụ 2', body: 'Nếu B = {a, b, c} thì a ∈ B và d ∉ B.' },
            { title: 'Ví dụ 3', body: 'C = {T, O, A, N} là tập hợp các chữ cái trong từ TOAN.' }
        ],
        skills: [
            { id: 'khai_niem', name: 'Hiểu khái niệm tập hợp', target: 80 },
            { id: 'liet_ke', name: 'Liệt kê phần tử của tập hợp', target: 80 },
            { id: 'ky_hieu', name: 'Dùng ký hiệu ∈ và ∉', target: 80 },
            { id: 'viet_tap_hop', name: 'Viết tập hợp đúng quy ước', target: 80 }
        ],
        tasks: ['Đọc lý thuyết ngắn', 'Xem 3 ví dụ mẫu', 'Làm 8 câu luyện tập'],
        questions: [
            {
                id: 'q1',
                skill: 'khai_niem',
                prompt: 'Câu nào mô tả đúng nhất về tập hợp?',
                options: [
                    'Một nhóm các đối tượng được xác định rõ ràng',
                    'Một phép tính cộng nhiều số',
                    'Một số tự nhiên bất kỳ',
                    'Một hình vẽ trong vở'
                ],
                answer: 0
            },
            {
                id: 'q2',
                skill: 'viet_tap_hop',
                prompt: 'Cách viết nào đúng cho tập hợp A gồm các số 1, 2, 3?',
                options: ['A = (1, 2, 3)', 'A = {1, 2, 3}', 'A = [1, 2, 3]', 'A = 1 + 2 + 3'],
                answer: 1
            },
            {
                id: 'q3',
                skill: 'ky_hieu',
                prompt: 'Cho B = {2, 4, 6, 8}. Khẳng định nào đúng?',
                options: ['3 ∈ B', '6 ∈ B', '8 ∉ B', '4 ∉ B'],
                answer: 1
            }
        ]
    };

    let lessons = [];
    let currentSlug = defaults.slug;

    function el(id) { return document.getElementById(id); }
    function getAdminKey() {
        try {
            return typeof cachedKey !== 'undefined' ? cachedKey : window.cachedKey;
        } catch {
            return window.cachedKey;
        }
    }
    function parseLines(text) { return String(text || '').split('\n').map(line => line.trim()).filter(Boolean); }
    function parseExamples(text) {
        return parseLines(text).map(line => {
            const [title, ...bodyParts] = line.split('||');
            return { title: (title || '').trim(), body: bodyParts.join('||').trim() };
        });
    }
    function parseSkills(text) {
        return parseLines(text).map((line, index) => {
            const [id, name, target] = line.split('|').map(part => part.trim());
            return { id: id || `skill_${index + 1}`, name: name || id || `Kỹ năng ${index + 1}`, target: Number(target) || 80 };
        });
    }

    async function loadLessons() {
        const adminKey = getAdminKey();
        if (!adminKey) return;
        const res = await fetch('api/lessons.php?admin=1', {
            headers: { 'X-Admin-Key': adminKey },
            cache: 'no-store'
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Không tải được bài học.');
        lessons = data.lessons || [];
        renderSelect();
        if (!lessons.some(item => item.slug === currentSlug)) currentSlug = lessons[0]?.slug || defaults.slug;
        fillForm(currentSlug);
    }

    function ensurePanel() {
        if (el('lessonEditorPanel')) return;
        const dashboard = el('dashboardSection');
        if (!dashboard) return;
        const listCard = dashboard.querySelector('.bg-white.rounded-xl.shadow-lg.overflow-hidden');
        if (!listCard) return;

        const panel = document.createElement('div');
        panel.id = 'lessonEditorPanel';
        panel.className = 'bg-white rounded-xl shadow-lg border border-slate-200 mb-8 p-6';
        panel.innerHTML = `
            <div class="flex items-center justify-between gap-4 mb-4">
                <div>
                    <h3 class="font-bold text-slate-800 text-lg"><i class="fas fa-book-open text-teal-600 mr-2"></i>Nhập nội dung lộ trình</h3>
                    <p class="text-sm text-slate-500 mt-1">Nhập lý thuyết, ví dụ, kỹ năng và câu hỏi trực tiếp vào database.</p>
                </div>
                <button id="lessonReloadBtn" class="text-sm font-bold text-teal-700 hover:text-teal-800"><i class="fas fa-rotate-right mr-1"></i>Tải lại</button>
            </div>
            <div class="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-4">
                <div class="space-y-3">
                    <label class="block text-sm font-bold text-slate-700">Chọn bài học
                        <select id="lessonSelect" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></select>
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Slug
                        <input id="lessonSlug" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none">
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Môn học
                        <input id="lessonSubject" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none">
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Chương
                        <input id="lessonChapter" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none">
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Tên bài
                        <input id="lessonTitle" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none">
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Thứ tự
                        <input id="lessonOrder" type="number" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" value="1">
                    </label>
                    <label class="flex items-center gap-2 text-sm font-bold text-slate-700">
                        <input id="lessonPublished" type="checkbox" class="w-4 h-4 text-teal-600 rounded" checked>
                        Được mở cho học sinh
                    </label>
                </div>
                <div class="space-y-4">
                    <label class="block text-sm font-bold text-slate-700">Mục tiêu bài học
                        <textarea id="lessonGoal" rows="2" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Lý thuyết, mỗi dòng 1 ý
                        <textarea id="lessonTheory" rows="4" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Ví dụ, mỗi dòng theo mẫu: <code>Tiêu đề||Nội dung</code>
                        <textarea id="lessonExamples" rows="5" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Kỹ năng, mỗi dòng theo mẫu: <code>id|Tên kỹ năng|target</code>
                        <textarea id="lessonSkills" rows="4" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Nhiệm vụ, mỗi dòng 1 việc
                        <textarea id="lessonTasks" rows="3" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Câu hỏi trắc nghiệm (JSON array)
                        <textarea id="lessonQuestions" rows="10" class="mt-1 w-full font-mono text-xs p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                    </label>
                    <div class="flex flex-wrap gap-3">
                        <button id="saveLessonBtn" class="bg-teal-600 hover:bg-teal-700 text-white px-5 py-2.5 rounded shadow font-bold text-sm transition flex items-center gap-2">
                            <i class="fas fa-save"></i> Lưu nội dung bài
                        </button>
                        <button id="seedLessonBtn" type="button" class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-5 py-2.5 rounded shadow-sm font-bold text-sm transition">
                            Điền mẫu Bài 1
                        </button>
                    </div>
                </div>
            </div>
        `;
        dashboard.insertBefore(panel, listCard);

        el('lessonReloadBtn').onclick = refreshLessons;
        el('lessonSelect').onchange = () => fillForm(el('lessonSelect').value);
        el('saveLessonBtn').onclick = saveLesson;
        el('seedLessonBtn').onclick = fillSeed;
    }

    function renderSelect() {
        const select = el('lessonSelect');
        if (!select) return;
        select.innerHTML = lessons.map(lesson => `<option value="${lesson.slug}">${lesson.title}</option>`).join('');
        if (currentSlug) select.value = currentSlug;
    }

    function fillForm(slug) {
        const lesson = lessons.find(item => item.slug === slug) || lessons[0] || defaults;
        currentSlug = lesson.slug;
        if (el('lessonSelect')) el('lessonSelect').value = lesson.slug;
        el('lessonSlug').value = lesson.slug || '';
        el('lessonSubject').value = lesson.subject || 'Toán 6';
        el('lessonChapter').value = lesson.chapter || '';
        el('lessonTitle').value = lesson.title || '';
        el('lessonOrder').value = lesson.order_index || 1;
        el('lessonPublished').checked = !!lesson.is_published;
        el('lessonGoal').value = lesson.goal || lesson.goal_text || '';
        el('lessonTheory').value = Array.isArray(lesson.theory) ? lesson.theory.join('\n') : (Array.isArray(defaults.theory) ? defaults.theory.join('\n') : '');
        el('lessonExamples').value = Array.isArray(lesson.examples) ? lesson.examples.map(item => `${item.title || ''}||${item.body || ''}`).join('\n') : '';
        el('lessonSkills').value = Array.isArray(lesson.skills) ? lesson.skills.map(skill => `${skill.id || ''}|${skill.name || ''}|${skill.target || 80}`).join('\n') : '';
        el('lessonTasks').value = Array.isArray(lesson.tasks) ? lesson.tasks.join('\n') : '';
        el('lessonQuestions').value = JSON.stringify(Array.isArray(lesson.questions) ? lesson.questions : defaults.questions, null, 2);
    }

    function fillSeed() {
        const d = defaults;
        el('lessonSlug').value = d.slug;
        el('lessonSubject').value = d.subject;
        el('lessonChapter').value = d.chapter;
        el('lessonTitle').value = d.title;
        el('lessonOrder').value = 1;
        el('lessonPublished').checked = true;
        el('lessonGoal').value = d.goal_text;
        el('lessonTheory').value = d.theory.join('\n');
        el('lessonExamples').value = d.examples.map(item => `${item.title}||${item.body}`).join('\n');
        el('lessonSkills').value = d.skills.map(skill => `${skill.id}|${skill.name}|${skill.target}`).join('\n');
        el('lessonTasks').value = d.tasks.join('\n');
        el('lessonQuestions').value = JSON.stringify(d.questions, null, 2);
    }

    function parseQuestions(text) {
        const value = String(text || '').trim();
        if (!value) return [];
        const parsed = JSON.parse(value);
        if (!Array.isArray(parsed)) throw new Error('questions must be array');
        return parsed;
    }

    async function saveLesson(event) {
        event.preventDefault();
        try {
            const payload = {
                action: 'save_content',
                slug: el('lessonSlug').value.trim(),
                subject: el('lessonSubject').value.trim(),
                chapter: el('lessonChapter').value.trim(),
                title: el('lessonTitle').value.trim(),
                order_index: Number(el('lessonOrder').value) || 0,
                is_published: el('lessonPublished').checked,
                goal_text: el('lessonGoal').value.trim(),
                theory: parseLines(el('lessonTheory').value),
                examples: parseExamples(el('lessonExamples').value),
                skills: parseSkills(el('lessonSkills').value),
                tasks: parseLines(el('lessonTasks').value),
                questions: parseQuestions(el('lessonQuestions').value)
            };
            const res = await fetch('api/lessons.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Admin-Key': getAdminKey() },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Không lưu được nội dung bài học.');
            currentSlug = payload.slug;
            await refreshLessons();
            alert('Đã lưu nội dung bài học.');
        } catch (e) {
            alert(e.message || 'Không lưu được nội dung bài học.');
        }
    }

    async function refreshLessons() {
        const adminKey = getAdminKey();
        if (!adminKey) return;
        try {
            await fetch('api/migrate_lessons.php', {
                method: 'POST',
                headers: { 'X-Admin-Key': adminKey }
            });
        } catch (e) {
            console.warn('Schema sync failed', e);
        }
        try {
            const res = await fetch('api/lessons.php?admin=1', {
                headers: { 'X-Admin-Key': adminKey },
                cache: 'no-store'
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Không tải được bài học.');
            lessons = data.lessons || [];
            if (!lessons.some(item => item.slug === currentSlug)) currentSlug = lessons[0]?.slug || defaults.slug;
            renderSelect();
            fillForm(currentSlug);
        } catch (e) {
            console.warn(e);
        }
    }

    function wrapLoadUsers() {
        if (typeof window.loadUsers !== 'function') return;
        const original = window.loadUsers;
        window.loadUsers = async function (...args) {
            const result = await original.apply(this, args);
            ensurePanel();
            await refreshLessons();
            return result;
        };
    }

    function bootIfReady() {
        ensurePanel();
        wrapLoadUsers();
        if (getAdminKey()) refreshLessons();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootIfReady);
    } else {
        bootIfReady();
    }
})();
