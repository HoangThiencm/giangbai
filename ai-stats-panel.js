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
            gemini: 'Gemini (fallback server)',
            gemini_browser: 'Gemini (trình duyệt)',
            mistral_ocr: 'Mistral OCR',
            shopaikey: 'ShopAIKey / DeepSeek',
            light_ai: 'Light AI (nội dung bài)',
            light_ai_math: 'Light AI (phương trình)',
        })[id] || id;
    }

    function moduleLabel(id) {
        return ({
            lotrinh: 'Lộ trình học',
            thitructuyen: 'Thi trực tuyến',
            vanban: 'Quản lý văn bản',
            matrande: 'Ma trận đề',
            kttx: 'KTTX',
            other: 'Khác',
        })[id] || id;
    }

    function moduleBucket(byModule, id) {
        return (byModule && byModule[id]) || { calls: 0, success: 0, error: 0, providers: {} };
    }

    function sumByMode(byMode) {
        return Object.values(byMode || {}).reduce((sum, value) => sum + (Number(value) || 0), 0);
    }

    function resolveTotalSuccess(summary) {
        const providerTotal = Number(summary?.total_success) || 0;
        const modeTotal = sumByMode(summary?.by_mode || {});
        return Math.max(providerTotal, modeTotal);
    }

    function providerInModule(mod, providerId) {
        const bucket = mod.providers?.[providerId];
        return bucket ? (bucket.success || 0) : 0;
    }

    function smartQuotaLevelMeta(level) {
        return ({
            disabled: { label: 'Tắt', border: 'border-slate-200', bg: 'bg-slate-50', text: 'text-slate-800', bar: 'bg-slate-400', icon: 'fa-circle-info' },
            normal: { label: 'Ổn định', border: 'border-emerald-200', bg: 'bg-emerald-50', text: 'text-emerald-900', bar: 'bg-emerald-500', icon: 'fa-circle-check' },
            warn: { label: 'Cảnh báo vàng', border: 'border-amber-300', bg: 'bg-amber-50', text: 'text-amber-950', bar: 'bg-amber-500', icon: 'fa-triangle-exclamation' },
            critical: { label: 'Sắp hết', border: 'border-orange-300', bg: 'bg-orange-50', text: 'text-orange-950', bar: 'bg-orange-500', icon: 'fa-circle-exclamation' },
            exhausted: { label: 'Hết quota', border: 'border-rose-300', bg: 'bg-rose-50', text: 'text-rose-950', bar: 'bg-rose-500', icon: 'fa-ban' },
        })[level] || { label: level, border: 'border-slate-200', bg: 'bg-slate-50', text: 'text-slate-800', bar: 'bg-slate-400', icon: 'fa-robot' };
    }

    function renderSmartQuotaPanel(sq, options = {}) {
        if (!sq || typeof sq !== 'object') return '';
        const compact = !!options.compact;
        const meta = smartQuotaLevelMeta(sq.level || 'normal');
        const usedPct = Math.max(0, Math.min(100, Number(sq.used_pct) || 0));
        const remainingPct = Math.max(0, Math.min(100, Number(sq.remaining_pct) || 0));
        const modeLabel = sq.exhausted_mode === 'block' ? 'Tắt AI lộ trình' : 'Tự chuyển Gemini / ShopAIKey';
        const notice = escapeHtml(sq.teacher_notice || sq.message || '');
        const resetsAt = escapeHtml(sq.resets_at_utc || '00:00 UTC');
        const statsLink = options.hideLink ? '' : `
            <a href="theodoi-ai.html" class="inline-flex items-center gap-1 text-xs font-bold underline ${meta.text} opacity-90 hover:opacity-100">
                <i class="fas fa-chart-line"></i> Chi tiết
            </a>
        `;

        if (compact) {
            if (!sq.enabled || sq.level === 'normal' || sq.level === 'disabled') return '';
            return `
                <div class="rounded-xl border ${meta.border} ${meta.bg} px-3 py-2.5 text-xs ${meta.text}">
                    <div class="flex flex-wrap items-center justify-between gap-2">
                        <span class="font-bold"><i class="fas ${meta.icon} mr-1"></i>Smart Quota · ${meta.label}</span>
                        <span>Còn ${formatNumber(remainingPct, 1)}% · ${formatNumber(sq.neurons_remaining)}/${formatNumber(sq.daily_limit)} Neurons</span>
                    </div>
                    ${notice ? `<p class="mt-1 leading-5">${notice}</p>` : ''}
                </div>
            `;
        }

        return `
            <section class="rounded-xl border ${meta.border} ${meta.bg} p-4">
                <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                        <div class="flex flex-wrap items-center gap-2">
                            <h3 class="text-sm font-bold ${meta.text}"><i class="fas ${meta.icon} mr-1"></i>Smart Quota · Cloudflare Neurons</h3>
                            <span class="inline-flex rounded-full border border-white/70 bg-white/80 px-2 py-0.5 text-[11px] font-bold uppercase tracking-wide ${meta.text}">${escapeHtml(meta.label)}</span>
                            ${sq.enabled ? '' : '<span class="text-[11px] font-semibold text-slate-500">(đang tắt)</span>'}
                        </div>
                        <p class="mt-2 text-sm leading-6 ${meta.text}">${notice || 'Áp dụng Cloudflare cho lộ trình học + quản lý văn bản. Thi trực tuyến dùng Mistral + Gemini riêng.'}</p>
                        <p class="mt-1 text-xs ${meta.text} opacity-80">Khi hết: <strong>${escapeHtml(modeLabel)}</strong> · Reset ${resetsAt}</p>
                    </div>
                    <div class="shrink-0 text-right text-xs ${meta.text}">
                        <div class="font-bold">Còn ${formatNumber(remainingPct, 1)}%</div>
                        <div>${formatNumber(sq.neurons_remaining)} / ${formatNumber(sq.daily_limit)} Neurons</div>
                        ${statsLink}
                    </div>
                </div>
                <div class="mt-3">
                    <div class="mb-1 flex justify-between text-[11px] font-semibold ${meta.text}">
                        <span>Đã dùng ${formatNumber(usedPct, 1)}%</span>
                        <span>${formatNumber(sq.neurons_used)} Neurons</span>
                    </div>
                    <div class="h-2.5 overflow-hidden rounded-full bg-white/70">
                        <div class="h-full rounded-full ${meta.bar}" style="width:${usedPct}%"></div>
                    </div>
                    ${sq.enabled ? `
                        <div class="mt-2 flex flex-wrap gap-3 text-[11px] ${meta.text} opacity-85">
                            <span>Cảnh báo vàng ≤ ${formatNumber(sq.warn_remaining_pct || 20)}%</span>
                            <span>Cảnh báo đỏ ≤ ${formatNumber(sq.critical_remaining_pct || 10)}%</span>
                        </div>
                    ` : ''}
                </div>
            </section>
        `;
    }

    function renderModuleCards(catalog, byModule) {
        const items = Array.isArray(catalog) && catalog.length
            ? catalog
            : [
                { id: 'lotrinh', label: moduleLabel('lotrinh'), note: 'api/ai_explain.php' },
                { id: 'thitructuyen', label: moduleLabel('thitructuyen'), note: 'Mistral OCR + Gemini' },
                { id: 'vanban', label: moduleLabel('vanban'), note: 'Tự nhận diện mẫu, không AI' },
            ];
        const toneClasses = {
            lotrinh: 'rounded-xl border border-sky-200 bg-sky-50 p-4 text-sky-900',
            thitructuyen: 'rounded-xl border border-violet-200 bg-violet-50 p-4 text-violet-900',
            vanban: 'rounded-xl border border-amber-200 bg-amber-50 p-4 text-amber-900',
        };
        return items.map((item) => {
            const mod = moduleBucket(byModule, item.id);
            const cardClass = toneClasses[item.id] || 'rounded-xl border border-slate-200 bg-slate-50 p-4 text-slate-900';
            const providerLines = (item.providers || []).map((pid) => {
                const count = providerInModule(mod, pid);
                if (!count) return '';
                return `${providerLabel(pid)}: ${formatNumber(count)}`;
            }).filter(Boolean).join(' · ');
            return `
                <div class="${cardClass}">
                    <div class="text-sm font-bold">${escapeHtml(item.label || moduleLabel(item.id))}</div>
                    <div class="mt-2 text-3xl font-black">${formatNumber(mod.success || 0)}</div>
                    <div class="text-xs opacity-90">thành công hôm nay · ${formatNumber(mod.calls || 0)} lượt gọi</div>
                    <div class="mt-2 text-xs opacity-90">${providerLines || escapeHtml(item.note || '')}</div>
                </div>
            `;
        }).join('');
    }

    function renderAiStats(data, ids = {}) {
        const loadingId = ids.loading || 'aiStatsLoading';
        const contentId = ids.content || 'aiStatsContent';
        const loading = document.getElementById(loadingId);
        const content = document.getElementById(contentId);
        if (!loading || !content) return;

        const cf = data.providers?.cloudflare || {};
        const gemini = data.providers?.gemini || {};
        const geminiBrowser = data.providers?.gemini_browser || {};
        const mistral = data.providers?.mistral_ocr || {};
        const shop = data.providers?.shopaikey || {};
        const internal = data.internal || {};
        const summary = internal.summary || {};
        const providers = summary.providers || {};
        const byModule = summary.by_module || {};
        const byMode = summary.by_mode || {};
        const totalSuccessToday = resolveTotalSuccess(summary);
        const history = Array.isArray(data.history) ? data.history : [];
        const recent = Array.isArray(internal.recent) ? internal.recent : [];
        const generatedAt = data.generated_at || '';
        const cfBucket = providers.cloudflare_workers_ai || {};
        const cfLogTotal = cfBucket.success || cf.requests_today_internal || 0;
        const cfLogLotrinh = providerInModule(moduleBucket(byModule, 'lotrinh'), 'cloudflare_workers_ai');
        const cfLogVanban = providerInModule(moduleBucket(byModule, 'vanban'), 'cloudflare_workers_ai');

        const historyRows = history.map(row => {
            const p = row.providers || {};
            return `<tr class="border-t border-slate-100">
                <td class="px-3 py-2 text-sm font-semibold">${escapeHtml(row.date)}</td>
                <td class="px-3 py-2 text-sm">${formatNumber(row.total_success || 0)}</td>
                <td class="px-3 py-2 text-sm">${formatNumber(p.cloudflare_workers_ai?.success || 0)}</td>
                <td class="px-3 py-2 text-sm">${formatNumber(p.mistral_ocr?.success || 0)}</td>
                <td class="px-3 py-2 text-sm">${formatNumber(p.gemini_browser?.success || 0)}</td>
                <td class="px-3 py-2 text-sm">${formatNumber(p.gemini?.success || 0)}</td>
                <td class="px-3 py-2 text-sm">${formatNumber(p.shopaikey?.success || 0)}</td>
            </tr>`;
        }).join('');

        const recentRows = recent.slice(0, 20).map(item => `
            <tr class="border-t border-slate-100">
                <td class="px-3 py-2 text-xs text-slate-500">${escapeHtml((item.ts || '').replace('T', ' ').slice(0, 19))}</td>
                <td class="px-3 py-2 text-xs font-semibold text-slate-700">${escapeHtml(moduleLabel(item.module || 'other'))}</td>
                <td class="px-3 py-2 text-sm">${escapeHtml(providerLabel(item.provider))}</td>
                <td class="px-3 py-2 text-sm">${escapeHtml(item.mode || '')}</td>
                <td class="px-3 py-2 text-sm">${item.ok ? '<span class="text-emerald-700 font-semibold">OK</span>' : '<span class="text-rose-700 font-semibold">Lỗi</span>'}${item.fallback ? ' <span class="text-amber-700 text-xs">(fallback)</span>' : ''}</td>
                <td class="px-3 py-2 text-xs text-slate-600">${escapeHtml(item.model || '')}</td>
            </tr>
        `).join('');

        const smartQuota = data.smart_quota || null;
        const explainCache = data.explain_cache || {};

        content.innerHTML = `
            ${renderSmartQuotaPanel(smartQuota)}

            <div class="rounded-xl border border-cyan-200 bg-cyan-50 p-4 text-cyan-950">
                <div class="text-sm font-bold">Cache câu trả lời lộ trình</div>
                <div class="mt-2 text-2xl font-black">${formatNumber(explainCache.entries || 0)}</div>
                <div class="text-xs text-cyan-800">câu đã lưu · tái sử dụng ${formatNumber(explainCache.total_hits || 0)} lần${explainCache.enabled === false ? ' · đang tắt' : ''}</div>
                <div class="mt-1 text-xs text-cyan-700">Giữ tối đa ${formatNumber(explainCache.max_entries || 0)} câu trong ${formatNumber(explainCache.ttl_days || 0)} ngày</div>
            </div>

            <div>
                <h4 class="text-sm font-bold text-slate-700 mb-2"><i class="fas fa-layer-group text-sky-600 mr-1"></i> Theo module hôm nay</h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">${renderModuleCards(internal.modules, byModule)}</div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-4">
                <div class="rounded-xl border border-orange-200 bg-orange-50 p-4">
                    <div class="flex items-center justify-between gap-2">
                        <div class="text-sm font-bold text-orange-900">Cloudflare Worker</div>
                        ${cf.available ? '<span class="text-xs font-semibold text-emerald-700">GraphQL OK</span>' : '<span class="text-xs font-semibold text-amber-700">GraphQL chưa có</span>'}
                    </div>
                    <div class="mt-2 text-2xl font-black text-orange-950">${cf.available ? formatNumber(cf.requests_today) : '—'}</div>
                    <div class="text-xs text-orange-800">Dashboard CF hôm nay</div>
                    <div class="mt-2 text-xs text-orange-800">Log nội bộ: ${formatNumber(cfLogTotal)} (lộ trình ${formatNumber(cfLogLotrinh)} · văn bản ${formatNumber(cfLogVanban)})</div>
                    <div class="mt-1 text-xs text-orange-700"><code>${escapeHtml(data.config?.cloudflare_model || '')}</code></div>
                    ${cf.dashboard_url ? `<a href="${escapeHtml(cf.dashboard_url)}" target="_blank" rel="noopener" class="mt-2 inline-flex text-xs font-bold text-orange-900 underline">Cloudflare Dashboard</a>` : ''}
                </div>
                <div class="rounded-xl border border-violet-200 bg-violet-50 p-4">
                    <div class="text-sm font-bold text-violet-900">Mistral OCR</div>
                    <div class="mt-2 text-2xl font-black text-violet-950">${formatNumber(mistral.requests_today_internal || 0)}</div>
                    <div class="text-xs text-violet-800">Thi trực tuyến · quét PDF</div>
                    <div class="mt-2 text-xs text-violet-700">${escapeHtml(mistral.message || '')}</div>
                </div>
                <div class="rounded-xl border border-blue-200 bg-blue-50 p-4">
                    <div class="text-sm font-bold text-blue-900">Gemini trình duyệt</div>
                    <div class="mt-2 text-2xl font-black text-blue-950">${formatNumber(geminiBrowser.requests_today_internal || 0)}</div>
                    <div class="text-xs text-blue-800">Thi trực tuyến · nhận diện câu hỏi</div>
                    <div class="mt-2 text-xs text-blue-700">${escapeHtml(geminiBrowser.message || '')}</div>
                </div>
                <div class="rounded-xl border border-emerald-200 bg-emerald-50 p-4">
                    <div class="text-sm font-bold text-emerald-900">Gemini fallback</div>
                    <div class="mt-2 text-2xl font-black text-emerald-950">${formatNumber(gemini.requests_today_internal || 0)}</div>
                    <div class="text-xs text-emerald-800">Lộ trình · khi hết Cloudflare</div>
                    <div class="mt-2 text-xs text-emerald-700">${formatNumber(gemini.keys_count || 0)} key · <code>${escapeHtml(gemini.model || '')}</code></div>
                </div>
                <div class="rounded-xl border border-indigo-200 bg-indigo-50 p-4">
                    <div class="flex items-center justify-between gap-2">
                        <div class="text-sm font-bold text-indigo-900">ShopAIKey</div>
                        ${shop.available ? '<span class="text-xs font-semibold text-emerald-700">API OK</span>' : '<span class="text-xs font-semibold text-amber-700">API chưa có</span>'}
                    </div>
                    <div class="mt-2 text-2xl font-black text-indigo-950">${formatNumber(shop.requests_today_internal || 0)}</div>
                    <div class="text-xs text-indigo-800">Lộ trình fallback · còn ${shop.remaining_usd != null ? formatUsd(shop.remaining_usd) : '—'}</div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="rounded-xl border border-sky-200 bg-sky-50 p-4 md:col-span-1">
                    <div class="text-xs font-bold uppercase text-sky-700">Tổng hôm nay (${escapeHtml(data.today || '')})</div>
                    <div class="mt-2 text-3xl font-black text-sky-950">${formatNumber(totalSuccessToday)}</div>
                    <div class="text-xs text-sky-800">phản hồi AI thành công (mọi module)</div>
                    <div class="mt-3 text-xs text-sky-800">Giải thích: <strong>${formatNumber(byMode.explain || 0)}</strong> · Chat: <strong>${formatNumber(byMode.chat || 0)}</strong> · OCR: <strong>${formatNumber(byMode.ocr || 0)}</strong></div>
                </div>
                <div class="md:col-span-3 rounded-xl border border-slate-200 bg-slate-50 p-4 text-xs leading-6 text-slate-700">
                    <div class="font-bold text-slate-800 mb-2">Bản đồ AI theo chức năng</div>
                    <ul class="list-disc pl-5 space-y-1">
                        <li><strong>Lộ trình học</strong> → Cloudflare Worker (chính) → Gemini / ShopAIKey (fallback)</li>
                        <li><strong>Thi trực tuyến</strong> → Mistral OCR (quét PDF) → Gemini trình duyệt (nhận diện câu hỏi)</li>
                        <li><strong>Quản lý văn bản</strong> → Tự nhận diện mẫu (không AI)</li>
                    </ul>
                </div>
            </div>

            <div>
                <h4 class="text-sm font-bold text-slate-700 mb-2">14 ngày gần nhất (log nội bộ)</h4>
                <div class="overflow-x-auto rounded-lg border border-slate-200">
                    <table class="min-w-full text-left">
                        <thead class="bg-slate-50 text-xs font-bold uppercase text-slate-500">
                            <tr><th class="px-3 py-2">Ngày</th><th class="px-3 py-2">Tổng</th><th class="px-3 py-2">CF</th><th class="px-3 py-2">Mistral</th><th class="px-3 py-2">Gemini TB</th><th class="px-3 py-2">Gemini FB</th><th class="px-3 py-2">ShopAIKey</th></tr>
                        </thead>
                        <tbody>${historyRows || '<tr><td colspan="7" class="px-3 py-4 text-sm text-slate-400">Chưa có dữ liệu.</td></tr>'}</tbody>
                    </table>
                </div>
            </div>

            <div>
                <h4 class="text-sm font-bold text-slate-700 mb-2">Lượt gọi gần đây</h4>
                <div class="overflow-x-auto rounded-lg border border-slate-200">
                    <table class="min-w-full text-left">
                        <thead class="bg-slate-50 text-xs font-bold uppercase text-slate-500">
                            <tr><th class="px-3 py-2">Thời gian</th><th class="px-3 py-2">Module</th><th class="px-3 py-2">Provider</th><th class="px-3 py-2">Mode</th><th class="px-3 py-2">Kết quả</th><th class="px-3 py-2">Model</th></tr>
                        </thead>
                        <tbody>${recentRows || '<tr><td colspan="6" class="px-3 py-4 text-sm text-slate-400">Chưa có lượt gọi nào.</td></tr>'}</tbody>
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
        const geminiBrowser = data.providers?.gemini_browser || {};
        const mistral = data.providers?.mistral_ocr || {};
        const summary = data.internal?.summary || {};
        const byModule = summary.by_module || {};
        const lotrinh = moduleBucket(byModule, 'lotrinh');
        const thitt = moduleBucket(byModule, 'thitructuyen');
        const vanban = moduleBucket(byModule, 'vanban');
        const cfWorker = cf.available ? cf.requests_today : null;

        const smartQuota = data.smart_quota || null;
        const quotaCompact = renderSmartQuotaPanel(smartQuota, { compact: true, hideLink: true });

        mount.innerHTML = `
            <div class="space-y-3">
            ${quotaCompact || ''}
            <div class="grid grid-cols-2 gap-3 lg:grid-cols-4">
                <div class="rounded-xl border border-sky-200 bg-sky-50 p-3">
                    <div class="text-[10px] font-bold uppercase text-sky-700">Lộ trình</div>
                    <div class="mt-1 text-2xl font-black text-sky-950">${formatNumber(lotrinh.success || 0)}</div>
                    <div class="text-[11px] text-sky-800">thành công hôm nay</div>
                </div>
                <div class="rounded-xl border border-violet-200 bg-violet-50 p-3">
                    <div class="text-[10px] font-bold uppercase text-violet-800">Thi trực tuyến</div>
                    <div class="mt-1 text-2xl font-black text-violet-950">${formatNumber(thitt.success || 0)}</div>
                    <div class="text-[11px] text-violet-800">Mistral ${formatNumber(mistral.requests_today_internal || 0)} · Gemini ${formatNumber(geminiBrowser.requests_today_internal || 0)}</div>
                </div>
                <div class="rounded-xl border border-amber-200 bg-amber-50 p-3">
                    <div class="text-[10px] font-bold uppercase text-amber-800">Quản lý VB</div>
                    <div class="mt-1 text-2xl font-black text-amber-950">${formatNumber(vanban.success || 0)}</div>
                    <div class="text-[11px] text-amber-800">Cloudflare hôm nay</div>
                </div>
                <div class="rounded-xl border border-orange-200 bg-orange-50 p-3">
                    <div class="text-[10px] font-bold uppercase text-orange-800">Worker CF</div>
                    <div class="mt-1 text-2xl font-black text-orange-950">${cfWorker != null ? formatNumber(cfWorker) : '—'}</div>
                    <div class="text-[11px] text-orange-800">Dashboard · tổng log ${formatNumber(resolveTotalSuccess(summary))}</div>
                </div>
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
        renderSmartQuota: renderSmartQuotaPanel,
        load: loadAiStats,
    };
    window.loadAiStats = loadAiStats;
})();