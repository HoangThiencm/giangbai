(() => {
    const API = 'api/thanhtich.php';
    const LS_YEAR_KEY = 'thanhtich_academic_year';
    const LS_TAB_KEY = 'thanhtich_participant_tab';

    const ORGANIZER_OTHER = 'Khác';
    const DEFAULT_ORGANIZERS = ['Bộ Giáo dục', 'Sở Giáo dục', 'Phòng Văn hoá', ORGANIZER_OTHER];

    const state = {
        meta: null,
        entries: [],
        selectedYear: localStorage.getItem(LS_YEAR_KEY) || '',
        activeTab: localStorage.getItem(LS_TAB_KEY) || 'teacher',
        search: '',
        winnersDraft: [],
        summary: null,
    };

    const $ = id => document.getElementById(id);
    const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[ch]));

    const SCOPE_LABELS = {
        school: 'Cấp trường',
        ward: 'Cấp phường/xã',
        city: 'Cấp thành phố',
        national: 'Cấp quốc gia',
        international: 'Cấp quốc tế',
        district: 'Cấp huyện',
        province: 'Cấp tỉnh',
    };

    const scopeLabel = scope => SCOPE_LABELS[scope] || scope || '—';

    const scopeTone = scope => ({
        school: 'bg-slate-100 text-slate-700',
        ward: 'bg-sky-100 text-sky-800',
        city: 'bg-indigo-100 text-indigo-800',
        national: 'bg-amber-100 text-amber-900',
        international: 'bg-rose-100 text-rose-800',
        district: 'bg-sky-100 text-sky-800',
        province: 'bg-indigo-100 text-indigo-800',
    }[scope] || 'bg-slate-100 text-slate-700');

    const dateText = value => value ? new Date(`${value}T00:00:00`).toLocaleDateString('vi-VN') : '—';

    function schoolYear(date = new Date()) {
        const y = date.getFullYear();
        const m = date.getMonth() + 1;
        return m >= 8 ? `${y}-${y + 1}` : `${y - 1}-${y}`;
    }

    function showToast(message) {
        const toast = $('toast');
        toast.textContent = message;
        toast.classList.remove('hidden');
        clearTimeout(showToast._timer);
        showToast._timer = setTimeout(() => toast.classList.add('hidden'), 2600);
    }

    function showError(message) {
        const box = $('loadError');
        box.textContent = message;
        box.classList.remove('hidden');
    }

    function hideError() {
        $('loadError').classList.add('hidden');
    }

    async function api(action, options = {}) {
        const url = new URL(API, window.location.href);
        url.searchParams.set('action', action);
        if (options.query) {
            Object.entries(options.query).forEach(([key, value]) => {
                if (value !== undefined && value !== null && value !== '') {
                    url.searchParams.set(key, value);
                }
            });
        }
        const init = {
            method: options.method || 'GET',
            credentials: 'include',
            headers: {},
        };
        if (options.body) {
            init.method = 'POST';
            init.headers['Content-Type'] = 'application/json';
            init.body = JSON.stringify(options.body);
        }
        const res = await fetch(url, init);
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(data.error || 'Không thể kết nối máy chủ.');
        }
        return data;
    }

    function filteredEntries() {
        const q = state.search.trim().toLowerCase();
        return state.entries.filter(entry => {
            if (entry.participant_type !== state.activeTab) return false;
            if (!q) return true;
            const hay = [
                entry.campaign_name,
                entry.organizer,
                entry.prize_summary,
                entry.note,
                ...(entry.winners || []).map(w => [w.full_name, w.class_or_role, w.prize_rank, w.prize_title].join(' ')),
            ].join(' ').toLowerCase();
            return hay.includes(q);
        });
    }

    function updateStats() {
        const rows = filteredEntries();
        const participants = rows.reduce((sum, row) => sum + Number(row.participant_count || 0), 0);
        const prizes = rows.reduce((sum, row) => sum + Number(row.prize_count || 0), 0);
        const winners = rows.reduce((sum, row) => sum + Number(row.winner_count || (row.winners || []).length), 0);
        $('statCompetitions').textContent = String(rows.length);
        $('statParticipants').textContent = String(participants);
        $('statPrizes').textContent = String(prizes);
        $('statWinners').textContent = String(winners);
    }

    function entryCardHtml(entry) {
        const winners = entry.winners || [];
        const winnerPreview = winners.slice(0, 4).map(w => `
            <span class="chip bg-amber-50 text-amber-900">${esc(w.full_name)}${w.prize_rank ? ` · ${esc(w.prize_rank)}` : ''}</span>
        `).join('');
        const more = winners.length > 4 ? `<span class="text-xs font-bold text-slate-500">+${winners.length - 4} người</span>` : '';
        return `<article class="rounded-2xl border border-slate-200 bg-white px-4 py-4 shadow-sm transition hover:border-amber-200 hover:shadow-md sm:px-5">
            <div class="grid gap-4 lg:grid-cols-[minmax(260px,1.7fr)_120px_120px_120px_auto] lg:items-center">
                <div class="min-w-0">
                    <div class="flex flex-wrap items-center gap-2">
                        <span class="chip ${scopeTone(entry.scope_level)}">${esc(entry.scope_label || entry.scope_level)}</span>
                        <span class="text-[11px] font-bold text-slate-400">${esc(dateText(entry.event_date))}</span>
                    </div>
                    <h3 class="mt-2 text-base font-black text-slate-900 sm:text-lg">${esc(entry.campaign_name)}</h3>
                    <p class="mt-1 truncate text-xs font-bold text-slate-500"><i class="fas fa-building-columns mr-1.5 text-amber-700"></i>${esc(entry.organizer || 'Chưa ghi cơ quan')}</p>
                    ${entry.prize_summary ? `<p class="mt-1 text-xs text-slate-600"><i class="fas fa-medal mr-1 text-amber-600"></i>${esc(entry.prize_summary)}</p>` : ''}
                    <div class="mt-2 flex flex-wrap gap-1.5">${winnerPreview}${more}</div>
                </div>
                <div class="rounded-xl bg-slate-50 px-3 py-2"><div class="text-lg font-black">${entry.participant_count || 0}</div><div class="text-[11px] text-slate-500">Tham gia</div></div>
                <div class="rounded-xl bg-amber-50 px-3 py-2"><div class="text-lg font-black text-amber-800">${entry.prize_count || 0}</div><div class="text-[11px] text-amber-700/70">Đạt giải</div></div>
                <div class="rounded-xl bg-emerald-50 px-3 py-2"><div class="text-lg font-black text-emerald-800">${winners.length}</div><div class="text-[11px] text-emerald-700/70">Họ tên</div></div>
                <div class="flex flex-wrap gap-2 lg:justify-end">
                    <button type="button" data-edit="${entry.id}" class="rounded-lg bg-slate-900 px-3 py-2 text-xs font-extrabold text-white"><i class="fas fa-pen mr-1"></i>Sửa</button>
                    <button type="button" data-delete="${entry.id}" class="grid h-9 w-9 place-items-center rounded-lg bg-red-50 text-red-600 hover:bg-red-100" title="Xóa"><i class="fas fa-trash-can"></i></button>
                </div>
            </div>
        </article>`;
    }

    function renderEntries() {
        const rows = filteredEntries();
        $('loading').classList.add('hidden');
        updateStats();
        if (!rows.length) {
            $('entryList').classList.add('hidden');
            $('emptyState').classList.remove('hidden');
            return;
        }
        $('emptyState').classList.add('hidden');
        $('entryList').classList.remove('hidden');
        $('entryList').innerHTML = rows.map(entryCardHtml).join('');
    }

    function populateYearSelect() {
        const years = [...new Set([
            ...(state.meta?.school_years || []),
            state.meta?.current_year,
            state.selectedYear,
        ].filter(Boolean))].sort((a, b) => b.localeCompare(a));

        const select = $('yearSelect');
        const prev = state.selectedYear || localStorage.getItem(LS_YEAR_KEY) || state.meta?.current_year || schoolYear();
        select.innerHTML = years.map(year => `<option value="${esc(year)}">Năm học ${esc(year)}</option>`).join('');
        state.selectedYear = years.includes(prev) ? prev : (years[0] || schoolYear());
        select.value = state.selectedYear;
        localStorage.setItem(LS_YEAR_KEY, state.selectedYear);
    }

    function organizerOptions() {
        return state.meta?.presets?.organizers || DEFAULT_ORGANIZERS;
    }

    function populateOrganizerSelect(selected = '') {
        const options = organizerOptions();
        $('organizerSelect').innerHTML = [
            '<option value="">-- Chọn cơ quan --</option>',
            ...options.map(item => `<option value="${esc(item)}">${esc(item)}</option>`),
        ].join('');
        if (selected && options.includes(selected)) {
            $('organizerSelect').value = selected;
            $('organizerCustom').value = '';
            $('organizerCustomWrap').classList.add('hidden');
            return;
        }
        if (selected) {
            $('organizerSelect').value = ORGANIZER_OTHER;
            $('organizerCustom').value = selected;
            $('organizerCustomWrap').classList.remove('hidden');
            return;
        }
        $('organizerSelect').value = '';
        $('organizerCustom').value = '';
        $('organizerCustomWrap').classList.add('hidden');
    }

    function toggleOrganizerCustom() {
        const isOther = $('organizerSelect').value === ORGANIZER_OTHER;
        $('organizerCustomWrap').classList.toggle('hidden', !isOther);
        if (!isOther) {
            $('organizerCustom').value = '';
        }
    }

    function readOrganizer() {
        const selected = $('organizerSelect').value.trim();
        if (selected === ORGANIZER_OTHER) {
            return $('organizerCustom').value.trim();
        }
        return selected;
    }

    function populatePresets() {
        const presets = state.meta?.presets || {};
        populateOrganizerSelect();
        $('scopeLevel').innerHTML = (presets.scope_levels || []).map(item => `<option value="${esc(item.value)}">${esc(item.label)}</option>`).join('');
        window.__prizeRankOptions = presets.prize_ranks || [];
    }

    function campaignPlaceholder(tab = state.activeTab) {
        return tab === 'teacher'
            ? 'Tự nhập tên phong trào, cuộc thi (giáo viên)'
            : 'Tự nhập tên phong trào, cuộc thi (học sinh)';
    }

    function refreshCampaignField() {
        const input = $('campaignName');
        if (!input) return;
        input.placeholder = campaignPlaceholder(state.activeTab);
    }

    function setActiveTab(tab) {
        state.activeTab = tab;
        localStorage.setItem(LS_TAB_KEY, tab);
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tab);
        });
        refreshCampaignField();
        renderEntries();
    }

    function winnerRowHtml(winner, index) {
        const ranks = (window.__prizeRankOptions || []).map(rank => `<option value="${esc(rank)}">`).join('');
        return `<div class="winner-row" data-winner-index="${index}">
            <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
                <label class="sm:col-span-2">
                    <span class="label">Họ và tên <span class="text-rose-600">*</span></span>
                    <input data-field="full_name" required class="field" value="${esc(winner.full_name || '')}" placeholder="Nguyễn Văn A">
                </label>
                <label>
                    <span class="label">${state.activeTab === 'teacher' ? 'Tổ CM / chức vụ' : 'Lớp'}</span>
                    <input data-field="class_or_role" class="field" value="${esc(winner.class_or_role || '')}" placeholder="${state.activeTab === 'teacher' ? 'Tổ Toán' : '8A1'}">
                </label>
                <label>
                    <span class="label">Hạng giải</span>
                    <input data-field="prize_rank" class="field" list="prizeRankList" value="${esc(winner.prize_rank || '')}" placeholder="Giải Nhất">
                </label>
                <label>
                    <span class="label">Tên giải / nội dung</span>
                    <input data-field="prize_title" class="field" value="${esc(winner.prize_title || '')}" placeholder="Giải nhất môn Toán">
                </label>
            </div>
            <div class="mt-2 flex justify-end">
                <button type="button" data-remove-winner="${index}" class="rounded-lg bg-red-50 px-3 py-1.5 text-xs font-extrabold text-red-700 hover:bg-red-100">Xóa dòng</button>
            </div>
        </div>`;
    }

    function renderWinnerRows() {
        if (!state.winnersDraft.length) {
            state.winnersDraft = [{ full_name: '', class_or_role: '', prize_rank: '', prize_title: '', note: '' }];
        }
        $('winnerRows').innerHTML = state.winnersDraft.map((winner, index) => winnerRowHtml(winner, index)).join('');
        if (!$('prizeRankList')) {
            const datalist = document.createElement('datalist');
            datalist.id = 'prizeRankList';
            datalist.innerHTML = (window.__prizeRankOptions || []).map(rank => `<option value="${esc(rank)}">`).join('');
            document.body.appendChild(datalist);
        }
    }

    function collectWinnerDraft() {
        const rows = [...$('winnerRows').querySelectorAll('[data-winner-index]')];
        return rows.map(row => {
            const read = field => row.querySelector(`[data-field="${field}"]`)?.value?.trim() || '';
            return {
                full_name: read('full_name'),
                class_or_role: read('class_or_role'),
                prize_rank: read('prize_rank'),
                prize_title: read('prize_title'),
                note: '',
            };
        }).filter(row => row.full_name);
    }

    function openEditor(entry = null) {
        $('formError').classList.add('hidden');
        $('entryId').value = entry ? entry.id : '';
        $('editorTitle').textContent = entry ? 'Sửa thành tích' : 'Thêm thành tích';
        if (entry?.participant_type && entry.participant_type !== state.activeTab) {
            setActiveTab(entry.participant_type);
        }
        refreshCampaignField();
        $('campaignName').value = entry?.campaign_name || '';
        populateOrganizerSelect(entry?.organizer || '');
        $('scopeLevel').value = entry?.scope_level || 'school';
        $('eventDate').value = entry?.event_date || '';
        $('participantCount').value = entry?.participant_count ?? 0;
        $('prizeCount').value = entry?.prize_count ?? 0;
        $('prizeSummary').value = entry?.prize_summary || '';
        $('entryNote').value = entry?.note || '';
        state.winnersDraft = entry?.winners?.length
            ? entry.winners.map(w => ({
                full_name: w.full_name || '',
                class_or_role: w.class_or_role || '',
                prize_rank: w.prize_rank || '',
                prize_title: w.prize_title || '',
                note: w.note || '',
            }))
            : [{ full_name: '', class_or_role: '', prize_rank: '', prize_title: '', note: '' }];
        renderWinnerRows();
        $('editorModal').classList.remove('hidden');
    }

    function closeEditor() {
        $('editorModal').classList.add('hidden');
    }

    function buildSummaryText(summary) {
        const totals = summary.totals || {};
        const lines = [
            `BÁO CÁO THÀNH TÍCH NĂM HỌC ${summary.academic_year}`,
            `Trường: ${state.meta?.school || 'THCS Trần Phú'}`,
            '',
            `Tổng số cuộc thi/phong trào: ${totals.competitions || 0}`,
            `- Giáo viên: ${totals.teacher_competitions || 0} cuộc, ${totals.teacher_prizes || 0} giải`,
            `- Học sinh: ${totals.student_competitions || 0} cuộc, ${totals.student_prizes || 0} giải`,
            `Tổng lượt tham gia: ${totals.participants || 0}`,
            `Tổng số giải đạt được: ${totals.prizes || 0}`,
            '',
            'Chi tiết theo cơ quan tổ chức:',
        ];
        (summary.by_organizer || []).forEach(group => {
            const typeLabel = group.participant_type === 'teacher' ? 'GV' : 'HS';
            lines.push(`- [${typeLabel}] ${group.organizer || 'Chưa rõ'} (${scopeLabel(group.scope_level)}): ${group.competition_count} cuộc, ${group.participants} tham gia, ${group.prizes} giải`);
        });
        if ((summary.prize_breakdown || []).length) {
            lines.push('', 'Phân loại giải:');
            summary.prize_breakdown.forEach(item => {
                const typeLabel = item.participant_type === 'teacher' ? 'GV' : 'HS';
                lines.push(`- [${typeLabel}] ${item.prize_rank || 'Khác'}: ${item.count}`);
            });
        }
        return lines.join('\n');
    }

    function summaryHtml(summary) {
        const totals = summary.totals || {};
        const organizerRows = (summary.by_organizer || []).map(group => `
            <tr class="border-t border-slate-100">
                <td class="px-3 py-2 text-sm">${group.participant_type === 'teacher' ? 'Giáo viên' : 'Học sinh'}</td>
                <td class="px-3 py-2 text-sm">${esc(group.organizer || '—')}</td>
                <td class="px-3 py-2 text-sm">${esc(scopeLabel(group.scope_level))}</td>
                <td class="px-3 py-2 text-right text-sm font-bold">${group.competition_count}</td>
                <td class="px-3 py-2 text-right text-sm font-bold">${group.participants}</td>
                <td class="px-3 py-2 text-right text-sm font-bold text-amber-700">${group.prizes}</td>
            </tr>
        `).join('');

        const prizeRows = (summary.prize_breakdown || []).map(item => `
            <span class="chip bg-amber-50 text-amber-900">${item.participant_type === 'teacher' ? 'GV' : 'HS'} · ${esc(item.prize_rank || 'Khác')}: ${item.count}</span>
        `).join('');

        return `
            <div class="grid gap-3 sm:grid-cols-4">
                <div class="rounded-2xl bg-slate-50 p-4"><div class="text-2xl font-black">${totals.competitions || 0}</div><div class="text-xs text-slate-500">Cuộc thi</div></div>
                <div class="rounded-2xl bg-sky-50 p-4"><div class="text-2xl font-black text-sky-800">${totals.participants || 0}</div><div class="text-xs text-sky-700/70">Tham gia</div></div>
                <div class="rounded-2xl bg-amber-50 p-4"><div class="text-2xl font-black text-amber-800">${totals.prizes || 0}</div><div class="text-xs text-amber-700/70">Giải</div></div>
                <div class="rounded-2xl bg-emerald-50 p-4"><div class="text-sm font-black text-emerald-800">GV ${totals.teacher_prizes || 0} · HS ${totals.student_prizes || 0}</div><div class="text-xs text-emerald-700/70">Theo đối tượng</div></div>
            </div>
            <div class="mt-5 overflow-x-auto rounded-2xl border border-slate-200">
                <table class="min-w-full text-left">
                    <thead class="bg-slate-50 text-xs font-extrabold uppercase tracking-wide text-slate-500">
                        <tr>
                            <th class="px-3 py-2">Đối tượng</th>
                            <th class="px-3 py-2">Cơ quan tổ chức</th>
                            <th class="px-3 py-2">Cấp</th>
                            <th class="px-3 py-2 text-right">Cuộc</th>
                            <th class="px-3 py-2 text-right">Tham gia</th>
                            <th class="px-3 py-2 text-right">Giải</th>
                        </tr>
                    </thead>
                    <tbody>${organizerRows || '<tr><td colspan="6" class="px-3 py-6 text-center text-sm text-slate-500">Chưa có dữ liệu.</td></tr>'}</tbody>
                </table>
            </div>
            ${prizeRows ? `<div class="mt-4 flex flex-wrap gap-2">${prizeRows}</div>` : ''}
            <div class="mt-5 flex flex-wrap gap-2">
                <button id="btnCopySummary" type="button" class="rounded-xl bg-slate-900 px-4 py-2.5 text-sm font-extrabold text-white"><i class="fas fa-copy mr-2"></i>Sao chép báo cáo</button>
                <button id="btnDownloadCsv" type="button" class="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-extrabold text-slate-700"><i class="fas fa-download mr-2"></i>Tải CSV</button>
            </div>
            <pre class="mt-4 hidden rounded-2xl bg-slate-50 p-4 text-xs leading-6 text-slate-700 sm:block">${esc(buildSummaryText(summary))}</pre>
        `;
    }

    async function openSummary() {
        if (!state.selectedYear) {
            showToast('Hãy chọn năm học trước.');
            return;
        }
        const data = await api('summary', { query: { year: state.selectedYear } });
        state.summary = data.summary;
        $('summaryTitle').textContent = `Báo cáo thành tích ${state.selectedYear}`;
        $('summaryBody').innerHTML = summaryHtml(state.summary);
        $('summaryModal').classList.remove('hidden');
        $('btnCopySummary')?.addEventListener('click', async () => {
            await navigator.clipboard.writeText(buildSummaryText(state.summary));
            showToast('Đã sao chép báo cáo.');
        });
        $('btnDownloadCsv')?.addEventListener('click', () => downloadCsv());
    }

    function downloadCsv() {
        const rows = state.entries.filter(entry => entry.academic_year === state.selectedYear);
        const headers = ['Đối tượng', 'Phong trào/Cuộc thi', 'Cơ quan tổ chức', 'Cấp', 'Ngày', 'Tham gia', 'Đạt giải', 'Họ tên', 'Lớp/Chức vụ', 'Hạng giải', 'Tên giải'];
        const lines = [headers.join(',')];
        rows.forEach(entry => {
            const winners = entry.winners?.length ? entry.winners : [{ full_name: '', class_or_role: '', prize_rank: '', prize_title: '' }];
            winners.forEach(winner => {
                const cols = [
                    entry.participant_type === 'teacher' ? 'Giáo viên' : 'Học sinh',
                    entry.campaign_name,
                    entry.organizer,
                    entry.scope_label || entry.scope_level,
                    entry.event_date || '',
                    entry.participant_count,
                    entry.prize_count,
                    winner.full_name,
                    winner.class_or_role,
                    winner.prize_rank,
                    winner.prize_title,
                ].map(value => `"${String(value ?? '').replace(/"/g, '""')}"`);
                lines.push(cols.join(','));
            });
        });
        const blob = new Blob(['\uFEFF' + lines.join('\n')], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `thanhtich-${state.selectedYear}.csv`;
        link.click();
        URL.revokeObjectURL(link.href);
        showToast('Đã tải file CSV.');
    }

    async function loadEntries() {
        hideError();
        $('loading').classList.remove('hidden');
        $('entryList').classList.add('hidden');
        $('emptyState').classList.add('hidden');
        const data = await api('list', { query: { year: state.selectedYear, type: 'all', q: state.search } });
        state.entries = data.entries || [];
        renderEntries();
    }

    async function bootstrap() {
        try {
            const data = await api('meta');
            state.meta = data;
            if (data.user?.name) {
                $('teacherName').textContent = data.user.name;
                $('teacherName').classList.remove('hidden');
            }
            populateYearSelect();
            populatePresets();
            setActiveTab(state.activeTab);
            await loadEntries();
        } catch (error) {
            $('loading').classList.add('hidden');
            showError(error.message);
        }
    }

    async function saveEntry(event) {
        event.preventDefault();
        $('formError').classList.add('hidden');
        const winners = collectWinnerDraft();
        const prizeCount = Math.max(Number($('prizeCount').value || 0), winners.length);
        const organizer = readOrganizer();
        if (!organizer) {
            $('formError').textContent = 'Vui lòng chọn cơ quan tổ chức (hoặc ghi rõ nếu chọn Khác).';
            $('formError').classList.remove('hidden');
            return;
        }
        const payload = {
            id: Number($('entryId').value || 0) || undefined,
            academic_year: state.selectedYear,
            participant_type: state.activeTab,
            campaign_name: $('campaignName').value.trim(),
            organizer,
            scope_level: $('scopeLevel').value,
            event_date: $('eventDate').value,
            participant_count: Number($('participantCount').value || 0),
            prize_count: prizeCount,
            prize_summary: $('prizeSummary').value.trim(),
            note: $('entryNote').value.trim(),
            winners,
        };
        try {
            await api('save', { body: payload });
            closeEditor();
            showToast('Đã lưu thành tích.');
            await loadEntries();
        } catch (error) {
            $('formError').textContent = error.message;
            $('formError').classList.remove('hidden');
        }
    }

    async function createSchoolYear() {
        const input = prompt('Nhập năm học, ví dụ: 2025-2026');
        if (!input) return;
        const year = input.trim().replace(/\s+/g, '');
        if (!/^\d{4}-\d{4}$/.test(year)) {
            showToast('Định dạng năm học không hợp lệ.');
            return;
        }
        try {
            await api('create_school_year', { body: { academic_year: year } });
            if (!state.meta.school_years.includes(year)) {
                state.meta.school_years.unshift(year);
            }
            state.selectedYear = year;
            populateYearSelect();
            await loadEntries();
            showToast(`Đã tạo năm học ${year}.`);
        } catch (error) {
            showToast(error.message);
        }
    }

    function bindEvents() {
        $('yearSelect').addEventListener('change', async event => {
            state.selectedYear = event.target.value;
            localStorage.setItem(LS_YEAR_KEY, state.selectedYear);
            await loadEntries();
        });

        $('searchInput').addEventListener('input', event => {
            state.search = event.target.value;
            renderEntries();
        });

        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => setActiveTab(btn.dataset.tab));
        });

        $('btnAddEntry').addEventListener('click', () => openEditor());
        $('btnAddEmpty').addEventListener('click', () => openEditor());
        $('btnCloseEditor').addEventListener('click', closeEditor);
        $('btnCancelEditor').addEventListener('click', closeEditor);
        $('entryForm').addEventListener('submit', saveEntry);
        $('organizerSelect').addEventListener('change', toggleOrganizerCustom);
        $('btnCreateYear').addEventListener('click', createSchoolYear);
        $('btnShowSummary').addEventListener('click', () => openSummary().catch(err => showToast(err.message)));
        $('btnExportSummary').addEventListener('click', () => {
            if (!state.entries.length) {
                showToast('Chưa có dữ liệu để xuất.');
                return;
            }
            downloadCsv();
        });
        $('btnCloseSummary').addEventListener('click', () => $('summaryModal').classList.add('hidden'));

        $('btnAddWinner').addEventListener('click', () => {
            state.winnersDraft = collectWinnerDraft();
            state.winnersDraft.push({ full_name: '', class_or_role: '', prize_rank: '', prize_title: '', note: '' });
            renderWinnerRows();
        });

        $('winnerRows').addEventListener('click', event => {
            const removeBtn = event.target.closest('[data-remove-winner]');
            if (!removeBtn) return;
            const index = Number(removeBtn.dataset.removeWinner);
            state.winnersDraft = collectWinnerDraft();
            state.winnersDraft.splice(index, 1);
            renderWinnerRows();
        });

        $('entryList').addEventListener('click', async event => {
            const editBtn = event.target.closest('[data-edit]');
            const deleteBtn = event.target.closest('[data-delete]');
            if (editBtn) {
                const entry = state.entries.find(item => String(item.id) === String(editBtn.dataset.edit));
                if (entry) {
                    if (entry.participant_type !== state.activeTab) {
                        setActiveTab(entry.participant_type);
                    }
                    openEditor(entry);
                }
                return;
            }
            if (deleteBtn) {
                const id = Number(deleteBtn.dataset.delete);
                if (!confirm('Xóa bản ghi thành tích này?')) return;
                try {
                    await api('delete', { body: { id } });
                    showToast('Đã xóa bản ghi.');
                    await loadEntries();
                } catch (error) {
                    showToast(error.message);
                }
            }
        });
    }

    bindEvents();
    bootstrap();
})();