(() => {
    const API = 'api/vanban.php';
    const SECTORS = {
        hanhchinh: { label: 'Hành chính', icon: 'fa-building', accent: 'teal', page: 'quanlyvanban-hanhchinh.html' },
        dang: { label: 'Đảng', icon: 'fa-flag', accent: 'rose', page: 'quanlyvanban-dang.html' },
    };

    const state = { documents: [], driveReady: false, driveHint: '', driveConfigured: false };

    const $ = id => document.getElementById(id);
    const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[ch]));

    function sectorOf(doc) {
        return doc.sector === 'dang' ? 'dang' : 'hanhchinh';
    }

    function statsFor(docs) {
        const incoming = docs.filter(d => d.direction === 'incoming').length;
        const outgoing = docs.filter(d => d.direction === 'outgoing').length;
        const needAction = docs.filter(d => ['pending', 'in_progress', 'overdue'].includes(d.effective_status)).length;
        const overdue = docs.filter(d => d.effective_status === 'overdue').length;
        return { total: docs.length, incoming, outgoing, needAction, overdue };
    }

    function reminderInfo(doc) {
        if (!Number(doc.report_required) || doc.effective_status === 'completed' || !doc.report_due_at) return null;
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const due = new Date(`${doc.report_due_at}T00:00:00`);
        if (Number.isNaN(due.getTime())) return null;
        const days = Math.round((due - today) / 86400000);
        if (days > 7) return null;
        const label = days < 0 ? `Quá hạn ${Math.abs(days)} ngày` : days === 0 ? 'Đến hạn hôm nay' : days === 1 ? 'Còn 1 ngày' : `Còn ${days} ngày`;
        const tone = days <= 1 ? 'rose' : days <= 3 ? 'orange' : 'amber';
        return { days, label, tone };
    }

    function renderSummary() {
        const s = statsFor(state.documents);
        const cards = [
            ['Văn bản đến', s.incoming, 'text-cyan-700', 'fa-inbox'],
            ['Văn bản đi', s.outgoing, 'text-indigo-700', 'fa-paper-plane'],
            ['Cần xử lý / báo cáo', s.needAction, 'text-amber-700', 'fa-clipboard-list'],
            ['Quá hạn', s.overdue, 'text-rose-700', 'fa-clock'],
        ];
        const host = $('summary');
        if (!host) return;
        host.innerHTML = cards.map(([label, value, tone, icon]) => `
            <div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                <div class="flex items-center justify-between gap-2">
                    <div class="text-xs font-bold uppercase tracking-wide text-slate-500">${label}</div>
                    <i class="fa-solid ${icon} ${tone} opacity-80"></i>
                </div>
                <div class="mt-2 text-3xl font-black ${tone}">${value}</div>
            </div>`).join('');
    }

    function sectorCard(key, meta, docs) {
        const s = statsFor(docs);
        const accent = meta.accent === 'rose'
            ? { border: 'border-rose-200', bg: 'bg-rose-50', text: 'text-rose-800', icon: 'text-rose-700', btn: 'bg-rose-700 hover:bg-rose-800' }
            : { border: 'border-teal-200', bg: 'bg-teal-50', text: 'text-teal-800', icon: 'text-teal-700', btn: 'bg-teal-700 hover:bg-teal-800' };
        const urgent = docs.filter(d => reminderInfo(d)).length;
        return `
            <a href="${meta.page}" class="group block rounded-2xl border ${accent.border} bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
                <div class="flex items-start justify-between gap-3">
                    <div>
                        <p class="text-xs font-extrabold uppercase tracking-[.12em] ${accent.text}">${meta.label}</p>
                        <h2 class="mt-1 text-xl font-black text-slate-950">
                            <i class="fa-solid ${meta.icon} mr-2 ${accent.icon}"></i>${meta.label}
                        </h2>
                    </div>
                    ${urgent ? `<span class="rounded-full bg-amber-100 px-2.5 py-1 text-xs font-extrabold text-amber-900">${urgent} việc gấp</span>` : ''}
                </div>
                <div class="mt-4 grid grid-cols-2 gap-2 text-sm">
                    <div class="rounded-lg ${accent.bg} px-3 py-2"><span class="block text-xs font-bold text-slate-500">Văn bản đến</span><span class="font-black text-slate-900">${s.incoming}</span></div>
                    <div class="rounded-lg ${accent.bg} px-3 py-2"><span class="block text-xs font-bold text-slate-500">Văn bản đi</span><span class="font-black text-slate-900">${s.outgoing}</span></div>
                    <div class="rounded-lg ${accent.bg} px-3 py-2"><span class="block text-xs font-bold text-slate-500">Cần xử lý</span><span class="font-black text-amber-800">${s.needAction}</span></div>
                    <div class="rounded-lg ${accent.bg} px-3 py-2"><span class="block text-xs font-bold text-slate-500">Quá hạn</span><span class="font-black text-rose-700">${s.overdue}</span></div>
                </div>
                <div class="mt-4 inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-bold text-white ${accent.btn}">
                    Mở mục ${meta.label} <i class="fa-solid fa-arrow-right transition group-hover:translate-x-0.5"></i>
                </div>
            </a>`;
    }

    function renderSectors() {
        const host = $('sectorCards');
        if (!host) return;
        host.innerHTML = Object.entries(SECTORS).map(([key, meta]) => {
            const docs = state.documents.filter(d => sectorOf(d) === key);
            return sectorCard(key, meta, docs);
        }).join('');
    }

    function renderReminders() {
        const items = state.documents
            .map(doc => ({ doc, info: reminderInfo(doc) }))
            .filter(item => item.info)
            .sort((a, b) => a.info.days - b.info.days);
        const panel = $('reminderPanel');
        if (!panel) return;
        if (!items.length) {
            panel.classList.add('hidden');
            return;
        }
        const overdue = items.filter(item => item.info.days < 0).length;
        const urgent = items.length - overdue;
        $('reminderSummary').textContent = `${overdue ? `${overdue} quá hạn` : 'Không có việc quá hạn'}${overdue && urgent ? ' · ' : ''}${urgent ? `${urgent} văn bản đến hạn trong 7 ngày` : ''}.`;
        $('reminderList').innerHTML = items.slice(0, 8).map(({ doc, info }) => {
            const sector = SECTORS[sectorOf(doc)];
            return `
                <a href="${sector.page}" class="flex items-center justify-between gap-3 rounded-lg border px-3 py-2.5 ${info.tone === 'rose' ? 'border-rose-200 bg-rose-50 text-rose-950' : info.tone === 'orange' ? 'border-orange-200 bg-orange-50 text-orange-950' : 'border-amber-200 bg-white text-amber-950'} hover:brightness-95">
                    <span class="min-w-0">
                        <span class="block truncate font-bold">${esc(doc.title)}</span>
                        <span class="mt-0.5 block text-xs opacity-80">${esc(sector.label)}${doc.document_number ? ` · ${esc(doc.document_number)}` : ''}</span>
                    </span>
                    <span class="shrink-0 rounded-full px-2 py-1 text-xs font-extrabold ${info.tone === 'rose' ? 'bg-rose-200 text-rose-900' : info.tone === 'orange' ? 'bg-orange-200 text-orange-900' : 'bg-amber-200 text-amber-900'}">${info.label}</span>
                </a>`;
        }).join('');
        panel.classList.remove('hidden');
    }

    function renderDriveWarning() {
        const box = $('driveWarning');
        if (!box) return;
        if (state.driveReady) {
            box.classList.add('hidden');
            return;
        }
        const hint = state.driveHint || (state.driveConfigured
            ? 'Google Drive chưa sẵn sàng để tải tệp.'
            : 'Google Drive chưa được cấu hình.');
        box.innerHTML = `<p><i class="fa-solid fa-triangle-exclamation mr-2"></i><strong>Google Drive:</strong> ${esc(hint)}</p>`;
        box.classList.remove('hidden');
    }

    async function load() {
        try {
            const response = await fetch(`${API}?action=list&with_drive=1`, { credentials: 'include', cache: 'no-store' });
            const data = await response.json().catch(() => ({}));
            if (!response.ok) throw new Error(data.error || 'Không tải được dữ liệu.');
            state.documents = data.documents || [];
            state.driveConfigured = !!data.drive_configured;
            state.driveReady = !!data.drive_ready;
            state.driveHint = data.drive_hint || '';
            renderDriveWarning();
            renderSummary();
            renderSectors();
            renderReminders();
        } catch (error) {
            const box = $('loadError');
            if (box) {
                box.textContent = error.message;
                box.classList.remove('hidden');
            }
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', load);
    } else {
        load();
    }
})();