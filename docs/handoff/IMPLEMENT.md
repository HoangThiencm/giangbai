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

2. **Bổ sung định nghĩa còn thiếu trong backup (`backupcode viettailieu/canvas_xaydungphuluc.html`)**:
   - Thêm các hàm phụ trợ cốt lõi trước `aiCandidates`: `emptyPpctRow`, `ppctRow`, `SUBJECT_SAMPLE_TOPICS`, `defaultPpctRows`, `fallback`, và gán `window.defaultPpctRows = defaultPpctRows`.
   - Cập nhật các vị trí gọi trong `aiCandidates`, `aiPickerRows`, `loadDefaultPpctStructure` sử dụng cơ chế an toàn `{includeAiSelection: false}` và defensive check.

## Test đã thực hiện

- Kiểm tra luồng khởi tạo trang khi `sourcePpctRows` rỗng: không còn lỗi `ReferenceError: defaultPpctRows is not defined`.
- Triệt tiêu hoàn toàn nguy cơ tràn call stack do đệ quy `getConfig()` <-> `aiCandidates()`.
- Đảm bảo tương thích với bộ kiểm thử tĩnh `tests/canvas-xaydungphuluc-smoke.js` (`defaultPpctRows(getConfig({includeAiSelection:false}))`).

## Vấn đề còn lại

- Không có.

