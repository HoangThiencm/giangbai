# PLAN: Tái Cấu Trúc Giao Diện Chuyên Nghiệp, Tách Tab Sổ Dạy Thay Riêng & Tối Ưu Phân Bổ Chi Tiết Từng Tiết Cho Các Lớp (phancongtochuyenmon.html)

## Hiện trạng
1. **Giao diện tổng thể bị rối**:
   - Thanh Top Navbar (`#top-navbar`) dồn ép quá nhiều thành phần vào một hàng duy nhất: Logo, tên tổ, bộ chọn đợt, 4 tab chuyển đổi (view switcher), nút khai báo tổ, cụm nút CSDL (Lưu/Nạp), cụm nút File (Mở/Xuất JSON), nút Xuất Excel, nút Trang chủ. Khi hiển thị trên màn hình máy tính thông thường hoặc chia đôi cửa sổ, navbar bị vỡ hàng, các nút chen chúc gây rối mắt.
   - Các bảng dữ liệu (Bảng chấm công, Quyết toán tăng giờ, Báo cáo) thiếu sticky header, viền và khoảng cách chưa chuẩn UI hiện đại.
   - Các khối phân loại màu sắc chưa đồng nhất, tạo cảm giác chật chội và kém chuyên nghiệp.
2. **Chức năng Dạy Thay bị chôn vùi trong Chấm Công**:
   - Hiện tại, chức năng Dạy Thay - Dạy Bù chỉ được mở qua nút bấm nhỏ (`openSubstituteModal()`) bên trong Tab "Chấm công GV".
   - Giáo viên hoặc Tổ trưởng phải vào Chấm công mới mở được modal sổ dạy thay, không gian modal popup nhỏ hẹp, khó quan sát tổng thể nhật ký trong tháng.
3. **Chức năng Dạy Thay chưa tối ưu phân bổ từng tiết cho từng lớp**:
   - Trong dữ liệu hiện tại (`state.attendance.substitutes`), một bản ghi chỉ chứa 1 trường `class_name` duy nhất và 1 trường `period_count` (số tiết).
   - **Vấn đề thực tế**: Khi một giáo viên dạy thay 3 tiết trong 1 buổi (ví dụ: Tiết 1 dạy lớp 9A1, Tiết 2 dạy lớp 9A2, Tiết 4 dạy lớp 8A3), form hiện tại chỉ cho chọn đúng 1 lớp duy nhất và nhập số 3. Người dùng không thể nhập chi tiết tiết 1 ở lớp nào, tiết 2 lớp nào, tiết 3 lớp nào, gây sai lệch thông tin và khó theo dõi.

---

## Mục tiêu cải thiện
1. **Thiết kế lại giao diện Top Header & Navigation chuẩn chuyên nghiệp**:
   - Phân chia bố cục 2 tầng khoa học:
     + **Tầng 1 (Brand & Action Bar)**: Logo Tổ, Tên Tổ & Năm học (click để sửa nhanh), Trạng thái kết nối CSDL, Nút "Lưu CSDL" nổi bật (kèm trạng thái auto-save), Menu gom nhóm công cụ (File/Excel/Khai báo/Trang chủ).
     + **Tầng 2 (Workspace Bar & Tabs)**: 
       * Bên trái: 5 Tab làm việc hiện đại, có icon và số thứ tự rõ ràng:
         1. 📋 Phân công giảng dạy
         2. 📅 Sổ Dạy Thay - Bù (TÁCH THÀNH TAB RIÊNG)
         3. ⏱️ Chấm công GV
         4. 🧮 Tăng Giờ
         5. 📊 Báo cáo & Thống kê
       * Bên phải: Bộ chọn Đợt phân công (`Phase Selector`) thanh lịch và nút `+ Đợt mới`.
   - Cải tiến Design System: Bảng màu chuẩn Slate/Indigo, các card và bảng dữ liệu bo góc hiện đại, sticky header bảng, hover mượt mà.
2. **Tách chức năng Dạy Thay thành một Tab riêng biệt (Tab 2: `view-daythay`)**:
   - Tạo Tab chính `tab-nav-daythay` và màn hình `view-daythay` toàn trang thay thế hoàn toàn cho modal nhỏ hẹp cũ.
   - Bố cục Tab Sổ Dạy Thay gồm:
     + Khối Form Ghi nhận lượt Dạy thay / Dạy bù (có hỗ trợ chế độ Thêm mới và Chỉnh sửa bản ghi).
     + Khối Thống kê nhanh theo tháng (Tổng lượt, Tổng tiết dạy thay, Tổng tiết dạy bù).
     + Khối Bảng Nhật ký chi tiết kèm bộ lọc đa năng (Lọc theo tháng, lọc theo GV dạy, lọc theo loại, tìm kiếm theo tên/lớp/lý do).
     + Nút "Xuất Excel Sổ Dạy Thay" độc lập và Nút "Đồng bộ số tiết sang Chấm Công".
   - Giữ liên kết nhanh từ Tab Chấm Công: Cột "Dạy thay" và "Dạy bù" vẫn tự động nhận số tiết, kèm nút mở nhanh chuyển sang Tab Sổ Dạy Thay.
3. **Tối ưu phân bổ từng tiết học cho từng lớp cụ thể (Period Slots Builder)**:
   - Trong form ghi nhận: Khi chọn Buổi (Sáng hoặc Chiều), hệ thống hiển thị danh sách các tiết học trong buổi (Tiết 1 đến Tiết 5):
     + Cho phép chọn/bật từng tiết (Tiết 1, 2, 3, 4, 5) bằng switch/checkbox hoặc nút thêm tiết linh hoạt.
     + Với mỗi tiết được kích hoạt: Cho phép chọn **Lớp học** tương ứng từ danh mục lớp (`state.classes`) và chọn **Môn học** (từ `state.subjects` hoặc mặc định).
     + Các nút thao tác nhanh: `[+ Tiết 1-2]`, `[+ Tiết 1-3]`, `[+ Tiết 3-4]`, `[+ Cả buổi 1-5]`, `[Xóa chọn]`.
     + Tổng số tiết (`period_count`) tự động tính = số tiết đã gán, không cần nhập tay.
   - Bảng nhật ký hiển thị rõ ràng từng tag/badge: `[Tiết 1: 9A1]` `[Tiết 2: 9A2]` `[Tiết 4: 8A3]`.
   - Đảm bảo tính tương thích ngược 100% với dữ liệu cũ đã lưu trên LocalStorage và CSDL MySQL.

---

## Phạm vi thực hiện
1. **Giao diện & Bố cục (`phancongtochuyenmon.html`)**:
   - Cập nhật cấu trúc HTML của Header, thanh Navigation 5 tab, và thêm container `div.app-view#view-daythay`.
   - Cập nhật CSS: Phong cách thiết kế hiện đại, typography, spacing, card styles, form controls, badges và responsive layout.
2. **Logic chức năng Sổ Dạy Thay (`phancongtochuyenmon.html`)**:
   - Nâng cấp cấu trúc dữ liệu bản ghi dạy thay:
     ```javascript
     {
       id: 'sub_' + Date.now(),
       type: 'replacement', // 'replacement' | 'makeup'
       date: 'YYYY-MM-DD',
       session: 'morning', // 'morning' | 'afternoon'
       teacher_id: '...', // GV thực dạy
       for_teacher_id: '...', // GV được thay (hoặc để trống nếu dạy bù)
       for_other: '',
       reason: '...',
       // Phân bổ chi tiết từng tiết cho từng lớp:
       periods_detail: [
         { period_num: 1, class_name: '9A1', subject: 'Toán' },
         { period_num: 2, class_name: '9A2', subject: 'Toán' },
         { period_num: 4, class_name: '8A3', subject: 'Toán' }
       ],
       // Tương thích ngược:
       period_count: 3,
       period: 'Tiết 1 (9A1), Tiết 2 (9A2), Tiết 4 (8A3)',
       class_name: '9A1, 9A2, 8A3'
     }
     ```
   - Xây dựng giao diện Slot Picker cho 5 tiết: Checkbox chọn tiết + Select chọn lớp cho tiết đó + Select chọn môn.
   - Xây dựng hàm `renderDayThayView()`: Render form, thống kê số liệu tháng, bảng nhật ký có bộ lọc (tháng, giáo viên, tìm kiếm).
   - Thêm chức năng **Chỉnh sửa (Edit)** bản ghi: Bấm nút Sửa sẽ nạp dữ liệu cũ vào form để cập nhật.
   - Thêm chức năng **Xuất Excel riêng cho Sổ Dạy Thay - Dạy Bù** chuẩn mẫu văn bản trường học.
   - Giữ nguyên cơ chế đồng bộ `autoSyncSubstitutePeriods()` sang Bảng Chấm Công và Quyết Toán Tăng Giờ.
3. **Cập nhật Điều hướng App View (`switchAppView`)**:
   - Bổ sung `view-daythay` vào `switchAppView(viewId)`: Tự động kích hoạt tab, nạp danh sách giáo viên/lớp vào form và render bảng nhật ký.

---

## Ngoài phạm vi
- Không thay đổi backend `api/phancong.php` vì trường `data_json` lưu trữ toàn bộ state dưới dạng JSON, cấu trúc mới hoàn toàn tương thích với JSON hiện có.
- Không thay đổi các bảng cơ sở dữ liệu MySQL khác.

---

## File dự kiến tác động
- `phancongtochuyenmon.html` [SỬA: Tái cấu trúc Header/Tabs, tạo View Dạy Thay mới, bổ sung Period Slot Picker, hoàn thiện CSS/JS]
- `docs/handoff/PLAN.md` [GHI ĐÈ: Tài liệu handoff này]
- `docs/handoff/.lock` [GHI: LOCK]

---

## Chi tiết các bước thực hiện cho Coder

### Bước 1: Tái cấu trúc HTML Header & Thanh Điều Hướng (Tabs)
1. **Header chính**:
   - Chia thành cụm Trái (Logo, Tên tổ, Năm học, DB status) và cụm Phải (Nút Lưu CSDL dạng primary có icon xoay khi lưu, Nút "Khai báo tổ", Cụm menu "Công cụ / Tệp" gồm: Nạp CSDL, Mở JSON, Xuất JSON, Xuất Excel, Nút Trang chủ).
2. **Thanh Tabs (Sub-navbar)**:
   - Thêm tab thứ 2:
     ```html
     <button class="view-tab-btn" id="tab-nav-daythay" onclick="switchAppView('view-daythay')">
         <i class="fas fa-book-bookmark text-blue-600"></i> 2. Sổ Dạy Thay - Bù
     </button>
     ```
   - Đánh số lại các tab: 1. Phân công, 2. Sổ Dạy Thay - Bù, 3. Chấm công GV, 4. Tăng Giờ, 5. Báo cáo & Thống kê.
   - Đặt bộ chọn Đợt (`phase-selector-wrapper`) và nút `+ Đợt mới` sang góc phải của thanh Sub-navbar một cách gọn gàng, tách biệt với Header chính.

### Bước 2: Tạo màn hình Tab mới `view-daythay`
1. **Thêm container view**:
   ```html
   <!-- 2. VIEW SỔ THEO DÕI DẠY THAY & DẠY BÙ (TAB RIÊNG) -->
   <div class="app-view" id="view-daythay">
       <!-- Bố cục 2 khối: Khối Form Ghi Nhận & Khối Bảng Nhật Ký -->
   </div>
   ```
2. **Khối Form Ghi Nhận (Card nhập liệu chuyên nghiệp)**:
   - **Hàng 1**: Loại hình (Dạy thay / Dạy bù), Ngày dạy (kèm hiển thị thứ trong tuần), Buổi dạy (Sáng / Chiều - khi đổi buổi sẽ cập nhật nhãn tiết 1-5 buổi sáng/chiều).
   - **Hàng 2**: Giáo viên thực dạy, Dạy thay cho giáo viên (hoặc Lớp bù), Lý do / Căn cứ thay (Nghỉ phép, Công tác, Ốm, Bồi dưỡng chuyên môn...).
   - **Hàng 3 - KHU VỰC PHÂN BỔ TỪNG TIẾT (Period Slots Builder)**:
     - Tạo một container bảng/lưới chứa 5 tiết của buổi (Tiết 1 -> Tiết 5):
       + Checkbox chọn tiết `[x] Tiết X`
       + Dropdown chọn Lớp cho tiết X (render từ `state.classes`)
       + Dropdown chọn Môn cho tiết X (render từ `state.subjects`)
       + Textbox ghi chú tiết (tùy chọn)
     - Dải nút chọn nhanh: `[+ Tiết 1-2]`, `[+ Tiết 1-3]`, `[+ Tiết 3-4]`, `[+ Cả buổi (1-5)]`, `[Bỏ chọn tất cả]`.
     - Badge tổng số tiết: `Tổng cộng: X tiết` (tự động tính realtime khi người dùng click chọn tiết).
   - **Hàng nút bấm**: Nút "Lưu vào Sổ Dạy Thay" (hoặc "Cập nhật thay đổi" khi đang ở chế độ sửa), Nút "Làm mới / Hủy sửa".

3. **Khối Thống kê & Bảng Nhật Ký**:
   - Bộ lọc đầu bảng:
     + Chọn tháng (Tháng 1 -> 12).
     + Lọc theo Giáo viên (Tất cả GV hoặc chọn GV cụ thể).
     + Lọc theo Loại (Tất cả / Dạy thay / Dạy bù).
     + Ô tìm kiếm nhanh (tìm kiếm tên GV, lớp học, lý do).
   - 3 Chip Thống kê nhanh: Tổng lượt trong tháng, Tổng số tiết dạy thay (+), Tổng số tiết dạy bù.
   - Nút hành động: `[Xuất Excel Sổ Dạy Thay]` và `[Đồng bộ số tiết sang Chấm Công]`.
   - **Bảng Nhật Ký**:
     + Cột STT, Loại, Ngày & Thứ, Buổi.
     + Cột **Chi tiết từng tiết & Lớp**: Hiển thị các tag nổi bật (ví dụ: `<span class="period-tag">Tiết 1: 9A1</span> <span class="period-tag">Tiết 2: 9A2</span> <span class="period-tag">Tiết 4: 8A3</span>`).
     + Cột Tổng số tiết (badge đậm).
     + Cột GV thực dạy, Thay cho GV, Lý do.
     + Cột Thao tác: Nút Sửa (✏️) nạp lại form để chỉnh sửa, Nút Xóa (🗑️).

### Bước 3: Cập nhật CSS Giao Diện Chuyên Nghiệp
1. Nâng cấp CSS màu sắc, typography, shadows, bo góc `rounded-xl`, badge, input focus rings theo phong cách Tailwind UI / Modern SaaS.
2. Thiết kế giao diện riêng cho `Period Slots Builder`: Các ô tiết hiển thị dạng thẻ card nhỏ trực quan, khi checkbox được tick thì sáng màu nổi bật (Indigo tint), khi chưa tick thì mờ nhạt (disabled).
3. Thêm CSS cho bảng Sticky Header (`position: sticky; top: 0; z-index: 10; background: #f8fafc;`) để khi cuộn dữ liệu dài không bị mất tiêu đề cột.

### Bước 4: Viết JavaScript Xử Lý Nghiệp Vụ Mới
1. **Hàm chuyển view `switchAppView(viewId)`**:
   - Bổ sung xử lý: Khi `viewId === 'view-daythay'`, gọi hàm `renderDayThayView()`.
2. **Hàm khởi tạo Form phân bổ tiết (`initPeriodSlotsBuilder()`)**:
   - Render 5 hàng/thẻ tương ứng với 5 tiết của buổi (Sáng hoặc Chiều).
   - Lắng nghe sự kiện tick/untick để cập nhật trạng thái disabled của select lớp và tự động đếm tổng số tiết.
   - Viết các hàm trợ giúp chọn nhanh: `setQuickSlots([1,2])`, `setQuickSlots([1,2,3])`, `clearAllSlots()`.
3. **Hàm Lưu / Cập nhật lượt dạy thay (`saveDayThayRecord()`)**:
   - Thu thập thông tin chung (loại, ngày, buổi, GV dạy, GV được thay, lý do).
   - Thu thập mảng `periods_detail`: Lọc các tiết được tick chọn, lấy `period_num`, `class_name`, `subject`.
   - Kiểm tra hợp lệ: Bắt buộc chọn GV dạy và phải chọn ít nhất 1 tiết (kèm lớp).
   - Tính toán các trường tương thích ngược:
     + `period_count = periods_detail.length`
     + `period = periods_detail.map(p => 'Tiết ' + p.period_num + ' (' + p.class_name + ')').join(', ')`
     + `class_name = [...new Set(periods_detail.map(p => p.class_name))].join(', ')`
   - Nếu đang sửa (`editingSubId`): Cập nhật bản ghi tương ứng; nếu mới: `push` bản ghi mới.
   - Tự động gọi `autoSyncSubstitutePeriods()` để số tiết tự động cập nhật ngay lập tức vào Bảng Chấm Công.
   - Lưu vào LocalStorage / kích hoạt Auto-save CSDL.
4. **Hàm Sửa bản ghi (`editDayThayRecord(id)`)**:
   - Tìm bản ghi theo `id`, fill dữ liệu lên các trường của form.
   - Đánh dấu các slot tiết tương ứng trong `periods_detail` (nếu là bản ghi cũ chưa có `periods_detail`, tự động trích xuất tiết từ chuỗi `period` hoặc tick tiết 1 với số tiết = `period_count`).
   - Đổi nút Lưu thành "Cập nhật thay đổi", cuộn mượt lên đầu form.
5. **Hàm Xuất Excel Sổ Dạy Thay (`exportDayThayToExcel()`)**:
   - Tạo file Excel định dạng HTML table chuẩn gồm tiêu đề trường học, tháng, bảng nhật ký có liệt kê chi tiết từng tiết cho từng lớp, chữ ký Tổ trưởng chuyên môn và Hiệu trưởng.
6. **Cập nhật Tab Chấm Công (`view-chamcong`)**:
   - Thay nút "Sổ Dạy Thay - Dạy Bù (X lượt)" cũ bằng nút "Xem chi tiết Sổ Dạy Thay (X lượt)" để chuyển nhanh sang Tab 2 (`switchAppView('view-daythay')`).
   - Cột "Dạy thay (tiết)" và "Dạy bù (tiết)" trong Bảng Chấm Công vẫn tự động hiển thị số tiết được tổng hợp chính xác từ Tab Sổ Dạy Thay.

---

## Rủi ro & Giải pháp
1. **Rủi ro tương thích dữ liệu cũ**: Người dùng có thể đã có dữ liệu chấm công và dạy thay cũ đã lưu trên máy hoặc CSDL chưa có mảng `periods_detail`.
   - *Giải pháp*: Trong tất cả các hàm render và tính toán, luôn kiểm tra nếu `item.periods_detail` tồn tại thì render chi tiết, nếu không thì fallback về `item.period` và `item.class_name` cũ. Hàm tính toán số tiết ưu tiên `item.period_count || item.periods_detail?.length || 1`.
2. **Rủi ro giao diện vỡ trên màn hình nhỏ**:
   - *Giải pháp*: Dùng CSS Grid và Flex-wrap có kiểm soát, thiết lập `min-width` hợp lý cho các cột bảng và cho phép cuộn ngang (`overflow-x: auto`) mượt mà trên thiết bị di động / tablet.

---

## Cách kiểm thử
1. **Kiểm tra giao diện tổng thể**:
   - Mở `phancongtochuyenmon.html` trên trình duyệt: Header sạch sẽ, gọn gàng, không bị tràn vỡ nút.
   - Thanh điều hướng có 5 tab rõ ràng, chuyển đổi giữa 5 tab mượt mà.
2. **Kiểm tra Tab Sổ Dạy Thay & Nhập chi tiết từng tiết**:
   - Chuyển sang Tab "2. Sổ Dạy Thay - Bù".
   - Chọn ngày dạy: 15/09/2025, Buổi Sáng.
   - Chọn GV dạy: Thầy A, Dạy thay cho: Cô B.
   - Trong khu vực chọn tiết:
     + Chọn Tiết 1: Chọn lớp `9A1`.
     + Chọn Tiết 2: Chọn lớp `9A2`.
     + Chọn Tiết 4: Chọn lớp `8A3`.
   - Quan sát badge tổng số tiết: Hiển thị đúng `3 tiết`.
   - Bấm "Lưu vào Sổ Dạy Thay".
   - Kiểm tra Bảng Nhật Ký: Xuất hiện dòng mới hiển thị đúng các tag `Tiết 1: 9A1`, `Tiết 2: 9A2`, `Tiết 4: 8A3`, tổng tiết là 3.
3. **Kiểm tra chức năng Sửa & Xóa**:
   - Bấm nút Sửa bản ghi vừa tạo: Form được điền lại đúng các tiết và lớp đã chọn.
   - Đổi lớp Tiết 4 thành `8A4` và bấm "Cập nhật thay đổi": Bảng cập nhật chính xác.
4. **Kiểm tra đồng bộ sang Tab Chấm Công & Tăng Giờ**:
   - Chuyển sang Tab "3. Chấm công GV": Cột "Dạy thay (tiết)" của Thầy A trong Tháng 9 hiển thị đúng `3` tiết.
   - Chuyển sang Tab "4. Tăng Giờ": Bảng quyết toán tính đúng 3 tiết dạy thay cộng thêm vào tổng số tiết thực dạy của Thầy A.
5. **Kiểm tra Xuất Excel**:
   - Bấm "Xuất Excel Sổ Dạy Thay": File tải về mở được trên Excel, có đầy đủ cột chi tiết tiết và lớp.

---

## Tiêu chí nghiệm thu (Acceptance Criteria)
1. Giao diện toàn trang được cải thiện chuyên nghiệp, hiện đại, bố cục header và các tab ngăn nắp, không bị rối mắt.
2. Chức năng Sổ Dạy Thay - Dạy Bù đã được tách thành một Tab riêng biệt, dễ dàng truy cập và quản lý toàn diện.
3. Người dùng nhập được cụ thể từng tiết cho từng lớp học khác nhau trong cùng một buổi dạy thay/dạy bù (ví dụ: Tiết 1 lớp 9A1, Tiết 2 lớp 9A2, Tiết 4 lớp 8A3).
4. Dữ liệu dạy thay đồng bộ tự động sang Tab Chấm Công và Quyết Toán Tăng Giờ mà không phát sinh lỗi.
5. Tương thích 100% với dữ liệu cũ và CSDL backend MySQL (`api/phancong.php`).