# PLAN: Khắc phục lỗi ReferenceError: defaultPpctRows is not defined trên canvas_xaydungphuluc

## Hiện trạng & Nguyên nhân
Khi chạy `canvas_xaydungphuluc.html` trong môi trường Gemini Canvas (`blob:https://...scf.usercontent.goog/...`), xảy ra lỗi:
`ReferenceError: defaultPpctRows is not defined at aiCandidates` khi trang khởi động (`DOMContentLoaded` -> `loadDefaultPpctStructure(true)`).

Nguyên nhân chính:
1. **Thiếu định nghĩa trong `backupcode viettailieu/canvas_xaydungphuluc.html`**:
   - Trong file này, hàm `defaultPpctRows` được gọi tại 3 vị trí (dòng 1242, 1332, 1376) nhưng hoàn toàn KHÔNG CÓ định nghĩa `function defaultPpctRows(c)`. Nếu người dùng copy code từ thư mục backup này vào Gemini Canvas, lỗi `ReferenceError` chắc chắn xảy ra 100%.
2. **Vòng lặp đệ quy qua lại giữa `aiCandidates` và `getConfig`**:
   - Tại dòng 1337 trong `canvas_xaydungphuluc.html`:
     `const rows = sourcePpctRows.length ? sourcePpctRows : defaultPpctRows(getConfig());`
     gọi `getConfig()` mà không truyền `{includeAiSelection: false}`.
   - `getConfig()` mặc định gọi `selectedAiLessons()` -> `selectedAiPeriods()` -> `aiPeriodCandidates()` -> `aiCandidates()`. Khi `sourcePpctRows` còn rỗng lúc khởi tạo trang, chuỗi gọi hàm này kích hoạt đệ quy vô hạn hoặc gây lỗi tham chiếu biến.
   - Tương tự, trong `loadDefaultPpctStructure(silent=false)` (dòng 1459):
     `const c = getConfig();` gọi đệ quy khi cấu trúc PPCT chưa được nạp.
3. **Thiếu cơ chế fallback an toàn (Defensive Fallback)**:
   - Các hàm `aiCandidates` và `loadDefaultPpctStructure` chưa kiểm tra an toàn `typeof defaultPpctRows === 'function'` và chưa gán vào `window.defaultPpctRows`, dẫn đến việc nếu hàm bị trì hoãn khởi tạo hoặc chạy trong sandbox thì trang bị crash hoàn toàn.

## Phạm vi tác động
- `canvas_xaydungphuluc.html`:
  1. Thêm gán toàn cục `window.defaultPpctRows = defaultPpctRows;` ngay sau định nghĩa hàm.
  2. Sửa dòng 1337 trong `aiCandidates`: Gọi an toàn `(typeof defaultPpctRows === 'function' ? defaultPpctRows(getConfig({includeAiSelection: false})) : [])`.
  3. Sửa dòng 1459 trong `loadDefaultPpctStructure`: Gọi `getConfig({includeAiSelection: false})` và gán `sourcePpctRows = (typeof defaultPpctRows === 'function') ? defaultPpctRows(c) : []`.
- `backupcode viettailieu/canvas_xaydungphuluc.html`:
  1. Bổ sung định nghĩa `function defaultPpctRows(c)` và catalog `SUBJECT_SAMPLE_TOPICS`.
  2. Áp dụng các biện pháp phòng vệ tương tự để người dùng có thể copy và chạy an toàn ở bất kỳ đâu.

## Ngoài phạm vi
- Không đổi giao diện hoặc logic tính điểm NLS/AI.
- Không sửa các file khác ngoài 2 file trên.

## Các bước thực hiện
1. **Cập nhật `canvas_xaydungphuluc.html`**:
   - Sửa hàm `aiCandidates`: Gọi `getConfig({includeAiSelection: false})` và bọc kiểm tra `typeof defaultPpctRows === 'function'`.
   - Sửa hàm `loadDefaultPpctStructure`: Sử dụng `getConfig({includeAiSelection: false})` và kiểm tra `typeof defaultPpctRows === 'function'`.
   - Gán `window.defaultPpctRows = defaultPpctRows;`.
2. **Cập nhật `backupcode viettailieu/canvas_xaydungphuluc.html`**:
   - Thêm `SUBJECT_SAMPLE_TOPICS` và `function defaultPpctRows(c)`.
   - Sửa các vị trí gọi hàm tương ứng.
3. **Kiểm thử**:
   - Xác nhận không còn tình trạng đệ quy hoặc ReferenceError khi `sourcePpctRows` rỗng.
   - Kiểm tra tương thích cả 2 file.

## Tiêu chí nghiệm thu
- Khởi tạo trang `canvas_xaydungphuluc.html` (kể cả khi `sourcePpctRows = []`) không gây ra bất kỳ lỗi `ReferenceError` nào.
- Dữ liệu PPCT mẫu được nạp mượt mà, sẵn sàng cho việc chọn 12 tiết AI và tích hợp NLS.


