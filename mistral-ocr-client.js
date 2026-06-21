/**
 * Mistral OCR — quét PDF/ảnh ra văn bản (markdown) cực nhanh.
 * https://docs.mistral.ai/api/endpoint/ocr
 */
(function (global) {
    const API = 'https://api.mistral.ai/v1/ocr';

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
        return model || (global.AiDesignConfig ? AiDesignConfig.getMistralModel() : null) || 'mistral-ocr-latest';
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

    async function ocrDocument(documentUrl, keys, model) {
        const apiKeys = getKeys(keys);
        if (!apiKeys.length) throw new Error('Thiếu Mistral API Key. Bấm Cấu hình AI trên trang này.');
        const currentModel = getModel(model);
        let lastError = 'Mistral OCR không phản hồi.';

        for (let i = 0; i < Math.min(apiKeys.length, 4); i++) {
            const key = apiKeys[i];
            try {
                const res = await fetch(API, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${key}`,
                    },
                    body: JSON.stringify({
                        model: currentModel,
                        document: {
                            type: 'document_url',
                            document_url: documentUrl,
                        },
                    }),
                });
                const raw = await res.json().catch(() => ({}));
                if (!res.ok) {
                    lastError = raw.message || raw.error?.message || `Mistral HTTP ${res.status}`;
                    if (res.status === 429 || res.status >= 500) continue;
                    throw new Error(lastError);
                }
                return { status: 'ok', data: raw, source: 'mistral-ocr' };
            } catch (err) {
                lastError = err.message || lastError;
            }
        }
        throw new Error(lastError);
    }

    async function ocrPdfFile(file, keys, model) {
        const mime = file.type || 'application/pdf';
        const b64 = await fileToBase64(file);
        const documentUrl = `data:${mime};base64,${b64}`;
        const result = await ocrDocument(documentUrl, keys, model);
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

    async function ocrImageDataUrl(dataUrl, keys, model) {
        const documentUrl = dataUrl.startsWith('data:') ? dataUrl : `data:image/jpeg;base64,${dataUrl}`;
        const result = await ocrDocument(documentUrl, keys, model);
        const ocrPages = result.data?.pages || [];
        const text = ocrPages.map((p) => p.markdown || p.text || '').join('\n\n');
        return { status: 'ok', text, raw: result.data, source: 'mistral-ocr' };
    }

    global.MistralOcr = {
        ocrPdfFile,
        ocrImageDataUrl,
        ocrDocument,
    };
})(window);