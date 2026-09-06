# PLAN: Nhân bản 1-1 xaydungphuluc.html sang canvas_xaydungphuluc.html (Môi trường Canvas nội bộ)

## Hiện trạng & Yêu cầu của người dùng
1. **Yêu cầu bắt buộc từ người dùng**:
   - `canvas_xaydungphuluc.html` bắt buộc lấy **toàn bộ ý tưởng, giao diện và cách chạy từ `xaydungphuluc.html` hoàn toàn 1-1**.
   - **Không được phép tự ý thay đổi, rút gọn hoặc viết lại code**.
   - **Chỉ thay đổi duy nhất ở việc chạy trong môi trường nội bộ Canvas** (không cần API key cá nhân, dùng endpoint `api/canvas_gemini.php` với model `gemini-3-flash-preview`).
2. **Vấn đề phát hiện ở bản thử nghiệm trước**:
   - Bản trước đó đã bị rút gọn/viết lại script riêng (83 dòng) khiến một số logic, bảng và prompt khác với bản chuẩn `xaydungphuluc.html`.
   - Banner kiểm tra ping trang chủ `fetch('https://hoangthiencm.id.vn')` bị trình duyệt chặn CORS (`cors: null`), dẫn đến báo đỏ *"Không kiểm tra được host"*.

---

## Phạm vi thực hiện

### 1. File nguồn và đích
- Tệp nguồn gốc (chuẩn 100%): `xaydungphuluc.html` (khoảng 420 dòng, 150KB).
- Tệp đích: `backupcode viettailieu/canvas_xaydungphuluc.html`.
- Tệp test: `tests/canvas-xaydungphuluc-smoke.js`.

### 2. Các điểm thay đổi DUY NHẤT để chạy môi trường Canvas nội bộ
Mọi cấu trúc HTML, CSS, DOM id, và logic JavaScript từ `xaydungphuluc.html` được giữ nguyên vẹn 1-1, CHỈ sửa đúng các điểm sau:
1. **Thư viện phụ thuộc đầu trang `<head>`**:
   - Đổi đường dẫn tương đối thành URL tuyệt đối từ host:
     `https://hoangthiencm.id.vn/js/khbd-yccd.js`
     `https://hoangthiencm.id.vn/js/khbd-standards.js`
   - Bỏ `js/security-guard.js` và `access-control.js` (không áp dụng chống debug hay chặn phân quyền đăng nhập trong Canvas).
2. **Thêm Banner trạng thái Canvas (`#canvasHostBanner`) ở đầu trang**:
   - Đặt ngay sau `<body>`.
   - Lệnh ping kết nối sử dụng method `OPTIONS` gửi tới endpoint API:
     ```javascript
     fetch('https://hoangthiencm.id.vn/api/canvas_gemini.php', { method: 'OPTIONS', credentials: 'omit' })
       .then(r => {
         if (r.ok || r.status === 204) {
           const b = document.getElementById('canvasHostBanner');
           if (b) { b.textContent = 'Đã kết nối Gemini Canvas · gemini-3-flash-preview'; b.className = 'ok'; }
         }
       })
       .catch(() => {
         const b = document.getElementById('canvasHostBanner');
         if (b) { b.textContent = 'Không kiểm tra được host; vẫn có thể thử tạo phụ lục.'; b.className = 'err'; }
       });
     ```
3. **Thanh Header (Giao diện trạng thái API Key & Model)**:
   - Thay cụm `<select id="selectModel">` và nút `🔑 Đang kiểm tra key…` bằng huy hiệu Canvas cố định:
     `<span class="rounded-full bg-violet-100 px-3 py-2 text-sm font-bold text-violet-800">Gemini Canvas · gemini-3-flash-preview (Hệ thống cấp)</span>`
   - Vẫn giữ nguyên cấu trúc DOM và các nút còn lại (Trang chủ, Lưu CSDL, Tải CSDL, Giao diện, Đặt lại).
4. **Tầng gọi AI nội bộ Canvas (`requestGemini` & `callGemini`)**:
   - Khởi tạo sẵn `apiKeys = ['canvas-session']`, `mistralKeys = []`.
   - Trong `requestGemini`: Thay thế việc gọi trực tiếp Google `https://generativelanguage.googleapis.com/...` bằng lời gọi POST tới endpoint hệ thống:
     ```javascript
     const CANVAS_ENDPOINT = 'https://hoangthiencm.id.vn/api/canvas_gemini.php';
     const response = await fetchWithGeminiTimeout(CANVAS_ENDPOINT, {
       method: 'POST',
       headers: { 'content-type': 'application/json' },
       credentials: 'omit',
       body: JSON.stringify({ payload, timeout: 75 })
     }, GEMINI_TIMEOUT_MS);
     ```
   - Trong `readGeminiResponse`: Giải nén `envelope.body` chứa `{ candidates: [{ content: { parts: [{ text }] } }] }`.
   - Bỏ qua modal chặn "Chưa có API key" trong `generateSelected` và `readStagedSgk`.
5. **Giữ nguyên 100% tất cả các hàm và thuật toán còn lại**:
   - Toàn bộ 7 bước giao diện.
   - Toàn bộ hàm bóc tách PPCT (`extractPpctRows`, `extractDocxTables`, `ingestSourceTables`...).
   - Toàn bộ bộ chọn 12 tiết AI (`aiCandidates`, `aiPeriodCandidates`, `selectedAiPeriods`, `renderAiPicker`...).
   - Toàn bộ prompt chi tiết (`appendixPrompt`, `currentPpctPromptSource`, `curriculumContext`, `lessonCatalog`...).
   - Toàn bộ thuật toán chuẩn hóa Phụ lục 1 (`appendixOneTable`, `normalizeAppendix`, `cleanAppendixOutcome`, tách riêng 02 cột NLS và AI).
   - Toàn bộ xuất Word (`exportDocx` khổ A4 ngang `11906x16838`) và xuất ZIP (`exportAll`).
   - Toàn bộ modal Thẩm định sư phạm (`complianceModal`).

---

## Ngoài phạm vi
- Không sửa source gốc `xaydungphuluc.html`.
- Không sửa `api/canvas_gemini.php`.

---

## File tác động
- `backupcode viettailieu/canvas_xaydungphuluc.html`
- `tests/canvas-xaydungphuluc-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/.lock`

---

## Các bước Coder thực hiện
1. **Bước 1**: Đọc toàn văn `xaydungphuluc.html`.
2. **Bước 2**: Nhân bản sang `backupcode viettailieu/canvas_xaydungphuluc.html` và áp dụng đúng 4 điểm điều chỉnh cho môi trường Canvas:
   - Thay link script head thành URL tuyệt đối host (bỏ `security-guard.js`, `access-control.js`).
   - Thêm banner `#canvasHostBanner` kèm logic ping OPTIONS tới `api/canvas_gemini.php`.
   - Cập nhật header hiển thị huy hiệu Gemini Canvas cố định.
   - Thay thế ruột hàm `requestGemini` trỏ về `api/canvas_gemini.php` với `credentials: 'omit'` và giải nén `envelope.body`; khởi tạo sẵn `apiKeys = ['canvas-session']`.
3. **Bước 3**: Cập nhật `tests/canvas-xaydungphuluc-smoke.js` để kiểm thử toàn diện code 1-1 mới.
4. **Bước 4**: Chạy toàn bộ test đảm bảo PASS.

---

## Cách kiểm thử
1. `node tests/canvas-xaydungphuluc-smoke.js` -> PASS.
2. `node tests/xaydungphuluc-smoke.js` -> PASS.
3. `node tests/xaydungphuluc-integration-smoke.js` -> PASS.
4. Kiểm tra ping OPTIONS tới `api/canvas_gemini.php` trả về 204 có CORS `*`.

---

## Tiêu chí nghiệm thu
- `canvas_xaydungphuluc.html` giống 1-1 hoàn toàn với `xaydungphuluc.html` về mọi tính năng, bảng, prompt, logic xử lý; chỉ thay thế tầng gọi AI sang `api/canvas_gemini.php` (Zero-Config API key).
- Banner kiểm tra host phản hồi màu xanh (OK) không bị lỗi CORS.
- File test chạy PASS.

