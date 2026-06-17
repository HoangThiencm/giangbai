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
        chapter: 'Chuong 1: So tu nhien',
        title: 'Bai 1: Tap hop',
        order_index: 1,
        is_published: true,
        goal_text: 'Hoc sinh hieu tap hop la gi, biet viet tap hop bang cach liet ke phan tu va dung ky hieu thuoc, khong thuoc.',
        theory: [
            'Tap hop la mot nhom cac doi tuong duoc xac dinh ro rang.',
            'Moi doi tuong trong mot tap hop duoc goi la mot phan tu.',
            'Ta thuong dat ten tap hop bang chu cai in hoa.',
            'Co the nhap cong thuc bang LaTeX, vi du: $A=\\{1,2,3\\}$.'
        ],
        examples: [
            { title: 'Vi du 1', body: 'A = $\\{1,2,3,4\\}$ la tap hop cac so tu nhien nho hon 5.' },
            { title: 'Vi du 2', body: 'Neu B = $\\{a,b,c\\}$ thi $a \\in B$ va $d \\notin B$.' }
        ],
        videos: [
            { title: 'Bai giang on lai', url: '' }
        ],
        skills: [
            { id: 'khai_niem', name: 'Hieu khai niem tap hop', target: 80 },
            { id: 'liet_ke', name: 'Liet ke phan tu cua tap hop', target: 80 },
            { id: 'ky_hieu', name: 'Dung ky hieu thuoc va khong thuoc', target: 80 }
        ],
        tasks: ['Doc ly thuyet ngan', 'Xem vi du mau', 'Lam bai luyen tap'],
        questions: [
            {
                id: 'q1',
                skill: 'khai_niem',
                prompt: 'Cau nao mo ta dung nhat ve tap hop?',
                options: ['Mot nhom cac doi tuong duoc xac dinh ro rang', 'Mot phep tinh cong', 'Mot so tu nhien bat ky', 'Mot hinh ve'],
                answer: 0
            },
            {
                id: 'q2',
                skill: 'ky_hieu',
                prompt: 'Cho $B=\\{2,4,6,8\\}$. Khang dinh nao dung?',
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
                name: name || id || `Ky nang ${index + 1}`,
                target: Number(target) || 80
            };
        });
    }

    function parseVideos(text) {
        return parseLines(text).map(line => {
            const parts = line.includes('||') ? line.split('||') : line.split('|');
            const [title, ...urlParts] = parts;
            return { title: (title || 'Video bai giang').trim(), url: urlParts.join('|').trim() };
        }).filter(video => video.url);
    }

    function parseQuestions(text) {
        return parseLines(text).map((line, index) => {
            const parts = line.split('|').map(part => part.trim());
            if (parts.length < 8) {
                throw new Error(`Cau hoi dong ${index + 1} chua dung mau: ky_nang | cau hoi | A | B | C | D | dap_an`);
            }
            const [skill, prompt, a, b, c, d, answer] = parts;
            const answerIndex = Math.max(0, Math.min(3, Number(answer) - 1));
            return {
                id: `q${index + 1}`,
                skill: slugify(skill),
                prompt,
                options: [a, b, c, d],
                answer: Number.isFinite(answerIndex) ? answerIndex : 0
            };
        });
    }

    function formatExamples(items) {
        return (items || []).map(item => `${item.title || ''} | ${item.body || ''}`).join('\n');
    }

    function formatSkills(items) {
        return (items || []).map(item => `${item.id || ''} | ${item.name || ''} | ${item.target || 80}`).join('\n');
    }

    function formatVideos(items) {
        return (items || []).map(item => `${item.title || 'Video bai giang'} | ${item.url || ''}`).join('\n');
    }

    function formatQuestions(items) {
        return (items || []).map(item => {
            const options = item.options || [];
            return [
                item.skill || '',
                item.prompt || '',
                options[0] || '',
                options[1] || '',
                options[2] || '',
                options[3] || '',
                Number(item.answer || 0) + 1
            ].join(' | ');
        }).join('\n');
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
                        <i class="fas fa-book-open text-teal-600 mr-2"></i>Tao bai hoc cho lo trinh
                    </h3>
                    <p class="text-sm text-slate-500 mt-1">Nhap noi dung theo tung muc. Cong thuc viet bang LaTeX trong dau <code>$...$</code>.</p>
                </div>
                <div class="flex flex-wrap gap-2" id="subjectPills"></div>
            </div>

            <div class="mt-5 grid grid-cols-1 xl:grid-cols-[300px_1fr] gap-5">
                <aside class="space-y-4">
                    <div>
                        <label class="block text-sm font-bold text-slate-700 mb-1">Chon bai hoc</label>
                        <select id="lessonSelect" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></select>
                    </div>
                    <button id="newLessonBtn" type="button" class="w-full bg-slate-100 hover:bg-slate-200 text-slate-800 px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-plus mr-1"></i>Tao bai moi
                    </button>
                    <button id="lessonReloadBtn" type="button" class="w-full bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 px-4 py-2.5 rounded font-bold text-sm">
                        <i class="fas fa-rotate-right mr-1"></i>Tai lai du lieu
                    </button>
                    <div class="rounded border border-teal-100 bg-teal-50 p-3 text-sm leading-6 text-teal-900">
                        Vi du cong thuc: <code>$A=\\{1,2,3\\}$</code>, <code>$x \\in A$</code>. Hoc sinh se nhin thay cong thuc da render.
                    </div>
                </aside>

                <form id="lessonForm" class="space-y-5">
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        <label class="block text-sm font-bold text-slate-700">Mon hoc
                            <select id="lessonSubject" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none">
                                ${SUBJECTS.map(item => `<option value="${item.title}">${item.label}</option>`).join('')}
                            </select>
                        </label>
                        <label class="block text-sm font-bold text-slate-700">Chuong
                            <input id="lessonChapter" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Chuong 1: So tu nhien">
                        </label>
                        <label class="block text-sm font-bold text-slate-700">Ten bai
                            <input id="lessonTitleInput" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Bai 1: Tap hop">
                        </label>
                        <div class="grid grid-cols-[1fr_110px] gap-3">
                            <label class="block text-sm font-bold text-slate-700">Slug
                                <input id="lessonSlug" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="math6-c1-b1-tap-hop">
                            </label>
                            <label class="block text-sm font-bold text-slate-700">Thu tu
                                <input id="lessonOrder" type="number" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" value="1">
                            </label>
                        </div>
                    </div>

                    <label class="flex items-center gap-2 text-sm font-bold text-slate-700">
                        <input id="lessonPublished" type="checkbox" class="w-4 h-4 text-teal-600 rounded">
                        Mo bai nay cho hoc sinh
                    </label>

                    <label class="block text-sm font-bold text-slate-700">Muc tieu bai hoc
                        <textarea id="lessonGoal" rows="2" class="mt-1 w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Sau bai nay hoc sinh can nam duoc..."></textarea>
                    </label>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        <label class="block text-sm font-bold text-slate-700">Ly thuyet
                            <span class="block text-xs font-medium text-slate-500 mb-1">Moi dong la mot y. Co the dung $...$.</span>
                            <textarea id="lessonTheory" rows="8" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                        </label>
                        <label class="block text-sm font-bold text-slate-700">Vi du
                            <span class="block text-xs font-medium text-slate-500 mb-1">Moi dong: Tieu de | Noi dung</span>
                            <textarea id="lessonExamples" rows="8" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                        </label>
                    </div>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        <label class="block text-sm font-bold text-slate-700">Ky nang can dat
                            <span class="block text-xs font-medium text-slate-500 mb-1">Moi dong: id | Ten ky nang | target</span>
                            <textarea id="lessonSkills" rows="6" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                        </label>
                        <label class="block text-sm font-bold text-slate-700">Nhiem vu hoc sinh
                            <span class="block text-xs font-medium text-slate-500 mb-1">Moi dong la mot viec can lam.</span>
                            <textarea id="lessonTasks" rows="6" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                        </label>
                    </div>

                    <label class="block text-sm font-bold text-slate-700">Video YouTube bai giang
                        <span class="block text-xs font-medium text-slate-500 mb-1">Moi dong: Tieu de | Link YouTube. Co the de trong neu bai chua co video.</span>
                        <textarea id="lessonVideos" rows="4" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Bai giang Tap hop | https://www.youtube.com/watch?v=..."></textarea>
                    </label>

                    <label class="block text-sm font-bold text-slate-700">Cau hoi trac nghiem
                        <span class="block text-xs font-medium text-slate-500 mb-1">Moi dong: ky_nang | Cau hoi | A | B | C | D | dap_an_1_den_4</span>
                        <textarea id="lessonQuestions" rows="8" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none font-mono text-xs"></textarea>
                    </label>

                    <div id="lessonPreview" class="rounded border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700"></div>

                    <div class="flex flex-wrap gap-3">
                        <button id="saveLessonBtn" class="bg-teal-600 hover:bg-teal-700 text-white px-5 py-2.5 rounded shadow font-bold text-sm transition flex items-center gap-2">
                            <i class="fas fa-save"></i>Luu bai hoc
                        </button>
                        <button id="seedLessonBtn" type="button" class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-5 py-2.5 rounded shadow-sm font-bold text-sm transition">
                            Dien mau Bai 1
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
        el('lessonTasks').value = 'Doc ly thuyet\nXem vi du\nLam bai luyen tap';
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
        try { questionCount = parseQuestions(el('lessonQuestions').value).length; } catch { questionCount = 0; }
        preview.innerHTML = `
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div><div class="text-xs text-slate-500">Ly thuyet</div><div class="font-bold">${parseLines(el('lessonTheory').value).length} y</div></div>
                <div><div class="text-xs text-slate-500">Vi du</div><div class="font-bold">${parseExamples(el('lessonExamples').value).length} muc</div></div>
                <div><div class="text-xs text-slate-500">Ky nang</div><div class="font-bold">${parseSkills(el('lessonSkills').value).length} ky nang</div></div>
                <div><div class="text-xs text-slate-500">Video / cau hoi</div><div class="font-bold">${parseVideos(el('lessonVideos').value).length} / ${questionCount}</div></div>
            </div>
        `;
    }

    async function saveLesson(event) {
        event.preventDefault();
        suggestSlug();
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
            skills: parseSkills(el('lessonSkills').value),
            tasks: parseLines(el('lessonTasks').value),
            questions: parseQuestions(el('lessonQuestions').value)
        };
        if (!payload.slug || !payload.title) {
            alert('Can nhap slug va ten bai.');
            return;
        }

        const btn = el('saveLessonBtn');
        const old = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>Dang luu...';
        try {
            const res = await fetch('api/lessons.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Admin-Key': getAdminKey() },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Khong luu duoc bai hoc.');
            currentSlug = payload.slug;
            selectedSubject = payload.subject;
            await refreshLessons();
            if (typeof window.refreshAdminProgress === 'function') window.refreshAdminProgress();
            alert('Da luu bai hoc.');
        } catch (e) {
            alert(e.message || 'Khong luu duoc bai hoc.');
        } finally {
            btn.disabled = false;
            btn.innerHTML = old;
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

        const res = await fetch('api/lessons.php?admin=1', {
            headers: { 'X-Admin-Key': adminKey },
            cache: 'no-store'
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Khong tai duoc bai hoc.');
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
