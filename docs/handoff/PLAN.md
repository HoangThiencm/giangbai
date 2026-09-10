# KẾ HOẠCH BÀN GIAO TRIỂN KHAI (HANDOFF PLAN)
## Nhiệm vụ 1: Sửa lỗi Vẽ hình AI không đọc cấu hình, module từ cài đặt (Model gemini-2.5-flash deprecated)
## Nhiệm vụ 2: Tích hợp chức năng đọc câu hỏi từ Word / LaTeX công thức cho các Game giáo dục

---

## 1. Hiện trạng & Phản ánh từ Người dùng
1. **Phản ánh Vẽ hình AI**:
   > *"vẽ hình bằng AI nó không đọc cấu hình, module từ cài đặt mà chạy độc lập thì phải và báo lỗi như ảnh"*
   - Ảnh báo lỗi: `Lỗi AI vẽ hình: This model models/gemini-2.5-flash is no longer available to new users. Please update your code to use models/gemini-3.6-flash for the latest features and improvements. We recommend you to use the Interactions API.`
2. **Phản ánh Game Giáo Dục**:
   > *"Các game giáo dục tích hợp thêm chức năng đọc câu hỏi từ word latex công thức để chạy game."*

---

## 2. Khảo sát Gốc rễ Mã nguồn (Root Cause Analysis)

### Gốc rễ Vấn đề 1 (Vẽ hình AI):
1. **Khóa cứng danh mục model lỗi thời tại Backend**:
   - Trong `api/vehinh_ai.php`:
     ```php
     function vehinh_provider_models(): array {
         return ['gemini' => ['gemini-3-flash-preview', 'gemini-2.5-flash']];
     }
     ```
     và hàm `vehinh_resolve_model()` chỉ chấp nhận model nằm trong danh mục trên. Bất kỳ model nào người dùng cấu hình từ cài đặt chung (như `gemini-3.6-flash`, `gemini-3.7-flash`...) đều bị hàm này loại bỏ và ép rơi về default cũ `gemini-2.5-flash`!
   - `api/ai_runtime_config.php` đặt mặc định `'gemini_model' => 'gemini-2.5-flash'`.
2. **Frontend `app.js` (`vehinh.html`) chạy độc lập, không đọc cấu hình chung**:
   - `app.js` khai báo `DRAWING_AI_MODEL_CATALOG` chỉ gồm `gemini-3-flash-preview` và `gemini-2.5-flash`.
   - `app.js` không đồng bộ `localStorage.getItem('default_gemini_module')` hay `khbd_gemini_model`.
   - Khi gửi request sang `api/vehinh_ai.php`, `app.js` không truyền kèm `api_keys` từ client (`global_gemini_keys`), dẫn đến phụ thuộc hoàn toàn vào session/DB.
   - `api/vehinh_ai.php` thiếu cơ chế fallback tự động khi Google báo model bị dừng hỗ trợ (`no longer available`).

### Gốc rễ Vấn đề 2 (Game Giáo Dục):
1. **Game Hub (`trochoi.html` & `trochoi.compiled.js`) chỉ có duy nhất luồng sinh bằng AI**:
   - Tại `trochoi.compiled.js` (`step === 'SETUP'`), chỉ có form nhập chủ đề và nút "Tạo nội dung với AI".
   - Giáo viên có sẵn đề thi, ngân hàng câu hỏi dạng Word `.docx` hoặc văn bản có công thức toán LaTeX không thể đưa vào để tạo màn chơi game.
2. **Các Game con (`game-*.html`) chưa tự động nhận diện dữ liệu chuyển tiếp**:
   - Các game con (`game-elimination.html`, `game-speedscore.html`, `game-tower.html`, `game-unlock.html`, `game-teambattle.html`) khi được mở từ `trochoi.html` chưa tự động nạp mảng câu hỏi từ `localStorage.getItem('gameData')`.
   - Bản thân các màn hình khởi tạo câu hỏi trong từng game con cũng thiếu chức năng bóc tách từ file Word / công thức LaTeX.

---

## 3. Kế hoạch Triển khai Chi tiết (Implementation Steps)

### Phần 1: Xử lý Vẽ hình AI
1. **`api/vehinh_ai.php`**:
   - Cập nhật `vehinh_provider_models()`: bổ sung `gemini-3.6-flash`, `gemini-3.7-flash`, `gemini-3-flash-preview`, `gemini-2.0-flash`, `gemini-2.5-pro`, `gemini-2.5-flash`.
   - `vehinh_resolve_model()`: Cho phép chấp nhận các model Gemini hợp lệ từ client gửi lên hoặc cấu hình runtime; ưu tiên mặc định là `gemini-3.6-flash`.
   - Trong `vehinh_call_gemini`: Tự động thử fallback sang `gemini-3.6-flash` / `gemini-3.7-flash` nếu model gặp lỗi `no longer available` hoặc 404.
   - Cho phép nhận `api_keys` từ payload client gửi kèm (fallback khi server session/DB chưa có key).
2. **`api/ai_runtime_config.php`**:
   - Cập nhật default `'gemini_model' => 'gemini-3.6-flash'`.
3. **`app.js` & `vehinh.html`**:
   - Bổ sung `gemini-3.6-flash` (Khuyên dùng) và `gemini-3.7-flash` vào danh mục model frontend.
   - Khi load trang, tự động đọc `default_gemini_module` hoặc `khbd_gemini_model` từ Cài đặt để đồng bộ làm model mặc định.
   - Truyền `api_keys` lấy từ `global_gemini_keys` trong request vẽ hình.
   - Cập nhật `ai-design-config.js` hỗ trợ chọn `gemini-3.6-flash` và `gemini-3.7-flash`.

### Phần 2: Xây dựng Module Đọc câu hỏi Word/LaTeX cho Game Giáo Dục
1. **Tạo `js/game-quiz-importer.js`**:
   - Dùng `mammoth.extractRawText` giải nén file `.docx` sang văn bản thô.
   - Bộ Regex Parser bóc tách:
     + Câu hỏi: `Câu 1:`, `Bài 1:`, `1.`, `1/`, v.v.
     + Phương án: `A.`, `B.`, `C.`, `D.` (hỗ trợ cả xuống dòng và inline).
     + Đáp án: `Đáp án: A`, `Đ/A: A`, `Key: A`, hoặc bảng đáp án cuối trang `1.A 2.B...`.
     + Lời giải / giải thích: `Lời giải:`, `Giải thích:`.
     + Bảo toàn 100% công thức toán học LaTeX (`\(...\)`, `$..$`, `$$...$$`, `\[...\]`).
     + Chuyển đổi linh hoạt sang schema tương thích của 8 game (`questions` gồm `id, prompt, choices, answer, explanation` hoặc `pairs` cho matching).
2. **Tích hợp vào `trochoi.html` & `trochoi.compiled.js`**:
   - Thêm thư viện `mammoth.browser.min.js` và `js/game-quiz-importer.js` vào `trochoi.html`.
   - Trong `trochoi.compiled.js` (Màn hình `SETUP`):
     + Thêm tab **"📄 Nhập từ Word / LaTeX"** song song với **"🤖 Tạo bằng AI"**.
     + UI cho phép kéo thả/chọn file `.docx` / `.txt` hoặc dán đề bài trực tiếp.
     + Hỗ trợ xem định dạng mẫu câu hỏi có công thức LaTeX.
     + Bấm "Xử lý & Nạp câu hỏi" -> Nạp vào `generatedContent` và chuyển ngay sang màn hình `REVIEW` (xem trước công thức hiển thị KaTeX sắc nét).
     + Bấm "Bắt đầu chơi" -> Lưu `gameData` và chuyển sang trang game tương ứng.
3. **Đồng bộ hóa các Game con (`game-*.html`)**:
   - `game-elimination.html`, `game-speedscore.html`, `game-unlock.html`, `game-tower.html`, `game-teambattle.html`:
     + Tự động nạp câu hỏi từ `localStorage.getItem('gameData')` khi khởi động.
     + Bổ sung nút nhập Word/LaTeX trực tiếp tại màn hình tạo câu hỏi riêng của từng game.

---

## 4. Kế hoạch Kiểm thử & Thẩm định
1. Chạy test tự động mới `tests/game-quiz-importer-smoke.js` kiểm tra bóc tách Word/LaTeX và cấu hình model vẽ hình AI.
2. Chạy `node tests/run-all-tests.js` bảo đảm 100% test suites hiện có đều PASS.
3. Kiểm thử thủ công:
   - Truy cập `vehinh.html` và thực hiện vẽ hình -> Không còn lỗi `gemini-2.5-flash deprecated`.
   - Mở `trochoi.html`, nạp file Word hoặc dán bài tập chứa công thức LaTeX -> Công thức hiển thị chuẩn KaTeX và game chạy mượt mà.
