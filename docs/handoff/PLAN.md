# PLAN: Khắc phục tính vô lý khi chọn GV nghỉ, đảm bảo luôn hiển thị Đề xuất dạy thay & Hỗ trợ kéo thả/sắp xếp Nhật ký

## 1. Phân tích nguyên nhân & Phản hồi của người dùng

### Vấn đề 1: Tính vô lý và "chưa thấy" bảng đề xuất 2 cột
1. **Tại sao người dùng "chưa thấy" bảng đề xuất 2 cột**:
   - Trong ảnh 2 người dùng gửi, ngày đang chọn là `09/12/2026` (Thứ Bảy).
   - Đối chiếu với TKB của thầy Nguyễn Văn Tính (ảnh 1): Thầy Tính chỉ có giờ vào Thứ 2, Thứ 4, Thứ 5. **Thứ Bảy thầy Tính không có tiết nào cả**.
   - Do thầy Tính không có tiết, nên không có tiết nào được tick (`Tổng cộng: 0 tiết`).
   - Logic code hiện tại đang ràng buộc: `canSuggest = ... && neededPeriods.length > 0; panel.hidden = !canSuggest`.
   - Vì `neededPeriods.length === 0`, bảng đề xuất `#daythay-suggestion-panel` bị **ẩn hoàn toàn** (`hidden`), khiến người dùng không nhìn thấy bảng đề xuất đâu và nghĩ rằng tính năng chưa được làm!
2. **Tại sao vô lý**:
   - Khi một giáo viên không có tiết dạy trong ngày/buổi đó, việc form vẫn hiển thị Buổi sáng và gán người dạy thay với 0 tiết là hoàn toàn phi thực tế.
   - Cần có cảnh báo rõ ràng ngay trên màn hình: *"Thầy/cô không có tiết dạy trong ngày/buổi này, không cần phân công dạy thay!"*.
   - Khung đề xuất `#daythay-suggestion-panel` **không được ẩn mất tăm**. Ngay cả khi chưa chọn tiết hoặc ngày đó không có tiết, panel phải luôn hiện diện với thông điệp/hướng dẫn phù hợp để người dùng luôn thấy tính năng đề xuất thông minh.
   - Khi chọn một ngày/buổi mà GV nghỉ CÓ TIẾT (như Thứ 4, Thứ 5): Hệ thống phải nạp ngay các tiết đó và hiển thị rõ ràng bảng 2 cột:
     - **Cột 1: Giáo viên trống cả buổi**.
     - **Cột 2: Giáo viên có mặt, trống tiết cần thay**.

### Vấn đề 2: Nhật ký chi tiết lộn xộn ngày (Thứ Năm trước Thứ Tư) và không kéo thay đổi được
- Trong ảnh 3: Ngày 17/09 (Thứ Năm) đứng trước Ngày 16/09 (Thứ Tư) vì hiện tại bảng hiển thị theo thứ tự thêm vào (insertion order).
- Chưa có cơ chế tự động sắp xếp theo trình tự thời gian tăng dần (`Ngày` -> `Buổi Sáng trước Chiều` -> `Tiết`).
- Chưa có tính năng kéo thả (Drag & Drop) để người dùng chủ động đổi vị trí các dòng trong Nhật ký chi tiết.

---

## 2. Giải pháp chi tiết cần triển khai

### A. Tối ưu trải nghiệm Form & Đảm bảo luôn hiển thị Đề xuất thông minh (`phancongtochuyenmon.html`)

1. **Bảng đề xuất `#daythay-suggestion-panel` luôn hiển thị trực quan**:
   - Bỏ trạng thái `hidden` cứng khi chưa có tiết.
   - Khi đã chọn Loại hình = Dạy thay và chọn Giáo viên nghỉ:
     - **Trường hợp GV nghỉ có tiết trong buổi/ngày đã chọn**: Hiển thị bảng đề xuất 2 cột chuẩn:
       - Cột 1: Giáo viên trống cả buổi / cả ngày.
       - Cột 2: Giáo viên có mặt tại trường, trống các tiết cần thay.
       - Nút `[Chọn dạy thay]` gán trực tiếp vào ô `Giáo viên thực dạy`.
     - **Trường hợp GV nghỉ không có tiết trong ngày/buổi đó**:
       - Hiển thị hộp thông báo màu xanh nhạt/vàng: *"ℹ️ Thầy/cô [Tên] không có tiết dạy trong [Buổi/Ngày] này. Hãy chọn buổi khác hoặc ngày khác có lịch dạy để hệ thống đề xuất."*
     - **Trường hợp chưa chọn tiết nào**:
       - Hiển thị hướng dẫn: *"💡 Hãy tick chọn các tiết cần dạy thay bên dưới để hệ thống tính toán giáo viên phù hợp."*
2. **Cảnh báo rõ ràng tại khung Preview TKB khi GV không có tiết**:
   - Khi ngày được chọn không có tiết dạy nào (như Thứ Bảy của thầy Tính):
     - Hiển thị badge / alert rõ ràng: *"⚠️ Thầy/cô [Tên] không có lịch dạy vào [Thứ X, ngày Y]. Không có tiết cần phân công dạy thay."*
     - Các nút chọn buổi sẽ disable hoặc ẩn nếu buổi đó 0 tiết.

### B. Tự động sắp xếp & Kéo thả (Drag & Drop) trong Nhật ký chi tiết

1. **Mặc định tự động sắp xếp theo trình tự thời gian**:
   - Trong `renderDayThayJournal()`:
     - Sắp xếp danh sách theo:
       1. Ngày (`date` tăng dần: 16/09 trước 17/09).
       2. Buổi (`session`: Sáng `morning` trước Chiều `afternoon`).
       3. Tiết bắt đầu (tiết nhỏ trước tiết lớn).
   - Thêm nút tiện ích `[<i class="fas fa-arrow-down-short-wide"></i> Sắp xếp theo ngày]` trên thanh công cụ Nhật ký để người dùng có thể kích hoạt sắp xếp lại danh sách gốc bất cứ lúc nào.
2. **Tính năng Kéo thả (Drag & Drop Reorder)**:
   - Thêm biểu tượng kéo thả `<i class="fas fa-grip-vertical drag-handle"></i>` vào cột STT của từng hàng trong bảng.
   - Thiết lập `draggable="true"` cho thẻ `<tr>`.
   - Xử lý các sự kiện:
     - `ondragstart`: Lưu lại vị trí dòng đang kéo.
     - `ondragover`: Cho phép drop và thêm hiệu ứng highlight viền dòng mục tiêu.
     - `ondrop`: Hoán đổi vị trí trong mảng `state.attendance.substitutes[mKey]`.
     - `ondragend`: Xóa hiệu ứng highlight.
   - Sau khi drop: Tự động đánh lại STT 1, 2, 3... và kích hoạt `triggerAutoSave()`.

---

## 3. Phạm vi tệp tin thay đổi

1. `phancongtochuyenmon.html`:
   - Cập nhật `renderAbsentTeacherSchedulePreview()`: bổ sung cảnh báo khi ngày/buổi không có tiết.
   - Cập nhật `renderDayThaySuggestions()`: không ẩn giấu panel khi `neededPeriods.length === 0`, hiển thị trạng thái hướng dẫn/thông báo phù hợp.
   - Cập nhật `renderDayThayJournal()`:
     - Tự động sắp xếp theo ngày và buổi.
     - Tích hợp HTML5 Drag & Drop reorder cho các dòng nhật ký.
     - Bổ sung nút "Sắp xếp theo ngày" trên thanh công cụ.
2. `tests/daythay-suggest-smoke.js`:
   - Bổ sung kiểm thử:
     - Panel đề xuất luôn hiển thị trạng thái hướng dẫn/thông báo ngay cả khi 0 tiết.
     - Kiểm thử logic tự động sắp xếp nhật ký theo ngày tăng dần.
     - Kiểm thử hàm hoán đổi vị trí (drag-and-drop reorder) của mảng nhật ký.

---

## 4. Kế hoạch kiểm thử (Verification Plan)

1. `node tests/daythay-suggest-smoke.js`: PASS toàn bộ kiểm thử mới.
2. `node tests/baogiang-weekday-segment-smoke.js`: PASS.
3. `node tests/timetable-render-smoke.js`: PASS.
4. `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
5. `node tests/auto-reload-smoke.js`: PASS.
6. `git diff --check`: PASS (không lỗi cú pháp/khoảng trắng).
