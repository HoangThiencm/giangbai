# PLAN

## Hiện trạng

1. **Lỗi thực thi mã vẽ Fabric.js: `Identifier 'canvas' has already been declared`**:
   - Khi người dùng chạy thử chức năng Vẽ hình AI, giao diện báo lỗi màu đỏ:
     `Lỗi thực thi mã vẽ: Identifier 'canvas' has already been declared`
   - **Nguyên nhân kỹ thuật gốc rễ**:
     - Trong `app.js` hàm `executeAiCode(fullText)`, hệ thống biên dịch mã vẽ của AI bằng `new Function`:
       ```javascript
       const drawFunction = new Function('canvas', 'fabric', 'addPoint', 'addText', 'drawLine', 'addRightAngleSymbol', 'addEqualityTick', 'addAngleArc', 'drawBarChart', 'drawPieChart', codeText);
       ```
     - Tham số đầu tiên được đặt tên là `'canvas'`.
     - Các mô hình AI từ kho mã Fabric.js rất quen tay sinh ra dòng code:
       `const canvas = new fabric.Canvas('geometry-canvas');`
       hoặc `let canvas = ...;` hoặc `const canvas = window.canvas;`
     - Trong JavaScript (ES6+), việc khai báo `const canvas` hoặc `let canvas` trong thân hàm khi tham số hàm đã mang tên `canvas` sẽ kích hoạt lỗi cú pháp nghiêm trọng:
       `SyntaxError: Identifier 'canvas' has already been declared`
     - Ngoài ra, nếu mã AI gọi `new fabric.Canvas('geometry-canvas')`, nó sẽ khởi tạo đè instance Fabric mới lên thẻ canvas DOM hiện tại, làm hỏng toàn bộ event listeners, zoom/pan và các đối tượng đang có.

2. **Lỗi GeoGebra: `Giá trị nhập vào không hợp lệ: ent(D, F)Segment(B, F)` (Ảnh người dùng vừa cung cấp)**:
   - Khi người dùng bấm "Sao chép lệnh GeoGebra" và dán vào thanh Input của khung GeoGebra:
     - GeoGebra báo lỗi chấm than: `▲ ent(D, F)Segment(B, F)`
     - Kèm thông báo lỗi: *"Giá trị nhập vào không hợp lệ"*.
   - **Nguyên nhân kỹ thuật gốc rễ**:
     - **Thanh Input của GeoGebra Web chỉ nhận 1 dòng đơn**: Khi người dùng paste khối text nhiều dòng (`\n`) vào ô Input của GeoGebra, trình duyệt gộp/bỏ qua các ký tự xuống dòng khiến các dòng lệnh bị dính liền vào nhau (ví dụ: `Segment(D, F)` và `Segment(B, F)` bị dính thành `ent(D, F)Segment(B, F)`).
     - **AI sinh chú thích `// ...` không hợp lệ trong cú pháp GeoGebra**: Trong phản hồi của AI xuất hiện các dòng có comment:
       `Tangent(M, Circle(O, R)) // This will create two tangents`
       `B = (R * cos(-pi/6), R * sin(-pi/6)) // B is`
       GeoGebra Input Bar không hỗ trợ chú thích cú pháp `//`, khiến bộ phân tích cú pháp của GeoGebra từ chối toàn bộ lệnh.
     - **Thiếu khởi tạo biến số/điểm mốc**: AI dùng ngay `R` hoặc `O` trong `M = (R * sqrt(3), R)` mà chưa khai báo trước `O = (0, 0)` và `R = 3`, làm GeoGebra không hiểu biến số `R`.
     - **Chưa tận dụng cú pháp `Execute({ ... })` hoặc nạp trực tiếp**: GeoGebra có lệnh nội tại cực mạnh `Execute({ "cmd1", "cmd2", ... })` cho phép chạy cả danh sách lệnh trên một dòng duy nhất, hoặc gọi trực tiếp qua JavaScript API `evalCommand()` mà không cần người dùng phải copy/paste thủ công.

3. **Thiếu hiển thị tiến trình thực tế khi gọi AI (Gây cảm giác "treo máy")**:
   - Khi người dùng bấm "Vẽ Hình (Ctrl+Q)", giao diện chỉ hiển thị spinner xoay tròn tĩnh kèm thông báo không đổi suốt 3-15 giây.
   - Thiếu Live Timer (đồng hồ đếm giây thực) và thanh tiến trình đa chặng (Nhận diện đề bài → Lập hệ tọa độ → Lập trình Fabric.js & GeoGebra).

4. **Hình vẽ xuất hiện đồng loạt trong 0.001 giây (Thiếu trực quan sư phạm & Tái hiện từng bước)**:
   - Các đỉnh, cạnh, góc vuông và nhãn xuất hiện cùng một lúc.
   - Thiếu hoạt cảnh vẽ từng nét (Step-by-step animation) và nút "Tái hiện từng bước vẽ" để phục vụ trình chiếu giảng dạy.

---

## Phạm vi

- **Frontend `app.js`**:
  1. **Khử triệt để lỗi cú pháp `Identifier 'canvas' has already been declared`**:
     - Xây dựng hàm tiền xử lý mã `sanitizeAiDrawingCode(codeText)`:
       + Tự động loại bỏ/vô hiệu hóa các khai báo trùng lặp `const canvas = ...`, `let canvas = ...`, `var canvas = ...`.
       + Loại bỏ các lệnh khởi tạo lại `new fabric.Canvas(...)` (nếu có).
       + Loại bỏ các khai báo trùng `fabric` như `const fabric = ...`.
     - Áp dụng `sanitizeAiDrawingCode(codeText)` trong `executeAiCode(fullText)`.
  2. **Khắc phục triệt để lỗi GeoGebra**:
     - Nâng cấp `splitGeoGebraBlocks(raw)`:
       + Lọc sạch hoàn toàn mọi comment chú thích `// ...` và `# ...` ở cuối hoặc đầu dòng lệnh.
       + Loại bỏ các dòng trống hoặc dòng văn bản không phải lệnh.
     - Bổ sung hàm định dạng `formatGeoGebraExecuteCommand(commandsList)`:
       + Chuyển danh sách lệnh thành cú pháp chuẩn GeoGebra: `Execute({"cmd1", "cmd2", ...})`.
       + Khi người dùng bấm "Sao chép lệnh GeoGebra", ưu tiên copy chuỗi `Execute({ ... })` 1 dòng duy nhất để người dùng dán 1 lần ăn ngay vào ô Input của GeoGebra mà không bị dính chữ.
     - Cung cấp nút tiện ích **"⚡ Nạp trực tiếp vào GeoGebra"**:
       + Gọi lệnh tự động qua API GeoGebra `ggbApplet.evalCommand(cmd)` hoặc `Execute({ ... })` để vẽ tức thì vào khung GeoGebra mà không cần thao tác dán thủ công.
  3. **Cập nhật `systemPrompt`**:
     - Khóa cứng quy tắc:
       + Biến `canvas` và `fabric` ĐÃ CÓ SẴN, TUYỆT ĐỐI KHÔNG viết `const canvas = ...` hay gọi `new fabric.Canvas(...)`.
       + Trong thẻ `<geogebra>`: TUYỆT ĐỐI KHÔNG viết chú thích `//` hoặc `#`.
       + Bắt buộc định nghĩa các điểm gốc và bán kính trước khi dùng tọa độ (ví dụ: `O = (0, 0)`, `R = 3`).
  4. **Bộ đếm thời gian & Tiến trình Đa chặng**:
     - `startProgressIndicator(modelName)` và `stopProgressIndicator(successText)` với Live Timer và Progress Bar.
  5. **Hoạt cảnh Vẽ từng nét (Step-by-step Construction Animation)**:
     - `animateDrawingSteps(objects)` và nút `#replay-construction-btn`.
- **Frontend `vehinh.html`**:
  - Bổ sung Widget hiển thị tiến trình thực tế `#ai-progress-widget`.
  - Bổ sung nút **"▶️ Tái hiện từng bước vẽ"** (`#replay-construction-btn`).
  - Nâng cấp panel GeoGebra: Bổ sung nút **"⚡ Nạp trực tiếp vào GeoGebra"** (`#inject-geogebra-btn`) và tùy chọn sao chép lệnh 1 dòng `Execute({ ... })`.
- **Kiểm thử tự động `tests/game-quiz-importer-smoke.js`**:
  - Bổ sung test kiểm tra hàm `sanitizeAiDrawingCode`.
  - Bổ sung test kiểm tra hàm `splitGeoGebraBlocks` lọc sạch comment `//` và sinh chuẩn `Execute({ ... })`.
  - Kiểm tra các phần tử DOM mới trong `vehinh.html`.

---

## Ngoài phạm vi
- Không can thiệp vào các API backend (`api/vehinh_ai.php` đã ổn định).
- Tuyệt đối không tự ý sửa source code trong vai trò Antigravity (ChatGPT sẽ implement).

---

## File dự kiến tác động
1. `app.js`
2. `vehinh.html`
3. `tests/game-quiz-importer-smoke.js`

---

## Các bước thực hiện chi tiết

### Bước 1: Khử triệt để lỗi cú pháp `Identifier 'canvas' has already been declared` trong `app.js`

1. Tạo hàm tiền xử lý `sanitizeAiDrawingCode(code)`:
   ```javascript
   function sanitizeAiDrawingCode(code) {
       let text = String(code || '');
       // Vô hiệu hóa khởi tạo canvas mới (kể cả dạng nhiều dòng)
       text = text.replace(/(?:const|let|var)\s+canvas\s*=\s*new\s+fabric\.Canvas\s*\([\s\S]*?\)\s*;?/gi, '// [canvas already provided]');
       // Vô hiệu hóa mọi khai báo const/let/var canvas còn lại
       text = text.replace(/^\s*(?:const|let|var)\s+canvas\s*(?:=[^;\n]+)?;/gmi, '// [canvas parameter provided]');
       // Thay thế các lệnh new fabric.Canvas gọi độc lập thành tham chiếu canvas có sẵn
       text = text.replace(/new\s+fabric\.Canvas\s*\([\s\S]*?\)/gi, 'canvas');
       // Vô hiệu hóa khai báo const/let/var fabric trùng lặp
       text = text.replace(/^\s*(?:const|let|var)\s+fabric\s*(?:=[^;\n]+)?;/gmi, '// [fabric parameter provided]');
       return text;
   }
   ```
2. Áp dụng vào hàm `executeAiCode(fullText)` trước khi gọi `new Function`.

---

### Bước 2: Khắc phục lỗi GeoGebra `Giá trị nhập vào không hợp lệ` trong `app.js`

1. Nâng cấp `splitGeoGebraBlocks(raw)` để làm sạch từng dòng lệnh:
   ```javascript
   function splitGeoGebraBlocks(raw) {
       const text = String(raw || '').trim();
       const steps = [];
       const commands = [];
       text.split(/\r?\n/).forEach((line) => {
           // Gỡ bỏ tiền tố bullet point và xóa sạch comment // hoặc #
           let trimmed = line.trim().replace(/^[-*•]\s*/, '');
           trimmed = trimmed.replace(/\/\/.*$/, '').replace(/#.*$/, '').trim();
           if (!trimmed) return;
           if (/^[A-Za-z][\w]*\s*=/.test(trimmed) || /^(Segment|Polygon|PerpendicularLine|Circle|Midpoint|Intersect|Line|Angle|Point|Vector|Ray|Arc|Tangent|Translate|Rotate|Dilate|Reflect|Distance|Area|AngleBisector|PerpendicularBisector|Circumcircle|Incircle|Execute)\s*\(/i.test(trimmed)) {
               commands.push(trimmed);
           } else {
               steps.push(line.trim());
           }
       });
       return { steps: steps.join('\n'), commands: commands.join('\n'), commandsArray: commands, raw: text };
   }
   ```
2. Thêm hàm sinh lệnh GeoGebra `Execute({ ... })` 1 dòng:
   ```javascript
   function formatGeoGebraExecuteCommand(commandsArray) {
       if (!commandsArray || !commandsArray.length) return '';
       const escaped = commandsArray.map(cmd => JSON.stringify(cmd));
       return `Execute({${escaped.join(', ')}})`;
   }
   ```
3. Cập nhật hàm sao chép `copyGeoGebraCommands()`:
   - Sao chép lệnh dạng `Execute({"cmd1", "cmd2", ...})` 1 dòng duy nhất.
   - Khi người dùng dán vào ô Input của GeoGebra, chỉ có 1 dòng lệnh duy nhất, GeoGebra tự động thực thi tuần tự tất cả các nét mà không bao giờ bị lỗi dính chữ hoặc lỗi `Giá trị nhập vào không hợp lệ`!
4. Cài đặt nút **"⚡ Nạp trực tiếp vào GeoGebra"**:
   - Nếu có thể truy cập ggbApplet (qua GeoGebra Web API hoặc postMessage):
     ```javascript
     function injectCommandsToGeoGebra() {
         const parts = splitGeoGebraBlocks(extractGeoGebraContent(lastFullAiText));
         if (!parts.commandsArray.length) {
             showVehinhToast('Chưa có lệnh GeoGebra để nạp.');
             return;
         }
         const ggb = window.ggbApplet || (document.querySelector('#geogebra-container iframe')?.contentWindow?.ggbApplet);
         if (ggb && typeof ggb.evalCommand === 'function') {
             parts.commandsArray.forEach(cmd => ggb.evalCommand(cmd));
             showVehinhToast('⚡ Đã vẽ xong hình vào GeoGebra!');
         } else {
             copyGeoGebraCommands();
             openGeoGebraPanel();
             showVehinhToast('Đã mở GeoGebra & copy lệnh Execute. Nhấn Ctrl+V vào ô Input!');
         }
     }
     ```

---

### Bước 3: Cập nhật `systemPrompt` trong `app.js`

Cập nhật phần mô tả trong `systemPrompt`:
```javascript
const systemPrompt = `Bạn là chuyên gia hình học, thống kê, lập trình Fabric.js và GeoGebra. Trả lời NGẮN GỌN: ưu tiên sinh đủ mã vẽ, không viết dài.
QUY TẮC BẮT BUỘC: PHƯƠNG PHÁP TỌA ĐỘ HÓA TOÁN HỌC (ANALYTIC GEOMETRY) để đảm bảo độ chính xác 100%:
1. KHÔNG VẼ CẢM TÍNH. Luôn thiết lập hệ tọa độ.
2. Ánh xạ tọa độ sang Canvas Fabric.js chuẩn xác.
3. Nhãn điểm: Không đè lên đỉnh hoặc cạnh.
4. Ký hiệu góc vuông và đoạn bằng nhau chuẩn.
PHẢN HỒI BẮT BUỘC 3 PHẦN:
PHẦN 1: PHÂN TÍCH trong <analysis>...</analysis> — chỉ 3-5 gạch đầu dòng, súc tích.
PHẦN 2: MÃ JAVASCRIPT trong <javascript>...</javascript>. CẤM markdown backtick. Biến 'canvas' và 'fabric' ĐÃ CÓ SẴN, TUYỆT ĐỐI KHÔNG viết const canvas = ... hoặc new fabric.Canvas(...). Cuối cùng gọi canvas.renderAll();
PHẦN 3: CÁC BƯỚC DỰNG HÌNH VÀ MÃ LỆNH GEOGEBRA trong <geogebra>...</geogebra>:
- Mô tả các bước dựng hình sư phạm (Bước 1, Bước 2...).
- Khối lệnh GeoGebra Script: mỗi dòng một lệnh chuẩn tiếng Anh (O=(0,0), R=3, A=(...), Segment(...)). TUYỆT ĐỐI KHÔNG viết chú thích // hoặc # trong khối lệnh GeoGebra. Mọi biến số và điểm gốc (O, R, A...) phải được định nghĩa trước khi dùng.`;
```

---

### Bước 4: Thiết kế giao diện Tiến trình & Nút Tái hiện & Nạp GeoGebra trong `vehinh.html`

1. Thêm khối hiển thị tiến trình `#ai-progress-widget` tại `#draw-action-buttons`:
   ```html
   <div id="ai-progress-widget" class="hidden rounded-lg border border-indigo-500/50 bg-gray-900/90 p-3 space-y-2">
       <div class="flex items-center justify-between text-xs text-indigo-300">
           <span id="ai-progress-status" class="font-semibold flex items-center gap-1.5">
               <i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i>
               <span>Đang khởi động AI...</span>
           </span>
           <span id="ai-progress-timer" class="font-mono text-emerald-400 font-bold">⏱️ 0.0s</span>
       </div>
       <div class="w-full bg-gray-700 h-1.5 rounded-full overflow-hidden">
           <div id="ai-progress-bar" class="bg-indigo-500 h-full rounded-full transition-all duration-300 w-0"></div>
       </div>
   </div>
   ```
2. Thêm nút **"▶️ Tái hiện từng bước vẽ"** (`#replay-construction-btn`).
3. Nâng cấp panel `#geogebra-construction-panel`:
   - Thêm nút **"⚡ Nạp trực tiếp vào GeoGebra"** (`#inject-geogebra-btn`).
   - Nút **"📋 Sao chép lệnh (Dán 1 lần vào GeoGebra)"** (`#copy-geogebra-btn`).

---

### Bước 5: Cài đặt Hoạt cảnh Vẽ từng nét (Step-by-Step Animation) trong `app.js`

1. Sau khi `drawFunction` vẽ xong và căn giữa, tạm ẩn các đối tượng mới (`opacity: 0`).
2. Dùng vòng lặp `async/await` hiện tuần tự từng nét với hiệu ứng `obj.animate('opacity', 1, ...)`.
3. Cho phép xem lại bất kỳ lúc nào bằng nút `#replay-construction-btn`.

---

### Bước 6: Kiểm thử tự động `tests/game-quiz-importer-smoke.js`

1. Test unit `sanitizeAiDrawingCode`:
   - Loại bỏ `const canvas = new fabric.Canvas(...)`.
   - Đảm bảo `new Function('canvas', 'fabric', sanitizedCode)` không ném lỗi `Identifier 'canvas' has already been declared`.
2. Test unit `splitGeoGebraBlocks` & `formatGeoGebraExecuteCommand`:
   - Đảm bảo lọc sạch comment `// This is comment`.
   - Đảm bảo sinh đúng cú pháp `Execute({"cmd1", "cmd2"})`.
3. Kiểm tra các element DOM mới trong `vehinh.html`.

---

## Rủi ro

- *Rủi ro*: Trình duyệt cũ không hỗ trợ `navigator.clipboard.writeText`.
- *Biện pháp*: Fallback dùng `document.execCommand('copy')` an toàn.
- *Rủi ro*: Học sinh paste nhiều dòng vào GeoGebra Desktop vs GeoGebra Web.
- *Biện pháp*: Định dạng `Execute({ ... })` hoạt động hoàn hảo trên CẢ GeoGebra Desktop, GeoGebra Web và GeoGebra Mobile.

---

## Cách kiểm thử

1. **Kiểm thử tự động**:
   - `node tests/game-quiz-importer-smoke.js`
   - `node tests/run-all-tests.js`
2. **Kiểm thử thủ công**:
   - Nhập prompt: *"Từ điểm M nằm ngoài đường tròn (O; R), kẻ hai tiếp tuyến MA, MB..."*
   - Bấm "Vẽ Hình (Ctrl+Q)":
     + Thấy Live Timer đếm giây thực tế: `⏱️ 0.5s... 1.2s... 2.5s...`.
     + Không còn lỗi `Identifier 'canvas' has already been declared`.
     + Hình vẽ xuất hiện tuần tự từng nét mượt mà trên Canvas.
     + Bấm "Sao chép lệnh GeoGebra", mở GeoGebra dán vào ô Input: Lệnh `Execute({ ... })` được thực thi trọn vẹn, **KHÔNG CÒN lỗi `Giá trị nhập vào không hợp lệ`**.

---

## Tiêu chí nghiệm thu

1. **Khắc phục 100% lỗi `Identifier 'canvas' has already been declared`**.
2. **Khắc phục 100% lỗi GeoGebra `Giá trị nhập vào không hợp lệ`**: lệnh được làm sạch hoàn toàn comment `//` và đóng gói thành `Execute({ ... })` 1 dòng tiện lợi hoặc nạp trực tiếp.
3. **Live Timer & Progress Bar** hiển thị trực quan trong suốt thời gian gọi AI.
4. **Hoạt cảnh vẽ từng nét** diễn ra tuần tự, đẹp mắt và có nút Tái hiện từng bước.
5. Toàn bộ 66+ test suites trong hệ thống đều PASS 100%.
