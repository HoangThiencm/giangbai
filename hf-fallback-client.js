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
        const enabled = isFallbackEnabled();
        return {
            enabled,
            label: enabled ? 'HF dự phòng: Bật' : 'Chỉ hosting (test)',
            hint: enabled
                ? 'Hosting lỗi → tự chuyển HuggingFace'
                : 'Đang test hosting — không qua HuggingFace',
            mode: enabled ? 'hybrid' : 'hosting-only',
        };
    }

    function toggleFallback() {
        const next = !isFallbackEnabled();
        const msg = next
            ? 'Bật fallback HuggingFace?\n\nKhi hosting lỗi, hệ thống tự chuyển sang Space HF.'
            : 'Tắt fallback HuggingFace?\n\nChế độ kiểm tra: CHỈ hosting. Nếu hosting lỗi sẽ báo lỗi, không chuyển sang HF — dùng để xem hosting có đủ tốt không.';
        if (!confirm(msg)) return false;
        setFallbackEnabled(next);
        return true;
    }

    function renderToggleHtml(variant) {
        const st = getFallbackStatus();
        const on = st.enabled;
        const compact = variant === 'compact';
        const navbar = variant === 'navbar';

        const trackOn = 'bg-violet-600';
        const trackOff = 'bg-emerald-600';
        const knob = on ? 'translate-x-5' : 'translate-x-0.5';

        if (navbar) {
            return `
                <button type="button" data-gb-hf-toggle data-gb-hf-variant="navbar"
                    title="${st.hint}"
                    class="inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-bold shadow-sm transition ${on ? 'border-violet-200 bg-violet-50 text-violet-800 hover:bg-violet-100' : 'border-emerald-200 bg-emerald-50 text-emerald-800 hover:bg-emerald-100'}">
                    <span class="relative inline-flex h-5 w-9 shrink-0 items-center rounded-full ${on ? trackOn : trackOff}">
                        <span class="inline-block h-4 w-4 transform rounded-full bg-white shadow transition ${knob}"></span>
                    </span>
                    <span data-gb-hf-label>${st.label}</span>
                </button>`;
        }

        return `
            <div data-gb-hf-toggle-wrap data-gb-hf-variant="${compact ? 'compact' : 'bar'}"
                class="${compact ? 'flex flex-wrap items-center justify-center gap-2 border-b border-slate-200 bg-slate-50 px-3 py-2 text-xs' : 'mb-4 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm shadow-sm'}">
                <div class="min-w-0">
                    <p class="font-bold text-slate-800 ${compact ? 'text-xs' : 'text-sm'}">
                        <i class="fas fa-flask ${on ? 'text-violet-500' : 'text-emerald-500'}"></i>
                        Kiểm tra hosting không qua HuggingFace
                    </p>
                    <p data-gb-hf-hint class="text-slate-500 ${compact ? 'text-[11px]' : 'text-xs'} mt-0.5">${st.hint}</p>
                </div>
                <button type="button" data-gb-hf-toggle
                    class="inline-flex shrink-0 items-center gap-2 rounded-full border px-3 py-1.5 font-bold transition ${on ? 'border-violet-200 bg-violet-50 text-violet-800' : 'border-emerald-200 bg-emerald-50 text-emerald-800'}">
                    <span class="relative inline-flex h-5 w-9 items-center rounded-full ${on ? trackOn : trackOff}">
                        <span class="inline-block h-4 w-4 transform rounded-full bg-white shadow transition ${knob}"></span>
                    </span>
                    <span data-gb-hf-label>${st.label}</span>
                </button>
            </div>`;
    }

    function refreshAllFallbackToggles() {
        document.querySelectorAll('[data-gb-hf-toggle-root]').forEach((root) => {
            const variant = root.getAttribute('data-gb-hf-variant') || 'bar';
            root.innerHTML = renderToggleHtml(variant);
        });
    }

    function mountFallbackToggle(containerId, options) {
        const opts = options || {};
        const el = typeof containerId === 'string' ? document.getElementById(containerId) : containerId;
        if (!el) return;
        const variant = opts.variant || (opts.compact ? 'compact' : 'bar');
        el.setAttribute('data-gb-hf-toggle-root', '1');
        el.setAttribute('data-gb-hf-variant', variant);
        el.innerHTML = renderToggleHtml(variant);
    }

    if (!global.__gbHfToggleBound) {
        global.__gbHfToggleBound = true;
        document.addEventListener('click', (e) => {
            const btn = e.target && e.target.closest ? e.target.closest('[data-gb-hf-toggle]') : null;
            if (!btn) return;
            e.preventDefault();
            toggleFallback();
        });
        document.addEventListener('giangbai-hf-fallback-change', () => refreshAllFallbackToggles());
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
        opts.headers = clientFallbackHeaders(opts.headers);
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

    function clientFallbackHeaders(extra) {
        const headers = Object.assign({}, extra || {});
        headers['X-Giangbai-Client-Hf-Fallback'] = isFallbackEnabled() ? '1' : '0';
        return headers;
    }

    async function axiosPostWithFallback(axios, hostUrl, hfUrlFull, body, axiosConfig, label) {
        const cfg = Object.assign({ withCredentials: true }, axiosConfig || {});
        cfg.headers = clientFallbackHeaders(cfg.headers);
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