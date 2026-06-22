/**
 * GiangBai API client — chỉ gọi hosting (đã bỏ fallback HuggingFace Space).
 */
(function (global) {
    const HF_DEFAULT = 'https://hoangthiencm-giangbai.hf.space';

    function isFallbackEnabled() {
        return false;
    }

    function setFallbackEnabled(enabled, options) {
        const opts = options || {};
        localStorage.setItem('hf_fallback_enabled', enabled ? 'true' : 'false');
        refreshAllFallbackToggles();
        if (!opts.silent) {
            document.dispatchEvent(new CustomEvent('giangbai-hf-fallback-change', {
                detail: { enabled: !!enabled },
            }));
        }
    }

    function getFallbackStatus() {
        return {
            enabled: false,
            label: 'Chỉ hosting',
            hint: 'API chạy trên hosting — không còn fallback HuggingFace Space.',
            mode: 'hosting-only',
        };
    }

    function toggleFallback() {
        return false;
    }

    function renderToggleHtml() {
        return '';
    }

    function refreshAllFallbackToggles() {}

    function mountFallbackToggle(containerId) {
        const el = typeof containerId === 'string' ? document.getElementById(containerId) : containerId;
        if (el) el.innerHTML = '';
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

    async function fetchWithFallback(hostUrl, _hfUrlFull, init, label) {
        const opts = init || {};
        opts.headers = clientFallbackHeaders(opts.headers);
        try {
            const hostRes = await fetch(hostUrl, opts);
            if (!shouldRetry(hostRes.status)) return hostRes;
            throw new Error(`[${label || 'API'}] Hosting HTTP ${hostRes.status}`);
        } catch (err) {
            throw err instanceof Error ? err : new Error(`[${label || 'API'}] Hosting lỗi.`);
        }
    }

    async function fetchJsonWithFallback(hostUrl, hfUrlFull, init, label) {
        const res = await fetchWithFallback(hostUrl, hfUrlFull, init, label);
        const data = await res.json().catch(() => ({}));
        return { res, data, source: res.headers.get('X-Giangbai-Source') || (res.url.includes('hf.space') ? 'hf-fallback' : 'hosting') };
    }

    function clientFallbackHeaders(extra) {
        const headers = Object.assign({}, extra || {});
        headers['X-Giangbai-Client-Hf-Fallback'] = isFallbackEnabled() ? '1' : '0';
        return headers;
    }

    async function axiosPostWithFallback(axios, hostUrl, _hfUrlFull, body, axiosConfig, _label) {
        const cfg = Object.assign({ withCredentials: true }, axiosConfig || {});
        cfg.headers = clientFallbackHeaders(cfg.headers);
        const res = await axios.post(hostUrl, body, cfg);
        return { res, source: 'hosting' };
    }

    async function axiosGetWithFallback(axios, hostUrl, _hfUrlFull, axiosConfig, _label) {
        const cfg = Object.assign({ withCredentials: true }, axiosConfig || {});
        const res = await axios.get(hostUrl, cfg);
        return { res, source: 'hosting' };
    }

    async function axiosDeleteWithFallback(axios, hostUrl, _hfUrlFull, axiosConfig, _label) {
        const cfg = Object.assign({ withCredentials: true }, axiosConfig || {});
        const res = await axios.delete(hostUrl, cfg);
        return { res, source: 'hosting' };
    }

    function openProgressStream(pageId, onMessage, onDone) {
        const source = new EventSource(examAiUrl(`progress/${pageId}`));
        source.onmessage = (e) => {
            const value = parseInt(e.data, 10);
            if (typeof onMessage === 'function') onMessage(value);
            if (value >= 100) {
                source.close();
                if (typeof onDone === 'function') onDone('hosting');
            }
        };
        source.onerror = () => { source.close(); };
        return {
            close() { try { source.close(); } catch (_) { /* noop */ } },
            get usedFallback() { return false; },
        };
    }

    global.GiangBaiApi = {
        HF_DEFAULT,
        isFallbackEnabled,
        setFallbackEnabled,
        getFallbackStatus,
        toggleFallback,
        mountFallbackToggle,
        refreshAllFallbackToggles,
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
        clientFallbackHeaders,
    };
})(window);