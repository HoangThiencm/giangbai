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
    let interactiveEditorMode = 'bulk';
    let questionsEditorMode = 'bulk';
    let previewRenderQueued = false;
    const LI = window.LessonImport;

    function scheduleRenderPreview() {
        if (previewRenderQueued) return;
        previewRenderQueued = true;
        requestAnimationFrame(() => {
            previewRenderQueued = false;
            renderPreview();
        });
    }

    function el(id) { return document.getElementById(id); }

    function requireLessonImport() {
        if (!LI) {
            alert('Thiếu lesson-import.js. Tải lại trang (Ctrl+F5).');
            return false;
        }
        return true;
    }

    if (!LI) {
        console.error('admin-lesson-manager.js requires lesson-import.js — load lesson-import.js before admin-lesson-manager.js');
        return;
    }

    const AI_MARKER = LI.AI_MARKER;
    const slugify = LI?.slugify || function slugifyLocal(value) {
        return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
            .replace(/đ/g, 'd').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 110);
    };
    const parseLines = (...a) => LI.parseLines(...a);
    const splitQuestionParts = (...a) => LI.splitQuestionParts(...a);
    const parseContentWithAiMarker = (...a) => LI.parseContentWithAiMarker(...a);
    const normalizeTheoryItem = (...a) => LI.normalizeTheoryItem(...a);
    const parseTheoryBlocks = (...a) => LI.parseTheoryBlocks(...a);
    const formatTheoryBlocks = (...a) => LI.formatTheoryBlocks(...a);
    const parseExamples = (...a) => LI.parseExamples(...a);
    const parseSkills = (...a) => LI.parseSkills(...a);
    const parseVideos = (...a) => LI.parseVideos(...a);
    const parseQuestions = (...a) => LI.parseQuestions(...a);
    const parseEssayExercises = (...a) => LI.parseEssayExercises(...a);
    const parseFillExercises = (...a) => LI.parseFillExercises(...a);
    const parseDragExercises = (...a) => LI.parseDragExercises(...a);
    const buildDragExercisesFromItems = (...a) => LI.buildDragExercisesFromItems(...a);
    const parseGeminiLessonSections = (...a) => LI.parseGeminiLessonSections(...a);
    const parseInteractiveBulkPaste = (...a) => LI.parseInteractiveBulkPaste(...a);
    const normalizeFillParts = (...a) => LI.normalizeFillParts(...a);
    const normalizeMcqBulkLine = (...a) => LI.normalizeMcqBulkLine(...a);
    const looksLikeSkillId = (...a) => LI.looksLikeSkillId(...a);
    const poolsLookLikeSortOrder = (...a) => LI.poolsLookLikeSortOrder(...a);
    const poolTextHasMultipleItems = (...a) => LI.poolTextHasMultipleItems(...a);
    const joinPoolText = (...a) => LI.joinPoolText(...a);
    const splitPoolText = (...a) => LI.splitPoolText(...a);
    const repairPoolPieces = (...a) => LI.repairPoolPieces(...a);
    const parseMatchPairs = (...a) => LI.parseMatchPairs(...a);
    const buildDefaultMatchPairSpec = (...a) => LI.buildDefaultMatchPairSpec(...a);
    const isDragMatchItem = (...a) => LI.isDragMatchItem(...a);
    const normalizeBulkHeading = (...a) => LI.normalizeBulkHeading(...a);
    const classifyInteractivePipeLine = (...a) => LI.classifyInteractivePipeLine(...a);
    const resolveInteractiveBulkSection = (...a) => LI.resolveInteractiveBulkSection(...a);
    const isInteractivePipeLine = (...a) => LI.isInteractivePipeLine(...a);
    const questionsToEditorItems = (...a) => LI.questionsToEditorItems(...a);

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
        if (LI) return LI.formatQuestionsBulk(items);
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

    const PENDING_IMAGE_PLACEHOLDER_RE = /!\[(?:Đang tải ảnh[^\]]*|ĐANG_TAI:[^\]]*)\]\(\s*\)/gi;
    const LESSON_IMAGE_MAX_EDGE = 1200;
    const LESSON_IMAGE_JPEG_QUALITY = 0.8;
    const LESSON_IMAGE_TARGET_BYTES = 480 * 1024;
    const LESSON_IMAGE_SKIP_BELOW_BYTES = 180 * 1024;
    let lessonPendingImageUploads = 0;

    function createLessonImageUploadToken() {
        return `upload-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    }

    function buildLessonImagePlaceholder(token, label = 'ảnh') {
        return `\n![ĐANG_TAI:${token}|${label}]()\n`;
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

    function lessonImageAltForMarkdown(label) {
        return isGenericLessonImageLabel(label) ? '' : String(label || '').trim();
    }

    function shouldShowLessonImageCaption(label) {
        return !isGenericLessonImageLabel(label);
    }

    function buildLessonImageMarkdown(label, url) {
        const alt = lessonImageAltForMarkdown(label);
        return `\n![${alt}](${url})\n`;
    }

    function extractDriveFileIdFromUrl(url) {
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

    function normalizeLessonImagePreviewUrl(url) {
        const value = String(url || '').trim();
        if (!/^https?:\/\//i.test(value)) return '';
        const fileId = extractDriveFileIdFromUrl(value);
        if (fileId) return `https://drive.google.com/thumbnail?id=${fileId}&sz=w1600`;
        return value;
    }

    function lessonEditorTextHasPendingImages(...values) {
        return values.some(value => PENDING_IMAGE_PLACEHOLDER_RE.test(String(value || '')));
    }

    function cleanupStaleLessonImagePlaceholders(text) {
        const source = String(text || '');
        if (!PENDING_IMAGE_PLACEHOLDER_RE.test(source)) {
            return { text: source, removed: 0 };
        }
        PENDING_IMAGE_PLACEHOLDER_RE.lastIndex = 0;
        let removed = 0;
        const cleaned = source.replace(PENDING_IMAGE_PLACEHOLDER_RE, () => {
            removed += 1;
            return '';
        });
        return { text: cleaned.replace(/\n{3,}/g, '\n\n').trim(), removed };
    }

    function formatLessonImageByteSize(bytes) {
        const size = Number(bytes) || 0;
        if (size < 1024) return `${size} B`;
        if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
        return `${(size / (1024 * 1024)).toFixed(1)} MB`;
    }

    function canvasToBlob(canvas, type, quality) {
        return new Promise(resolve => {
            canvas.toBlob(blob => resolve(blob), type, quality);
        });
    }

    function loadLessonImageElement(file) {
        return new Promise((resolve, reject) => {
            const url = URL.createObjectURL(file);
            const image = new Image();
            image.onload = () => {
                URL.revokeObjectURL(url);
                resolve(image);
            };
            image.onerror = () => {
                URL.revokeObjectURL(url);
                reject(new Error('Không đọc được ảnh để nén.'));
            };
            image.src = url;
        });
    }

    async function compressLessonImageFile(file) {
        const mime = String(file?.type || '').toLowerCase();
        if (!file || !mime.startsWith('image/')) return file;
        if (mime === 'image/gif' || mime === 'image/svg+xml') return file;

        let image;
        try {
            image = await loadLessonImageElement(file);
        } catch (_) {
            return file;
        }

        let width = image.naturalWidth || image.width;
        let height = image.naturalHeight || image.height;
        if (!width || !height) return file;

        const maxEdge = Math.max(width, height);
        const withinSize = file.size <= LESSON_IMAGE_SKIP_BELOW_BYTES;
        const withinEdge = maxEdge <= LESSON_IMAGE_MAX_EDGE;
        if (withinSize && withinEdge) return file;

        if (maxEdge > LESSON_IMAGE_MAX_EDGE) {
            const scale = LESSON_IMAGE_MAX_EDGE / maxEdge;
            width = Math.max(1, Math.round(width * scale));
            height = Math.max(1, Math.round(height * scale));
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        if (!ctx) return file;

        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, width, height);
        ctx.drawImage(image, 0, 0, width, height);

        let quality = LESSON_IMAGE_JPEG_QUALITY;
        let blob = await canvasToBlob(canvas, 'image/jpeg', quality);
        while (blob && blob.size > LESSON_IMAGE_TARGET_BYTES && quality > 0.52) {
            quality = Math.max(0.52, quality - 0.08);
            blob = await canvasToBlob(canvas, 'image/jpeg', quality);
        }
        if (!blob || blob.size >= file.size) return file;

        const baseName = String(file.name || 'anh-minh-hoa').replace(/\.[^.]+$/, '') || 'anh-minh-hoa';
        return new File([blob], `${baseName}.jpg`, {
            type: 'image/jpeg',
            lastModified: Date.now()
        });
    }

    function replaceLessonImagePlaceholder(field, token, finalMd) {
        const exact = buildLessonImagePlaceholder(token);
        if (field.value.includes(exact)) {
            field.value = field.value.replace(exact, finalMd);
            return true;
        }
        const tokenPattern = new RegExp(`!\\[ĐANG_TAI:${token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[^\\]]*\\]\\(\\s*\\)`, 'g');
        if (tokenPattern.test(field.value)) {
            field.value = field.value.replace(tokenPattern, finalMd);
            return true;
        }
        if (PENDING_IMAGE_PLACEHOLDER_RE.test(field.value)) {
            field.value = field.value.replace(PENDING_IMAGE_PLACEHOLDER_RE, finalMd.trim());
            return true;
        }
        field.value += finalMd;
        return false;
    }

    function insertEditorImage(targetId) {
        const field = el(targetId);
        if (!field) return;

        // Offer two ways: URL or local file (which will auto-upload to Drive)
        const choice = window.prompt('1 = Dán link ảnh sẵn có\n2 = Chọn file ảnh từ máy (sẽ tự upload lên Google Drive)', '2');
        if (choice === '1') {
            const url = window.prompt('Dán link ảnh (https://...)');
            if (!url) return;
            const alt = window.prompt('Mô tả ảnh (có thể để trống)', '') || 'ảnh';
            const insert = `\n![${alt}](${url.trim()})\n`;
            const start = field.selectionStart ?? field.value.length;
            field.setRangeText(insert, start, start, 'end');
            field.focus();
            field.dispatchEvent(new Event('input', { bubbles: true }));
            return;
        }

        // File picker + upload to Drive
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = async () => {
            const file = input.files && input.files[0];
            if (file) await uploadImageFileToDrive(file, field);
        };
        input.click();
    }

    async function uploadImageFileToDrive(file, targetField) {
        if (!file || !targetField) return;

        const uploadToken = createLessonImageUploadToken();
        const imageLabel = (file.name || 'ảnh screenshot').replace(/\s+/g, ' ').trim() || 'ảnh';
        const cursor = targetField.selectionStart ?? targetField.value.length;
        const placeholder = buildLessonImagePlaceholder(uploadToken, imageLabel);
        lessonPendingImageUploads += 1;

        showLessonImageUploadStatus(`Đang nén “${imageLabel}” trước khi tải lên...`, 'loading');
        targetField.setRangeText(placeholder, cursor, cursor, 'end');
        targetField.dispatchEvent(new Event('input', { bubbles: true }));

        let uploadFile = file;
        try {
            uploadFile = await compressLessonImageFile(file);
        } catch (_) {
            uploadFile = file;
        }

        const compressedNote = uploadFile.size < file.size
            ? ` (${formatLessonImageByteSize(file.size)} → ${formatLessonImageByteSize(uploadFile.size)})`
            : '';
        showLessonImageUploadStatus(`Đang tải “${imageLabel}” lên Google Drive${compressedNote}...`, 'loading');

        const form = new FormData();
        form.append('image', uploadFile);
        form.append('action', 'upload_image');

        try {
            const res = await fetch('api/lessons.php', {
                method: 'POST',
                credentials: 'include',
                body: form
            });
            let data = {};
            try {
                data = await res.json();
            } catch (_) {
                throw new Error(`Máy chủ trả lời không hợp lệ (HTTP ${res.status}).`);
            }

            if (!res.ok || !data.ok || !data.url) {
                throw new Error(data.error || data.detail || `Upload thất bại (HTTP ${res.status}).`);
            }

            const previewUrl = normalizeLessonImagePreviewUrl(data.url);
            const finalMd = buildLessonImageMarkdown(imageLabel, previewUrl || data.url);
            replaceLessonImagePlaceholder(targetField, uploadToken, finalMd);

            targetField.focus();
            targetField.dispatchEvent(new Event('input', { bubbles: true }));
            const savedText = uploadFile.size < file.size
                ? ` Đã giảm dung lượng ${formatLessonImageByteSize(file.size)} → ${formatLessonImageByteSize(uploadFile.size)}.`
                : '';
            showLessonImageUploadStatus(`Đã tải ảnh lên Google Drive và chèn vào nội dung.${savedText}`, 'success');
        } catch (err) {
            replaceLessonImagePlaceholder(targetField, uploadToken, '');
            const message = 'Không thể tải ảnh lên Google Drive: ' + (err.message || err);
            showLessonImageUploadStatus(message, 'error');
            alert(message);
            targetField.dispatchEvent(new Event('input', { bubbles: true }));
        } finally {
            lessonPendingImageUploads = Math.max(0, lessonPendingImageUploads - 1);
        }
    }

    function showLessonImageUploadStatus(message, type = 'loading') {
        let notice = document.getElementById('lessonImageUploadStatus');
        if (!notice) {
            notice = document.createElement('div');
            notice.id = 'lessonImageUploadStatus';
            notice.className = 'fixed bottom-5 right-5 z-[10000] max-w-sm rounded-xl px-4 py-3 text-sm font-medium shadow-xl';
            document.body.appendChild(notice);
        }

        const styles = {
            loading: 'bg-sky-600 text-white',
            success: 'bg-emerald-600 text-white',
            error: 'bg-rose-600 text-white'
        };
        notice.className = `fixed bottom-5 right-5 z-[10000] max-w-sm rounded-xl px-4 py-3 text-sm font-medium shadow-xl ${styles[type] || styles.loading}`;
        notice.innerHTML = `${type === 'loading' ? '<i class="fas fa-spinner fa-spin mr-2"></i>' : type === 'success' ? '<i class="fas fa-circle-check mr-2"></i>' : '<i class="fas fa-circle-exclamation mr-2"></i>'}${message}`;
        clearTimeout(window.lessonImageUploadStatusTimer);
        window.lessonImageUploadStatusTimer = setTimeout(() => notice.remove(), type === 'loading' ? 30000 : 5000);
    }

    function getDriveFileIdFromImageUrl(url) {
        try {
            const parsed = new URL(String(url || ''), window.location.origin);
            const queryId = parsed.searchParams.get('id');
            if (queryId) return queryId;
            const pathMatch = parsed.pathname.match(/\/d\/([a-zA-Z0-9_-]+)/);
            return pathMatch ? pathMatch[1] : '';
        } catch (_) {
            return '';
        }
    }

    function getLessonFieldPreview(field) {
        if (!field?.id) return null;
        let preview = document.getElementById(`lessonImagePreview_${field.id}`);
        if (preview) return preview;

        preview = document.createElement('div');
        preview.id = `lessonImagePreview_${field.id}`;
        preview.className = 'lesson-inline-image-preview hidden mt-2 rounded-lg border border-sky-200 bg-sky-50 p-3 text-sm';
        field.insertAdjacentElement('afterend', preview);
        return preview;
    }

    async function deleteLessonDriveImage(field, markdown, imageUrl) {
        const fileId = getDriveFileIdFromImageUrl(imageUrl);
        const actionText = fileId ? 'xóa ảnh khỏi nội dung và xóa tệp tương ứng trên Google Drive' : 'xóa ảnh khỏi nội dung';
        if (!window.confirm(`Bạn có muốn ${actionText}?`)) return;

        try {
            if (fileId) {
                showLessonImageUploadStatus('Đang xóa ảnh trên Google Drive...', 'loading');
                const form = new FormData();
                form.append('action', 'delete_image');
                form.append('file_id', fileId);
                const response = await fetch('api/lessons.php', {
                    method: 'POST',
                    credentials: 'include',
                    body: form
                });
                const data = await response.json();
                if (!response.ok || !data.ok) throw new Error(data.error || `HTTP ${response.status}`);
            }

            field.value = field.value.replace(markdown, '');
            field.dispatchEvent(new Event('input', { bubbles: true }));
            showLessonImageUploadStatus(fileId ? 'Đã xóa ảnh khỏi bài học và Google Drive.' : 'Đã xóa ảnh khỏi nội dung.', 'success');
        } catch (error) {
            const message = `Không thể xóa ảnh: ${error?.message || error}`;
            showLessonImageUploadStatus(message, 'error');
            alert(message);
        }
    }

    function renderLessonFieldImagePreview(field) {
        const preview = getLessonFieldPreview(field);
        if (!preview) return;
        const value = String(field.value || '');
        const imagePattern = /!\[([^\]]*)\]\((https?:\/\/[^\s)]+)\)/g;
        const pendingPattern = PENDING_IMAGE_PLACEHOLDER_RE;
        if (!imagePattern.test(value) && !pendingPattern.test(value)) {
            preview.classList.add('hidden');
            preview.replaceChildren();
            return;
        }

        imagePattern.lastIndex = 0;
        pendingPattern.lastIndex = 0;
        preview.classList.remove('hidden');
        preview.replaceChildren();
        const title = document.createElement('div');
        title.className = 'mb-2 text-xs font-bold text-sky-800';
        title.textContent = 'Xem trước trong bài học (ảnh hiển thị đúng vị trí Markdown)';
        preview.appendChild(title);

        if (pendingPattern.test(value)) {
            pendingPattern.lastIndex = 0;
            const pendingNote = document.createElement('div');
            pendingNote.className = 'mb-3 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-xs font-semibold text-amber-800';
            pendingNote.innerHTML = '<i class="fas fa-spinner fa-spin mr-1"></i>Đang tải ảnh — đợi thông báo xanh rồi mới bấm Lưu bài học.';
            preview.appendChild(pendingNote);
        }

        let cursor = 0;
        let match;
        while ((match = imagePattern.exec(value)) !== null) {
            const markdown = match[0];
            const altText = match[1].replace(/^ĐANG_TAI:[^|]*\|?/i, '');
            const imageUrl = normalizeLessonImagePreviewUrl(match[2]);
            const textBefore = cleanupStaleLessonImagePlaceholders(value.slice(cursor, match.index)).text.trim();
            if (textBefore) {
                const text = document.createElement('div');
                text.className = 'mb-2 whitespace-pre-wrap text-slate-700';
                text.textContent = textBefore;
                preview.appendChild(text);
            }

            const figure = document.createElement('figure');
            figure.className = 'mb-3 rounded-lg border border-slate-200 bg-white p-2';
            const image = document.createElement('img');
            image.src = imageUrl;
            image.alt = altText || 'Ảnh minh họa';
            image.className = 'max-h-80 max-w-full rounded object-contain';
            image.addEventListener('error', () => {
                const fileId = extractDriveFileIdFromUrl(imageUrl);
                if (!fileId || image.dataset.fallbackTried === '1') return;
                image.dataset.fallbackTried = '1';
                image.src = `https://drive.google.com/uc?export=view&id=${fileId}`;
            }, { once: true });
            figure.appendChild(image);

            if (shouldShowLessonImageCaption(altText)) {
                const caption = document.createElement('figcaption');
                caption.className = 'mt-1 text-xs text-slate-500';
                caption.textContent = altText;
                figure.appendChild(caption);
            }
            const actions = document.createElement('div');
            actions.className = 'mt-1 flex justify-end';
            const deleteButton = document.createElement('button');
            deleteButton.type = 'button';
            deleteButton.className = 'rounded bg-rose-50 px-2 py-1 text-xs font-semibold text-rose-700 hover:bg-rose-100';
            deleteButton.innerHTML = '<i class="fas fa-trash"></i> Xóa ảnh';
            deleteButton.onclick = () => deleteLessonDriveImage(field, markdown, imageUrl);
            actions.appendChild(deleteButton);
            figure.appendChild(actions);
            preview.appendChild(figure);
            cursor = imagePattern.lastIndex;
        }

        const textAfter = cleanupStaleLessonImagePlaceholders(value.slice(cursor)).text.trim();
        if (textAfter) {
            const text = document.createElement('div');
            text.className = 'whitespace-pre-wrap text-slate-700';
            text.textContent = textAfter;
            preview.appendChild(text);
        }
    }

    // Full support: paste image *file* (Ctrl+V screenshot) → auto upload to Google Drive + insert link
    // Also still supports pasting a plain image URL
    async function handleRichImagePaste(e, ta) {
        if (!ta) return;
        const clipboard = e.clipboardData;
        if (!clipboard) return;

        // 1. Check for actual image files in clipboard (the main feature requested)
        const items = clipboard.items || [];
        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            if (item.kind === 'file' && item.type.indexOf('image') === 0) {
                e.preventDefault();
                const file = item.getAsFile();
                if (file) {
                    await uploadImageFileToDrive(file, ta);
                }
                return;
            }
        }

        // 2. Also support files from clipboardData.files (some browsers)
        if (clipboard.files && clipboard.files.length) {
            for (let f of clipboard.files) {
                if (f.type.indexOf('image') === 0) {
                    e.preventDefault();
                    await uploadImageFileToDrive(f, ta);
                    return;
                }
            }
        }

        // 3. Fallback: plain URL paste (text link to image)
        const text = clipboard.getData('text/plain') || '';
        if (/^https?:\/\/\S+\.(png|jpe?g|gif|webp|svg)(\?.*)?$/i.test(text.trim())) {
            e.preventDefault();
            const start = ta.selectionStart ?? ta.value.length;
            const md = `\n![ảnh](${text.trim()})\n`;
            ta.setRangeText(md, start, start, 'end');
            ta.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }

    function setupRichImagePaste(ta) {
        if (!ta || ta.dataset.richImagePasteReady) return;
        ta.dataset.richImagePasteReady = '1';
        ta.addEventListener('paste', (e) => {
            handleRichImagePaste(e, ta);
        });
        ta.addEventListener('input', () => renderLessonFieldImagePreview(ta));
        renderLessonFieldImagePreview(ta);
    }

    function setupImagePasteHandlers() {
        ['lessonTheory', 'lessonExamples', 'lessonSelfPractice'].forEach(id => {
            const ta = el(id);
            if (ta) setupRichImagePaste(ta);
        });
    }

    function setupDynamicImagePaste() {
        // Main fields + any current dynamic per-item textareas
        setupImagePasteHandlers();

        const selectors = '.lesson-tab-content textarea[id^="essay-de-"], .lesson-tab-content textarea[id^="fill-de-"], .lesson-tab-content textarea[id^="drag-de-"], .lesson-tab-content textarea[id^="q-cau-"]';
        document.querySelectorAll(selectors).forEach(ta => {
            setupRichImagePaste(ta);
        });
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
    function syncEssayToTextarea(options = {}) {
        const ta = el('lessonEssay');
        if (!ta) return;
        ta.value = essayItems.map(i => `${i.de}|${i.dap}|${i.goi}`).join('\n');
        if (options.refreshPreview && interactiveEditorMode === 'items') scheduleRenderPreview();
    }
    function renderEssayItems() {
        const cont = el('essayItems');
        if (!cont) return;
        cont.innerHTML = '';
        essayItems.forEach((it, i) => {
            const d = document.createElement('div');
            d.className = 'p-2.5 border border-slate-200 rounded-lg bg-white text-xs shadow-sm';
            d.innerHTML = `
                <div class="flex items-center mb-1">
                    <span class="font-bold text-teal-700">Tự luận ${i+1}</span>
                    <button type="button" class="remove-item-btn ml-auto text-rose-500 hover:text-rose-700">✕</button>
                </div>
                ${richToolbarHtml(`essay-de-${i}`)}
                <textarea id="essay-de-${i}" class="w-full p-1.5 border border-slate-300 rounded text-xs" placeholder="Đề (dán ảnh hoặc viết trực tiếp)"></textarea>
                <div class="flex gap-1 mt-1">
                    <input id="essay-dap-${i}" class="flex-1 p-1 border border-slate-300 rounded text-xs" placeholder="Đáp án">
                    <input id="essay-goi-${i}" class="flex-1 p-1 border border-slate-300 rounded text-xs" placeholder="Gợi ý">
                </div>
            `;
            cont.appendChild(d);
            const removeBtn = d.querySelector('.remove-item-btn');
            if (removeBtn) removeBtn.onclick = () => removeEssayItem(i);

            const de = d.querySelector(`#essay-de-${i}`);
            de.value = it.de || '';
            de.oninput = () => { essayItems[i].de = de.value; syncEssayToTextarea({ refreshPreview: true }); };
            const dap = d.querySelector(`#essay-dap-${i}`);
            dap.value = it.dap || '';
            dap.oninput = () => { essayItems[i].dap = dap.value; syncEssayToTextarea({ refreshPreview: true }); };
            const goi = d.querySelector(`#essay-goi-${i}`);
            goi.value = it.goi || '';
            goi.oninput = () => { essayItems[i].goi = goi.value; syncEssayToTextarea({ refreshPreview: true }); };
        });
        setupRichToolbars();
        setupDynamicImagePaste();
    }
    function addEssayItem() { essayItems.push({de:'', dap:'', goi:''}); renderEssayItems(); syncEssayToTextarea({ refreshPreview: true }); }
    function removeEssayItem(i) { essayItems.splice(i,1); renderEssayItems(); syncEssayToTextarea({ refreshPreview: true }); }

    function syncFillToTextarea(options = {}) {
        const ta = el('lessonFill');
        if (!ta) return;
        ta.value = fillItems.map(i => `${i.de}|${i.manh}|${i.dap}|${i.goi}`).join('\n');
        if (options.refreshPreview && interactiveEditorMode === 'items') scheduleRenderPreview();
    }
    function renderFillItems() {
        const cont = el('fillItems');
        if (!cont) return;
        cont.innerHTML = '';
        fillItems.forEach((it, i) => {
            const d = document.createElement('div');
            d.className = 'p-2.5 border border-slate-200 rounded-lg bg-white text-xs shadow-sm';
            d.innerHTML = `
                <div class="flex items-center mb-1"><span class="font-bold text-teal-700">Kéo thả ${i+1}</span><button type="button" class="remove-item-btn ml-auto text-rose-500 hover:text-rose-700">✕</button></div>
                ${richToolbarHtml(`fill-de-${i}`)}
                <textarea id="fill-de-${i}" class="w-full p-1.5 border border-slate-300 rounded text-xs" placeholder="Câu có ___ (dán ảnh nếu cần)"></textarea>
                <div class="grid grid-cols-3 gap-1 mt-1">
                    <input id="fill-manh-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="Mảnh » ...">
                    <input id="fill-dap-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="Đáp án">
                    <input id="fill-goi-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="Gợi ý">
                </div>
            `;
            cont.appendChild(d);
            const removeBtn = d.querySelector('.remove-item-btn');
            if (removeBtn) removeBtn.onclick = () => removeFillItem(i);

            const de = d.querySelector(`#fill-de-${i}`); de.value = it.de||''; de.oninput = ()=>{fillItems[i].de=de.value; syncFillToTextarea({ refreshPreview: true });};
            ['manh','dap','goi'].forEach(k=>{ const inp=d.querySelector(`#fill-${k}-${i}`); inp.value=it[k]||''; inp.oninput=()=>{fillItems[i][k]=inp.value; syncFillToTextarea({ refreshPreview: true });}; });
        });
        setupRichToolbars();
        setupDynamicImagePaste();
    }
    function addFillItem(){ fillItems.push({de:'',manh:'',dap:'',goi:''}); renderFillItems(); syncFillToTextarea({ refreshPreview: true }); }
    function removeFillItem(i){ fillItems.splice(i,1); renderFillItems(); syncFillToTextarea({ refreshPreview: true }); }

    function syncDragToTextarea(options = {}) {
        const ta = el('lessonDrag');
        if (!ta) return;
        ta.value = dragItems.map(item => {
            if (isDragMatchItem(item)) {
                return `${item.de}|${item.trai}|${item.phai}|${item.map}|${item.goi}`;
            }
            return `${item.de}|${item.trai}|${item.phai}|${item.goi}`;
        }).join('\n');
        if (options.refreshPreview && interactiveEditorMode === 'items') scheduleRenderPreview();
    }
    function renderDragItems() {
        const cont = el('dragItems');
        if (!cont) return;
        cont.innerHTML = '';
        dragItems.forEach((it, i) => {
            const d = document.createElement('div');
            d.className = 'p-2.5 border border-slate-200 rounded-lg bg-white text-xs shadow-sm';
            d.innerHTML = `
                <div class="flex items-center mb-1"><span class="font-bold text-teal-700">Nối/Sắp xếp ${i+1}</span><button type="button" class="remove-item-btn ml-auto text-rose-500 hover:text-rose-700">✕</button></div>
                ${richToolbarHtml(`drag-de-${i}`)}
                <textarea id="drag-de-${i}" class="w-full p-1.5 border border-slate-300 rounded text-xs" placeholder="Đề (dán ảnh nếu cần)"></textarea>
                <div class="grid grid-cols-4 gap-1 mt-1">
                    <input id="drag-trai-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="Trái »">
                    <input id="drag-phai-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="Phải »">
                    <input id="drag-map-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="0-0,1-1">
                    <input id="drag-goi-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="Gợi ý">
                </div>
            `;
            cont.appendChild(d);
            const removeBtn = d.querySelector('.remove-item-btn');
            if (removeBtn) removeBtn.onclick = () => removeDragItem(i);

            const de = d.querySelector(`#drag-de-${i}`); de.value = it.de||''; de.oninput = ()=>{dragItems[i].de=de.value; syncDragToTextarea({ refreshPreview: true });};
            ['trai','phai','map','goi'].forEach(k=>{ const inp=d.querySelector(`#drag-${k}-${i}`); inp.value=it[k]||''; inp.oninput=()=>{dragItems[i][k]=inp.value; syncDragToTextarea({ refreshPreview: true });}; });
        });
        setupRichToolbars();
        setupDynamicImagePaste();
    }
    function addDragItem(){ dragItems.push({de:'',trai:'',phai:'',map:'',goi:''}); renderDragItems(); syncDragToTextarea({ refreshPreview: true }); }
    function removeDragItem(i){ dragItems.splice(i,1); renderDragItems(); syncDragToTextarea({ refreshPreview: true }); }

    function syncQuestionsToTextarea(options = {}) {
        const ta = el('lessonQuestions');
        if (!ta) return;
        ta.value = questionItems.map(row => [
            row.skill || '',
            row.cau || '',
            row.a || '',
            row.b || '',
            row.c || '',
            row.d || '',
            row.dung || ''
        ].join(' | ')).join('\n');
        if (options.refreshPreview && questionsEditorMode === 'items') scheduleRenderPreview();
    }
    function renderQuestionItems() {
        const cont = el('questionItems');
        if (!cont) return;
        cont.innerHTML = '';
        questionItems.forEach((it, i) => {
            const d = document.createElement('div');
            d.className = 'p-2.5 border border-slate-200 rounded-lg bg-white text-xs shadow-sm';
            d.innerHTML = `
                <div class="flex items-center mb-1"><span class="font-bold text-teal-700">Câu ${i+1}</span><button type="button" class="remove-item-btn ml-auto text-rose-500 hover:text-rose-700">✕</button></div>
                ${richToolbarHtml(`q-cau-${i}`)}
                <textarea id="q-cau-${i}" class="w-full p-1.5 border border-slate-300 rounded text-xs" placeholder="Câu hỏi (dán ảnh nếu cần)"></textarea>
                <div class="grid grid-cols-5 gap-1 mt-1">
                    <input id="q-a-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="A">
                    <input id="q-b-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="B">
                    <input id="q-c-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="C">
                    <input id="q-d-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="D">
                    <input id="q-dung-${i}" class="p-1 border border-slate-300 rounded text-xs" placeholder="Đúng (A/B/C/D)">
                </div>
            `;
            cont.appendChild(d);
            const removeBtn = d.querySelector('.remove-item-btn');
            if (removeBtn) removeBtn.onclick = () => removeQuestionItem(i);

            const cau = d.querySelector(`#q-cau-${i}`); cau.value=it.cau||''; cau.oninput=()=>{questionItems[i].cau=cau.value; syncQuestionsToTextarea({ refreshPreview: true });};
            ['a','b','c','d','dung'].forEach(k=>{ const inp=d.querySelector(`#q-${k}-${i}`); inp.value=it[k]||''; inp.oninput=()=>{questionItems[i][k]=inp.value; syncQuestionsToTextarea({ refreshPreview: true });}; });
        });
        setupRichToolbars();
        setupDynamicImagePaste();
    }
    function addQuestionItem(){ questionItems.push({skill:'',cau:'',a:'',b:'',c:'',d:'',dung:''}); renderQuestionItems(); syncQuestionsToTextarea({ refreshPreview: true }); }
    function removeQuestionItem(i){ questionItems.splice(i,1); renderQuestionItems(); syncQuestionsToTextarea({ refreshPreview: true }); }

    // parse from | format to items (for load)
    function parseEssayToItems(str) {
        return (str || '').split('\n').filter(Boolean).map(line => {
            const p = splitQuestionParts(line);
            return {de: p[0] || '', dap: p[1] || '', goi: p[2] || ''};
        });
    }
    function parseFillToItems(str) {
        return (str || '').split('\n').filter(Boolean).map(line => {
            const normalized = normalizeFillParts(splitQuestionParts(line));
            return {
                de: normalized.prompt || '',
                manh: joinPoolText(normalized.pool),
                dap: joinPoolText(normalized.answers),
                goi: normalized.hint || ''
            };
        });
    }
    function parseDragToItems(str) {
        const text = String(str || '').trim();
        if (!text) return [];
        return text.split('\n').filter(Boolean).map(line => {
            const p = splitQuestionParts(line);
            const pairSpec = String(p[3] || '').trim();
            if (p.length >= 4 && /\d+\s*-\s*\d+/.test(pairSpec)) {
                return { de: p[0] || '', trai: p[1] || '', phai: p[2] || '', map: pairSpec, goi: p[4] || '' };
            }
            const left = splitPoolText(p[1]);
            const right = splitPoolText(p[2]);
            if (poolTextHasMultipleItems(p[1]) && poolTextHasMultipleItems(p[2]) && !poolsLookLikeSortOrder(left, right)) {
                return {
                    de: p[0] || '',
                    trai: p[1] || '',
                    phai: p[2] || '',
                    map: buildDefaultMatchPairSpec(left.length, right.length),
                    goi: p[3] || ''
                };
            }
            return { de: p[0] || '', trai: p[1] || '', phai: p[2] || '', map: '', goi: p[3] || '' };
        });
    }
    function parseQuestionToItems(str) {
        const text = String(str || '').trim();
        if (!text) return [];
        const skills = parseSkills(el('lessonSkills')?.value || '');
        try {
            return questionsToEditorItems(parseQuestions(text, skills), skills);
        } catch {
            return text.split('\n').map(line => line.trim()).filter(Boolean).map(line => {
                const p = splitQuestionParts(normalizeMcqBulkLine(line));
                if (p.length < 6) return null;
                const hasSkill = p.length >= 7 && looksLikeSkillId(p[0]);
                const offset = hasSkill ? 1 : 0;
                return {
                    skill: hasSkill ? p[0] : '',
                    cau: p[offset] || '',
                    a: p[offset + 1] || '',
                    b: p[offset + 2] || '',
                    c: p[offset + 3] || '',
                    d: p[offset + 4] || '',
                    dung: p[offset + 5] || ''
                };
            }).filter(Boolean);
        }
    }

    function serializeInteractiveBulkFromItems() {
        const parts = [];
        if (essayItems.length) {
            parts.push('**BÀI TẬP TỰ LUẬN NGẮN**');
            parts.push(...essayItems.map(item => `${item.de}|${item.dap}|${item.goi}`));
            parts.push('');
        }
        if (fillItems.length) {
            parts.push('**KÉO THẢ VÀO Ô TRỐNG**');
            parts.push(...fillItems.map(item => `${item.de}|${item.manh}|${item.dap}|${item.goi}`));
            parts.push('');
        }
        const sortItems = dragItems.filter(item => !isDragMatchItem(item));
        const matchItems = dragItems.filter(item => isDragMatchItem(item));
        if (sortItems.length) {
            parts.push('**SẮP XẾP THỨ TỰ**');
            parts.push(...sortItems.map(item => `${item.de}|${item.trai}|${item.phai}|${item.goi}`));
            parts.push('');
        }
        if (matchItems.length) {
            parts.push('**NỐI Ô**');
            parts.push(...matchItems.map(item => `${item.de}|${item.trai}|${item.phai}|${item.map}|${item.goi}`));
        }
        return parts.join('\n').trim();
    }

    function refreshInteractiveBulkTextarea() {
        const ta = el('interactiveBulkPaste');
        if (!ta) return;
        ta.value = serializeInteractiveBulkFromItems();
    }

    function readInteractiveBulkText() {
        return String(el('interactiveBulkPaste')?.value || '').trim();
    }

    function syncItemsFromInteractiveBulk() {
        const bulkText = readInteractiveBulkText();
        if (!bulkText) {
            if (essayItems.length || fillItems.length || dragItems.length) return;
            essayItems = [];
            fillItems = [];
            dragItems = [];
            syncEssayToTextarea();
            syncFillToTextarea();
            syncDragToTextarea();
            return;
        }
        const parsed = parseInteractiveBulkPaste(bulkText);
        essayItems = parseEssayToItems(parsed.essay);
        fillItems = parseFillToItems(parsed.fill);
        dragItems = [
            ...parseDragExercises(parsed.dragMatch, { preferMatch: true }),
            ...parseDragExercises(parsed.dragSort),
            ...parseDragExercises(parsed.drag)
        ].map(item => {
            if (item.mode === 'match') {
                return {
                    de: item.prompt || '',
                    trai: joinPoolText(item.left),
                    phai: joinPoolText(item.right),
                    map: item.pair_spec || '',
                    goi: item.hint || ''
                };
            }
            return {
                de: item.prompt || '',
                trai: joinPoolText(item.items),
                phai: joinPoolText(item.answer),
                map: '',
                goi: item.hint || ''
            };
        });
        syncEssayToTextarea();
        syncFillToTextarea();
        syncDragToTextarea();
    }

    function serializeQuestionsBulkFromItems() {
        return questionItems.map(item => [
            item.skill || '',
            item.cau || '',
            item.a || '',
            item.b || '',
            item.c || '',
            item.d || '',
            item.dung || ''
        ].join(' | ')).join('\n');
    }

    function refreshQuestionsBulkTextarea() {
        const ta = el('questionsBulkPaste');
        if (!ta) return;
        ta.value = serializeQuestionsBulkFromItems();
    }

    function readQuestionsBulkText() {
        return String(el('questionsBulkPaste')?.value || '').split('\n').map(line => line.trim()).filter(line => {
            if (!line.includes('|')) return false;
            const heading = normalizeBulkHeading(line);
            return !/^TRẮC NGHIỆM|^KỸ NĂNG|^NHIỆM VỤ/.test(heading);
        }).map(normalizeMcqBulkLine).filter(Boolean).join('\n');
    }

    function syncItemsFromQuestionsBulk() {
        const bulkText = readQuestionsBulkText();
        if (!bulkText) {
            if (questionItems.length) return;
            questionItems = [];
            syncQuestionsToTextarea();
            return;
        }
        questionItems = parseQuestionToItems(bulkText);
        syncQuestionsToTextarea();
    }

    function applyEditorModeButtons(activeBtn, inactiveBtn, activeIsFirst) {
        if (activeBtn) {
            activeBtn.classList.toggle('bg-teal-600', activeIsFirst);
            activeBtn.classList.toggle('text-white', activeIsFirst);
            activeBtn.classList.toggle('bg-white', !activeIsFirst);
            activeBtn.classList.toggle('text-slate-600', !activeIsFirst);
        }
        if (inactiveBtn) {
            inactiveBtn.classList.toggle('bg-teal-600', !activeIsFirst);
            inactiveBtn.classList.toggle('text-white', !activeIsFirst);
            inactiveBtn.classList.toggle('bg-white', activeIsFirst);
            inactiveBtn.classList.toggle('text-slate-600', activeIsFirst);
        }
    }

    function setInteractiveEditorMode(mode, options = {}) {
        const { skipSync = false } = options;
        const nextMode = mode === 'items' ? 'items' : 'bulk';
        if (!skipSync && nextMode !== interactiveEditorMode) {
            if (interactiveEditorMode === 'bulk' && nextMode === 'items') {
                syncItemsFromInteractiveBulk();
                renderEssayItems();
                renderFillItems();
                renderDragItems();
            } else if (interactiveEditorMode === 'items' && nextMode === 'bulk') {
                refreshInteractiveBulkTextarea();
            }
        }
        interactiveEditorMode = nextMode;
        const isBulk = interactiveEditorMode === 'bulk';
        el('interactiveBulkPanel')?.classList.toggle('hidden', !isBulk);
        el('interactiveItemsPanel')?.classList.toggle('hidden', isBulk);
        applyEditorModeButtons(el('interactiveModeBulk'), el('interactiveModeItems'), isBulk);
        const hint = el('interactiveModeHint');
        if (hint) {
            hint.textContent = isBulk
                ? 'Dán khối BÀI TẬP TƯƠNG TÁC từ Gemini. Chuyển sang Từng câu để chỉnh chi tiết hoặc dán ảnh vào đề.'
                : 'Soạn từng bài, dán ảnh vào đề khi cần. Chuyển sang Hàng loạt để xem/ghi theo format Gemini.';
        }
        if (!skipSync) scheduleRenderPreview();
    }

    function setQuestionsEditorMode(mode, options = {}) {
        const { skipSync = false } = options;
        const nextMode = mode === 'items' ? 'items' : 'bulk';
        if (!skipSync && nextMode !== questionsEditorMode) {
            if (questionsEditorMode === 'bulk' && nextMode === 'items') {
                syncItemsFromQuestionsBulk();
                renderQuestionItems();
            } else if (questionsEditorMode === 'items' && nextMode === 'bulk') {
                refreshQuestionsBulkTextarea();
            }
        }
        questionsEditorMode = nextMode;
        const isBulk = questionsEditorMode === 'bulk';
        el('questionsBulkPanel')?.classList.toggle('hidden', !isBulk);
        el('questionsItemsPanel')?.classList.toggle('hidden', isBulk);
        applyEditorModeButtons(el('questionsModeBulk'), el('questionsModeItems'), isBulk);
        const hint = el('questionsModeHint');
        if (hint) {
            hint.textContent = isBulk
                ? 'Dán các dòng trắc nghiệm từ Gemini. Chuyển sang Từng câu để chỉnh hoặc dán ảnh vào câu hỏi.'
                : 'Soạn từng câu, dán ảnh khi cần. Chuyển sang Hàng loạt để xem/ghi theo format Gemini.';
        }
        if (!skipSync) scheduleRenderPreview();
    }

    function formatImageManifestText(lesson) {
        const saved = Array.isArray(lesson?.image_manifest) ? lesson.image_manifest : [];
        const savedById = new Map(saved.map(img => [String(img.id || '').toUpperCase(), img]));
        const pkg = LI.packageFromSavePayload({
            goal_text: lesson?.goal || lesson?.goal_text || '',
            theory: lesson?.theory || [],
            examples: lesson?.examples || [],
            self_practice: lesson?.self_practice || [],
            essay_exercises: lesson?.essay_exercises || [],
            fill_exercises: lesson?.fill_exercises || [],
            drag_exercises: lesson?.drag_exercises || [],
            questions: lesson?.questions || []
        });
        const markers = LI.collectMarkersFromPackage(pkg);
        const ids = [...new Set([...markers, ...saved.map(img => img.id).filter(Boolean)])];
        if (!ids.length) return '';
        return ids.map(id => {
            const entry = savedById.get(String(id).toUpperCase()) || saved.find(img => img.id === id);
            if (entry) {
                return `${entry.id}: LOẠI: ${entry.type || 'diagram'} | ${entry.alt || entry.id}`;
            }
            return `${id}: LOẠI: diagram | ${id}`;
        }).join('\n');
    }

    function buildFormLessonPackage() {
        flushBulkEditorsBeforeSave();
        const skills = parseSkills(el('lessonSkills').value);
        let questions = [];
        try { questions = resolveQuestionsForSave(skills); } catch { questions = []; }
        return LI.packageFromSavePayload({
            subject: (isPageScopedEditor() ? PAGE_SUBJECT : el('lessonSubject').value).trim(),
            chapter: el('lessonChapter').value.trim(),
            title: el('lessonTitleInput').value.trim(),
            slug: el('lessonSlug').value.trim(),
            order_index: Number(el('lessonOrder').value) || 0,
            is_published: false,
            goal_text: el('lessonGoalInput').value.trim(),
            theory: parseTheoryBlocks(el('lessonTheory').value),
            examples: parseExamples(el('lessonExamples').value),
            self_practice: parseExamples(el('lessonSelfPractice')?.value || ''),
            essay_exercises: parseEssayExercises(el('lessonEssay').value),
            fill_exercises: parseFillExercises(el('lessonFill').value),
            drag_exercises: buildDragExercisesFromItems(dragItems),
            videos: parseVideos(el('lessonVideos').value),
            skills,
            tasks: parseLines(el('lessonTasks').value),
            questions,
            image_manifest: LI.parseImageManifest(el('lessonImageManifest')?.value || '')
        });
    }

    function applyLessonPackageToForm(pkg, report) {
        const filled = [];
        if (pkg.goal_text) { el('lessonGoalInput').value = pkg.goal_text; filled.push('mục tiêu'); }
        if (pkg.chapter) {
            el('lessonChapter').value = pkg.chapter;
            filled.push('chương');
        }
        if (pkg.title) {
            el('lessonTitleInput').value = pkg.title;
            filled.push('tên bài');
        }
        if (pkg.slug) el('lessonSlug').value = pkg.slug;
        if (pkg.order_index) el('lessonOrder').value = String(pkg.order_index);
        if (!isPageScopedEditor() && pkg.subject) {
            el('lessonSubject').value = pkg.subject;
            selectedSubject = pkg.subject;
        }
        el('lessonPublished').checked = false;

        if (pkg.theory?.length) {
            el('lessonTheory').value = LI.formatTheoryBlocks(pkg.theory);
            filled.push('lý thuyết');
        }
        if (pkg.examples?.length) {
            el('lessonExamples').value = pkg.examples.map(ex => `${ex.title}\n${ex.body}`).join('\n\n');
            filled.push('ví dụ');
        }
        if (pkg.self_practice?.length) {
            el('lessonSelfPractice').value = pkg.self_practice.map(ex => `${ex.title}\n${ex.body}`).join('\n\n');
            filled.push('bài nộp');
        }
        if (pkg.skills?.length) {
            el('lessonSkills').value = pkg.skills.map(s => `${s.id} | ${s.name} | ${s.target}`).join('\n');
            filled.push(`kỹ năng (${pkg.skills.length})`);
        }
        if (pkg.essay_exercises?.length) {
            el('lessonEssay').value = formatEssayExercises(pkg.essay_exercises);
            filled.push(`tự luận (${pkg.essay_exercises.length})`);
        }
        if (pkg.fill_exercises?.length) {
            el('lessonFill').value = formatFillExercises(pkg.fill_exercises);
            filled.push(`điền khuyết (${pkg.fill_exercises.length})`);
        }
        if (pkg.drag_exercises?.length) {
            dragItems = pkg.drag_exercises.map(item => {
                if (item.mode === 'match') {
                    return {
                        de: item.prompt || '',
                        trai: joinPoolText(item.left),
                        phai: joinPoolText(item.right),
                        map: item.pair_spec || (item.pairs || []).map(p => `${p.left}-${p.right}`).join(','),
                        goi: item.hint || ''
                    };
                }
                return {
                    de: item.prompt || '',
                    trai: joinPoolText(item.items),
                    phai: joinPoolText(item.answer),
                    map: '',
                    goi: item.hint || ''
                };
            });
            syncDragToTextarea();
            const matchCount = pkg.drag_exercises.filter(d => d.mode === 'match').length;
            filled.push(`nối ô/sắp xếp (${pkg.drag_exercises.length}, nối ô: ${matchCount})`);
        }
        if (pkg.questions?.length) {
            el('lessonQuestions').value = LI.formatQuestionsBulk(pkg.questions);
            filled.push(`trắc nghiệm (${pkg.questions.length})`);
        }
        if (pkg.tasks?.length) {
            el('lessonTasks').value = pkg.tasks.join('\n');
            filled.push('nhiệm vụ');
        }
        if (pkg.videos?.length) {
            el('lessonVideos').value = formatVideos(pkg.videos);
            filled.push(`video (${pkg.videos.length})`);
        }
        if (pkg.image_manifest?.length && el('lessonImageManifest')) {
            el('lessonImageManifest').value = pkg.image_manifest.map(img =>
                `${img.id}: LOẠI: ${img.type || 'diagram'} | ${img.alt || img.id}`
            ).join('\n');
        }

        essayItems = parseEssayToItems(el('lessonEssay').value || '');
        fillItems = parseFillToItems(el('lessonFill').value || '');
        if (!pkg.drag_exercises?.length) {
            dragItems = parseDragToItems(el('lessonDrag').value || '');
        }
        questionItems = parseQuestionToItems(el('lessonQuestions').value || '');
        renderEssayItems();
        renderFillItems();
        renderDragItems();
        renderQuestionItems();
        refreshInteractiveBulkTextarea();
        refreshQuestionsBulkTextarea();
        ['lessonTheory', 'lessonExamples', 'lessonSelfPractice'].forEach(id => {
            const field = el(id);
            if (field) renderLessonFieldImagePreview(field);
        });
        renderPreview();
        return { filled, report };
    }

    function importGeminiLessonRaw(raw) {
        if (!requireLessonImport()) return;
        const text = String(raw || '').trim();
        if (!text) {
            alert('Dán nội dung Gemini trả về trước.');
            return;
        }
        const pkg = LI.buildLessonImportPackage({
            rawGeminiText: text,
            metadata: {
                subject: isPageScopedEditor() ? PAGE_SUBJECT : (el('lessonSubject')?.value || selectedSubject),
                chapter: el('lessonChapter')?.value || '',
                title: el('lessonTitleInput')?.value || '',
                slug: el('lessonSlug')?.value || '',
                tool: 'gemini-text-import'
            }
        });
        const validation = LI.validateLessonImportPackage(pkg, {
            pageSubject: PAGE_SUBJECT || '',
            existingSlugs: lessonsForScope().map(l => l.slug).filter(Boolean)
        });
        const { filled } = applyLessonPackageToForm(pkg, validation);
        if (!filled.length) {
            alert('Không nhận diện được section. Hãy đảm bảo Gemini trả về đúng heading: LÝ THUYẾT, NỐI Ô, TRẮC NGHIỆM, KỸ NĂNG...');
            return;
        }
        if (!el('lessonSlug').value.trim()) suggestSlug();
        const warnText = validation.warnings.length ? `\n\nCảnh báo:\n• ${validation.warnings.join('\n• ')}` : '';
        const errText = validation.errors.length ? `\n\nLỗi (vẫn điền form, kiểm tra trước khi lưu):\n• ${validation.errors.join('\n• ')}` : '';
        alert(`Đã điền: ${filled.join(', ')}.${warnText}${errText}\n\nKiểm tra preview → dán ảnh thật thay HINH_xx → bấm Lưu bài học.`);
        el('geminiImportRaw').value = '';
    }

    function importLessonJsonFile(file) {
        if (!requireLessonImport()) return;
        const reader = new FileReader();
        reader.onload = () => {
            let parsed;
            try {
                parsed = JSON.parse(String(reader.result || ''));
            } catch {
                alert('File JSON không hợp lệ.');
                return;
            }
            const pkg = LI.normalizeLessonImportPackage(parsed, {
                defaultSubject: isPageScopedEditor() ? PAGE_SUBJECT : selectedSubject,
                forceUnpublished: true
            });
            const validation = LI.validateLessonImportPackage(pkg, {
                pageSubject: PAGE_SUBJECT || '',
                existingSlugs: lessonsForScope().map(l => l.slug).filter(Boolean)
            });
            if (validation.errors.length) {
                alert(`Không import được:\n• ${validation.errors.join('\n• ')}`);
                return;
            }
            const { filled } = applyLessonPackageToForm(pkg, validation);
            const warnText = validation.warnings.length ? `\n\nCảnh báo:\n• ${validation.warnings.join('\n• ')}` : '';
            alert(`Đã import JSON: ${filled.join(', ')}.${warnText}\n\nChưa lưu — kiểm tra và bấm Lưu bài học.`);
        };
        reader.readAsText(file, 'utf-8');
    }

    function exportLessonJson() {
        if (!requireLessonImport()) return;
        const pkg = buildFormLessonPackage();
        const validation = LI.validateLessonImportPackage(pkg, { pageSubject: PAGE_SUBJECT || '' });
        const blob = new Blob([JSON.stringify(pkg, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${pkg.slug || 'lesson'}-import-v1.json`;
        a.click();
        URL.revokeObjectURL(url);
        const parts = [`Đã tải file: ${pkg.slug || 'lesson'}-import-v1.json`];
        if (validation.warnings.length) {
            parts.push(`Cảnh báo:\n• ${validation.warnings.join('\n• ')}`);
        }
        if (validation.errors.length) {
            parts.push(`Lỗi dữ liệu (sửa tab Tương tác / Trắc nghiệm trước khi lưu):\n• ${validation.errors.join('\n• ')}`);
        }
        if (parts.length > 1) alert(parts.join('\n\n'));
    }

    function openStudentPreview() {
        if (!requireLessonImport()) return;
        const pkg = buildFormLessonPackage();
        const markers = LI.collectMarkersFromPackage(pkg);
        const manifestIds = new Set((pkg.image_manifest || []).map(m => m.id));
        const missing = markers.filter(id => !manifestIds.has(id));
        const dragMatch = (pkg.drag_exercises || []).filter(d => d.mode === 'match').length;
        const dragSort = (pkg.drag_exercises || []).length - dragMatch;
        const lines = [
            `<header style="border-bottom:2px solid #0d9488;padding-bottom:1rem;margin-bottom:1.5rem">`,
            `<h1 style="margin:0 0 .5rem">${escapeHtml(pkg.title || 'Xem thử')}</h1>`,
            `<p style="margin:0;color:#475569"><strong>${escapeHtml(pkg.subject)}</strong> · ${escapeHtml(pkg.chapter)} · <code>${escapeHtml(pkg.slug || '')}</code></p>`,
            `</header>`
        ];
        if (pkg.goal_text) {
            lines.push(`<section style="margin-bottom:1.5rem"><h2>Mục tiêu</h2><p>${escapeHtml(pkg.goal_text)}</p></section>`);
        }
        if (missing.length) {
            lines.push(`<p style="color:#b45309;background:#fffbeb;padding:.75rem;border-radius:.5rem">Ảnh còn thiếu manifest: ${missing.map(escapeHtml).join(', ')}</p>`);
        }
        lines.push(`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:.5rem;margin:1rem 0;padding:1rem;background:#f8fafc;border-radius:.5rem;font-size:.85rem">`);
        lines.push(`<div><div style="color:#64748b">Lý thuyết</div><strong>${(pkg.theory || []).length} đoạn</strong></div>`);
        lines.push(`<div><div style="color:#64748b">Ví dụ</div><strong>${(pkg.examples || []).length}</strong></div>`);
        lines.push(`<div><div style="color:#64748b">Tương tác</div><strong>${(pkg.essay_exercises || []).length + (pkg.fill_exercises || []).length + (pkg.drag_exercises || []).length}</strong><div style="font-size:.75rem;color:#64748b">TL ${(pkg.essay_exercises || []).length} · ĐK ${(pkg.fill_exercises || []).length} · Nối ${dragMatch} · SX ${dragSort}</div></div>`);
        lines.push(`<div><div style="color:#64748b">Trắc nghiệm</div><strong>${(pkg.questions || []).length}</strong></div>`);
        lines.push(`<div><div style="color:#64748b">Kỹ năng</div><strong>${(pkg.skills || []).length}</strong></div>`);
        lines.push(`</div>`);
        if ((pkg.skills || []).length) {
            lines.push(`<section style="margin-bottom:1.5rem"><h2>Kỹ năng</h2><ul>${pkg.skills.map(s => `<li><code>${escapeHtml(s.id)}</code> — ${escapeHtml(s.name)} (${s.target || 80}%)</li>`).join('')}</ul></section>`);
        }
        (pkg.theory || []).forEach((block, i) => {
            const text = typeof block === 'string' ? block : (block.text || '');
            const ai = typeof block === 'object' && block.ai ? ' <span style="color:#7c3aed">[AI]</span>' : '';
            lines.push(`<section style="margin-bottom:1rem"><h3>Lý thuyết ${i + 1}${ai}</h3><pre style="white-space:pre-wrap;background:#fff;border:1px solid #e2e8f0;padding:.75rem;border-radius:.5rem">${escapeHtml(text)}</pre></section>`);
        });
        (pkg.examples || []).slice(0, 3).forEach((ex, i) => {
            lines.push(`<section style="margin-bottom:1rem"><h3>${escapeHtml(ex.title || `Ví dụ ${i + 1}`)}</h3><pre style="white-space:pre-wrap;background:#fff;border:1px solid #e2e8f0;padding:.75rem;border-radius:.5rem">${escapeHtml(ex.body || '')}</pre></section>`);
        });
        if ((pkg.examples || []).length > 3) {
            lines.push(`<p style="color:#64748b;font-size:.85rem">… và ${pkg.examples.length - 3} ví dụ khác</p>`);
        }
        (pkg.questions || []).slice(0, 2).forEach((q, i) => {
            const opts = (q.options || []).map((opt, j) => `<li>${'ABCD'[j]}. ${escapeHtml(opt)}</li>`).join('');
            const ans = 'ABCD'[Number(q.answer)] || '?';
            lines.push(`<section style="margin-bottom:1rem"><h3>Câu ${i + 1}${q.skill ? ` <small style="color:#64748b">(${escapeHtml(q.skill)})</small>` : ''}</h3><p>${escapeHtml(q.prompt || '')}</p><ol type="A" style="list-style:none;padding:0">${opts}</ol><p style="color:#0d9488;font-size:.85rem">Đáp án: ${ans}</p></section>`);
        });
        if ((pkg.questions || []).length > 2) {
            lines.push(`<p style="color:#64748b;font-size:.85rem">… và ${pkg.questions.length - 2} câu trắc nghiệm khác</p>`);
        }
        const html = `<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8"><title>Xem thử — ${escapeHtml(pkg.title || '')}</title>
            <style>body{font-family:Segoe UI,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;line-height:1.5;color:#1e293b} h2{color:#0d9488;border-bottom:1px solid #e2e8f0;padding-bottom:.25rem} h3{color:#334155;font-size:1rem}</style></head><body>${lines.join('')}<footer style="margin-top:2rem;padding-top:1rem;border-top:1px solid #e2e8f0;color:#64748b;font-size:.85rem"><em>Preview nhanh từ form — lưu bài để học sinh xem đầy đủ trên lộ trình.</em></footer></body></html>`;
        const w = window.open('', '_blank');
        if (w) { w.document.write(html); w.document.close(); }
    }

    function resolveDragForSave() {
        const bulkText = readInteractiveBulkText();
        if (bulkText && interactiveEditorMode === 'bulk') {
            syncItemsFromInteractiveBulk();
        }
        return buildDragExercisesFromItems(dragItems);
    }

    function flushBulkEditorsBeforeSave() {
        if (interactiveEditorMode === 'bulk') {
            const bulkText = readInteractiveBulkText();
            if (bulkText) {
                syncItemsFromInteractiveBulk();
            } else if (!dragItems.length && String(el('lessonDrag')?.value || '').trim()) {
                dragItems = parseDragToItems(el('lessonDrag').value);
            }
        }
        if (questionsEditorMode === 'bulk') {
            const bulkText = readQuestionsBulkText();
            if (bulkText) {
                syncItemsFromQuestionsBulk();
            } else if (!questionItems.length && String(el('lessonQuestions')?.value || '').trim()) {
                questionItems = parseQuestionToItems(el('lessonQuestions').value);
            }
        }
        syncEssayToTextarea();
        syncFillToTextarea();
        syncDragToTextarea();
        syncQuestionsToTextarea();
    }

    function resolveQuestionsForSave(skills) {
        const bulkText = readQuestionsBulkText();
        const rawText = bulkText || String(el('lessonQuestions')?.value || '').trim();
        if (!rawText) return [];
        return parseQuestions(rawText, skills);
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
                const clipboard = event.clipboardData;
                const hasImage = Array.from(clipboard?.items || []).some(item =>
                    item.kind === 'file' && String(item.type || '').startsWith('image/')
                ) || Array.from(clipboard?.files || []).some(file =>
                    String(file.type || '').startsWith('image/')
                );

                // Ảnh screenshot phải đi tiếp tới handleRichImagePaste() để upload Drive.
                // Handler này đang chạy ở capture phase nên nếu chặn ở đây, listener ảnh sẽ không bao giờ nhận được event.
                if (hasImage) {
                    const imageItem = Array.from(clipboard?.items || []).find(item =>
                        item.kind === 'file' && String(item.type || '').startsWith('image/')
                    );
                    const imageFile = imageItem?.getAsFile() || Array.from(clipboard?.files || []).find(file =>
                        String(file.type || '').startsWith('image/')
                    );
                    if (imageFile) {
                        event.preventDefault();
                        event.stopImmediatePropagation();
                        void uploadImageFileToDrive(imageFile, field);
                    }
                    return;
                }

                const text = clipboard?.getData('text/plain');
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
            <div class="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between mb-2">
                <div>
                    <h3 class="font-bold text-slate-800 text-lg">
                        <i class="fas fa-book-open text-teal-600 mr-2"></i>Thiết kế bài học
                    </h3>
                    <p id="lessonEditorScopeHint" class="text-sm text-slate-500">Mỗi tab là một phần nội dung. <strong>Dán ảnh (Ctrl+V) sẽ tự nén (tối đa 1200px, ~480KB) rồi upload Google Drive</strong> và chèn link. Bài tập tương tác / Trắc nghiệm có 2 chế độ <strong>Hàng loạt ↔ Từng câu</strong>, chuyển qua lại được.</p>
                </div>
                <div class="flex flex-wrap gap-2" id="subjectPills"></div>
            </div>

            <!-- Lesson picker + actions (clean top bar, no mixing with fields) -->
            <div class="flex flex-wrap items-center gap-2 mb-3 p-2 bg-slate-50 border border-slate-200 rounded">
                <div class="flex-1 min-w-[240px]">
                    <select id="lessonSelect" class="w-full p-2 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-teal-500 outline-none"></select>
                </div>
                <button id="newLessonBtn" type="button" class="px-3 py-1.5 text-xs bg-slate-800 text-white rounded font-bold"><i class="fas fa-plus mr-1"></i>Mới</button>
                <button id="duplicateLessonBtn" type="button" class="px-3 py-1.5 text-xs bg-white border border-slate-300 rounded font-bold"><i class="fas fa-copy mr-1"></i>Nhân bản</button>
                <button id="deleteLessonBtn" type="button" class="px-3 py-1.5 text-xs bg-rose-50 border border-rose-200 text-rose-700 rounded font-bold"><i class="fas fa-trash mr-1"></i>Xóa</button>
                <button id="lessonReloadBtn" type="button" class="px-3 py-1.5 text-xs bg-white border border-slate-300 rounded font-bold"><i class="fas fa-rotate-right mr-1"></i>Tải lại</button>
                <button id="viewSubmissionsBtn" type="button" class="px-3 py-1.5 text-xs bg-sky-600 text-white rounded font-bold"><i class="fas fa-cloud-arrow-down mr-1"></i>Bài nộp HS</button>
            </div>

            <!-- Compact metadata (always visible, above tabs) -->
            <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-6 gap-3 mb-4">
                <label class="block text-xs font-bold text-slate-700">Môn học
                    <select id="lessonSubject" class="mt-0.5 w-full p-2 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-teal-500 outline-none">
                        ${SUBJECTS.map(item => `<option value="${item.title}">${item.label}</option>`).join('')}
                    </select>
                </label>
                <label class="block text-xs font-bold text-slate-700">Chương
                    <div class="flex gap-2">
                        <input id="lessonChapter" list="lessonChapterOptions" class="flex-1 p-2 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Chương 1: ...">
                        <button id="renameChapterBtn" type="button" class="text-[10px] px-2 border border-teal-200 text-teal-700 rounded hover:bg-teal-50">Đổi tên</button>
                    </div>
                    <datalist id="lessonChapterOptions"></datalist>
                </label>
                <label class="block text-xs font-bold text-slate-700">Tên bài
                    <input id="lessonTitleInput" class="mt-0.5 w-full p-2 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Bài 1: ...">
                </label>
                <label class="block text-xs font-bold text-slate-700">Slug
                    <input id="lessonSlug" class="mt-0.5 w-full p-2 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-teal-500 outline-none" placeholder="math6-c1-b1-xxx">
                </label>
                <div class="grid grid-cols-2 gap-2">
                    <label class="block text-xs font-bold text-slate-700">Thứ tự
                        <input id="lessonOrder" type="number" class="mt-0.5 w-full p-2 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-teal-500 outline-none" value="1">
                    </label>
                    <label class="block text-xs font-bold text-slate-700 mt-0.5">Công khai
                        <div class="mt-1">
                            <input id="lessonPublished" type="checkbox" class="w-4 h-4 text-teal-600 rounded">
                            <span class="ml-1 text-xs text-slate-600">Mở cho HS</span>
                        </div>
                    </label>
                </div>
                <div class="text-[11px] text-slate-500 self-end pb-1 hidden xl:block">Dùng tab bên dưới để soạn nội dung linh hoạt. Dán ảnh khi cần.</div>
            </div>

            <!-- Tab navigation -->
            <div class="flex border-b border-slate-200 mb-3 overflow-x-auto" id="lessonTabs">
                <button data-tab="lythuyet" class="lesson-tab px-5 py-2 font-bold text-sm border-b-2 border-teal-600 text-teal-700 active whitespace-nowrap">Lý thuyết</button>
                <button data-tab="vidu" class="lesson-tab px-5 py-2 font-bold text-sm text-slate-600 hover:text-slate-800 whitespace-nowrap">Ví dụ</button>
                <button data-tab="baitap" class="lesson-tab px-5 py-2 font-bold text-sm text-slate-600 hover:text-slate-800 whitespace-nowrap">Bài tập tương tác</button>
                <button data-tab="tracnghiem" class="lesson-tab px-5 py-2 font-bold text-sm text-slate-600 hover:text-slate-800 whitespace-nowrap">Trắc nghiệm</button>
                <button data-tab="khac" class="lesson-tab px-5 py-2 font-bold text-sm text-slate-600 hover:text-slate-800 whitespace-nowrap">Khác</button>
            </div>

            <!-- Tab contents: clean, no duplication. One editor set only. -->
            <div id="tab-lythuyet" class="lesson-tab-content">
                <label class="block text-sm font-bold text-slate-700 mb-1">Mục tiêu bài học
                    <textarea id="lessonGoalInput" rows="2" class="w-full p-2 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none text-sm" placeholder="Sau bài này học sinh cần nắm được..."></textarea>
                </label>
                <label class="block text-sm font-bold text-slate-700">Lý thuyết
                    <span class="block text-[11px] text-slate-500 mb-1">Dùng Enter 2 lần tách đoạn. <strong>Dán ảnh (Ctrl+V) tự nén rồi upload Drive</strong> hoặc dùng nút ảnh. Công thức $...$.</span>
                    ${richToolbarHtml('lessonTheory')}
                    <textarea id="lessonTheory" rows="11" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                </label>
            </div>

            <div id="tab-vidu" class="lesson-tab-content hidden">
                <label class="block text-sm font-bold text-slate-700">Ví dụ / Dạng toán (dán hình minh họa khi cần)
                    <span class="block text-[11px] text-slate-500 mb-1">Mỗi dạng theo khung: <strong>DẠNG 1: Tên dạng → PHƯƠNG PHÁP GIẢI → Bài 1/Lời giải → Bài 2/Lời giải</strong> (có thể thêm Bài 3). Nên có ít nhất một <strong>DẠNG TOÁN THỰC TẾ</strong>. Dán ảnh vào đúng vị trí nếu cần.</span>
                    ${richToolbarHtml('lessonExamples')}
                    <textarea id="lessonExamples" rows="12" class="w-full p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                </label>
            </div>

            <div id="tab-baitap" class="lesson-tab-content hidden">
                <label class="block text-sm font-bold text-slate-700">Bài tập nộp giáo viên (rich text)
                    <span class="block text-[11px] text-slate-500 mb-1">Học sinh làm xong các dạng rồi nộp chung. Dán hình cho từng dạng nếu cần.</span>
                    ${richToolbarHtml('lessonSelfPractice')}
                    <textarea id="lessonSelfPractice" rows="5" class="w-full p-2 border border-slate-300 rounded focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                </label>

                <div class="mt-4 flex flex-wrap items-center justify-between gap-2">
                    <span class="text-sm font-bold text-slate-700">Bài tập tương tác</span>
                    <div class="inline-flex rounded-lg border border-slate-300 overflow-hidden text-xs shadow-sm" role="group" aria-label="Chế độ soạn bài tập tương tác">
                        <button type="button" id="interactiveModeBulk" class="px-3 py-1.5 font-bold bg-teal-600 text-white">Hàng loạt</button>
                        <button type="button" id="interactiveModeItems" class="px-3 py-1.5 font-bold bg-white text-slate-600">Từng câu</button>
                    </div>
                </div>
                <p id="interactiveModeHint" class="text-[11px] text-slate-500 mb-2">Dán khối BÀI TẬP TƯƠNG TÁC từ Gemini. Chuyển sang Từng câu để chỉnh chi tiết hoặc dán ảnh vào đề.</p>

                <div id="interactiveBulkPanel" class="rounded-lg border border-amber-200 bg-amber-50 p-3">
                    <p class="text-[11px] text-amber-800 mb-2">Dán nguyên khối từ soanbaigemini/Gemini. Cần heading <strong>NỐI Ô</strong> và <strong>SẮP XẾP THỨ TỰ</strong> riêng. Điền khuyết: <code>Đề có ___ | mảnh » ... | đáp án » từng ô | gợi ý</code> (4 cột).</p>
                    <textarea id="interactiveBulkPaste" rows="10" class="w-full p-2 border border-amber-300 rounded text-xs font-mono focus:ring-2 focus:ring-amber-500 outline-none" placeholder="**BÀI TẬP TỰ LUẬN NGẮN**&#10;Đề 1 | Đáp án | Gợi ý&#10;**KÉO THẢ VÀO Ô TRỐNG**&#10;Số ___ gồm ___ | 4 » 8 » đơn vị | 4 » 8 » đơn vị | Gợi ý&#10;**SẮP XẾP THỨ TỰ**&#10;Đề | 3 » 1 » 2 | 1 » 2 » 3 | Gợi ý&#10;**NỐI Ô**&#10;Đề | Trái1 » Trái2 | Phải1 » Phải2 | 0-0,1-1 | Gợi ý"></textarea>
                </div>

                <div id="interactiveItemsPanel" class="hidden mt-2 space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <span class="text-sm font-bold text-slate-700">Bài tập tự luận</span>
                            <button type="button" id="addEssayBtn" class="text-xs px-2 py-0.5 bg-teal-600 text-white rounded">+ Thêm bài</button>
                        </div>
                        <div id="essayItems" class="space-y-2"></div>
                        <textarea id="lessonEssay" class="hidden"></textarea>
                    </div>
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <span class="text-sm font-bold text-slate-700">Kéo thả vào ô trống</span>
                            <button type="button" id="addFillBtn" class="text-xs px-2 py-0.5 bg-teal-600 text-white rounded">+ Thêm</button>
                        </div>
                        <div id="fillItems" class="space-y-2"></div>
                        <textarea id="lessonFill" class="hidden"></textarea>
                    </div>
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <span class="text-sm font-bold text-slate-700">Nối ô / sắp xếp</span>
                            <button type="button" id="addDragBtn" class="text-xs px-2 py-0.5 bg-teal-600 text-white rounded">+ Thêm</button>
                        </div>
                        <div id="dragItems" class="space-y-2"></div>
                        <textarea id="lessonDrag" class="hidden"></textarea>
                    </div>
                </div>

                <!-- Submissions inside Bài tập tab for visual grouping -->
                <section id="selfPracticeSubmissionsPanel" class="mt-4 rounded border border-sky-200 bg-sky-50 p-3 text-xs">
                    <div class="flex items-center justify-between">
                        <div class="font-bold text-sky-900"><i class="fas fa-folder-open mr-1"></i>Bài nộp học sinh (Drive)</div>
                        <button type="button" id="reloadSelfPracticeSubmissionsBtn" class="px-2 py-0.5 border border-sky-300 bg-white rounded text-sky-700">Tải</button>
                    </div>
                    <div id="selfPracticeSubmissionsBody" class="mt-2 text-sky-800">Chọn bài để xem bài nộp của học sinh.</div>
                </section>
            </div>

            <div id="tab-tracnghiem" class="lesson-tab-content hidden">
                <div class="flex flex-wrap items-center justify-between gap-2 mb-1">
                    <span class="text-sm font-bold text-slate-700">Trắc nghiệm</span>
                    <div class="inline-flex rounded-lg border border-slate-300 overflow-hidden text-xs shadow-sm" role="group" aria-label="Chế độ soạn trắc nghiệm">
                        <button type="button" id="questionsModeBulk" class="px-3 py-1.5 font-bold bg-teal-600 text-white">Hàng loạt</button>
                        <button type="button" id="questionsModeItems" class="px-3 py-1.5 font-bold bg-white text-slate-600">Từng câu</button>
                    </div>
                </div>
                <p id="questionsModeHint" class="text-[11px] text-slate-500 mb-2">Dán các dòng trắc nghiệm từ Gemini. Chuyển sang Từng câu để chỉnh hoặc dán ảnh vào câu hỏi.</p>

                <div id="questionsBulkPanel" class="mb-3 rounded-lg border border-amber-200 bg-amber-50 p-3">
                    <p class="text-[11px] text-amber-800 mb-2">Mỗi dòng: <code>Câu? | A | B | C | D | B</code> hoặc <code>Câu 1 | ... | A | B | C | D | B</code>. Có thể dán cả khối <strong>TRẮC NGHIỆM</strong> từ Gemini.</p>
                    <textarea id="questionsBulkPaste" rows="8" class="w-full p-2 border border-amber-300 rounded text-xs font-mono focus:ring-2 focus:ring-amber-500 outline-none"></textarea>
                </div>

                <div id="questionsItemsPanel" class="hidden">
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-sm font-bold text-slate-700">Danh sách câu hỏi</span>
                        <button type="button" id="addQuestionBtn" class="text-xs px-2 py-0.5 bg-teal-600 text-white rounded">+ Thêm câu</button>
                    </div>
                    <div id="questionItems" class="space-y-2"></div>
                </div>
                <textarea id="lessonQuestions" class="hidden"></textarea>
            </div>

            <div id="tab-khac" class="lesson-tab-content hidden">
                <div class="mb-4 rounded-lg border border-violet-200 bg-violet-50 p-3">
                    <div class="text-sm font-bold text-violet-900 mb-1"><i class="fas fa-file-import mr-1"></i> Nhập khối từ Gemini / Soạn bài Gemini</div>
                    <p class="text-[11px] text-violet-800 mb-2">Ưu tiên <strong>Đường A</strong>: dán <strong>toàn bộ</strong> bài Gemini → Import text hoặc Import JSON <code>lesson-import-v1</code>. Sau đó dán ảnh thật thay <code>HINH_xx</code> rồi <strong>Lưu bài</strong> (không tự lưu).</p>
                    <textarea id="geminiImportRaw" rows="5" class="w-full p-2 border border-violet-300 rounded text-xs font-mono focus:ring-2 focus:ring-violet-500 outline-none" placeholder="Dán nguyên khối MỤC TIÊU, LÝ THUYẾT, NỐI Ô, TRẮC NGHIỆM, KỸ NĂNG..."></textarea>
                    <div class="mt-2 flex flex-wrap gap-2">
                        <button id="geminiImportBtn" type="button" class="rounded bg-violet-700 px-4 py-2 text-xs font-bold text-white hover:bg-violet-800">
                            <i class="fas fa-wand-magic-sparkles mr-1"></i> Import text Gemini
                        </button>
                        <label class="rounded bg-indigo-600 px-4 py-2 text-xs font-bold text-white hover:bg-indigo-700 cursor-pointer">
                            <i class="fas fa-file-code mr-1"></i> Import JSON
                            <input id="lessonJsonImportInput" type="file" accept=".json,application/json" class="hidden">
                        </label>
                        <button id="lessonJsonExportBtn" type="button" class="rounded bg-slate-700 px-4 py-2 text-xs font-bold text-white hover:bg-slate-800">
                            <i class="fas fa-download mr-1"></i> Export JSON
                        </button>
                        <button id="lessonStudentPreviewBtn" type="button" class="rounded bg-teal-700 px-4 py-2 text-xs font-bold text-white hover:bg-teal-800">
                            <i class="fas fa-eye mr-1"></i> Xem thử
                        </button>
                    </div>
                </div>
                <label class="block text-sm font-bold text-slate-700 mb-3">Manifest ảnh (từ DANH SÁCH HÌNH Gemini)
                    <span class="block text-[11px] text-slate-500 font-normal">Tự điền khi import. Dùng để kiểm tra marker HINH_xx trước khi công khai.</span>
                    <textarea id="lessonImageManifest" rows="3" class="w-full p-2 border border-slate-300 rounded text-xs font-mono focus:ring-2 focus:ring-teal-500 outline-none" placeholder="HINH_01: LOẠI: SƠ_ĐỒ | Mô tả..."></textarea>
                </label>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-3">
                    <label class="block text-sm font-bold text-slate-700">Kỹ năng cần đạt
                        <span class="block text-[11px] text-slate-500">Mỗi dòng: <code>id_khong_dau | Tên kỹ năng | 80</code> — không cần gõ chữ "id:" hay "Tên:"</span>
                        <textarea id="lessonSkills" rows="5" class="w-full p-2 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-teal-500 outline-none" placeholder="cac-so-den-100000 | Nhận biết, đọc viết và so sánh các số đến 100 000 | 80"></textarea>
                        <span id="lessonSkillsHint" class="mt-1 block text-[11px] text-slate-500"></span>
                    </label>
                    <label class="block text-sm font-bold text-slate-700">Nhiệm vụ học sinh
                        <span class="block text-[11px] text-slate-500">Mỗi dòng = 1 việc cần làm</span>
                        <textarea id="lessonTasks" rows="5" class="w-full p-2 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-teal-500 outline-none"></textarea>
                    </label>
                </div>
                <label class="block text-sm font-bold text-slate-700 mt-3">Video YouTube
                    <span class="block text-[11px] text-slate-500">Tiêu đề | https://youtube...</span>
                    <textarea id="lessonVideos" rows="3" class="w-full p-2 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-teal-500 outline-none" placeholder="Bài 1 | https://..."></textarea>
                </label>
                <div class="mt-3 rounded border border-teal-100 bg-teal-50 p-2 text-[11px] text-teal-800">
                    Mẹo: <strong>Dán ảnh (Ctrl+V)</strong> sẽ tự nén (1200px, ~480KB) rồi upload Google Drive & chèn link. Hoặc nhấn nút ảnh chọn file từ máy.
                </div>
            </div>

            <div id="lessonPreview" class="mt-3 rounded border border-slate-200 bg-slate-50 p-2 text-xs text-slate-600"></div>

            <div class="mt-3 flex flex-wrap gap-3">
                <button id="saveLessonBtn" class="bg-teal-600 hover:bg-teal-700 text-white px-5 py-2 rounded font-bold text-sm flex items-center gap-2">
                    <i class="fas fa-save"></i> Lưu bài học
                </button>
                <button id="seedLessonBtn" type="button" class="bg-slate-100 hover:bg-slate-200 px-4 py-2 rounded font-bold text-sm">
                    Điền mẫu
                </button>
                <span class="self-center text-xs text-slate-500">Ảnh và nội dung linh hoạt theo ý bạn — chèn hay không là do bạn quyết định khi soạn từng mục.</span>
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
        el('geminiImportBtn')?.addEventListener('click', () => importGeminiLessonRaw(el('geminiImportRaw')?.value || ''));
        el('lessonJsonImportInput')?.addEventListener('change', event => {
            const file = event.target.files?.[0];
            if (file) importLessonJsonFile(file);
            event.target.value = '';
        });
        el('lessonJsonExportBtn')?.addEventListener('click', exportLessonJson);
        el('lessonStudentPreviewBtn')?.addEventListener('click', openStudentPreview);

        // Attach add buttons (no inline onclick because functions are in IIFE scope)
        const addEssay = el('addEssayBtn'); if (addEssay) addEssay.onclick = addEssayItem;
        const addFill = el('addFillBtn'); if (addFill) addFill.onclick = addFillItem;
        const addDrag = el('addDragBtn'); if (addDrag) addDrag.onclick = addDragItem;
        const addQ = el('addQuestionBtn'); if (addQ) addQ.onclick = addQuestionItem;
        const interactiveModeBulk = el('interactiveModeBulk'); if (interactiveModeBulk) interactiveModeBulk.onclick = () => setInteractiveEditorMode('bulk');
        const interactiveModeItems = el('interactiveModeItems'); if (interactiveModeItems) interactiveModeItems.onclick = () => setInteractiveEditorMode('items');
        const questionsModeBulk = el('questionsModeBulk'); if (questionsModeBulk) questionsModeBulk.onclick = () => setQuestionsEditorMode('bulk');
        const questionsModeItems = el('questionsModeItems'); if (questionsModeItems) questionsModeItems.onclick = () => setQuestionsEditorMode('items');
        el('interactiveBulkPaste')?.addEventListener('input', () => {
            syncItemsFromInteractiveBulk();
            scheduleRenderPreview();
        });
        el('questionsBulkPaste')?.addEventListener('input', () => {
            syncItemsFromQuestionsBulk();
            scheduleRenderPreview();
        });

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
            // Activate the Bài tập tab so the submissions panel inside is visible
            const baitapBtn = panel.querySelector('button[data-tab="baitap"]');
            if (baitapBtn) baitapBtn.click();
            setTimeout(() => {
                el('selfPracticeSubmissionsPanel')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                loadSelfPracticeSubmissions();
            }, 80);
        });
        setupEditorFieldShortcuts();
        setupRichToolbars();
        setupImagePasteHandlers();
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
        setupDynamicImagePaste();
        setInteractiveEditorMode('bulk', { skipSync: true });
        setQuestionsEditorMode('bulk', { skipSync: true });

        // Tab switching for visual design
        const tabButtons = panel.querySelectorAll('.lesson-tab');
        const tabContents = panel.querySelectorAll('.lesson-tab-content');
        tabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const target = btn.dataset.tab;
                tabButtons.forEach(b => b.classList.remove('active', 'border-b-2', 'border-teal-600', 'text-teal-700'));
                tabButtons.forEach(b => b.classList.add('text-slate-600'));
                btn.classList.add('active', 'border-b-2', 'border-teal-600', 'text-teal-700');
                btn.classList.remove('text-slate-600');

                tabContents.forEach(c => c.classList.add('hidden'));
                const activeContent = panel.querySelector(`#tab-${target}`);
                if (activeContent) activeContent.classList.remove('hidden');
            });
        });

        // Show first tab by default
        if (tabButtons.length) tabButtons[0].click();

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
            .lesson-rich-toolbar { display: flex; flex-wrap: wrap; gap: 4px; margin: 4px 0; }
            .lesson-rich-toolbar button {
                display: inline-flex; align-items: center; gap: 3px;
                padding: 2px 8px; border: 1px solid #cbd5e1; border-radius: 5px;
                background: #fff; color: #334155; font-size: 0.7rem; font-weight: 700; cursor: pointer;
            }
            .lesson-rich-toolbar button:hover { background: #f1f5f9; border-color: #94a3b8; }

            .lesson-tab.active { border-bottom: 3px solid #0f766e; color: #0f766e; font-weight: 700; }
            .lesson-tab-content { display: block; }
            .lesson-tab-content.hidden { display: none; }
            .lesson-tab { transition: all 0.1s; padding-bottom: 6px; margin-right: 6px; }
            .lesson-tab:hover { color: #0f766e; }

            .lesson-tab-content textarea { min-height: 160px; font-size: 0.95rem; line-height: 1.45; }
            #lessonTheory, #lessonExamples { min-height: 240px; }
            .lesson-rich-toolbar { background: #f8fafc; border-radius: 4px; padding: 2px; }
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
        const theoryText = formatTheoryBlocks(lesson.theory);
        const examplesText = formatExamples(lesson.examples);
        const selfPracticeText = formatExamples(lesson.self_practice || []);
        const theoryCleanup = cleanupStaleLessonImagePlaceholders(theoryText);
        const examplesCleanup = cleanupStaleLessonImagePlaceholders(examplesText);
        const selfPracticeCleanup = cleanupStaleLessonImagePlaceholders(selfPracticeText);
        const removedPlaceholders = theoryCleanup.removed + examplesCleanup.removed + selfPracticeCleanup.removed;
        el('lessonTheory').value = theoryCleanup.text;
        el('lessonExamples').value = examplesCleanup.text;
        if (el('lessonSelfPractice')) el('lessonSelfPractice').value = selfPracticeCleanup.text;
        if (removedPlaceholders > 0) {
            showLessonImageUploadStatus(`Đã gỡ ${removedPlaceholders} ảnh chưa tải xong. Vui lòng dán lại ảnh rồi lưu bài.`, 'error');
        }
        el('lessonEssay').value = formatEssayExercises(lesson.essay_exercises);
        el('lessonFill').value = formatFillExercises(lesson.fill_exercises);
        el('lessonDrag').value = formatDragExercises(lesson.drag_exercises);
        el('lessonVideos').value = formatVideos(lesson.videos);
        el('lessonSkills').value = formatSkills(lesson.skills);
        el('lessonTasks').value = Array.isArray(lesson.tasks) ? lesson.tasks.join('\n') : '';
        el('lessonQuestions').value = formatQuestions(lesson.questions);
        if (el('lessonImageManifest')) {
            el('lessonImageManifest').value = formatImageManifestText(lesson);
        }

        // populate dynamic items for flexible UI
        essayItems = parseEssayToItems(el('lessonEssay').value || '');
        fillItems = parseFillToItems(el('lessonFill').value || '');
        dragItems = parseDragToItems(el('lessonDrag').value || '');
        questionItems = parseQuestionToItems(el('lessonQuestions').value || '');
        ['lessonTheory', 'lessonExamples', 'lessonSelfPractice'].forEach(id => {
            const field = el(id);
            if (field) renderLessonFieldImagePreview(field);
        });
        renderEssayItems();
        renderFillItems();
        renderDragItems();
        renderQuestionItems();
        refreshInteractiveBulkTextarea();
        refreshQuestionsBulkTextarea();
        setInteractiveEditorMode('items', { skipSync: true });
        setQuestionsEditorMode('items', { skipSync: true });

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
        refreshInteractiveBulkTextarea();
        refreshQuestionsBulkTextarea();
        setInteractiveEditorMode('items', { skipSync: true });
        setQuestionsEditorMode('items', { skipSync: true });
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
        if (el('interactiveBulkPaste')) el('interactiveBulkPaste').value = '';
        if (el('questionsBulkPaste')) el('questionsBulkPaste').value = '';
        if (el('lessonImageManifest')) el('lessonImageManifest').value = '';
        renderEssayItems();
        renderFillItems();
        renderDragItems();
        renderQuestionItems();
        setInteractiveEditorMode('bulk', { skipSync: true });
        setQuestionsEditorMode('bulk', { skipSync: true });
        renderPreview();
    }

    function suggestSlug() {
        if (el('lessonSlug').value.trim()) return;
        el('lessonSlug').value = LI.suggestSlugFromMeta({
            subject: isPageScopedEditor() ? PAGE_SUBJECT : el('lessonSubject').value,
            chapter: el('lessonChapter').value,
            title: el('lessonTitleInput').value
        });
    }

    function renderSkillsHint() {
        const hint = el('lessonSkillsHint');
        if (!hint) return;
        const skills = parseSkills(el('lessonSkills')?.value || '');
        if (!skills.length) {
            hint.innerHTML = '<span class="text-amber-700"><i class="fas fa-triangle-exclamation mr-1"></i>Chưa nhận kỹ năng nào. Mỗi dòng cần ít nhất id và tên, cách nhau bởi dấu <code>|</code>.</span>';
            return;
        }
        hint.innerHTML = `<span class="text-teal-700"><i class="fas fa-circle-check mr-1"></i>Đã nhận ${skills.length} kỹ năng: ${skills.map(skill => escapeHtml(skill.name || skill.id)).join(' · ')}</span>`;
    }

    function renderPreview() {
        const preview = el('lessonPreview');
        if (!preview) return;
        let questionCount = 0;
        const skills = parseSkills(el('lessonSkills').value);
        try { questionCount = resolveQuestionsForSave(skills).length; } catch { questionCount = 0; }
        const essayCount = parseEssayExercises(el('lessonEssay').value).length;
        const fillCount = parseFillExercises(el('lessonFill').value).length;
        const dragParsed = buildDragExercisesFromItems(dragItems);
        const dragMatchCount = dragParsed.filter(item => item.mode === 'match').length;
        const dragSortCount = dragParsed.filter(item => item.mode !== 'match').length;
        const videoCount = parseVideos(el('lessonVideos')?.value || '').length;
        renderSkillsHint();
        let imageWarn = '';
        if (LI) {
            const textBlob = [
                el('lessonGoalInput')?.value,
                el('lessonTheory')?.value,
                el('lessonExamples')?.value,
                el('lessonSelfPractice')?.value,
                el('lessonEssay')?.value,
                el('lessonFill')?.value,
                el('lessonDrag')?.value,
                el('lessonQuestions')?.value
            ].join('\n');
            const markers = LI.extractImageMarkers(textBlob);
            const manifestIds = new Set(LI.parseImageManifest(el('lessonImageManifest')?.value || '').map(m => m.id));
            const missing = markers.filter(id => !manifestIds.has(id));
            if (missing.length) {
                imageWarn = `<div class="mt-2 rounded border border-amber-200 bg-amber-50 px-2 py-1 text-amber-900"><i class="fas fa-image mr-1"></i>Ảnh chưa có manifest: ${missing.map(escapeHtml).join(', ')}</div>`;
            }
        }
        preview.innerHTML = `
            <div class="grid grid-cols-2 md:grid-cols-6 gap-2 text-center">
                <div><div class="text-[10px] text-slate-500">Lý thuyết</div><div class="font-bold">${(() => { const blocks = parseTheoryBlocks(el('lessonTheory').value); return `${blocks.length} đoạn`; })()}</div></div>
                <div><div class="text-[10px] text-slate-500">Ví dụ</div><div class="font-bold">${parseExamples(el('lessonExamples').value).length}</div></div>
                <div><div class="text-[10px] text-slate-500">Bài tập nộp</div><div class="font-bold">${parseExamples(el('lessonSelfPractice')?.value || '').length} dạng</div></div>
                <div><div class="text-[10px] text-slate-500">Tương tác</div><div class="font-bold">${essayCount + fillCount + dragParsed.length}<div class="text-[9px] font-normal text-slate-500">TL ${essayCount} · ĐK ${fillCount} · Nối ${dragMatchCount} · SX ${dragSortCount}</div></div></div>
                <div><div class="text-[10px] text-slate-500">Trắc nghiệm</div><div class="font-bold ${questionCount ? 'text-teal-700' : 'text-amber-700'}">${questionCount}</div></div>
                <div><div class="text-[10px] text-slate-500">Kỹ năng / Video</div><div class="font-bold ${skills.length ? 'text-teal-700' : 'text-amber-700'}">${skills.length}<div class="text-[9px] font-normal text-slate-500">${videoCount} video</div></div></div>
            </div>
            ${imageWarn}
        `;
    }

    async function saveLesson(event) {
        event.preventDefault();
        if (lessonPendingImageUploads > 0) {
            alert('Đang tải ảnh lên Google Drive. Vui lòng đợi thông báo "Đã tải ảnh" rồi mới lưu bài.');
            return;
        }
        suggestSlug();
        flushBulkEditorsBeforeSave();
        const editorValues = [
            el('lessonTheory')?.value || '',
            el('lessonExamples')?.value || '',
            el('lessonSelfPractice')?.value || '',
            el('lessonEssay')?.value || '',
            el('lessonFill')?.value || '',
            el('lessonDrag')?.value || '',
            el('lessonQuestions')?.value || ''
        ];
        if (lessonEditorTextHasPendingImages(...editorValues)) {
            alert('Còn ảnh chưa tải xong trong nội dung. Đợi upload hoàn tất hoặc xóa dòng "Đang tải ảnh" trước khi lưu.');
            return;
        }
        const skills = parseSkills(el('lessonSkills').value);
        const savedDrag = resolveDragForSave();
        const dragCount = savedDrag.length;
        const dragMatchCount = savedDrag.filter(item => item.mode === 'match').length;
        const dragSortCount = savedDrag.filter(item => item.mode !== 'match').length;
        let savedQuestions = [];
        try {
            savedQuestions = resolveQuestionsForSave(skills);
        } catch (err) {
            alert(err.message || 'Trắc nghiệm chưa đúng format. Kiểm tra tab Trắc nghiệm rồi thử lại.');
            return;
        }
        const questionCount = savedQuestions.length;
        const missingParts = [];
        if (!skills.length) missingParts.push('kỹ năng');
        if (!dragCount) missingParts.push('nối ô / sắp xếp');
        if (!questionCount) missingParts.push('trắc nghiệm');
        if (missingParts.length && !confirm(`Bài đang thiếu: ${missingParts.join(', ')}. Học sinh sẽ không thấy các phần này trên lộ trình. Vẫn lưu?`)) {
            return;
        }
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
            drag_exercises: savedDrag,
            videos: parseVideos(el('lessonVideos').value),
            skills,
            tasks: parseLines(el('lessonTasks').value),
            questions: savedQuestions
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
            const saveBits = [];
            if (dragCount) saveBits.push(`Nối ô: ${dragMatchCount}, Sắp xếp: ${dragSortCount}`);
            if (questionCount) saveBits.push(`Trắc nghiệm: ${questionCount} câu`);
            alert(`Đã lưu bài học.${saveBits.length ? ` ${saveBits.join('. ')}.` : ''}`);
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

    // Expose the dynamic item add/remove functions on window.
    // This ensures `onclick="addXXXItem()"` (if any old/cached HTML remains) works,
    // even though the preferred method is direct property assignment from inside the IIFE.
    window.addEssayItem = addEssayItem;
    window.addFillItem = addFillItem;
    window.addDragItem = addDragItem;
    window.addQuestionItem = addQuestionItem;
    window.removeEssayItem = removeEssayItem;
    window.removeFillItem = removeFillItem;
    window.removeDragItem = removeDragItem;
    window.removeQuestionItem = removeQuestionItem;
})();
