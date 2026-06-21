/**
 * Gộp câu hỏi bị cắt ngang giữa 2 trang PDF ([[Tiếp nối]], đáp án mồ côi).
 */
(function (global) {
    const CONTINUATION_RE = /^\[\[?\s*(tiếp\s*nối|tiep\s*noi|continued)\s*\]\]?/i;

    function normalizeText(text) {
        return String(text || '').replace(/\s+/g, '').toLowerCase();
    }

    function ensureOptions(opts) {
        const arr = Array.isArray(opts) ? opts.map((o) => String(o || '').trim()) : [];
        while (arr.length < 4) arr.push('');
        return arr.slice(0, 4);
    }

    function countFilledOptions(opts) {
        return ensureOptions(opts).filter((o) => o.length > 0).length;
    }

    function stripContinuationMarker(text) {
        return String(text || '')
            .replace(/^\[\[?\s*(tiếp\s*nối|tiep\s*noi|continued[^\]]*)\s*\]\]?\s*/i, '')
            .trim();
    }

    function isContinuationQuestion(q) {
        if (!q || typeof q !== 'object') return false;
        const text = String(q.question || '').trim();
        if (CONTINUATION_RE.test(text)) return true;
        if (/tiếp\s*nối/i.test(text) && text.length < 40) return true;
        const filled = countFilledOptions(q.options);
        const qNorm = normalizeText(stripContinuationMarker(text));
        if (filled >= 2 && qNorm.length < 18) return true;
        return false;
    }

    function isIncompleteQuestion(q) {
        if (!q || typeof q !== 'object') return false;
        const text = String(q.question || '').trim();
        if (!text || isContinuationQuestion(q)) return false;
        const opts = ensureOptions(q.options);
        const filled = countFilledOptions(opts);
        if (filled < 4) return true;
        if (!opts[3] || (!opts[2] && filled <= 3)) return true;
        return false;
    }

    function shouldMergeAcrossPages(prev, next) {
        if (!prev || !next || !isContinuationQuestion(next)) return false;
        const nextText = String(next.question || '').trim();
        if (CONTINUATION_RE.test(nextText) || /tiếp\s*nối/i.test(nextText)) return true;
        return isIncompleteQuestion(prev);
    }

    function mergeTwoQuestions(prev, next) {
        const pOpts = ensureOptions(prev.options);
        const nOpts = ensureOptions(next.options);
        const mergedOpts = pOpts.map((p, i) => (p || nOpts[i] || ''));

        let question = String(prev.question || '').trim();
        const nextQ = stripContinuationMarker(next.question || '');
        if (nextQ && !CONTINUATION_RE.test(String(next.question || ''))) {
            if (!question) question = nextQ;
            else if (!/[.?!:;)\]]$/.test(question) || /^[a-zà-ỹ0-9$\\]/.test(nextQ)) {
                question = `${question} ${nextQ}`.replace(/\s+/g, ' ').trim();
            }
        }

        const prevIdx = parseInt(prev.correct_index, 10);
        const nextIdx = parseInt(next.correct_index, 10);
        return {
            ...prev,
            question,
            options: mergedOpts,
            correct_index: prevIdx >= 0 ? prevIdx : (nextIdx >= 0 ? nextIdx : -1),
            status: prev.status || next.status || 'done',
            stitched: true,
        };
    }

    function isDuplicate(q1, q2) {
        if (!q1 || !q2) return false;
        let t1 = normalizeText(q1.question);
        let t2 = normalizeText(q2.question);
        if (t1.length < 20) t1 += normalizeText((q1.options || []).join(''));
        if (t2.length < 20) t2 += normalizeText((q2.options || []).join(''));
        if (!t1 || !t2) return false;
        if (t1 === t2) return true;
        if (t1.length > 50 && t2.length > 50 && (t1.includes(t2) || t2.includes(t1))) return true;
        const minLen = Math.min(t1.length, t2.length);
        const maxLen = Math.max(t1.length, t2.length);
        if (maxLen === 0) return false;
        let same = 0;
        for (let i = 0; i < minLen; i++) if (t1[i] === t2[i]) same++;
        return (same / maxLen) > 0.85;
    }

    function dedupeQuestions(rows) {
        const out = [];
        (rows || []).forEach((q) => {
            if (!q) return;
            if (!out.some((x) => isDuplicate(x, q))) out.push(q);
        });
        return out;
    }

    function stitchPageQuestionsList(pageQuestions, sortedPages) {
        const result = {};
        Object.keys(pageQuestions || {}).forEach((k) => {
            result[k] = (pageQuestions[k] || []).map((q) => ({ ...q, options: ensureOptions(q.options) }));
        });

        const pages = Array.isArray(sortedPages) ? sortedPages : [];
        for (let pi = 1; pi < pages.length; pi++) {
            const prevPage = pages[pi - 1];
            const currPage = pages[pi];
            const prevQs = result[prevPage.id];
            const currQs = result[currPage.id];
            if (!prevQs?.length || !currQs?.length) continue;

            while (currQs.length > 0) {
                const head = currQs[0];
                const tail = prevQs[prevQs.length - 1];
                if (!shouldMergeAcrossPages(tail, head)) break;
                prevQs[prevQs.length - 1] = mergeTwoQuestions(tail, head);
                currQs.shift();
            }
        }

        return result;
    }

    function flattenStitchedQuestions(pageQuestions, sortedPages) {
        const stitched = stitchPageQuestionsList(pageQuestions, sortedPages);
        const flat = [];
        const pages = Array.isArray(sortedPages) ? sortedPages : [];
        pages.forEach((p) => {
            const qs = dedupeQuestions(stitched[p.id] || []);
            qs.forEach((q) => {
                if (!flat.some((x) => isDuplicate(x, q))) flat.push(q);
            });
        });
        return flat;
    }

    function countStitchMerges(before, after, sortedPages) {
        let removed = 0;
        const pages = Array.isArray(sortedPages) ? sortedPages : [];
        pages.forEach((p) => {
            const a = (before[p.id] || []).length;
            const b = (after[p.id] || []).length;
            if (b < a) removed += (a - b);
        });
        return removed;
    }

    global.ExamStitch = {
        isContinuationQuestion,
        isIncompleteQuestion,
        shouldMergeAcrossPages,
        mergeTwoQuestions,
        isDuplicate,
        dedupeQuestions,
        stitchPageQuestionsList,
        flattenStitchedQuestions,
        countStitchMerges,
        ensureOptions,
    };
})(window);