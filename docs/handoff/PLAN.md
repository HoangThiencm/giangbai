# PLAN: Khai Báo Thủ Công Model Gemini Mới Nhất & Tùy Chọn Model Mặc Định, Model Fallback

## Hiện trạng
1. **Modal "Cài đặt AI & Key" (`js/user-ai-settings.js`)**:
   - Hiện tại modal chỉ có 1 trường chọn model Gemini mặc định (`userAiGeminiModel`) dạng `<select>` cố định với danh sách gồm 8 model hardcode (`gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemini-2.5-pro`, `gemini-3-flash-preview`).
   - Chưa cho phép người dùng tự do nhập thủ công bất kỳ model ID mới nào (custom model name, ví dụ: các phiên bản experimental, thinking preview, hoặc các model mới ra mắt trong tương lai).
   - Hoàn toàn chưa có cấu hình **Model Fallback** (dự phòng): hệ thống đang gán cứng model fallback là `gemini-2.5-flash` ở khắp các file (`js/khbd-gemini.js`, `xaydungphuluc.html`, `nghiencuubaihoc.html`, v.v.), người dùng không thể chủ động chọn model nào sẽ đóng vai trò fallback khi model chính bị lỗi (HTTP 429, 503, timeout hoặc quá tải).
2. **Cơ chế Fallback trong các module xử lý AI**:
   - Trong `js/khbd-gemini.js`: hàm `_fallbackModelId()` trả về chuỗi cố định `"gemini-2.5-flash"`.
   - Trong `xaydungphuluc.html`: biến `GEMINI_FALLBACK_MODEL` đang gán cứng `'gemini-2.5-flash'`.
   - Các công cụ khác (`app.js`, `exam-vision-client.js`, `kttx.html`, `smartquiz.html`, `trochoi.compiled.js`) đều fallback về chuỗi cố định `'gemini-2.5-flash'`.

---

## Phạm vi
1. **Nâng cấp giao diện Modal "Cài đặt AI & Key" (`js/user-ai-settings.js`)**:
   - Bổ sung các model mới nhất vào danh mục gợi ý sẵn (bổ sung `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-2.0-pro-exp-02-05`, `gemini-2.0-flash-thinking-exp-01-21`, `gemini-3.7-flash-thinking` nếu có).
   - Thêm tùy chọn "Tự nhập model khác..." hoặc ô input text cho phép người dùng khai báo thủ công bất kỳ model ID nào theo ý muốn.
   - Tách bạch rõ 02 thiết lập riêng biệt:
     + **Model Gemini mặc định (Primary Model)**: chọn từ danh mục hoặc nhập thủ công. Lưu vào `default_gemini_module` và `khbd_gemini_model`.
     + **Model Gemini dự phòng (Fallback Model)**: chọn từ danh mục hoặc nhập thủ công. Lưu vào `default_gemini_fallback` và `khbd_gemini_fallback_model` (mặc định là `gemini-2.5-flash`).
   - Hiển thị mô tả rõ ràng ngay dưới các trường nhập liệu để người dùng nắm được chức năng của từng model.
2. **Cập nhật cơ chế đọc Model Fallback động**:
   - Trong `js/user-ai-settings.js`:
     + Bổ sung các hàm helper `currentFallbackModel()` và `persistFallbackModel(modelId)`.
     + Cập nhật `fillForm` và `saveSettings` để nạp và lưu đồng bộ cả Model Mặc Định lẫn Model Fallback.
   - Trong `js/khbd-gemini.js`:
     + Sửa hàm `_fallbackModelId()` để đọc giá trị từ `localStorage.getItem('default_gemini_fallback') || localStorage.getItem('khbd_gemini_fallback_model') || 'gemini-2.5-flash'`.
     + Cho phép thêm model thủ công vào `this.availableModels` nếu chưa có, tránh bị chặn ở điều kiện kiểm tra model hợp lệ.
   - Trong `xaydungphuluc.html`:
     + Đổi cơ chế fallback: đọc `getFallbackModel()` từ `localStorage` thay vì hằng số cứng `GEMINI_FALLBACK_MODEL`.
   - Trong `nghiencuubaihoc.html`:
     + Đọc model fallback động từ `localStorage` khi gặp lỗi 429/503.
3. **Cập nhật kiểm thử tự động**:
   - Cập nhật `tests/user-ai-settings-smoke.js` để kiểm tra:
     + Sự hiện diện của cấu hình model mặc định và model fallback.
     + Khả năng nhập thủ công model mới.
     + Lưu trữ đúng các key `default_gemini_module`, `khbd_gemini_model`, `default_gemini_fallback`, `khbd_gemini_fallback_model`.

---

## Ngoài phạm vi
- Không thay đổi backend PHP `api/user_gemini_keys.php` (key lưu trên CSDL, còn cài đặt model cục bộ trên trình duyệt qua localStorage để linh hoạt theo từng thiết bị và phiên làm việc).
- Không can thiệp các module bài giảng / logic nghiệp vụ khác ngoài phần kết nối và xoay vòng model Gemini.

---

## File dự kiến tác động
- `js/user-ai-settings.js`: Cập nhật UI modal, danh sách model gợi ý, ô nhập thủ công, lưu/tải model mặc định & fallback.
- `js/khbd-gemini.js`: Cập nhật `_fallbackModelId()` đọc động từ localStorage và hỗ trợ custom model.
- `xaydungphuluc.html`: Cập nhật logic fallback model động.
- `tests/user-ai-settings-smoke.js`: Bổ sung assertions kiểm tra tính năng mới.
- `docs/handoff/PLAN.md` (kế hoạch này).
- `docs/handoff/.lock` (file khóa).

---

## Các bước thực hiện
1. **Bước 1: Cập nhật danh mục model & hỗ trợ custom model trong `js/user-ai-settings.js`**:
   - Bổ sung các model mới vào `GEMINI_MODELS`.
   - Viết hàm `modelOptionsHtml(selected, customValue)` có tùy chọn `__custom__` ("Tự nhập model khác...").
   - Thêm UI cho 2 khối:
     + Khối 1: "Module Gemini mặc định" gồm select + input text nhập thủ công (hiện ra khi chọn "Tự nhập...").
     + Khối 2: "Module Gemini dự phòng (Fallback khi lỗi/quá tải)" gồm select + input text nhập thủ công.
2. **Bước 2: Xây dựng hàm lưu & nạp model mặc định và fallback**:
   - Thêm `currentFallbackModel()`: đọc `localStorage.getItem('default_gemini_fallback') || localStorage.getItem('khbd_gemini_fallback_model') || 'gemini-2.5-flash'`.
   - Thêm `persistFallbackModel(val)`: lưu vào `default_gemini_fallback` và `khbd_gemini_fallback_model`.
   - Trong `fillForm()`: nạp giá trị vào select và input custom cho cả model mặc định và fallback.
   - Trong `saveSettings()`: đọc giá trị (nếu là `__custom__` thì lấy từ ô input text), lưu vào localStorage cho cả 2 trường.
3. **Bước 3: Cập nhật `js/khbd-gemini.js`**:
   - Sửa `_fallbackModelId()`:
     ```javascript
     _fallbackModelId() {
       return localStorage.getItem('default_gemini_fallback')
         || localStorage.getItem('khbd_gemini_fallback_model')
         || 'gemini-2.5-flash';
     }
     ```
   - Trong `generateContent` hoặc chỗ kiểm tra `this.availableModels`: nếu `fallbackModel` chưa có trong `availableModels`, tự động thêm object `{ id: fallbackModel, name: fallbackModel }` để không bị từ chối chuyển model.
4. **Bước 4: Cập nhật `xaydungphuluc.html`**:
   - Cập nhật hàm `getFallbackModel()`:
     ```javascript
     function getFallbackModel() {
       return localStorage.getItem('default_gemini_fallback')
         || localStorage.getItem('khbd_gemini_fallback_model')
         || 'gemini-2.5-flash';
     }
     ```
   - Trong `callGemini`: dùng `getFallbackModel()` thay cho hằng số cứng `GEMINI_FALLBACK_MODEL`.
5. **Bước 5: Cập nhật và chạy kiểm thử tự động**:
   - Cập nhật `tests/user-ai-settings-smoke.js`.
   - Chạy `node tests/user-ai-settings-smoke.js` và `node tests/xaydungphuluc-smoke.js`.

---

## Rủi ro
- **Giá trị rỗng hoặc không hợp lệ**: Người dùng có thể để trống ô nhập thủ công; cần fallback an toàn về `gemini-3.7-flash` (mặc định) và `gemini-2.5-flash` (fallback) nếu chuỗi rỗng.
- **Model trùng nhau**: Nếu người dùng đặt model mặc định và model fallback trùng nhau, khi gặp lỗi quá tải hệ thống không nên xoay vòng vô tận vào chính model đó. Cần kiểm tra `activeModel !== fallbackModel` trước khi chuyển.

---

## Cách kiểm thử
1. **Kiểm thử tự động bằng Node**:
   - Chạy `node tests/user-ai-settings-smoke.js` -> PASS.
   - Chạy `node tests/khbd-gemini-retry-smoke.js` -> PASS.
   - Chạy `node tests/xaydungphuluc-smoke.js` -> PASS.
2. **Kiểm thử giao diện & localStorage**:
   - Mở modal "Cài đặt AI & Key":
     + Chọn model mặc định từ dropdown -> Lưu -> Kiểm tra `localStorage.getItem('default_gemini_module')`.
     + Chọn "Tự nhập model khác..." -> Nhập `gemini-experimental` -> Lưu -> Kiểm tra localStorage lưu đúng `gemini-experimental`.
     + Chọn model fallback là `gemini-2.5-flash-lite` -> Lưu -> Kiểm tra `localStorage.getItem('default_gemini_fallback')`.
     + Chọn "Tự nhập model khác..." cho fallback -> Nhập `gemini-2.0-flash` -> Lưu -> Kiểm tra localStorage lưu đúng `gemini-2.0-flash`.
3. **Kiểm thử hành vi Fallback**:
   - Giả lập lỗi 503/429 ở model mặc định: kiểm tra hệ thống tự động đổi sang model fallback đã cấu hình trong localStorage và thông báo chính xác tên model fallback.

---

## Tiêu chí nghiệm thu
- Modal "Cài đặt AI & Key" có đầy đủ:
  + Cấu hình Model Gemini mặc định (cho phép chọn hoặc tự nhập tên model thủ công).
  + Cấu hình Model Gemini fallback dự phòng (cho phép chọn hoặc tự nhập tên model thủ công).
- Khi lưu, cả 2 giá trị được ghi nhận chuẩn xác vào `localStorage` (`default_gemini_module`, `khbd_gemini_model`, `default_gemini_fallback`, `khbd_gemini_fallback_model`).
- Khi mở lại modal, các lựa chọn (kể cả model tự nhập thủ công) vẫn được giữ nguyên đầy đủ.
- Các module gọi AI (`khbd-gemini.js`, `xaydungphuluc.html`, v.v.) tự động dùng đúng model fallback được cấu hình khi model chính gặp lỗi hoặc quá tải.
- Tất cả các bộ test tự động liên quan đều PASS.
