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

    const DOCUMENT_TYPES = [
        'Công văn', 'Thông báo', 'Quyết định', 'Nghị quyết', 'Chỉ thị',
        'Kế hoạch', 'Hướng dẫn', 'Thông tư', 'Quy định', 'Tờ trình',
        'Báo cáo', 'Triển khai',
    ];

    const state = {
        documents: [],
        schoolYears: [],
        selectedYear: localStorage.getItem(LS_YEAR_KEY) || '',
        yearInitialized: false,
        activeDirection: localStorage.getItem(LS_TAB_KEY) || 'incoming',
        statusFilter: '',
        typeFilter: '',
        search: '',
        detailDocId: null,
        driveConfigured: false,
        driveReady: false,
        driveProven: false,
        driveHint: '',
        driveDiag: {},
        pendingUploadFiles: [],
        uploadMaxBytes: null,
        postMaxBytes: null,
        appMaxFileMb: 25,
    };

    function parseIniSize(value) {
        const match = String(value || '').trim().match(/^(\d+(?:\.\d+)?)\s*([KMG])?$/i);
        if (!match) return null;
        const amount = Number(match[1]);
        const unit = (match[2] || '').toUpperCase();
        const mult = unit === 'G' ? 1024 ** 3 : unit === 'M' ? 1024 ** 2 : unit === 'K' ? 1024 : 1;
        return Math.floor(amount * mult);
    }

    function effectiveUploadMaxBytes() {
        const appMax = (state.appMaxFileMb || 25) * 1024 * 1024;
        if (state.driveReady) return appMax;
        const limits = [appMax, state.uploadMaxBytes, state.postMaxBytes].filter(n => Number.isFinite(n) && n > 0);
        return limits.length ? Math.min(...limits) : appMax;
    }

    function formatBytes(bytes) {
        if (!Number.isFinite(bytes) || bytes <= 0) return '0 B';
        if (bytes >= 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
        if (bytes >= 1024) return `${Math.round(bytes / 1024)} KB`;
        return `${bytes} B`;
    }

    const $ = id => document.getElementById(id);
    const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[ch]));

    const statusInfo = status => ({
        not_required: ['Không cần báo cáo', 'bg-slate-100 text-slate-700'],
        pending: ['Chưa xử lý', 'bg-amber-100 text-amber-800'],
        in_progress: ['Đang xử lý', 'bg-sky-100 text-sky-800'],
        completed: ['Đã báo cáo', 'bg-teal-100 text-teal-800'],
        aware: ['Chỉ biết', 'bg-slate-100 text-slate-700'],
        overdue: ['Quá hạn', 'bg-rose-100 text-rose-800'],
    }[status] || ['Chưa xử lý', 'bg-amber-100 text-amber-800']);

    const isResolvedReportStatus = status => status === 'completed' || status === 'aware';

    const documentTypeTone = type => ({
        'Quyết định': 'bg-violet-100 text-violet-800',
        'Nghị quyết': 'bg-purple-100 text-purple-800',
        'Hướng dẫn': 'bg-blue-100 text-blue-800',
        'Thông tư': 'bg-cyan-100 text-cyan-800',
        'Kế hoạch': 'bg-indigo-100 text-indigo-800',
        'Công văn': 'bg-slate-200 text-slate-800',
        'Thông báo': 'bg-sky-100 text-sky-800',
        'Tờ trình': 'bg-amber-100 text-amber-900',
        'Báo cáo': 'bg-emerald-100 text-emerald-800',
        'Quy định': 'bg-rose-100 text-rose-800',
        'Chỉ thị': 'bg-orange-100 text-orange-900',
        'Triển khai': 'bg-teal-100 text-teal-800',
    }[type] || 'bg-slate-100 text-slate-700');

    const dateText = value => value ? new Date(`${value}T00:00:00`).toLocaleDateString('vi-VN') : '—';

    function formatYMDToDMY(ymd) {
        if (!ymd || typeof ymd !== 'string') return '';
        const m = ymd.match(/^(\d{4})-(\d{2})-(\d{2})$/);
        if (m) return `${m[3]}/${m[2]}/${m[1]}`;
        return ymd;
    }

    function parseDMYToYMD(dmy) {
        if (!dmy || typeof dmy !== 'string') return '';
        const m = dmy.match(/^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})$/);
        if (m) {
            const d = m[1].padStart(2, '0');
            const mo = m[2].padStart(2, '0');
            const y = m[3];
            return `${y}-${mo}-${d}`;
        }
        // fallback if already YMD
        if (/^\d{4}-\d{2}-\d{2}$/.test(dmy)) return dmy;
        return '';
    }

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
        const driveQuery = action === 'list' ? '&with_drive=1' : '';
        const response = await fetch(`${API}?action=${encodeURIComponent(action)}&sector=${encodeURIComponent(SECTOR)}${driveQuery}`, {
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
        const docType = $('typeFilter')?.value || state.typeFilter || '';
        return state.documents.filter(doc => {
            if (year && doc.academic_year !== year) return false;
            if (state.activeDirection && doc.direction !== state.activeDirection) return false;
            if (status && doc.effective_status !== status) return false;
            if (docType && doc.document_type !== docType) return false;
            if (q && !`${doc.document_number} ${doc.title} ${doc.organization} ${doc.summary_text} ${doc.document_type}`.toLowerCase().includes(q)) return false;
            return true;
        }).sort((a, b) => {
            const da = a.document_date || '';
            const db = b.document_date || '';
            if (da !== db) return db.localeCompare(da);
            return String(a.title || '').localeCompare(String(b.title || ''), 'vi');
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

    function isLocalFile(file) {
        const id = String(file?.drive_file_id || '').trim();
        const url = String(file?.view_url || '');
        return id.startsWith('local:') || url.includes('action=file');
    }

    function driveFileId(file) {
        const direct = String(file?.drive_file_id || '').trim();
        if (direct.startsWith('local:')) return '';
        if (direct) return direct;
        const url = String(file?.view_url || '');
        const match = url.match(/\/d\/([A-Za-z0-9_-]+)/) || url.match(/[?&]id=([A-Za-z0-9_-]+)/);
        return match ? match[1] : '';
    }

    function renderFileChip(doc, file) {
        const fileId = driveFileId(file);
        const previewUrl = isLocalFile(file) ? String(file.view_url || '') : '';
        const canPreview = fileId || previewUrl;
        const dbFileId = Number(file.id || 0);
        return `<span class="inline-flex max-w-full items-center gap-1.5 rounded bg-slate-100 px-2 py-1 text-xs font-bold text-slate-700">
            <i class="fa-solid fa-paperclip shrink-0"></i>
            <span class="truncate">${esc(file.original_name)}</span>
            ${canPreview ? `<button type="button" data-preview-id="${esc(fileId)}" data-preview-url="${esc(previewUrl)}" data-preview-title="${esc(file.original_name)}" class="shrink-0 rounded ${accentPrimary()} px-2 py-0.5 text-[11px] font-bold text-white"><i class="fa-solid fa-eye mr-0.5"></i>Xem</button>` : ''}
            ${dbFileId ? `<button type="button" data-delete-file-id="${dbFileId}" data-doc-id="${doc.id}" data-file-name="${esc(file.original_name)}" class="shrink-0 rounded border border-rose-200 bg-white px-2 py-0.5 text-[11px] font-bold text-rose-700 hover:bg-rose-50" title="Xóa tệp này"><i class="fa-solid fa-trash-can"></i></button>` : ''}
        </span>`;
    }

    function ensureExistingFilesPanel() {
        let panel = $('existingFilesPanel');
        if (panel) return panel;
        const anchor = $('selectedFilesNote') || $('files');
        if (!anchor) return null;
        panel = document.createElement('div');
        panel.id = 'existingFilesPanel';
        panel.className = 'hidden rounded-lg border border-slate-200 bg-slate-50 p-3';
        anchor.parentElement?.insertBefore(panel, anchor);
        return panel;
    }

    function renderExistingFilesInModal(doc) {
        const panel = ensureExistingFilesPanel();
        if (!panel) return;
        const files = doc?.files || [];
        if (!files.length) {
            panel.classList.add('hidden');
            panel.innerHTML = '';
            return;
        }
        panel.classList.remove('hidden');
        panel.innerHTML = `
            <p class="mb-2 text-xs font-bold text-slate-700">Tệp đã đính kèm (${files.length})</p>
            <div class="flex flex-wrap gap-2">${files.map(file => renderFileChip(doc, file)).join('')}</div>
            <p class="mt-2 text-[11px] text-slate-500">Bấm <i class="fa-solid fa-trash-can"></i> để xóa tệp thừa. Thêm tệp mới ở ô bên dưới.</p>`;
        bindFileActions(panel);
    }

    async function deleteAttachedFile(documentId, fileId, fileName) {
        if (!confirm(`Xóa tệp “${fileName}”?\n\nTệp sẽ bị xóa khỏi Drive/hosting và danh mục văn bản.`)) return;
        try {
            const data = await api('delete_file', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ document_id: documentId, file_id: fileId }),
            });
            toast(data.message || 'Đã xóa tệp đính kèm.');
            await load();
            const doc = state.documents.find(item => Number(item.id) === Number(documentId));
            if ($('documentModal') && !$('documentModal').classList.contains('hidden')) {
                openModal(doc || null);
            }
        } catch (error) {
            toast(error.message, 'rose');
        }
    }

    function bindFileActions(root) {
        if (!root) return;
        root.querySelectorAll('[data-preview-id], [data-preview-url]').forEach(button => {
            button.onclick = event => {
                event.preventDefault();
                event.stopPropagation();
                openDrivePreview(
                    button.dataset.previewId || '',
                    button.dataset.previewTitle || 'Tệp đính kèm',
                    button.dataset.previewUrl || ''
                );
            };
        });
        root.querySelectorAll('[data-delete-file-id]').forEach(button => {
            button.onclick = event => {
                event.preventDefault();
                event.stopPropagation();
                deleteAttachedFile(
                    Number(button.dataset.docId),
                    Number(button.dataset.deleteFileId),
                    button.dataset.fileName || 'tệp đính kèm'
                );
            };
        });
    }

    function openDrivePreview(fileId, title = 'Tệp đính kèm', directUrl = '') {
        const src = directUrl || (fileId ? `https://drive.google.com/file/d/${encodeURIComponent(fileId)}/preview` : '');
        if (!src) return;
        $('drivePreviewTitle').textContent = title;
        $('drivePreviewFrame').src = src;
        $('drivePreviewModal').classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
    }

    function closeDrivePreview() {
        $('drivePreviewModal').classList.add('hidden');
        $('drivePreviewFrame').src = 'about:blank';
        document.body.classList.remove('overflow-hidden');
    }

    function renderTypeFilter() {
        const select = $('typeFilter');
        if (!select) return;
        const current = select.value || state.typeFilter || '';
        const typesInData = [...new Set(state.documents.map(doc => doc.document_type).filter(Boolean))];
        const allTypes = [...new Set([...DOCUMENT_TYPES, ...typesInData])].sort((a, b) => a.localeCompare(b, 'vi'));
        select.innerHTML = ['<option value="">Tất cả loại</option>', ...allTypes.map(type => `<option value="${esc(type)}">${esc(type)}</option>`)].join('');
        select.value = allTypes.includes(current) || current === '' ? current : '';
        state.typeFilter = select.value;
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
        host.innerHTML = `
            <div class="overflow-x-auto">
                <table class="min-w-full text-left text-sm">
                    <thead class="border-b border-slate-200 bg-slate-50 text-xs font-bold uppercase tracking-wide text-slate-600">
                        <tr>
                            <th class="w-12 px-3 py-3 text-center">STT</th>
                            <th class="min-w-[120px] px-3 py-3">Số/KH</th>
                            <th class="min-w-[100px] px-3 py-3">Loại VB</th>
                            <th class="min-w-[280px] px-3 py-3">Trích yếu</th>
                            <th class="min-w-[90px] px-3 py-3">Ngày VB</th>
                            <th class="min-w-[110px] px-3 py-3">Báo cáo</th>
                            <th class="min-w-[120px] px-3 py-3 text-right">Thao tác</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${docs.map((doc, index) => {
                            const [label, tone] = statusInfo(doc.effective_status);
                            const typeBadge = doc.document_type
                                ? `<span class="inline-block rounded-full px-2 py-0.5 text-[11px] font-bold ${documentTypeTone(doc.document_type)}">${esc(doc.document_type)}</span>`
                                : '<span class="text-xs text-slate-400">—</span>';
                            return `<tr class="border-b border-slate-100 hover:bg-slate-50/80">
                                <td class="px-3 py-3 text-center font-bold text-slate-500">${index + 1}</td>
                                <td class="px-3 py-3 align-top">
                                    <div class="font-bold text-slate-800">${doc.document_number ? esc(doc.document_number) : '—'}</div>
                                    <div class="mt-1 text-[11px] text-slate-500">${esc(doc.academic_year || '')}</div>
                                </td>
                                <td class="px-3 py-3 align-top">${typeBadge}</td>
                                <td class="px-3 py-3 align-top">
                                    <button type="button" data-view-id="${doc.id}" class="text-left font-bold text-slate-900 ${meta.accent === 'rose' ? 'hover:text-rose-700' : 'hover:text-teal-700'} hover:underline">${esc(doc.title)}</button>
                                    <p class="mt-1 line-clamp-2 text-xs text-slate-500">${esc(doc.organization || 'Chưa ghi nơi gửi/nhận')}</p>
                                </td>
                                <td class="px-3 py-3 align-top text-slate-700">${doc.document_date ? dateText(doc.document_date) : '—'}</td>
                                <td class="px-3 py-3 align-top">
                                    <span class="inline-block rounded-full px-2 py-0.5 text-[11px] font-bold ${tone}">${label}</span>
                                    ${doc.report_required && doc.report_due_at ? `<div class="mt-1 text-[11px] text-slate-500">Hạn ${dateText(doc.report_due_at)}</div>` : ''}
                                </td>
                                <td class="px-3 py-3 align-top">
                                    <div class="flex flex-wrap justify-end gap-1">
                                        <button data-action="edit" data-id="${doc.id}" class="rounded border border-slate-300 bg-white px-2 py-1 text-[11px] font-bold text-slate-700 hover:bg-slate-100" title="Sửa"><i class="fa-solid fa-pen"></i></button>
                                        ${doc.report_required && !isResolvedReportStatus(doc.effective_status) ? `<button data-action="progress" data-id="${doc.id}" class="rounded border border-sky-200 bg-sky-50 px-2 py-1 text-[11px] font-bold text-sky-800" title="Đang xử lý"><i class="fa-solid fa-spinner"></i></button><button data-action="aware" data-id="${doc.id}" class="rounded border border-slate-300 bg-slate-50 px-2 py-1 text-[11px] font-bold text-slate-700" title="Chỉ biết"><i class="fa-solid fa-eye"></i></button><button data-action="complete" data-id="${doc.id}" class="rounded ${accentPrimary()} px-2 py-1 text-[11px] font-bold text-white" title="Đã báo cáo"><i class="fa-solid fa-check"></i></button>` : ''}
                                        <button data-action="delete" data-id="${doc.id}" class="rounded border border-rose-200 bg-white px-2 py-1 text-[11px] font-bold text-rose-700 hover:bg-rose-50" title="Xóa"><i class="fa-solid fa-trash"></i></button>
                                    </div>
                                </td>
                            </tr>`;
                        }).join('')}
                    </tbody>
                </table>
            </div>
            <p class="border-t border-slate-100 px-4 py-2 text-xs text-slate-500"><i class="fa-solid fa-circle-info mr-1"></i>Bấm <strong>trích yếu</strong> để xem đầy đủ nội dung, tóm tắt và tệp đính kèm.</p>`;
        host.querySelectorAll('[data-action]').forEach(button => {
            button.onclick = () => handleAction(button.dataset.action, Number(button.dataset.id));
        });
        host.querySelectorAll('[data-view-id]').forEach(button => {
            button.onclick = () => openDetailModal(state.documents.find(doc => Number(doc.id) === Number(button.dataset.viewId)));
        });
        bindFileActions(host);
    }

    function openDetailModal(doc) {
        if (!doc) return;
        state.detailDocId = doc.id;
        const modal = $('documentDetailModal');
        const body = $('detailBody');
        const actions = $('detailActions');
        if (!modal || !body || !actions) return openModal(doc);

        const [label, tone] = statusInfo(doc.effective_status);
        const files = (doc.files || []).map(file => renderFileChip(doc, file)).join('') || '<span class="text-sm text-slate-500">Chưa có tệp đính kèm.</span>';

        if ($('detailTitle')) $('detailTitle').textContent = doc.title || 'Văn bản';
        if ($('detailSubtitle')) {
            $('detailSubtitle').innerHTML = [
                doc.document_number ? `<span class="font-bold">${esc(doc.document_number)}</span>` : '',
                doc.document_type ? `<span class="rounded-full px-2 py-0.5 text-xs font-bold ${documentTypeTone(doc.document_type)}">${esc(doc.document_type)}</span>` : '',
                doc.document_date ? `<span>${dateText(doc.document_date)}</span>` : '',
                `<span class="rounded-full px-2 py-0.5 text-xs font-bold ${tone}">${label}</span>`,
            ].filter(Boolean).join(' · ');
        }

        body.innerHTML = `
            <div class="grid gap-3 sm:grid-cols-2">
                <div class="rounded-lg border border-slate-200 bg-slate-50 p-3">
                    <div class="text-[11px] font-bold uppercase text-slate-500">Năm học</div>
                    <div class="mt-1 font-semibold text-slate-900">${esc(doc.academic_year || '—')}</div>
                </div>
                <div class="rounded-lg border border-slate-200 bg-slate-50 p-3">
                    <div class="text-[11px] font-bold uppercase text-slate-500">Loại danh mục</div>
                    <div class="mt-1 font-semibold text-slate-900">${doc.direction === 'outgoing' ? 'Văn bản đi' : 'Văn bản đến'}</div>
                </div>
                <div class="rounded-lg border border-slate-200 bg-slate-50 p-3 sm:col-span-2">
                    <div class="text-[11px] font-bold uppercase text-slate-500">Nơi gửi / nhận</div>
                    <div class="mt-1 font-semibold text-slate-900">${esc(doc.organization || 'Chưa ghi')}</div>
                </div>
            </div>
            ${doc.summary_text ? `<section><h3 class="text-sm font-bold text-slate-800">Tóm tắt việc cần làm</h3><p class="mt-2 whitespace-pre-line text-sm leading-6 text-slate-700">${esc(doc.summary_text)}</p></section>` : ''}
            ${Number(doc.report_required) ? `<section class="rounded-xl border border-amber-200 bg-amber-50 p-4"><h3 class="text-sm font-bold text-amber-950">Theo dõi báo cáo</h3><p class="mt-2 text-sm text-amber-900">Hạn: <strong>${dateText(doc.report_due_at)}</strong>${doc.report_note ? ` · ${esc(doc.report_note)}` : ''}</p></section>` : ''}
            <section><h3 class="text-sm font-bold text-slate-800">Tệp đính kèm</h3><div class="mt-2 flex flex-wrap gap-2">${files}</div></section>`;

        actions.innerHTML = `
            <button type="button" data-detail-action="edit" data-id="${doc.id}" class="rounded border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:bg-slate-100"><i class="fa-solid fa-pen mr-1"></i>Sửa</button>
            ${doc.report_required && !isResolvedReportStatus(doc.effective_status) ? `<button type="button" data-detail-action="progress" data-id="${doc.id}" class="rounded border border-sky-200 bg-sky-50 px-4 py-2 text-sm font-bold text-sky-800">Đang xử lý</button><button type="button" data-detail-action="aware" data-id="${doc.id}" class="rounded border border-slate-300 bg-slate-50 px-4 py-2 text-sm font-bold text-slate-700">Chỉ biết</button><button type="button" data-detail-action="complete" data-id="${doc.id}" class="rounded ${accentPrimary()} px-4 py-2 text-sm font-bold text-white">Đã báo cáo</button>` : ''}
            <button type="button" id="closeDetailFooterBtn" class="ml-auto rounded border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:bg-slate-50">Đóng</button>`;

        actions.querySelectorAll('[data-detail-action]').forEach(button => {
            button.onclick = async () => {
                const id = Number(button.dataset.id);
                closeDetailModal();
                await handleAction(button.dataset.detailAction, id);
            };
        });
        $('closeDetailFooterBtn')?.addEventListener('click', closeDetailModal, { once: true });
        bindFileActions(body);
        modal.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
    }

    function closeDetailModal() {
        $('documentDetailModal')?.classList.add('hidden');
        state.detailDocId = null;
        document.body.classList.remove('overflow-hidden');
    }

    function reminderInfo(doc) {
        if (!Number(doc.report_required) || isResolvedReportStatus(doc.effective_status) || !doc.report_due_at) return null;
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
            button.onclick = () => openDetailModal(state.documents.find(doc => Number(doc.id) === Number(button.dataset.reminderId)));
        });
    }

    function applyDriveStatus(data) {
        state.driveProven = !!data.drive_proven;
        state.driveConfigured = !!data.drive_configured || state.driveProven;
        state.driveReady = !!data.drive_ready || state.driveProven;
        state.driveHint = data.drive_hint || '';
    }

    function renderDriveWarning() {
        const box = $('driveWarning');
        if (!box) return;
        if (state.driveReady || state.driveConfigured) {
            box.classList.add('hidden');
            return;
        }
        const hint = state.driveHint || 'Chưa cấu hình GOOGLE_DRIVE trong api/config.php.';
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
        renderTypeFilter();
        renderSummary();
        renderDirectionTabs();
        renderReminders();
        renderDriveWarning();
        renderList();
        if (state.detailDocId) {
            const doc = state.documents.find(item => Number(item.id) === Number(state.detailDocId));
            if (doc) openDetailModal(doc);
            else closeDetailModal();
        }
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

    async function checkDriveRemote() {
        try {
            const data = await api('drive_check');
            // Remote probe may fail while uploads still work — only upgrade status, never downgrade.
            if (data.drive_configured) state.driveConfigured = true;
            if (data.drive_ready) state.driveReady = true;
            if (!state.driveReady && data.drive_hint) state.driveHint = data.drive_hint;
            state.uploadMaxBytes = parseIniSize(data.upload_max_filesize);
            state.postMaxBytes = parseIniSize(data.post_max_size);
            state.appMaxFileMb = Number(data.app_max_file_mb) || 25;
            renderDriveWarning();
        } catch (_) {
            // Keep list response values when remote check is unavailable.
        }
    }

    async function load() {
        try {
            const data = await api('list');
            state.documents = data.documents || [];
            state.schoolYears = data.school_years || [];
            applyDriveStatus(data);
            state.driveDiag = data;
            renderYears();
            render();
            checkDriveRemote();
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
        state.pendingUploadFiles = [];
        $('documentForm')?.reset();
        $('formError')?.classList.add('hidden');
        if ($('selectedFilesNote')) {
            $('selectedFilesNote').textContent = 'Có thể chọn nhiều tệp, gồm ZIP/RAR/7Z · tối đa 25 MB cho mỗi tệp.';
        }
        if ($('documentId')) $('documentId').value = doc?.id || '';
        if ($('modalTitle')) $('modalTitle').textContent = doc ? 'Cập nhật văn bản' : `Thêm văn bản · ${meta.label}`;
        if ($('academicYear')) $('academicYear').value = doc?.academic_year || state.selectedYear || '';
        if ($('direction')) $('direction').value = doc?.direction || state.activeDirection || 'incoming';
        if ($('documentNumber')) $('documentNumber').value = doc?.document_number || '';
        if ($('title')) $('title').value = doc?.title || '';
        if ($('documentDate')) $('documentDate').value = formatYMDToDMY(doc?.document_date) || '';
        setDocumentType(doc?.document_type);
        if ($('organization')) $('organization').value = doc?.organization || '';
        if ($('summaryText')) $('summaryText').value = doc?.summary_text || '';
        if ($('sourceText')) $('sourceText').value = doc?.source_text || '';
        if ($('reportRequired')) $('reportRequired').checked = !!Number(doc?.report_required || 0);
        if ($('reportDueAt')) $('reportDueAt').value = formatYMDToDMY(doc?.report_due_at) || '';
        if ($('reportStatus')) $('reportStatus').value = ['pending', 'in_progress', 'completed', 'aware'].includes(doc?.report_status) ? doc.report_status : 'pending';
        if ($('reportNote')) $('reportNote').value = doc?.report_note || '';
        $('parseNote')?.classList.add('hidden');
        setReportVisibility();
        renderExistingFilesInModal(doc);
        $('documentModal')?.classList.remove('hidden');
    }

    function closeModal() {
        $('existingFilesPanel')?.classList.add('hidden');
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
        const status = action === 'complete' ? 'completed' : (action === 'aware' ? 'aware' : 'in_progress');
        try {
            await api('update_status', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id, report_status: status }) });
            toast(status === 'completed' ? 'Đã xác nhận hoàn thành báo cáo.' : (status === 'aware' ? 'Đã đánh dấu chỉ biết.' : 'Đã chuyển sang đang xử lý.'));
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

        for (let i = 1; i <= Math.min(pdf.numPages, 3); i++) {  // chỉ cần 3 trang đầu cho header
            const page = await pdf.getPage(i);
            const content = await page.getTextContent();

            // Cải thiện: nhóm text theo vị trí y để tái tạo layout header tốt hơn (hai cột, dòng trên)
            const items = content.items
                .filter(it => it.str && it.str.trim())
                .map(it => {
                    const t = it.transform || [1,0,0,1,0,0];
                    return {
                        str: it.str,
                        x: t[4] || 0,
                        y: t[5] || 0,
                        height: Math.abs(t[3] || 10)
                    };
                });

            // Sắp xếp từ trên xuống (y cao trước), rồi trái sang phải
            items.sort((a, b) => {
                if (Math.abs(a.y - b.y) > 5) return b.y - a.y; // y cao hơn (trên) trước
                return a.x - b.x;
            });

            // Gom thành dòng: các item có y gần nhau coi là cùng dòng
            const lines = [];
            let currentLine = [];
            let lastY = null;

            for (const item of items) {
                if (lastY === null || Math.abs(item.y - lastY) <= 8) {
                    currentLine.push(item);
                } else {
                    if (currentLine.length) {
                        currentLine.sort((a,b) => a.x - b.x);
                        lines.push(currentLine.map(it => it.str).join(' '));
                    }
                    currentLine = [item];
                }
                lastY = item.y;
            }
            if (currentLine.length) {
                currentLine.sort((a,b) => a.x - b.x);
                lines.push(currentLine.map(it => it.str).join(' '));
            }

            // Chỉ lấy các dòng đầu của trang (header thường ở 15 dòng đầu)
            const headerLines = lines.slice(0, 20);
            pages.push(headerLines.join('\n'));
        }

        let text = pages.join('\n\n');
        text = text.replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n').trim();
        return text;
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

    async function extractPdfFirstPageImage(file) {
        if (!window.pdfjsLib) throw new Error('pdfjs not loaded');
        const pdf = await window.pdfjsLib.getDocument({ data: await file.arrayBuffer() }).promise;
        if (!pdf.numPages) throw new Error('No pages');
        const page = await pdf.getPage(1);
        const scale = 1.8;
        const viewport = page.getViewport({ scale });
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        await page.render({ canvasContext: ctx, viewport }).promise;
        return canvas.toDataURL('image/jpeg', 0.85);
    }

    function fileToDataUrl(f) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(f);
        });
    }

    async function extractPdf(file) {
        if (!file) throw new Error('Không có file.');

        const fileName = file.name.toLowerCase();
        const isPdfFile = file.type === 'application/pdf' || fileName.endsWith('.pdf');
        const isImageFile = file.type.startsWith('image/') || fileName.match(/\.(jpg|jpeg|png|webp|gif)$/);

        if (isImageFile) {
            if (!hasMistralOcr()) {
                throw new Error('Cần bật Mistral OCR để đọc ảnh.');
            }
            const dataUrl = await fileToDataUrl(file);
            const res = await window.MistralOcr.ocrImageDataUrl(dataUrl);
            const txt = res.text || '';
            if (meaningfulTextLength(txt) < 10) throw new Error('Không đọc được chữ từ ảnh.');
            return { text: txt, mode: 'mistral-ocr' };
        }

        if (!isPdfFile) {
            throw new Error('Chỉ hỗ trợ file PDF hoặc ảnh.');
        }

        // PDF: ưu tiên thử text layer, nếu header kém (rất phổ biến với PDF ký số trên Android) thì ngay lập tức thử render trang đầu + OCR
        let text = '';
        let mode = 'text-layer';
        try {
            text = await extractPdfTextLayer(file);
        } catch (e) {
            text = '';
        }

        const headerCheck = text.substring(0, 700);
        const headerLooksBad = meaningfulTextLength(text) < 80 ||
                               /Số\s*[:\.]?\s*[^0-9\w]/i.test(headerCheck) ||
                               /Số\s*:\s*\//i.test(headerCheck);

        if (headerLooksBad && hasMistralOcr()) {
            try {
                const imgDataUrl = await extractPdfFirstPageImage(file);
                const ocrRes = await window.MistralOcr.ocrImageDataUrl(imgDataUrl);
                const ocrText = ocrRes.text || '';
                if (meaningfulTextLength(ocrText) > 15) {
                    text = ocrText;
                    mode = 'mistral-ocr';
                }
            } catch (e) {
                // sẽ thử extractPdfOcr ở dưới
            }
        }

        if (meaningfulTextLength(text) < 60 && hasMistralOcr()) {
            try {
                const img = await extractPdfFirstPageImage(file);
                const res = await window.MistralOcr.ocrImageDataUrl(img);
                text = res.text || text;
                mode = 'mistral-ocr';
            } catch {
                text = await extractPdfOcr(file);
                mode = 'mistral-ocr';
            }
        }

        if (meaningfulTextLength(text) < 15) {
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
        setValue('documentDate', formatYMDToDMY(item.document_date));
        if ($('reportRequired')) $('reportRequired').checked = !!item.report_required;
        setValue('reportDueAt', formatYMDToDMY(item.report_due_at));
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
        // Chỉ gửi phần đầu cho nhận diện (tiết kiệm quota AI)
        const forParse = source.substring(0, 1800);
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
                body: JSON.stringify({ source_text: forParse }),
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

    function buildSavePayload() {
        return {
            id: Number($('documentId')?.value) || 0,
            sector: SECTOR,
            academic_year: $('academicYear')?.value,
            direction: $('direction')?.value,
            document_number: $('documentNumber')?.value,
            title: $('title')?.value,
            document_date: parseDMYToYMD($('documentDate')?.value),
            document_type: $('documentType')?.value,
            organization: $('organization')?.value,
            summary_text: $('summaryText')?.value,
            source_text: $('sourceText')?.value,
            report_required: !!$('reportRequired')?.checked,
            report_due_at: parseDMYToYMD($('reportDueAt')?.value),
            report_status: $('reportStatus')?.value,
            report_note: $('reportNote')?.value,
        };
    }

    async function uploadFileViaChunks(documentId, file, index) {
        const mime = file.type || 'application/octet-stream';
        const init = await api('upload_init', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                document_id: documentId,
                filename: file.name,
                size: file.size,
                mime,
                index,
            }),
        });
        const chunkSize = Number(init.chunk_size) || (1024 * 1024);
        let lastResult = null;
        for (let offset = 0; offset < file.size; offset += chunkSize) {
            const blob = file.slice(offset, Math.min(offset + chunkSize, file.size));
            const form = new FormData();
            form.append('session_id', init.session_id);
            form.append('offset', String(offset));
            form.append('total_size', String(file.size));
            form.append('chunk', blob, `${file.name}.part`);
            const response = await fetch(`${API}?action=upload_chunk&sector=${encodeURIComponent(SECTOR)}`, {
                method: 'POST',
                credentials: 'include',
                body: form,
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok) {
                const backend = data.upload_backend ? ` [${data.upload_backend}]` : '';
                throw new Error((data.error || 'Không tải được phần tệp lên Google Drive.') + backend);
            }
            lastResult = data;
            if (data.complete) return data;
        }
        if (!lastResult?.complete) {
            throw new Error('Google Drive chưa nhận đủ các phần của tệp.');
        }
        return lastResult;
    }

    async function saveDocument(payload) {
        const pending = state.pendingUploadFiles || [];
        const saveData = await api('save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!pending.length) return saveData;
        if (state.driveReady) {
            for (let index = 0; index < pending.length; index += 1) {
                await uploadFileViaChunks(Number(saveData.document?.id) || Number(payload.id) || 0, pending[index], index);
            }
            return {
                ok: true,
                document: saveData.document,
                storage: 'drive',
                message: `Đã lưu văn bản và ${pending.length} tệp lên Google Drive.`,
            };
        }
        const form = new FormData();
        Object.entries(payload).forEach(([key, value]) => {
            if (value === undefined || value === null) return;
            form.append(key, typeof value === 'boolean' ? (value ? '1' : '0') : String(value));
        });
        pending.forEach(file => form.append('files[]', file, file.name));
        const response = await fetch(`${API}?action=save_upload&sector=${encodeURIComponent(SECTOR)}`, {
            method: 'POST',
            credentials: 'include',
            body: form,
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            const backend = data.upload_backend ? ` [${data.upload_backend}]` : '';
            throw new Error((data.error || 'Không lưu được văn bản và tệp đính kèm.') + backend);
        }
        return data;
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
            const hadPendingFiles = (state.pendingUploadFiles || []).length > 0;
            try {
                const data = await saveDocument(buildSavePayload());
                state.pendingUploadFiles = [];
                closeModal();
                if (data.storage === 'local') {
                    toast(data.message || 'Đã lưu tệp tạm trên hosting vì Google Drive chưa kết nối được.');
                } else if (data.storage === 'drive' || hadPendingFiles) {
                    toast(data.message || 'Đã lưu văn bản và tệp đính kèm.');
                } else {
                    toast(data.message || 'Đã lưu văn bản.');
                }
                load();
            } catch (error) {
                const hint = error.message;
                if ($('formError')) {
                    $('formError').textContent = hint;
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
            const files = [...event.target.files];
            const maxBytes = effectiveUploadMaxBytes();
            const oversized = files.filter(file => file.size > maxBytes);
            state.pendingUploadFiles = oversized.length ? [] : files;
            const selectedNote = $('selectedFilesNote');
            if (selectedNote) {
                if (oversized.length) {
                    const limitText = formatBytes(maxBytes);
                    const hint = state.driveReady
                        ? `Tệp vượt giới hạn ${limitText}/tệp của ứng dụng.`
                        : `Tệp ${oversized.map(file => file.name).join(', ')} vượt giới hạn ${limitText}/tệp trên hosting. Vào cPanel → PHP → đặt upload_max_filesize ≥ 32M, hoặc bật Google Drive.`;
                    selectedNote.textContent = hint;
                    toast(selectedNote.textContent, 'rose');
                    event.target.value = '';
                } else {
                    selectedNote.textContent = files.length
                        ? `Đã chọn ${files.length} tệp: ${files.map(file => file.name).join(', ')} · tối đa ${formatBytes(maxBytes)}/tệp`
                        : `Có thể chọn nhiều tệp, gồm ZIP/RAR/7Z · tối đa ${formatBytes(maxBytes)} cho mỗi tệp.`;
                }
            }
            if (oversized.length) return;

            // Chỉ dùng tệp PDF đầu tiên để tự nhận diện thông tin văn bản.
            // Tất cả tệp đã chọn (ảnh, Office, PDF...) vẫn được upload đầy đủ.
            const file = files.find(item => item.type === 'application/pdf' || /\.pdf$/i.test(item.name));
            if (!file || !$('parseNote') || !$('sourceText')) return;

            $('parseNote').textContent = `Đang đọc file ${file.name} (chỉ trang đầu)...`;
            $('parseNote').classList.remove('hidden');

            try {
                const extracted = await extractPdf(file);
                const modeLabel = extracted.mode === 'mistral-ocr' ? 'Mistral OCR' : 'lớp chữ';
                $('sourceText').value = extracted.text;
                $('parseNote').textContent = `Đã đọc bằng ${modeLabel}. Đang tự điền thông tin...`;
                await runAutoParse({ silent: true });
            } catch (error) {
                $('parseNote').textContent = error.message || 'Không đọc được file. Thử lại hoặc dán text thủ công.';
                toast(error.message || 'Lỗi đọc PDF trên Android. Thử file khác hoặc dùng ảnh.', 'rose');
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
        $('typeFilter')?.addEventListener('change', event => {
            state.typeFilter = event.target.value;
            render();
        });
        $('searchInput')?.addEventListener('input', render);
        $('closeDetailBtn')?.addEventListener('click', closeDetailModal);
        $('documentDetailModal')?.addEventListener('click', event => {
            if (event.target === $('documentDetailModal')) closeDetailModal();
        });
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
