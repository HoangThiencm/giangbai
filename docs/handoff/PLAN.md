# PLAN

## Hiện trạng

1. **Cơ chế nạp Model AI vẽ hình chưa theo đúng Cài đặt người dùng**:
   - Trên Trang chủ (`index.html` và `js/user-ai-settings.js`), người dùng được phép tùy chọn độc lập 2 module:
     - **Module Gemini mặc định (Primary Model)**: lưu vào `khbd_gemini_model` và `default_gemini_module` (ví dụ: `gemini-3.7-flash` hoặc bất kỳ model nào người dùng chỉ định).
     - **Module Gemini dự phòng (Fallback Model)**: lưu vào `khbd_gemini_fallback_model` và `default_gemini_fallback` (ví dụ: `gemini-2.5-flash`, `gemini-3.6-flash`...).
   - Tuy nhiên trong `vehinh.html` và `app.js`:
     - Mã nguồn đang gán cứng catalog hoặc fallback cố định (`gemini-3.6-flash`), không đọc động đúng module ưu tiên và module fallback mà người dùng đã thiết lập trong Cài đặt chung.
     - Tại `api/vehinh_ai.php`, danh sách model dự phòng `$fallbackList` đang gán cứng mảng tĩnh `['gemini-3.6-flash', 'gemini-3.7-flash', ...]`, hoàn toàn bỏ qua cấu hình fallback do người dùng lựa chọn.

2. **Lỗi thực thi mã vẽ Fabric.js: `"" is not a function`**:
   - Trong `app.js` dòng 592, `systemPrompt` hướng dẫn AI: `(có thể thêm khối markdown \`\`\`javascript)`. Do đó, mô hình AI trả về khối mã lồng trong thẻ xml và khối markdown: `<javascript>```javascript ... ```</javascript>`.
   - Hàm `extractDrawingJavascript()` lấy nội dung trong thẻ `<javascript>` nhưng không lọc bỏ các dấu backtick ````javascript```.
   - Khi chuyển chuỗi vào `new Function(..., codeText)`, engine JavaScript hiểu ````javascript` là một tagged template literal gọi trên chuỗi rỗng `""(...)`. Vì `String` không phải là hàm (`callable`), JavaScript ném ngoại lệ: `TypeError: "" is not a function`, làm quá trình vẽ hình bị ngắt quãng hoàn toàn.
   - Hàm `new Function` trong `app.js` hiện thiếu các helper vẽ cơ bản (`addPoint`, `addText`), dẫn đến nguy cơ lỗi `ReferenceError: addPoint is not defined` nếu AI sinh mã gọi đến chúng.

3. **Yếu tố ảnh hưởng đến độ chính xác tối đa của hình vẽ AI (Thiếu phương pháp tọa độ hóa chuẩn mực)**:
   - Trước đây AI thường "vẽ mò" hoặc ước lượng tọa độ pixel cảm tính, không có hệ quy chiếu toán học dẫn đến:
     - Góc vuông nhưng đo lại thành 88° hay 93°.
     - Chân đường cao $H$ bị lệch khỏi cạnh đáy $BC$.
     - Trung điểm hoặc các đoạn bằng nhau không thực sự bằng nhau về số pixel.
     - Nhãn điểm (labels như A, B, C) bị vẽ đè trực tiếp lên điểm hoặc cạnh.
     - Hình vẽ bị quá to, quá nhỏ hoặc nằm lệch góc canvas do thiếu ma trận chuyển đổi từ tọa độ toán học sang tọa độ màn hình.

4. **Nhu cầu xuất hình vẽ sang GeoGebra (Các bước dựng hình & Lệnh GeoGebra Script)**:
   - `vehinh.html` hiện đã có sẵn khung nhúng GeoGebra Classic (`#geogebra-container` với iframe `https://www.geogebra.org/classic` ở dòng 334-344), nhưng hiện tại chỉ là khung tĩnh.
   - AI chưa được huấn luyện để sinh song song:
     - Khối Fabric.js để vẽ tương tác trực tiếp trên canvas HTML5.
     - Khối các bước dựng hình sư phạm (tiếng Việt chuẩn toán học).
     - Khối mã lệnh GeoGebra Script (GGB commands như `A = (0, 0)`, `Segment(A, B)`, `Polygon(...)`, `PerpendicularLine(...)`) để giáo viên có thể sao chép 1-click hoặc nạp tự động vào GeoGebra.

5. **Bất cập vị trí nút "Vẽ Hình" và "Vẽ lại" (UX layout)**:
   - Cụm nút `#generate-btn` và `#regenerate-btn` đang đặt ở đỉnh sidebar. Sau khi nhập đề bài hoặc tải ảnh ở phía dưới, người dùng buộc phải cuộn ngược lên trên đỉnh để nhấn vẽ, rồi lại phải cuộn xuống dưới cùng để đọc khung phân tích của AI. Thao tác cuộn lên cuộn xuống liên tục gây bất tiện.

---

## Phạm vi

- **Frontend `app.js`**:
  - **Đồng bộ Dynamic Model & Fallback Model**:
    - `getSystemDrawingModel()`: Đọc chính xác model ưu tiên từ `localStorage.getItem('khbd_gemini_model') || localStorage.getItem('default_gemini_module') || 'gemini-3.7-flash'`.
    - `getSystemDrawingFallbackModel()`: Đọc chính xác model dự phòng từ `localStorage.getItem('khbd_gemini_fallback_model') || localStorage.getItem('default_gemini_fallback') || 'gemini-2.5-flash'`.
    - Dropdown `#ai-model-select`: Tùy chọn đầu tiên luôn là `✨ Theo Cài đặt chung (${primaryModel} · dự phòng: ${fallbackModel})`. Tuyệt đối không gán cứng cố định một model nào nếu người dùng chọn model khác.
    - Payload gửi lên `api/vehinh_ai.php`: Gửi đầy đủ cả `model` và `fallback_model`.
  - **Ứng dụng triệt để Phương pháp Tọa độ hóa (Coordinate Geometry) vào System Prompt**:
    - Chuẩn hóa quy trình vẽ: Đặt gốc tọa độ toán học $O(0, 0)$, xác định tọa độ giải tích chính xác của các đỉnh và điểm đặc biệt (chân đường cao, trung điểm, tâm đường tròn, tiếp điểm).
    - Ánh xạ từ tọa độ toán học sang tọa độ màn hình: `screenX = originX + mathX * scale`, `screenY = originY - mathY * scale`.
    - Quy tắc chống đè nhãn (offset nhãn theo vector pháp tuyến hoặc hướng ngoài của đỉnh).
    - Hàm hậu xử lý `autoCenterAndFitDrawing(canvas)` tự động tính bounding box, căn giữa và điều chỉnh zoom để hình vẽ luôn hoàn hảo trên canvas.
  - **Khắc phục lỗi `"" is not a function` & Chuẩn hóa helper**:
    - Sửa `systemPrompt`: Nghiêm cấm sinh markdown backtick trong thẻ `<javascript>`.
    - Nâng cấp `extractDrawingJavascript()`: Tự động strip sạch mọi dấu ````javascript/js ... ```` ở đầu và cuối.
    - Bổ sung đầy đủ helper vào `new Function`: `addPoint`, `addText`, `addRightAngleSymbol`, `addEqualityTick`, `addAngleArc`, `drawBarChart`, `drawPieChart`. Hỗ trợ linh hoạt cả chữ ký `(canvas, ...)` lẫn `(...)`.
  - **Tích hợp xuất hình vẽ GeoGebra**:
    - Hướng dẫn AI trong `systemPrompt` sinh thêm phần 3: Các bước dựng hình sư phạm và mã lệnh GeoGebra Script trong thẻ `<geogebra>...</geogebra>`.
    - Bóc tách nội dung `<geogebra>` và hiển thị ra giao diện.
    - Cung cấp nút **"📋 Sao chép lệnh GeoGebra"** để giáo viên dán 1-click vào thanh Input của GeoGebra.
    - Thêm cơ chế hỗ trợ nạp lệnh tự động vào khung GeoGebra.
- **Frontend `vehinh.html`**:
  - Chuyển cụm nút `#generate-btn` và `#regenerate-btn` xuống ngay sau khu vực nhập đề bài & tải ảnh câu hỏi, phía trên khung phân tích AI.
  - Thêm khối hiển thị "📐 Các bước dựng hình & Lệnh GeoGebra" với nút sao chép nhanh và nút mở khung GeoGebra.
  - Cập nhật script hiển thị model theo đúng Cài đặt chung của người dùng.
- **Backend `api/vehinh_ai.php`**:
  - Nhận `model` và `fallback_model` từ client.
  - Xây dựng danh sách ứng viên `$modelCandidates` linh hoạt:
    1. `$initialModel` (model do người dùng chọn hoặc ưu tiên theo Cài đặt chung).
    2. `$fallbackModel` (model dự phòng do người dùng chọn trong Cài đặt chung).
    3. Các model còn lại trong catalog đóng vai trò lưới an toàn cuối cùng.
  - Tuyệt đối không ép cứng thứ tự model!
- **Kiểm thử tự động `tests/game-quiz-importer-smoke.js`**:
  - Cập nhật test cases kiểm thử dynamic model & fallback resolution, GeoGebra extraction, sanitization, và vị trí các nút giao diện.

---

## Ngoài phạm vi
- Không can thiệp vào các API key hoặc bảng giá token ngoài phạm vi module vẽ hình và cấu hình AI chung.
- Không thay đổi các chức năng khác trên trang chủ ngoài việc đọc đúng các key cấu hình đã có.

---

## File dự kiến tác động
1. `app.js`
2. `vehinh.html`
3. `api/vehinh_ai.php`
4. `tests/game-quiz-importer-smoke.js`

---

## Các bước thực hiện

### Bước 1: Xây dựng cơ chế Dynamic Model & Fallback Model (Không gán cứng)
1. **Trong `app.js`**:
   - Viết các hàm đọc cấu hình động:
     ```javascript
     function getSystemDrawingModel() {
         return localStorage.getItem('khbd_gemini_model')
             || localStorage.getItem('default_gemini_module')
             || 'gemini-3.7-flash';
     }
     function getSystemDrawingFallbackModel() {
         return localStorage.getItem('khbd_gemini_fallback_model')
             || localStorage.getItem('default_gemini_fallback')
             || 'gemini-2.5-flash';
     }
     ```
   - Cập nhật hàm `syncDrawingModelSelect()`:
     - Lấy `systemModel = getSystemDrawingModel()` và `systemFallback = getSystemDrawingFallbackModel()`.
     - Tùy chọn đầu tiên:
       ```javascript
       followOpt.value = FOLLOW_SYSTEM_MODEL;
       followOpt.textContent = `✨ Theo Cài đặt chung (${getDrawingModelLabel(systemModel)} · DP: ${getDrawingModelLabel(systemFallback)})`;
       ```
     - Khi người dùng giữ nguyên chế độ mặc định này, model gửi lên server là `systemModel`, và fallback gửi kèm là `systemFallback`.
     - Nếu người dùng chọn một model cụ thể trong danh sách dropdown, dùng model đó làm primary và vẫn gửi kèm `systemFallback`.
   - Trong `handleGenerateClick`:
     ```javascript
     const selectedModel = resolveDrawingRequestModel(selectedProvider) || getSystemDrawingModel();
     const selectedFallbackModel = getSystemDrawingFallbackModel();
     // Gửi cả model và fallback_model trong body request fetch
     ```
2. **Trong `api/vehinh_ai.php`**:
   - Tiếp nhận tham số:
     ```php
     $requestedModel = trim((string)($data['model'] ?? ''));
     $requestedFallback = trim((string)($data['fallback_model'] ?? ''));
     ```
   - Trong `vehinh_call_gemini`:
     ```php
     $initialModel = vehinh_resolve_model($runtime, $requestedModel);
     $modelCandidates = [$initialModel];
     if ($requestedFallback !== '' && !in_array($requestedFallback, $modelCandidates, true)) {
         $modelCandidates[] = $requestedFallback;
     }
     // Bổ sung các model catalog làm phương án dự phòng cuối cùng
     foreach (vehinh_provider_models()['gemini'] as $fb) {
         if (!in_array($fb, $modelCandidates, true)) {
             $modelCandidates[] = $fb;
         }
     }
     ```

### Bước 2: Chuẩn hóa Phương pháp Tọa độ hóa (Coordinate Geometry) để đạt độ chính xác tối đa
1. **Nâng cấp `systemPrompt` áp dụng phương pháp tọa độ chuẩn mực**:
   - Chỉ định rõ quy trình tính toán tọa độ toán học:
     ```javascript
     const systemPrompt = `Bạn là chuyên gia hình học, thống kê, lập trình Fabric.js và GeoGebra.
     QUY TẮC BẮT BUỘC: PHƯƠNG PHÁP TỌA ĐỘ HÓA TOÁN HỌC (ANALYTIC GEOMETRY) để đảm bảo độ chính xác 100%:
     1. KHÔNG VẼ CẢM TÍNH. Luôn thiết lập hệ tọa độ:
        - Chọn 1 điểm mốc làm gốc (thường là đỉnh góc vuông hoặc đỉnh đáy trái B).
        - Đặt cạnh đáy nằm ngang song song trục hoành.
        - Dùng công thức toán học giải tích để tính tọa độ tất cả các điểm còn lại:
          * Chân đường cao H: nếu đáy BC nằm ngang thì H.x = A.x, H.y = B.y.
          * Trung điểm M của BC: M.x = (B.x + C.x)/2, M.y = (B.y + C.y)/2.
          * Trọng tâm G: G.x = (A.x + B.x + C.x)/3, G.y = (A.y + B.y + C.y)/3.
          * Tâm đường tròn ngoại tiếp / nội tiếp: tính theo công thức tọa độ chuẩn.
     2. Ánh xạ tọa độ sang Canvas:
        - Tâm canvas: (cx, cy) = (${canvasW/2}, ${canvasH/2}).
        - scale chuẩn sao cho hình chiếm khoảng 60-70% kích thước canvas.
        - const toScreen = (mx, my) => ({ x: cx + mx * scale, y: cy - my * scale });
     3. Nhãn điểm (labels): KHÔNG ĐÈ LÊN ĐỈNH HOẶC CẠNH.
        - Đỉnh phía trên: offset y - 20, x giữ nguyên.
        - Đáy bên trái: offset x - 15, y + 15.
        - Đáy bên phải: offset x + 15, y + 15.
     4. Ký hiệu góc vuông và đoạn bằng nhau: Gọi đúng thứ tự điểm để ký hiệu nằm bên trong góc.`;
     ```
2. **Nâng cấp `executeAiCode(fullText)` & Bộ Helper**:
   - Regex trích xuất sạch mã JS, loại bỏ mọi markdown fence ````javascript ... ```` (giải quyết triệt để lỗi `"" is not a function`).
   - Bổ sung trọn bộ hàm trợ giúp vào `new Function`:
     - `addPoint`: hỗ trợ cả `addPoint(canvas, x, y, color)` lẫn `addPoint(x, y, label, color)`.
     - `addText`: hỗ trợ cả `addText(canvas, ...)` lẫn `addText(x, y, content, color)`.
     - `drawLine(p1, p2, options)`: vẽ đoạn thẳng nối 2 điểm.
     - `addRightAngleSymbol`, `addEqualityTick`, `addAngleArc`, `drawBarChart`, `drawPieChart`.
3. **Thêm hàm tự động căn giữa và vừa vặn khung nhìn (`autoCenterAndFitDrawing`)**:
   - Sau khi các đối tượng Fabric.js được thêm vào canvas, hàm sẽ:
     1. Lấy bounding box tập hợp của toàn bộ đối tượng vừa tạo (`canvas.getObjects()`).
     2. Nếu hình vẽ bị lệch tâm hoặc chạm viền canvas, tính toán độ lệch $(\Delta x, \Delta y)$ và dịch chuyển về chính giữa canvas.
     3. Đảm bảo toàn bộ hình vẽ luôn nằm gọn gàng, đẹp mắt ở trung tâm màn hình của người dùng.

### Bước 3: Tích hợp xuất hình vẽ sang GeoGebra (Các bước dựng hình & Lệnh GeoGebra)
1. **Prompt hướng dẫn AI sinh khối GeoGebra**:
   - Bổ sung yêu cầu PHẦN 3 trong `systemPrompt`:
     ```
     PHẦN 3: CÁC BƯỚC DỰNG HÌNH VÀ MÃ LỆNH GEOGEBRA trong thẻ <geogebra>...</geogebra>:
     - Phần mô tả các bước dựng hình sư phạm (Bước 1, Bước 2...).
     - Khối lệnh GeoGebra Script (mỗi dòng một lệnh chuẩn GeoGebra, ví dụ: A=(0,0), B=(6,0), C=(2,4), Polygon(A,B,C), PerpendicularLine(C, Segment(A,B))...).
     ```
2. **Trích xuất và hiển thị GeoGebra trên giao diện**:
   - Viết hàm `extractGeoGebraContent(fullText)`: Bóc tách nội dung trong thẻ `<geogebra>...</geogebra>`.
   - Trong `vehinh.html`: Bổ sung khối "📐 Các bước dựng hình & Lệnh GeoGebra" cạnh khung GeoGebra hoặc ngay dưới khung phân tích của AI:
     - Hiển thị danh sách các bước dựng hình sư phạm.
     - Khối mã lệnh GeoGebra dạng code block (`<pre><code>...</code></pre>`).
     - Nút **"📋 Sao chép lệnh GeoGebra"**: Khi bấm, sao chép toàn bộ khối lệnh vào clipboard và hiển thị toast thông báo cho giáo viên.
     - Nút **"🚀 Mở khung GeoGebra"**: Tự động mở khung nhúng GeoGebra Classic sẵn có trong trang để giáo viên dán lệnh và tương tác.

### Bước 4: Tái cấu trúc layout nút "Vẽ Hình" & "Vẽ lại" trong `vehinh.html`
1. Xóa cụm nút `#generate-btn` và `#regenerate-btn` ở đỉnh sidebar (dòng 360-369).
2. Chuyển cụm nút xuống ngay sau Accordion "Nhập đề bài" & "Tải ảnh lên" (ngay phía trên khung "Phân tích của AI"):
   - Nút "Vẽ Hình (Ctrl+Q)" to rõ, màu indigo nổi bật, hiệu ứng hover/active sinh động.
   - Nút "Vẽ lại" màu xám trung tính, biểu tượng xoay `rotate-cw`.
3. Đảm bảo toàn bộ listener sự kiện và phím tắt `Ctrl+Q` tiếp tục hoạt động mượt mà.

### Bước 5: Kiểm thử tự động & Bàn giao
1. Bổ sung các assertions trong `tests/game-quiz-importer-smoke.js`:
   - Kiểm tra `getSystemDrawingModel()` và `getSystemDrawingFallbackModel()` đọc đúng từ `localStorage`.
   - Kiểm tra server `api/vehinh_ai.php` tiếp nhận và ưu tiên `fallback_model` từ client.
   - Kiểm tra `extractDrawingJavascript` loại bỏ hoàn toàn markdown fences lồng nhau.
   - Kiểm tra `extractGeoGebraContent` bóc tách chính xác các bước dựng hình và lệnh GeoGebra.
   - Kiểm tra cấu trúc DOM của `vehinh.html`: cụm nút vẽ hình đặt đúng vị trí sau phần câu hỏi.
2. Chạy `node tests/game-quiz-importer-smoke.js` và `node tests/run-all-tests.js` bảo đảm 100% test suites PASS.

---

## Rủi ro
- *Rủi ro*: Một số lệnh GeoGebra tiếng Anh/tiếng Việt có thể khác nhau tùy vào cài đặt ngôn ngữ của applet GeoGebra trên máy người dùng.
- *Biện pháp giảm thiểu*: Hướng dẫn AI sinh mã lệnh GeoGebra bằng cú pháp chuẩn quốc tế (tiếng Anh như `Polygon`, `Segment`, `PerpendicularLine`, `Circle`, `Midpoint`, `Intersect`), vì đây là cú pháp mà GeoGebra Classic trên web luôn hiểu 100% bất kể ngôn ngữ giao diện của người dùng.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy `node tests/game-quiz-importer-smoke.js`.
   - Chạy `node tests/run-all-tests.js`.
2. **Kiểm thử thủ công**:
   - **Thử nghiệm Dynamic Model & Fallback**:
     + Vào Cài đặt AI & Key trên Trang chủ, đổi Primary Model thành model A (ví dụ: `gemini-3.7-flash`) và Fallback thành model B (ví dụ: `gemini-2.5-flash`).
     + Mở `vehinh.html`: Dropdown hiển thị đúng `✨ Theo Cài đặt chung (Gemini 3.7 Flash · DP: Gemini 2.5 Flash)`.
     + Đổi sang model khác trên trang chủ: `vehinh.html` tự động cập nhật theo đúng model đã chọn, không bị ép cứng.
   - **Thử nghiệm Phương pháp Tọa độ hóa & Khắc phục lỗi**:
     + Nhập đề bài: "Cho tam giác ABC vuông tại A có AB = 3cm, AC = 4cm. Vẽ đường cao AH và ký hiệu góc vuông."
     + Thấy cụm nút "Vẽ Hình (Ctrl+Q)" nằm ngay bên dưới phần đề bài. Bấm "Vẽ Hình".
     + Hình vẽ được render chính xác tuyệt đối theo phương pháp tọa độ: góc vuông $A$ chuẩn 90°, đường cao $AH$ vuông góc tuyệt đối với $BC$, ký hiệu góc vuông chuẩn xác, nhãn điểm A, B, C, H không bị đè lên cạnh, hình vẽ được căn chính giữa canvas.
     + Không xuất hiện lỗi `"" is not a function`.
   - **Thử nghiệm GeoGebra**:
     + Kiểm tra khung phân tích xuất hiện khối "Các bước dựng hình & Lệnh GeoGebra".
     + Bấm nút "📋 Sao chép lệnh GeoGebra": Lệnh được copy vào clipboard.
     + Mở khung GeoGebra Classic, dán lệnh vào thanh nhập lệnh: Hình vẽ xuất hiện tức thì và chuẩn xác trong GeoGebra.

---

## Tiêu chí nghiệm thu
1. Module vẽ hình AI đọc động và tôn trọng 100% cấu hình Model ưu tiên và Model dự phòng từ Cài đặt chung của người dùng, tuyệt đối không gán cứng cố định.
2. Ứng dụng phương pháp tọa độ hóa giải tích giúp hình vẽ Fabric.js đạt độ chính xác tối đa: các góc, đường cao, trung điểm chuẩn xác 100% theo toán học, nhãn điểm không đè nét vẽ, tự động căn giữa canvas vừa vặn.
3. Khắc phục triệt để lỗi thực thi `"" is not a function`.
4. AI sinh đầy đủ các bước dựng hình và khối lệnh GeoGebra Script; giao diện có nút sao chép 1-click và liên kết thuận tiện với khung GeoGebra.
5. Nút "Vẽ Hình" và "Vẽ lại" nằm ngay sau phần nhận diện câu hỏi, loại bỏ hoàn toàn việc cuộn trang lên xuống.
6. Toàn bộ 66+ test suites trong hệ thống đều PASS 100%.
