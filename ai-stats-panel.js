(function () {
    function escapeHtml(value) {
        return String(value ?? '').replace(/[&<>"']/g, ch => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        }[ch]));
    }

    function formatNumber(value, digits = 0) {
        const num = Number(value);
        if (!Number.isFinite(num)) return '—';
        return digits > 0
            ? num.toLocaleString('vi-VN', { maximumFractionDigits: digits, minimumFractionDigits: digits })
            : num.toLocaleString('vi-VN');
    }

    function formatUsd(value) {
        const num = Number(value);
        if (!Number.isFinite(num)) return '—';
        return '$' + num.toLocaleString('vi-VN', { maximumFractionDigits: 2, minimumFractionDigits: 2 });
    }

    function providerLabel(id) {
        return ({
            cloudflare_workers_ai: 'Cloudflare Workers AI',
            gemini: 'Gemini',
            shopaikey: 'ShopAIKey / DeepSeek',
        })[id] || id;
    }

    function renderAiStats(data, ids = {}) {
        const loadingId = ids.loading || 'aiStatsLoading';
        const contentId = ids.content || 'aiStatsContent';
        const loading = document.getElementById(loadingId);
        const content = document.getElementById(contentId);
        if (!loading || !content) return;

        const cf = data.providers?.cloudflare || {};
        const gemini = data.providers?.gemini || {};
        const shop = data.providers?.shopaikey || {};
        const internal = data.internal || {};
        const summary = internal.summary || {};
        const providers = summary.providers || {};
        const byMode = summary.by_mode || {};
        const history = Array.isArray(data.history) ? data.history : [];
        const recent = Array.isArray(internal.recent) ? internal.recent : [];
        const generatedAt = data.generated_at || '';

        const providerCards = ['cloudflare_workers_ai', 'gemini', 'shopaikey'].map(id => {
            const bucket = providers[id] || {};
            let mainValue = bucket.success || 0;
            let subtitle = 'thành công hôm nay (log lộ trình)';
            let detailLine = `Gọi log: ${formatNumber(bucket.calls || 0)} · Lỗi log: ${formatNumber(bucket.error || 0)}`;

            if (id === 'cloudflare_workers_ai') {
                const workerRequests = bucket.worker_requests_today ?? (cf.available ? cf.requests_today : null);
                const workerSuccess = bucket.worker_success_today ?? (cf.available ? cf.success_today : null);
                if (workerRequests != null) {
                    mainValue = workerRequests;
                    subtitle = 'lượt gọi Worker (Cloudflare Dashboard)';
                    detailLine = `Thành công CF: ${formatNumber(workerSuccess ?? 0)} · Log lộ trình: ${formatNumber(bucket.success || cf.requests_today_internal || 0)}`;
                }
            }

            const tokenPart = bucket.total_tokens ? ` · Token: ${formatNumber(bucket.total_tokens)}` : '';
            const usdPart = bucket.estimated_usd ? ` · ~${formatUsd(bucket.estimated_usd)}` : '';

            return `
                <div class="rounded-xl border border-slate-200 bg-slate-50 p-4">
                    <div class="text-xs font-bold uppercase tracking-wide text-slate-500">${escapeHtml(providerLabel(id))}</div>
                    <div class="mt-2 text-2xl font-black text-slate-900">${formatNumber(mainValue)}</div>
                    <div class="text-xs text-slate-500">${subtitle}</div>
                    <div class="mt-2 text-xs text-slate-600">${detailLine}${tokenPart}${usdPart}</div>
                </div>
            `;
        }).join('');

        const historyRows = history.map(row => {
            const cfDay = row.providers?.cloudflare_workers_ai?.success || 0;
            const gemDay = row.providers?.gemini?.success || 0;
            const shopDay = row.providers?.shopaikey?.success || 0;
            return `<tr class="border-t border-slate-100"><td class="px-3 py-2 text-sm font-semibold">${escapeHtml(row.date)}</td><td class="px-3 py-2 text-sm">${formatNumber(row.total_success || 0)}</td><td class="px-3 py-2 text-sm">${formatNumber(cfDay)}</td><td class="px-3 py-2 text-sm">${formatNumber(gemDay)}</td><td class="px-3 py-2 text-sm">${formatNumber(shopDay)}</td></tr>`;
        }).join('');

        const recentRows = recent.slice(0, 15).map(item => `
            <tr class="border-t border-slate-100">
                <td class="px-3 py-2 text-xs text-slate-500">${escapeHtml((item.ts || '').replace('T', ' ').slice(0, 19))}</td>
                <td class="px-3 py-2 text-sm">${escapeHtml(providerLabel(item.provider))}</td>
                <td class="px-3 py-2 text-sm">${escapeHtml(item.mode || '')}</td>
                <td class="px-3 py-2 text-sm">${item.ok ? '<span class="text-emerald-700 font-semibold">OK</span>' : '<span class="text-rose-700 font-semibold">Lỗi</span>'}${item.fallback ? ' <span class="text-amber-700 text-xs">(fallback)</span>' : ''}</td>
                <td class="px-3 py-2 text-xs text-slate-600">${escapeHtml(item.model || '')}</td>
            </tr>
        `).join('');

        content.innerHTML = `
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="rounded-xl border border-orange-200 bg-orange-50 p-4">
                    <div class="flex items-center justify-between gap-2">
                        <div class="text-sm font-bold text-orange-900">Cloudflare Workers AI</div>
                        ${cf.available ? '<span class="text-xs font-semibold text-emerald-700">GraphQL OK</span>' : '<span class="text-xs font-semibold text-amber-700">GraphQL chưa có</span>'}
                    </div>
                    <div class="mt-3 grid grid-cols-2 gap-3 text-sm">
                        <div><div class="text-xs text-orange-800">Worker hôm nay (CF)</div><div class="text-xl font-black text-orange-950">${cf.available ? formatNumber(cf.requests_today) : '—'}</div></div>
                        <div><div class="text-xs text-orange-800">Lộ trình hôm nay (log)</div><div class="text-xl font-black text-orange-950">${formatNumber(cf.requests_today_internal || 0)}</div></div>
                    </div>
                    <div class="mt-2 text-xs text-orange-800">Model: <code>${escapeHtml(data.config?.cloudflare_model || '')}</code>${cf.script_name ? ` · Script: <code>${escapeHtml(cf.script_name)}</code>` : ''}</div>
                    <div class="mt-2 text-xs text-orange-700">${escapeHtml(cf.message || '')}</div>
                    ${cf.dashboard_url ? `<a href="${escapeHtml(cf.dashboard_url)}" target="_blank" rel="noopener" class="mt-2 inline-flex text-xs font-bold text-orange-900 underline">Mở Cloudflare Dashboard</a>` : ''}
                </div>
                <div class="rounded-xl border border-emerald-200 bg-emerald-50 p-4">
                    <div class="text-sm font-bold text-emerald-900">Google Gemini (fallback)</div>
                    <div class="mt-3 text-3xl font-black text-emerald-950">${formatNumber(gemini.requests_today_internal || 0)}</div>
                    <div class="text-xs text-emerald-800">lượt fallback thành công hôm nay</div>
                    <div class="mt-2 text-xs text-emerald-800">${formatNumber(gemini.keys_count || 0)} key · Model <code>${escapeHtml(gemini.model || '')}</code></div>
                    <div class="mt-2 text-xs text-emerald-700">${escapeHtml(gemini.message || '')}</div>
                    ${gemini.dashboard_url ? `<a href="${escapeHtml(gemini.dashboard_url)}" target="_blank" rel="noopener" class="mt-2 inline-flex text-xs font-bold text-emerald-900 underline">Mở Google AI Studio</a>` : ''}
                </div>
                <div class="rounded-xl border border-indigo-200 bg-indigo-50 p-4">
                    <div class="flex items-center justify-between gap-2">
                        <div class="text-sm font-bold text-indigo-900">ShopAIKey / DeepSeek</div>
                        ${shop.available ? '<span class="text-xs font-semibold text-emerald-700">API OK</span>' : '<span class="text-xs font-semibold text-amber-700">API chưa có</span>'}
                    </div>
                    <div class="mt-3 grid grid-cols-3 gap-2 text-center">
                        <div><div class="text-xs text-indigo-800">Đã dùng</div><div class="text-lg font-black text-indigo-950">${shop.used_usd != null ? formatUsd(shop.used_usd) : '—'}</div></div>
                        <div><div class="text-xs text-indigo-800">Còn lại</div><div class="text-lg font-black text-indigo-950">${shop.remaining_usd != null ? formatUsd(shop.remaining_usd) : '—'}</div></div>
                        <div><div class="text-xs text-indigo-800">Hôm nay (log)</div><div class="text-lg font-black text-indigo-950">${formatNumber(shop.requests_today_internal || 0)}</div></div>
                    </div>
                    <div class="mt-2 text-xs text-indigo-800">Model: <code>${escapeHtml(data.config?.shopaikey_model || '')}</code>${shop.estimated_usd_today_internal ? ` · Ước tính hôm nay: ${formatUsd(shop.estimated_usd_today_internal)}` : ''}</div>
                    <div class="mt-2 text-xs text-indigo-700">${escapeHtml(shop.message || '')}</div>
                    ${shop.dashboard_url ? `<a href="${escapeHtml(shop.dashboard_url)}" target="_blank" rel="noopener" class="mt-2 inline-flex text-xs font-bold text-indigo-900 underline">Mở ShopAIKey Dashboard</a>` : ''}
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="rounded-xl border border-sky-200 bg-sky-50 p-4 md:col-span-1">
                    <div class="text-xs font-bold uppercase text-sky-700">Hôm nay (${escapeHtml(data.today || '')})</div>
                    <div class="mt-2 text-3xl font-black text-sky-950">${formatNumber(summary.total_success || 0)}</div>
                    <div class="text-xs text-sky-800">phản hồi AI thành công (lộ trình)</div>
                    <div class="mt-3 text-xs text-sky-800">Giải thích: <strong>${formatNumber(byMode.explain || 0)}</strong> · Chat: <strong>${formatNumber(byMode.chat || 0)}</strong></div>
                </div>
                <div class="md:col-span-3">
                    <div class="mb-2 text-xs font-semibold text-slate-500">Chi tiết theo provider · Cloudflare lấy từ Dashboard, Gemini/ShopAIKey từ log <code>api/ai_explain.php</code></div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">${providerCards}</div>
                </div>
            </div>

            <div>
                <h4 class="text-sm font-bold text-slate-700 mb-2">14 ngày gần nhất (log nội bộ)</h4>
                <div class="overflow-x-auto rounded-lg border border-slate-200">
                    <table class="min-w-full text-left">
                        <thead class="bg-slate-50 text-xs font-bold uppercase text-slate-500">
                            <tr><th class="px-3 py-2">Ngày</th><th class="px-3 py-2">Thành công</th><th class="px-3 py-2">CF</th><th class="px-3 py-2">Gemini</th><th class="px-3 py-2">ShopAIKey</th></tr>
                        </thead>
                        <tbody>${historyRows || '<tr><td colspan="5" class="px-3 py-4 text-sm text-slate-400">Chưa có dữ liệu.</td></tr>'}</tbody>
                    </table>
                </div>
            </div>

            <div>
                <h4 class="text-sm font-bold text-slate-700 mb-2">Lượt gọi gần đây</h4>
                <div class="overflow-x-auto rounded-lg border border-slate-200">
                    <table class="min-w-full text-left">
                        <thead class="bg-slate-50 text-xs font-bold uppercase text-slate-500">
                            <tr><th class="px-3 py-2">Thời gian</th><th class="px-3 py-2">Provider</th><th class="px-3 py-2">Mode</th><th class="px-3 py-2">Kết quả</th><th class="px-3 py-2">Model</th></tr>
                        </thead>
                        <tbody>${recentRows || '<tr><td colspan="5" class="px-3 py-4 text-sm text-slate-400">Chưa có lượt gọi nào.</td></tr>'}</tbody>
                    </table>
                </div>
            </div>

            <div class="rounded-lg border border-amber-100 bg-amber-50 px-4 py-3 text-xs leading-6 text-amber-900">
                <div class="font-bold mb-1">Lưu ý</div>
                <ul class="list-disc pl-5 space-y-1">
                    ${(data.notes || []).map(note => `<li>${escapeHtml(note)}</li>`).join('')}
                    <li>${escapeHtml(internal.note || '')}</li>
                </ul>
                <div class="mt-2 text-slate-600">Cập nhật lúc: ${escapeHtml(generatedAt)} · Múi giờ: ${escapeHtml(data.timezone || '')}</div>
            </div>
        `;

        loading.classList.add('hidden');
        content.classList.remove('hidden');
    }

    function renderAiStatsCompact(data, mountEl) {
        const mount = typeof mountEl === 'string' ? document.getElementById(mountEl) : mountEl;
        if (!mount) return;

        const cf = data.providers?.cloudflare || {};
        const gemini = data.providers?.gemini || {};
        const shop = data.providers?.shopaikey || {};
        const summary = data.internal?.summary || {};
        const providers = summary.providers || {};
        const cfBucket = providers.cloudflare_workers_ai || {};
        const cfWorker = cfBucket.worker_requests_today ?? (cf.available ? cf.requests_today : null);
        const cfLog = cfBucket.success || cf.requests_today_internal || 0;
        const gemLog = gemini.requests_today_internal || providers.gemini?.success || 0;
        const shopLog = shop.requests_today_internal || providers.shopaikey?.success || 0;

        mount.innerHTML = `
            <div class="grid grid-cols-2 gap-3 lg:grid-cols-4">
                <div class="rounded-xl border border-sky-200 bg-sky-50 p-3">
                    <div class="text-[10px] font-bold uppercase text-sky-700">Lộ trình hôm nay</div>
                    <div class="mt-1 text-2xl font-black text-sky-950">${formatNumber(summary.total_success || 0)}</div>
                    <div class="text-[11px] text-sky-800">phản hồi thành công</div>
                </div>
                <div class="rounded-xl border border-orange-200 bg-orange-50 p-3">
                    <div class="text-[10px] font-bold uppercase text-orange-800">Cloudflare Worker</div>
                    <div class="mt-1 text-2xl font-black text-orange-950">${cfWorker != null ? formatNumber(cfWorker) : '—'}</div>
                    <div class="text-[11px] text-orange-800">log lộ trình: ${formatNumber(cfLog)}</div>
                </div>
                <div class="rounded-xl border border-emerald-200 bg-emerald-50 p-3">
                    <div class="text-[10px] font-bold uppercase text-emerald-800">Gemini fallback</div>
                    <div class="mt-1 text-2xl font-black text-emerald-950">${formatNumber(gemLog)}</div>
                    <div class="text-[11px] text-emerald-800">lượt hôm nay</div>
                </div>
                <div class="rounded-xl border border-indigo-200 bg-indigo-50 p-3">
                    <div class="text-[10px] font-bold uppercase text-indigo-800">ShopAIKey</div>
                    <div class="mt-1 text-2xl font-black text-indigo-950">${formatNumber(shopLog)}</div>
                    <div class="text-[11px] text-indigo-800">${shop.remaining_usd != null ? `còn ${formatUsd(shop.remaining_usd)}` : 'log hôm nay'}</div>
                </div>
            </div>
        `;
        mount.classList.remove('hidden');
    }

    async function loadAiStats(force = false, options = {}) {
        const ids = options.ids || {};
        const loadingId = ids.loading || 'aiStatsLoading';
        const contentId = ids.content || 'aiStatsContent';
        const btnId = ids.refreshBtn || 'aiStatsRefreshBtn';
        const adminKey = options.adminKey || '';
        const useSession = options.useSession !== false && !adminKey;
        const isCompact = !!options.compact;
        const compactMountId = options.compactMount || 'teacherAiStatsMount';

        if (!adminKey && !useSession) return;

        const loading = document.getElementById(loadingId);
        const content = isCompact ? null : document.getElementById(contentId);
        const compactMount = isCompact ? document.getElementById(compactMountId) : null;
        const btn = document.getElementById(btnId);
        if (!loading || (!isCompact && !content) || (isCompact && !compactMount)) return;

        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Đang tải...';
        }
        loading.classList.remove('hidden');
        loading.innerHTML = '<i class="fas fa-circle-notch fa-spin mr-2 text-sky-600"></i>Đang tải thống kê AI...';
        if (content) content.classList.add('hidden');
        if (compactMount) compactMount.classList.add('hidden');

        try {
            const headers = {};
            if (adminKey) headers['X-Admin-Key'] = adminKey;
            const res = await fetch('api/ai_stats.php', {
                headers,
                credentials: adminKey ? 'same-origin' : 'include',
                cache: force ? 'no-store' : 'default'
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Không tải được thống kê AI.');
            if (isCompact) {
                renderAiStatsCompact(data, compactMount);
                loading.classList.add('hidden');
            } else {
                renderAiStats(data, ids);
            }
        } catch (err) {
            loading.innerHTML = `<span class="text-rose-700"><i class="fas fa-triangle-exclamation mr-2"></i>${escapeHtml(err.message || 'Không tải được thống kê AI.')}</span>`;
            loading.classList.remove('hidden');
            if (content) content.classList.add('hidden');
            if (compactMount) compactMount.classList.add('hidden');
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-rotate-right mr-2"></i>Tải lại';
            }
        }
    }

    window.AiStatsPanel = {
        render: renderAiStats,
        renderCompact: renderAiStatsCompact,
        load: loadAiStats,
    };
    window.loadAiStats = loadAiStats;
})();