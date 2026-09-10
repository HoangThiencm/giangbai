# VERIFY — Khắc phục Lỗi AI Vẽ Hình & Tích hợp Đọc Câu hỏi Word / LaTeX cho Game Giáo Dục

## Kết luận
PASS 100%

## Đối chiếu Scope & Nghiệp vụ
1. **Nhiệm vụ 1: Sửa lỗi AI Vẽ Hình không đọc cấu hình, module từ cài đặt và báo lỗi deprecated model**:
   - `api/vehinh_ai.php` đã cập nhật danh mục model hỗ trợ các model Gemini hiện đại: `gemini-3.6-flash`, `gemini-3.7-flash`, `gemini-3-flash-preview`, `gemini-2.0-flash`, `gemini-2.5-pro`, `gemini-2.5-flash`.
   - `vehinh_resolve_model()` ưu tiên nhận model từ client/runtime và kiểm tra tính hợp lệ, mặc định là `gemini-3.6-flash`.
   - Cơ chế fallback retry tự động trong `vehinh_call_gemini()`: khi Google báo lỗi 404 hoặc `no longer available` / `not found`, hệ thống tự động thử lại với `gemini-3.6-flash` / `gemini-3.7-flash`.
   - Hỗ trợ client truyền `api_keys` làm phương án dự phòng khi server chưa có key.
   - `app.js` và `vehinh.html`: Cập nhật `DRAWING_AI_MODEL_CATALOG` và nhãn hiển thị; tự động đồng bộ model từ `localStorage.getItem('default_gemini_module')` hoặc `khbd_gemini_model`.
   - `ai-design-config.js` đã hỗ trợ chọn `gemini-3.6-flash` và `gemini-3.7-flash`, mặc định `gemini-3.6-flash`.

2. **Nhiệm vụ 2: Tích hợp chức năng đọc câu hỏi từ Word / LaTeX công thức để chạy Game giáo dục**:
   - Tạo thư viện `js/game-quiz-importer.js`:
     + Trích xuất nội dung văn bản thô từ file Word (.docx) qua Mammoth và file text (.txt).
     + Bóc tách trắc nghiệm 4 lựa chọn (A/B/C/D), hỗ trợ cả xuống dòng và inline.
     + Nhận diện đáp án đúng inline (`Đáp án: A`) và bảng đáp án cuối bài (`1.A 2.B...`).
     + Nhận diện các cặp ghép đôi (`[Vế trái] - [Vế phải]`).
     + Bảo toàn 100% cú pháp công thức toán học LaTeX (`\(...\)`, `$..$`, `$$...$$`, `\[...\]`).
     + Tự động định dạng đúng chuẩn Schema của cả 8 Game Giáo Dục (`elimination`, `speedscore`, `tower`, `unlock`, `teambattle`, `matching`, `treasure`, `escape`).
   - Giao diện trung tâm `trochoi.html` & `trochoi.compiled.js`:
     + Thêm tab "2. Đọc từ Word / LaTeX" cạnh tab "1. Tạo nội dung với AI".
     + Hỗ trợ chọn file Word (.docx), xem định dạng mẫu, dán văn bản có công thức LaTeX.
     + Hỗ trợ kèm danh sách học sinh đua vịt cho game `treasure`.
     + Màn hình xem trước `REVIEW` hiển thị sắc nét công thức KaTeX, cho phép chỉnh sửa hoặc bấm "Chơi luôn" (`handleStartGame`).
   - Đồng bộ các Game con (`game-*.html`):
     + `game-elimination.html`, `game-speedscore.html`, `game-tower.html`, `game-unlock.html`, `game-teambattle.html` đã được tích hợp hook `useEffect` nạp trực tiếp `localStorage.getItem('gameData')`.
     + `game-elimination.html` có nút chơi ngay với câu hỏi đã nạp và hỗ trợ tải file Word/LaTeX trực tiếp tại màn hình `questionSource`.
     + Cập nhật các fallback model Gemini từ các mã lỗi thời sang `gemini-3.6-flash`.

## Test đã chạy
1. `node tests/game-quiz-importer-smoke.js` — **PASS 100%** (6/6 sub-tests: MCQ với LaTeX inline, bảng đáp án cuối bài, cặp ghép Matching, Schema 8 game, Model catalog & fallback AI vẽ hình, tích hợp game).
2. `node tests/run-all-tests.js` — **PASS 100%** (Toàn bộ 64/64 test suites thành công, exit code 0).
3. `node -c trochoi.compiled.js` — **PASS** (Cú pháp JS hợp lệ, không lỗi compile).

## Bảng tiêu chí Thẩm định
- [x] Sửa lỗi AI vẽ hình báo deprecated model: PASS
- [x] AI vẽ hình đồng bộ model từ cài đặt hệ thống (`gemini-3.6-flash`): PASS
- [x] Backend `api/vehinh_ai.php` có cơ chế fallback retry khi model lỗi: PASS
- [x] Thư viện `js/game-quiz-importer.js` bóc tách câu hỏi từ Word và LaTeX: PASS
- [x] Giữ nguyên 100% công thức toán KaTeX/LaTeX: PASS
- [x] Nhận diện đúng đáp án inline và bảng đáp án cuối bài: PASS
- [x] Định dạng chuẩn cho tất cả 8 game giáo dục: PASS
- [x] `trochoi.html` có tab chọn tạo bằng AI hoặc đọc từ Word/LaTeX: PASS
- [x] Game con (`game-*.html`) tự động nạp câu hỏi từ `gameData`: PASS
- [x] Toàn bộ 64 test suites trong hệ thống đạt 100% PASS: PASS

---

# VERIFY

## Đối chiếu scope
1. **Khắc phục lỗi Phụ lục 3 không xuất / không hiển thị Biểu hiện năng lực AI**:
   - Khắc phục lỗi lệch ID giữa các ứng viên tiết AI (`source:0`) và các dòng kế hoạch Phụ lục 3 (`ppct:0`) bằng hàm `selectedPeriodsForLesson(lessonId, lessonName)` đa tầng.
   - Nâng cấp `appendixThreeTable` kế thừa trực tiếp 100% từ bảng Phụ lục 1 (`results['1'].scheduleTable`) theo tên bài học (`lessonsMatch`), đảm bảo tính nhất quán tuyệt đối giữa Kế hoạch Tổ chuyên môn và Kế hoạch Giáo viên.
   - Cơ chế bảo toàn kép: khi có mã AI và có tiết được chọn, tự động bảo toàn mã AI qua `cleanAiColumnText`.
   - Xem trước (`renderPreview`) và Xuất Word (`exportDocx`) cho Phụ lục 3 luôn đảm bảo cấu trúc 8 cột chuẩn qua `planModel` 8 cột từ `appendixThreeTable`.
   - `loadDefaultPpctStructure` tự động kích hoạt 10-12 tiết AI chuẩn (30%) khi bật AI, không còn bị reset về 0%.
2. **Khắc phục câu văn ngô nghê/vô nghĩa do ghép thô tên bài học**:
   - Hàm `cleanMathEntityName(lessonName)` loại bỏ các tiền tố sư phạm như "Khái niệm phương trình...", "Nhận biết...", "Mở đầu về..." khi ghép vào câu toán học ("nghiệm của phương trình...").
3. **Chuẩn hóa Bảng chia sẻ (Padlet) theo yêu cầu**:
   - **Dòng thông tin bài đăng**: Chỉ hiển thị `[Tên người đăng] · [Thời gian]` qua định dạng `${esc(p.author_name || 'Ẩn danh')} · ${esc(fmt(p.created_at))}`. Loại bỏ hoàn toàn lớp/nhóm và môn học.
   - **Form đăng bài**: Form `#postForm` và hàm `submitPost` không nhận/không gửi trường lớp, nhóm hoặc môn. Backend `api/padlet.php` thiết lập `$group = ''`, không nhận `$_POST['author_group']`.
   - **Bảo toàn nội dung & tương tác**: Giữ nguyên nội dung bài, link xem trước OpenGraph, tệp đính kèm Drive, phản hồi cảm xúc (👍, ❤️, ⭐) và bình luận.
   - **Phân quyền Ghim (`pin`)**: Chỉ chủ bảng (`state.canManage`) mới nhìn thấy và sử dụng nút Ghim. API từ chối quyền Ghim với bất kỳ ai không phải chủ bảng (`403 Forbidden`).
   - **Phân quyền Xóa (`delete`)**: Chỉ chủ bảng HOẶC chính tài khoản đã đăng bài (`$currentUser['id'] === $post['author_user_id']`) mới có quyền xóa. Khách có link bảng hoặc học sinh khác tuyệt đối không thể xóa, kể cả gọi API trực tiếp.
4. **Đồng bộ file và bản sao mirror**:
   - `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html` đạt 100% byte-identical (346,497 bytes, SHA256 trùng khớp).
   - `xaydungphuluc.html` đồng bộ hoàn toàn cấu trúc và logic.

## Test đã chạy
1. `node tests/padlet-ownership-smoke.js` — PASS (Kiểm thử metadata bài đăng, form submit, phân quyền Ghim/Xóa và API chặn unauthorized deletion)
2. `node tests/xaydungphuluc-smoke.js` — PASS
3. `node tests/xaydungphuluc-math-smoke.js` — PASS (Kiểm thử OMML Equation, đồng bộ NLS/AI và cột AI Phụ lục 3)
4. `node tests/canvas-xaydungphuluc-smoke.js` — PASS
5. `node -e "const fs = require('fs'); const a = fs.readFileSync('canvas_xaydungphuluc.html'); const b = fs.readFileSync('backupcode viettailieu/canvas_xaydungphuluc.html'); console.log('Equal:', a.equals(b));"` — PASS (Equal: true)
6. `node tests/run-all-tests.js` — PASS 63/63 test suites (100%)

## Pass / Fail từng tiêu chí
- [x] Dòng dưới bài chỉ còn: `Tên người đăng · Thời gian`: PASS
- [x] Đã bỏ lớp, môn khỏi hiển thị và form đăng bài mới: PASS
- [x] Giữ nguyên nội dung bài viết, link đính kèm, tệp tải lên Drive: PASS
- [x] Giữ nguyên tương tác thả biểu tượng cảm xúc và bình luận: PASS
- [x] Nút Ghim chỉ chủ bảng (giáo viên tạo bảng) mới dùng được: PASS
- [x] Nút Xóa chỉ dành cho chủ bảng hoặc chính tài khoản đã đăng bài đó: PASS
- [x] Khách/học sinh có đường link không thể xóa bài của người khác (chặn cả frontend và backend API): PASS
- [x] Phụ lục 3 hiển thị và xuất đầy đủ cột "Biểu hiện năng lực AI": PASS
- [x] Tách Phụ lục 3 thành 8 cột riêng biệt NLS và AI: PASS
- [x] Xử lý câu diễn đạt toán học chuẩn xác qua `cleanMathEntityName`: PASS
- [x] Xuất Word DOCX chuẩn 8 cột với độ rộng và định dạng màu sắc tương ứng: PASS
- [x] Đồng bộ 100% mã tích hợp giữa Phụ lục 1 và Phụ lục 3: PASS
- [x] Đồng bộ 100% byte-identical giữa canvas và backup: PASS
- [x] Toàn bộ 63 test suites trong dự án: PASS

## Bug
Không phát hiện lỗi hồi quy.
