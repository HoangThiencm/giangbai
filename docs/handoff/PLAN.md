# PLAN: Tích Hợp Chọn Model Gemini 3.7 Flash, Tự Động Fallback Về 2.5 Flash Và Hiển Thị Thông Báo Lỗi Rõ Ràng Khi Nhận Diện PPCT Trong xaydungphuluc.html

## Hiện trạng
1. **Khảo sát cách hoạt động AI từ `soankhbd.html` và `js/khbd-gemini.js`**:
   - `soankhbd.html` có bộ chọn `<select id="selectModel">` với các options: `gemini-3.7-flash` (mặc định), `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemini-3-flash-preview`.
   - Model được lưu trữ trong `localStorage.getItem('khbd_gemini_model')` (mặc định: `gemini-3.7-flash`).
   - Cấu hình `thinkingConfig: { thinkingBudget: 0 }` để Gemini 3.7 Flash phản hồi ngay lập tức, không tốn token suy nghĩ cho output JSON/văn bản cấu trúc.
   - **Cơ chế Fallback thông minh (Dynamic Model Fallback)**: Khi model chính (3.7 Flash) gặp lỗi transient (500, 502, 503, 504, "high demand", "unavailable", "try again later"), lỗi timeout mạng hoặc 429 ở key cuối cùng, hệ thống tự động fallback tạm thời sang `gemini-2.5-flash` cho request đó mà không ghi đè cài đặt người dùng.
   - **Cơ chế Proxy Fallback**: Gọi Google API trực tiếp, nếu lỗi kết nối / CORS / firewall thì tự động gọi qua proxy máy chủ `api/khbd_gemini.php`.
   - **Cơ chế Xoay vòng Key (Key Rotation)**: Khi gặp 429/403/hết hạn mức ngày, tự động chuyển sang key kế tiếp và retry có giãn cách (exponential backoff).
   - Có callback trạng thái (`onStatusCallback`, `emitGeminiStatus`) cập nhật thông điệp trực tiếp đến người dùng.

2. **Hiện trạng trong `xaydungphuluc.html`**:
   - Chưa có bộ chọn Model AI trên giao diện; code đang hardcode cứng `gemini-2.5-flash` trong URL API.
   - Chưa có cơ chế chọn `gemini-3.7-flash` làm mặc định và tự động fallback về `gemini-2.5-flash` khi quá tải / lỗi kết nối.
   - Chưa có proxy fallback `api/khbd_gemini.php` khi Google API trực tiếp bị chặn hoặc chập chờn mạng.
   - **Nguyên nhân gây ra hiện tượng "nhận diện không được thì im luôn không hiển thị thông báo gì cả"**:
     * Trong hàm `parseFiles(files)`: khi `recognizePpctWithAi(text)` ném ngoại lệ (do chưa có API key, mạng lỗi, Gemini lỗi, hoặc AI không trả về đúng định dạng JSON PPCT), khối `catch(error)` chỉ bắt lỗi và cố chạy bộ bóc tách dự phòng regex `extractPpctRows(text)`.
     * Nếu bộ bóc tách dự phòng cũng trả về 0 dòng (như với file PDF scan, file rỗng, layout phức tạp), mảng `ppctRows` vẫn rỗng (`[]`).
     * Không có lệnh `notify(...)` cảnh báo nổi bật (Toast), không ghi log vào `#log` ở giai đoạn nhận diện file.
     * Cuối hàm `parseFiles`, hệ thống vẫn gọi `setProgress(100, 'Đã nhận diện hoàn tất bảng PPCT!')` tạo cảm giác thành công giả mạo dù không có dữ liệu nào được trích xuất.
     * Mục 3 (Bảng chọn tiết AI) và Mục 7 (Xem trước) hoàn toàn trống rỗng trong sự im lặng của hệ thống.

---

## Phạm vi
1. **Giao diện người dùng (UI)**:
   - Thêm dropdown `<select id="selectModel">` trên header/thanh công cụ của `xaydungphuluc.html` với đầy đủ các dòng model Gemini (mặc định: `gemini-3.7-flash`, `gemini-2.5-flash`, ...), đồng bộ và lưu trữ lựa chọn vào `localStorage.getItem('khbd_gemini_model')`.
2. **Cơ chế AI Client & Fallback**:
   - Nâng cấp hàm `callGemini(prompt, options)`:
     * Sử dụng model được chọn từ dropdown (mặc định `gemini-3.7-flash`), bổ sung `thinkingConfig: { thinkingBudget: 0 }`.
     * Tự động fallback sang `gemini-2.5-flash` khi model 3.7 gặp lỗi quá tải (503 / 500 / 502 / 504 / high demand / unavailable / try again later / timeout / rate-limit key cuối).
     * Tự động chuyển tiếp sang proxy `api/khbd_gemini.php` nếu direct fetch Google API gặp lỗi mạng / CORS.
     * Giữ nguyên cơ chế xoay vòng key khi gặp 429/403.
3. **Khắc phục triệt để lỗi "im lặng không thông báo"**:
   - Khi người dùng tải file lên nếu chưa có API Key: Hiển thị ngay Toast cảnh báo `notify('Chưa có API Key. Vui lòng bấm Quản lý API Key để nhập key.')` và tự động nhắc mở Modal API Key.
   - Khi file không có văn bản (file PDF scan không có layer text / file rỗng): Thông báo rõ ràng `✗ Tệp không có văn bản hoặc là PDF scan cần OCR`.
   - Khi AI nhận diện gặp lỗi: Ghi log chi tiết vào `#log`, hiển thị Toast cảnh báo `⚠ Lỗi AI (${error.message}). Đang chuyển sang đọc bảng/văn bản trực tiếp từ tệp...`.
   - Khi không trích xuất được dòng PPCT nào (kể cả sau fallback):
     * Không đặt tiến trình 100% "Đã hoàn tất" giả tạo; cập nhật thông báo lỗi rõ ràng.
     * Hiển thị Toast cảnh báo màu đỏ: `✗ Không thể nhận diện được dòng PPCT nào từ tệp. Hãy kiểm tra lại tệp hoặc bấm "Nạp cấu trúc PPCT chuẩn"!`.
     * Cập nhật danh sách tệp `#fileList` với thông báo lỗi đỏ rõ ràng.
4. **Bảo mật & Tương thích**:
   - Giữ nguyên quy tắc bảo mật: Không bao giờ lưu API Key vào `localStorage` hay `sessionStorage`.
   - Cập nhật test `tests/xaydungphuluc-smoke.js` đảm bảo pass 100%.

---

## Ngoài phạm vi
- Không can thiệp vào mã nguồn `soankhbd.html` hoặc `admin.html`.
- Không thay đổi các quy chuẩn sư phạm (CV 5512, TT 38/2021, TT 14/2020, NLS CV 3456, AI QĐ 2422).
- Không thay đổi cấu trúc bảng 8 cột hay logic xuất Word docx đã hoàn thiện.

---

## File dự kiến tác động
- `xaydungphuluc.html` [THÊM CHỌN MODEL GEMINI 3.7 FLASH, FALLBACK 2.5 FLASH, PROXY FALLBACK, TOAST & LOG BÁO LỖI RÕ RÀNG]
- `tests/xaydungphuluc-smoke.js` [CẬP NHẬT TEST KIỂM TRA BỘ CHỌN MODEL, LOGIC FALLBACK VÀ THÔNG BÁO LỖI]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi hoàn thành triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

---

## Các bước thực hiện
1. **Bước 1: Bổ sung UI chọn Model AI vào `xaydungphuluc.html`**:
   - Thêm phần tử `<select id="selectModel" class="field text-sm" onchange="onModelChange(this.value)">` vào header hoặc thanh công cụ cạnh nút Quản lý API Key.
   - Thêm các options:
     * `<option value="gemini-3.7-flash" selected>Gemini 3.7 Flash (Mới nhất & Tối ưu)</option>`
     * `<option value="gemini-3.6-flash">Gemini 3.6 Flash</option>`
     * `<option value="gemini-3.5-flash">Gemini 3.5 Flash</option>`
     * `<option value="gemini-3.5-flash-lite">Gemini 3.5 Flash Lite</option>`
     * `<option value="gemini-2.5-flash">Gemini 2.5 Flash (Nhanh & Ổn định)</option>`
     * `<option value="gemini-2.5-flash-lite">Gemini 2.5 Flash Lite</option>`
     * `<option value="gemini-3-flash-preview">Gemini 3 Flash Preview</option>`
   - Thêm hàm `getSelectedModel()`, `onModelChange(modelId)` lưu model vào `localStorage.setItem('khbd_gemini_model', modelId)`.

2. **Bước 2: Nâng cấp `callGemini` và cơ chế Fallback trong `xaydungphuluc.html`**:
   - Đọc model hiện tại từ `getSelectedModel()` (mặc định `gemini-3.7-flash`).
   - Chuẩn bị payload với `thinkingConfig: { thinkingBudget: 0 }`.
   - Hỗ trợ gọi trực tiếp Google API và fallback proxy `api/khbd_gemini.php`.
   - Xử lý transient error (500, 502, 503, 504, high demand, unavailable, rate-limit key cuối, timeout): tự động chuyển tạm thời sang `gemini-2.5-flash`, ghi log và thông báo trạng thái `Đổi model tạm thời sang Gemini 2.5 Flash (do quá tải/lỗi kết nối)...`.
   - Tiếp tục xoay vòng key khi gặp 429/403.

3. **Bước 3: Nâng cấp `parseFiles` và `recognizePpctWithAi` để thông báo lỗi rõ ràng, không im lặng**:
   - Kiểm tra `apiKeys.length` và `mistralKeys.length` trước khi nhận diện. Nếu không có key:
     * Hiển thị Toast cảnh báo: `notify('Chưa có API Key. Hãy bấm "Quản lý API Key" để nạp key trước khi nhận diện.')`.
     * Ghi thông báo vào `#fileList` và `#log`.
   - Nếu trích xuất văn bản từ tệp ra rỗng:
     * Báo Toast `notify('Tệp không có văn bản hoặc là file PDF scan cần OCR.')`.
     * Ghi rõ vào `#fileList`.
   - Trong khối `catch(error)` của `recognizePpctWithAi`:
     * Ghi log lỗi chi tiết vào `#log`.
     * Bật toast `notify('Lỗi AI nhận diện: ' + error.message + '. Chuyển sang đọc trực tiếp từ tệp.')`.
   - Sau khi hoàn thành bóc tách:
     * Nếu `sourcePpctRows.length === 0`:
       - Đặt tiến trình `setProgress(100, 'Không tìm thấy dòng PPCT hợp lệ.', true, 3000)`.
       - Hiển thị Toast: `notify('Không thể trích xuất dòng PPCT nào từ tệp. Bạn có thể bấm "Nạp cấu trúc PPCT chuẩn"!')`.
       - Ghi chú ý rõ ràng trong `#fileList`.
     * Nếu `sourcePpctRows.length > 0`:
       - Hiển thị Toast thành công và cập nhật số dòng PPCT đã trích xuất.

4. **Bước 4: Cập nhật `tests/xaydungphuluc-smoke.js`**:
   - Bổ sung assertion kiểm tra sự hiện diện của `selectModel`, `gemini-3.7-flash`, `gemini-2.5-flash`, `thinkingConfig`, proxy fallback `api/khbd_gemini.php`, cơ chế fallback model và các thông báo cảnh báo lỗi.
   - Đảm bảo kiểm tra bảo mật key không lưu vào localStorage tiếp tục PASS.

5. **Bước 5: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

---

## Rủi ro & Giải pháp
1. **Rủi ro Gemini 3.7 Flash sinh output suy nghĩ làm chậm**:
   - *Giải pháp*: Luôn gửi `generationConfig: { thinkingConfig: { thinkingBudget: 0 } }` khi gọi 3.7 Flash.
2. **Rủi ro mạng Google API bị gián đoạn**:
   - *Giải pháp*: Tích hợp cơ chế tự động thử qua proxy `api/khbd_gemini.php` giống như trong `js/khbd-gemini.js`.
3. **Rủi ro vi phạm bảo mật key**:
   - *Giải pháp*: Chỉ lưu Model ID (`khbd_gemini_model`) vào LocalStorage; API Key tuyệt đối không lưu LocalStorage/SessionStorage.

---

## Cách kiểm thử
1. **Kiểm tra tĩnh**:
   - Kiểm tra mã nguồn HTML/JS chứa thẻ `selectModel`, model `gemini-3.7-flash` (mặc định), `gemini-2.5-flash`.
   - Kiểm tra `callGemini` có chứa `thinkingBudget: 0`, fallback sang `gemini-2.5-flash`, proxy `api/khbd_gemini.php`.
   - Kiểm tra `parseFiles` có đầy đủ các nhánh thông báo lỗi Toast `notify`, `#log`, cảnh báo khi không có key hoặc khi nhận diện 0 dòng.
2. **Kiểm tra bảo mật**:
   - Đảm bảo không có dòng code nào gọi `localStorage.setItem` cho API Key.

---

## Tiêu chí nghiệm thu
- [x] Có dropdown chọn Model AI trên giao diện `xaydungphuluc.html` với giá trị mặc định là `gemini-3.7-flash`.
- [x] Khi `gemini-3.7-flash` gặp sự cố quá tải/503/high demand/timeout, hệ thống tự động fallback sang `gemini-2.5-flash` và thông báo rõ ràng cho người dùng.
- [x] Tích hợp proxy trung gian `api/khbd_gemini.php` dự phòng khi mạng trực tiếp đến Google bị lỗi.
- [x] Khi nhận diện không thành công (thiếu key, file scan rỗng, lỗi AI, không bóc tách được dòng nào), giao diện hiển thị thông báo Toast cảnh báo tức thì, ghi log chi tiết, không còn tình trạng im lặng.
- [x] Đảm bảo tuyệt đối không lưu API Key vào LocalStorage/SessionStorage.
