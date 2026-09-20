# PLAN: Khắc Phục Triệt Để SyntaxError: Identifier 'DocxGenerator' has already been declared

## Hiện trạng & Phân tích nguyên nhân gốc rễ (Root Cause)

1. **Lỗi `SyntaxError: Identifier 'DocxGenerator' has already been declared` tại runtime:**
   - Trình duyệt báo lỗi chính xác: `DocxGenerator` đã được khai báo trước đó nhưng lại bị khai báo lại trong cùng môi trường Script.

2. **Tại sao chốt kiểm tra trước đó bị lọt?**
   - File `https://hoangthiencm.id.vn/js/khbd-docx.js` trên hosting là file đã qua đóng gói/obfuscate, trong đó khai báo:
     ```javascript
     class DocxGenerator { ... }
     const docxGenerator = new DocxGenerator();
     ```
   - Trong chuẩn JavaScript ES6 (ECMAScript 2015+):
     + Khai báo `class` và `const` ở top-level của một script nằm trong **Script Lexical Scope**, **KHÔNG tự động gán vào thuộc tính của `window`**!
     + Tức là: `typeof DocxGenerator !== "undefined"` và `typeof docxGenerator !== "undefined"` là TRUE, nhưng `typeof window.DocxGenerator` và `typeof window.docxGenerator` lại là `"undefined"`!
   - Trong `canvas_soankhbd.html`:
     + Script primary tải `khbd-docx.js` từ host.
     + Sau khi tải xong, `onload` gọi `ensureKhbdDocxFallback()`.
     + Hàm này kiểm tra:
       `if (typeof window.docxGenerator !== "undefined" || typeof window.DocxGenerator !== "undefined") return;`
     + Vì `window.docxGenerator` là `"undefined"`, điều kiện `if` bị **FAIL (không return)**!
     + Hàm tiếp tục gọi `document.write` nạp file `khbd-docx.js` lần thứ 2 từ CDN jsDelivr!
   - Khi file thứ hai tải về:
     + Dù trong file có `if (typeof window !== "undefined" && window.DocxGenerator)`, điều kiện này vẫn sai (vì không có trên `window`).
     + Quan trọng hơn: Trong JS, khai báo top-level `class DocxGenerator` được parser phân tích trước khi code chạy. Parser thấy `DocxGenerator` đã tồn tại trong Script Lexical Scope từ file thứ nhất $\rightarrow$ Ném ngay lập tức:
       **`SyntaxError: Identifier 'DocxGenerator' has already been declared`**!

---

## Giải pháp Triển khai Toàn diện cho Coder

### 1. Đóng gói IIFE cho `js/khbd-docx.js` (Bảo vệ tuyệt đối khỏi va chạm Lexical Scope)
Bọc toàn bộ nội dung `js/khbd-docx.js` vào IIFE để `class DocxGenerator` nằm trong function scope, không bao giờ bị parser đụng độ với global lexical scope:
```javascript
(function (global) {
  if (typeof global.DocxGenerator !== "undefined" || typeof global.docxGenerator !== "undefined" || (typeof DocxGenerator !== "undefined" && typeof docxGenerator !== "undefined")) {
    return;
  }

  class DocxGenerator {
    // ... toàn bộ nội dung DocxGenerator ...
  }

  const docxGenerator = new DocxGenerator();

  global.DocxGenerator = DocxGenerator;
  global.docxGenerator = docxGenerator;

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { DocxGenerator, docxGenerator };
  }
})(typeof window !== "undefined" ? window : globalThis);
```

### 2. Đóng gói IIFE tương tự cho `js/khbd-prompts.js` và `js/khbd-pedagogy-catalog.js`
- **`js/khbd-prompts.js`**: Bọc toàn bộ vào IIFE `(function (global) { ... })(typeof window !== "undefined" ? window : globalThis);`.
  Kiểm tra đầu file:
  `if (typeof global.getPromptTemplate === "function" && global.PROMPTS && global.PROMPTS.GENERATE_OBJECTIVES) return;`
  Các biến `const LATEX_SPACING_BAN`, `const ACTIVITY_TABLE_CONTRACT` nằm trong IIFE sẽ không bao giờ bị lỗi `already been declared` dù file có nạp lại.
  Xuất ra `global.PROMPTS = PROMPTS;`, `global.getPromptTemplate = getPromptTemplate;`...
- **`js/khbd-pedagogy-catalog.js`**: Bọc toàn bộ vào IIFE `(function (global) { ... })(typeof window !== "undefined" ? window : globalThis);`.
  Kiểm tra đầu file:
  `if (typeof global.KHBD_PEDAGOGY_CATALOG !== "undefined") return;`
  Xuất ra `global.KHBD_PEDAGOGY_CATALOG = KHBD_PEDAGOGY_CATALOG;`.

### 3. Sửa Guard trong `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`
Trong cả 2 file HTML, sửa guard trong các hàm fallback để kiểm tra cả phạm vi biến tự do (lexical) lẫn `window`:
- `ensureKhbdPromptsFallback`:
  ```javascript
  window.ensureKhbdPromptsFallback = function ensureKhbdPromptsFallback() {
    if ((typeof window.getPromptTemplate === "function" && window.PROMPTS) || (typeof getPromptTemplate === "function")) return;
    document.write('<script src="' + (isLocal ? "js/khbd-prompts.js" : cdnPrompts) + '" crossorigin="anonymous"><\/script>');
  };
  ```
- `ensureKhbdDocxFallback`:
  ```javascript
  window.ensureKhbdDocxFallback = function ensureKhbdDocxFallback() {
    if (typeof docxGenerator !== "undefined" || typeof DocxGenerator !== "undefined" || typeof window.docxGenerator !== "undefined" || typeof window.DocxGenerator !== "undefined") return;
    document.write('<script src="' + (isLocal ? "js/khbd-docx.js" : cdnDocx) + '" crossorigin="anonymous"><\/script>');
  };
  ```
- `ensureKhbdPedagogyCatalogFallback`:
  ```javascript
  window.ensureKhbdPedagogyCatalogFallback = function ensureKhbdPedagogyCatalogFallback() {
    if (typeof KHBD_PEDAGOGY_CATALOG !== "undefined" || typeof window.KHBD_PEDAGOGY_CATALOG !== "undefined") return;
    document.write('<script src="' + (isLocal ? "js/khbd-pedagogy-catalog.js" : cdnCatalog) + '" crossorigin="anonymous"><\/script>');
  };
  ```

### 4. Cập nhật và chạy Smoke Tests
- Cập nhật `tests/canvas-soankhbd-smoke.js` kiểm tra IIFE wrapper và guard mới.
- Chạy toàn bộ test suite đảm bảo 100% PASS:
  `node tests/canvas-soankhbd-smoke.js`
  `node tests/canvas-prompts-integrity-smoke.js`
  `node tests/khbd-table-columns-smoke.js`
  `node tests/khbd-pedagogy-rate-smoke.js`
  `node tests/khbd-nls-ai-bold-italic-smoke.js`

---

## File dự kiến tác động
1. `js/khbd-docx.js`
2. `js/khbd-prompts.js`
3. `js/khbd-pedagogy-catalog.js`
4. `canvas_soankhbd.html`
5. `backupcode viettailieu/canvas_soankhbd.html`
6. `tests/canvas-soankhbd-smoke.js`
