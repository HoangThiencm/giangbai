# PLAN

## Hiện trạng

1. **Chọn trực tiếp model (ví dụ `gemini-2.5-flash`) bị âm thầm ghi đè về `gemini-3.7-flash`**:
   - Trong `app.js`, mảng `DEPRECATED_DRAWING_MODELS` đang gán cứng:
     ```javascript
     const DEPRECATED_DRAWING_MODELS = ['gemini-2.5-flash', 'gemini-2.5-flash-lite'];
     ```
   - Tại hàm giải quyết model gửi request:
     ```javascript
     function resolveDrawingRequestModel(provider) {
         const raw = allDOMElements.aiModelSelect?.value || '';
         if (raw && raw !== FOLLOW_SYSTEM_MODEL && !isDeprecatedDrawingModel(raw)) return raw;
         return getCurrentDrawingModel(provider);
     }
     ```
   - Khi người dùng mở menu `#ai-model-select` và chủ động chọn `Gemini 2.5 Flash` nhằm mục đích vẽ nhanh, giá trị `raw` là `'gemini-2.5-flash'`.
   - Vì `isDeprecatedDrawingModel(raw)` trả về `true`, điều kiện `!isDeprecatedDrawingModel(raw)` bị `false`. Hàm bỏ qua lựa chọn của người dùng và gọi `getCurrentDrawingModel(provider)`.
   - `getCurrentDrawingModel(provider)` tự động fallback về `systemModel` (`gemini-3.7-flash`).
   - Do đó, dù người dùng chọn 2.5 Flash, hệ thống vẫn hiển thị trên màn hình:
     `AI đang phân tích bằng Gemini · gemini-3.7-flash · DP: gemini-2.5-flash...`
   - Việc âm thầm ép sang 3.7 Flash đi ngược lại chủ đích của người dùng.

2. **Tiến trình gọi AI vẽ hình "chạy rất lâu" (Độ trễ suy nghĩ của Gemini 3.7 Flash so với 2.5 Flash)**:
   - **Bản chất kiến trúc mô hình**:
     + `gemini-3.7-flash` là dòng mô hình lai tư duy (Hybrid Reasoning Model) thế hệ mới của Google với mạng nơ-ron sâu và cơ chế chuỗi suy nghĩ (Chain-of-Thought). Thời gian tính toán và trễ phản hồi (TTFT) của 3.7 thường mất 10–25 giây.
     + Trong khi đó, dòng thuần Flash như `gemini-2.5-flash` và `gemini-3.6-flash` được tối ưu hóa cho tốc độ cực nhanh (thường chỉ mất 2–4 giây là xong).
     + Khi người dùng chủ động chọn 2.5 Flash để vẽ nhanh, việc hệ thống tự ý ép sang 3.7 Flash đã buộc người dùng phải gánh độ trễ suy nghĩ nặng nề của 3.7 Flash.
   - **Timeout cURL quá dài**: Trong `api/vehinh_ai.php` dòng 32, hàm `vehinh_post_json` đặt `$timeout = 90` giây. Nếu gặp độ trễ mạng hoặc Google xử lý lâu, request sẽ treo chờ tới 1.5 phút.
   - **Vòng lặp vét cạn quá nhiều model và key**:
     - `$modelCandidates` hiện đang nạp toàn bộ danh mục 7 model của catalog (`vehinh_provider_models()['gemini']`).
     - Với mỗi model, backend lại lặp qua toàn bộ danh sách API keys (`$keys`). Nếu người dùng có 3–5 key, số lượng request cURL có thể lên đến 20–35 lượt gọi liên tiếp!
     - Khi model gặp lỗi `400 Bad Request` hoặc không hỗ trợ, backend vẫn tiếp tục thử các key còn lại với cùng model đó, gây lãng phí thời gian vô ích.
   - **Cấu hình token và throttling chưa tối ưu**:
     - `maxOutputTokens` đặt ở mức `16384`, quá lớn so với nhu cầu sinh mã vẽ hình (~800–1500 tokens), khiến Google phân bổ tài nguyên lâu hơn.
     - Hàm `waitForAiThrottle()` ở frontend tự động delay cứng 2–3 giây ngẫu nhiên trước mỗi lần gọi ngay cả khi không có thao tác liên tục.

---

## Phạm vi

- **Frontend `app.js`**:
  - Tôn trọng 100% lựa chọn thủ công của người dùng: Khi người dùng chọn bất kỳ model cụ thể nào trong `#ai-model-select` (khác `FOLLOW_SYSTEM_MODEL`), `resolveDrawingRequestModel` PHẢI trả về chính xác model đó, không được dùng `isDeprecatedDrawingModel` để ghi đè.
  - Loại bỏ việc gán cứng `gemini-2.5-flash` làm deprecated chặn lựa chọn của người dùng. Cho phép người dùng tận dụng tối đa tốc độ tức thì của `gemini-2.5-flash` khi cần vẽ nhanh.
  - Cập nhật dòng trạng thái phân tích (`analysisOutput`): Khi chọn model cụ thể, hiển thị đúng model đó (ví dụ: `AI đang phân tích bằng Gemini · gemini-2.5-flash...`).
  - Tối ưu `waitForAiThrottle()`: Chỉ áp dụng độ trễ khi các lần bấm cách nhau dưới 1 giây, tránh trì hoãn nhân tạo 2–3 giây vô ích.
- **Backend `api/vehinh_ai.php`**:
  - Giảm timeout cURL từ 90s xuống mức thực tế: **25–30 giây**.
  - Giới hạn chuỗi `$modelCandidates` tối đa **2–3 model** (Model người dùng chọn → Model dự phòng người dùng chọn → Tối đa 1 fallback an toàn `gemini-3.6-flash`), tuyệt đối không duyệt toàn bộ 7 model.
  - Cơ chế Fast-fail (Ngắt nhanh): Nếu model trả về mã lỗi `400 Bad Request`, `404 Not Found`, hoặc chứa `"no longer available"` / `"not supported"`, lập tức `break` khỏi vòng lặp key để chuyển ngay sang model dự phòng kế tiếp, không thử lại các key khác với cùng một model lỗi.
  - Tinh chỉnh `maxOutputTokens` xuống mức tối ưu: `8192` (vừa đủ sinh thoải mái mã Fabric + GeoGebra mà phản hồi nhanh hơn nhiều).
- **Kiểm thử tự động `tests/game-quiz-importer-smoke.js`**:
  - Cập nhật assertions để đảm bảo việc chọn trực tiếp model được giữ nguyên, timeout cURL và cơ chế candidate rút gọn hoạt động chính xác.

---

## Ngoài phạm vi
- Không thay đổi các chức năng vẽ hình Fabric.js, GeoGebra, hoặc các công cụ khác ngoài luồng chọn model và gọi API vẽ hình.
- Không can thiệp vào các API key cá nhân của người dùng.

---

## File dự kiến tác động
1. `app.js`
2. `api/vehinh_ai.php`
3. `tests/game-quiz-importer-smoke.js`

---

## Các bước thực hiện

### Bước 1: Khắc phục lỗi chọn trực tiếp model trong `app.js`
1. Sửa hàm `resolveDrawingRequestModel(provider)`:
   ```javascript
   function resolveDrawingRequestModel(provider) {
       const raw = allDOMElements.aiModelSelect?.value || '';
       // Nếu người dùng chủ động chọn một model cụ thể trong menu, tôn trọng 100% lựa chọn đó
       if (raw && raw !== FOLLOW_SYSTEM_MODEL) return raw;
       return getCurrentDrawingModel(provider);
   }
   ```
2. Điều chỉnh `DEPRECATED_DRAWING_MODELS`:
   - Không chặn các model hợp lệ nằm trong catalog (`gemini-2.5-flash` được người dùng cấu hình làm fallback hoặc chọn trực tiếp).
   - Chỉ giữ các mã model thực sự lỗi thời đã bị Google xóa bỏ hoàn toàn (như `gemini-1.5-flash`, `gemini-1.0-pro`).
3. Cập nhật thông báo trạng thái tại `handleGenerateClick`:
   ```javascript
   const selectedModel = resolveDrawingRequestModel(selectedProvider);
   const isCustomSelection = (allDOMElements.aiModelSelect?.value && allDOMElements.aiModelSelect.value !== FOLLOW_SYSTEM_MODEL);
   const fallbackText = isCustomSelection ? '' : (selectedFallbackModel ? ` · DP: ${selectedFallbackModel}` : '');
   allDOMElements.analysisOutput.innerHTML = `AI đang phân tích bằng Gemini · ${selectedModel}${fallbackText}...`;
   ```
4. Tối ưu `waitForAiThrottle`:
   - Giảm ngưỡng kiểm tra: nếu khoảng cách giữa 2 lần bấm nhỏ hơn 1000ms thì chỉ chờ phần còn thiếu; nếu đã quá 1000ms thì thực thi ngay không trì hoãn.

### Bước 2: Tối ưu hóa tốc độ và cơ chế xử lý lỗi trong `api/vehinh_ai.php`
1. Giảm timeout cURL:
   - Đặt `$timeout = 30` giây trong `vehinh_post_json(string $url, array $headers, array $payload, int $timeout = 30)`.
2. Tinh gọn danh sách ứng viên `$modelCandidates`:
   ```php
   $modelCandidates = [$initialModel];
   $requestedFallback = trim((string)$requestedFallback);
   if ($requestedFallback !== '' && !in_array($requestedFallback, $modelCandidates, true)) {
       $modelCandidates[] = $requestedFallback;
   }
   // Chỉ bổ sung tối đa 1 model dự phòng an toàn cuối cùng nếu chưa có
   $safeFallback = 'gemini-3.6-flash';
   if (!in_array($safeFallback, $modelCandidates, true)) {
       $modelCandidates[] = $safeFallback;
   }
   ```
   (Tổng danh sách chỉ từ 2 đến 3 model, không duyệt cả 7 model).
3. Thêm Fast-fail khi lỗi cấp Model:
   ```php
   if (!$response['ok']) {
       $errMsg = (string)($response['error'] ?: ($response['json']['error']['message'] ?? ('Gemini HTTP ' . $response['status'])));
       $lastError = $errMsg;
       $status = (int)$response['status'];
       // Nếu lỗi cấp model (404, 400 Bad Request, model không tồn tại hoặc không khả dụng)
       if ($status === 404 || $status === 400 || stripos($errMsg, 'not found') !== false || stripos($errMsg, 'no longer available') !== false || stripos($errMsg, 'not supported') !== false) {
           break; // Bỏ qua ngay lập tức các key còn lại của model này, chuyển sang model dự phòng kế tiếp
       }
       continue;
   }
   ```
4. Tinh chỉnh `maxOutputTokens`:
   - Đặt `'maxOutputTokens' => 8192` trong `generationConfig`, giúp tăng tốc độ sinh phản hồi từ Google AI.

### Bước 3: Cập nhật kiểm thử tự động
1. Cập nhật `tests/game-quiz-importer-smoke.js`:
   - Kiểm tra khi `aiModelSelect.value = 'gemini-2.5-flash'`, `resolveDrawingRequestModel` trả về đúng `'gemini-2.5-flash'`.
   - Kiểm tra `api/vehinh_ai.php` sử dụng timeout tối ưu 30s và candidate list giới hạn an toàn.
2. Chạy `node tests/game-quiz-importer-smoke.js` và `node tests/run-all-tests.js` đảm bảo 100% test suites PASS.

---

## Rủi ro
- *Rủi ro*: Nếu người dùng chọn một model mà tài khoản Google của họ không có quyền truy cập (hoặc Google trả về 404).
- *Biện pháp giảm thiểu*: Cơ chế Fast-fail sẽ lập tức phát hiện mã 404 trong vòng 1-2 giây và tự động chuyển sang model fallback (`gemini-2.5-flash` hoặc `gemini-3.6-flash`), trả về kết quả nhanh chóng mà không bị treo 90 giây.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - `node tests/game-quiz-importer-smoke.js`
   - `node tests/run-all-tests.js`
2. **Kiểm thử thủ công**:
   - Mở `vehinh.html`.
   - Tại menu "Chọn model", chọn trực tiếp **Gemini 2.5 Flash**.
   - Bấm nút "Vẽ Hình (Ctrl+Q)":
     + Dòng thông báo hiển thị đúng: `AI đang phân tích bằng Gemini · gemini-2.5-flash...` (không bị đổi thành 3.7 flash).
     + Tốc độ phản hồi nhanh tức thì (2–4 giây), không còn bị treo lâu như khi chạy 3.7 Flash.
     + Nếu model 2.5 flash thành công, hình vẽ hiển thị ngay; nếu model gặp lỗi, hệ thống chuyển fallback mượt mà trong vài giây.

---

## Tiêu chí nghiệm thu
1. Khi người dùng chọn trực tiếp bất kỳ model nào trong menu (như Gemini 2.5 Flash), hệ thống tôn trọng 100% lựa chọn đó, gửi đúng model lên API và hiển thị đúng trên giao diện.
2. Khắc phục triệt để tình trạng "chạy rất lâu": người dùng chọn dòng Flash nhẹ sẽ có tốc độ phản hồi nhanh tức thì; timeout giảm còn 30s, danh sách candidate giới hạn 2-3 model, ngắt nhanh (fast-fail) khi model lỗi.
3. Toàn bộ 66+ test suites trong hệ thống đều PASS 100%.
