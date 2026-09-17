# PLAN: Xây Dựng Lịch Báo Giảng Theo Giáo Viên (1 Tháng, Thứ-Ngày-Tháng) & Tự Động Đồng Bộ, Lưu CSDL Phần Chấm Công

## User Review Required
> [!IMPORTANT]
> - **Mục 1 (Lịch báo giảng 1 tháng theo GV bất kỳ)**: Bổ sung bộ lọc chọn giáo viên trong tổ, bộ chọn tháng (30 ngày), và giao diện trực quan chuẩn Sổ Báo Giảng THCS gom theo từng Thứ - Ngày - Buổi - Tiết.
> - **Mục 2 (Tự động đồng bộ và tự lưu CSDL phần Chấm công)**:
>   1. Tự động đồng bộ số tiết Dạy thay & Dạy bù từ Sổ Dạy Thay sang bảng Chấm Công ngay khi mở tab Chấm Công hoặc khi đổi tháng.
>   2. Hàm "Điền chuẩn theo phân công" sẽ tự động lấy đúng số tiết dạy thay/dạy bù thực tế thay vì gán về 0.
>   3. Bổ sung nút "Lưu CSDL" và thanh trạng thái đồng bộ trực tiếp trên thanh công cụ Chấm Công.
>   4. Tự động kích hoạt lưu CSDL tức thì khi thay đổi chấm công, đổi tháng, hoặc khi chuyển tab (loại bỏ độ trễ mất dữ liệu).
> - **Cấm sửa mã ngoài phạm vi**: Chỉ cập nhật giao diện và logic trong `phancongtochuyenmon.html` và viết test kiểm thử tự động.

---

## I. Phân Tích Hiện Trạng & Nguyên Nhân

### 1. Vấn đề Lịch báo giảng
- Hiện tại Tab 4 (Lịch báo giảng) chỉ có ô chọn ngày bắt đầu và số ngày xem (mặc định 14 ngày).
- Hiển thị bảng phẳng dồn tất cả giáo viên vào một bảng lớn, không có bộ lọc chọn giáo viên riêng lẻ và không có bố cục theo từng Thứ - Ngày - Tháng chuẩn Sổ Báo Giảng THCS.

### 2. Vấn đề Chấm công không tự đồng bộ CSDL và tự lưu
- **Nguyên nhân 1 (Thiếu tự động đồng bộ từ Sổ Dạy Thay)**: Khi giáo viên ghi nhận lượt dạy thay / dạy bù ở Tab 5, số tiết chỉ cập nhật vào `attendance.substitutes`. Khi người dùng mở Tab 6 (Chấm công) hoặc đổi tháng (`changeAttendanceMonth`), hệ thống KHÔNG tự động gọi `autoSyncSubstitutePeriods()`.
- **Nguyên nhân 2 (Nút Điền chuẩn xóa mất tiết dạy thay/bù)**: Hàm `autoFillAttendance()` hiện tại gán cứng `teach_replace: 0, makeup_periods: 0`, vô tình xóa sạch số tiết dạy thay/bù đã ghi nhận trong tháng.
- **Nguyên nhân 3 (Cơ chế lưu CSDL bị ngắt quãng)**:
  + Các ô nhập điểm danh, số tiết, xếp loại, ghi chú chỉ kích hoạt `onchange` (phải click ra ngoài mới chạy) và chỉ gọi `saveToLocal()`.
  + `saveToLocal()` dùng debounce 1500ms để gọi ngầm `performSaveToDB({ isAuto: true })`. Nếu người dùng đổi tháng, chuyển tab hoặc đóng trình duyệt trước 1.5 giây, lệnh lưu CSDL sẽ không được gửi đi.
  + Hàm `changeAttendanceMonth(val)` hoàn toàn không gọi `saveToLocal()` hay lưu CSDL.
- **Nguyên nhân 4 (Thiếu nút và chỉ báo lưu tại chỗ)**: Tab Chấm công không có nút "Lưu CSDL" riêng (như ở tab Báo giảng hay Dạy thay), và không có biểu tượng trạng thái lưu tại chỗ, khiến người dùng không biết dữ liệu đã lên CSDL MySQL hay chưa.

---

## II. Kế Hoạch Triển Khai Chi Tiết

### PHẦN A: LỊCH BÁO GIẢNG 1 THÁNG THEO GIÁO VIÊN (THỨ - NGÀY - THÁNG)

#### Module 1: Thanh Công Cụ & Bộ Lọc Lịch Báo Giảng (`view-baogiang`)
1. **Dropdown chọn Giáo viên (`#bg-filter-teacher`)**:
   - Danh sách giáo viên trong tổ (`state.teachers`), mặc định chọn giáo viên đầu tiên hoặc giáo viên đang đăng nhập.
   - Có tùy chọn `[Tất cả giáo viên]` để xem toàn tổ.
2. **Bộ chọn Tháng & Điều hướng thời gian (`#bg-filter-month`)**:
   - Input tháng `type="month"` (ví dụ: `2026-09`).
   - Nút điều hướng nhanh: `◀ Tháng trước`, `Tháng này`, `Tháng sau ▶`.
   - Tự động tính ngày đầu tháng (`YYYY-MM-01`) đến ngày cuối tháng (`YYYY-MM-LastDay`).
3. **Giao diện chuẩn Sổ Báo Giảng THCS theo Thứ - Ngày - Tháng**:
   - Gom nhóm từng ngày có tiết dạy trong tháng: `Thứ Hai, Ngày 07/09/2026 (Tuần 1)`.
   - Chia 2 bảng rõ rệt: **Buổi sáng** (Tiết 1–5) và **Buổi chiều** (Tiết 1–4).
   - Cột: Tiết | Lớp | Môn | Tiết PPCT | Tên bài dạy | Phân đoạn/Mạch kiến thức.
   - Nút **In Sổ Báo Giảng (Print)** chuẩn A4 và **Xuất Excel** báo giảng tháng.

---

### PHẦN B: TỰ ĐỘNG ĐỒNG BỘ VÀ TỰ LƯU CSDL PHẦN CHẤM CÔNG

#### Module 2: Tự Động Đồng Bộ Số Tiết Dạy Thay / Dạy Bù Sang Chấm Công
1. **Tự động kích hoạt đồng bộ khi xem Chấm công**:
   - Trong hàm `renderAttendance()`: Tự động chạy `autoSyncSubstitutePeriods({ silent: true, mKey, autoSave: false })` trước khi hiển thị bảng, đảm bảo số tiết dạy thay/bù từ Sổ Dạy Thay luôn luôn khớp 100% với Chấm công mà không cần người dùng phải bấm nút thủ công.
   - Khi chuyển tháng trong `changeAttendanceMonth(val)`: Đồng bộ ngay số liệu của tháng mới, lưu vào `state.attendance.current_month`, gọi `saveToLocal()` và tự động lưu CSDL.
2. **Nâng cấp `autoFillAttendance()`**:
   - Khi bấm "Điền chuẩn theo phân công": Điền `w1..w4: 'Đủ'`, `observe: 1`, `meeting: 2`, `rating: 'Tốt'`.
   - Đồng thời **bảo lưu hoặc tự động tính toán lại ngay** số tiết `teach_replace` và `makeup_periods` từ `state.attendance.substitutes[mKey]`, KHÔNG bị gán về 0.
   - Sau khi điền chuẩn: Gọi `saveToDB()` lưu thẳng vào CSDL và báo thông báo thành công.

#### Module 3: Hoàn Thiện Cơ Chế Tự Động Lưu CSDL Cho Chấm Công
1. **Bổ sung nút thao tác và chỉ báo trạng thái trên thanh công cụ Chấm công (`.attendance-toolbar`)**:
   - Thêm nút: `<button class="btn-small btn-small-primary" onclick="saveAttendanceToDB()"><i class="fas fa-cloud-arrow-up"></i> Lưu Chấm Công vào CSDL</button>`.
   - Thêm nút: `<button class="btn-small" onclick="autoSyncSubstitutePeriods()"><i class="fas fa-rotate"></i> Đồng bộ từ Sổ Dạy Thay</button>`.
   - Thêm badge trạng thái tại chỗ: `<span id="att-db-status" style="font-size:0.8rem; font-weight:700;"></span>` hiển thị rõ: "Đã lưu CSDL", "Đang lưu...", hoặc "Chưa lưu".
2. **Cải tiến hàm cập nhật ô chấm công `updateAttRecord`**:
   - Hỗ trợ cả sự kiện `change` và `blur`.
   - Cập nhật trạng thái `hasUnsavedChanges = true`.
   - Tự động debounce lưu CSDL (`scheduleAutoSave()`).
   - Cập nhật badge `#att-db-status` để người dùng an tâm dữ liệu đã được tự động lưu.
3. **Bảo toàn dữ liệu khi chuyển View / chuyển Đợt**:
   - Trong `switchAppView(viewId)`: Nếu có thay đổi chấm công chưa lưu, tự động gọi `performSaveToDB({ isAuto: true })` trước khi chuyển sang tab khác.
   - Khi chọn tháng khác (`changeAttendanceMonth`): Tự động lưu tháng cũ và tải/lưu tháng mới.

---

## III. Danh Sách File Cần Chỉnh Sửa

| Tệp tin | Vị trí | Mục đích thay đổi |
| :--- | :--- | :--- |
| `phancongtochuyenmon.html` | Tab `#view-baogiang` (Dòng ~2020–2035) | Bổ sung bộ lọc GV, bộ chọn Tháng, chuyển chế độ xem Thứ-Ngày-Tháng, nút In/Xuất |
| `phancongtochuyenmon.html` | Hàm `renderBaoGiangView` (Dòng ~3847–3900) | Lọc theo giáo viên được chọn, tính phạm vi tháng, render thẻ theo Thứ-Ngày-Tháng |
| `phancongtochuyenmon.html` | Tab `#view-chamcong` (Dòng ~2195–2225) | Thêm nút Lưu CSDL, nút Đồng bộ Sổ Dạy Thay, badge trạng thái lưu CSDL |
| `phancongtochuyenmon.html` | Hàm `renderAttendance`, `updateAttRecord`, `autoFillAttendance`, `changeAttendanceMonth` (Dòng ~5256–5366) | Tự động đồng bộ số tiết từ Sổ Dạy Thay, không xóa mất tiết khi điền chuẩn, tự động lưu CSDL khi sửa ô hoặc đổi tháng |
| `phancongtochuyenmon.html` | Hàm `switchAppView` (Dòng ~3901–3925) | Tự động lưu dữ liệu đang dở trước khi đổi tab |
| `tests/baogiang-teacher-month-smoke.js` | Tạo mới | Kiểm thử tự động tính năng lọc giáo viên và lịch báo giảng 1 tháng |
| `tests/attendance-autosync-smoke.js` | Tạo mới | Kiểm thử tự động đồng bộ Sổ Dạy Thay sang Chấm Công và tự lưu CSDL |

---

## IV. Kế Hoạch Kiểm Thử (Verification Plan)

### 1. Kiểm thử tự động (Smoke Tests)
- `node tests/attendance-autosync-smoke.js` — PASS 100% (Kiểm tra auto-sync từ Sổ Dạy Thay vào Chấm công, không mất tiết khi autoFill, tự động kích hoạt lưu).
- `node tests/baogiang-teacher-month-smoke.js` — PASS 100% (Kiểm tra lọc giáo viên bất kỳ và tính toán ngày/buổi/tiết trong tháng).
- `node tests/baogiang-weekday-segment-smoke.js` — PASS 100%.
- `node tests/baogiang-recognition-smoke.js` — PASS 100%.
- `node tests/timetable-render-smoke.js` — PASS 100%.

### 2. Kiểm thử thủ công trên giao diện
1. **Lịch báo giảng**:
   - Vào tab "4. Lịch báo giảng" -> Chọn GV bất kỳ -> Chọn Tháng -> Kiểm tra giao diện hiển thị đúng từng Thứ, Ngày, Buổi sáng/chiều và bài học PPCT.
2. **Chấm công & Tự động đồng bộ**:
   - Vào tab "5. Sổ Dạy Thay - Bù" -> Thêm 1 lượt dạy thay cho GV A (ví dụ 3 tiết).
   - Sang tab "6. Chấm công GV" -> Kiểm tra cột "Dạy thay" của GV A đã tự động nhảy số 3 mà không cần bấm thủ công.
   - Thử bấm "Điền chuẩn theo phân công" -> Xác nhận cột Dạy thay vẫn giữ nguyên số 3 (không bị về 0).
   - Sửa ghi chú hoặc xếp loại của 1 GV -> Xác nhận badge "Đã lưu CSDL" báo xanh thành công.
   - Tải lại trang (F5) -> Xác nhận toàn bộ dữ liệu chấm công và tháng đang chọn vẫn được bảo toàn nguyên vẹn từ CSDL.
