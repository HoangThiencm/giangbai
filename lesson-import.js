/**
 * lesson-import.js — parser, normalizer, validator và adapter lesson-import-v1
 * Dùng chung: admin-lesson-manager.js, soanbaigemini.html
 */
(function (global) {
    'use strict';

    const SCHEMA_VERSION = 'lesson-import-v1';
    const PROMPT_VERSION = '2026-06-sync-v1';
    const VALID_SUBJECTS = ['Toán 4', 'Toán 5', 'Toán 6', 'Toán 7', 'Toán 8', 'Toán 9'];
    const SUBJECT_CODES = {
        'Toán 4': 'math4', 'Toán 5': 'math5', 'Toán 6': 'math6',
        'Toán 7': 'math7', 'Toán 8': 'math8', 'Toán 9': 'math9'
    };
    const POOL_ITEM_JOINER = ' » ';
    const POOL_ITEM_SEP_RE = /\s*»\s*/u;
    const BLANK_TOKEN_RE = /_{3,}|\[\.\.\.\]|\[\s*\]|\[(?:\d+(?:[.,]\d+)?)\]/g;
    const FILL_COMMA_LIST_RE = /\s*,\s+|\s+,\s*/;
    const AI_MARKER = '[AI]';
    const AI_MARKER_LINE_RE = /^\s*(\[\[AI\]\]|\[AI\])\s*$/i;
    const AI_MARKER_INLINE_RE = /\s*(\[\[AI\]\]|\[AI\])\s*$/i;
    const IMAGE_MARKER_RE = /!\[[^\]]*\]\((HINH[_\s-]*\d+|HÌNH[_\s-]*\d+)\)/gi;
    const IMAGE_REF_RE = /^(?:HINH|HÌNH|IMAGE)[_\s-]*\d+$/i;

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

    const POOL_LABEL_PREFIX_RE = /^(?:trái|phải|nối|mảnh|phần\s*tử|thứ\s*tự(?:\s*đúng)?|đáp\s*án)\s*[:»›]\s*/iu;
    const PROMPT_PREFIX_RE = /^[-–—*#\s]*(?:đề|bài|câu|question)\s*[:：]\s*/iu;
    const CAU_NUMBER_PREFIX_RE = /^[-–—*#\s]*(?:\*\*)?(?:câu|bài)\s*\d+\s*(?:\*\*)?\s*[:：]\s*/iu;
    const ESSAY_ANSWER_INLINE_RE = /\s*(?:\*\*)?(?:đáp\s*án|answer)\s*(?:\*\*)?\s*[:：]\s*/iu;
    const ESSAY_ANSWER_LINE_RE = /^(?:\*\*)?(?:đáp\s*án|answer)\s*(?:\*\*)?\s*[:：]\s*(.+)$/iu;
    const ESSAY_HINT_LINE_RE = /^(?:\*\*)?(?:gợi\s*ý|hint)\s*(?:\*\*)?\s*[:：]\s*(.+)$/iu;
    const ESSAY_CAU_LINE_RE = /^(?:\*\*)?(?:câu|bài)\s*\d+\s*(?:\*\*)?\s*[:：]\s*(.+)$/iu;
    const HINT_PREFIX_RE = /^(?:gợi\s*ý|hint)\s*[:：]\s*/iu;
    const POOL_LABEL_ONLY_RE = /^(?:trái|phải|nối|mảnh)$/iu;

    function stripPromptPrefix(value) {
        let text = String(value || '').trim();
        for (let i = 0; i < 4; i += 1) {
            const next = text.replace(PROMPT_PREFIX_RE, '').replace(CAU_NUMBER_PREFIX_RE, '').trim();
            if (next === text) break;
            text = next;
        }
        return text.replace(/\*\*/g, '').trim();
    }

    function stripEssayMarkdown(line) {
        let text = String(line || '').trim();
        text = text.replace(/^\s*[-*+]\s+/, '');
        text = text.replace(/^\s*#{1,6}\s+/, '');
        return text.trim();
    }

    function stripEssayAnswerPrefix(value) {
        let text = String(value || '').trim().replace(/^\*\*|\*\*$/g, '').trim();
        text = text.replace(/^(?:đáp\s*án|answer)\s*[:：]\s*/iu, '').trim();
        return text.replace(/\*\*/g, '').trim();
    }

    function splitEssayInlineAnswer(text) {
        const raw = stripEssayMarkdown(text);
        if (!ESSAY_ANSWER_INLINE_RE.test(raw)) return null;
        const parts = raw.split(ESSAY_ANSWER_INLINE_RE);
        if (parts.length < 2) return null;
        const promptPart = stripPromptPrefix(parts[0]);
        let rest = parts.slice(1).join(' ').trim().replace(/^\*\*|\*\*$/g, '').trim();
        let answer = rest;
        let hint = '';
        const hintParts = rest.split(/\s*(?:\*\*)?(?:gợi\s*ý|hint)\s*(?:\*\*)?\s*[:：]\s*/iu);
        if (hintParts.length >= 2) {
            answer = stripEssayAnswerPrefix(hintParts[0]);
            hint = stripHintPrefix(hintParts.slice(1).join(' '));
        } else {
            answer = stripEssayAnswerPrefix(answer);
        }
        return { prompt: promptPart, answer, hint };
    }

    function formatEssayLine(item) {
        const p = stripPromptPrefix(item.prompt || '');
        const a = stripEssayAnswerPrefix(item.answer || '');
        const h = stripHintPrefix(item.hint || '');
        if (!p) return '';
        if (!a && !h) return p;
        if (!h) return `${p} | ${a}`;
        return `${p} | ${a} | ${h}`;
    }

    function preprocessEssaySectionText(text) {
        const lines = String(text || '').replace(/\r/g, '').split('\n').map(line => line.trim()).filter(Boolean);
        const result = [];
        let pending = null;

        const flushPending = () => {
            if (pending && pending.prompt) result.push(formatEssayLine(pending));
            pending = null;
        };

        lines.forEach(rawLine => {
            const stripped = stripEssayMarkdown(rawLine);
            if (!stripped) return;
            if (/BÀI TẬP TỰ LUẬN/.test(normalizeGeminiSectionHeading(rawLine))) return;

            const inline = stripped.includes('|') ? null : splitEssayInlineAnswer(stripped);
            if (inline && inline.prompt) {
                flushPending();
                result.push(formatEssayLine(inline));
                return;
            }

            const answerOnly = stripped.match(ESSAY_ANSWER_LINE_RE);
            const hintOnly = stripped.match(ESSAY_HINT_LINE_RE);
            const cauOnly = stripped.match(ESSAY_CAU_LINE_RE);

            if (answerOnly) {
                if (pending) pending.answer = answerOnly[1].trim();
                else pending = { prompt: '', answer: answerOnly[1].trim(), hint: '' };
                return;
            }
            if (hintOnly) {
                if (pending) {
                    pending.hint = hintOnly[1].trim();
                    flushPending();
                }
                return;
            }
            if (cauOnly) {
                flushPending();
                pending = { prompt: cauOnly[1].trim(), answer: '', hint: '' };
                return;
            }

            if (stripped.includes('|')) {
                flushPending();
                const parts = splitQuestionParts(stripped);
                result.push(formatEssayLine({
                    prompt: parts[0] || '',
                    answer: parts[1] || '',
                    hint: parts[2] || ''
                }));
                return;
            }

            if (pending && !pending.answer) {
                pending.prompt = pending.prompt ? `${pending.prompt} ${stripped}` : stripped;
            } else if (pending && pending.answer && !pending.hint) {
                pending.answer = `${pending.answer} ${stripped}`;
            } else {
                flushPending();
                pending = { prompt: stripped, answer: '', hint: '' };
            }
        });
        flushPending();
        return result.join('\n');
    }

    function canonicalizeEssayExercise(item) {
        if (!item || typeof item !== 'object') return item;
        return {
            ...item,
            prompt: stripPromptPrefix(item.prompt || ''),
            answer: stripEssayAnswerPrefix(item.answer || ''),
            hint: stripHintPrefix(item.hint || '')
        };
    }

    function stripHintPrefix(value) {
        return String(value || '').replace(HINT_PREFIX_RE, '').trim();
    }

    function stripPoolColumnLabel(value) {
        let text = String(value || '').trim();
        for (let i = 0; i < 4; i += 1) {
            const next = text.replace(POOL_LABEL_PREFIX_RE, '').trim();
            if (next === text) break;
            text = next;
        }
        return text;
    }

    function normalizePoolToken(token) {
        return String(token || '').trim().replace(/\s+/g, ' ');
    }

    function normalizePoolPieces(value) {
        const stripped = stripPoolColumnLabel(value);
        if (!stripped) return [];
        if (POOL_ITEM_SEP_RE.test(stripped)) {
            return splitPoolText(stripped).map(normalizePoolToken).filter(Boolean);
        }
        if (/,/.test(stripped)) {
            return stripped.split(/\s*,\s*/).map(normalizePoolToken).filter(Boolean);
        }
        const single = normalizePoolToken(stripped);
        return single ? [single] : [];
    }

    function normalizePoolArray(value) {
        if (Array.isArray(value)) {
            const flat = [];
            value.forEach(item => {
                normalizePoolPieces(item).forEach(piece => flat.push(piece));
            });
            return flat.filter(piece => piece && !POOL_LABEL_ONLY_RE.test(piece));
        }
        return normalizePoolPieces(value).filter(piece => piece && !POOL_LABEL_ONLY_RE.test(piece));
    }

    function extractMatchPairsFromSpec(spec) {
        const pairs = [];
        const source = String(spec || '');
        const re = /(\d+)\s*-\s*(\d+)/g;
        let match;
        while ((match = re.exec(source)) !== null) {
            const left = Number.parseInt(match[1], 10);
            const right = Number.parseInt(match[2], 10);
            if (Number.isFinite(left) && Number.isFinite(right)) {
                pairs.push({ left, right });
            }
        }
        return pairs;
    }

    function formatMatchPairSpec(pairs) {
        return (pairs || []).map(pair => `${pair.left}-${pair.right}`).join(',');
    }

    function normalizeDragLineParts(line) {
        const parts = splitQuestionParts(line);
        if (!parts.length) return parts;
        parts[0] = stripPromptPrefix(parts[0]);
        if (parts.length > 1) parts[1] = stripPoolColumnLabel(parts[1]);
        if (parts.length > 2) parts[2] = stripPoolColumnLabel(parts[2]);
        if (parts.length > 3) {
            const pairs = extractMatchPairsFromSpec(parts[3]);
            if (pairs.length) parts[3] = formatMatchPairSpec(pairs);
            else parts[3] = stripPoolColumnLabel(parts[3]);
        }
        if (parts.length > 4) parts[4] = stripHintPrefix(parts[4]);
        return parts;
    }

    function getInteractiveFormatGuide() {
        return `**QUY TẮC ĐỊNH DẠNG (parser lesson-import-v1 — copy JSON là chạy, không sửa tay):**
- Mỗi câu bài tập = **đúng 1 dòng**, các cột phân tách bằng | (pipe).
- KHÔNG dùng markdown trong các mục pipe: không **Câu 1:**, không **Đáp án:**, không bullet -, không heading ###.
- KHÔNG tách đề và đáp án thành 2 dòng — ghép thành 1 dòng pipe.
- KHÔNG ghi nhãn cột như "Đề:", "Trái »", "Phải »", "Nối »", "gợi ý:" — chỉ nội dung thuần.
- Mảnh trong cùng cột PHẢI nối bằng » (không dùng dấu phẩy , giữa các mảnh).

**BÀI TẬP TỰ LUẬN NGẮN** — 2–5 dòng, đúng 3 cột:
Viết số gồm 4 chục nghìn, 5 nghìn, 6 trăm và 2 đơn vị | 45602 | Đọc từng hàng
SAI: - **Câu 1:** Viết số... (markdown, thiếu đáp án)
SAI: **Câu 1:** ... rồi dòng riêng **Đáp án:** 45602

**KÉO THẢ VÀO Ô TRỐNG** — đúng 2 dòng, 4 cột:
Câu có ___ | mảnh1 » mảnh2 » mảnh_nhiễu | đáp_án1 » đáp_án2 | gợi ý ngắn

**SẮP XẾP THỨ TỰ** — đúng 2 dòng, 4 cột (cột 2 và 3 cùng bộ mảnh, chỉ khác thứ tự):
Sắp xếp từ bé đến lớn | 9 800 » 12 050 » 12 500 » 12 505 | 9 800 » 12 050 » 12 500 » 12 505 | So sánh hàng nghìn trước

**NỐI Ô** — 1–2 dòng, 5 cột (cột 4 chỉ ghi chỉ số nối, không chữ "Nối"):
Nối số với cách đọc | 60 006 » 66 000 | Sáu mươi nghìn không trăm linh sáu » Sáu mươi sáu nghìn | 0-0,1-1 | Đọc kỹ hàng nghìn

**KỸ NĂNG CẦN ĐẠT** (heading riêng, trước TRẮC NGHIỆM) — mỗi dòng 3 cột:
doc_so | Đọc và viết số trong phạm vi 100 000 | 80

**TRẮC NGHIỆM** — 5–10 dòng, đúng 7 cột (cột 1 = skill_id có trong KỸ NĂNG; phân bổ đều, không gán cùng 1 skill cho >80% câu):
doc_so | Số nào lớn nhất? | 45 006 | 45 602 | 45 062 | 46 052 | B

**DANH SÁCH HÌNH ẢNH CẦN TẠO** — mọi HINH_xx dùng trong bài PHẢI khai báo ở cuối:
HINH_01: theory | Sơ đồ bảng hàng | diagram | Mô tả prompt tạo ảnh`;
    }

    function canonicalizeDragExerciseItem(item) {
        if (!item || typeof item !== 'object') return item;
        const copy = { ...item };
        copy.prompt = stripPromptPrefix(copy.prompt || '');
        copy.hint = stripHintPrefix(copy.hint || '');

        const isMatch = copy.mode === 'match'
            || (Array.isArray(copy.left) && Array.isArray(copy.right))
            || /\d+\s*-\s*\d+/.test(String(copy.pair_spec || copy.map || ''));

        if (isMatch) {
            let left = normalizePoolArray(copy.left || copy.items || copy.trai || []);
            let right = normalizePoolArray(copy.right || copy.answer || copy.phai || []);
            let pairs = Array.isArray(copy.pairs) && copy.pairs.length
                ? copy.pairs
                : extractMatchPairsFromSpec(copy.pair_spec || copy.map || copy.pairs_text || '');
            if (!pairs.length) {
                pairs = extractMatchPairsFromSpec(buildDefaultMatchPairSpec(left.length, right.length));
            }
            if (!pairs.length && left.length && right.length) {
                pairs = extractMatchPairsFromSpec(buildDefaultMatchPairSpec(left.length, right.length));
            }
            const pairSpec = formatMatchPairSpec(pairs);
            copy.mode = 'match';
            copy.left = left;
            copy.right = right;
            copy.pairs = pairs;
            copy.pair_spec = pairSpec;
            delete copy.items;
            delete copy.answer;
            return copy;
        }

        copy.mode = 'sort';
        copy.items = normalizePoolArray(copy.items || copy.left || copy.trai || []);
        copy.answer = normalizePoolArray(copy.answer || copy.right || copy.phai || copy.items || []);
        delete copy.left;
        delete copy.right;
        delete copy.pairs;
        delete copy.pair_spec;
        return copy;
    }

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

    function cleanExampleTypeHeading(line) {
        return String(line || '')
            .replace(/^\s*#{1,6}\s*/, '')
            .replace(/^\s*[-+*]\s+/, '')
            .replace(/^\s*\d+[.)]\s+(?=(?:\*\*|__)?DẠNG\b)/i, '')
            .replace(/^\s*(?:\*\*|__)/, '')
            .replace(/(?:\*\*|__)\s*$/, '')
            .trim();
    }

    function isExampleTypeHeading(line) {
        const heading = cleanExampleTypeHeading(line);
        return /^DẠNG\s+(?:\d+|[IVXLCDM]+)\s*(?::|[.\-–—]|$)/i.test(heading)
            || /^DẠNG\s+TOÁN\s+THỰC\s+TẾ\s*(?::|[.\-–—]|$)/i.test(heading)
            || /^DẠNG\s*(?::|[\-–—])/i.test(heading);
    }

    function parseExamplesByTypeHeadings(text) {
        const lines = String(text || '').replace(/\r/g, '').split('\n');
        const headingIndexes = [];
        lines.forEach((line, index) => {
            if (isExampleTypeHeading(line)) headingIndexes.push(index);
        });
        if (!headingIndexes.length) return [];

        const preamble = lines.slice(0, headingIndexes[0]).join('\n').trim();
        return headingIndexes.map((startIndex, groupIndex) => {
            const endIndex = headingIndexes[groupIndex + 1] ?? lines.length;
            const title = cleanExampleTypeHeading(lines[startIndex]) || `DẠNG ${groupIndex + 1}`;
            const bodyParts = lines.slice(startIndex + 1, endIndex);
            if (groupIndex === 0 && preamble) bodyParts.unshift(preamble, '');
            const parsed = parseContentWithAiMarker(bodyParts.join('\n').replace(/\n{3,}/g, '\n\n').trim());
            return { title, body: parsed.text, ai: parsed.ai };
        }).filter(example => example.title || example.body);
    }

    function parseExamples(text) {
        const normalizedText = String(text || '').replace(/\r/g, '');
        const typedExamples = parseExamplesByTypeHeadings(normalizedText);
        if (typedExamples.length) return typedExamples;

        const blocks = normalizedText.split(/\n\s*\n+/).map(block => block.trim()).filter(Boolean);
        const source = blocks.length > 1 || !normalizedText.includes('|') ? blocks : parseLines(normalizedText);
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

    function normalizeSkillField(value, kind) {
        let text = String(value || '').trim();
        if (kind === 'id') text = text.replace(/^id\s*[:：]\s*/i, '').trim();
        else if (kind === 'name') text = text.replace(/^t[eê]n\s*[:：]\s*/i, '').trim();
        else if (kind === 'target') text = text.replace(/^(?:target|muc|mục)\s*[:：]\s*/i, '').trim();
        return text;
    }

    function mergeSkillInputLines(text) {
        const merged = [];
        String(text || '').replace(/\r/g, '').split('\n').forEach(rawLine => {
            const line = rawLine.trim();
            if (!line) return;
            if (/^\d{1,3}$/.test(line) && merged.length && /\|\s*$/.test(merged[merged.length - 1])) {
                merged[merged.length - 1] = `${merged[merged.length - 1].replace(/\|\s*$/, '')} | ${line}`;
                return;
            }
            merged.push(line);
        });
        return merged;
    }

    function parseSkills(text) {
        return mergeSkillInputLines(text).map((line, index) => {
            const parts = line.split('|').map(part => part.trim());
            if (parts.length === 1 && /^\d{1,3}$/.test(parts[0])) return null;
            const idRaw = normalizeSkillField(parts[0], 'id');
            const nameRaw = normalizeSkillField(parts[1], 'name');
            const targetRaw = normalizeSkillField(parts[2], 'target');
            const id = slugify(idRaw || nameRaw || `skill-${index + 1}`);
            const name = nameRaw || idRaw || `Kỹ năng ${index + 1}`;
            const targetNum = Number(targetRaw);
            const target = Number.isFinite(targetNum) && targetNum > 0
                ? Math.min(100, Math.max(1, Math.round(targetNum)))
                : 80;
            if (!id && !name) return null;
            return { id, name, target };
        }).filter(Boolean);
    }

    function parseVideos(text) {
        return parseLines(text).map(line => {
            const trimmed = String(line || '').trim();
            if (/^https?:\/\//i.test(trimmed)) {
                return { title: 'Video bài giảng', url: trimmed };
            }
            const parts = line.includes('||') ? line.split('||') : line.split('|');
            const [title, ...urlParts] = parts;
            const url = urlParts.join('|').trim();
            if (/^https?:\/\//i.test(String(title || '').trim()) && !url) {
                return { title: 'Video bài giảng', url: String(title || '').trim() };
            }
            return { title: (title || 'Video bài giảng').trim(), url };
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

    function normalizeMcqBulkLine(line) {
        let text = String(line || '').trim();
        if (!text) return '';
        text = text.replace(/^\*\*|\*\*$/g, '').trim();
        text = text.replace(/^câu\s*\d+\s*[.:)\-–—]?\s*\|/iu, '').trim();
        text = text.replace(/^\d+\s*[.)]\s*/, '').trim();
        return text;
    }

    function looksLikeSkillId(value) {
        const text = String(value || '').trim();
        return /^[a-z0-9][a-z0-9_-]*$/i.test(text)
            && text.length >= 3
            && !/^câu\s*\d+$/i.test(text)
            && !/^[ABCD]$/i.test(text);
    }

    function parseQuestionLine(line, index, fallbackSkill) {
        const parts = splitQuestionParts(normalizeMcqBulkLine(line));
        if (parts.length < 6) {
            throw new Error(`Câu hỏi số ${index + 1} chưa đúng mẫu: skill_id | Câu hỏi | A | B | C | D | đáp án`);
        }
        const hasSkill = parts.length >= 7 && looksLikeSkillId(parts[0]);
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
        } catch (err) {
            return false;
        }
    }

    function flushQuestionBuffer(buffer, blocks, fallbackSkill) {
        const trimmed = String(buffer || '').trim();
        if (!trimmed) return;
        if (canParseQuestionBlock(trimmed, fallbackSkill)) {
            blocks.push(trimmed);
        }
    }

    function readQuestionBlocks(text, fallbackSkill) {
        const lines = decodePastedText(text).split('\n').map(line => line.trim()).filter(Boolean);
        const blocks = [];
        let buffer = '';
        lines.forEach(line => {
            const normalized = normalizeMcqBulkLine(line);
            if (splitQuestionParts(normalized).length >= 6) {
                flushQuestionBuffer(buffer, blocks, fallbackSkill);
                if (canParseQuestionBlock(normalized, fallbackSkill)) {
                    blocks.push(normalized);
                }
                buffer = '';
                return;
            }
            buffer = buffer ? `${buffer} ${line}` : line;
            if (canParseQuestionBlock(buffer, fallbackSkill)) {
                blocks.push(buffer);
                buffer = '';
            }
        });
        flushQuestionBuffer(buffer, blocks, fallbackSkill);
        return blocks;
    }

    function parseQuestionsReport(text, skills = []) {
        const fallbackSkill = (skills[0] && skills[0].id) || 'tong_hop';
        const questions = [];
        const skipped = [];
        readQuestionBlocks(text, fallbackSkill).forEach((line) => {
            try {
                questions.push(parseQuestionLine(line, questions.length, fallbackSkill));
            } catch (err) {
                skipped.push({ line, message: err.message || 'Không parse được câu trắc nghiệm.' });
            }
        });
        return { questions, skipped };
    }

    function parseQuestions(text, skills = []) {
        return parseQuestionsReport(text, skills).questions;
    }

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

    function countBlankTokens(prompt) {
        const matches = String(prompt || '').match(BLANK_TOKEN_RE);
        return matches?.length || 1;
    }

    function looksLikeFillHintText(value) {
        const text = String(value || '').trim();
        if (!text) return false;
        if (POOL_ITEM_SEP_RE.test(text)) return false;
        if (text.length < 18 && !/[.():]/.test(text)) return false;
        return /xác định|ô trống|gợi ý|hãy|em hãy|điền|tính|phân tích|nhận xét|giải thích/i.test(text);
    }

    function inferFillAnswersFromPool(pool, blankCount) {
        if (!Array.isArray(pool) || !pool.length || blankCount < 1) return [];
        if (pool.length === blankCount) return [...pool];
        if (pool.length > blankCount) return pool.slice(0, blankCount);
        return [...pool];
    }

    function poolsLookLikeSortOrder(leftItems, rightItems) {
        const left = (leftItems || []).map(item => String(item || '').trim()).filter(Boolean);
        const right = (rightItems || []).map(item => String(item || '').trim()).filter(Boolean);
        if (!left.length || !right.length || left.length !== right.length) return false;
        const signature = items => [...items].sort((a, b) => a.localeCompare(b, 'vi')).join('\u0001');
        return signature(left) === signature(right);
    }

    function normalizeFillPromptBlanks(prompt, answers) {
        let text = String(prompt || '').trim();
        if (!text || countBlankTokens(text) > 0 || !answers.length) return text;
        answers.forEach(answer => {
            const token = String(answer || '').trim();
            if (!token || token.length > 24) return;
            const escaped = token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            text = text.replace(new RegExp('\\b' + escaped + '\\b(?!_)'), function(match, offset, source) {
                if (offset > 0 && source.charAt(offset - 1) === '_') return match;
                return '___';
            });
        });
        return text;
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

    function normalizeFillParts(parts) {
        const rawParts = (parts || []).map(part => String(part || '').trim());
        let prompt = rawParts[0] || '';
        let pool = [];
        let answer = '';
        let hint = '';

        if (poolTextHasMultipleItems(rawParts[1])) {
            pool = splitPoolText(rawParts[1]);
            if (rawParts.length >= 4) {
                answer = rawParts[2] || '';
                hint = rawParts[3] || '';
            } else if (rawParts.length === 3) {
                if (looksLikeFillHintText(rawParts[2])) {
                    hint = rawParts[2];
                    answer = joinPoolText(inferFillAnswersFromPool(pool, countBlankTokens(prompt)));
                } else {
                    answer = rawParts[2];
                }
            } else {
                answer = joinPoolText(inferFillAnswersFromPool(pool, countBlankTokens(prompt)));
            }
        } else if (rawParts[1]) {
            answer = rawParts[1];
            pool = [answer];
            hint = rawParts[2] || '';
        }

        let blankCount = countBlankTokens(prompt);
        if (looksLikeFillHintText(answer)) {
            hint = hint || answer;
            answer = joinPoolText(inferFillAnswersFromPool(pool, blankCount));
        }

        let answers = splitFillAnswerList(answer, blankCount);
        if (answers.length === 1 && blankCount > 1) {
            const expanded = splitFillAnswerList(answers[0], blankCount);
            if (expanded.length > 1) answers = expanded;
        }
        if ((!answers.length || looksLikeFillHintText(answers.join(' '))) && pool.length) {
            answers = inferFillAnswersFromPool(pool, blankCount);
            answer = joinPoolText(answers);
        }

        prompt = normalizeFillPromptBlanks(prompt, answers);
        blankCount = countBlankTokens(prompt);
        if (answers.length === 1 && blankCount > 1) {
            const expanded = splitFillAnswerList(answers[0], blankCount);
            if (expanded.length > 1) answers = expanded;
        }

        return { prompt, pool, answers, hint, blankCount };
    }

    function parseFillExercises(text) {
        return parseLines(text).map((line, index) => {
            const normalized = normalizeFillParts(splitQuestionParts(line));
            return {
                id: `fill_${index + 1}`,
                prompt: normalized.prompt,
                items: normalized.pool,
                pool: normalized.pool,
                answer: normalized.answers.length <= 1 ? (normalized.answers[0] || '') : normalized.answers,
                hint: normalized.hint
            };
        }).filter(item => item.prompt && (item.pool.length || item.answer));
    }

    function parseMatchPairs(spec) {
        return extractMatchPairsFromSpec(spec);
    }

    function buildDefaultMatchPairSpec(leftCount, rightCount) {
        const count = Math.min(leftCount, rightCount);
        if (!count) return '';
        return Array.from({ length: count }, (_, index) => `${index}-${index}`).join(',');
    }

    function isDragMatchItem(item) {
        return /\d+\s*-\s*\d+/.test(String(item?.map || item?.pair_spec || ''));
    }

    function buildDragExercisesFromItems(items) {
        return (items || []).map((item, index) => {
            if (isDragMatchItem(item)) {
                const left = repairPoolPieces(splitPoolText(item.trai || item.left), 0);
                const right = repairPoolPieces(splitPoolText(item.phai || item.right), 0);
                const pairSpec = String(item.map || item.pair_spec || '').trim() || buildDefaultMatchPairSpec(left.length, right.length);
                const pairs = parseMatchPairs(pairSpec);
                return {
                    id: `drag_${index + 1}`,
                    mode: 'match',
                    prompt: item.de || item.prompt || '',
                    left,
                    right,
                    pairs,
                    pair_spec: pairSpec,
                    hint: item.goi || item.hint || ''
                };
            }
            const sortItems = repairPoolPieces(splitPoolText(item.trai || item.items), 0);
            const sortAnswer = repairPoolPieces(splitPoolText(item.phai || item.answer), sortItems.length);
            return {
                id: `drag_${index + 1}`,
                mode: 'sort',
                prompt: item.de || item.prompt || '',
                items: sortItems,
                answer: sortAnswer,
                hint: item.goi || item.hint || ''
            };
        }).filter(item => {
            if (item.mode === 'match') return item.prompt && item.left?.length && item.right?.length && item.pairs?.length;
            return item.prompt && item.items?.length && item.answer?.length;
        });
    }

    function parseSingleDragLine(line, index, options = {}) {
        const parts = normalizeDragLineParts(line);
        const prompt = parts[0] || '';
        let pairs = parts.length > 3 ? extractMatchPairsFromSpec(parts[3]) : [];
        let hint = parts[4] || '';

        if (!pairs.length && options.preferMatch && parts.length >= 3) {
            const left = repairPoolPieces(normalizePoolPieces(parts[1]), 0);
            const right = repairPoolPieces(normalizePoolPieces(parts[2]), 0);
            pairs = extractMatchPairsFromSpec(buildDefaultMatchPairSpec(left.length, right.length));
        }

        if (pairs.length && parts.length >= 3) {
            const left = repairPoolPieces(normalizePoolPieces(parts[1]), pairs.length);
            const right = repairPoolPieces(normalizePoolPieces(parts[2]), pairs.length);
            const pairSpec = formatMatchPairSpec(pairs);
            return canonicalizeDragExerciseItem({
                id: `drag_${index + 1}`,
                mode: 'match',
                prompt,
                left,
                right,
                pairs,
                pair_spec: pairSpec,
                hint
            });
        }

        const items = normalizePoolPieces(parts[1]);
        const answer = normalizePoolPieces(parts[2] || parts[1]);
        if (!hint && parts[3] && !extractMatchPairsFromSpec(parts[3]).length) {
            hint = stripHintPrefix(parts[3]);
        }
        return canonicalizeDragExerciseItem({
            id: `drag_${index + 1}`,
            mode: 'sort',
            prompt,
            items,
            answer,
            hint
        });
    }

    function parseDragExercises(text, options = {}) {
        return parseLines(text)
            .map((line, index) => parseSingleDragLine(line, index, options))
            .filter(item => {
                if (item.mode === 'match') return item.prompt && item.left?.length && item.right?.length && item.pairs?.length;
                return item.prompt && item.items?.length && item.answer?.length;
            });
    }

    function parseEssayExercises(text) {
        const preprocessed = preprocessEssaySectionText(text);
        return parseLines(preprocessed).map((line, index) => {
            const parts = splitQuestionParts(line);
            return canonicalizeEssayExercise({
                id: `essay_${index + 1}`,
                prompt: parts[0] || '',
                answer: parts[1] || '',
                hint: parts[2] || ''
            });
        }).filter(item => item.prompt);
    }

    function normalizeBulkHeading(line) {
        return String(line || '')
            .replace(/^\s*#{1,6}\s*/, '')
            .replace(/^\s*\d+[.)]\s*/, '')
            .replace(/^\s*\*\*|\*\*\s*$/g, '')
            .trim()
            .toUpperCase();
    }

    function resolveInteractiveBulkSection(line) {
        const trimmed = String(line || '').trim();
        if (trimmed.includes('|')) return '';
        const heading = normalizeBulkHeading(line);
        if (!heading) return '';
        if (/^BÀI TẬP TƯƠNG TÁC/.test(heading)) return 'skip';
        if (/BÀI TẬP TỰ LUẬN/.test(heading)) return 'essay';
        if (/KÉO THẢ|KÉO VÀO Ô|KÉO VÀO TRỐNG/.test(heading)) return 'fill';
        if (/NỐI Ô/.test(heading) && /SẮP XẾP/.test(heading)) return 'dragMixed';
        if (/NỐI Ô|^NỐI\s/.test(heading)) return 'dragMatch';
        if (/SẮP XẾP/.test(heading)) return 'dragSort';
        if (/^TRẮC NGHIỆM|^KỸ NĂNG|^NHIỆM VỤ|^DANH SÁCH HÌNH|^PROMPT TẠO/.test(heading)) return 'stop';
        return '';
    }

    function isInteractivePipeLine(line) {
        const text = String(line || '').trim();
        if (!text || !text.includes('|')) return false;
        if (/^\*\*.+\*\*$/.test(text)) return false;
        return !resolveInteractiveBulkSection(text);
    }

    function classifyInteractivePipeLine(line) {
        const parts = splitQuestionParts(line);
        if (parts.length >= 4 && /\d+\s*-\s*\d+/.test(parts[3] || '')) return 'dragMatch';
        if (parts.length >= 4) {
            const leftMulti = poolTextHasMultipleItems(parts[1]);
            const rightMulti = poolTextHasMultipleItems(parts[2]);
            if (leftMulti && rightMulti) {
                return poolsLookLikeSortOrder(splitPoolText(parts[1]), splitPoolText(parts[2])) ? 'dragSort' : 'dragMatch';
            }
            if (leftMulti || /___|…/.test(parts[0] || '')) return 'fill';
        }
        return 'essay';
    }

    function pushInteractiveDragLine(buckets, line) {
        const kind = classifyInteractivePipeLine(line);
        if (kind === 'dragMatch') buckets.dragMatch.push(line);
        else if (kind === 'dragSort') buckets.dragSort.push(line);
        else buckets.drag.push(line);
    }

    function isEssayBulkLine(line, section) {
        if (section !== 'essay') return false;
        const text = String(line || '').trim();
        if (!text || resolveInteractiveBulkSection(text)) return false;
        if (text.includes('|')) return true;
        return /(?:câu|bài)\s*\d+|đáp\s*án|gợi\s*ý|^\s*[-*+]\s+/iu.test(text);
    }

    function pushInteractiveBulkLines(buckets, section, lines) {
        if (section === 'essay') {
            const preprocessed = preprocessEssaySectionText(lines.join('\n'));
            if (preprocessed) buckets.essay.push(preprocessed);
            return;
        }
        const pipeLines = lines.filter(isInteractivePipeLine);
        if (!pipeLines.length) return;
        if (section === 'dragMatch') { buckets.dragMatch.push(...pipeLines); return; }
        if (section === 'dragSort') { buckets.dragSort.push(...pipeLines); return; }
        if (section === 'dragMixed') {
            pipeLines.forEach(line => {
                const kind = classifyInteractivePipeLine(line);
                if (kind === 'dragMatch' || kind === 'dragSort') buckets[kind].push(line);
                else if (kind === 'drag') pushInteractiveDragLine(buckets, line);
                else buckets[kind].push(line);
            });
            return;
        }
        if (section === 'fill' || section === 'drag') {
            buckets[section].push(...pipeLines);
        }
    }

    function parseInteractiveBulkPaste(text) {
        const buckets = { essay: [], fill: [], drag: [], dragMatch: [], dragSort: [] };
        let section = '';
        let stop = false;
        const buffer = [];
        const flush = () => {
            if (!section || section === 'skip' || !buffer.length) { buffer.length = 0; return; }
            pushInteractiveBulkLines(buckets, section, buffer);
            buffer.length = 0;
        };
        String(text || '').split('\n').forEach(rawLine => {
            if (stop) return;
            const line = String(rawLine || '').trim();
            if (!line) return;
            const nextSection = resolveInteractiveBulkSection(line);
            if (nextSection === 'stop') { flush(); stop = true; return; }
            if (nextSection) { flush(); if (nextSection !== 'skip') section = nextSection; return; }
            if (!isInteractivePipeLine(line)) {
                if (isEssayBulkLine(line, section)) buffer.push(line);
                return;
            }
            if (section && section !== 'skip') { buffer.push(line); return; }
            const kind = classifyInteractivePipeLine(line);
            if (kind === 'dragMatch' || kind === 'dragSort') buckets[kind].push(line);
            else if (kind === 'drag') pushInteractiveDragLine(buckets, line);
            else buckets[kind].push(line);
        });
        flush();
        return {
            essay: buckets.essay.join('\n'),
            fill: buckets.fill.join('\n'),
            drag: buckets.drag.join('\n'),
            dragMatch: buckets.dragMatch.join('\n'),
            dragSort: buckets.dragSort.join('\n')
        };
    }

    function normalizeGeminiSectionHeading(line) {
        return String(line || '')
            .replace(/^\s*#{1,6}\s*/, '')
            .replace(/^\s*[-*+]\s+/, '')
            .replace(/^\s*\d+[.)\-:]\s*/, '')
            .replace(/^\s*\*\*|\*\*\s*$/g, '')
            .replace(/[:：]\s*$/, '')
            .trim()
            .toUpperCase();
    }

    function resolveGeminiSectionKey(line) {
        const trimmed = String(line || '').trim();
        if (trimmed.includes('|')) return '';
        const heading = normalizeGeminiSectionHeading(line);
        if (!heading) return '';
        if (/^MỤC TIÊU(?:\s+BÀI HỌC)?/.test(heading)) return 'goal';
        if (/^LÝ THUYẾT/.test(heading)) return 'theory';
        if (/^(?:PHẦN\s+)?VÍ DỤ/.test(heading)) return 'examples';
        if (/^BÀI TẬP NỘP/.test(heading)) return 'selfPractice';
        if (/^BÀI TẬP TƯƠNG TÁC/.test(heading)) return 'interactive';
        if (/BÀI TẬP TỰ LUẬN/.test(heading)) return 'essay';
        if (/KÉO THẢ|KÉO VÀO Ô|KÉO VÀO TRỐNG/.test(heading)) return 'fill';
        if (/NỐI Ô/.test(heading) && /SẮP XẾP/.test(heading)) return 'dragMixed';
        if (/NỐI Ô|^NỐI\s/.test(heading)) return 'dragMatch';
        if (/SẮP XẾP/.test(heading)) return 'dragSort';
        if (/^TRẮC NGHIỆM/.test(heading)) return 'questions';
        if (/^KỸ NĂNG/.test(heading)) return 'skills';
        if (/^NHIỆM VỤ/.test(heading)) return 'tasks';
        if (/^DANH SÁCH HÌNH|^PROMPT TẠO/.test(heading)) return 'imageList';
        return '';
    }

    function parseGeminiLessonSections(raw) {
        const sections = {
            goal: '', theory: '', examples: '', selfPractice: '',
            interactive: '', essay: '', fill: '', drag: '', dragMatch: '', dragSort: '', dragMixed: '',
            questions: '', skills: '', tasks: '', imageList: ''
        };
        let current = '';
        const buffer = [];
        const flush = () => {
            if (!current || !buffer.length) { buffer.length = 0; return; }
            const text = buffer.join('\n').trim();
            if (text) sections[current] = sections[current] ? `${sections[current]}\n\n${text}` : text;
            buffer.length = 0;
        };
        String(raw || '').replace(/\r/g, '').split('\n').forEach(line => {
            const next = resolveGeminiSectionKey(line);
            if (next) { flush(); current = next; return; }
            if (current) buffer.push(line);
        });
        flush();
        const parsedInteractive = parseInteractiveBulkPaste(sections.interactive);
        const parsedDragMixed = parseInteractiveBulkPaste(sections.dragMixed);
        return {
            goal: sections.goal,
            theory: sections.theory,
            examples: sections.examples,
            selfPractice: sections.selfPractice,
            essay: preprocessEssaySectionText([sections.essay, parsedInteractive.essay].filter(Boolean).join('\n')),
            fill: sections.fill || parsedInteractive.fill,
            drag: [sections.drag, parsedInteractive.drag, parsedDragMixed.drag].filter(Boolean).join('\n'),
            dragMatch: [sections.dragMatch, parsedInteractive.dragMatch, parsedDragMixed.dragMatch].filter(Boolean).join('\n'),
            dragSort: [sections.dragSort, parsedInteractive.dragSort, parsedDragMixed.dragSort].filter(Boolean).join('\n'),
            questions: sections.questions,
            skills: sections.skills,
            tasks: sections.tasks,
            imageList: sections.imageList
        };
    }

    function normalizeImageId(value) {
        const text = String(value || '').trim().toUpperCase().replace(/\s+/g, '_');
        const match = text.match(/HINH[_-]*(\d+)/i) || text.match(/HÌNH[_-]*(\d+)/i);
        if (match) return `HINH_${String(match[1]).padStart(2, '0')}`;
        return text;
    }

    function parseImageManifest(text) {
        const entries = [];
        const lines = String(text || '').replace(/\r/g, '').split('\n');
        let current = null;
        lines.forEach(rawLine => {
            const line = String(rawLine || '').trim();
            if (!line) return;
            const hinhMatch = line.match(/^(HINH[_\s-]*\d+|HÌNH[_\s-]*\d+)\s*[:：]\s*(.+)$/i);
            if (hinhMatch) {
                if (current) entries.push(current);
                const id = normalizeImageId(hinhMatch[1]);
                const rest = hinhMatch[2].trim();
                const pipeParts = rest.split('|').map(p => p.trim());
                if (pipeParts.length >= 3) {
                    current = {
                        id,
                        section: pipeParts[0] || 'theory',
                        alt: pipeParts[1] || id,
                        type: pipeParts[2] || 'diagram',
                        prompt: pipeParts.slice(3).join(' | ') || ''
                    };
                } else {
                    const typeMatch = rest.match(/LOẠI:\s*(\S+)/i);
                    current = {
                        id,
                        section: 'theory',
                        alt: id,
                        type: (typeMatch?.[1] || 'diagram').toLowerCase(),
                        prompt: rest
                    };
                }
                return;
            }
            if (/^PROMPT TẠO ẢNH/i.test(line)) return;
            if (current && (line.startsWith('"') || line.length > 10)) {
                current.prompt = current.prompt ? `${current.prompt}\n${line.replace(/^["']|["']$/g, '')}` : line.replace(/^["']|["']$/g, '');
            }
        });
        if (current) entries.push(current);
        return entries;
    }

    function extractImageMarkers(text) {
        const found = new Set();
        let match;
        const re = new RegExp(IMAGE_MARKER_RE.source, 'gi');
        while ((match = re.exec(String(text || ''))) !== null) {
            found.add(normalizeImageId(match[1]));
        }
        String(text || '').split('\n').forEach(line => {
            const ref = line.trim();
            if (IMAGE_REF_RE.test(ref)) found.add(normalizeImageId(ref));
        });
        return [...found];
    }

    function collectMarkersFromPackage(pkg) {
        const markers = new Set();
        const scan = value => extractImageMarkers(value).forEach(id => markers.add(id));
        scan(pkg.goal_text || '');
        (pkg.theory || []).forEach(item => scan(typeof item === 'string' ? item : item.text));
        ['examples', 'self_practice'].forEach(key => {
            (pkg[key] || []).forEach(item => {
                scan(item.title || '');
                scan(item.body || '');
            });
        });
        ['essay_exercises', 'fill_exercises', 'drag_exercises', 'questions'].forEach(key => {
            (pkg[key] || []).forEach(item => {
                scan(item.prompt || '');
                (item.options || []).forEach(opt => scan(opt));
            });
        });
        return [...markers];
    }

    function formatQuestionPipeLine(q) {
        const options = q.options || [];
        const answerIndex = Number(q.answer);
        const letter = Number.isFinite(answerIndex) && answerIndex >= 0 && answerIndex <= 3
            ? ('ABCD'[answerIndex] || 'A')
            : String(q.answer || 'A').trim().toUpperCase().charAt(0) || 'A';
        return [q.skill || '', q.prompt || '', options[0] || '', options[1] || '', options[2] || '', options[3] || '', letter].join(' | ');
    }

    function formatQuestionsBulk(questions) {
        return (questions || []).map(formatQuestionPipeLine).join('\n');
    }

    function suggestSlugFromMeta(meta) {
        const subject = meta?.subject || '';
        const subjectCode = SUBJECT_CODES[subject] || 'lesson';
        return slugify([subjectCode, meta?.chapter || '', meta?.title || ''].join(' '));
    }

    function inferLessonTitle(pkg) {
        const existing = String(pkg?.title || '').trim();
        if (existing) return existing;
        const goal = String(pkg?.goal_text || '').trim();
        if (goal) {
            const line = goal.split(/\n+/).map(part => part.trim()).find(Boolean) || '';
            if (line.length >= 8) return line.slice(0, 120);
        }
        const chapter = String(pkg?.chapter || '').trim();
        if (chapter) return `Bài học — ${chapter}`.slice(0, 120);
        return 'Bài học import';
    }

    function ensureArray(value) {
        return Array.isArray(value) ? value : [];
    }

    function normalizeLessonImportPackage(pkg, options = {}) {
        const input = pkg && typeof pkg === 'object' ? { ...pkg } : {};
        const normalized = {
            schema_version: SCHEMA_VERSION,
            subject: String(input.subject || options.defaultSubject || '').trim(),
            chapter: String(input.chapter || '').trim(),
            title: String(input.title || '').trim(),
            slug: String(input.slug || '').trim(),
            order_index: Number(input.order_index) || 0,
            is_published: false,
            goal_text: String(input.goal_text || input.goal || '').trim(),
            theory: ensureArray(input.theory).map(normalizeTheoryItem).filter(b => b.text),
            examples: parseExamples(typeof input.examples === 'string' ? input.examples : formatExamplesFromArray(input.examples)),
            self_practice: parseExamples(typeof input.self_practice === 'string' ? input.self_practice : formatExamplesFromArray(input.self_practice)),
            essay_exercises: ensureArray(input.essay_exercises).length
                ? ensureArray(input.essay_exercises).map(canonicalizeEssayExercise)
                : parseEssayExercises(input.essay || ''),
            fill_exercises: ensureArray(input.fill_exercises).length
                ? ensureArray(input.fill_exercises)
                : parseFillExercises(input.fill || ''),
            drag_exercises: ensureArray(input.drag_exercises).length
                ? ensureArray(input.drag_exercises)
                : [
                    ...parseDragExercises(input.dragMatch || '', { preferMatch: true }),
                    ...parseDragExercises(input.dragSort || ''),
                    ...parseDragExercises(input.drag || '')
                ],
            questions: ensureArray(input.questions).length
                ? ensureArray(input.questions)
                : parseQuestions(input.questionsText || input.questions || '', parseSkills(input.skillsText || '')),
            skills: ensureArray(input.skills).length ? ensureArray(input.skills) : parseSkills(input.skillsText || ''),
            tasks: ensureArray(input.tasks).length ? ensureArray(input.tasks).map(String) : parseLines(input.tasksText || input.tasks || ''),
            videos: ensureArray(input.videos),
            image_manifest: ensureArray(input.image_manifest),
            generated_at: input.generated_at || new Date().toISOString(),
            source: input.source || { tool: 'unknown', prompt_version: PROMPT_VERSION },
            import_notes: ensureArray(input.import_notes)
        };

        if (!normalized.title) {
            normalized.title = inferLessonTitle(normalized);
        }

        if (!normalized.slug) {
            normalized.slug = suggestSlugFromMeta(normalized);
        }

        if (!normalized.image_manifest.length && input.imageList) {
            normalized.image_manifest = parseImageManifest(input.imageList);
        }

        if (options.forceUnpublished !== false) {
            normalized.is_published = false;
        }

        normalized.drag_exercises = ensureArray(normalized.drag_exercises)
            .map(canonicalizeDragExerciseItem)
            .filter(item => {
                if (item.mode === 'match') return item.prompt && item.left?.length && item.right?.length && item.pairs?.length;
                return item.prompt && item.items?.length && item.answer?.length;
            });

        return normalized;
    }

    function formatExamplesFromArray(items) {
        return (items || []).map(item => `${item.title || ''}\n${item.body || ''}`).join('\n\n');
    }

    function multisetEqual(a, b) {
        const sig = arr => [...arr].map(normalizePoolToken).filter(Boolean).sort((x, y) => x.localeCompare(y, 'vi')).join('\u0001');
        return sig(a) === sig(b);
    }

    const DEFAULT_LESSON_VIDEO_URL = 'https://www.youtube.com/watch?v=PLACEHOLDER_CAP_NHAT_SAU';

    function quoteLine(text, maxLen = 160) {
        const value = String(text || '').trim();
        if (!value) return '«(không thấy dòng trong bài)»';
        if (value.length <= maxLen) return `«${value}»`;
        return `«${value.slice(0, maxLen)}…»`;
    }

    function getSectionRawLines(raw, sectionKey) {
        if (!raw) return [];
        const sections = parseGeminiLessonSections(raw);
        const section = sections[sectionKey] || '';
        return String(section).split('\n').map(line => line.trim()).filter(Boolean);
    }

    function findEssayRawLine(essayLines, essay, index) {
        const lines = essayLines || [];
        if (lines[index]) return lines[index];
        if (!essay || !essay.prompt) return lines[index] || '';
        const needle = String(essay.prompt).trim().slice(0, 48);
        for (let i = 0; i < lines.length; i++) {
            if (lines[i].includes(needle)) return lines[i];
            if (needle.includes(lines[i].slice(0, 48))) return lines[i];
        }
        return lines[index] || '';
    }

    function buildValidationContext(raw, pkg) {
        return {
            raw: raw || '',
            pkg: pkg || null,
            tool: 'soanbaigemini',
            essayLines: getSectionRawLines(raw, 'essay'),
            fillLines: getSectionRawLines(raw, 'fill'),
            dragSortLines: getSectionRawLines(raw, 'dragSort'),
            dragMatchLines: getSectionRawLines(raw, 'dragMatch'),
            questionLines: getSectionRawLines(raw, 'questions'),
            essayItems: (pkg && pkg.essay_exercises) || [],
            fillItems: (pkg && pkg.fill_exercises) || [],
            dragItems: (pkg && pkg.drag_exercises) || [],
            questionItems: (pkg && pkg.questions) || []
        };
    }

    function humanizeValidationError(message, context = {}) {
        const text = String(message || '');
        let m;
        const pkg = context.pkg || {};

        m = text.match(/essay_exercises\[(\d+)\]\.answer rỗng/);
        if (m) {
            const essayIdx = Number(m[1]);
            const essayNo = essayIdx + 1;
            const essay = context.essayItems && context.essayItems[essayIdx];
            const rawLine = findEssayRawLine(context.essayLines, essay, essayIdx);
            return `【BÀI TẬP TỰ LUẬN — Câu ${essayNo}】Thiếu cột Đáp án (số) ở giữa.\n`
                + `📍 Tìm heading BÀI TẬP TỰ LUẬN NGẮN, sửa dòng thứ ${essayNo}:\n`
                + `   Hiện tại: ${quoteLine(rawLine || (essay && essay.prompt))}\n`
                + `✏️ Đúng 3 cột: Đề bài | Đáp án (chỉ số, vd 42) | Gợi ý\n`
                + `   Ví dụ: ${quoteLine('Tính 12 + 15 | 27 | Cộng hàng đơn vị trước')}`;
        }

        m = text.match(/fill_exercises\[(\d+)\]\.pool rỗng/);
        if (m) {
            const fillIdx = Number(m[1]);
            return `【KÉO THẢ VÀO Ô TRỐNG — Câu ${fillIdx + 1}】Thiếu cột mảnh kéo (cột 2).\n`
                + `📍 Dòng hiện tại: ${quoteLine(context.fillLines && context.fillLines[fillIdx])}\n`
                + `✏️ Đủ 4 cột: Đề có ___ | mảnh1 » mảnh2 » nhiễu | đáp án1 » đáp án2 | gợi ý`;
        }

        m = text.match(/drag_exercises\[(\d+)\]/);
        if (m) {
            const dragIdx = Number(m[1]);
            const drag = context.dragItems && context.dragItems[dragIdx];
            const dragName = drag && drag.mode === 'sort' ? 'SẮP XẾP THỨ TỰ' : 'NỐI Ô';
            let rawDragLine = '';
            if (drag && drag.mode === 'sort' && context.dragSortLines) {
                let sortCount = 0;
                (context.dragItems || []).forEach((item, i) => {
                    if (i < dragIdx && item.mode === 'sort') sortCount++;
                });
                rawDragLine = context.dragSortLines[sortCount] || '';
            }
            if (/số phần tử đáp án/.test(text)) {
                return `【${dragName} — Câu ${dragIdx + 1}】Số mảnh ở cột 3 không khớp cột 2.\n`
                    + `📍 Dòng hiện tại: ${quoteLine(rawDragLine || (drag && drag.prompt))}\n`
                    + `✏️ Cột 3 phải có đúng số mảnh như cột 2.`;
            }
            if (/mode phải là match hoặc sort/.test(text)) {
                return `【NỐI Ô / SẮP XẾP — Câu ${dragIdx + 1}】Dòng chưa đúng dạng bài tập kéo thả.\n`
                    + `📍 ${quoteLine(rawDragLine || (drag && drag.prompt))}`;
            }
            if (/pairs/.test(text)) {
                return `【NỐI Ô — Câu ${dragIdx + 1}】Chỉ số nối (vd 0-0,1-1) vượt quá số ô Trái/Phải.`;
            }
        }

        m = text.match(/questions\[(\d+)\]/);
        if (m) {
            const qIdx = Number(m[1]);
            const qNo = qIdx + 1;
            const qLine = context.questionLines && context.questionLines[qIdx];
            if (/answer phải từ 0 đến 3/.test(text)) {
                return `【TRẮC NGHIỆM — Câu ${qNo}】Đáp án cuối phải là A, B, C hoặc D.\n`
                    + `📍 Dòng hiện tại: ${quoteLine(qLine)}`;
            }
            if (/phải có đúng 4 lựa chọn/.test(text)) {
                return `【TRẮC NGHIỆM — Câu ${qNo}】Thiếu phương án A/B/C/D.\n`
                    + `📍 Dòng hiện tại: ${quoteLine(qLine)}\n`
                    + `✏️ Đủ 7 cột: skill_id | Câu hỏi | A | B | C | D | B`;
            }
            if (/skill/.test(text)) {
                return `【TRẮC NGHIỆM — Câu ${qNo}】skill_id không có trong phần KỸ NĂNG.\n`
                    + `📍 Dòng hiện tại: ${quoteLine(qLine)}`;
            }
        }

        if (text === 'Thiếu title.') {
            return context.tool === 'admin'
                ? '【THÔNG TIN BÀI】Chưa có tên bài — điền ô "Tên bài học" ở mục 1.'
                : '【THÔNG TIN BÀI】Chưa có tên bài — điền ô "Tên bài học" ở mục 1.';
        }
        if (text === 'Thiếu slug.') {
            return context.tool === 'admin'
                ? '【THÔNG TIN BÀI】Chưa tạo được slug — kiểm tra tên bài và chương ở mục 1.'
                : '【THÔNG TIN BÀI】Chưa tạo được slug — kiểm tra tên bài và chương.';
        }
        if (/Môn ".+" không hợp lệ/.test(text)) return '【LỚP/MÔN】Chọn đúng Toán 4–9 ở mục 1.';
        if (/schema_version/.test(text)) return '【JSON】Sai phiên bản file import — tải lại trang (Ctrl+F5).';

        const hint = context.tool === 'admin'
            ? '✏️ Sửa trong ô import Gemini hoặc tab tương ứng rồi bấm Kiểm tra import.'
            : '✏️ Sửa trong ô kết quả Gemini rồi bấm Kiểm tra import.';
        return `【LỖI】${text}\n${hint}`;
    }

    function humanizeValidationWarning(message, context = {}) {
        const text = String(message || '');
        const m = text.match(/drag_exercises\[(\d+)\]/);
        if (m && /hoán vị/.test(text)) {
            const dragIdx = Number(m[1]);
            const drag = context.dragItems && context.dragItems[dragIdx];
            return `【SẮP XẾP — Câu ${dragIdx + 1}】Thứ tự đúng có thể chưa khớp các mảnh.\n`
                + `📍 Đề: ${quoteLine(drag && drag.prompt, 100)}`;
        }
        if (/skill/.test(text) && /80%/.test(text)) return '【TRẮC NGHIỆM】Nhiều câu dùng chung một skill_id — kiểm tra cột đầu mỗi dòng.';
        if (/Marker/.test(text)) return `【HÌNH ẢNH】${text.replace('Marker ', 'Ảnh ')} — bổ sung trong DANH SÁCH HÌNH ẢNH.`;
        if (/image_manifest rỗng/.test(text)) return '【HÌNH ẢNH】Có HINH_xx trong bài nhưng chưa khai báo DANH SÁCH HÌNH ẢNH.';
        if (/trắc nghiệm ít hơn/.test(text)) return '【TRẮC NGHIỆM】Ít hơn 5 câu — có thể vẫn import.';
        if (/Không có ảnh/.test(text)) return '【HÌNH ẢNH】Bài không có HINH_xx — không bắt buộc nếu không cần minh họa.';
        if (/fill_exercises/.test(text)) return '【KÉO THẢ】Đáp án có thể không nằm trong danh sách mảnh — kiểm tra cột 2 và 3.';
        if (/subject/.test(text) && /khác trang/.test(text)) return '【LỚP】Môn trong bài khác mục Lớp đã chọn.';
        if (/Slug/.test(text)) return `【SLUG】${text} — đổi tên bài nếu cần.`;
        return `【CẢNH BÁO】${text}`;
    }

    function filterValidationWarnings(warnings = []) {
        return (warnings || []).filter(item => item !== 'Thiếu video.');
    }

    function ensurePackageVideos(pkg, options = {}) {
        if (!pkg) return pkg;
        if (pkg.videos && pkg.videos.length) return pkg;
        const videoUrl = String(options.videoUrl || '').trim();
        if (videoUrl) {
            pkg.videos = parseVideos(videoUrl);
            return pkg;
        }
        pkg.videos = [{ title: 'Video bài giảng (cập nhật sau)', url: DEFAULT_LESSON_VIDEO_URL }];
        return pkg;
    }

    function enrichLessonValidation(validation, raw, pkg, options = {}) {
        const context = buildValidationContext(raw, pkg);
        context.tool = options.tool || context.tool;
        const errors = validation?.errors || [];
        const warnings = filterValidationWarnings(validation?.warnings || []);
        return {
            errors,
            errorsVi: errors.map(item => humanizeValidationError(item, context)),
            warnings,
            warningsVi: warnings.map(item => humanizeValidationWarning(item, context)),
            ready: errors.length === 0,
            pkg: pkg || null,
            context
        };
    }

    function validateLessonImportPackage(pkg, options = {}) {
        const errors = [];
        const warnings = [];
        const pageSubject = options.pageSubject || '';
        const existingSlugs = new Set((options.existingSlugs || []).map(s => String(s).trim()));

        if (!pkg || typeof pkg !== 'object') {
            errors.push('JSON không parse được hoặc không phải object.');
            return { errors, warnings };
        }

        if (pkg.schema_version !== SCHEMA_VERSION) {
            errors.push(`schema_version phải là "${SCHEMA_VERSION}".`);
        }

        if (!VALID_SUBJECTS.includes(pkg.subject)) {
            errors.push(`Môn "${pkg.subject || ''}" không hợp lệ.`);
        }

        if (!pkg.title) errors.push('Thiếu title.');
        if (!pkg.slug) errors.push('Thiếu slug.');

        if (pageSubject && pkg.subject && pkg.subject !== pageSubject) {
            warnings.push(`subject "${pkg.subject}" khác trang đang mở "${pageSubject}".`);
        }

        if (existingSlugs.has(pkg.slug)) {
            warnings.push(`Slug "${pkg.slug}" có thể trùng bài đang có.`);
        }

        const skillIds = new Set((pkg.skills || []).map(s => s.id));
        (pkg.questions || []).forEach((q, i) => {
            const answer = Number(q.answer);
            if (!Number.isFinite(answer) || answer < 0 || answer > 3) {
                errors.push(`questions[${i}].answer phải từ 0 đến 3.`);
            }
            if (!Array.isArray(q.options) || q.options.length !== 4) {
                errors.push(`questions[${i}] phải có đúng 4 lựa chọn.`);
            }
            if (q.skill && skillIds.size && !skillIds.has(q.skill)) {
                errors.push(`questions[${i}].skill "${q.skill}" không tồn tại trong skills.`);
            }
        });

        if (pkg.questions?.length && skillIds.size) {
            const counts = {};
            pkg.questions.forEach(q => { counts[q.skill] = (counts[q.skill] || 0) + 1; });
            const max = Math.max(...Object.values(counts));
            if (max / pkg.questions.length > 0.8) {
                warnings.push('Hơn 80% câu TN gán vào một skill — có thể thiếu cột skill_id.');
            }
        }

        (pkg.skills || []).forEach((s, i) => {
            const t = Number(s.target);
            if (!Number.isFinite(t) || t < 0 || t > 100) {
                warnings.push(`skills[${i}].target nên từ 0–100.`);
            }
        });

        (pkg.essay_exercises || []).forEach((e, i) => {
            if (!String(e.answer || '').trim()) {
                errors.push(`essay_exercises[${i}].answer rỗng.`);
            }
        });

        (pkg.fill_exercises || []).forEach((f, i) => {
            const pool = f.pool || f.items || [];
            if (!pool.length) errors.push(`fill_exercises[${i}].pool rỗng.`);
            const answers = Array.isArray(f.answer) ? f.answer : [f.answer];
            if (answers.length === 1 && pool.length && !pool.includes(answers[0])) {
                warnings.push(`fill_exercises[${i}]: đáp án có thể không nằm trong pool.`);
            }
        });

        (pkg.drag_exercises || []).forEach((d, i) => {
            if (d.mode !== 'match' && d.mode !== 'sort') {
                errors.push(`drag_exercises[${i}].mode phải là match hoặc sort.`);
            }
            if (d.mode === 'match') {
                (d.pairs || []).forEach((p, pi) => {
                    if (p.left >= (d.left || []).length || p.right >= (d.right || []).length) {
                        errors.push(`drag_exercises[${i}].pairs[${pi}] vượt phạm vi.`);
                    }
                });
            }
            if (d.mode === 'sort' && d.items?.length && d.answer?.length) {
                if (d.items.length !== d.answer.length) {
                    errors.push(`drag_exercises[${i}]: số phần tử đáp án phải bằng số mảnh sắp xếp.`);
                } else if (!multisetEqual(d.items, d.answer)) {
                    warnings.push(`drag_exercises[${i}]: đáp án có thể chưa là hoán vị chuẩn của các mảnh — kiểm tra tab Sắp xếp.`);
                }
            }
        });

        const markers = collectMarkersFromPackage(pkg);
        const manifestIds = new Set((pkg.image_manifest || []).map(e => normalizeImageId(e.id)));
        markers.forEach(id => {
            if (!manifestIds.has(id)) warnings.push(`Marker ${id} chưa có trong image_manifest.`);
        });
        if (markers.length && !pkg.image_manifest?.length) {
            warnings.push('Nội dung có HINH_xx nhưng image_manifest rỗng.');
        }

        if (!pkg.videos?.length) warnings.push('Thiếu video.');
        if (!markers.length && !pkg.image_manifest?.length) warnings.push('Không có ảnh/minh họa.');
        if (pkg.questions?.length < 5) warnings.push('Số lượng trắc nghiệm ít hơn gợi ý (5+).');

        return { errors, warnings };
    }

    function buildLessonImportPackage(options = {}) {
        const raw = String(options.rawGeminiText || '').trim();
        const meta = options.metadata || {};
        const sections = parseGeminiLessonSections(raw);
        const skills = parseSkills(sections.skills);
        const pkg = normalizeLessonImportPackage({
            schema_version: SCHEMA_VERSION,
            subject: meta.subject || '',
            chapter: meta.chapter || '',
            title: meta.title || '',
            slug: meta.slug || '',
            order_index: meta.order_index || 0,
            is_published: false,
            goal_text: sections.goal,
            theory: parseTheoryBlocks(sections.theory),
            examples: parseExamples(sections.examples),
            self_practice: parseExamples(sections.selfPractice),
            essay_exercises: parseEssayExercises(sections.essay),
            fill_exercises: parseFillExercises(sections.fill),
            drag_exercises: [
                ...parseDragExercises(sections.dragMatch, { preferMatch: true }),
                ...parseDragExercises(sections.dragSort),
                ...parseDragExercises(sections.drag || '')
            ],
            questions: parseQuestions(sections.questions, skills),
            skills,
            tasks: parseLines(sections.tasks),
            videos: [],
            image_manifest: parseImageManifest(sections.imageList),
            generated_at: new Date().toISOString(),
            source: {
                tool: meta.tool || 'soanbaigemini',
                prompt_version: meta.prompt_version || PROMPT_VERSION,
                model: meta.model || ''
            },
            import_notes: []
        }, { defaultSubject: meta.subject, forceUnpublished: true });
        return pkg;
    }

    function packageFromSavePayload(payload) {
        const p = payload || {};
        return normalizeLessonImportPackage({
            schema_version: SCHEMA_VERSION,
            subject: p.subject,
            chapter: p.chapter,
            title: p.title,
            slug: p.slug,
            order_index: p.order_index,
            is_published: false,
            goal_text: p.goal_text || p.goal || '',
            theory: p.theory || [],
            examples: p.examples || [],
            self_practice: p.self_practice || [],
            essay_exercises: p.essay_exercises || [],
            fill_exercises: p.fill_exercises || [],
            drag_exercises: p.drag_exercises || [],
            questions: p.questions || [],
            skills: p.skills || [],
            tasks: p.tasks || [],
            videos: p.videos || [],
            image_manifest: p.image_manifest || [],
            generated_at: new Date().toISOString(),
            source: { tool: 'admin-export', prompt_version: PROMPT_VERSION },
            import_notes: []
        }, { forceUnpublished: true });
    }

    function packageToSavePayload(pkg) {
        const p = normalizeLessonImportPackage(pkg, { forceUnpublished: true });
        return {
            action: 'save_content',
            slug: p.slug,
            subject: p.subject,
            chapter: p.chapter,
            title: p.title,
            order_index: p.order_index,
            is_published: p.is_published,
            goal_text: p.goal_text,
            theory: p.theory,
            examples: p.examples,
            self_practice: p.self_practice,
            essay_exercises: p.essay_exercises,
            fill_exercises: p.fill_exercises,
            drag_exercises: p.drag_exercises,
            videos: p.videos,
            skills: p.skills,
            tasks: p.tasks,
            questions: p.questions
        };
    }

    function formatEssayExercises(items) {
        return (items || []).map(item => {
            const c = canonicalizeEssayExercise(item);
            return [c.prompt || '', c.answer || '', c.hint || ''].join(' | ');
        }).join('\n');
    }

    function formatFillExercises(items) {
        return (items || []).map(item => {
            const pool = joinPoolText(item.pool || item.items || []);
            const answer = Array.isArray(item.answer) ? joinPoolText(item.answer) : String(item.answer || '');
            const parts = [item.prompt || '', pool, answer, item.hint || ''];
            return parts.filter((part, idx, arr) => !(idx === 1 && part === arr[2])).join(' | ');
        }).join('\n');
    }

    function formatDragExercises(items) {
        return (items || []).map(item => {
            const c = canonicalizeDragExerciseItem(item);
            if (c.mode === 'match') {
                return [c.prompt, joinPoolText(c.left), joinPoolText(c.right), c.pair_spec || '', c.hint || ''].join(' | ');
            }
            return [c.prompt, joinPoolText(c.items), joinPoolText(c.answer), c.hint || ''].join(' | ');
        }).join('\n');
    }

    function sectionsToEditorTexts(sections, skills) {
        const dragItems = [
            ...parseDragExercises(sections.dragMatch || '', { preferMatch: true }),
            ...parseDragExercises(sections.dragSort || ''),
            ...parseDragExercises(sections.drag || '')
        ];
        return {
            goal: sections.goal || '',
            theory: sections.theory || '',
            examples: sections.examples || '',
            selfPractice: sections.selfPractice || '',
            essay: sections.essay || '',
            fill: sections.fill || '',
            drag: dragItems.map(item => {
                if (item.mode === 'match') {
                    return [item.prompt, joinPoolText(item.left), joinPoolText(item.right), item.pair_spec, item.hint].join(' | ');
                }
                return [item.prompt, joinPoolText(item.items), joinPoolText(item.answer), item.hint].join(' | ');
            }).join('\n'),
            questions: formatQuestionsBulk(parseQuestions(sections.questions || '', skills)),
            skills: (skills || []).map(s => `${s.id} | ${s.name} | ${s.target}`).join('\n'),
            tasks: sections.tasks || '',
            imageList: sections.imageList || ''
        };
    }

    function formatExamplesText(items) {
        return (items || []).map(item => {
            const title = String(item?.title ?? '').trim() || 'Ví dụ';
            const parsed = parseContentWithAiMarker(String(item?.body ?? ''));
            const ai = Object.prototype.hasOwnProperty.call(item || {}, 'ai') ? !!item.ai : parsed.ai;
            const body = ai ? `${parsed.text}\n${AI_MARKER}` : parsed.text;
            return `${title}\n${body}`.trim();
        }).join('\n\n');
    }

    function questionsToEditorItems(questions, skills = []) {
        return (questions || []).map(item => {
            const options = item.options || [];
            const answerIndex = Number(item.answer);
            const answerLetter = Number.isFinite(answerIndex) && answerIndex >= 0 && answerIndex <= 3
                ? ('ABCD'[answerIndex] || 'A')
                : String(item.answer || 'A').trim().toUpperCase().charAt(0) || 'A';
            return {
                skill: item.skill || skills[0]?.id || '',
                cau: item.prompt || '',
                a: options[0] || '',
                b: options[1] || '',
                c: options[2] || '',
                d: options[3] || '',
                dung: answerLetter
            };
        });
    }

    const LessonImport = {
        SCHEMA_VERSION,
        PROMPT_VERSION,
        getInteractiveFormatGuide,
        preprocessEssaySectionText,
        canonicalizeEssayExercise,
        canonicalizeDragExerciseItem,
        normalizeDragLineParts,
        normalizePoolPieces,
        extractMatchPairsFromSpec,
        VALID_SUBJECTS,
        SUBJECT_CODES,
        AI_MARKER,
        DEFAULT_LESSON_VIDEO_URL,
        quoteLine,
        getSectionRawLines,
        findEssayRawLine,
        buildValidationContext,
        humanizeValidationError,
        humanizeValidationWarning,
        filterValidationWarnings,
        ensurePackageVideos,
        enrichLessonValidation,
        slugify,
        parseLines,
        splitQuestionParts,
        parseContentWithAiMarker,
        normalizeTheoryItem,
        parseTheoryBlocks,
        formatTheoryBlocks,
        parseExamples,
        formatExamplesText,
        parseSkills,
        parseVideos,
        parseQuestions,
        parseQuestionsReport,
        parseEssayExercises,
        parseFillExercises,
        parseDragExercises,
        buildDragExercisesFromItems,
        parseGeminiLessonSections,
        parseInteractiveBulkPaste,
        parseImageManifest,
        extractImageMarkers,
        collectMarkersFromPackage,
        normalizeLessonImportPackage,
        validateLessonImportPackage,
        buildLessonImportPackage,
        packageFromSavePayload,
        packageToSavePayload,
        suggestSlugFromMeta,
        formatQuestionPipeLine,
        formatQuestionsBulk,
        questionsToEditorItems,
        sectionsToEditorTexts,
        formatEssayExercises,
        formatFillExercises,
        formatDragExercises,
        normalizeFillParts,
        normalizeMcqBulkLine,
        looksLikeSkillId,
        poolsLookLikeSortOrder,
        poolTextHasMultipleItems,
        joinPoolText,
        splitPoolText,
        repairPoolPieces,
        parseMatchPairs,
        buildDefaultMatchPairSpec,
        isDragMatchItem,
        normalizeBulkHeading,
        classifyInteractivePipeLine,
        resolveInteractiveBulkSection,
        isInteractivePipeLine
    };

    global.LessonImport = LessonImport;
})(typeof window !== 'undefined' ? window : globalThis);