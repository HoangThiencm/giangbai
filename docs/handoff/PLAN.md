# PLAN: Khắc phục sự cố Vehinh.html bị treo "Đang tải danh sách model..." và không vẽ được

## 1. Hiện trạng & Phân tích nguyên nhân gốc rễ (Root Cause)

### Hiện trạng
Khi người dùng mở trang `vehinh.html`:
- Mục **Chọn model** bị kẹt cứng ở `<option>Đang tải danh sách model...</option>`.
- Khung tóm tắt cấu hình bị kẹt ở `Đang kiểm tra cấu hình AI...`.
- Người dùng nhấn nút **Vẽ Hình (Ctrl+Q)** nhưng không có bất kỳ phản hồi nào ("ko vẽ được").

### Phân tích Root Cause

1. **Vấn đề vòng đời khởi động (Lifecycle Startup Lockup) trong `app.js`:**
   - Tại dòng 337 của `app.js`:
     ```javascript
     document.addEventListener('DOMContentLoaded', function () {
         // Toàn bộ khởi tạo canvas, DOM elements, syncDrawingModelSelect, loadDrawingAiConfig, addEventListener cho nút Vẽ hình...
     });
     ```
   - Trong `vehinh.html`, thẻ `<script src="app.js?..."></script>` đặt ở cuối `<body>` (dòng 525).
   - Khi trình duyệt tải tài nguyên (đặc biệt khi có cache, duyệt qua iframe/webview, hoặc kết nối mạng nạp chậm các CDN trong `<head>`), đến thời điểm `app.js` được thực thi thì `document.readyState` có thể đã chuyển sang `'interactive'` hoặc `'complete'`.
   - Chuẩn HTML DOM quy định: Nếu sự kiện `DOMContentLoaded` đã xảy ra trước khi hàm `addEventListener('DOMContentLoaded', ...)` được đăng ký, **sự kiện sẽ KHÔNG BAO GIỜ được kích hoạt lại**!
   - Kết quả: Toàn bộ hàm bên trong không bao giờ chạy:
     + `#geometry-canvas` không được khởi tạo.
     + `syncDrawingModelSelect()` không chạy $\rightarrow$ dropdown giữ nguyên option HTML tĩnh: `Đang tải danh sách model...`.
     + `updateDrawingAiSummary()` không chạy $\rightarrow$ giữ nguyên text: `Đang kiểm tra cấu hình AI...`.
     + Nút `#generate-btn` ("Vẽ hình") không được gắn sự kiện `click` $\rightarrow$ bấm vào hoàn toàn vô tác dụng.

2. **Gọi `createPatterns()` ở top-level trước khi Fabric.js sẵn sàng:**
   - Tại dòng 23 của `app.js`:
     ```javascript
     function createPatterns() {
         const patternSize = 10;
         const patternCanvas = new fabric.StaticCanvas(null, { width: patternSize, height: patternSize });
         ...
     }
     createPatterns();
     ```
   - Lệnh này chạy ngay khi file `app.js` được nạp, hoàn toàn không có guard kiểm tra `typeof fabric !== 'undefined'`.
   - Nếu CDN `cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js` gặp sự cố (mạng học đường chặn cdnjs, mạng lag, chế độ offline), `fabric` sẽ là `undefined` $\rightarrow$ Ném ngay lỗi: `Uncaught ReferenceError: fabric is not defined` tại dòng 10.
   - Khi đó script `app.js` lập tức dừng thực thi trước khi đến được dòng 337. `vehinh.html` cũng chưa có CDN dự phòng (fallback) cho `fabric.js`.

3. **HTML tĩnh chứa placeholder rỗng thay vì giá trị mặc định:**
   - Trong `vehinh.html` (dòng 371 & 374):
     `<option value="">Đang tải danh sách model...</option>`
     `Đang kiểm tra cấu hình AI...`
   - Điều này khiến giao diện trông như bị lỗi nếu JS tải trễ. Đáng lẽ cần điền sẵn các model mặc định của hệ thống (`✨ Theo Cài đặt chung...`, `Gemini 3.6 Flash...`).

4. **Chặn 401 không cần thiết ở endpoint GET trong `api/vehinh_ai.php`:**
   - Tại dòng 159 của `api/vehinh_ai.php`, lệnh `vehinh_require_login()` được gọi trước cả khối xử lý request GET:
     ```php
     vehinh_require_login();
     if ($_SERVER['REQUEST_METHOD'] === 'GET') { ... }
     ```
   - Khi người dùng chưa có session PHP (hoặc session cookie bị mất/hết hạn), việc gọi `GET api/vehinh_ai.php` để lấy danh sách model và kiểm tra trạng thái bị chặn đứng với mã lỗi HTTP 401.
   - Endpoint GET chỉ trả về danh sách model công khai của hệ thống và cờ trạng thái, không tiết lộ dữ liệu nhạy cảm, nên không được chặn 401.
   - Đồng thời, ở request POST, nếu client có gửi kèm `api_keys` (người dùng tự nhập key hoặc lấy từ `localStorage`), hệ thống nên cho phép gọi AI mà không ép buộc phải có session trên máy chủ.

5. **Lỗi hồi quy trong test `tests/game-quiz-importer-smoke.js`:**
   - Commit `9be42aa` thêm hàm `isGeoGebraCoordinateRequested` vào `formatGeoGebraExecuteCommand` nhưng trong test `tests/game-quiz-importer-smoke.js` chưa trích xuất hàm này, dẫn đến `ReferenceError: isGeoGebraCoordinateRequested is not defined`.

---

## 2. Giải pháp Triển khai Chi tiết cho Coder

### Bước 1: Tối ưu và bảo vệ vòng đời khởi động trong `app.js`

1. **Bảo vệ `createPatterns()`:**
   - Thêm guard an toàn để không bao giờ ném Exception nếu `fabric` chưa sẵn sàng:
     ```javascript
     function createPatterns() {
         if (typeof fabric === 'undefined' || !fabric.StaticCanvas) return;
         try {
             const patternSize = 10;
             const patternCanvas = new fabric.StaticCanvas(null, { width: patternSize, height: patternSize });
             // ... các mẫu pattern ...
         } catch (e) {
             console.warn('Không thể tạo chart patterns:', e);
         }
     }
     ```
   - Xóa lời gọi top-level `createPatterns();` ở dòng 23, chuyển lời gọi này vào bên trong hàm khởi động `bootVehinhApp()`.

2. **Đóng gói toàn bộ logic khởi tạo trong `bootVehinhApp()` và hỗ trợ khởi động kép:**
   - Bọc toàn bộ nội dung trong `document.addEventListener('DOMContentLoaded', ...)` vào hàm:
     ```javascript
     function bootVehinhApp() {
         if (window.__vehinhAppBooted) return;
         window.__vehinhAppBooted = true;
         createPatterns();
         // ... toàn bộ nội dung khởi tạo canvas, DOM elements, sự kiện ...
     }
     
     if (document.readyState === 'loading') {
         document.addEventListener('DOMContentLoaded', bootVehinhApp, { once: true });
     } else {
         bootVehinhApp();
     }
     ```
   - Đảm bảo dù trang đã `loading`, `interactive` hay `complete`, `bootVehinhApp()` luôn được kích hoạt lập tức mà không bao giờ bị bỏ sót.

3. **Đồng bộ Dropdown Model và Tóm tắt AI ngay lập tức:**
   - Trong `loadDrawingAiConfig()`:
     Đảm bảo `syncDrawingModelSelect()` và `updateDrawingAiSummary()` chạy đồng bộ ngay ở dòng đầu tiên của hàm trước khi gửi request mạng `fetch('api/vehinh_ai.php')`.
     Khi đó, ngay khi script vừa chạy, dropdown lập tức có đầy đủ danh sách model và tóm tắt, tuyệt đối không bao giờ kẹt ở "Đang tải...".

4. **Đảm bảo an toàn cho `formatGeoGebraExecuteCommand`:**
   - Trong `formatGeoGebraExecuteCommand(commandsArray)`:
     Kiểm tra an toàn `typeof isGeoGebraCoordinateRequested === 'function'` để không bị crash nếu chạy trong môi trường sandbox cô lập.

---

### Bước 2: Cập nhật `vehinh.html`

1. **Cung cấp danh sách option mặc định trực tiếp trong HTML:**
   Thay thế các dòng 368–375 trong `vehinh.html`:
   ```html
   <label for="ai-model-select" class="mb-2 mt-3 block text-sm font-semibold text-gray-200">Chọn model</label>
   <select id="ai-model-select"
       class="w-full rounded-lg border border-gray-600 bg-gray-700 px-3 py-2 text-sm font-medium text-white outline-none focus:ring-2 focus:ring-indigo-500"
       onchange="window.__vehinhOnModelChange && window.__vehinhOnModelChange()">
       <option value="__system__">✨ Theo Cài đặt chung (Gemini 3.7 Flash · DP: Gemini 2.5 Flash)</option>
       <option value="gemini-3.6-flash">Gemini 3.6 Flash (khuyên dùng)</option>
       <option value="gemini-3.7-flash">Gemini 3.7 Flash</option>
       <option value="gemini-3-flash-preview">Gemini 3 Flash Preview</option>
       <option value="gemini-2.0-flash">Gemini 2.0 Flash</option>
       <option value="gemini-2.5-pro">Gemini 2.5 Pro</option>
       <option value="gemini-2.5-flash">Gemini 2.5 Flash</option>
       <option value="gemini-2.0-flash-lite">Gemini 2.0 Flash Lite</option>
   </select>
   <div id="ai-model-summary" class="mt-2 rounded border border-gray-700 bg-gray-800 px-3 py-2 text-xs leading-5 text-gray-300">
       <div><strong>Google Gemini</strong>: <code>gemini-3.7-flash</code></div>
       <div>Gemini 3.7 Flash · theo Cài đặt chung · có hỗ trợ ảnh</div>
   </div>
   ```

2. **Thêm CDN Fallback cho `fabric.js`:**
   Tại dòng 19 trong `vehinh.html`:
   ```html
   <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"></script>
   <script>
       if (typeof fabric === 'undefined') {
           document.write('<script src="https://cdn.jsdelivr.net/npm/fabric@5.3.1/dist/fabric.min.js"><\/script>');
       }
   </script>
   ```

---

### Bước 3: Cập nhật `api/vehinh_ai.php`

1. **Cho phép GET request đọc cấu hình model mà không bị chặn 401:**
   - Chuyển `vehinh_require_login()` xuống dưới khối xử lý `$_SERVER['REQUEST_METHOD'] === 'GET'`.
   - Khối GET trả về `ok: true`, danh sách models và cờ trạng thái `configured`.
2. **Nới lỏng đăng nhập cho POST nếu client gửi kèm `api_keys`:**
   - Cập nhật hàm `vehinh_require_login(?array $clientKeys = null)`:
     ```php
     function vehinh_require_login(?array $clientKeys = null): void
     {
         if (!empty($_SESSION['user_id'])) {
             return;
         }
         if (is_array($clientKeys) && !empty($clientKeys)) {
             return; // Cho phép người dùng sử dụng key cá nhân hợp lệ
         }
         respond(['error' => 'Cần đăng nhập hoặc cung cấp Gemini API Key để dùng AI vẽ hình.'], 401);
     }
     ```
   - Khi nhận body POST, trích xuất `$clientKeys = normalize_api_keys($data['api_keys'] ?? ($data['keys'] ?? []));` rồi mới gọi `vehinh_require_login($clientKeys);`.

---

### Bước 4: Sửa `tests/game-quiz-importer-smoke.js` & Viết Test Mới `tests/vehinh-boot-smoke.js`

1. **Trong `tests/game-quiz-importer-smoke.js`:**
   - Thêm `extractNamed(appJs, 'isGeoGebraCoordinateRequested')` vào mảng `extractSrc`.
   - Cập nhật kiểm tra `formatGeoGebraExecuteCommand` để khớp với logic tiền tố `ShowAxes`/`ShowGrid`.

2. **Tạo mới `tests/vehinh-boot-smoke.js`:**
   - Kiểm tra `app.js` có mẫu khởi động an toàn kép (`document.readyState === 'loading' ? addEventListener : bootVehinhApp()`).
   - Kiểm tra `createPatterns` có guard `typeof fabric === 'undefined'`.
   - Kiểm tra `vehinh.html` có các option model mặc định trong HTML tĩnh và có CDN fallback cho `fabric.js`.
   - Kiểm tra `api/vehinh_ai.php` xử lý GET không bị chặn 401 khi chưa có session.
   - Chạy test đảm bảo 100% PASS.

---

## 3. Danh sách File Cần Chỉnh Sửa
1. `app.js` (Sửa guard `createPatterns`, đóng gói `bootVehinhApp`, khởi động kép `readyState`, an toàn cho GeoGebra helper)
2. `vehinh.html` (Thêm model mặc định, thêm fallback CDN `fabric.js`)
3. `api/vehinh_ai.php` (Mở GET không chặn 401, cho phép POST với client API keys)
4. `tests/game-quiz-importer-smoke.js` (Cập nhật `isGeoGebraCoordinateRequested` vào sandbox)
5. `tests/vehinh-boot-smoke.js` (Tạo mới để kiểm thử tự động toàn diện)
