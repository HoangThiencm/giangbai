# PLAN: Sửa triệt để lỗi "PROMPTS is not defined" khi 1-Click Generate trên Gemini Canvas

## 1. Hiện trạng & Nguyên nhân gốc rễ (Root Cause Analysis)

Khi người dùng nhấn nút **1-Click Generate** (Soạn bài 1-Click) trên Gemini Canvas, ứng dụng báo lỗi console:
```
[CONSOLE_ERROR] 1-Click Generate Error: Error: PROMPTS is not defined
Stack: ReferenceError: PROMPTS is not defined
    at buildPedagogicalPrompt (https://hoangthiencm.id.vn/js/khbd-app.js?v=20260916-textbook-exact-v15:1:339454)
    at executeStep (blob:...:2335:62)
    at HTMLButtonElement.handle1ClickGenerate (blob:...:2378:17)
```

Qua khảo sát thực tế toàn diện hệ thống:
1. **File trên host `https://hoangthiencm.id.vn/js/khbd-prompts.js` đang rỗng (0 bytes)**:
   - Kiểm tra trực tiếp HTTP response từ host: `https://hoangthiencm.id.vn/js/khbd-prompts.js` trả về HTTP 200 nhưng độ dài nội dung là **0 bytes** (`Len: 0`).
   - Khi Canvas nạp thẻ `<script src="https://hoangthiencm.id.vn/js/khbd-prompts.js?v=..."></script>`, trình duyệt tải về file rỗng nên không có bất kỳ khai báo nào được thực thi.
2. **CI / CD chưa giám sát `js/khbd-prompts.js`**:
   - Trong `tools/check-required-assets.js`, danh sách file bắt buộc không có `js/khbd-prompts.js` và `js/khbd-app.js`. Do đó, khi file bị rỗng trên máy chủ FTP, CI không phát hiện được và vẫn báo deploy thành công.
3. **Khai báo trong `js/khbd-prompts.js` không gán vào `window.PROMPTS`**:
   - Ở cuối file `js/khbd-prompts.js` (dòng 1702–1712), code chỉ gán:
     `window.isEnglishSubject = isEnglishSubject;`
     `window.getSystemRole = getSystemRole;`
     `window.getPromptTemplate = getPromptTemplate;` ...
     nhưng **hoàn toàn bỏ quên** `window.PROMPTS = PROMPTS;` và `globalThis.PROMPTS = PROMPTS;`.
   - Trong môi trường obfuscation, bundling hoặc các thẻ script riêng rẽ, `const PROMPTS` ở phạm vi script không tự động trở thành thuộc tính của `window`.
4. **`buildPedagogicalPrompt` trong `js/khbd-app.js` truy cập biến trần không an toàn**:
   - Tại dòng 5046:
     ```javascript
     function buildPedagogicalPrompt(prompt) {
       let out = `${prompt}\n\n${PROMPTS.OUTPUT_CONTRACT}`;
       if (typeof isEnglishSubject === "function" && isEnglishSubject(appState.selectedSubject) && PROMPTS.ENGLISH_ELT_DIRECTIVE) {
         out += `\n\n${PROMPTS.ENGLISH_ELT_DIRECTIVE}`;
       }
       return out;
     }
     ```
   - Truy cập trực tiếp `PROMPTS.OUTPUT_CONTRACT` mà không qua hàm bọc an toàn hoặc kiểm tra `typeof PROMPTS !== 'undefined'`, gây crash ngay lập tức (`ReferenceError`).
5. **Canvas thiếu stub fallback dự phòng cho `PROMPTS`**:
   - Trong `canvas_soankhbd.html` đã có fallback cho `KHBD_STANDARDS`, `KHBD_YCCD`, `getSystemRole`, nhưng chưa có fallback stub cho `PROMPTS` (chứa `OUTPUT_CONTRACT` và `ENGLISH_ELT_DIRECTIVE`).

---

## 2. Phạm vi can thiệp

1. **Host & CI Integrity**:
   - Bổ sung `js/khbd-prompts.js` và `js/khbd-app.js` vào `tools/check-required-assets.js`.
   - Nâng cache-busting version từ `v15` lên `v16` (`20260916-textbook-exact-v16`) trên tất cả các file để ép trình duyệt và CDN nạp file mới đầy đủ nội dung.
2. **Xuất biến toàn cục trong `js/khbd-prompts.js`**:
   - Thêm `window.PROMPTS = PROMPTS;` và `if (typeof globalThis !== 'undefined') globalThis.PROMPTS = PROMPTS;`.
3. **Phòng thủ đa tầng trong `js/khbd-app.js`**:
   - Tạo hàm `getSafePrompts()` để truy xuất an toàn từ `PROMPTS`, `window.PROMPTS`, hoặc `globalThis.PROMPTS`.
   - Cập nhật `buildPedagogicalPrompt` sử dụng `getSafePrompts()` và fallback chuỗi hợp đồng đầu ra chuẩn CV 5512, không bao giờ để ném ngoại lệ `ReferenceError`.
4. **Dự phòng nhúng trong `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`**:
   - Thêm fallback stub cho `window.PROMPTS` chứa đầy đủ `OUTPUT_CONTRACT` và `ENGLISH_ELT_DIRECTIVE` trước khi nạp `khbd-app.js`.

---

## 3. Ngoài phạm vi

- Không thay đổi cấu trúc luồng 1-Click hay logic xử lý AI.
- Không thay đổi các thuật toán phân tích SGK đa trang đã hoàn thành ở bước trước.

---

## 4. Danh sách file tác động

1. `tools/check-required-assets.js`
2. `js/khbd-prompts.js`
3. `js/khbd-app.js`
4. `canvas_soankhbd.html`
5. `backupcode viettailieu/canvas_soankhbd.html`
6. `tests/canvas-prompts-integrity-smoke.js` (Test mới kiểm tra tính toàn vẹn và fallback của PROMPTS)

---

## 5. Chi tiết các bước triển khai (Dành cho Coder)

### Bước 1: Cập nhật `tools/check-required-assets.js`
Thêm `"js/khbd-prompts.js"` và `"js/khbd-app.js"` vào mảng `required`:
```javascript
const required = [
  "js/khbd-curriculum.js",
  "js/khbd-standards.js",
  "js/khbd-yccd.js",
  "js/khbd-prompts.js",
  "js/khbd-app.js",
  "ai-design-config.js"
];
```

### Bước 2: Xuất toàn cục trong `js/khbd-prompts.js`
1. Cập nhật header version lên `20260916-textbook-exact-v16`.
2. Tại khối `if (typeof window !== 'undefined')` (khoảng dòng 1702):
   ```javascript
   if (typeof window !== 'undefined') {
     window.PROMPTS = PROMPTS;
     window.isEnglishSubject = isEnglishSubject;
     window.getSystemRole = getSystemRole;
     window.getPromptTemplate = getPromptTemplate;
     window.calculateActivityTimeBudgets = calculateActivityTimeBudgets;
     window.extractTextbookSubsections = extractTextbookSubsections;
     window.normalizeTextbookSubsectionProfiles = normalizeTextbookSubsectionProfiles;
     window.extractTextbookLessonMap = extractTextbookLessonMap;
     window.getGeneralCompetenciesForSubject = getGeneralCompetenciesForSubject;
     window.formatGeneralCompetenciesGuide = formatGeneralCompetenciesGuide;
   }
   if (typeof globalThis !== 'undefined') {
     globalThis.PROMPTS = PROMPTS;
   }
   ```

### Bước 3: Phòng thủ trong `js/khbd-app.js`
1. Thêm hàm trợ giúp an toàn trước `buildPedagogicalPrompt`:
   ```javascript
   function getSafePrompts() {
     if (typeof PROMPTS !== 'undefined' && PROMPTS) return PROMPTS;
     if (typeof window !== 'undefined' && window.PROMPTS) return window.PROMPTS;
     if (typeof globalThis !== 'undefined' && globalThis.PROMPTS) return globalThis.PROMPTS;
     return null;
   }
   ```
2. Viết lại `buildPedagogicalPrompt`:
   ```javascript
   function buildPedagogicalPrompt(prompt) {
     const p = getSafePrompts();
     const contract = (p && p.OUTPUT_CONTRACT) || (typeof window !== 'undefined' && window.__KHBD_DEFAULT_OUTPUT_CONTRACT) || '';
     let out = contract ? `${prompt}\n\n${contract}` : prompt;
     const isEng = typeof isEnglishSubject === 'function' ? isEnglishSubject(appState.selectedSubject) : false;
     if (isEng && p && p.ENGLISH_ELT_DIRECTIVE) {
       out += `\n\n${p.ENGLISH_ELT_DIRECTIVE}`;
     }
     return out;
   }
   ```

### Bước 4: Thêm fallback stub trong `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`
1. Nâng phiên bản cache-busting cho script `khbd-prompts.js` và `khbd-app.js` lên `v16`:
   `v=20260916-textbook-exact-v16`.
2. Trong khối script fallback trước `khbd-app.js` (ngay vị trí định nghĩa `window.getSystemRole`):
   ```javascript
   if (typeof window.PROMPTS === "undefined") {
     window.PROMPTS = {
       OUTPUT_CONTRACT: "HỢP ĐỒNG ĐẦU RA BẮT BUỘC:\n- BẮT ĐẦU NGAY LẬP TỨC bằng tiêu đề/mục chuyên môn phù hợp.\n- TUYỆT ĐỐI CẤM: lời chào hỏi, khen ngợi, giới thiệu, nhận xét ngoài lề, lời chúc ở cuối bài.\n- TUYỆT ĐỐI CẤM dùng code block fence (```markdown hoặc ```). Chỉ xuất Markdown thuần túy.\n- CẤM xuất HTML, thẻ span, thuộc tính style hay mã màu.\n- BẮT BUỘC: Các vị trí tích hợp NLS và AI phải được in đậm và in nghiêng (***...***).",
       ENGLISH_ELT_DIRECTIVE: "ENGLISH-MEDIUM ELT LESSON PLAN OVERRIDE (subject = Tiếng Anh / English):\nWrite the ENTIRE lesson plan in natural classroom English (100% English)."
     };
   }
   ```

### Bước 5: Viết bài test kiểm chứng `tests/canvas-prompts-integrity-smoke.js`
- Test 1: Kiểm tra `tools/check-required-assets.js` chạy thành công và quét cả `js/khbd-prompts.js` và `js/khbd-app.js`.
- Test 2: Kiểm tra `js/khbd-prompts.js` có gán `window.PROMPTS` và `globalThis.PROMPTS`.
- Test 3: Kiểm tra `buildPedagogicalPrompt` trong `js/khbd-app.js` hoạt động mượt mà khi `PROMPTS` không tồn tại ở scope trần (dùng fallback / window).
- Test 4: Kiểm tra `canvas_soankhbd.html` và bản backup chứa fallback stub và version `v16`.

---

## 6. Tiêu chí kiểm thử nghiệm thu (Verification Criteria)

1. Chạy bài test mới `node tests/canvas-prompts-integrity-smoke.js` đạt PASS 100%.
2. Chạy toàn bộ các test canvas hiện có: `tests/canvas-soankhbd-smoke.js`, `tests/canvas-gemini-api-smoke.js`, `tests/canvas-textbook-analysis-smoke.js` đạt PASS 100%.
3. Sau khi commit và push, chạy kiểm tra từ xa URL:
   `https://hoangthiencm.id.vn/js/khbd-prompts.js?v=20260916-textbook-exact-v16`
   đảm bảo trả về HTTP 200 và độ dài nội dung > 100,000 bytes (không bao giờ còn 0 bytes).
4. Xác nhận chức năng 1-Click Generate trên Canvas không còn bất kỳ lỗi `ReferenceError: PROMPTS is not defined`.
