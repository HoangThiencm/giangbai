# PLAN: Triển khai tính năng Kéo thả tiết học trên lưới TKB và thêm Tab "9. Đánh giá xếp loại" (A, B, C, D) trong Quản lý tổ chuyên môn

## Hiện trạng
1. **Kéo thả tiết học trên lưới Thời khoá biểu GV (`phancongtochuyenmon.html`)**:
   - Trên Tab 2 "Thời khoá biểu GV" (`#view-timetable`), mỗi ô tiết học hiện chỉ là một `<button class="tt-cell" onclick="editTimetableCell(...)">`.
   - Người dùng chỉ có thể bấm vào từng ô rồi nhập chữ qua prompt (`Môn - Lớp`) rất thủ công và chậm.
   - Chưa hỗ trợ kéo thả (Drag & Drop) để di chuyển tiết học từ buổi/thứ/tiết này sang ô khác, hoặc hoán đổi vị trí giữa 2 tiết học.
   - Khi AI nhận diện TKB từ ảnh chụp bị lệch hoặc nhầm lẫn vị trí tiết (như người dùng phản ánh), người dùng không thể kéo điều chỉnh nhanh mà phải xóa đi gõ lại từ đầu.

2. **Đánh giá xếp loại hàng tháng**:
   - Tab 6 "Chấm công GV" (`#view-chamcong`) hiện có cột "Đánh giá tháng" nhưng chỉ gồm 4 mức cũ (Tốt, Khá, Đạt, Chưa đạt) nằm ghép chung trong bảng chấm công ngày công.
   - Hệ thống chưa có Tab riêng biệt "9. Đánh giá xếp loại" theo đúng mô hình quản lý tổ chuyên môn với thang xếp loại chuẩn thi đua viên chức: **A, B, C, D** kèm theo cột **Ghi chú** (nêu lý do, thành tích nổi bật, vi phạm hoặc nhắc nhở cần khắc phục), cùng các tiện ích theo dõi theo từng tháng, tự động gợi ý xếp loại dựa trên số liệu chấm công (dạy thay, dự giờ, nghỉ...) và xuất file bảng tổng hợp / Excel đánh giá tháng.

---

## Phạm vi
- **Tính năng 1: Kéo thả tiết học (Drag & Drop) trên lưới Thời khóa biểu GV**:
  + Thêm thuộc tính `draggable="true"` cho các ô có tiết học trên lưới TKB Sáng và Chiều (`phancongtochuyenmon.html`).
  + Xử lý sự kiện kéo thả HTML5 chuẩn: `dragstart`, `dragover`, `dragleave`, `drop`.
  + Khi kéo ô nguồn thả vào ô đích:
    * Nếu ô đích **trống**: Di chuyển tiết học từ ô nguồn sang ô đích (ô nguồn trở về trống).
    * Nếu ô đích **đã có tiết**: Hỗ trợ linh hoạt cả 2 trường hợp như người dùng yêu cầu ("cả 2 luôn vì nhiều khi AI nhận diện nhầm"): hiển thị hộp thoại lựa chọn nhanh hoặc menu context cho phép chọn **Hoán đổi vị trí 2 tiết (Swap)** hoặc **Ghi đè tiết tại ô đích (Overwrite)**.
    * Sau khi kéo thả: tự động cập nhật `editingTimetable`, lưu local, và tự động đồng bộ sang Phân công giảng dạy nếu checkbox "Tự động cập nhật phân công khi lưu TKB" đang bật.
- **Tính năng 2: Thêm Tab "9. Đánh giá xếp loại" với xếp loại A, B, C, D và Ghi chú**:
  + Thêm nút chuyển tab `tab-nav-danhgia` ("9. Đánh giá xếp loại") trên thanh điều hướng `workspace-bar`.
  + Thêm container giao diện `<div class="app-view" id="view-danhgia">` hiển thị bảng đánh giá xếp loại giáo viên theo tháng.
  + Bộ lọc tháng: Chọn tháng đánh giá (Tháng 9, 10, 11, 12, 1, 2, 3, 4, 5...).
  + Bảng đánh giá gồm các cột chuẩn:
    1. STT
    2. Họ và tên giáo viên
    3. Chức vụ / Nhiệm vụ trong tổ
    4. Số tiết dạy/tuần (tổng hợp từ TKB)
    5. Dữ liệu tham khảo từ Chấm công (Dạy thay, Dạy bù, Dự giờ, SHCM, Số tiết nghỉ)
    6. **Xếp loại tháng**: Dropdown chọn các mức **A, B, C, D** (A: Hoàn thành xuất sắc nhiệm vụ; B: Hoàn thành tốt; C: Hoàn thành; D: Chưa hoàn thành).
    7. **Ghi chú**: Cột ô nhập văn bản để ghi chú cụ thể cho từng giáo viên.
  + Các nút tiện ích: "Xếp loại tất cả là A", "Tự động đánh giá theo chấm công", "Xuất Excel Đánh giá", "Lưu CSDL".
  + Cấu trúc lưu trữ dữ liệu trong `state.evaluations.records[monthKey][teacherId] = { rating: 'A', note: '' }`, tự động lưu LocalStorage và CSDL MySQL qua `saveToDB()`.
- **Smoke test**:
  + Cập nhật `tests/timetable-render-smoke.js` bổ sung các bài test tự động cho logic di chuyển/hoán đổi tiết học và cấu trúc giao diện tab Đánh giá xếp loại.

---

## Ngoài phạm vi
- Không sửa đổi schema cơ sở dữ liệu MySQL (trường `data_json` dạng `LONGTEXT` đã tự động hỗ trợ lưu trữ toàn bộ các trường mới trong `state`).
- Không làm thay đổi logic tính toán tăng giờ ở Tab 7 hay các mẫu báo cáo sẵn có ở Tab 8.

---

## File dự kiến tác động
- `phancongtochuyenmon.html`
- `tests/timetable-render-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

---

## Các bước thực hiện
1. **Bước 1: Mở khóa handoff**:
   - Coder xóa file `docs/handoff/.lock` trước khi sửa mã nguồn.
2. **Bước 2: Triển khai tính năng Kéo thả tiết học (Drag & Drop) trong `phancongtochuyenmon.html`**:
   - Thêm biến toàn cục theo dõi ô đang kéo: `let draggedTimetableCell = null;`.
   - Xây dựng các hàm kéo thả:
     + `onTimetableCellDragStart(event, session, day, period)`: lưu thông tin ô nguồn và thiết lập hiệu ứng kéo.
     + `onTimetableCellDragOver(event)`: `event.preventDefault()` và thêm class highlight `drag-target`.
     + `onTimetableCellDragLeave(event)`: xóa class `drag-target`.
     + `onTimetableCellDrop(event, tgtSession, tgtDay, tgtPeriod)`:
       * Lấy dữ liệu nguồn từ `draggedTimetableCell`. Nếu trùng ô nguồn và ô đích thì bỏ qua.
       * Kiểm tra ô đích: nếu trống -> chuyển nội dung từ nguồn sang đích, xóa nguồn.
       * Nếu ô đích đã có tiết -> hỏi người dùng qua dialog xác nhận rõ ràng: "Ô đích đã có tiết [Môn - Lớp]. Bạn muốn: 1. Hoán đổi 2 tiết (OK) | 2. Ghi đè tiết tại ô đích (hoặc bấm Hủy để không đổi)".
       * Cập nhật `editingTimetable`, gọi `renderTimetableGrid()`, `persistAndSaveTimetableLocal()`, và cập nhật phân công (nếu bật `tt-auto-apply-assign`).
   - Cập nhật hàm `renderTimetableSessionGrid` để gắn `draggable="true"` cho ô có dữ liệu và gắn các sự kiện `ondragstart`, `ondragover`, `ondragleave`, `ondrop`.
   - Bổ sung CSS cho lớp `.tt-cell.drag-target` (viền nổi bật màu xanh dương nhạt hoặc tím).
3. **Bước 3: Triển khai Tab "9. Đánh giá xếp loại" (A, B, C, D + Ghi chú)**:
   - Thêm nút tab trong `.view-switcher`:
     ```html
     <button class="view-tab-btn" id="tab-nav-danhgia" onclick="switchAppView('view-danhgia')">
         <i class="fas fa-award"></i> 9. Đánh giá xếp loại
     </button>
     ```
   - Thêm vùng chứa view `<div class="app-view" id="view-danhgia">` với thanh điều khiển tháng, nút lưu CSDL, nút xuất Excel, nút xếp loại nhanh và bảng dữ liệu.
   - Cập nhật hàm `switchAppView(viewId)`: khi `viewId === 'view-danhgia'` thì gọi `renderEvaluation()`.
   - Cập nhật `defaultState` bổ sung:
     ```javascript
     evaluations: {
         current_month: '',
         records: {}
     }
     ```
   - Xây dựng các hàm:
     + `getEvaluationMonthKey()`: lấy mã tháng hiện tại (VD: `2026-09`).
     + `renderEvaluation()`: vẽ bảng danh sách giáo viên với dropdown chọn A, B, C, D (màu sắc trực quan cho từng mức: A xanh lá, B xanh dương, C vàng cam, D đỏ) và input ghi chú.
     + `updateEvaluationRecord(teacherId, field, value)`: cập nhật giá trị vào `state.evaluations.records[mKey][teacherId]`, đánh dấu `hasUnsavedChanges = true` và tự động lưu local.
     + `quickSetAllEvaluation(rating)`: gán nhanh tất cả giáo viên trong tháng sang mức rating được chọn (mặc định A).
     + `autoSuggestEvaluationFromAttendance()`: tự động đối chiếu số liệu chấm công (nếu có nghỉ không phép hoặc vi phạm -> hạ bậc C/D; nếu chuyên cần tốt -> A/B).
     + `exportEvaluationToExcel()`: xuất bảng đánh giá tháng ra file Excel/CSV.
4. **Bước 4: Cập nhật bài test `tests/timetable-render-smoke.js`**:
   - Viết test kiểm tra:
     + Logic hoán đổi/di chuyển ô tiết TKB (di chuyển vào ô trống, hoán đổi 2 ô).
     + Cấu trúc HTML có nút tab `tab-nav-danhgia` và container `view-danhgia`.
     + Logic cập nhật và lưu trữ xếp loại A, B, C, D cùng ghi chú trong state.
   - Chạy `node tests/timetable-render-smoke.js` kiểm tra PASS 100%.
5. **Bước 5: Ghi nhật ký vào `docs/handoff/IMPLEMENT.md` và tạo lại `docs/handoff/.lock` nội dung `LOCK`**.

---

## Rủi ro
- Khi kéo thả giữa 2 buổi khác nhau (ví dụ từ Sáng sang Chiều hoặc ngược lại): cần bảo đảm session nguồn và session đích được cập nhật chính xác trong `editingTimetable[session][day][period]`.
  -> Biện pháp xử lý: Hàm `onTimetableCellDrop` nhận rõ ràng 4 tham số `(tgtSession, tgtDay, tgtPeriod)` và đọc `(srcSession, srcDay, srcPeriod)` từ biến `draggedTimetableCell`.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy `node tests/timetable-render-smoke.js` -> 100% PASS.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở Tab 2: Kéo 1 ô tiết thả vào ô trống -> Tiết di chuyển sang ô đích, ô nguồn trở về trống.
   - Kéo 1 ô tiết thả vào ô đã có tiết -> Hiện xác nhận hoán đổi/ghi đè -> Bấm hoán đổi: 2 tiết đổi chỗ cho nhau hoàn hảo.
   - Bấm sang Tab 9 "Đánh giá xếp loại":
     + Bảng danh sách giáo viên hiện ra đầy đủ với cột xếp loại A, B, C, D và cột Ghi chú.
     + Chọn mức A/B/C/D và nhập ghi chú cho giáo viên.
     + Chuyển sang tháng khác hoặc chuyển tab khác rồi quay lại -> Dữ liệu được bảo toàn nguyên vẹn.
     + Bấm "Lưu tất cả lên CSDL" -> Lưu thành công lên hosting.

---

## Tiêu chí nghiệm thu
- Kéo thả tiết học hoạt động trơn tru trên cả bảng Sáng và Chiều (hỗ trợ cả di chuyển vào ô trống và hoán đổi/ghi đè khi ô đích đã có tiết).
- Tab 9 hiển thị đẹp mắt, xếp loại 4 mức A, B, C, D rõ ràng, có cột Ghi chú và các nút tiện ích.
- Dữ liệu lưu trữ ổn định trên LocalStorage và CSDL MySQL qua API `phancong.php`.
- Smoke test chạy thành công 100% không có lỗi hồi quy.
