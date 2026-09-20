# PLAN: Khắc Phục Triệt Để [GLOBAL] Script error Do Tải Trùng Lặp Thư Viện & Race Condition Fallback

## Hiện trạng & Phân tích nguyên nhân gốc rễ (Root Cause)

1. **Lỗi `[GLOBAL] Script error.` xuất hiện khi tải `canvas_soankhbd.html`:**
   - Trong `canvas_soankhbd.html` (và `backupcode viettailieu/canvas_soankhbd.html`), đoạn mã nạp `khbd-prompts.js`, `khbd-docx.js`, `khbd-pedagogy-catalog.js` đang dùng 2 thẻ script liên tiếp:
     ```html
     <script>
       document.write(`<script src="https://hoangthiencm.id.vn/js/khbd-prompts.js?..."><\/script>`);
     </script>
     <script>
       (function ensureKhbdPromptsFallback() {
         if (typeof window.getPromptTemplate === "function" && window.PROMPTS) return;
         var cdnPrompts = "https://cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-prompts.js";
         document.write('<script src="' + cdnPrompts + '"><\/script>');
       })();
     </script>
     ```
   - **Cơ chế gây lỗi (Race Condition)**:
     - Khi gọi `document.write` nạp file từ host `hoangthiencm.id.vn`, trình duyệt bắt đầu gửi yêu cầu tải mạng (bất đồng bộ).
     - Thẻ `<script>` thứ hai chứa hàm `ensureKhbdPromptsFallback()` được trình duyệt thực thi **NGAY LẬP TỨC** khi file từ host chưa kịp tải xong!
     - Tại thời điểm đó, `window.getPromptTemplate` vẫn là `undefined`!
     - Do đó, `ensureKhbdPromptsFallback()` tưởng host bị lỗi và gọi tiếp `document.write` lần 2 để tải file dự phòng từ CDN jsDelivr!
     - Hệ quả: **Cả 2 file cùng tải về và cùng chạy trên window**:
       * File 1 chạy khai báo: `const LATEX_SPACING_BAN = ...;`, `const ACTIVITY_TABLE_CONTRACT = ...;`, `const PROMPTS = ...;`.
       * File 2 chạy sau đè lên phạm vi toàn cục:
         $\rightarrow$ `Uncaught SyntaxError: Identifier 'LATEX_SPACING_BAN' has already been declared`.
       * Hiện tượng tương tự xảy ra ở `khbd-docx.js` (`class DocxGenerator` khai báo lần 2 $\rightarrow$ SyntaxError) và `khbd-pedagogy-catalog.js` (`const KHBD_PEDAGOGY_CATALOG` $\rightarrow$ SyntaxError).
     - Vì file nạp từ CDN jsDelivr khác domain (cross-origin) và không có thuộc tính `crossorigin="anonymous"`, trình duyệt bảo mật che giấu chi tiết lỗi và bắn sự kiện ra `window.onerror` thành:
       **`[GLOBAL] Script error.`**!

---

## Giải pháp Triển khai Toàn diện

### 1. Bảo vệ Idempotent (Chống Tải Lặp) trong các File Thư Viện JS
Thêm chốt bảo vệ ở đầu mỗi file để nếu script có bị gọi 2 lần thì lần thứ 2 tự động return an toàn, không bao giờ ném lỗi SyntaxError:
- **`js/khbd-prompts.js`**:
  Thêm vào đầu file:
  ```javascript
  if (typeof window !== "undefined" && window.__KHBD_PROMPTS_LOADED__) {
    // Đã nạp thành công trước đó, bỏ qua để không khai báo lại const toàn cục
  } else {
    if (typeof window !== "undefined") window.__KHBD_PROMPTS_LOADED__ = true;
    // Toàn bộ mã nguồn khbd-prompts.js
  }
  ```
  (Đồng thời các hằng số dùng `var` hoặc gán vào `window`/`globalThis` để an toàn tuyệt đối).

- **`js/khbd-docx.js`**:
  Thêm chốt ở đầu file:
  ```javascript
  if (typeof window !== "undefined" && (window.docxGenerator || window.DocxGenerator)) {
    // Đã có DocxGenerator, không khai báo lại
  }
  ```

- **`js/khbd-pedagogy-catalog.js`**:
  Thêm chốt ở đầu file:
  ```javascript
  if (typeof window !== "undefined" && window.KHBD_PEDAGOGY_CATALOG) {
    // Đã có KHBD_PEDAGOGY_CATALOG, không khai báo lại
  }
  ```

### 2. Chuẩn hóa Cơ Chế Tải Script trong `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`
- Xóa bỏ việc kiểm tra tức thời bằng `document.write` gây race condition.
- Dùng cơ chế nạp qua `onerror` hoặc nạp tuần tự:
  Khi thẻ `<script>` chính nạp từ host bị lỗi (error event) hoặc sau khi load kiểm tra 0 bytes, mới kích hoạt nạp CDN fallback với `crossorigin="anonymous"`.
  Hoặc tải qua loader có Promise giống `bootstrapCanvasCoreModules()` (đã có sẵn cơ chế `load()` có timeout và fallback chuẩn mực).

### 3. File Kiểm thử `tests/canvas-soankhbd-smoke.js`
- Cập nhật test kiểm tra bảo đảm không có race condition tải kép.
- Chạy toàn bộ test suite.

---

## File dự kiến tác động
1. `js/khbd-prompts.js`
2. `js/khbd-docx.js`
3. `js/khbd-pedagogy-catalog.js`
4. `canvas_soankhbd.html`
5. `backupcode viettailieu/canvas_soankhbd.html`
6. `tests/canvas-soankhbd-smoke.js`
