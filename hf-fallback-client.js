/**
 * GiangBai API client — ưu tiên hosting, fallback HuggingFace khi lỗi.
 */
(function (global) {
    const HF_DEFAULT = 'https://hoangthiencm-giangbai.hf.space';

    function isFallbackEnabled() {
        const v = localStorage.getItem('hf_fallback_enabled');
        if (v === '0' || v === 'false') return false;
        return true;
    }

    function hfUrl() {
        return (localStorage.getItem('hf_fallback_url')
            || localStorage.getItem('omr_backend_url')
            || HF_DEFAULT).replace(/\/$/, '');
    }

    function hostingApiFile(filename) {
        const override = localStorage.getItem('hosting_api_url');
        if (override) return override.replace(/\/$/, '') + '/' + filename;
        const path = window.location.pathname.replace(/[^/]*$/, '');
        return `${window.location.origin}${path}api/${filename}`;
    }

    function examUrl(route) {
        const base = hostingApiFile('exam.php');
        const r = String(route || '').replace(/^\//, '');
        return `${base}?route=${encodeURIComponent(r)}`;
    }

    function examAiUrl(route) {
        const base = hostingApiFile('exam_ai.php');
        const r = String(route || '').replace(/^\//, '');
        return r ? `${base}?route=${encodeURIComponent(r)}` : base;
    }

    function trondeUrl(route) {
        const base = hostingApiFile('tronde.php');
        const r = String(route || '').replace(/^\//, '');
        return r ? `${base}?route=${encodeURIComponent(r)}` : base;
    }

    function hfExamUrl(route) {
        const r = String(route || '').replace(/^\//, '');
        return `${hfUrl()}/api/exam/${r}`;
    }

    function hfTrondeUrl(route) {
        const r = String(route || '').replace(/^\//, '');
        return `${hfUrl()}/${r}`;
    }

    function shouldRetry(status) {
        return !status || status >= 500 || status === 0 || status === 408 || status === 429;
    }

    async function fetchWithFallback(hostUrl, hfUrlFull, init, label) {
        const opts = init || {};
        let hostRes = null;
        try {
            hostRes = await fetch(hostUrl, opts);
            if (!shouldRetry(hostRes.status)) return hostRes;
            console.warn(`[${label || 'API'}] Hosting HTTP ${hostRes.status}, thử HuggingFace...`);
        } catch (err) {
            console.warn(`[${label || 'API'}] Hosting lỗi, thử HuggingFace:`, err.message);
        }

        if (!isFallbackEnabled()) {
            if (hostRes) return hostRes;
            throw new Error('Hosting lỗi và fallback HuggingFace đang tắt.');
        }

        return fetch(hfUrlFull, opts);
    }

    async function fetchJsonWithFallback(hostUrl, hfUrlFull, init, label) {
        const res = await fetchWithFallback(hostUrl, hfUrlFull, init, label);
        const data = await res.json().catch(() => ({}));
        return { res, data, source: res.headers.get('X-Giangbai-Source') || (res.url.includes('hf.space') ? 'hf-fallback' : 'hosting') };
    }

    async function axiosPostWithFallback(axios, hostUrl, hfUrlFull, body, axiosConfig, label) {
        const cfg = Object.assign({ withCredentials: true }, axiosConfig || {});
        try {
            const res = await axios.post(hostUrl, body, cfg);
            return { res, source: res.headers?.['x-giangbai-source'] || 'hosting' };
        } catch (hostErr) {
            const status = hostErr?.response?.status;
            if (!shouldRetry(status) && status !== undefined) throw hostErr;
            console.warn(`[${label || 'API'}] Hosting POST lỗi, thử HuggingFace...`);
            if (!isFallbackEnabled()) throw hostErr;
            const res = await axios.post(hfUrlFull, body, Object.assign({}, cfg, { withCredentials: false }));
            return { res, source: 'hf-fallback' };
        }
    }

    async function axiosGetWithFallback(axios, hostUrl, hfUrlFull, axiosConfig, label) {
        const cfg = Object.assign({ withCredentials: true }, axiosConfig || {});
        try {
            const res = await axios.get(hostUrl, cfg);
            return { res, source: 'hosting' };
        } catch (hostErr) {
            const status = hostErr?.response?.status;
            if (!shouldRetry(status) && status !== undefined) throw hostErr;
            console.warn(`[${label || 'API'}] Hosting GET lỗi, thử HuggingFace...`);
            if (!isFallbackEnabled()) throw hostErr;
            const res = await axios.get(hfUrlFull, Object.assign({}, cfg, { withCredentials: false }));
            return { res, source: 'hf-fallback' };
        }
    }

    async function axiosDeleteWithFallback(axios, hostUrl, hfUrlFull, axiosConfig, label) {
        const cfg = Object.assign({ withCredentials: true }, axiosConfig || {});
        try {
            const res = await axios.delete(hostUrl, cfg);
            return { res, source: 'hosting' };
        } catch (hostErr) {
            const status = hostErr?.response?.status;
            if (!shouldRetry(status) && status !== undefined) throw hostErr;
            if (!isFallbackEnabled()) throw hostErr;
            const res = await axios.delete(hfUrlFull, Object.assign({}, cfg, { withCredentials: false }));
            return { res, source: 'hf-fallback' };
        }
    }

    function openProgressStream(pageId, onMessage, onDone) {
        const hostUrl = examAiUrl(`progress/${pageId}`);
        const hfProgressUrl = hfExamUrl(`progress/${pageId}`);
        let source = new EventSource(hostUrl);
        let usedFallback = false;

        source.onmessage = (e) => {
            const value = parseInt(e.data, 10);
            if (typeof onMessage === 'function') onMessage(value);
            if (value >= 100) {
                source.close();
                if (typeof onDone === 'function') onDone(usedFallback ? 'hf-fallback' : 'hosting');
            }
        };

        source.onerror = () => {
            if (usedFallback || !isFallbackEnabled()) {
                source.close();
                return;
            }
            usedFallback = true;
            source.close();
            source = new EventSource(hfProgressUrl);
            source.onmessage = (e) => {
                const value = parseInt(e.data, 10);
                if (typeof onMessage === 'function') onMessage(value);
                if (value >= 100) {
                    source.close();
                    if (typeof onDone === 'function') onDone('hf-fallback');
                }
            };
        };

        return {
            close() { try { source.close(); } catch (_) { /* noop */ } },
            get usedFallback() { return usedFallback; },
        };
    }

    global.GiangBaiApi = {
        HF_DEFAULT,
        isFallbackEnabled,
        hfUrl,
        hostingApiFile,
        examUrl,
        examAiUrl,
        trondeUrl,
        hfExamUrl,
        hfTrondeUrl,
        fetchWithFallback,
        fetchJsonWithFallback,
        axiosPostWithFallback,
        axiosGetWithFallback,
        axiosDeleteWithFallback,
        openProgressStream,
    };
})(window);