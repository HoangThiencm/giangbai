# PLAN: Tối ưu quy trình ghi nhận Dạy thay: Chọn GV nghỉ trước, hiển thị TKB ngày nghỉ và đề xuất người dạy thay

## Hiện trạng & Vấn đề logic người dùng phản ánh

1. **Thứ tự trường trên Form bị ngược quy trình tư duy**:
   - Hiện tại, ô "Giáo viên thực dạy" lại nằm ở vị trí đầu tiên trước ô "Dạy thay cho giáo viên (nghỉ)".
   - Trong thực tế, Tổ trưởng luôn biết **ai xin nghỉ trước**, sau đó mới đi tìm người dạy thay. Việc đặt ô người dạy thay lên đầu gây gượng gạo, dễ nhầm lẫn.

2. **Chưa thấy TKB của giáo viên nghỉ nên không biết nghỉ buổi nào**:
   - Khi chọn ngày và chọn giáo viên nghỉ, Tổ trưởng không biết hôm đó giáo viên đó có tiết sáng hay chiều, hay cả ngày, gồm những tiết nào, lớp nào.
   - Khi chọn Buổi dạy (Sáng/Chiều), nếu chọn sai buổi mà GV không có tiết, hệ thống báo "không có tiết" và xóa rỗng lưới tiết, khiến người dùng phải tự mò mẫm thử lại.

---

## Mục tiêu & Giải pháp thiết kế

### 1. Đổi thứ tự trực quan các trường trên Form
Sắp xếp lại form `#daythay-form-card` theo luồng logic tự nhiên 3 bước:
- **Hàng 1 — Thông tin nghỉ dạy**:
  - `Loại hình` (`#new-sub-type`): Dạy thay / Dạy bù.
  - `Ngày nghỉ / Ngày dạy` (`#new-sub-date`): Chọn ngày (hiển thị Thứ).
  - `Giáo viên nghỉ (Dạy thay cho giáo viên)` (`#group-for-teacher` / `#new-sub-for-teacher`): **Đưa lên vị trí ưu tiên số 1** ngay cạnh Ngày nghỉ.
- **Hàng 2 — Khung xem nhanh TKB của Giáo viên nghỉ trong ngày (`#daythay-absent-schedule-preview`)**:
  - Ngay khi chọn Ngày + Giáo viên nghỉ, một khung preview lịch dạy trực quan xuất hiện:
    - Hiển thị đầy đủ: Lịch dạy Thứ X của thầy/cô [Tên]:
      - `☀️ Buổi sáng`: Tiết [X] (Lớp [L] - Môn [M]), Tiết [Y]... (hoặc *Không có tiết*).
      - `🌙 Buổi chiều`: Tiết [Z] (Lớp [L] - Môn [M])... (hoặc *Không có tiết*).
    - **Cơ chế tự động chọn buổi (`auto-detect session`)**:
      - Nếu giáo viên chỉ có tiết Buổi sáng -> Tự động chọn `#new-sub-session = 'morning'` và tự nạp các tiết sáng vào bảng phân bổ.
      - Nếu giáo viên chỉ có tiết Buổi chiều -> Tự động chọn `#new-sub-session = 'afternoon'` và tự nạp các tiết chiều vào bảng phân bổ.
      - Nếu giáo viên có tiết cả hai buổi -> Tự động chọn `#new-sub-session = 'all_day'` và nạp toàn bộ tiết trong ngày.
      - Kèm nút bấm nhanh: `[Chọn buổi Sáng]`, `[Chọn buổi Chiều]`, `[Chọn Cả ngày]` để người dùng chuyển đổi tức thì chỉ bằng 1 click.
- **Hàng 3 — Thông tin phân công dạy thay**:
  - `Buổi dạy` (`#new-sub-session`): Sáng / Chiều / Cả ngày.
  - `Giáo viên thực dạy` (`#new-sub-teacher`): Người được phân công dạy thay.
  - `Lý do / Căn cứ thay` (`#new-sub-reason`).
- **Hàng 4 — Bảng đề xuất thông minh 2 cột** (`#daythay-suggestion-panel`):
  - Hiển thị danh sách giáo viên có thể dạy thay:
    - **Cột 1**: Giáo viên trống cả buổi / cả ngày.
    - **Cột 2**: Giáo viên có mặt tại trường nhưng trống đúng các tiết cần thay.
  - Bấm nút `[Chọn dạy thay]` -> tự động điền vào ô "Giáo viên thực dạy".

---

## Chi tiết kỹ thuật cần triển khai

### 1. Giao diện HTML (`phancongtochuyenmon.html`)
- Hoán đổi vị trí giữa `#group-for-teacher` (Dạy thay cho giáo viên) và `#new-sub-teacher` (Giáo viên thực dạy).
- Thêm container `#daythay-absent-schedule-preview` ngay dưới Hàng 1.
  - Khi chưa chọn GV nghỉ hoặc loại hình là `makeup`: ẩn container này.
  - Khi đã chọn GV nghỉ: hiển thị thẻ tóm tắt TKB với badge màu sắc rõ ràng (màu vàng cam cho Sáng, màu xanh lam cho Chiều).

### 2. Hàm hiển thị TKB ngày nghỉ & tự động chọn buổi (`renderAbsentTeacherSchedulePreview`)
- Xây dựng hàm `renderAbsentTeacherSchedulePreview()`:
  - Lấy ngày từ `#new-sub-date`, lấy giáo viên từ `#new-sub-for-teacher`.
  - Tính `dayNum = weekdayNumberFromDate(date)`.
  - Lấy `morningSlots = getTimetableDaySlots(teacher, 'morning', dayNum)`.
  - Lấy `afternoonSlots = getTimetableDaySlots(teacher, 'afternoon', dayNum)`.
  - Render thẻ HTML preview TKB ngày đó:
    - Liệt kê chi tiết tiết, lớp, môn của từng buổi.
    - Nếu có tiết sáng mà không có tiết chiều: tự động set `#new-sub-session` thành `'morning'` (nếu người dùng chưa tự đổi thủ công).
    - Nếu có tiết chiều mà không có tiết sáng: tự động set `#new-sub-session` thành `'afternoon'`.
    - Nếu có cả 2 buổi: tự động set `#new-sub-session` thành `'all_day'`.
  - Sau khi xác định buổi, tự động gọi nạp tiết vào form và tính bảng đề xuất dạy thay 2 cột.

### 3. Tích hợp sự kiện
- Khi thay đổi `#new-sub-for-teacher`:
  - Gọi `renderAbsentTeacherSchedulePreview()`.
  - Tự động đồng bộ buổi dạy và đề xuất giáo viên dạy thay.
- Khi thay đổi `#new-sub-date`:
  - Cập nhật lại `renderAbsentTeacherSchedulePreview()`.

---

## Phạm vi thực hiện

1. `phancongtochuyenmon.html`:
   - Hoán đổi thứ tự hiển thị của cụm "Dạy thay cho giáo viên" lên trước "Giáo viên thực dạy".
   - Thêm container `#daythay-absent-schedule-preview`.
   - Viết hàm `renderAbsentTeacherSchedulePreview()`.
   - Kết nối sự kiện `onchange` của `#new-sub-for-teacher` và `#new-sub-date` để tự động render lịch và tự chọn buổi.
2. `tests/daythay-suggest-smoke.js`:
   - Bổ sung kiểm tra:
     - Khung preview TKB giáo viên nghỉ được render đúng theo ngày.
     - Cơ chế auto-detect session khi giáo viên nghỉ chỉ dạy sáng, chỉ dạy chiều hoặc dạy cả ngày.
     - Đề xuất giáo viên cập nhật ngay sau khi chọn giáo viên nghỉ.

---

## Ngoài phạm vi

- Không thay đổi cấu trúc lưu trữ của Sổ Dạy Thay (`state.attendance.substitutes`).
- Không thay đổi bảng quyết toán hay báo cáo tăng giờ.

---

## Kế hoạch kiểm thử (Verification Plan)

1. `node tests/daythay-suggest-smoke.js`: PASS kiểm thử luồng chọn GV nghỉ trước, preview TKB và auto-detect buổi dạy.
2. `node tests/baogiang-weekday-segment-smoke.js`: PASS.
3. `node tests/timetable-render-smoke.js`: PASS.
4. `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
5. `node tests/auto-reload-smoke.js`: PASS.
6. `git diff --check`: PASS.
