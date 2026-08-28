/**
 * Mistral OCR — quét PDF/ảnh ra văn bản (markdown) cực nhanh.
 * https://docs.mistral.ai/api/endpoint/ocr
 */
(function (global) {
    const API = 'https://api.mistral.ai/v1/ocr';
    const OCR_MODEL_FALLBACK = 'mistral-ocr-latest';

    function isOcrEnabled() {
        if (global.AiDesignConfig && typeof AiDesignConfig.isMistralEnabled === 'function') {
            return AiDesignConfig.isMistralEnabled();
        }
        try {
            return localStorage.getItem('global_mistral_enabled') !== 'false';
        } catch {
            return true;
        }
    }

    function sanitizeOcrModel(model) {
        const value = (model || '').trim();
        if (/^mistral-ocr/i.test(value)) return value;
        return OCR_MODEL_FALLBACK;
    }

    function getKeys(keys) {
        if (keys && keys.length) return keys.filter(Boolean);
        if (global.AiDesignConfig) return AiDesignConfig.getMistralKeys();
        try {
            return JSON.parse(localStorage.getItem('global_mistral_keys') || '[]').filter(Boolean);
        } catch {
            return [];
        }
    }

    function getModel(model) {
        const raw = model || (global.AiDesignConfig ? AiDesignConfig.getMistralModel() : null) || OCR_MODEL_FALLBACK;
        return sanitizeOcrModel(raw);
    }

    function toDataUrl(fileOrBuffer, mime) {
        if (typeof fileOrBuffer === 'string') return fileOrBuffer;
        return null;
    }

    async function fileToBase64(file) {
        const buf = await file.arrayBuffer();
        const bytes = new Uint8Array(buf);
        let binary = '';
        const chunk = 0x8000;
        for (let i = 0; i < bytes.length; i += chunk) {
            binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
        }
        return btoa(binary);
    }

    function reportMistral(model, ok, error, moduleName) {
        if (!global.AiUsageReporter) return;
        AiUsageReporter.report({
            provider: 'mistral_ocr',
            module: moduleName || 'thitructuyen',
            mode: 'ocr',
            model: model || '',
            ok,
            error: ok ? '' : (error || 'Mistral OCR lỗi'),
        });
    }

    function normalizeOptions(model, options) {
        if (model && typeof model === 'object' && !options) {
            return { model: undefined, options: model };
        }
        return { model, options: options && typeof options === 'object' ? options : {} };
    }

    function buildDocumentPayload(documentUrl) {
        if (/^data:image\//i.test(documentUrl) || /\.(png|jpe?g|webp|gif)(\?|$)/i.test(documentUrl)) {
            return { type: 'image_url', image_url: documentUrl };
        }
        return { type: 'document_url', document_url: documentUrl };
    }

    function isReady() {
        return isOcrEnabled() && getKeys().length > 0;
    }

    async function ocrDocument(documentUrl, keys, model, options) {
        const normalized = normalizeOptions(model, options);
        const opts = normalized.options;
        const moduleName = opts.module || 'thitructuyen';
        if (!isOcrEnabled()) throw new Error('Mistral OCR đang tắt trong Admin. Chỉ bật khi cần quét PDF.');
        const apiKeys = getKeys(keys);
        if (!apiKeys.length) throw new Error('Thiếu Mistral API Key. Bấm Cấu hình AI trên trang này.');
        const currentModel = getModel(normalized.model);
        let lastError = 'Mistral OCR không phản hồi.';

        const payload = {
            model: currentModel,
            document: buildDocumentPayload(documentUrl),
            include_image_base64: false,
        };
        if (Array.isArray(opts.pages) && opts.pages.length) {
            payload.pages = opts.pages.map(Number).filter((n) => Number.isInteger(n) && n >= 0);
        }

        for (let i = 0; i < Math.min(apiKeys.length, 4); i++) {
            const key = apiKeys[i];
            const controller = new AbortController();
            const timer = setTimeout(() => controller.abort(), 25000);
            try {
                const res = await fetch(API, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${key}`,
                    },
                    body: JSON.stringify(payload),
                    signal: controller.signal
                });
                clearTimeout(timer);
                const raw = await res.json().catch(() => ({}));
                if (!res.ok) {
                    lastError = raw.message || raw.error?.message || `Mistral HTTP ${res.status}`;
                    if (res.status === 429 || res.status >= 500) continue;
                    throw new Error(lastError);
                }
                reportMistral(currentModel, true, '', moduleName);
                return { status: 'ok', data: raw, source: 'mistral-ocr' };
            } catch (err) {
                clearTimeout(timer);
                if (err.name === 'AbortError') {
                    lastError = 'Mistral OCR hết thời gian chờ (Timeout 25s). Vui lòng thử lại.';
                } else {
                    lastError = err.message || lastError;
                }
            }
        }
        reportMistral(getModel(normalized.model), false, lastError, moduleName);
        throw new Error(lastError);
    }

    async function ocrPdfFile(file, keys, model, options) {
        const mime = file.type || 'application/pdf';
        const b64 = await fileToBase64(file);
        const documentUrl = `data:${mime};base64,${b64}`;
        const result = await ocrDocument(documentUrl, keys, model, options);
        const ocrPages = result.data?.pages || [];
        const pages = ocrPages.map((p, idx) => ({
            id: `mistral-${Date.now()}-${idx + 1}`,
            page_index: idx + 1,
            image_data: null,
            ocr_text: p.markdown || p.text || '',
            status: 'pending',
            q_count: 0,
        }));
        return { status: 'ok', pages, raw: result.data, source: 'mistral-ocr' };
    }

    async function ocrImageDataUrl(dataUrl, keys, model, options) {
        const documentUrl = dataUrl.startsWith('data:') ? dataUrl : `data:image/jpeg;base64,${dataUrl}`;
        const result = await ocrDocument(documentUrl, keys, model, options);
        const ocrPages = result.data?.pages || [];
        const text = ocrPages.map((p) => p.markdown || p.text || '').join('\n\n');
        return { status: 'ok', text, raw: result.data, source: 'mistral-ocr' };
    }

    global.MistralOcr = {
        ocrPdfFile,
        ocrImageDataUrl,
        ocrDocument,
        isReady,
    };
})(window);