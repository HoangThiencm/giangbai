# PLAN: Sửa Lỗi Danh Sách Giáo Viên Trống Trong Lịch Báo Giảng & Hỗ Trợ Tự Động Nhận Giáo Viên Từ PCCM / Các Đợt

## User Review Required
> [!IMPORTANT]
> - **Hiện tượng người dùng phản ánh**: Đã có Phân công chuyên môn (PCCM), nhưng khi mở Tab 4 "Lịch báo giảng", dropdown **Giáo viên** chỉ có duy nhất lựa chọn `"Tất cả giáo viên"`, không có tên bất kỳ giáo viên nào.
> - **Nguyên nhân kỹ thuật**:
>   1. **Nguồn dữ liệu giáo viên bị phụ thuộc cứng vào `state.teachers`**: Dropdown `#bg-filter-teacher` hiện tại chỉ map từ `state.teachers` ở root. Nếu giáo viên nằm trong đợt phân công hiện tại (`state.phase_assignments[curPhase].teachers`) mà chưa được đồng bộ ra root, hoặc đang mở đợt chưa nạp snapshot, thì `state.teachers` rỗng `[]`.
>   2. **Chưa có cơ chế fallback thông minh**: Không tự động quét giáo viên từ các đợt phân công (`phase_assignments`), từ bảng phân công lớp (`assignments`), hay từ CSDL giáo viên hệ thống (`systemData.teachers`).
>   3. **Nguyên lý sinh Lịch báo giảng**: Lịch báo giảng cần **Thời khóa biểu (TKB ở Tab 2)** + **PPCT** để tự ghép lịch dạy. Nếu người dùng chỉ mới phân công môn-lớp ở Tab 1 (PCCM) mà chưa nhập TKB ở Tab 2, hệ thống không có dữ liệu thứ/tiết để sinh dòng lịch. Tuy nhiên, dropdown Giáo viên **vẫn bắt buộc phải hiển thị đầy đủ danh sách giáo viên đã có trong PCCM** để người dùng lựa chọn và kiểm tra.
>   4. **Thiếu thông báo điều hướng**: Khi chưa có giáo viên hoặc giáo viên chưa có TKB, giao diện chỉ hiện một dòng mờ nhạt "Chưa có tiết TKB trong tháng này", không chỉ dẫn người dùng cần làm gì tiếp theo.

---

## I. Kế Hoạch Triển Khai Chi Tiết

### Module 1: Xây Dựng Hàm Chuẩn Hóa Danh Sách Giáo Viên Cho Lịch Báo Giảng (`getBaoGiangTeacherList`)
Trong `phancongtochuyenmon.html`:
1. Viết hàm `getBaoGiangTeacherList()`:
   - Ưu tiên 1: Lấy `state.teachers` nếu có phần tử.
   - Ưu tiên 2: Nếu `state.teachers` rỗng, lấy từ đợt phân công hiện tại: `state.phase_assignments?.[state.info?.current_phase_id]?.teachers`.
   - Ưu tiên 3: Gom tất cả giáo viên duy nhất (theo `id` / `name`) từ toàn bộ các đợt trong `state.phase_assignments`.
   - Ưu tiên 4: Nếu vẫn rỗng, fallback về `systemData.teachers` (nếu đã nạp từ CSDL hệ thống).
   - Đảm bảo luôn trả về danh sách giáo viên đầy đủ, loại bỏ trùng lặp.
2. Đồng bộ ngược lại `state.teachers` nếu root bị rỗng nhưng đợt hiện tại có giáo viên, tránh tình trạng mất đồng bộ giữa các view.

### Module 2: Nâng Cấp Render Dropdown & Bảng Lịch Báo Giảng
1. Trong `renderBaoGiangMonthView()`:
   - Dùng `getBaoGiangTeacherList()` để render dropdown `#bg-filter-teacher`.
   - Hiển thị rõ số lượng giáo viên: `Tất cả giáo viên (X GV)`.
   - Từng option giáo viên hiển thị: `Họ tên GV (Chức vụ / Số lớp phân công)`.
2. Hỗ trợ hiển thị lịch ngay cả khi chỉ có PCCM (chưa có TKB chi tiết từng tiết):
   - Nếu giáo viên đã có phân công lớp/môn ở Tab 1 nhưng chưa có TKB chi tiết ở Tab 2:
     Hiển thị thẻ cảnh báo hướng dẫn rõ ràng:
     `⚠️ Thầy/cô [Tên GV] đã có phân công chuyên môn ([Môn] lớp [Lớp]), nhưng chưa được xếp Thời khóa biểu cụ thể theo thứ/tiết ở Tab "2. Thời khoá biểu GV". Vui lòng nhập TKB để hệ thống tự động ghép bài dạy theo ngày.`
   - Có nút bấm nhanh: `👉 Sang Tab Thời khóa biểu GV để nhập TKB cho thầy/cô này`.

### Module 3: Kiểm Thử Tự Động (`tests/baogiang-teacher-month-smoke.js`)
1. Bổ sung kịch bản test:
   - Test case 1: Khi `state.teachers` rỗng nhưng `state.phase_assignments` có giáo viên -> dropdown `#bg-filter-teacher` vẫn hiển thị đầy đủ danh sách giáo viên.
   - Test case 2: Khi có giáo viên nhưng chưa có TKB -> hiển thị hướng dẫn thân thiện, không bị crash hoặc trắng bảng.
   - Test case 3: Khi có giáo viên và có TKB -> hiển thị đầy đủ lịch báo giảng theo tháng và theo giáo viên đã chọn.

---

## II. Danh Sách File Cần Chỉnh Sửa

| Tệp tin | Vị trí | Mục đích thay đổi |
| :--- | :--- | :--- |
| `phancongtochuyenmon.html` | Dòng ~3060 (`renderBaoGiangMonthView`) | Dùng `getBaoGiangTeacherList()` fallback thông minh từ `phase_assignments`, hiển thị danh sách GV đầy đủ |
| `phancongtochuyenmon.html` | Dòng ~3920 (`renderBaoGiangView`) | Đồng bộ `state.teachers` từ đợt hiện tại nếu root bị rỗng, hiển thị banner hướng dẫn TKB |
| `tests/baogiang-teacher-month-smoke.js` | Cuối file | Bổ sung test kiểm tra fallback giáo viên từ phase_assignments |

---

## III. Kế Hoạch Kiểm Thử (Verification Plan)

### 1. Kiểm thử tự động
- `node tests/baogiang-teacher-month-smoke.js` — PASS 100%.
- `node tests/attendance-autosync-smoke.js` — PASS 100%.
- `node tests/baogiang-weekday-segment-smoke.js` — PASS 100%.

### 2. Kiểm thử thủ công
1. Mở `phancongtochuyenmon.html` với kế hoạch có giáo viên trong đợt phân công.
2. Chuyển sang Tab **4. Lịch báo giảng**.
3. Mở dropdown **Giáo viên** -> Xác nhận hiển thị đầy đủ danh sách tất cả các giáo viên trong tổ.
4. Chọn một giáo viên cụ thể -> Xem lịch báo giảng theo tháng của giáo viên đó.
