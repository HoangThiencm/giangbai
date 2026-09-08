# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Khắc phục câu văn ngô nghê/vô nghĩa do ghép thô tên bài học**:
   - Hàm `cleanMathEntityName(lessonName)` đã được bổ sung và tích hợp trong `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`, và `xaydungphuluc.html`.
   - Các tiền tố sư phạm như "Khái niệm phương trình...", "Nhận biết...", "Mở đầu về..." đã được loại bỏ khi ghép chuỗi vào ngữ cảnh toán học.
   - Chuỗi "nghiệm của Khái niệm phương trình..." được chuyển thành "nghiệm của phương trình và hệ hai phương trình bậc nhất hai ẩn", chuẩn ngữ pháp tiếng Việt và ngôn ngữ học thuật toán học.
2. **Tách Phụ lục 3 thành 8 cột riêng biệt cho NLS và AI**:
   - Cột 7: Biểu hiện năng lực số (màu xanh lam `#0070C0`).
   - Cột 8: Biểu hiện năng lực AI (màu tím `#7030A0`).
   - Cập nhật đồng bộ trên HTML xem trước, xuất Word DOCX, bảng nhập liệu PPCT, và kiểm tra thẩm định CV 5512.
3. **Đồng bộ file và bản sao mirror**:
   - `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html` đạt 100% byte-identical (344,893 bytes).
   - `xaydungphuluc.html` đồng bộ hoàn toàn cấu trúc và logic.

## Test đã chạy
1. `node tests/xaydungphuluc-smoke.js` — PASS
2. `node tests/xaydungphuluc-math-smoke.js` — PASS (Kiểm thử OMML Equation và đồng bộ NLS/AI)
3. `node -e "const fs = require('fs'); const a = fs.readFileSync('canvas_xaydungphuluc.html'); const b = fs.readFileSync('backupcode viettailieu/canvas_xaydungphuluc.html'); console.log('Equal:', a.equals(b));"` — PASS (Equal: true)
4. `node tests/run-all-tests.js` — PASS 61/61 test suites

## Pass / Fail từng tiêu chí
- [x] Tách Phụ lục 3 thành 8 cột riêng biệt NLS và AI: PASS
- [x] Xử lý câu diễn đạt toán học chuẩn xác qua `cleanMathEntityName`: PASS
- [x] Xuất Word DOCX chuẩn 8 cột với độ rộng và định dạng màu sắc tương ứng: PASS
- [x] Báo cáo thẩm định đồng bộ NLS & AI giữa PL1 và PL3: PASS
- [x] Đồng bộ 100% byte-identical giữa canvas và backup: PASS
- [x] Toàn bộ 61 test suites trong dự án: PASS

## Bug
Không phát hiện lỗi hồi quy.
