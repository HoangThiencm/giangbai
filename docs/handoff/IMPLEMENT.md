# IMPLEMENT

Trạng thái: ĐÃ LÀM

## File đã đổi

- `canvas_xaydungphuluc.html`
- `backupcode viettailieu/canvas_xaydungphuluc.html`

## Nội dung chính

1. **Khắc phục đệ quy vô hạn và lỗi tham chiếu `defaultPpctRows` (`canvas_xaydungphuluc.html`)**:
   - Thêm gán toàn cục `window.defaultPpctRows = defaultPpctRows;` ngay sau định nghĩa hàm và bổ sung fallback an toàn `c = c || {}`.
   - Trong `aiCandidates`: Triệt tiêu vòng lặp đệ quy qua lại giữa `getConfig()` và `selectedAiLessons()` bằng cách gọi `getConfig({includeAiSelection: false})`, đồng thời áp dụng defensive lookup `getRows` (`typeof defaultPpctRows === 'function' ? defaultPpctRows : window.defaultPpctRows`).
   - Trong `aiPickerRows`: Áp dụng pattern kiểm tra an toàn `getRows` và `{includeAiSelection: false}` tương tự.
   - Trong `loadDefaultPpctStructure`: Chuyển sang gọi `getConfig({includeAiSelection: false})` và nạp `sourcePpctRows` bằng `getRows` an toàn trước khi gọi các listener cập nhật AI/NLS.

2. **Đồng bộ hóa 1:1 file backup (`backupcode viettailieu/canvas_xaydungphuluc.html`)**:
   - Đồng bộ hóa toàn diện 100% nội dung từ `canvas_xaydungphuluc.html` sang `backupcode viettailieu/canvas_xaydungphuluc.html` (bao gồm đầy đủ `formatTietCT`, `formatWeek`, `normalizePeriods`, `ppct-sticky`, các xử lý chuẩn hóa bảng và sao lưu/phục hồi nháp).
   - Đảm bảo người dùng lấy code từ file chính hoặc file backup đều hoạt động đồng nhất.

## Test đã thực hiện

- Kiểm tra cú pháp toàn bộ 13 thẻ `<script>` và 12 thư viện CDN bên ngoài: 100% đạt chuẩn cú pháp JS.
- Kiểm tra luồng khởi tạo trang khi `sourcePpctRows` rỗng: không còn lỗi `ReferenceError: defaultPpctRows is not defined`.
- Triệt tiêu hoàn toàn nguy cơ tràn call stack do đệ quy `getConfig()` <-> `aiCandidates()`.
- Chạy kiểm thử thực tế trên Chromium/Edge qua giao thức Chrome DevTools Protocol (CDP) trực tiếp từ URL `blob:`: không phát sinh bất kỳ ngoại lệ cú pháp nào (`SyntaxError`).
- Vượt qua toàn bộ bộ kiểm thử tĩnh `tests/canvas-xaydungphuluc-smoke.js`.

## Vấn đề còn lại

- Không có.


