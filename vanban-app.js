(() => {
    const API = 'api/vanban.php';
    const SECTOR = window.VANBAN_SECTOR === 'dang' ? 'dang' : 'hanhchinh';
    const SECTOR_META = {
        hanhchinh: { label: 'Hành chính', icon: 'fa-building', accent: 'teal', page: 'quanlyvanban-hanhchinh.html' },
        dang: { label: 'Đảng', icon: 'fa-flag', accent: 'rose', page: 'quanlyvanban-dang.html' },
    };
    const meta = SECTOR_META[SECTOR];
    const LS_YEAR_KEY = `vbd_academic_year_${SECTOR}`;
    const LS_TAB_KEY = `vbd_direction_tab_${SECTOR}`;

    const state = {
        documents: [],
        schoolYears: [],
        selectedYear: localStorage.getItem(LS_YEAR_KEY) || '',
        yearInitialized: false,
        activeDirection: localStorage.getItem(LS_TAB_KEY) || 'incoming',
        statusFilter: '',
        search: '',
        driveConfigured: false,
        driveReady: false,
        driveHint: '',
        driveDiag: {},
    };

    const $ = id => document.getElementById(id);
    const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[ch]));

    const statusInfo = status => ({
        not_required: ['Không cần báo cáo', 'bg-slate-100 text-slate-700'],
        pending: ['Chưa xử lý', 'bg-amber-100 text-amber-800'],
        in_progress: ['Đang xử lý', 'bg-sky-100 text-sky-800'],
        completed: ['Đã báo cáo', 'bg-teal-100 text-teal-800'],
        overdue: ['Quá hạn', 'bg-rose-100 text-rose-800'],
    }[status] || ['Chưa xử lý', 'bg-amber-100 text-amber-800']);

    const dateText = value => value ? new Date(`${value}T00:00:00`).toLocaleDateString('vi-VN') : '—';

    function accentBtn(active = false) {
        const map = {
            teal: active ? 'bg-teal-700 text-white' : 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50',
            rose: active ? 'bg-rose-700 text-white' : 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50',
        };
        return map[meta.accent] || map.teal;
    }

    function accentPrimary() {
        return meta.accent === 'rose' ? 'bg-rose-700 hover:bg-rose-800' : 'bg-teal-700 hover:bg-teal-800';
    }

    function toast(message, tone = 'teal') {
        const box = $('toast');
        if (!box) return;
        box.textContent = message;
        box.className = `fixed bottom-4 right-4 z-[70] max-w-sm rounded-lg px-4 py-3 text-sm font-semibold shadow-xl ${tone === 'rose' ? 'bg-rose-700 text-white' : 'bg-teal-700 text-white'}`;
        box.classList.remove('hidden');
        clearTimeout(window.vbdToast);
        window.vbdToast = setTimeout(() => box.classList.add('hidden'), 4200);
    }

    async function api(action, options = {}) {
        const response = await fetch(`${API}?action=${encodeURIComponent(action)}&sector=${encodeURIComponent(SECTOR)}`, {
            credentials: 'include',
            cache: 'no-store',
            ...options,
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(data.error || 'Không thể xử lý yêu cầu.');
        return data;
    }

    function scopedDocs() {
        const year = $('academicYearFilter')?.value || '';
        const q = ($('searchInput')?.value || '').trim().toLowerCase();
        const status = $('statusFilter')?.value || '';
        return state.documents.filter(doc => {
            if (year && doc.academic_year !== year) return false;
            if (state.activeDirection && doc.direction !== state.activeDirection) return false;
            if (status && doc.effective_status !== status) return false;
            if (q && !`${doc.document_number} ${doc.title} ${doc.organization} ${doc.summary_text}`.toLowerCase().includes(q)) return false;
            return true;
        });
    }

    function yearScopedDocs() {
        const year = $('academicYearFilter')?.value || '';
        return state.documents.filter(doc => !year || doc.academic_year === year);
    }

    function renderNav() {
        const host = $('vanbanNav');
        if (!host) return;
        const other = SECTOR === 'dang' ? SECTOR_META.hanhchinh : SECTOR_META.dang;
        host.innerHTML = `
            <div class="border-b border-slate-200 bg-white">
                <div class="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-3 lg:flex-row lg:items-center lg:justify-between">
                    <div class="min-w-0">
                        <a href="quanlyvanban.html" class="inline-flex items-center gap-2 text-sm font-semibold text-slate-600 hover:text-slate-900">
                            <i class="fa-solid fa-arrow-left"></i> Quản lý văn bản
                        </a>
                        <h1 class="mt-1 text-xl font-black text-slate-950 sm:text-2xl">
                            <i class="fa-solid ${meta.icon} mr-2 ${meta.accent === 'rose' ? 'text-rose-700' : 'text-teal-700'}"></i>${meta.label}
                        </h1>
                    </div>
                    <div class="flex flex-wrap items-center gap-2">
                        <a href="index.html" class="inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 sm:text-sm">
                            <i class="fa-solid fa-home"></i> Trang chính
                        </a>
                        <a href="${other.page}" class="inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 sm:text-sm">
                            <i class="fa-solid ${other.icon}"></i> ${other.label}
                        </a>
                        <button id="exportExcelBtn" type="button" class="inline-flex items-center gap-2 rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs font-bold text-emerald-800 hover:bg-emerald-100 sm:text-sm">
                            <i class="fa-solid fa-file-excel"></i> Xuất Excel
                        </button>
                        <button id="newDocumentBtn" type="button" class="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-xs font-bold text-white sm:text-sm ${accentPrimary()}">
                            <i class="fa-solid fa-plus"></i> Thêm văn bản
                        </button>
                    </div>
                </div>
            </div>`;
        $('newDocumentBtn')?.addEventListener('click', () => openModal());
        $('exportExcelBtn')?.addEventListener('click', exportExcel);
    }

    function renderSummary() {
        const docs = yearScopedDocs();
        const incoming = docs.filter(d => d.direction === 'incoming').length;
        const outgoing = docs.filter(d => d.direction === 'outgoing').length;
        const needAction = docs.filter(d => ['pending', 'in_progress', 'overdue'].includes(d.effective_status)).length;
        const overdue = docs.filter(d => d.effective_status === 'overdue').length;
        const cards = [
            ['Văn bản đến', incoming, 'text-cyan-700', 'fa-inbox'],
            ['Văn bản đi', outgoing, 'text-indigo-700', 'fa-paper-plane'],
            ['Cần xử lý / báo cáo', needAction, 'text-amber-700', 'fa-clipboard-list'],
            ['Quá hạn', overdue, 'text-rose-700', 'fa-clock'],
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

    function renderDirectionTabs() {
        const docs = yearScopedDocs();
        const incoming = docs.filter(d => d.direction === 'incoming').length;
        const outgoing = docs.filter(d => d.direction === 'outgoing').length;
        const host = $('directionTabs');
        if (!host) return;
        host.innerHTML = ['incoming', 'outgoing'].map(direction => {
            const active = state.activeDirection === direction;
            const count = direction === 'incoming' ? incoming : outgoing;
            const label = direction === 'incoming' ? 'Văn bản đến' : 'Văn bản đi';
            return `<button type="button" data-direction-tab="${direction}" class="rounded-lg px-4 py-2 text-sm font-bold ${accentBtn(active)}">${label} <span class="ml-1 opacity-80">(${count})</span></button>`;
        }).join('');
        host.querySelectorAll('[data-direction-tab]').forEach(button => {
            button.onclick = () => {
                state.activeDirection = button.dataset.directionTab || 'incoming';
                localStorage.setItem(LS_TAB_KEY, state.activeDirection);
                renderDirectionTabs();
                renderList();
                const dirSelect = $('direction');
                if (dirSelect) dirSelect.value = state.activeDirection;
            };
        });
    }

    function driveFileId(file) {
        const direct = String(file?.drive_file_id || '').trim();
        if (direct) return direct;
        const url = String(file?.view_url || '');
        const match = url.match(/\/d\/([A-Za-z0-9_-]+)/) || url.match(/[?&]id=([A-Za-z0-9_-]+)/);
        return match ? match[1] : '';
    }

    function openDrivePreview(fileId, title = 'Tệp đính kèm') {
        if (!fileId) return;
        $('drivePreviewTitle').textContent = title;
        $('drivePreviewFrame').src = `https://drive.google.com/file/d/${encodeURIComponent(fileId)}/preview`;
        $('drivePreviewModal').classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
    }

    function closeDrivePreview() {
        $('drivePreviewModal').classList.add('hidden');
        $('drivePreviewFrame').src = 'about:blank';
        document.body.classList.remove('overflow-hidden');
    }

    function renderList() {
        const docs = scopedDocs();
        $('documentCount').textContent = `Hiển thị ${docs.length}/${state.documents.length} văn bản`;
        const host = $('documentList');
        if (!host) return;
        if (!docs.length) {
            host.innerHTML = '<div class="p-10 text-center text-slate-500"><i class="fa-regular fa-folder-open mb-3 text-3xl"></i><p>Chưa có văn bản trong mục này.</p></div>';
            return;
        }
        host.innerHTML = docs.map(doc => {
            const [label, tone] = statusInfo(doc.effective_status);
            const due = doc.report_required
                ? `<span class="text-xs text-slate-500"><i class="fa-regular fa-calendar mr-1"></i>Hạn: ${dateText(doc.report_due_at)}</span>`
                : '';
            const files = (doc.files || []).map(file => {
                const fileId = driveFileId(file);
                return `<span class="inline-flex max-w-full items-center gap-1.5 rounded bg-slate-100 px-2 py-1 text-xs font-bold text-slate-700">
                    <i class="fa-solid fa-paperclip shrink-0"></i>
                    <span class="truncate">${esc(file.original_name)}</span>
                    ${fileId ? `<button type="button" data-preview-id="${esc(fileId)}" data-preview-title="${esc(file.original_name)}" class="shrink-0 rounded ${accentPrimary()} px-2 py-0.5 text-[11px] font-bold text-white"><i class="fa-solid fa-eye mr-0.5"></i>Xem</button>` : ''}
                </span>`;
            }).join('');
            return `<article class="border-b border-slate-100 p-4 last:border-b-0 hover:bg-slate-50/80">
                <div class="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                    <div class="min-w-0 flex-1">
                        <div class="flex flex-wrap items-center gap-2">
                            <span class="rounded bg-slate-100 px-2 py-1 text-xs font-bold text-slate-700">${esc(doc.academic_year || '')}</span>
                            <span class="rounded-full px-2.5 py-1 text-xs font-bold ${tone}">${label}</span>
                            ${doc.document_number ? `<span class="text-xs font-bold text-slate-600">${esc(doc.document_number)}</span>` : ''}
                        </div>
                        <h3 class="mt-2 text-base font-bold text-slate-900">${esc(doc.title)}</h3>
                        <p class="mt-1 text-sm text-slate-600">${esc(doc.organization || 'Chưa ghi nơi gửi/nhận')}${doc.document_date ? ` · ${dateText(doc.document_date)}` : ''}${doc.document_type ? ` · ${esc(doc.document_type)}` : ''}</p>
                        ${doc.summary_text ? `<p class="mt-2 text-sm leading-6 text-slate-700">${esc(doc.summary_text)}</p>` : ''}
                        <div class="mt-3 flex flex-wrap items-center gap-2">${due}${files}</div>
                    </div>
                    <div class="flex shrink-0 flex-wrap gap-2">
                        <button data-action="edit" data-id="${doc.id}" class="rounded border border-slate-300 bg-white px-3 py-2 text-xs font-bold text-slate-700 hover:bg-slate-100"><i class="fa-solid fa-pen mr-1"></i>Sửa</button>
                        ${doc.report_required && doc.effective_status !== 'completed' ? `<button data-action="progress" data-id="${doc.id}" class="rounded border border-sky-200 bg-sky-50 px-3 py-2 text-xs font-bold text-sky-800 hover:bg-sky-100">Đang xử lý</button><button data-action="complete" data-id="${doc.id}" class="rounded ${accentPrimary()} px-3 py-2 text-xs font-bold text-white">Đã báo cáo</button>` : ''}
                        <button data-action="delete" data-id="${doc.id}" class="rounded border border-rose-200 bg-white px-3 py-2 text-xs font-bold text-rose-700 hover:bg-rose-50"><i class="fa-solid fa-trash"></i></button>
                    </div>
                </div>
            </article>`;
        }).join('');
        host.querySelectorAll('[data-action]').forEach(button => {
            button.onclick = () => handleAction(button.dataset.action, Number(button.dataset.id));
        });
        host.querySelectorAll('[data-preview-id]').forEach(button => {
            button.onclick = () => openDrivePreview(button.dataset.previewId, button.dataset.previewTitle || 'Tệp đính kèm');
        });
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

    function renderReminders() {
        const items = state.documents.map(doc => ({ doc, info: reminderInfo(doc) })).filter(item => item.info).sort((a, b) => a.info.days - b.info.days);
        const panel = $('reminderPanel');
        if (!panel) return;
        if (!items.length) {
            panel.classList.add('hidden');
            return;
        }
        const overdue = items.filter(item => item.info.days < 0).length;
        const urgent = items.length - overdue;
        $('reminderSummary').textContent = `${overdue ? `${overdue} quá hạn` : 'Không có việc quá hạn'}${overdue && urgent ? ' · ' : ''}${urgent ? `${urgent} văn bản đến hạn trong 7 ngày` : ''}.`;
        $('reminderList').innerHTML = items.slice(0, 6).map(({ doc, info }) => `
            <button type="button" data-reminder-id="${doc.id}" class="flex items-center justify-between gap-3 rounded-lg border px-3 py-2.5 text-left ${info.tone === 'rose' ? 'border-rose-200 bg-rose-50 text-rose-950' : info.tone === 'orange' ? 'border-orange-200 bg-orange-50 text-orange-950' : 'border-amber-200 bg-white text-amber-950'} hover:brightness-95">
                <span class="min-w-0">
                    <span class="block truncate font-bold">${esc(doc.title)}</span>
                    <span class="mt-0.5 block text-xs opacity-80">${doc.document_number ? `${esc(doc.document_number)} · ` : ''}Hạn ${dateText(doc.report_due_at)}</span>
                </span>
                <span class="shrink-0 rounded-full px-2 py-1 text-xs font-extrabold ${info.tone === 'rose' ? 'bg-rose-200 text-rose-900' : info.tone === 'orange' ? 'bg-orange-200 text-orange-900' : 'bg-amber-200 text-amber-900'}">${info.label}</span>
            </button>`).join('');
        panel.classList.remove('hidden');
        panel.querySelectorAll('[data-reminder-id]').forEach(button => {
            button.onclick = () => openModal(state.documents.find(doc => Number(doc.id) === Number(button.dataset.reminderId)));
        });
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

    function renderYears() {
        const years = state.schoolYears || [];
        if (!state.yearInitialized) {
            state.selectedYear = years.includes(state.selectedYear) ? state.selectedYear : (years[0] || '');
            state.yearInitialized = true;
        }
        if (state.selectedYear && !years.includes(state.selectedYear)) state.selectedYear = years[0] || '';
        const options = ['<option value="">Tất cả năm học</option>', ...years.map(year => `<option value="${esc(year)}">${esc(year)}</option>`)].join('');
        if ($('academicYearFilter')) {
            $('academicYearFilter').innerHTML = options;
            $('academicYearFilter').value = state.selectedYear;
        }
        if ($('academicYear')) {
            $('academicYear').innerHTML = years.length
                ? years.map(year => `<option value="${esc(year)}">${esc(year)}</option>`).join('')
                : '<option value="">Chưa có năm học — hãy tạo mới</option>';
        }
    }

    function render() {
        renderSummary();
        renderDirectionTabs();
        renderReminders();
        renderDriveWarning();
        renderList();
    }

    function statusLabel(status) {
        return statusInfo(status)[0];
    }

    function exportExcel() {
        const docs = scopedDocs();
        if (!docs.length) {
            toast('Không có văn bản để xuất.', 'rose');
            return;
        }
        const rows = [
            ['Lĩnh vực', 'Loại', 'Năm học', 'Số/Ký hiệu', 'Trích yếu', 'Ngày VB', 'Nơi gửi/nhận', 'Loại VB', 'Hạn báo cáo', 'Trạng thái', 'Tóm tắt', 'Ghi chú', 'Tệp đính kèm'],
            ...docs.map(doc => [
                meta.label,
                doc.direction === 'outgoing' ? 'Văn bản đi' : 'Văn bản đến',
                doc.academic_year || '',
                doc.document_number || '',
                doc.title || '',
                doc.document_date || '',
                doc.organization || '',
                doc.document_type || '',
                doc.report_due_at || '',
                statusLabel(doc.effective_status),
                doc.summary_text || '',
                doc.report_note || '',
                (doc.files || []).map(f => f.original_name).join('; '),
            ]),
        ];
        const csv = '\ufeff' + rows.map(row => row.map(v => `"${String(v ?? '').replace(/"/g, '""')}"`).join(',')).join('\r\n');
        const a = document.createElement('a');
        a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
        a.download = `van-ban-${SECTOR}-${state.activeDirection}-${new Date().toISOString().slice(0, 10)}.csv`;
        a.click();
        URL.revokeObjectURL(a.href);
        toast('Đã xuất file Excel (CSV).');
    }

    async function load() {
        try {
            const data = await api('list');
            state.documents = data.documents || [];
            state.schoolYears = data.school_years || [];
            state.driveConfigured = !!data.drive_configured;
            state.driveReady = !!data.drive_ready;
            state.driveHint = data.drive_hint || '';
            state.driveDiag = data;
            renderYears();
            render();
        } catch (error) {
            toast(error.message, 'rose');
        }
    }

    function setReportVisibility() {
        $('reportFields')?.classList.toggle('hidden', !$('reportRequired')?.checked);
    }

    function setDocumentType(value) {
        const select = $('documentType');
        if (!select) return;
        const type = String(value || '').trim();
        select.querySelectorAll('[data-custom-document-type]').forEach(option => option.remove());
        if (type && ![...select.options].some(option => option.value === type)) {
            const option = new Option(`${type} (khác)`, type);
            option.dataset.customDocumentType = '1';
            select.add(option);
        }
        select.value = type;
    }

    function openModal(doc = null) {
        $('documentForm')?.reset();
        $('formError')?.classList.add('hidden');
        if ($('documentId')) $('documentId').value = doc?.id || '';
        if ($('modalTitle')) $('modalTitle').textContent = doc ? 'Cập nhật văn bản' : `Thêm văn bản · ${meta.label}`;
        if ($('academicYear')) $('academicYear').value = doc?.academic_year || state.selectedYear || '';
        if ($('direction')) $('direction').value = doc?.direction || state.activeDirection || 'incoming';
        if ($('documentNumber')) $('documentNumber').value = doc?.document_number || '';
        if ($('title')) $('title').value = doc?.title || '';
        if ($('documentDate')) $('documentDate').value = doc?.document_date || '';
        setDocumentType(doc?.document_type);
        if ($('organization')) $('organization').value = doc?.organization || '';
        if ($('summaryText')) $('summaryText').value = doc?.summary_text || '';
        if ($('sourceText')) $('sourceText').value = doc?.source_text || '';
        if ($('reportRequired')) $('reportRequired').checked = !!Number(doc?.report_required || 0);
        if ($('reportDueAt')) $('reportDueAt').value = doc?.report_due_at || '';
        if ($('reportStatus')) $('reportStatus').value = ['pending', 'in_progress', 'completed'].includes(doc?.report_status) ? doc.report_status : 'pending';
        if ($('reportNote')) $('reportNote').value = doc?.report_note || '';
        $('parseNote')?.classList.add('hidden');
        setReportVisibility();
        $('documentModal')?.classList.remove('hidden');
    }

    function closeModal() {
        $('documentModal')?.classList.add('hidden');
    }

    async function handleAction(action, id) {
        const doc = state.documents.find(item => Number(item.id) === id);
        if (!doc) return;
        if (action === 'edit') return openModal(doc);
        if (action === 'delete') {
            const count = (doc.files || []).length;
            if (!confirm(`XÓA VĨNH VIỄN văn bản “${doc.title}”?\n\nThao tác này sẽ xóa danh mục và ${count} tệp đính kèm trên Google Drive.`)) return;
            try {
                const data = await api('delete', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id }) });
                toast(data.message || 'Đã xóa văn bản và tệp trên Google Drive.');
                load();
            } catch (error) {
                toast(error.message, 'rose');
            }
            return;
        }
        const status = action === 'complete' ? 'completed' : 'in_progress';
        try {
            await api('update_status', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id, report_status: status }) });
            toast(status === 'completed' ? 'Đã xác nhận hoàn thành báo cáo.' : 'Đã chuyển sang đang xử lý.');
            load();
        } catch (error) {
            toast(error.message, 'rose');
        }
    }

    function meaningfulTextLength(text) {
        return String(text || '').replace(/\s+/g, '').length;
    }

    async function extractPdfTextLayer(file) {
        if (!window.pdfjsLib) throw new Error('Chưa tải được công cụ đọc PDF.');
        window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        const pdf = await window.pdfjsLib.getDocument({ data: await file.arrayBuffer() }).promise;
        const pages = [];
        for (let i = 1; i <= Math.min(pdf.numPages, 12); i++) {
            const page = await pdf.getPage(i);
            const content = await page.getTextContent();
            pages.push(content.items.map(item => item.str).join(' '));
        }
        return pages.join('\n').replace(/[ \t]+/g, ' ').trim();
    }

    function hasMistralOcr() {
        return window.MistralOcr
            && window.AiDesignConfig
            && AiDesignConfig.isMistralEnabled()
            && AiDesignConfig.getMistralKeys().length > 0;
    }

    async function extractPdfOcr(file) {
        if (!hasMistralOcr()) {
            throw new Error('PDF scan/ảnh cần Mistral OCR. Admin bật và nạp key trong global_config.json.');
        }
        const result = await MistralOcr.ocrPdfFile(file);
        const text = (result.pages || []).map(page => page.ocr_text || '').filter(Boolean).join('\n\n').trim();
        if (meaningfulTextLength(text) < 20) {
            throw new Error('Mistral OCR không đọc được chữ từ PDF này.');
        }
        return text;
    }

    async function extractPdf(file) {
        let text = '';
        let mode = 'text-layer';
        try {
            text = await extractPdfTextLayer(file);
        } catch {
            text = '';
        }
        if (meaningfulTextLength(text) < 80) {
            text = await extractPdfOcr(file);
            mode = 'mistral-ocr';
        }
        if (meaningfulTextLength(text) < 20) {
            throw new Error('Không đọc được nội dung PDF. Dán thủ công phần đầu văn bản (số, ngày, trích yếu).');
        }
        return { text, mode };
    }

    let parseTimer = null;
    let parseBusy = false;

    function applyParsedFields(item) {
        if (!item || typeof item !== 'object') return 0;
        let filled = 0;
        const setValue = (id, value) => {
            const el = $(id);
            const next = String(value ?? '').trim();
            if (!el || !next) return;
            el.value = next;
            filled += 1;
        };
        setValue('documentNumber', item.document_number);
        setValue('title', item.title);
        setValue('organization', item.organization);
        if (item.document_type) setDocumentType(item.document_type);
        setValue('summaryText', item.summary_text);
        setValue('documentDate', item.document_date);
        if ($('reportRequired')) $('reportRequired').checked = !!item.report_required;
        setValue('reportDueAt', item.report_due_at);
        setReportVisibility();
        return filled;
    }

    function showParseNote(item, filled) {
        const note = $('parseNote');
        if (!note) return;
        const confidence = item.confidence || 'medium';
        const detail = item.note ? ` · ${item.note}` : '';
        note.textContent = `Tự nhận diện: đã điền ${filled} trường · độ tin cậy ${confidence}${detail}. Kiểm tra trước khi lưu.`;
        note.classList.remove('hidden');
    }

    async function runAutoParse(options = {}) {
        const source = $('sourceText')?.value.trim() || '';
        if (source.length < 20) {
            if (!options.silent) toast('Hãy dán nội dung văn bản hoặc chọn PDF trước.', 'rose');
            return null;
        }
        if (parseBusy) return null;
        parseBusy = true;
        const note = $('parseNote');
        if (note) {
            note.textContent = 'Đang nhận diện thông tin từ văn bản...';
            note.classList.remove('hidden');
        }
        try {
            const data = await api('parse_document', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source_text: source }),
            });
            const item = data.suggestion || {};
            const filled = applyParsedFields(item);
            showParseNote(item, filled);
            if (!filled && !options.silent) {
                toast('Không nhận diện được trường nào. Thử dán phần đầu văn bản hoặc PDF có chữ rõ.', 'rose');
            } else if (!options.silent && filled) {
                toast(`Đã tự điền ${filled} trường từ văn bản.`);
            }
            return item;
        } catch (error) {
            if (note) note.textContent = error.message;
            if (!options.silent) toast(error.message, 'rose');
            throw error;
        } finally {
            parseBusy = false;
        }
    }

    function scheduleAutoParse() {
        clearTimeout(parseTimer);
        parseTimer = setTimeout(() => runAutoParse({ silent: true }), 600);
    }

    async function uploadFiles(documentId) {
        const files = $('files')?.files;
        if (!files?.length) return;
        const form = new FormData();
        form.append('document_id', documentId);
        [...files].forEach(file => form.append('files[]', file));
        const response = await fetch(`${API}?action=upload&sector=${encodeURIComponent(SECTOR)}`, { method: 'POST', credentials: 'include', body: form });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(data.error || 'Không tải được tệp lên Google Drive.');
    }

    function bindEvents() {
        $('documentForm')?.addEventListener('submit', async event => {
            event.preventDefault();
            const button = $('saveDocumentBtn');
            const original = button?.innerHTML || '';
            if (button) {
                button.disabled = true;
                button.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i>Đang lưu...';
            }
            try {
                const data = await api('save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        id: Number($('documentId')?.value) || 0,
                        sector: SECTOR,
                        academic_year: $('academicYear')?.value,
                        direction: $('direction')?.value,
                        document_number: $('documentNumber')?.value,
                        title: $('title')?.value,
                        document_date: $('documentDate')?.value,
                        document_type: $('documentType')?.value,
                        organization: $('organization')?.value,
                        summary_text: $('summaryText')?.value,
                        source_text: $('sourceText')?.value,
                        report_required: $('reportRequired')?.checked,
                        report_due_at: $('reportDueAt')?.value,
                        report_status: $('reportStatus')?.value,
                        report_note: $('reportNote')?.value,
                    }),
                });
                await uploadFiles(data.document.id);
                closeModal();
                toast('Đã lưu văn bản.');
                load();
            } catch (error) {
                if ($('formError')) {
                    $('formError').textContent = error.message;
                    $('formError').classList.remove('hidden');
                }
            } finally {
                if (button) {
                    button.disabled = false;
                    button.innerHTML = original;
                }
            }
        });

        $('sourceText')?.addEventListener('input', scheduleAutoParse);

        $('files')?.addEventListener('change', async event => {
            const file = [...event.target.files].find(item => item.type === 'application/pdf' || item.name.toLowerCase().endsWith('.pdf'));
            if (!file || !$('parseNote') || !$('sourceText')) return;
            $('parseNote').textContent = 'Đang đọc PDF (lớp chữ hoặc Mistral OCR)...';
            $('parseNote').classList.remove('hidden');
            try {
                const extracted = await extractPdf(file);
                const mode = extracted.mode === 'mistral-ocr' ? 'Mistral OCR' : 'lớp chữ PDF';
                $('sourceText').value = extracted.text;
                $('parseNote').textContent = `Đã đọc PDF bằng ${mode}. Đang tự điền thông tin...`;
                await runAutoParse({ silent: true });
            } catch (error) {
                $('parseNote').textContent = error.message;
                toast(error.message, 'rose');
            }
        });

        $('newSchoolYearBtn')?.addEventListener('click', async () => {
            const year = prompt('Nhập năm học, ví dụ: 2025-2026');
            if (year === null) return;
            try {
                const data = await api('create_school_year', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ academic_year: year }) });
                state.selectedYear = data.academic_year;
                localStorage.setItem(LS_YEAR_KEY, state.selectedYear);
                toast(data.message);
                await load();
            } catch (error) {
                toast(error.message, 'rose');
            }
        });

        $('closeModalBtn')?.addEventListener('click', closeModal);
        $('cancelModalBtn')?.addEventListener('click', closeModal);
        $('closeDrivePreviewBtn')?.addEventListener('click', closeDrivePreview);
        $('drivePreviewModal')?.addEventListener('click', event => { if (event.target === $('drivePreviewModal')) closeDrivePreview(); });
        $('documentModal')?.addEventListener('click', event => { if (event.target === $('documentModal')) closeModal(); });
        $('reportRequired')?.addEventListener('change', setReportVisibility);
        $('academicYearFilter')?.addEventListener('change', event => {
            state.selectedYear = event.target.value;
            localStorage.setItem(LS_YEAR_KEY, state.selectedYear);
            render();
        });
        $('statusFilter')?.addEventListener('change', render);
        $('searchInput')?.addEventListener('input', render);
    }

    function init() {
        renderNav();
        bindEvents();
        if ($('direction')) $('direction').value = state.activeDirection;
        load();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();