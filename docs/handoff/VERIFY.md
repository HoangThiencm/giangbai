# VERIFY

## Kết luận
PASS 100%

## Đối chiếu scope
1. **Khắc phục lỗi Phụ lục 3 không xuất / không hiển thị Biểu hiện năng lực AI**:
   - Khắc phục lỗi lệch ID giữa các ứng viên tiết AI (`source:0`) và các dòng kế hoạch Phụ lục 3 (`ppct:0`) bằng hàm `selectedPeriodsForLesson(lessonId, lessonName)` đa tầng.
   - Nâng cấp `appendixThreeTable` kế thừa trực tiếp 100% từ bảng Phụ lục 1 (`results['1'].scheduleTable`) theo tên bài học (`lessonsMatch`), đảm bảo tính nhất quán tuyệt đối giữa Kế hoạch Tổ chuyên môn và Kế hoạch Giáo viên.
   - Cơ chế bảo toàn kép: khi có mã AI và có tiết được chọn, tự động bảo toàn mã AI qua `cleanAiColumnText`.
   - Xem trước (`renderPreview`) và Xuất Word (`exportDocx`) cho Phụ lục 3 luôn đảm bảo cấu trúc 8 cột chuẩn qua `planModel` 8 cột từ `appendixThreeTable`.
   - `loadDefaultPpctStructure` tự động kích hoạt 10-12 tiết AI chuẩn (30%) khi bật AI, không còn bị reset về 0%.
2. **Khắc phục câu văn ngô nghê/vô nghĩa do ghép thô tên bài học**:
   - Hàm `cleanMathEntityName(lessonName)` loại bỏ các tiền tố sư phạm như "Khái niệm phương trình...", "Nhận biết...", "Mở đầu về..." khi ghép vào câu toán học ("nghiệm của phương trình...").
3. **Đồng bộ file và bản sao mirror**:
   - `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html` đạt 100% byte-identical (346,497 bytes, SHA256 trùng khớp).
   - `xaydungphuluc.html` đồng bộ hoàn toàn cấu trúc và logic.

## Test đã chạy
1. `node tests/xaydungphuluc-smoke.js` — PASS
2. `node tests/xaydungphuluc-math-smoke.js` — PASS (Kiểm thử OMML Equation, đồng bộ NLS/AI và cột AI Phụ lục 3)
3. `node tests/canvas-xaydungphuluc-smoke.js` — PASS
4. `node -e "const fs = require('fs'); const a = fs.readFileSync('canvas_xaydungphuluc.html'); const b = fs.readFileSync('backupcode viettailieu/canvas_xaydungphuluc.html'); console.log('Equal:', a.equals(b));"` — PASS (Equal: true)
5. `node tests/run-all-tests.js` — PASS 63/63 test suites (100%)

## Pass / Fail từng tiêu chí
- [x] Phụ lục 3 hiển thị và xuất đầy đủ cột "Biểu hiện năng lực AI": PASS
- [x] Tách Phụ lục 3 thành 8 cột riêng biệt NLS và AI: PASS
- [x] Xử lý câu diễn đạt toán học chuẩn xác qua `cleanMathEntityName`: PASS
- [x] Xuất Word DOCX chuẩn 8 cột với độ rộng và định dạng màu sắc tương ứng: PASS
- [x] Đồng bộ 100% mã tích hợp giữa Phụ lục 1 và Phụ lục 3: PASS
- [x] Đồng bộ 100% byte-identical giữa canvas và backup: PASS
- [x] Toàn bộ 63 test suites trong dự án: PASS

## Bug
Không phát hiện lỗi hồi quy.
