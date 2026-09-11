# PLAN

## Hiện trạng

1. **Vấn đề 1: Canvas Fabric.js thiếu hoàn toàn chấm điểm và nhãn chữ tên điểm**:
   - Khi người dùng chạy chức năng Vẽ hình AI (ví dụ: bài toán tiếp tuyến từ M đến đường tròn (O; R)), canvas Fabric.js vẽ được các đường tròn, tiếp tuyến và đoạn thẳng, nhưng **hoàn toàn không hiển thị bất kỳ chấm điểm hay nhãn chữ tên điểm nào (O, A, B, C, M, H, F...)** (ảnh người dùng cung cấp).
   - Trong khi đó, ở phần kịch bản GeoGebra, AI vẫn sinh ra các lệnh `Point(O)`, `Point(A)`, `Point(B)`... chứng tỏ AI hoàn toàn nhận thức được sự tồn tại của các điểm, nhưng phía Fabric.js lại bị mất toàn bộ tên điểm.
   - **Nguyên nhân kỹ thuật gốc rễ**:
     - **`addPoint()` trong `app.js` không hỗ trợ tham số tên điểm từ AI**: Hàm `addPoint()` cũ chỉ phục vụ người dùng click chuột thủ công, tự động tạo nhãn A, B, C tăng dần (`pointLabelCounter++`), hoàn toàn không nhận tham số tên điểm cụ thể (như `'O'`, `'M'`, `'H'`).
     - **`wrapAddPoint()` không giải nén được tọa độ dạng Object `{x, y}`**: AI tính toán giải tích trả về điểm dạng `const O = toScreen(0, 0)`. Khi AI gọi `addPoint(O, 'O')`, `wrapAddPoint` truyền thẳng `{x, y}` vào vị trí `x`, khiến Fabric.js nhận `left: NaN, top: NaN`.
     - **`wrapAddText()` sai lệch thứ tự tham số**: `addText(canvas, x, y, color, textContent)` đặt nội dung chữ ở vị trí thứ 5, làm AI gọi theo chuẩn `addText(x, y, 'O')` hoặc `addText('O', x, y)` bị lỗi `NaN` hoặc mất chữ.
     - **`systemPrompt` thiếu code mẫu hướng dẫn gọi `addPoint`**: Prompt chỉ có quy tắc vị trí nhưng không có mẫu code `addPoint(pt, 'Tên')`, khiến AI thường bỏ sót gọi hàm vẽ điểm trên Canvas.

2. **Vấn đề 2: Không nạp lệnh được vào khung GeoGebra bên dưới**:
   - Khi người dùng bấm nút **"⚡ Nạp trực tiếp vào GeoGebra"**, khung GeoGebra bên dưới hoàn toàn không tự động vẽ hình.
   - **Nguyên nhân kỹ thuật gốc rễ**:
     - Khung GeoGebra hiện tại trong `vehinh.html` đang nhúng bằng thẻ `<iframe>` từ nguồn ngoại vi:
       `<iframe src="https://www.geogebra.org/classic"></iframe>`
     - Theo chính sách bảo mật **Same-Origin Policy (SOP)** của trình duyệt, JavaScript trên trang hiện tại (`app.js`) **hoàn toàn bị trình duyệt chặn** không được phép truy cập vào thuộc tính hoặc hàm của frame ngoại vi (`iframeWin.ggbApplet` ném lỗi `DOMException: Blocked a frame with origin from accessing a cross-origin frame`).
     - Do đó, câu lệnh `const ggb = iframeWin?.ggbApplet` luôn bị lỗi/trả về `undefined`.
     - Hàm `injectCommandsToGeoGebra()` luôn rơi vào nhánh fallback: chỉ sao chép chuỗi `Execute({...})` vào clipboard và hiện toast yêu cầu người dùng tự bấm phím dán vào GeoGebra, chứ không thể nạp trực tiếp vào GeoGebra được.

---

## Phạm vi

- **Frontend `vehinh.html`**:
  - Tích hợp thư viện Web API chính thức của GeoGebra:
    `<script src="https://www.geogebra.org/apps/deployggb.js"></script>`
  - Thay thế thẻ `<iframe>` cứng bằng thẻ `<div id="geogebra-container"></div>` cho phép `deployggb.js` nhúng applet HTML5 trực tiếp trong cùng ngữ cảnh (same window context), tạo sẵn đối tượng `window.ggbApplet` có đầy đủ quyền gọi `evalCommand()`.

- **Frontend `app.js`**:
  1. **Nạp trực tiếp lệnh vào GeoGebra (`deployggb.js` + `evalCommand`)**:
     - Khởi tạo applet GeoGebra thông qua `GGBApplet`:
       ```javascript
       const params = {
           "appName": "classic",
           "width": 850,
           "height": 600,
           "showToolBar": true,
           "showAlgebraInput": true,
           "showMenuBar": true,
           "appletOnLoad": function(api) { window.ggbApplet = api; }
       };
       ```
     - Cài đặt hàm `injectCommandsToGeoGebra()`:
       + Mở khung GeoGebra `#geogebra-container`.
       + Gọi trực tiếp `window.ggbApplet.reset()` và `parts.commandsArray.forEach(cmd => window.ggbApplet.evalCommand(cmd))`.
       + Toàn bộ đường tròn, tiếp tuyến, giao điểm, tên điểm lập tức xuất hiện trực tiếp trong GeoGebra mà người dùng không cần sao chép/dán thủ công!
       + Vẫn giữ nút "Sao chép lệnh" dạng `Execute({...})` 1 dòng làm phương án dự phòng khi giáo viên muốn dán vào phần mềm GeoGebra cài ngoài máy tính.
  2. **Nâng cấp `wrapAddPoint` & `addPoint` thông minh cho Fabric.js**:
     - Hỗ trợ toàn bộ các kiểu gọi của AI:
       + `addPoint(pt, 'Tên', color)`
       + `addPoint(x, y, 'Tên', color)`
       + `addPoint('Tên', pt)` / `addPoint('Tên', x, y)`
       + `addPoint(canvas, ...)`
     - Vẽ 1 chấm tròn `fabric.Circle` (radius 3.5px, màu đậm, `originX: 'center', originY: 'center'`, `source: 'ai_primitive'`).
     - Vẽ 1 nhãn chữ `fabric.IText` (font Inter, size 16px, in đậm `bold`, offset tự động `x + 8, y - 18`, `source: 'ai_primitive'`).
  3. **Nâng cấp `wrapAddText` thông minh**:
     - Tự động bóc tách đúng vị trí và nội dung: `addText(x, y, text)`, `addText(text, x, y)`, `addText(pt, text)`.
  4. **Cập nhật `systemPrompt`**:
     - Thêm quy tắc và code mẫu bắt buộc cho việc đặt tên điểm:
       ```javascript
       QUY TẮC BẮT BUỘC: ĐẶT TÊN VÀ CHẤM ĐIỂM (LABELING):
       - Mọi đỉnh và điểm mốc hình học (O, A, B, C, M, H, F...) BẮT BUỘC PHẢI CÓ TÊN TRÊN HÌNH.
       - Sau khi tính tọa độ và vẽ các đường, BẮT BUỘC gọi addPoint(pt, 'Tên') cho TỪNG ĐIỂM:
         Ví dụ:
           addPoint(O, 'O');
           addPoint(A, 'A');
           addPoint(B, 'B');
           addPoint(M, 'M');
       ```
  5. **Cơ chế bảo hiểm tự động (Auto-Recovery Heuristic) trong `executeAiCode`**:
     - Nếu canvas đã vẽ các đường nét nhưng số lượng nhãn tên điểm bằng 0, tự động trích xuất các biến điểm viết hoa `const ([A-Z][0-9]?)` trong mã để tự động bù chấm điểm và nhãn tên.

- **Kiểm thử tự động `tests/game-quiz-importer-smoke.js`**:
  - Kiểm tra `wrapAddPoint` nhận diện đúng các dạng tham số `(pt, 'O')`, `(x, y, 'A')`, tạo đủ chấm tròn và nhãn chữ hợp lệ (không chứa `NaN`).
  - Kiểm tra sự hiện diện của `deployggb.js` trong `vehinh.html` và hàm nạp lệnh `evalCommand`.

---

## Ngoài phạm vi
- Backend `api/vehinh_ai.php` (đã hoàn thiện, không cần sửa).
- Không tự ý sửa source code trong vai trò Antigravity (ChatGPT sẽ implement).

---

## File dự kiến tác động
1. `vehinh.html`
2. `app.js`
3. `tests/game-quiz-importer-smoke.js`

---

## Các bước thực hiện chi tiết

### Bước 1: Nhúng `deployggb.js` trong `vehinh.html`

1. Thêm thẻ script nhúng GeoGebra API trong `<head>`:
   ```html
   <script src="https://www.geogebra.org/apps/deployggb.js"></script>
   ```
2. Thay thế `<iframe>` cứng trong `#geogebra-container`:
   ```html
   <div id="geogebra-container" class="mt-2 w-full h-[600px] border rounded-lg overflow-hidden shadow hidden bg-white">
       <!-- Applet GeoGebra HTML5 được khởi tạo động qua deployggb.js -->
   </div>
   ```

---

### Bước 2: Cài đặt nạp trực tiếp GeoGebra trong `app.js`

1. Quản lý khởi tạo và nạp lệnh GeoGebra:
   ```javascript
   let ggbAppletInstance = null;
   let isGgbAppletReady = false;
   let pendingGgbCommands = null;

   function ensureGeoGebraAppletLoaded(callback) {
       const container = document.getElementById('geogebra-container');
       if (!container) return;
       if (isGgbAppletReady && window.ggbApplet) {
           if (callback) callback();
           return;
       }
       if (typeof GGBApplet === 'function' && !ggbAppletInstance) {
           const params = {
               "appName": "classic",
               "width": container.clientWidth || 850,
               "height": 600,
               "showToolBar": true,
               "showAlgebraInput": true,
               "showMenuBar": true,
               "enableLabelDrags": true,
               "enableShiftDragZoom": true,
               "enableRightClick": true,
               "showResetIcon": true,
               "language": "vi",
               "appletOnLoad": function(api) {
                   window.ggbApplet = api;
                   isGgbAppletReady = true;
                   if (pendingGgbCommands) {
                       runCommandsOnGeoGebra(pendingGgbCommands);
                       pendingGgbCommands = null;
                   }
                   if (callback) callback();
               }
           };
           ggbAppletInstance = new GGBApplet(params, true);
           ggbAppletInstance.inject('geogebra-container');
       }
   }

   function runCommandsOnGeoGebra(commandsArray) {
       if (!window.ggbApplet || typeof window.ggbApplet.evalCommand !== 'function') return false;
       try {
           window.ggbApplet.reset();
           commandsArray.forEach(cmd => {
               if (cmd && cmd.trim()) {
                   window.ggbApplet.evalCommand(cmd.trim());
               }
           });
           showVehinhToast('⚡ Đã nạp thành công hình vẽ vào GeoGebra!');
           return true;
       } catch (err) {
           console.error('Lỗi evalCommand GeoGebra:', err);
           return false;
       }
   }

   function injectCommandsToGeoGebra() {
       const source = lastFullAiText || document.getElementById('geogebra-commands')?.textContent || '';
       const parts = lastGeoGebraParts.commandsArray?.length
           ? lastGeoGebraParts
           : splitGeoGebraBlocks(extractGeoGebraContent(source) || source);
       if (!parts.commandsArray.length) {
           showVehinhToast('Chưa có lệnh GeoGebra để nạp.');
           return;
       }
       openGeoGebraPanel();
       if (window.ggbApplet && isGgbAppletReady) {
           runCommandsOnGeoGebra(parts.commandsArray);
       } else {
           pendingGgbCommands = parts.commandsArray;
           ensureGeoGebraAppletLoaded();
           showVehinhToast('Đang khởi động GeoGebra và chuẩn bị nạp lệnh...');
       }
   }
   ```

---

### Bước 3: Nâng cấp `wrapAddPoint` và `wrapAddText` thông minh trong `app.js`

1. `smartAddPoint`:
   - Bóc tách mọi kiểu tham số `(pt, 'Tên')`, `(x, y, 'Tên')`, `('Tên', pt)`.
   - Tạo chấm tròn `fabric.Circle` (radius 3.5, origin center, `source: 'ai_primitive'`).
   - Tạo nhãn chữ `fabric.IText` (font Inter, size 16 bold, offset `x + 8, y - 18`, `source: 'ai_primitive'`).
   - Thêm trực tiếp vào `canvas`.
2. `smartAddText`:
   - Nhận diện `(x, y, text)`, `(text, x, y)`, `(pt, text)`.
   - Tạo `fabric.IText` không bị lỗi tọa độ `NaN`.

---

### Bước 4: Cập nhật `systemPrompt` và Cơ chế bảo hiểm tự động

1. Thêm chỉ thị bắt buộc trong `systemPrompt`:
   ```javascript
   QUY TẮC BẮT BUỘC: ĐẶT TÊN VÀ CHẤM ĐIỂM (LABELING):
   - Mọi đỉnh và điểm mốc hình học (O, A, B, C, M, H, F...) BẮT BUỘC PHẢI CÓ TÊN HIỂN THỊ TRÊN HÌNH.
   - Sau khi tính tọa độ và dựng các đường, BẮT BUỘC gọi addPoint(pt, 'Tên') cho TỪNG ĐIỂM:
     Ví dụ:
       addPoint(O, 'O');
       addPoint(A, 'A');
       addPoint(B, 'B');
       addPoint(M, 'M');
   - TUYỆT ĐỐI KHÔNG ĐƯỢC BỎ SÓT ĐIỂM NÀO KHÔNG ĐẶT TÊN.
   ```
2. Thêm logic bảo hiểm (Auto-Recovery) trong `executeAiCode()`: Nếu canvas không có bất kỳ nhãn điểm nào, tự động quét các biến điểm viết hoa (`const O = ...`, `const A = ...`) để bù nhãn điểm.

---

### Bước 5: Cập nhật kiểm thử tự động trong `tests/game-quiz-importer-smoke.js`

1. Kiểm tra unit test `smartAddPoint` và `smartAddText`.
2. Kiểm tra `vehinh.html` có thẻ nhúng `deployggb.js` và hàm `runCommandsOnGeoGebra`.
3. Chạy `node tests/run-all-tests.js` đảm bảo 100% test suites PASS.

---

## Rủi ro

- *Rủi ro*: Mạng internet chậm làm `deployggb.js` tải mất vài giây trong lần đầu tiên mở GeoGebra.
- *Biện pháp*: Biến `pendingGgbCommands` sẽ lưu trữ danh sách lệnh và tự động thực thi ngay khi `appletOnLoad` hoàn tất; đồng thời vẫn giữ nút copy lệnh dạng `Execute({...})` 1 dòng làm fallback.

---

## Cách kiểm thử

1. **Kiểm thử tự động**:
   - `node tests/game-quiz-importer-smoke.js`
   - `node tests/run-all-tests.js`
2. **Kiểm thử thủ công**:
   - Mở `vehinh.html`, nhập đề bài tiếp tuyến đường tròn (O; R) và bấm "Vẽ Hình (Ctrl+Q)".
   - Kiểm tra Canvas Fabric.js: tất cả các điểm O, M, A, B, C, D, H, F đều có chấm tròn và nhãn chữ tên điểm đặt cạnh ngay ngắn.
   - Bấm nút **"⚡ Nạp trực tiếp vào GeoGebra"**:
     + Khung GeoGebra mở ra.
     + Toàn bộ hình vẽ (đường tròn, các đoạn thẳng, tiếp tuyến và tên điểm) được vẽ trực tiếp vào GeoGebra một cách mượt mà, **không cần người dùng phải bấm sao chép và dán thủ công**.

---

## Tiêu chí nghiệm thu

1. **100% các điểm hình học trên Canvas Fabric.js đều có chấm điểm và nhãn chữ tên điểm rõ nét**.
2. **Nút "⚡ Nạp trực tiếp vào GeoGebra" vẽ trực tiếp thành công hình học vào GeoGebra applet** mà không bị lỗi Same-Origin Policy.
3. Toàn bộ 66+ test suites trong hệ thống đều PASS 100%.
