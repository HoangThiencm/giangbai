/**
 * lesson-import.js — parser, normalizer, validator và adapter lesson-import-v1
 * Dùng chung: admin-lesson-manager.js, soanbaigemini.html
 */
(function (global) {
    'use strict';

    const SCHEMA_VERSION = 'lesson-import-v1';
    const PROMPT_VERSION = '2026-06-scope-v3';
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
        } catch {
            return false;
        }
    }

    function readQuestionBlocks(text, fallbackSkill) {
        const lines = decodePastedText(text).split('\n').map(line => line.trim()).filter(Boolean);
        const blocks = [];
        let buffer = '';
        lines.forEach(line => {
            const normalized = normalizeMcqBulkLine(line);
            if (splitQuestionParts(normalized).length >= 6) {
                if (buffer.trim()) parseQuestionLine(buffer, blocks.length, fallbackSkill);
                blocks.push(normalized);
                buffer = '';
                return;
            }
            buffer = buffer ? `${buffer} ${line}` : line;
            if (canParseQuestionBlock(buffer, fallbackSkill)) {
                blocks.push(buffer);
                buffer = '';
            }
        });
        if (buffer.trim()) parseQuestionLine(buffer, blocks.length, fallbackSkill);
        return blocks;
    }

    function parseQuestions(text, skills = []) {
        const fallbackSkill = skills[0]?.id || 'tong_hop';
        return readQuestionBlocks(text, fallbackSkill).map((line, index) => parseQuestionLine(line, index, fallbackSkill));
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
            text = text.replace(new RegExp(`(?<!_)\\b${escaped}\\b(?!_)`), '___');
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
        return String(spec || '').split(',').map(part => part.trim()).filter(Boolean).map(part => {
            const [left, right] = part.split('-').map(value => Number.parseInt(value, 10));
            if (!Number.isFinite(left) || !Number.isFinite(right)) return null;
            return { left, right };
        }).filter(Boolean);
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
        const parts = splitQuestionParts(line);
        const prompt = parts[0] || '';
        let pairSpec = parts[3] || '';
        if (!(pairSpec && /\d+\s*-\s*\d+/.test(pairSpec)) && options.preferMatch) {
            const left = repairPoolPieces(splitPoolText(parts[1]), 0);
            const right = repairPoolPieces(splitPoolText(parts[2]), 0);
            pairSpec = buildDefaultMatchPairSpec(left.length, right.length);
        }
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
        return parseLines(text).map((line, index) => {
            const parts = splitQuestionParts(line);
            return { id: `essay_${index + 1}`, prompt: parts[0] || '', answer: parts[1] || '', hint: parts[2] || '' };
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

    function pushInteractiveBulkLines(buckets, section, lines) {
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
        if (section === 'essay' || section === 'fill' || section === 'drag') {
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
            if (!isInteractivePipeLine(line)) return;
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
            essay: sections.essay || parsedInteractive.essay,
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
                ? ensureArray(input.essay_exercises)
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

        return normalized;
    }

    function formatExamplesFromArray(items) {
        return (items || []).map(item => `${item.title || ''}\n${item.body || ''}`).join('\n\n');
    }

    function multisetEqual(a, b) {
        const sig = arr => [...arr].map(x => String(x).trim()).sort((x, y) => x.localeCompare(y, 'vi')).join('\u0001');
        return sig(a) === sig(b);
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
                if (!multisetEqual(d.items, d.answer)) {
                    errors.push(`drag_exercises[${i}]: answer phải là hoán vị của items.`);
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
        VALID_SUBJECTS,
        SUBJECT_CODES,
        AI_MARKER,
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