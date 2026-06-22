/**
 * Gọi Gemini Vision trực tiếp từ trình duyệt — không phụ thuộc PHP/hosting gọi ra ngoài.
 */
(function (global) {
    const SEGMENT_PROMPT = `Trích xuất câu hỏi trắc nghiệm từ phần ảnh này.

YÊU CẦU QUAN TRỌNG:
1. ĐỌC KỸ: Tìm đủ các câu có đánh số (Câu X, Bài X...).
2. CHUẨN HÓA NGHIÊM NGẶT TOÁN HỌC (LATEX): Inline $...$, Display $$...$$
3. ĐÁP ÁN: Tách riêng 4 lựa chọn A, B, C, D vào mảng "options".
4. KHÔNG BỊA ĐẶT nội dung bị cắt.
5. CẮT TRANG: Nếu thấy đáp án (A,B,C,D) ở ĐẦU ảnh mà không có câu hỏi -> tạo câu question="[[Tiếp nối]]" với các options tương ứng. Nếu câu cuối ảnh thiếu đáp án (chỉ có A,B) -> chỉ ghi những gì thấy, KHÔNG bịa C,D.

OUTPUT JSON (Mảng): [{"question": "...", "options": ["...",...], "correct_index": -1}, ...]`;

    const MANUAL_PROMPT = `Trích xuất câu hỏi trắc nghiệm từ VÙNG ẢNH.
Toán học bắt buộc dùng LaTeX: $x^2$, $\\frac{a}{b}$, $\\Delta$.
OUTPUT JSON (Mảng): [{"question": "...", "options": ["A","B","C","D"], "correct_index": -1}, ...]
Nếu không có câu hỏi, trả về [].`;

    const ANSWER_PROMPT = `Trích xuất danh sách đáp án từ ảnh bảng đáp án này.
Output JSON: [{"index": 1, "answer": "A"}, {"index": 2, "answer": "C"}...]`;

    function getKeys(keys) {
        const list = keys || JSON.parse(localStorage.getItem('global_gemini_keys') || '[]');
        return Array.isArray(list) ? list.filter(Boolean) : [];
    }

    function getModel(model) {
        return model || localStorage.getItem('default_gemini_module') || 'gemini-2.5-flash';
    }

    function imageParts(dataUrl) {
        const raw = String(dataUrl || '');
        const base64 = raw.includes('base64,') ? raw.split('base64,')[1] : raw;
        const mime = raw.startsWith('data:image/png') ? 'image/png' : 'image/jpeg';
        return { base64, mime };
    }

    function parseVisionJson(text) {
        let t = String(text || '').trim();
        if (t.includes('```json')) t = t.split('```json')[1].split('```')[0].trim();
        else if (t.includes('```')) t = t.replace(/```/g, '').trim();
        const data = JSON.parse(t);
        if (Array.isArray(data)) return data;
        if (data && typeof data === 'object') return [data];
        return [];
    }

    function cleanOption(text) {
        return String(text || '').replace(/^([A-Da-d0-9]+)([\.\)\:\-])\s*/, '').replace(/\s+/g, ' ').trim();
    }

    function mergeSegmentQuestions(rows) {
        const merged = {};
        rows.forEach((q, idx) => {
            if (!q || typeof q !== 'object') return;
            const opts = Array.isArray(q.options) ? q.options.map(cleanOption) : ['', '', '', ''];
            const item = { ...q, options: opts, status: 'done', id: q.id || `${Date.now()}_${idx}` };
            const text = String(q.question || '');
            const m = text.match(/(Câu|Question|Bài)\s*(\d+)/iu);
            if (m) merged[parseInt(m[2], 10)] = item;
            else merged[`x${idx}`] = item;
        });
        const keys = Object.keys(merged).sort((a, b) => {
            const na = parseInt(a, 10); const nb = parseInt(b, 10);
            if (!isNaN(na) && !isNaN(nb)) return na - nb;
            return String(a).localeCompare(String(b));
        });
        const list = keys.map((k) => merged[k]);
        if (global.ExamStitch && ExamStitch.dedupeQuestions) {
            return ExamStitch.dedupeQuestions(list);
        }
        return list;
    }

    function reportGemini(logMode, model, ok, raw, error) {
        if (!global.AiUsageReporter) return;
        const tokens = ok && raw ? AiUsageReporter.extractGeminiTokens(raw) : {};
        AiUsageReporter.report({
            provider: 'gemini_browser',
            module: 'thitructuyen',
            mode: logMode,
            model: model || '',
            ok,
            ...tokens,
            error: ok ? '' : (error || 'Gemini lỗi'),
        });
    }

    async function callGeminiText(prompt, keys, model, timeoutMs, logMode = 'normalize') {
        const apiKeys = getKeys(keys);
        if (!apiKeys.length) throw new Error('Thiếu Gemini API Key. Bấm Cấu hình AI trên trang này để nạp key.');
        const models = [getModel(model)];
        if (!models.includes('gemini-2.5-flash')) models.push('gemini-2.5-flash');

        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), timeoutMs || 90000);
        let lastError = 'Gemini không phản hồi.';

        try {
            for (const currentModel of models) {
                const shuffled = [...apiKeys].sort(() => Math.random() - 0.5);
                for (let i = 0; i < Math.min(shuffled.length, 4); i++) {
                    const key = shuffled[i];
                    try {
                        const res = await fetch(
                            `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(currentModel)}:generateContent?key=${encodeURIComponent(key)}`,
                            {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                signal: controller.signal,
                                body: JSON.stringify({
                                    contents: [{ parts: [{ text: prompt }] }],
                                    generationConfig: { temperature: 0.1, maxOutputTokens: 8192 },
                                }),
                            }
                        );
                        const raw = await res.json().catch(() => ({}));
                        if (!res.ok) {
                            lastError = raw.error?.message || `Gemini HTTP ${res.status}`;
                            if (res.status === 429 || res.status >= 500) continue;
                            throw new Error(lastError);
                        }
                        const parts = raw.candidates?.[0]?.content?.parts || [];
                        let text = '';
                        parts.forEach((p) => { if (p.text) text += p.text; });
                        text = text.trim();
                        if (!text) throw new Error('Gemini trả về rỗng.');
                        reportGemini(logMode, currentModel, true, raw);
                        return text;
                    } catch (err) {
                        if (err.name === 'AbortError') throw new Error('Hết thời gian chờ Gemini (90s). Thử lại.');
                        lastError = err.message || lastError;
                    }
                }
            }
        } finally {
            clearTimeout(timer);
        }
        reportGemini(logMode, getModel(model), false, null, lastError);
        throw new Error(lastError);
    }

    async function callGeminiVision(dataUrl, prompt, keys, model, timeoutMs, logMode = 'vision') {
        const apiKeys = getKeys(keys);
        if (!apiKeys.length) throw new Error('Thiếu Gemini API Key. Bấm Cấu hình AI trên trang này để nạp key.');
        const models = [getModel(model)];
        if (!models.includes('gemini-2.5-flash')) models.push('gemini-2.5-flash');

        const { base64, mime } = imageParts(dataUrl);
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), timeoutMs || 90000);
        let lastError = 'Gemini không phản hồi.';

        try {
            for (const currentModel of models) {
                const shuffled = [...apiKeys].sort(() => Math.random() - 0.5);
                for (let i = 0; i < Math.min(shuffled.length, 4); i++) {
                    const key = shuffled[i];
                    try {
                        const res = await fetch(
                            `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(currentModel)}:generateContent?key=${encodeURIComponent(key)}`,
                            {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                signal: controller.signal,
                                body: JSON.stringify({
                                    contents: [{
                                        parts: [
                                            { text: prompt },
                                            { inline_data: { mime_type: mime, data: base64 } },
                                        ],
                                    }],
                                    generationConfig: { temperature: 0.1, maxOutputTokens: 8192 },
                                }),
                            }
                        );
                        const raw = await res.json().catch(() => ({}));
                        if (!res.ok) {
                            lastError = raw.error?.message || `Gemini HTTP ${res.status}`;
                            if (res.status === 429 || res.status >= 500) continue;
                            throw new Error(lastError);
                        }
                        const parts = raw.candidates?.[0]?.content?.parts || [];
                        let text = '';
                        parts.forEach((p) => { if (p.text) text += p.text; });
                        text = text.trim();
                        if (!text) throw new Error('Gemini trả về rỗng.');
                        reportGemini(logMode, currentModel, true, raw);
                        return text;
                    } catch (err) {
                        if (err.name === 'AbortError') throw new Error('Hết thời gian chờ Gemini (90s). Thử lại.');
                        lastError = err.message || lastError;
                    }
                }
            }
        } finally {
            clearTimeout(timer);
        }
        reportGemini(logMode, getModel(model), false, null, lastError);
        throw new Error(lastError);
    }

    async function normalizeSegment(imageDataUrl, keys, model) {
        const text = await callGeminiVision(imageDataUrl, SEGMENT_PROMPT, keys, model, undefined, 'vision');
        const rows = parseVisionJson(text);
        return { status: 'ok', data: mergeSegmentQuestions(rows), source: 'browser-gemini' };
    }

    async function normalizeSegmentFromText(ocrText, keys, model) {
        const body = String(ocrText || '').trim();
        if (!body) throw new Error('Trang PDF chưa có văn bản OCR.');
        const prompt = `${SEGMENT_PROMPT}

VĂN BẢN ĐÃ QUÉT BẰNG MISTRAL OCR (markdown):
---
${body}
---`;
        const text = await callGeminiText(prompt, keys, model, undefined, 'normalize');
        const rows = parseVisionJson(text);
        return { status: 'ok', data: mergeSegmentQuestions(rows), source: 'mistral-ocr+gemini' };
    }

    async function normalizeManual(imageDataUrl, keys, model) {
        const text = await callGeminiVision(imageDataUrl, MANUAL_PROMPT, keys, model, undefined, 'manual');
        const rows = parseVisionJson(text).map((q, i) => ({
            ...q,
            id: `${Date.now()}_${i}`,
            status: 'manual',
            options: Array.isArray(q.options) ? q.options : ['', '', '', ''],
        }));
        return { status: 'ok', data: rows, source: 'browser-gemini' };
    }

    async function importAnswerSheet(imageDataUrl, keys, model) {
        const text = await callGeminiVision(imageDataUrl, ANSWER_PROMPT, keys, model, undefined, 'answer_sheet');
        const rows = parseVisionJson(text);
        return { status: 'ok', data: rows, source: 'browser-gemini' };
    }

    global.ExamVision = {
        callGeminiVision,
        callGeminiText,
        normalizeSegment,
        normalizeSegmentFromText,
        normalizeManual,
        importAnswerSheet,
    };
})(window);