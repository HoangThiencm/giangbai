(function () {
    const API = 'api/tranphu_data.php';
    let lists = [];
    let pendingExcelRows = [];
    let activeSubTab = 'excel';
    let currentPeople = [];
    let peopleSearchQuery = '';

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
                        <p class="text-xs font-extrabold uppercase tracking-[.14em] text-sky-700">THCS Trần Phú</p>
                        <h3 class="mt-1 text-xl font-black text-slate-900"><i class="fas fa-school mr-2 text-sky-600"></i>Danh mục báo cáo & nộp bài</h3>
                        <p class="mt-2 max-w-3xl text-sm leading-6 text-slate-600">Khai báo một lần danh sách toàn trường, giáo viên, đảng viên — hoặc <b>tự tạo danh sách</b> cho từng đợt báo cáo (Tổ bộ môn, Ban Chuyên Môn, Đoàn Đội...). Giáo viên chọn danh sách này khi tạo đợt nộp.</p>
                    </div>
                    <span class="inline-flex items-center rounded-full bg-white px-3.5 py-1.5 text-xs font-bold text-sky-800 shadow-sm border border-sky-100"><i class="fas fa-database mr-1.5 text-sky-600"></i>Cơ sở dữ liệu trường</span>
                </div>
                <div id="tranPhuListCards" class="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3"></div>
            </div>

            <div class="rounded-xl border border-teal-200 bg-gradient-to-r from-teal-50 to-white p-6 shadow-sm">
                <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                        <p class="text-xs font-extrabold uppercase tracking-[.14em] text-teal-700">Tạo danh sách mới</p>
                        <h4 class="mt-1 text-lg font-black text-slate-900"><i class="fas fa-plus-circle mr-2 text-teal-600"></i>Danh sách báo cáo tùy chỉnh</h4>
                        <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-600">Đặt tên danh sách theo mục đích (Tổ Toán - Tin, Ban Chuyên Môn, Chi đoàn...). Sau khi tạo, chọn danh sách bên dưới để nhập dữ liệu.</p>
                    </div>
                </div>
                <div class="mt-4 flex flex-col gap-2 sm:flex-row sm:items-end">
                    <label class="flex-1 text-sm font-bold text-slate-700">Tên danh sách mới *
                        <input id="tranPhuNewListTitle" class="mt-1 w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 outline-none focus:ring-2 focus:ring-teal-500" placeholder="Ví dụ: Tổ Toán — Báo cáo tháng 3, Ban Chuyên Môn, Đoàn Đội…">
                    </label>
                    <button type="button" id="tranPhuCreateListBtn" class="rounded-lg bg-teal-700 px-5 py-2.5 text-sm font-bold text-white shadow hover:bg-teal-800 transition"><i class="fas fa-plus mr-1.5"></i>Tạo danh sách</button>
                </div>
            </div>

            <div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                <div class="grid gap-4 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-end">
                    <label class="text-sm font-bold text-slate-700">Danh sách đang chọn để quản lý
                        <div class="mt-1 flex items-center gap-2">
                            <select id="tranPhuListSelect" class="w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-base font-bold text-slate-800 outline-none focus:ring-2 focus:ring-sky-500 shadow-sm"></select>
                            <button type="button" id="tranPhuRenameListBtn" class="flex-shrink-0 rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm font-bold text-slate-700 hover:bg-slate-50 transition shadow-sm" title="Đổi tên danh sách">
                                <i class="fas fa-pen text-slate-600 mr-1.5"></i>Đổi tên
                            </button>
                        </div>
                    </label>
                    <div class="flex flex-wrap gap-2">
                        <button type="button" id="tranPhuTemplateBtn" class="rounded-lg border border-sky-300 bg-sky-50 px-4 py-2.5 text-sm font-bold text-sky-800 hover:bg-sky-100 transition"><i class="fas fa-download mr-1.5"></i>Tải mẫu Excel</button>
                        <button type="button" id="tranPhuClearBtn" class="rounded-lg border border-amber-200 bg-white px-4 py-2.5 text-sm font-bold text-amber-800 hover:bg-amber-50 transition"><i class="fas fa-eraser mr-1.5"></i>Xóa sạch dữ liệu</button>
                        <button type="button" id="tranPhuDeleteListBtn" class="hidden rounded-lg border border-red-200 bg-white px-4 py-2.5 text-sm font-bold text-red-700 hover:bg-red-50 transition"><i class="fas fa-trash-can mr-1.5"></i>Xóa danh sách này</button>
                    </div>
                </div>

                <!-- TABS CHUYỂN ĐỔI -->
                <div class="mt-6 border-b border-slate-200">
                    <div class="flex flex-wrap gap-1" id="tranPhuSubTabNav">
                        <button type="button" data-tranphu-subtab="excel" class="tranphu-subtab-btn inline-flex items-center gap-2 rounded-t-lg border-b-2 border-sky-600 bg-sky-50 px-5 py-3 text-sm font-bold text-sky-800 transition">
                            <i class="fas fa-file-excel text-emerald-600"></i>Nhập từ file Excel
                        </button>
                        <button type="button" data-tranphu-subtab="direct" class="tranphu-subtab-btn inline-flex items-center gap-2 rounded-t-lg border-b-2 border-transparent px-5 py-3 text-sm font-bold text-slate-600 transition hover:bg-slate-50 hover:text-slate-900">
                            <i class="fas fa-paste text-indigo-600"></i>Nhập trực tiếp / Dán văn bản
                        </button>
                        <button type="button" data-tranphu-subtab="view" class="tranphu-subtab-btn inline-flex items-center gap-2 rounded-t-lg border-b-2 border-transparent px-5 py-3 text-sm font-bold text-slate-600 transition hover:bg-slate-50 hover:text-slate-900">
                            <i class="fas fa-users text-sky-600"></i>Xem danh sách hiện có
                        </button>
                    </div>
                </div>

                <!-- TAB 1: NHẬP EXCEL -->
                <div id="tranPhuSubtabContentExcel" class="mt-5 space-y-4">
                    <div class="rounded-lg border border-slate-200 bg-slate-50 p-4">
                        <p class="text-sm font-bold text-slate-800"><i class="fas fa-circle-info mr-1.5 text-sky-600"></i>Cấu trúc file</p>
                        <p id="tranPhuStructureHint" class="mt-1 text-sm text-slate-600">Cột bắt buộc: <b>Họ và tên</b>. Các cột nên có: <b>Tổ/đơn vị hoặc lớp</b>, <b>Chức vụ/Vai trò</b>, <b>Email/Số điện thoại</b>. Các cột khác vẫn được lưu làm thông tin bổ sung.</p>
                        <label class="mt-4 block text-sm font-bold text-slate-700">Chọn file Excel (.xlsx, .xls, .csv)
                            <input id="tranPhuImportFile" type="file" accept=".xlsx,.xls,.csv" class="mt-1 block w-full text-sm file:mr-3 file:rounded-lg file:border-0 file:bg-sky-600 file:px-4 file:py-2.5 file:text-sm file:font-bold file:text-white hover:file:bg-sky-700 cursor-pointer">
                        </label>
                        
                        <div class="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-slate-200 pt-4">
                            <div class="flex items-center gap-4 text-sm">
                                <span class="font-bold text-slate-700">Chế độ lưu:</span>
                                <label class="inline-flex items-center gap-1.5 cursor-pointer font-semibold text-slate-700">
                                    <input type="radio" name="tranPhuExcelMode" value="replace" checked class="text-sky-600 focus:ring-sky-500"> Thay thế toàn bộ
                                </label>
                                <label class="inline-flex items-center gap-1.5 cursor-pointer font-semibold text-slate-700">
                                    <input type="radio" name="tranPhuExcelMode" value="append" class="text-sky-600 focus:ring-sky-500"> Thêm nối tiếp (bỏ qua trùng)
                                </label>
                            </div>
                            <div class="flex items-center gap-3">
                                <span id="tranPhuExcelPreviewCount" class="text-sm font-bold text-sky-700"></span>
                                <button type="button" id="tranPhuImportBtn" class="rounded-lg bg-sky-700 px-5 py-2.5 text-sm font-bold text-white shadow hover:bg-sky-800 transition">
                                    <i class="fas fa-upload mr-1.5"></i>Lưu dữ liệu Excel
                                </button>
                            </div>
                        </div>
                    </div>
                    <div id="tranPhuExcelPreviewTable" class="hidden overflow-x-auto rounded-lg border border-slate-200"></div>
                </div>

                <!-- TAB 2: NHẬP TRỰC TIẾP / DÁN VĂN BẢN -->
                <div id="tranPhuSubtabContentDirect" class="mt-5 hidden space-y-4">
                    <div class="rounded-lg border border-indigo-100 bg-indigo-50/50 p-4">
                        <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                            <div>
                                <h5 class="text-sm font-black text-indigo-950"><i class="fas fa-keyboard mr-1.5 text-indigo-600"></i>Nhập trực tiếp hoặc Dán từ Excel / Sheets / Word / Zalo</h5>
                                <p class="text-xs text-slate-600 mt-0.5">Mỗi người 1 dòng. Tự động nhận dạng khi dán từ bảng tính (Tab), gạch đứng (<code class="bg-white px-1 py-0.5 rounded border border-indigo-200">|</code>), chấm phẩy (<code class="bg-white px-1 py-0.5 rounded border border-indigo-200">;</code>) hoặc phẩy.</p>
                            </div>
                            <div class="flex items-center gap-2">
                                <button type="button" id="tranPhuSampleBtn" class="rounded border border-indigo-200 bg-white px-3 py-1.5 text-xs font-bold text-indigo-700 shadow-sm hover:bg-indigo-50 transition"><i class="fas fa-magic mr-1"></i>Chèn mẫu</button>
                                <button type="button" id="tranPhuDirectClearBtn" class="rounded border border-slate-200 bg-white px-3 py-1.5 text-xs font-bold text-slate-600 shadow-sm hover:bg-slate-50 transition"><i class="fas fa-eraser mr-1"></i>Xóa trắng</button>
                            </div>
                        </div>

                        <div class="mt-3">
                            <textarea id="tranPhuDirectText" rows="9" class="w-full font-mono text-sm leading-relaxed p-3.5 rounded-lg border border-slate-300 bg-white outline-none focus:ring-2 focus:ring-indigo-500 shadow-inner" placeholder="Ví dụ dán từ Excel hoặc gõ:&#10;Nguyễn Văn An&#9;Tổ Toán&#9;Tổ trưởng&#9;0912345678&#10;Trần Thị Bình&#9;Tổ Văn&#9;Tổ phó&#9;0987654321&#10;&#10;Hoặc định dạng gạch đứng:&#10;Lê Văn Cường | Tổ Hóa | Giáo viên | 0901234567"></textarea>
                        </div>

                        <div class="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-t border-indigo-100 pt-3">
                            <div class="flex items-center gap-4 text-sm">
                                <span class="font-bold text-slate-700">Chế độ lưu:</span>
                                <label class="inline-flex items-center gap-1.5 cursor-pointer font-semibold text-slate-700">
                                    <input type="radio" name="tranPhuDirectMode" value="replace" checked class="text-indigo-600 focus:ring-indigo-500"> Thay thế toàn bộ
                                </label>
                                <label class="inline-flex items-center gap-1.5 cursor-pointer font-semibold text-slate-700">
                                    <input type="radio" name="tranPhuDirectMode" value="append" class="text-indigo-600 focus:ring-indigo-500"> Thêm nối tiếp (bỏ qua trùng)
                                </label>
                            </div>
                            <div class="flex items-center gap-3">
                                <span id="tranPhuDirectCountBadge" class="text-sm font-bold text-indigo-700"></span>
                                <button type="button" id="tranPhuSaveDirectBtn" class="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-bold text-white shadow hover:bg-indigo-700 transition">
                                    <i class="fas fa-floppy-disk mr-1.5"></i>Lưu vào danh sách
                                </button>
                            </div>
                        </div>
                    </div>

                    <div id="tranPhuDirectPreviewSection" class="hidden space-y-2">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-extrabold uppercase tracking-wide text-slate-500">Xem trước kết quả nhận diện</span>
                            <span id="tranPhuDirectPreviewSummary" class="text-xs font-bold text-slate-600"></span>
                        </div>
                        <div id="tranPhuDirectPreviewTable" class="overflow-x-auto rounded-lg border border-slate-200"></div>
                    </div>
                </div>

                <!-- TAB 3: XEM DANH SÁCH HIỆN CÓ -->
                <div id="tranPhuSubtabContentView" class="mt-5 hidden space-y-4">
                    <div class="rounded-lg border border-slate-200 bg-slate-50 p-4">
                        <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                            <div class="flex items-center gap-2">
                                <h5 id="tranPhuViewListTitle" class="text-base font-black text-slate-900">Danh sách hiện có</h5>
                                <span id="tranPhuViewListCountBadge" class="rounded-full bg-sky-100 px-2.5 py-0.5 text-xs font-bold text-sky-800">0 người</span>
                            </div>
                            <div class="flex flex-wrap items-center gap-2">
                                <div class="relative">
                                    <input id="tranPhuSearchPeopleInput" type="text" placeholder="Tìm tên, tổ, chức vụ..." class="w-56 rounded-lg border border-slate-300 bg-white py-1.5 pl-8 pr-3 text-sm outline-none focus:ring-2 focus:ring-sky-500">
                                    <i class="fas fa-search absolute left-2.5 top-2.5 text-xs text-slate-400"></i>
                                </div>
                                <button type="button" id="tranPhuCopyPeopleBtn" class="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm font-bold text-slate-700 shadow-sm hover:bg-slate-50 transition"><i class="fas fa-copy mr-1 text-slate-500"></i>Sao chép (Text)</button>
                                <button type="button" id="tranPhuReloadPeopleBtn" class="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm font-bold text-slate-700 shadow-sm hover:bg-slate-50 transition"><i class="fas fa-rotate mr-1 text-slate-500"></i>Làm mới</button>
                            </div>
                        </div>

                        <!-- Form Thêm nhanh 1 người -->
                        <div class="mt-4 rounded-lg border border-sky-100 bg-sky-50/70 p-3">
                            <div class="text-xs font-extrabold uppercase tracking-wide text-sky-800 mb-2"><i class="fas fa-user-plus mr-1"></i>Thêm nhanh 1 thành viên vào danh sách</div>
                            <form id="tranPhuQuickAddForm" class="grid gap-2 sm:grid-cols-2 md:grid-cols-5 items-center" onsubmit="return false;">
                                <input id="tranPhuAddFullName" type="text" placeholder="Họ và tên *" required class="rounded border border-slate-300 bg-white px-3 py-1.5 text-sm outline-none focus:ring-2 focus:ring-sky-500">
                                <input id="tranPhuAddGroupName" type="text" placeholder="Tổ / Lớp / Đơn vị" class="rounded border border-slate-300 bg-white px-3 py-1.5 text-sm outline-none focus:ring-2 focus:ring-sky-500">
                                <input id="tranPhuAddRoleLabel" type="text" placeholder="Chức vụ / Vai trò" class="rounded border border-slate-300 bg-white px-3 py-1.5 text-sm outline-none focus:ring-2 focus:ring-sky-500">
                                <input id="tranPhuAddContact" type="text" placeholder="SĐT / Email / Ghi chú" class="rounded border border-slate-300 bg-white px-3 py-1.5 text-sm outline-none focus:ring-2 focus:ring-sky-500">
                                <button type="button" id="tranPhuAddPersonBtn" class="rounded bg-sky-600 px-4 py-1.5 text-sm font-bold text-white shadow hover:bg-sky-700 transition"><i class="fas fa-plus mr-1"></i>Thêm</button>
                            </form>
                        </div>
                    </div>

                    <div id="tranPhuPeopleTableContainer" class="overflow-x-auto rounded-lg border border-slate-200"></div>
                </div>

                <div id="tranPhuMessage" class="mt-4 hidden"></div>
            </div>

            <!-- Modal Chỉnh sửa thành viên -->
            <div id="tranPhuEditPersonModal" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4 hidden">
                <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl border border-slate-100 animate-in fade-in zoom-in duration-150">
                    <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                        <h3 class="text-base font-black text-slate-800 flex items-center gap-2">
                            <i class="fas fa-pen-to-square text-sky-600"></i>Chỉnh sửa thông tin thành viên
                        </h3>
                        <button type="button" id="tranPhuCloseEditModalBtn" class="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 transition">
                            <i class="fas fa-times text-base"></i>
                        </button>
                    </div>
                    <form id="tranPhuEditPersonForm" class="mt-4 space-y-3.5" onsubmit="return false;">
                        <input type="hidden" id="tranPhuEditPersonId">
                        <div>
                            <label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">Họ và tên *</label>
                            <input id="tranPhuEditFullName" type="text" required class="w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-sm text-slate-900 outline-none focus:ring-2 focus:ring-sky-500 font-semibold">
                        </div>
                        <div>
                            <label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">Tổ / Đơn vị / Lớp</label>
                            <input id="tranPhuEditGroupName" type="text" class="w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-sm text-slate-900 outline-none focus:ring-2 focus:ring-sky-500">
                        </div>
                        <div>
                            <label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">Chức vụ / Vai trò</label>
                            <input id="tranPhuEditRoleLabel" type="text" class="w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-sm text-slate-900 outline-none focus:ring-2 focus:ring-sky-500">
                        </div>
                        <div>
                            <label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">SĐT / Email / Liên hệ</label>
                            <input id="tranPhuEditContact" type="text" class="w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-sm text-slate-900 outline-none focus:ring-2 focus:ring-sky-500">
                        </div>
                        <div id="tranPhuEditError" class="hidden rounded-lg bg-red-50 p-2.5 text-xs font-semibold text-red-600 border border-red-200"></div>
                        <div class="mt-5 flex items-center justify-end gap-2 border-t border-slate-100 pt-4">
                            <button type="button" id="tranPhuCancelEditBtn" class="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:bg-slate-50 transition">Hủy</button>
                            <button type="button" id="tranPhuSaveEditPersonBtn" class="rounded-lg bg-sky-600 px-5 py-2 text-sm font-bold text-white shadow hover:bg-sky-700 transition">
                                <i class="fas fa-floppy-disk mr-1.5"></i>Lưu thay đổi
                            </button>
                        </div>
                    </form>
                </div>
            </div>`;

        dashboard.appendChild(node);

        // Event listeners
        node.querySelector('#tranPhuListSelect').addEventListener('change', onListSelectChange);
        node.querySelector('#tranPhuRenameListBtn').addEventListener('click', renameList);
        node.querySelector('#tranPhuTemplateBtn').addEventListener('click', downloadTemplate);
        node.querySelector('#tranPhuClearBtn').addEventListener('click', clearRows);
        node.querySelector('#tranPhuCreateListBtn').addEventListener('click', createList);
        node.querySelector('#tranPhuDeleteListBtn').addEventListener('click', deleteList);

        // Subtabs
        node.querySelectorAll('.tranphu-subtab-btn').forEach(btn => {
            btn.addEventListener('click', () => switchSubTab(btn.dataset.tranphuSubtab));
        });

        // Tab 1 (Excel)
        node.querySelector('#tranPhuImportFile').addEventListener('change', previewExcelImport);
        node.querySelector('#tranPhuImportBtn').addEventListener('click', importExcelRows);

        // Tab 2 (Direct text)
        const directText = node.querySelector('#tranPhuDirectText');
        directText.addEventListener('input', renderDirectPreview);
        node.querySelector('#tranPhuSampleBtn').addEventListener('click', insertDirectSample);
        node.querySelector('#tranPhuDirectClearBtn').addEventListener('click', clearDirectText);
        node.querySelector('#tranPhuSaveDirectBtn').addEventListener('click', saveDirectRows);

        // Tab 3 (View people)
        node.querySelector('#tranPhuSearchPeopleInput').addEventListener('input', e => {
            peopleSearchQuery = e.target.value.trim();
            renderPeopleTable();
        });
        node.querySelector('#tranPhuCopyPeopleBtn').addEventListener('click', copyPeopleToClipboard);
        node.querySelector('#tranPhuReloadPeopleBtn').addEventListener('click', loadCurrentPeople);
        node.querySelector('#tranPhuAddPersonBtn').addEventListener('click', addSinglePerson);

        // Enter key in quick add form
        node.querySelector('#tranPhuQuickAddForm').addEventListener('keydown', e => {
            if (e.key === 'Enter') {
                e.preventDefault();
                addSinglePerson();
            }
        });

        // Edit person modal listeners
        node.querySelector('#tranPhuCloseEditModalBtn').addEventListener('click', closeEditPersonModal);
        node.querySelector('#tranPhuCancelEditBtn').addEventListener('click', closeEditPersonModal);
        node.querySelector('#tranPhuSaveEditPersonBtn').addEventListener('click', saveEditPerson);
        node.querySelector('#tranPhuEditPersonForm').addEventListener('keydown', e => {
            if (e.key === 'Enter') {
                e.preventDefault();
                saveEditPerson();
            }
        });
        node.querySelector('#tranPhuEditPersonModal').addEventListener('click', e => {
            if (e.target.id === 'tranPhuEditPersonModal') {
                closeEditPersonModal();
            }
        });

        return node;
    }

    async function request(url, options = {}) {
        const response = await fetch(url, { credentials: 'same-origin', ...options });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(data.error || 'Không thể xử lý yêu cầu.');
        return data;
    }

    function switchSubTab(tabName) {
        activeSubTab = tabName;
        const navBtns = document.querySelectorAll('.tranphu-subtab-btn');
        navBtns.forEach(btn => {
            const isTarget = btn.dataset.tranphuSubtab === tabName;
            if (isTarget) {
                btn.className = 'tranphu-subtab-btn inline-flex items-center gap-2 rounded-t-lg border-b-2 border-sky-600 bg-sky-50 px-5 py-3 text-sm font-bold text-sky-800 transition';
            } else {
                btn.className = 'tranphu-subtab-btn inline-flex items-center gap-2 rounded-t-lg border-b-2 border-transparent px-5 py-3 text-sm font-bold text-slate-600 transition hover:bg-slate-50 hover:text-slate-900';
            }
        });
        document.getElementById('tranPhuSubtabContentExcel')?.classList.toggle('hidden', tabName !== 'excel');
        document.getElementById('tranPhuSubtabContentDirect')?.classList.toggle('hidden', tabName !== 'direct');
        document.getElementById('tranPhuSubtabContentView')?.classList.toggle('hidden', tabName !== 'view');

        if (tabName === 'view') {
            loadCurrentPeople();
        }
    }

    function onListSelectChange() {
        pendingExcelRows = [];
        renderExcelPreview();
        renderListHint();
        renderDirectPreview();
        const current = selectedList();
        const deleteBtn = document.getElementById('tranPhuDeleteListBtn');
        if (deleteBtn) deleteBtn.classList.toggle('hidden', !current || current.is_system);

        if (activeSubTab === 'view') {
            loadCurrentPeople();
        }
    }

    function renderLists() {
        const select = document.getElementById('tranPhuListSelect');
        const cards = document.getElementById('tranPhuListCards');
        if (!select || !cards) return;
        const previous = select.value;
        select.innerHTML = lists.map(list => `<option value="${esc(list.list_code)}">${esc(list.title)} (${list.people_count} người)</option>`).join('');
        if (lists.some(list => list.list_code === previous)) select.value = previous;
        cards.innerHTML = lists.map(list => `<div class="rounded-lg border border-slate-200 bg-white p-4 shadow-sm hover:border-sky-300 transition"><div class="flex items-center gap-2"><div class="text-xs font-bold uppercase tracking-wide text-slate-500">${esc(list.list_code)}</div>${list.is_system ? '<span class="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-500">Mặc định</span>' : '<span class="rounded-full bg-sky-100 px-2 py-0.5 text-[10px] font-bold text-sky-700">Tùy chỉnh</span>'}</div><div class="mt-1 font-extrabold text-slate-900 line-clamp-1">${esc(list.title)}</div><div class="mt-2 text-2xl font-black text-sky-700">${list.people_count}</div><div class="text-xs text-slate-500">người trong danh sách</div></div>`).join('');
        const deleteBtn = document.getElementById('tranPhuDeleteListBtn');
        const current = selectedList();
        if (deleteBtn) deleteBtn.classList.toggle('hidden', !current || current.is_system);
        renderListHint();
    }

    function renderListHint() {
        const holder = document.getElementById('tranPhuStructureHint');
        const list = selectedList();
        if (!holder || !list) return;
        holder.innerHTML = list.list_code === 'party'
            ? 'Cột bắt buộc: <b>Họ tên</b> hoặc <b>Họ và tên</b>. Cột thứ hai: <b>Ghi chú / Chức vụ</b>. Đây là danh sách ngắn gọn dành riêng cho đảng viên.'
            : list.list_code === 'teachers'
                ? 'Đúng ba cột: <b>STT</b>, <b>Họ và tên</b>, <b>Lớp chủ nhiệm</b>. STT chỉ để đánh số và được bỏ qua khi nhập.'
                : 'Cột bắt buộc: <b>Họ và tên</b>. Nên có thêm <b>Tổ/đơn vị hoặc lớp</b>, <b>Chức vụ/Vai trò</b>, <b>Email/SĐT</b>. Cột <b>STT</b> nếu có sẽ được bỏ qua.';
    }

    function mapHeader(header) {
        const value = norm(header);
        if (!value) return '';

        // 1. STT / No / TT
        if (value === 'stt' || value === 'no' || value === 'tt' || value === 'so thu tu' || value === 'so tt' || value === 'sott' || value === 'thu tu') {
            return 'stt';
        }

        // 2. Chức vụ / Vai trò / Ghi chú (Check specific role keywords first before general org keywords)
        const roleKeywords = [
            'chuc vu', 'vai tro', 'chuc danh', 'nhiem vu', 'vi tri', 'role', 'position',
            'ghi chu', 'phan cong', 'trach nhiem', 'to truong', 'to pho', 'truong ban',
            'pho ban', 'truong phong', 'pho phong', 'truong khoa', 'pho khoa', 'chu tich',
            'pho chu tich', 'hieu truong', 'hieu pho', 'bi thu', 'pho bi thu'
        ];
        if (roleKeywords.some(k => value === k || value.includes(k))) {
            return 'role_label';
        }

        // 3. Liên hệ / Phone / Email
        const contactKeywords = [
            'email', 'thu dien tu', 'dien thoai', 'sdt', 'so dien thoai',
            'phone', 'tel', 'mobile', 'lien he', 'thong tin lien he', 'zalo'
        ];
        if (contactKeywords.some(k => value === k || value.includes(k))) {
            return 'contact';
        }

        // 4. Họ và tên
        if (
            value.includes('ho va ten') || value.includes('ho ten') || value === 'hoten' ||
            value.includes('ho va chu lot') || value.includes('ho chu lot') ||
            value.includes('full name') || value.includes('fullname') ||
            value.includes('ten can bo') || value.includes('ten giao vien') ||
            value.includes('ten nhan vien') || value.includes('ten thanh vien') ||
            value.includes('nguoi nop') || value.includes('nguoi thuc hien') ||
            value === 'ten' || value === 'ho' || value === 'can bo' ||
            value === 'giao vien' || value === 'nhan vien' || value === 'thanh vien' ||
            (value.includes('ho') && value.includes('ten'))
        ) {
            return 'full_name';
        }

        // 5. Tổ / Đơn vị / Lớp / Ban / Phòng / Khoa
        if (
            value.startsWith('to ') ||
            value.startsWith('lop ') ||
            value.startsWith('khoi ') ||
            value.startsWith('phong ') ||
            value.startsWith('ban ') ||
            value.startsWith('khoa ') ||
            value === 'to' || value === 'lop' || value === 'khoi' || value === 'phong' ||
            value === 'ban' || value === 'khoa' || value === 'dv' || value === 'dvct' ||
            value === 'tcm' || value === 'tbm' || value === 'to cm' || value === 'to bm' ||
            value.includes('don vi') || value.includes('noi cong tac') ||
            value.includes('to don vi') || value.includes('to chuyen mon') ||
            value.includes('to bo mon') || value.includes('bo mon') ||
            value.includes('phong ban') || value.includes('co quan') ||
            value.includes('lop chu nhiem') || value.includes('lop hoc') ||
            value.includes('khoi lop') || value.includes('chi bo') ||
            value.includes('dang bo') || value.includes('to nhom') ||
            value.includes('ban chuyen mon') || value.includes('toan truong') ||
            value.includes('phan ban') || value.includes('to giam thi') ||
            value.includes('to bao ve') || value.includes('to phuc vu') ||
            value.includes('to khao thi') || value.includes('nhom')
        ) {
            return 'group_name';
        }

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
                    if (headerIndex < 0) throw new Error('Không tìm thấy cột “Họ tên” hoặc “Họ và tên”. Hãy tải file mẫu để dùng đúng định dạng.');
                    const headers = rows[headerIndex] || [];
                    const parsed = [];
                    for (let rowIndex = headerIndex + 1; rowIndex < rows.length; rowIndex++) {
                        const values = rows[rowIndex] || [];
                        const item = { extra: {}, source_row: rowIndex + 1 };
                        headers.forEach((header, index) => {
                            const text = String(values[index] ?? '').trim();
                            if (!text) return;
                            const key = mapHeader(header);
                            if (key && key !== 'stt') item[key] = text;
                            else if (key !== 'stt') item.extra[String(header || `Cột ${index + 1}`).trim()] = text;
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

    function renderExcelPreview() {
        const previewCount = document.getElementById('tranPhuExcelPreviewCount');
        const table = document.getElementById('tranPhuExcelPreviewTable');
        if (!previewCount || !table) return;
        previewCount.textContent = pendingExcelRows.length ? `Đã đọc ${pendingExcelRows.length} dòng hợp lệ.` : '';
        if (!pendingExcelRows.length) { table.classList.add('hidden'); table.innerHTML = ''; return; }
        table.classList.remove('hidden');
        table.innerHTML = `
            <table class="w-full min-w-[640px] text-left text-sm">
                <thead class="bg-slate-100 text-xs uppercase text-slate-600">
                    <tr>
                        <th class="p-3 w-12 text-center">STT</th>
                        <th class="p-3">Họ và tên</th>
                        <th class="p-3">Tổ / Đơn vị / Lớp</th>
                        <th class="p-3">Vai trò / Chức vụ</th>
                        <th class="p-3">Liên hệ</th>
                    </tr>
                </thead>
                <tbody>
                    ${pendingExcelRows.slice(0, 8).map((row, idx) => `
                        <tr class="border-t border-slate-100 hover:bg-slate-50">
                            <td class="p-3 text-center text-xs text-slate-400 font-semibold">${idx + 1}</td>
                            <td class="p-3 font-bold text-slate-800">${esc(row.full_name)}</td>
                            <td class="p-3 text-slate-600">${esc(row.group_name || '—')}</td>
                            <td class="p-3 text-slate-600">${esc(row.role_label || '—')}</td>
                            <td class="p-3 text-slate-600">${esc(row.contact || '—')}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            ${pendingExcelRows.length > 8 ? `<div class="border-t border-slate-100 bg-slate-50 p-2.5 text-center text-xs text-slate-500 font-semibold">… và ${pendingExcelRows.length - 8} dòng khác.</div>` : ''}
        `;
    }

    function tokenizeLine(line) {
        if (line.includes('\t')) return line.split('\t').map(c => c.trim());
        if (line.includes('|')) return line.split('|').map(c => c.trim());
        if (line.includes(';')) return line.split(';').map(c => c.trim());
        if (line.includes(' - ')) return line.split(/\s+-\s+/).map(c => c.trim());
        if (line.includes(',') && line.split(',').length > 1) return line.split(',').map(c => c.trim());
        return [line.trim()];
    }

    function classifyDirectToken(token) {
        if (!token || typeof token !== 'string') return null;
        const clean = token.trim();
        if (!clean) return null;
        const v = norm(clean);

        // Contact check: email or phone
        if (clean.includes('@') || /^(?:\+84|0|\(0\))[0-9\.\-\s]{8,15}$/.test(clean.replace(/\s+/g, '')) || (/^[0-9\+\(\)\.\-\s]{9,15}$/.test(clean) && (clean.match(/\d/g) || []).length >= 9)) {
            return { type: 'contact', value: clean };
        }

        // Role check
        const roleKeywords = [
            'hieu truong', 'hieu pho', 'to truong', 'to pho', 'bi thu', 'pho bi thu',
            'giao vien', 'gvcn', 'gvbm', 'nhan vien', 'ke toan', 'thu quy', 'van thu',
            'y te', 'bao ve', 'tong phu trach', 'tpt', 'dang vien', 'truong ban',
            'pho ban', 'truong phong', 'pho phong', 'truong khoa', 'pho khoa',
            'chu tich', 'pho chu tich', 'pho hieu truong', 'can bo', 'doan vien',
            'chuyen vien', 'thu vien', 'tap vu', 'phuc vu', 'giam thi'
        ];
        if (roleKeywords.some(k => v === k || v.includes(k))) {
            return { type: 'role_label', value: clean };
        }

        // Group / Org check
        const groupPrefixes = ['to ', 'lop ', 'khoi ', 'phong ', 'ban ', 'khoa '];
        const groupMatches = [
            'chi bo', 'dang bo', 'bgh', 'ban giam hieu', 'toan truong', 'khtn', 'khxh',
            'van phong', 'su dia', 'toan tin', 'toan', 'ly', 'hoa', 'sinh', 'van',
            'su', 'dia', 'gdcd', 'the duc', 'am nhac', 'my thuat', 'tin hoc',
            'tieng anh', 'ngoai ngu', 'giam thi', 'bao ve', 'khao thi', 'doan doi'
        ];
        if (
            groupPrefixes.some(p => v.startsWith(p)) ||
            groupMatches.some(k => v === k || v.includes(k)) ||
            /^[1-9][0-2]?[a-z0-9\/\-\.]+$/i.test(clean)
        ) {
            return { type: 'group_name', value: clean };
        }

        return null;
    }

    function parseDirectText(rawText, listCode = '') {
        if (!rawText || typeof rawText !== 'string') return [];
        const lines = rawText.split(/\r?\n/).map(line => line.trim()).filter(Boolean);
        if (!lines.length) return [];

        let headerCols = null;
        let startIndex = 0;

        const firstTokens = tokenizeLine(lines[0]);
        const hasNameHeader = firstTokens.some(tok => mapHeader(tok) === 'full_name');
        if (hasNameHeader) {
            headerCols = firstTokens.map(tok => mapHeader(tok));
            startIndex = 1;
        }

        const results = [];
        const seen = new Set();

        for (let i = startIndex; i < lines.length; i++) {
            let tokens = tokenizeLine(lines[i]).filter(c => c !== '');
            if (!tokens.length) continue;

            let fullName = '';
            let groupName = '';
            let roleLabel = '';
            let contact = '';
            const extra = {};

            if (headerCols && headerCols.length) {
                tokens.forEach((val, idx) => {
                    const key = headerCols[idx];
                    if (key === 'full_name') fullName = val;
                    else if (key === 'group_name') groupName = val;
                    else if (key === 'role_label') roleLabel = val;
                    else if (key === 'contact') contact = val;
                    else if (key !== 'stt' && val) {
                        extra[firstTokens[idx] || `Cột ${idx + 1}`] = val;
                    }
                });
            } else {
                if (tokens.length >= 2 && /^(\d+[\.\)]?|stt|no|tt)$/i.test(tokens[0])) {
                    tokens = tokens.slice(1);
                }

                if (!tokens.length) continue;

                let rawFirst = tokens[0];
                const leadingNumberMatch = rawFirst.match(/^(\d+)[\.\)\/\-:\s]+\s*(.+)$/);
                if (leadingNumberMatch && leadingNumberMatch[2]) {
                    tokens[0] = leadingNumberMatch[2].trim();
                }

                fullName = tokens[0] || '';

                const remainingTokens = tokens.slice(1);
                const unclassified = [];

                for (const tok of remainingTokens) {
                    const classified = classifyDirectToken(tok);
                    if (classified) {
                        if (classified.type === 'contact' && !contact) {
                            contact = classified.value;
                        } else if (classified.type === 'role_label' && !roleLabel) {
                            roleLabel = classified.value;
                        } else if (classified.type === 'group_name' && !groupName) {
                            groupName = classified.value;
                        } else {
                            unclassified.push(tok);
                        }
                    } else {
                        unclassified.push(tok);
                    }
                }

                if (listCode === 'party') {
                    if (!roleLabel && unclassified.length > 0) roleLabel = unclassified.shift();
                    if (!groupName && unclassified.length > 0) groupName = unclassified.shift();
                    if (!contact && unclassified.length > 0) contact = unclassified.shift();
                } else if (listCode === 'teachers') {
                    if (!groupName && unclassified.length > 0) groupName = unclassified.shift();
                    if (!roleLabel && unclassified.length > 0) roleLabel = unclassified.shift();
                    if (!contact && unclassified.length > 0) contact = unclassified.shift();
                } else {
                    if (!groupName && unclassified.length > 0) groupName = unclassified.shift();
                    if (!roleLabel && unclassified.length > 0) roleLabel = unclassified.shift();
                    if (!contact && unclassified.length > 0) contact = unclassified.shift();
                }

                if (unclassified.length > 0) {
                    unclassified.forEach((tok, uIdx) => {
                        extra[`Cột bổ sung ${uIdx + 1}`] = tok;
                    });
                }
            }

            fullName = fullName.trim();
            if (!fullName) continue;

            const dedupKey = (fullName + '|' + groupName).toLowerCase();
            if (seen.has(dedupKey)) continue;
            seen.add(dedupKey);

            results.push({
                full_name: fullName,
                group_name: groupName || null,
                role_label: roleLabel || null,
                contact: contact || null,
                extra: extra,
                source_row: i + 1
            });
        }

        return results;
    }

    function renderDirectPreview() {
        const text = document.getElementById('tranPhuDirectText')?.value || '';
        const list = selectedList();
        const parsed = parseDirectText(text, list?.list_code || '');
        const badge = document.getElementById('tranPhuDirectCountBadge');
        const section = document.getElementById('tranPhuDirectPreviewSection');
        const summary = document.getElementById('tranPhuDirectPreviewSummary');
        const table = document.getElementById('tranPhuDirectPreviewTable');

        if (!badge || !section || !table) return;

        if (!parsed.length) {
            badge.textContent = '';
            section.classList.add('hidden');
            table.innerHTML = '';
            return;
        }

        badge.textContent = `Đã nhận diện ${parsed.length} người`;
        section.classList.remove('hidden');
        if (summary) summary.textContent = `Hiển thị ${Math.min(parsed.length, 8)} / ${parsed.length} người`;

        table.innerHTML = `
            <table class="w-full min-w-[640px] text-left text-sm bg-white">
                <thead class="bg-indigo-100/60 text-xs uppercase text-indigo-900">
                    <tr>
                        <th class="p-3 w-12 text-center">STT</th>
                        <th class="p-3">Họ và tên</th>
                        <th class="p-3">Tổ / Đơn vị / Lớp</th>
                        <th class="p-3">Vai trò / Chức vụ</th>
                        <th class="p-3">Liên hệ</th>
                    </tr>
                </thead>
                <tbody>
                    ${parsed.slice(0, 8).map((row, idx) => `
                        <tr class="border-t border-slate-100 hover:bg-indigo-50/40">
                            <td class="p-3 text-center text-xs text-slate-400 font-semibold">${idx + 1}</td>
                            <td class="p-3 font-bold text-slate-900">${esc(row.full_name)}</td>
                            <td class="p-3 text-slate-700">${esc(row.group_name || '—')}</td>
                            <td class="p-3 text-slate-700">${esc(row.role_label || '—')}</td>
                            <td class="p-3 text-slate-700">${esc(row.contact || '—')}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            ${parsed.length > 8 ? `<div class="border-t border-slate-100 bg-slate-50 p-2 text-center text-xs text-slate-500 font-semibold">… và ${parsed.length - 8} người khác.</div>` : ''}
        `;
    }

    function insertDirectSample() {
        const list = selectedList();
        const textarea = document.getElementById('tranPhuDirectText');
        if (!textarea) return;

        if (list?.list_code === 'party') {
            textarea.value = `Bùi Ngọc Nam\tBí thư Chi bộ\t0912345671
Nguyễn Ngọc Nam\tPhó Bí thư\t0912345672
Nguyễn Văn An\tĐảng viên\t0912345673
Trần Thị Bình\tĐảng viên\t0912345674`;
        } else if (list?.list_code === 'teachers') {
            textarea.value = `1\tNguyễn Văn An\t6A
2\tTrần Thị Bình\t7A
3\tLê Văn Cường\t8A
4\tPhạm Thị Dung\t9A`;
        } else {
            textarea.value = `Nguyễn Văn An | Ban Giám Hiệu | Hiệu trưởng | 0912345678
Trần Thị Bình | Tổ Toán - Tin | Tổ trưởng | 0987654321
Lê Văn Cường | Tổ KHTN | Giáo viên | 0901234567
Phạm Thị Dung | Tổ KHXH | Tổ phó | 0934567890
Hoàng Minh Đức | Ban Chuyên Môn | Thành viên | 0976543210`;
        }
        renderDirectPreview();
    }

    function clearDirectText() {
        const textarea = document.getElementById('tranPhuDirectText');
        if (textarea) {
            textarea.value = '';
            renderDirectPreview();
        }
    }

    function downloadTemplate() {
        const list = selectedList();
        if (!list) return;
        const rows = list.list_code === 'party'
            ? [['Họ và tên', 'Ghi chú / Chức vụ'], ['Bùi Ngọc Nam', 'Bí thư Chi bộ'], ['Nguyễn Ngọc Nam', 'Phó Bí thư'], ['Nguyễn Văn An', 'Đảng viên']]
            : list.list_code === 'teachers'
                ? [['STT', 'Họ và tên', 'Lớp chủ nhiệm'], [1, 'Nguyễn Văn An', '6A'], [2, 'Trần Thị Bình', '7A'], [3, 'Lê Văn Cường', '8A']]
                : [['STT', 'Họ và tên', 'Tổ / Đơn vị', 'Chức vụ', 'Số điện thoại'], [1, 'Nguyễn Văn An', 'Ban Giám Hiệu', 'Hiệu trưởng', '0912345678'], [2, 'Trần Thị Bình', 'Tổ Toán', 'Tổ trưởng', '0987654321'], [3, 'Lê Văn Cường', 'Tổ Lý', 'Giáo viên', '0901234567']];
        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.aoa_to_sheet(rows);
        ws['!cols'] = list.list_code === 'party' ? [{ wch: 28 }, { wch: 28 }] : [{ wch: 8 }, { wch: 28 }, { wch: 20 }, { wch: 20 }, { wch: 18 }];
        XLSX.utils.book_append_sheet(wb, ws, list.title.substring(0, 30));
        XLSX.writeFile(wb, `${list.list_code}-danh-sach.xlsx`);
    }

    async function createList() {
        const input = document.getElementById('tranPhuNewListTitle');
        const title = input?.value.trim() || '';
        if (!title) return show('Hãy nhập tên danh sách mới.', true);
        const btn = document.getElementById('tranPhuCreateListBtn');
        const original = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-1.5"></i>Đang tạo...';
        try {
            const data = await request(`${API}?action=create-list`, { method: 'POST', headers: adminHeaders(), body: JSON.stringify({ title }) });
            input.value = '';
            show(data.message || 'Đã tạo danh sách.');
            await loadLists();
            if (data.list?.list_code) document.getElementById('tranPhuListSelect').value = data.list.list_code;
            onListSelectChange();
            renderLists();
        } catch (error) { show(error.message, true); }
        finally { btn.disabled = false; btn.innerHTML = original; }
    }

    async function deleteList() {
        const list = selectedList();
        if (!list || list.is_system) return;
        if (!confirm(`Xóa hẳn danh sách “${list.title}”?\n\nDanh sách và toàn bộ người trong đó sẽ bị xóa. Không thể hoàn tác.`)) return;
        try {
            const data = await request(`${API}?action=delete-list`, { method: 'POST', headers: adminHeaders(), body: JSON.stringify({ list_code: list.list_code }) });
            show(data.message || 'Đã xóa danh sách.');
            await loadLists();
        } catch (error) { show(error.message, true); }
    }

    async function previewExcelImport(event) {
        const file = event.target.files?.[0];
        pendingExcelRows = [];
        if (!file) return renderExcelPreview();
        try {
            pendingExcelRows = await parseWorkbook(file);
            renderExcelPreview();
        } catch (error) {
            renderExcelPreview();
            show(error.message, true);
        }
    }

    async function importExcelRows() {
        const list = selectedList();
        if (!list) return;
        if (!pendingExcelRows.length) return show('Hãy chọn file Excel có ít nhất một dòng hợp lệ.', true);
        const mode = document.querySelector('input[name="tranPhuExcelMode"]:checked')?.value || 'replace';
        const confirmMsg = mode === 'replace'
            ? `Thay thế toàn bộ danh sách “${list.title}” bằng ${pendingExcelRows.length} dòng trong file Excel?`
            : `Thêm ${pendingExcelRows.length} dòng từ file Excel vào danh sách “${list.title}”? (Người trùng họ tên và tổ sẽ tự động bỏ qua)`;

        if (!confirm(confirmMsg)) return;

        const btn = document.getElementById('tranPhuImportBtn');
        const original = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-1.5"></i>Đang lưu...';
        try {
            const data = await request(`${API}?action=import`, {
                method: 'POST',
                headers: adminHeaders(),
                body: JSON.stringify({ list_code: list.list_code, rows: pendingExcelRows, mode: mode })
            });
            show(data.message || 'Đã nhập dữ liệu thành công.');
            pendingExcelRows = [];
            document.getElementById('tranPhuImportFile').value = '';
            renderExcelPreview();
            await loadLists();
            if (activeSubTab === 'view') loadCurrentPeople();
        } catch (error) { show(error.message, true); }
        finally { btn.disabled = false; btn.innerHTML = original; }
    }

    async function saveDirectRows() {
        const list = selectedList();
        if (!list) return;
        const text = document.getElementById('tranPhuDirectText')?.value || '';
        const parsed = parseDirectText(text, list.list_code);
        if (!parsed.length) return show('Vui lòng nhập hoặc dán ít nhất 1 dòng có Họ và tên hợp lệ.', true);

        const mode = document.querySelector('input[name="tranPhuDirectMode"]:checked')?.value || 'replace';
        const confirmMsg = mode === 'replace'
            ? `Thay thế toàn bộ danh sách “${list.title}” bằng ${parsed.length} người vừa nhập?`
            : `Thêm ${parsed.length} người vào danh sách “${list.title}”? (Người trùng họ tên và tổ sẽ tự động bỏ qua)`;

        if (!confirm(confirmMsg)) return;

        const btn = document.getElementById('tranPhuSaveDirectBtn');
        const original = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-1.5"></i>Đang lưu...';
        try {
            const data = await request(`${API}?action=import`, {
                method: 'POST',
                headers: adminHeaders(),
                body: JSON.stringify({ list_code: list.list_code, rows: parsed, mode: mode })
            });
            show(data.message || 'Đã lưu danh sách thành công.');
            await loadLists();
            if (activeSubTab === 'view') loadCurrentPeople();
        } catch (error) { show(error.message, true); }
        finally { btn.disabled = false; btn.innerHTML = original; }
    }

    async function clearRows() {
        const list = selectedList();
        if (!list || !confirm(`Xóa toàn bộ ${list.people_count} người trong “${list.title}”?`)) return;
        try {
            const data = await request(`${API}?action=clear`, { method: 'POST', headers: adminHeaders(), body: JSON.stringify({ list_code: list.list_code }) });
            show(`Đã xóa sạch ${data.count || 0} người khỏi danh sách.`);
            await loadLists();
            if (activeSubTab === 'view') loadCurrentPeople();
        } catch (error) { show(error.message, true); }
    }

    async function loadCurrentPeople() {
        const list = selectedList();
        const titleEl = document.getElementById('tranPhuViewListTitle');
        const countBadge = document.getElementById('tranPhuViewListCountBadge');
        if (!list) return;

        if (titleEl) titleEl.textContent = `Danh sách: ${list.title}`;
        if (countBadge) countBadge.textContent = 'Đang tải...';

        try {
            const data = await request(`${API}?action=people&list=${encodeURIComponent(list.list_code)}`, { headers: adminHeaders() });
            currentPeople = data.people || [];
            if (countBadge) countBadge.textContent = `${currentPeople.length} người`;
            renderPeopleTable();
        } catch (error) {
            show(error.message, true);
            if (countBadge) countBadge.textContent = 'Lỗi';
        }
    }

    async function renameList() {
        const list = selectedList();
        if (!list) return;
        const newTitle = prompt(`Nhập tên mới cho danh sách "${list.title}":`, list.title);
        if (newTitle === null) return;
        const trimmed = newTitle.trim();
        if (!trimmed) {
            return show('Tên danh sách không được để trống.', true);
        }
        if (trimmed === list.title) return;

        try {
            const data = await request(`${API}?action=update-list-title`, {
                method: 'POST',
                headers: adminHeaders(),
                body: JSON.stringify({ list_code: list.list_code, title: trimmed })
            });
            show(data.message || 'Đã cập nhật tên danh sách.');
            await loadLists();
            const select = document.getElementById('tranPhuListSelect');
            if (select) select.value = list.list_code;
            onListSelectChange();
        } catch (error) {
            show(error.message, true);
        }
    }

    function openEditPersonModal(personId) {
        const person = currentPeople.find(p => p.id === personId);
        if (!person) return;

        const modal = document.getElementById('tranPhuEditPersonModal');
        const idInput = document.getElementById('tranPhuEditPersonId');
        const nameInput = document.getElementById('tranPhuEditFullName');
        const groupInput = document.getElementById('tranPhuEditGroupName');
        const roleInput = document.getElementById('tranPhuEditRoleLabel');
        const contactInput = document.getElementById('tranPhuEditContact');
        const errorBox = document.getElementById('tranPhuEditError');

        if (!modal || !idInput || !nameInput || !groupInput || !roleInput || !contactInput) return;

        idInput.value = person.id;
        nameInput.value = person.full_name || '';
        groupInput.value = person.group_name || '';
        roleInput.value = person.role_label || '';
        contactInput.value = person.contact || '';

        if (errorBox) {
            errorBox.textContent = '';
            errorBox.classList.add('hidden');
        }

        modal.classList.remove('hidden');
        nameInput.focus();
    }

    function closeEditPersonModal() {
        const modal = document.getElementById('tranPhuEditPersonModal');
        if (modal) modal.classList.add('hidden');
    }

    async function saveEditPerson() {
        const idInput = document.getElementById('tranPhuEditPersonId');
        const nameInput = document.getElementById('tranPhuEditFullName');
        const groupInput = document.getElementById('tranPhuEditGroupName');
        const roleInput = document.getElementById('tranPhuEditRoleLabel');
        const contactInput = document.getElementById('tranPhuEditContact');
        const errorBox = document.getElementById('tranPhuEditError');
        const btn = document.getElementById('tranPhuSaveEditPersonBtn');

        const personId = parseInt(idInput?.value || '0', 10);
        const fullName = nameInput?.value.trim() || '';
        const groupName = groupInput?.value.trim() || '';
        const roleLabel = roleInput?.value.trim() || '';
        const contact = contactInput?.value.trim() || '';

        if (personId <= 0) return;
        if (!fullName) {
            if (errorBox) {
                errorBox.textContent = 'Vui lòng nhập Họ và tên.';
                errorBox.classList.remove('hidden');
            }
            return;
        }

        if (errorBox) {
            errorBox.textContent = '';
            errorBox.classList.add('hidden');
        }

        const original = btn ? btn.innerHTML : '';
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-1.5"></i>Đang lưu...';
        }

        try {
            const data = await request(`${API}?action=update-person`, {
                method: 'POST',
                headers: adminHeaders(),
                body: JSON.stringify({
                    person_id: personId,
                    full_name: fullName,
                    group_name: groupName,
                    role_label: roleLabel,
                    contact: contact
                })
            });
            closeEditPersonModal();
            show(data.message || 'Đã cập nhật thông tin thành viên.');
            await loadLists();
            await loadCurrentPeople();
        } catch (error) {
            if (errorBox) {
                errorBox.textContent = error.message;
                errorBox.classList.remove('hidden');
            } else {
                show(error.message, true);
            }
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = original;
            }
        }
    }

    function renderPeopleTable() {
        const container = document.getElementById('tranPhuPeopleTableContainer');
        if (!container) return;

        let filtered = currentPeople;
        if (peopleSearchQuery) {
            const q = norm(peopleSearchQuery);
            filtered = currentPeople.filter(p => {
                return norm(p.full_name).includes(q) ||
                    norm(p.group_name).includes(q) ||
                    norm(p.role_label).includes(q) ||
                    norm(p.contact).includes(q);
            });
        }

        if (!currentPeople.length) {
            container.innerHTML = `
                <div class="p-8 text-center bg-white">
                    <i class="fas fa-user-slash text-3xl text-slate-300 mb-2"></i>
                    <p class="text-sm font-bold text-slate-600">Danh sách hiện chưa có dữ liệu.</p>
                    <p class="text-xs text-slate-400 mt-1">Hãy chuyển sang tab "Nhập từ file Excel" hoặc "Nhập trực tiếp" để thêm thành viên.</p>
                </div>
            `;
            return;
        }

        if (!filtered.length) {
            container.innerHTML = `
                <div class="p-6 text-center bg-white">
                    <p class="text-sm font-semibold text-slate-500">Không tìm thấy người nào khớp với từ khóa "${esc(peopleSearchQuery)}".</p>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <table class="w-full min-w-[700px] text-left text-sm bg-white">
                <thead class="bg-slate-100 text-xs uppercase text-slate-600">
                    <tr>
                        <th class="p-3 w-12 text-center">STT</th>
                        <th class="p-3">Họ và tên</th>
                        <th class="p-3">Tổ / Đơn vị / Lớp</th>
                        <th class="p-3">Vai trò / Chức vụ</th>
                        <th class="p-3">Liên hệ / Ghi chú</th>
                        <th class="p-3 w-24 text-center">Thao tác</th>
                    </tr>
                </thead>
                <tbody>
                    ${filtered.map((person, index) => `
                        <tr class="border-t border-slate-100 hover:bg-sky-50/50 transition">
                            <td class="p-3 text-center text-xs font-semibold text-slate-400">${index + 1}</td>
                            <td class="p-3 font-bold text-slate-900">${esc(person.full_name)}</td>
                            <td class="p-3 text-slate-700">${esc(person.group_name || '—')}</td>
                            <td class="p-3 text-slate-700">${esc(person.role_label || '—')}</td>
                            <td class="p-3 text-slate-700">${esc(person.contact || '—')}</td>
                            <td class="p-3 text-center whitespace-nowrap">
                                <button type="button" data-person-id="${person.id}" class="tranphu-edit-person-btn rounded p-1.5 text-sky-600 hover:bg-sky-50 hover:text-sky-800 transition mr-1" title="Chỉnh sửa thông tin">
                                    <i class="fas fa-pen-to-square text-sm"></i>
                                </button>
                                <button type="button" data-person-id="${person.id}" data-person-name="${esc(person.full_name)}" class="tranphu-del-person-btn rounded p-1.5 text-red-500 hover:bg-red-50 hover:text-red-700 transition" title="Xóa người này">
                                    <i class="fas fa-trash-can text-sm"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            <div class="border-t border-slate-100 bg-slate-50 px-4 py-2 text-xs font-semibold text-slate-500 flex justify-between items-center">
                <span>Tổng cộng: ${currentPeople.length} người</span>
                ${peopleSearchQuery ? `<span>Hiển thị: ${filtered.length} kết quả</span>` : ''}
            </div>
        `;

        container.querySelectorAll('.tranphu-edit-person-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = parseInt(btn.dataset.personId, 10);
                openEditPersonModal(id);
            });
        });

        container.querySelectorAll('.tranphu-del-person-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = parseInt(btn.dataset.personId, 10);
                const name = btn.dataset.personName;
                deleteSinglePerson(id, name);
            });
        });
    }

    async function deleteSinglePerson(personId, personName) {
        if (!personId) return;
        if (!confirm(`Xóa “${personName}” khỏi danh sách này?`)) return;
        try {
            const data = await request(`${API}?action=delete-person`, {
                method: 'POST',
                headers: adminHeaders(),
                body: JSON.stringify({ person_id: personId })
            });
            show(data.message || 'Đã xóa người khỏi danh sách.');
            await loadLists();
            await loadCurrentPeople();
        } catch (error) { show(error.message, true); }
    }

    async function addSinglePerson() {
        const list = selectedList();
        if (!list) return;
        const nameInput = document.getElementById('tranPhuAddFullName');
        const groupInput = document.getElementById('tranPhuAddGroupName');
        const roleInput = document.getElementById('tranPhuAddRoleLabel');
        const contactInput = document.getElementById('tranPhuAddContact');

        const fullName = nameInput?.value.trim() || '';
        const groupName = groupInput?.value.trim() || '';
        const roleLabel = roleInput?.value.trim() || '';
        const contact = contactInput?.value.trim() || '';

        if (!fullName) return show('Vui lòng nhập Họ và tên.', true);

        const btn = document.getElementById('tranPhuAddPersonBtn');
        const original = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        try {
            const data = await request(`${API}?action=add-person`, {
                method: 'POST',
                headers: adminHeaders(),
                body: JSON.stringify({
                    list_code: list.list_code,
                    full_name: fullName,
                    group_name: groupName,
                    role_label: roleLabel,
                    contact: contact
                })
            });
            show(data.message || 'Đã thêm thành viên.');
            nameInput.value = '';
            groupInput.value = '';
            roleInput.value = '';
            contactInput.value = '';
            await loadLists();
            await loadCurrentPeople();
        } catch (error) { show(error.message, true); }
        finally { btn.disabled = false; btn.innerHTML = original; }
    }

    function copyPeopleToClipboard() {
        if (!currentPeople.length) return show('Danh sách đang trống, không có dữ liệu để sao chép.', true);
        const lines = currentPeople.map(p => {
            const parts = [p.full_name, p.group_name || '', p.role_label || '', p.contact || ''];
            return parts.join('\t');
        });
        const header = ['Họ và tên', 'Tổ / Đơn vị', 'Chức vụ', 'Liên hệ'].join('\t');
        const text = header + '\n' + lines.join('\n');

        navigator.clipboard.writeText(text).then(() => {
            show(`Đã sao chép ${currentPeople.length} người vào clipboard (dạng bảng Tab, dán trực tiếp vào Excel/Word)!`);
        }).catch(() => {
            show('Không thể tự động sao chép vào bộ nhớ tạm. Hãy cấp quyền cho trình duyệt.', true);
        });
    }

    async function loadLists() {
        try {
            const data = await request(`${API}?action=options`, { headers: adminHeaders() });
            lists = data.lists || [];
            renderLists();
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
