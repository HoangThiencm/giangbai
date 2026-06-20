(function () {
    const API = 'api/tranphu_data.php';
    let lists = [];
    let pendingRows = [];

    const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[ch]));
    const norm = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
    const adminHeaders = () => ({
        'Content-Type': 'application/json',
        'X-Admin-Key': document.getElementById('adminKey')?.value.trim() || ''
    });

    function panel() { return document.getElementById('tranPhuDataPanel'); }
    function selectedList() { return lists.find(item => item.list_code === document.getElementById('tranPhuListSelect')?.value) || null; }
    function show(message, error = false) {
        const box = document.getElementById('tranPhuMessage');
        if (!box) return;
        box.textContent = message;
        box.className = `mt-4 rounded-lg px-4 py-3 text-sm font-semibold ${error ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-emerald-50 text-emerald-800 border border-emerald-200'}`;
        box.classList.remove('hidden');
    }

    function ensurePanel() {
        if (panel()) return panel();
        const dashboard = document.getElementById('dashboardSection');
        if (!dashboard) return null;
        const node = document.createElement('section');
        node.id = 'tranPhuDataPanel';
        node.className = 'space-y-5';
        node.innerHTML = `
            <div class="rounded-xl border border-sky-200 bg-gradient-to-r from-sky-50 to-white p-6 shadow-sm">
                <div class="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                    <div>
                        <p class="text-xs font-extrabold uppercase tracking-[.14em] text-sky-700">Danh mục dùng chung</p>
                        <h3 class="mt-1 text-xl font-black text-slate-900"><i class="fas fa-school mr-2 text-sky-600"></i>THCS Trần Phú</h3>
                        <p class="mt-2 max-w-3xl text-sm leading-6 text-slate-600">Khai báo một lần danh sách toàn trường, giáo viên và đảng viên. Giáo viên sẽ chọn các danh sách này khi tạo đợt báo cáo.</p>
                    </div>
                    <span class="inline-flex items-center rounded-full bg-white px-3 py-1 text-xs font-bold text-sky-800 shadow-sm"><i class="fas fa-file-excel mr-1.5"></i>Nhập Excel</span>
                </div>
                <div id="tranPhuListCards" class="mt-5 grid gap-3 md:grid-cols-3"></div>
            </div>
            <div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                <div class="grid gap-4 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-end">
                    <label class="text-sm font-bold text-slate-700">Danh sách cần cập nhật
                        <select id="tranPhuListSelect" class="mt-1 w-full rounded border border-slate-300 bg-white px-3 py-2.5 outline-none focus:ring-2 focus:ring-sky-500"></select>
                    </label>
                    <div class="flex flex-wrap gap-2">
                        <button type="button" id="tranPhuTemplateBtn" class="rounded border border-sky-300 bg-sky-50 px-4 py-2.5 text-sm font-bold text-sky-800 hover:bg-sky-100"><i class="fas fa-download mr-1"></i>Tải mẫu Excel</button>
                        <button type="button" id="tranPhuClearBtn" class="rounded border border-red-200 bg-white px-4 py-2.5 text-sm font-bold text-red-700 hover:bg-red-50"><i class="fas fa-trash-can mr-1"></i>Xóa danh sách</button>
                    </div>
                </div>
                <div class="mt-4 rounded-lg border border-slate-200 bg-slate-50 p-4">
                    <p class="text-sm font-bold text-slate-800">Cấu trúc file</p>
                    <p id="tranPhuStructureHint" class="mt-1 text-sm text-slate-600">Cột bắt buộc: <b>Họ và tên</b>. Các cột nên có: <b>Tổ/đơn vị hoặc lớp</b>, <b>Chức vụ/Vai trò</b>, <b>Email/Số điện thoại</b>. Các cột khác vẫn được lưu làm thông tin bổ sung.</p>
                    <label class="mt-4 block text-sm font-bold text-slate-700">Chọn file Excel
                        <input id="tranPhuImportFile" type="file" accept=".xlsx,.xls,.csv" class="mt-1 block w-full text-sm file:mr-3 file:rounded file:border-0 file:bg-sky-600 file:px-3 file:py-2 file:text-sm file:font-bold file:text-white hover:file:bg-sky-700">
                    </label>
                    <div class="mt-4 flex flex-wrap items-center gap-3"><button type="button" id="tranPhuImportBtn" class="rounded bg-sky-700 px-4 py-2.5 text-sm font-bold text-white shadow hover:bg-sky-800"><i class="fas fa-upload mr-1"></i>Thay thế bằng dữ liệu Excel</button><span id="tranPhuPreview" class="text-sm font-semibold text-slate-600"></span></div>
                </div>
                <div id="tranPhuMessage" class="mt-4 hidden"></div>
                <div id="tranPhuPreviewTable" class="mt-5 hidden overflow-x-auto rounded-lg border border-slate-200"></div>
            </div>`;
        dashboard.appendChild(node);
        node.querySelector('#tranPhuListSelect').addEventListener('change', () => { pendingRows = []; renderPreview(); renderListHint(); });
        node.querySelector('#tranPhuTemplateBtn').addEventListener('click', downloadTemplate);
        node.querySelector('#tranPhuImportFile').addEventListener('change', previewImport);
        node.querySelector('#tranPhuImportBtn').addEventListener('click', importRows);
        node.querySelector('#tranPhuClearBtn').addEventListener('click', clearRows);
        return node;
    }

    async function request(url, options = {}) {
        const response = await fetch(url, { credentials: 'same-origin', ...options });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(data.error || 'Không thể xử lý yêu cầu.');
        return data;
    }

    function renderLists() {
        const select = document.getElementById('tranPhuListSelect');
        const cards = document.getElementById('tranPhuListCards');
        if (!select || !cards) return;
        const previous = select.value;
        select.innerHTML = lists.map(list => `<option value="${esc(list.list_code)}">${esc(list.title)} (${list.people_count} người)</option>`).join('');
        if (lists.some(list => list.list_code === previous)) select.value = previous;
        cards.innerHTML = lists.map(list => `<div class="rounded-lg border border-slate-200 bg-white p-4"><div class="text-xs font-bold uppercase tracking-wide text-slate-500">${esc(list.list_code)}</div><div class="mt-1 font-extrabold text-slate-900">${esc(list.title)}</div><div class="mt-2 text-2xl font-black text-sky-700">${list.people_count}</div><div class="text-xs text-slate-500">người trong danh sách</div></div>`).join('');
        renderListHint();
    }

    function renderListHint() {
        const holder = document.getElementById('tranPhuStructureHint');
        const list = selectedList();
        if (!holder || !list) return;
        holder.innerHTML = list.list_code === 'party'
            ? 'Cột bắt buộc: <b>Họ tên</b>. Cột thứ hai: <b>Ghi chú / Chức vụ</b>. Đây là danh sách ngắn gọn dành riêng cho đảng viên.'
            : list.list_code === 'teachers'
                ? 'Đúng ba cột: <b>STT</b>, <b>Họ và tên</b>, <b>Lớp chủ nhiệm</b>. STT chỉ để đánh số và được bỏ qua khi nhập.'
                : 'Đúng ba cột: <b>STT</b>, <b>Họ và tên</b>, <b>Chức vụ</b>. STT chỉ để đánh số và được bỏ qua khi nhập.';
    }

    function mapHeader(header) {
        const value = norm(header);
        if (value.includes('ho va ten') || value === 'ten' || value.includes('full name')) return 'full_name';
        if (value.includes('to don vi') || value.includes('lop nhom') || value.includes('lop chu nhiem') || value === 'lop' || value.includes('nhom')) return 'group_name';
        if (value.includes('chuc vu') || value.includes('vai tro') || value.includes('role')) return 'role_label';
        if (value.includes('email') || value.includes('dien thoai') || value.includes('sdt') || value.includes('lien he')) return 'contact';
        return '';
    }

    function parseWorkbook(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = event => {
                try {
                    const book = XLSX.read(new Uint8Array(event.target.result), { type: 'array' });
                    const sheet = book.Sheets[book.SheetNames[0]];
                    const rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '' });
                    let headerIndex = -1;
                    for (let i = 0; i < Math.min(15, rows.length); i++) {
                        if ((rows[i] || []).some(cell => mapHeader(cell) === 'full_name')) { headerIndex = i; break; }
                    }
                    if (headerIndex < 0) throw new Error('Không tìm thấy cột “Họ và tên”. Hãy tải file mẫu để dùng đúng định dạng.');
                    const headers = rows[headerIndex] || [];
                    const parsed = [];
                    for (let rowIndex = headerIndex + 1; rowIndex < rows.length; rowIndex++) {
                        const values = rows[rowIndex] || [];
                        const item = { extra: {}, source_row: rowIndex + 1 };
                        headers.forEach((header, index) => {
                            const text = String(values[index] ?? '').trim();
                            if (!text) return;
                            const key = mapHeader(header);
                            if (key) item[key] = text;
                            else item.extra[String(header || `Cột ${index + 1}`).trim()] = text;
                        });
                        if (item.full_name) parsed.push(item);
                    }
                    resolve(parsed);
                } catch (error) { reject(error); }
            };
            reader.onerror = () => reject(new Error('Không đọc được file Excel.'));
            reader.readAsArrayBuffer(file);
        });
    }

    function renderPreview() {
        const preview = document.getElementById('tranPhuPreview');
        const table = document.getElementById('tranPhuPreviewTable');
        if (!preview || !table) return;
        preview.textContent = pendingRows.length ? `Đã đọc ${pendingRows.length} dòng hợp lệ.` : '';
        if (!pendingRows.length) { table.classList.add('hidden'); table.innerHTML = ''; return; }
        table.classList.remove('hidden');
        table.innerHTML = `<table class="w-full min-w-[640px] text-left text-sm"><thead class="bg-slate-100 text-xs uppercase text-slate-500"><tr><th class="p-3">Họ và tên</th><th class="p-3">Tổ/đơn vị</th><th class="p-3">Vai trò</th><th class="p-3">Liên hệ</th></tr></thead><tbody>${pendingRows.slice(0, 8).map(row => `<tr class="border-t border-slate-100"><td class="p-3 font-bold">${esc(row.full_name)}</td><td class="p-3">${esc(row.group_name || '')}</td><td class="p-3">${esc(row.role_label || '')}</td><td class="p-3">${esc(row.contact || '')}</td></tr>`).join('')}</tbody></table>${pendingRows.length > 8 ? `<p class="border-t border-slate-100 p-3 text-xs text-slate-500">… và ${pendingRows.length - 8} dòng khác.</p>` : ''}`;
    }

    function downloadTemplate() {
        const list = selectedList();
        if (!list) return;
        const rows = list.list_code === 'party'
            ? [['Họ tên', 'Ghi chú / Chức vụ'], ['Bùi Ngọc Nam', 'Bí thư Chi bộ'], ['Nguyễn Ngọc Nam', 'Phó Bí thư'], ['Nguyễn Văn An', 'Đảng viên']]
            : list.list_code === 'teachers'
                ? [['STT', 'Họ và tên', 'Lớp chủ nhiệm'], [1, 'Nguyễn Văn An', '6A'], [2, 'Trần Thị Bình', '7A'], [3, 'Lê Văn Cường', '8A']]
                : [['STT', 'Họ và tên', 'Chức vụ'], [1, 'Nguyễn Văn An', 'Hiệu trưởng'], [2, 'Trần Thị Bình', 'Phó Hiệu trưởng'], [3, 'Lê Văn Cường', 'Giáo viên']];
        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.aoa_to_sheet(rows);
        ws['!cols'] = list.list_code === 'party' ? [{ wch: 28 }, { wch: 28 }] : [{ wch: 8 }, { wch: 28 }, { wch: 24 }];
        XLSX.utils.book_append_sheet(wb, ws, list.title.substring(0, 30));
        XLSX.writeFile(wb, `${list.list_code}-THCS-Tran-Phu.xlsx`);
    }

    async function previewImport(event) {
        const file = event.target.files?.[0];
        pendingRows = [];
        if (!file) return renderPreview();
        try { pendingRows = await parseWorkbook(file); renderPreview(); }
        catch (error) { renderPreview(); show(error.message, true); }
    }

    async function importRows() {
        const list = selectedList();
        if (!list) return;
        if (!pendingRows.length) return show('Hãy chọn file Excel có ít nhất một dòng hợp lệ.', true);
        if (!confirm(`Thay thế toàn bộ danh sách “${list.title}” bằng ${pendingRows.length} dòng trong file?`)) return;
        const btn = document.getElementById('tranPhuImportBtn');
        const original = btn.innerHTML; btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-1"></i>Đang nhập...';
        try {
            const data = await request(`${API}?action=import`, { method: 'POST', headers: adminHeaders(), body: JSON.stringify({ list_code: list.list_code, rows: pendingRows }) });
            show(data.message || 'Đã nhập dữ liệu.'); pendingRows = []; document.getElementById('tranPhuImportFile').value = ''; renderPreview(); await loadLists();
        } catch (error) { show(error.message, true); }
        finally { btn.disabled = false; btn.innerHTML = original; }
    }

    async function clearRows() {
        const list = selectedList();
        if (!list || !confirm(`Xóa toàn bộ ${list.people_count} người trong “${list.title}”?`)) return;
        try { const data = await request(`${API}?action=clear`, { method: 'POST', headers: adminHeaders(), body: JSON.stringify({ list_code: list.list_code }) }); show(`Đã xóa ${data.count || 0} dòng.`); await loadLists(); }
        catch (error) { show(error.message, true); }
    }

    async function loadLists() {
        try {
            const data = await request(`${API}?action=options`, { headers: adminHeaders() });
            lists = data.lists || []; renderLists();
        } catch (error) { show(error.message, true); }
    }

    function boot() {
        ensurePanel();
        const original = window.forceAdminTabs;
        if (typeof original === 'function' && !original.__tranPhuWrapped) {
            const wrapped = function (...args) { const result = original.apply(this, args); ensurePanel(); return result; };
            wrapped.__tranPhuWrapped = true; window.forceAdminTabs = wrapped;
        }
        window.forceAdminTabs?.();
        const dashboard = document.getElementById('dashboardSection');
        if (dashboard && !dashboard.classList.contains('hidden')) loadLists();
        const previousLoadUsers = window.loadUsers;
        if (typeof previousLoadUsers === 'function' && !previousLoadUsers.__tranPhuLoaded) {
            window.loadUsers = async function (...args) { const out = await previousLoadUsers.apply(this, args); loadLists(); return out; };
            window.loadUsers.__tranPhuLoaded = true;
        }
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
