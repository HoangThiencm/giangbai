# KẾ HOẠCH BÀN GIAO TRIỂN KHAI (HANDOFF PLAN)
## Nhiệm vụ 1: Sửa lỗi Vẽ hình AI không đọc cấu hình, module từ cài đặt (Model gemini-2.5-flash deprecated)
## Nhiệm vụ 2: Tích hợp chức năng đọc câu hỏi từ Word / LaTeX công thức cho các Game giáo dục
## Nhiệm vụ 3: Tích hợp cấu trúc hiển thị 4 Bước chuẩn Bộ GD&ĐT (Công văn 5555) vào Nghiên cứu bài học AI (`nghiencuubaihoc.html`)

---

## 1. Hiện trạng & Yêu cầu từ Người dùng

1. **Nhiệm vụ 1 (Vẽ hình AI)**:
   > *"vẽ hình bằng AI nó không đọc cấu hình, module từ cài đặt mà chạy độc lập thì phải và báo lỗi như ảnh"*
   - Lỗi hiển thị: `Lỗi AI vẽ hình: This model models/gemini-2.5-flash is no longer available to new users. Please update your code to use models/gemini-3.6-flash for the latest features and improvements. We recommend you to use the Interactions API.`

2. **Nhiệm vụ 2 (Game Giáo Dục)**:
   > *"Các game giáo dục tích hợp thêm chức năng đọc câu hỏi từ word latex công thức để chạy game."*

3. **Nhiệm vụ 3 (Nghiên cứu bài học - 4 Bước chuẩn Bộ GD&ĐT)**:
   > *"xem nghiencuubaihoc.html có đủ 4 bước không"* ➔ Khảo sát xác nhận đủ 100% nghiệp vụ 4 bước theo CV 5555, hiện thực hóa qua 12 bước vi mô.
   > Phản hồi người dùng: *"đúng thế"* ➔ Cần nâng cấp giao diện để thể hiện rõ ràng thanh 4 Giai đoạn chuẩn của Bộ (Phase Header), giúp giáo viên và cán bộ quản lý nhìn vào thấy ngay cấu trúc 4 bước chuẩn của Bộ GD&ĐT, đồng thời thao tác mượt mà với 12 bước vi mô.

---

## 2. Khảo sát Gốc rễ Mã nguồn & Phân tích Kiến trúc (Root Cause & Architecture)

### Gốc rễ Vấn đề 1 (Vẽ hình AI):
1. **Khóa cứng danh mục model lỗi thời tại Backend**:
   - Trong `api/vehinh_ai.php`: hàm `vehinh_provider_models()` chỉ trả về `['gemini-3-flash-preview', 'gemini-2.5-flash']`.
   - `vehinh_resolve_model()` loại bỏ các model hiện đại người dùng cấu hình từ cài đặt chung (như `gemini-3.6-flash`, `gemini-3.7-flash`) và ép rơi về default cũ `gemini-2.5-flash`.
   - `api/ai_runtime_config.php` đặt mặc định `'gemini_model' => 'gemini-2.5-flash'`.
2. **Frontend `app.js` (`vehinh.html`) bị kẹt bộ nhớ cache riêng, đè lên cấu hình user đã khai báo**:
   - Trong `app.js`, hàm `getCurrentDrawingModel()` kiểm tra `savedModel = localStorage.getItem('vehinh_ai_model_gemini')` TRƯỚC:
     `if (savedModel && models.includes(savedModel)) return savedModel;`
   - Vì trước đó trình duyệt đã từng lưu `gemini-2.5-flash` vào biến `vehinh_ai_model_gemini`, nên nó đè bẹp `localStorage.getItem('default_gemini_module')` (dù ở trang Cài đặt user đã chọn `Gemini 3.7 Flash`).
   - Nếu `savedModel` là model đã deprecated (`gemini-2.5-flash`), `app.js` không tự động dọn dẹp hoặc fallback sang model user khai báo, dẫn đến dropdown bị "ghim chết" vào `Gemini 2.5 Flash`.
   - Không gửi kèm API keys từ `global_gemini_keys` trong request vẽ hình.
3. **Hiện tượng chạy lâu rồi báo 'Không tìm thấy mã JavaScript trong phản hồi của AI'**:
   - **Gốc rễ tràn token & Thinking ngầm định**: Trong `api/vehinh_ai.php`, `generationConfig` đang đặt `maxOutputTokens = 4096` và thiếu cấu hình `thinkingBudget: 0`.
   - Với các model hiện đại (Gemini 2.5 / 3.7 / 3.6), AI bật chế độ suy nghĩ (Thinking) tốn 15-30 giây và ngốn phần lớn token trong ngân sách 4096. Khi AI bắt đầu viết lời phân tích, văn bản bị chạm kịch trần 4096 tokens (`finishReason: MAX_TOKENS`) và bị Google cắt ngang giữa chừng (ảnh thực tế: bị đứt ở `3. **Đường`), hoàn toàn chưa kịp sinh ra khối `<javascript>...</javascript>`!
   - **Regex bóc tách mã đơn điệu**: Trong `app.js`, hàm `executeAiCode()` chỉ bắt duy nhất thẻ `<javascript>...</javascript>`. Nếu AI dùng khối mã markdown ```javascript ... ``` thì cũng bị báo lỗi không tìm thấy.

### Gốc rễ Vấn đề 2 (Game Giáo Dục):
1. **Game Hub (`trochoi.html` & `trochoi.compiled.js`) chỉ có duy nhất luồng sinh bằng AI**:
   - Tại màn hình SETUP, thiếu giao diện và bộ parser trích xuất câu hỏi từ file Word `.docx` hoặc văn bản chứa công thức toán LaTeX.
2. **Các Game con (`game-*.html`) chưa tự động nhận diện dữ liệu chuyển tiếp**:
   - Các game con khi mở từ `trochoi.html` chưa tự động nạp mảng câu hỏi từ `localStorage.getItem('gameData')`.

### Kiến trúc & Hiện trạng Vấn đề 3 (`nghiencuubaihoc.html`):
1. **Đối chiếu Chuyên môn Sư phạm**:
   - **Quy định chuẩn Bộ GD&ĐT (Công văn 5555/BGDĐT-GDTrH)** gồm 4 bước:
     + **Bước 1: Xây dựng bài dạy minh họa** (Cùng nhau thiết kế KHBD, dự kiến phản ứng HS, chuẩn bị công cụ quan sát).
     + **Bước 2: Tổ chức dạy học minh họa và dự giờ** (Dạy thực tế, dự giờ tập trung vào việc học của HS, chụp ảnh minh chứng).
     + **Bước 3: Phân tích bài học sau giờ dạy** (Thảo luận chuyên môn dựa trên minh chứng, không xếp loại GV).
     + **Bước 4: Vận dụng kết quả vào thực tiễn** (Điều chỉnh KHBD và áp dụng vào các bài học hàng ngày).
   - **Hiện thực hóa trong mã nguồn `nghiencuubaihoc.html`**:
     + Đã có đầy đủ cả 4 bước, được mô hình hóa sâu sắc thành 12 bước vi mô (`STEPS = 1..12`) và 13 sản phẩm minh chứng (`PRODUCTS_13`).
     + *Giai đoạn 1 (Bước 1 Bộ)*: Tương ứng Bước 1 ➔ Bước 7 (Khởi tạo, Phân tích, Đánh giá GA, Câu hỏi NC, Dự kiến HS, KHBD v1 hai lớp, Hồ sơ trước dạy). Sản phẩm 1 đến 9.
     + *Giai đoạn 2 (Bước 2 Bộ)*: Tương ứng Bước 8 (Dạy minh họa, ghi chú thời gian thực, lưu trữ minh chứng). Sản phẩm 10.
     + *Giai đoạn 3 (Bước 3 Bộ)*: Tương ứng Bước 9 & Bước 10 (AI đối chiếu Dự kiến ↔ Thực tế, Thảo luận tổ CM, lập Biên bản phân tích). Sản phẩm 11 & 12.
     + *Giai đoạn 4 (Bước 4 Bộ)*: Tương ứng Bước 11 & Bước 12 (Điều chỉnh KHBD v2, Hoàn thiện & Xuất trọn bộ hồ sơ NCBH). Sản phẩm 13.
2. **Vấn đề Giao diện (UI/UX)**:
   - Header dòng 54 chỉ ghi: `Chu trình NCBH sư phạm · 12 bước · KHBD 2 lớp`.
   - Thanh `#stepperBar` (dòng 67) hiển thị một hàng phẳng 12 nút bước con (`Bước 1` đến `Bước 12`).
   - Thiếu một thanh định vị cấp cao (Macro Phase Bar) gom nhóm 4 giai đoạn chuẩn của Bộ GD&ĐT. Người dùng nhìn vào không thấy ngay 4 bước lớn quen thuộc của Công văn 5555 mà chỉ thấy 12 bước vi mô dàn trải, dễ gây thắc mắc về tính chuẩn hóa.

---

## 3. Kế hoạch Triển khai Chi tiết (Implementation Plan)

### Phần 1: Xử lý Vẽ hình AI
1. **`api/vehinh_ai.php`**:
   - Bổ sung `gemini-3.6-flash`, `gemini-3.7-flash`, `gemini-3-flash-preview`, `gemini-2.0-flash`, `gemini-2.5-pro` vào danh mục `vehinh_provider_models()`.
   - Cập nhật `vehinh_resolve_model()`: Mặc định `gemini-3.6-flash`, tôn trọng model hợp lệ client truyền lên.
   - Bổ sung cơ chế fallback tự động trong `vehinh_call_gemini` khi gặp mã lỗi model dừng hoạt động.
   - Tiếp nhận `api_keys` từ client payload khi session/DB chưa có key.
   - **Khắc phục triệt để lỗi tràn token & chờ lâu**:
     + Tăng `maxOutputTokens` từ `4096` lên `16384`.
     + Thêm `'thinkingConfig' => ['thinkingBudget' => 0]` (vẽ hình trực tiếp, không cần tốn 20-30s "suy nghĩ" ngầm làm hao hụt token).
     + Nâng timeout curl lên 90s.
2. **`api/ai_runtime_config.php`**:
   - Cập nhật default `'gemini_model' => 'gemini-3.6-flash'`.
3. **`app.js` & `vehinh.html`**:
   - Bổ sung `gemini-3.6-flash` (Khuyên dùng) và `gemini-3.7-flash` vào giao diện chọn model.
   - Sửa hàm `getCurrentDrawingModel(provider)`: Ưu tiên đọc cấu hình từ Cài đặt chung `localStorage.getItem('default_gemini_module')` hoặc `khbd_gemini_model`.
   - Cơ chế tự động dọn dẹp model lỗi thời: Nếu `savedModel` (trong `vehinh_ai_model_gemini`) là model bị deprecated như `gemini-2.5-flash`, lập tức xóa bỏ khỏi `localStorage` và tự động nhảy về model user đã khai báo ở Cài đặt chung (ví dụ `Gemini 3.7 Flash` hoặc `Gemini 3.6 Flash`).
   - Bổ sung tùy chọn đầu tiên trong dropdown: `✨ Theo Cài đặt chung (${systemModel})` để người dùng luôn nhận biết rõ ràng model đang chạy theo trang khai báo của mình.
   - Cải tiến system prompt: yêu cầu phần phân tích ngắn gọn súc tích (3-5 gạch đầu dòng), tập trung toàn lực sinh đầy đủ khối mã `<javascript>...</javascript>`.
   - Cải tiến `executeAiCode()`: hỗ trợ linh hoạt cả thẻ `<javascript>...</javascript>`, khối markdown ```javascript ... ``` và ```js ... ```.
   - Gửi kèm API keys từ `global_gemini_keys` trong request vẽ hình.

### Phần 2: Module Đọc câu hỏi Word/LaTeX cho Game Giáo Dục
1. **Tạo `js/game-quiz-importer.js`**:
   - Giải nén file Word `.docx` bằng Mammoth, trích xuất text thô.
   - Regex Parser thông minh nhận diện: Câu hỏi (`Câu 1`, `1.`, `Bài 1`), Phương án (`A.`, `B.`, `C.`, `D.`), Đáp án đúng (`Đáp án: A`, `Key: A`, hoặc bảng đáp án cuối bài), Lời giải (`Giải thích:`, `Lời giải:`).
   - Bảo toàn nguyên vẹn 100% công thức toán học LaTeX (`\(...\)`, `$..$`, `$$...$$`, `\[...\]`).
   - Chuẩn hóa đầu ra tương thích schema của các game (`questions` array hoặc `pairs` array).
2. **Tích hợp vào `trochoi.html` & `trochoi.compiled.js`**:
   - Thêm tab **"📄 Nhập từ Word / LaTeX"** tại màn hình `SETUP`.
   - Cho phép kéo thả file `.docx` / `.txt` hoặc paste văn bản trực tiếp.
   - Xem trước KaTeX trực quan tại màn hình `REVIEW` trước khi bắt đầu chơi.
3. **Đồng bộ hóa các Game con (`game-*.html`)**:
   - Tự động nạp dữ liệu câu hỏi từ `localStorage.getItem('gameData')`.
   - Bổ sung nút nhập nhanh từ Word/LaTeX tại giao diện tạo câu hỏi riêng của từng game.

### Phần 3: Tích hợp Cấu trúc 4 Bước Chuẩn Bộ GD&ĐT vào `nghiencuubaihoc.html`
1. **Định nghĩa Hằng số 4 Giai đoạn chuẩn (Phases Definition)**:
   ```javascript
   const PHASES_4 = [
       {
           id: 1,
           title: 'Bước 1: Xây dựng bài dạy minh họa',
           shortTitle: 'Bước 1: Xây dựng KHBD',
           desc: 'Chuẩn bị, nghiên cứu bài học, xác định vấn đề và thiết kế KHBD 2 lớp',
           color: 'emerald',
           steps: [1, 2, 3, 4, 5, 6, 7],
           icon: 'fa-book-open-reader'
       },
       {
           id: 2,
           title: 'Bước 2: Tổ chức dạy minh họa & dự giờ',
           shortTitle: 'Bước 2: Dạy & Dự giờ',
           desc: 'Dự giờ tập trung vào hoạt động học của HS, ghi chép và thu thập minh chứng',
           color: 'blue',
           steps: [8],
           icon: 'fa-chalkboard-user'
       },
       {
           id: 3,
           title: 'Bước 3: Phân tích bài học sau tiết dạy',
           shortTitle: 'Bước 3: Phân tích bài học',
           desc: 'Thảo luận tổ chuyên môn dựa trên minh chứng thực tế, không xếp loại GV',
           color: 'amber',
           steps: [9, 10],
           icon: 'fa-comments'
       },
       {
           id: 4,
           title: 'Bước 4: Vận dụng kết quả vào thực tiễn',
           shortTitle: 'Bước 4: Vận dụng & Hoàn thiện',
           desc: 'Điều chỉnh bài học (KHBD v2), hoàn thiện và đóng gói trọn bộ hồ sơ NCBH',
           color: 'purple',
           steps: [11, 12],
           icon: 'fa-award'
       }
   ];
   ```
2. **Nâng cấp Giao diện Tiến trình (Progress & Navigation UI)**:
   - **Header trang**: Cập nhật subtitle:
     `Chu trình NCBH sư phạm · 4 bước chuẩn Bộ GD&ĐT (Công văn 5555) · 12 bước số hóa chuyên sâu · KHBD 2 lớp`.
   - **Bổ sung Thanh 4 Giai đoạn chuẩn (`#phaseBar`)** đặt phía trên `#stepperBar`:
     + Hiển thị 4 khối (Card) đại diện cho 4 bước chuẩn của Bộ GD&ĐT.
     + Phase đang thực hiện (`currentStep` nằm trong `phase.steps`) được highlight nổi bật (active border, background gradient, glow effect).
     + Hiển thị huy hiệu trạng thái: `Đang thực hiện` / `Hoàn thành (X/Y bước)` / `Chưa bắt đầu`.
     + Khi người dùng click vào một Phase Card: Chuyển ngay đến bước con đầu tiên chưa hoàn thành (hoặc bước đầu tiên) của giai đoạn đó.
   - **Nâng cấp Thanh 12 Bước vi mô (`#stepperBar`)**:
     + Phân nhóm trực quan theo 4 Phase: Thêm viền màu / nhãn màu tương ứng của Phase mẹ (Phase 1: viền emerald, Phase 2: viền blue, Phase 3: viền amber, Phase 4: viền purple).
     + Giữ nguyên cơ chế chuyển bước `goStep(n)`, tích hợp mượt mà với `state.currentStep` và `state.completedSteps`.
   - **Bổ sung Modal / Card tra cứu Sơ đồ 4 bước chuẩn**:
     + Nút "📖 Sơ đồ 4 bước chuẩn CV 5555" trên header hoặc cạnh thanh tiến trình.
     + Modal hiển thị bảng ánh xạ chuẩn xác: 4 bước Bộ GD&ĐT ➔ Mục đích sư phạm ➔ 12 bước phần mềm ➔ 13 sản phẩm bàn giao, giúp giáo viên và thanh tra chuyên môn tra cứu nhanh chóng.
3. **Bảo toàn Nguyên vẹn Logic Hệ thống**:
   - Giữ nguyên cấu trúc dữ liệu `state`, `emptyState()`, `STEPS`, `PRODUCTS_13`, `CAN_CU`.
   - Không làm ảnh hưởng đến các hàm gọi AI (`runAiTask`), lưu CSDL (`saveSession`, `loadSessionById`), và xuất file (`exportDocx`, `exportZip`).

---

## 4. Kế hoạch Kiểm thử & Thẩm định (Verification Plan)

1. **Kiểm thử Tự động**:
   - `tests/game-quiz-importer-smoke.js`: Kiểm tra giải nén `.docx`, regex parser câu hỏi/phương án/đáp án/LaTeX, và kiểm tra cấu hình model vẽ hình AI.
   - `tests/nghiencuubaihoc-phases-test.js`: Kiểm tra logic gom nhóm 4 phases của `nghiencuubaihoc.html`, đảm bảo 12 bước phủ kín 100% 4 phases không bị trùng lặp hay sót bước.
   - Chạy `node tests/run-all-tests.js` bảo đảm tất cả test suites đều PASS.
2. **Kiểm thử Thủ công**:
   - **Vẽ hình AI**: Mở `vehinh.html`, tạo yêu cầu vẽ hình toán học -> Model mặc định là `gemini-3.6-flash`, hình sinh thành công, không còn thông báo `gemini-2.5-flash deprecated`.
   - **Game Giáo Dục**: Mở `trochoi.html`, tab "Nhập từ Word / LaTeX", nạp file đề mẫu có KaTeX -> Xem trước KaTeX hiển thị đẹp, chuyển sang game con chạy đúng bộ câu hỏi.
   - **Nghiên cứu bài học**: Mở `nghiencuubaihoc.html`:
     + Quan sát thanh 4 Bước chuẩn của Bộ hiển thị rõ ràng trên đầu stepper.
     + Chuyển từ Bước 1 ➔ Bước 7: Phase 1 sáng và đếm tiến độ `X/7`.
     + Chuyển sang Bước 8: Phase 2 sáng `1/1`.
     + Chuyển sang Bước 9, 10: Phase 3 sáng.
     + Chuyển sang Bước 11, 12: Phase 4 sáng.
     + Bấm mở modal tra cứu Sơ đồ 4 bước chuẩn hiển thị đầy đủ, sắc nét.
     + Lưu CSDL, tải lại hồ sơ, chạy các tác vụ AI và xuất file DOCX/ZIP hoạt động hoàn hảo.
