# PLAN: Khắc phục lỗi tính số tiết Năng lực số (NLS) và Trí tuệ nhân tạo (AI) không chuẩn trong Xây dựng phụ lục

---

## 1. Yêu cầu & Mục tiêu
- **Vấn đề người dùng phản ánh**: Khi người dùng cấu hình/yêu cầu tích hợp đúng **28 tiết Năng lực số** và **12 tiết AI**, khi đếm trong bảng phụ lục (hoặc xem kết quả) thì lại ra **30 tiết Năng lực số** và **14 tiết AI** (bị dôi ra +2 tiết NLS và +2 tiết AI).
- **Mục tiêu**: Đảm bảo hệ thống tính toán, phân bổ và hiển thị số tiết NLS và AI chuẩn xác 100% theo đúng số lượng tiết (hoặc bài) mà người dùng yêu cầu; loại bỏ hoàn toàn hiện tượng dôi/tràn tiết do so khớp chéo (false-positive match) giữa các bài học có tên tương tự.

---

## 2. Phân tích Nguyên nhân gốc rễ (Root Causes)

1. **Lỗi so khớp chéo (Fuzzy Match Collision) trong `isLessonNlsSelected` và `selectedPeriodsForLesson`**:
   - Trong `isLessonNlsSelected(lessonId, lessonName, c, index)`:
     Khi `lessonId` được truyền vào (ví dụ `ppct:27`), nếu bài này **không được chọn** (`nlsSelectedLessonIds.has(lessonId) === false`), hàm lại tiếp tục chạy xuống:
     ```javascript
     if (lessonName) {
       const match = nlsCandidates().find(x => typeof lessonsMatch === 'function' ? lessonsMatch(x.lesson, lessonName) : x.lesson === lessonName);
       if (match && nlsSelectedLessonIds.has(match.id)) return true;
     }
     ```
   - Tương tự trong `selectedPeriodsForLesson(lessonId, lessonName)`:
     Khi `lessonId` có truyền vào nhưng bài đó không có tiết AI (`byId.length === 0`), hàm lại fallback sang so khớp tên bài bằng `lessonsMatch(x.lesson, lessonName)`.
   - Trong khi đó, `lessonsMatch` có quy tắc kiểm tra từ khóa trùng lặp (`overlap >= 2`), nhưng hàm `cleanLessonName` và `lessonKeywords` lại **chưa loại bỏ** các từ chung như `'TRAI'`, `'NGHIEM'`, `'VA'`, `'HINH'`, cụm `"THỰC HÀNH VÀ TRẢI NGHIỆM"`.
   - Hậu quả: Bài học A (được chọn NLS/AI, ví dụ bài trải nghiệm 2 tiết) bị khớp nhầm sang Bài học B (không hề được chọn NLS/AI, cũng là bài trải nghiệm 2 tiết). Kết quả là Bài B tự động bị gán ké NLS và AI, dẫn đến tổng số tiết bị dôi ra đúng 2 tiết NLS (28 -> 30) và 2 tiết AI (12 -> 14)!

2. **Lỗi đồng bộ mã tích hợp sang Phụ lục 3 (`appendixThreeTable` & `syncIntegrationFromAppendixOne`)**:
   - Khi nối dữ liệu từ Phụ lục 1 sang Phụ lục 3:
     `const pl1Row = pl1Model.rows.find(item => !item.isHeader && lessonsMatch((item.cells||[])[pl1LessonIdx], row.lesson));`
   - Việc dùng `find` với `lessonsMatch` khiến nhiều dòng có tên chung (như "Ôn tập", "Luyện tập chung", "Thực hành trải nghiệm") ở các học kỳ khác nhau cùng trỏ về một dòng duy nhất của Phụ lục 1, làm nhân bản mã NLS/AI sang các dòng không mong muốn.

3. **Prompt sinh Phụ lục của AI thiếu danh sách bài học NLS được chọn**:
   - Trong `appendixPrompt(no, c)`: Prompt có danh sách tiết AI (`selectedText`) và yêu cầu nghiêm ngặt cấm xuất mã AI ngoài danh sách. Tuy nhiên, với NLS, prompt chỉ ghi quy tắc phân bổ chung chung mà **hoàn toàn không có danh sách các bài NLS được chọn** (`nlsSelectedText`). Do đó AI tự ý gán NLS vào nhiều bài khác, và do bug so khớp ở mục 1, các mã NLS này được chấp nhận vào bảng.

4. **Thuật toán chọn tiết trong `chooseNlsLessonsForPeriods` và `syncAiSelectionFromCount`**:
   - Cần đảm bảo khi người dùng nhập 28 tiết NLS và 12 tiết AI, danh sách chọn bài (`nlsSelectedLessonIds` và `aiSelectedLessonIds`) có tổng số tiết chuẩn xác, đồng bộ nhất quán giữa số hiển thị ở Section 3, Section 5 và các bảng kết quả ở Section 8.

---

## 3. Phạm vi tệp tin cần sửa đổi (Scope)
1. `xaydungphuluc.html`
2. `backupcode viettailieu/canvas_xaydungphuluc.html`
3. `canvas_xaydungphuluc.html` (đồng bộ từ bản canvas để đảm bảo môi trường kiểm thử đầy đủ)
4. `tests/xaydungphuluc-smoke.js`

---

## 4. Hướng dẫn chi tiết cho Coder

### PHẦN A: Sửa logic so khớp trong `xaydungphuluc.html` và các file canvas

1. **Sửa hàm `isLessonNlsSelected(lessonId, lessonName, c, index)`**:
   - Khi `lessonId` được cung cấp (khác rỗng):
     - Chỉ kiểm tra duy nhất: `if (nlsSelectedLessonIds.has(lessonId)) return true; else return false;`.
     - **Tuyệt đối không** fallback xuống `lessonName` / `lessonsMatch` khi `lessonId` đã xác định rõ ràng.
   - Chỉ fallback sang `lessonName` / `lessonsMatch` khi `lessonId` là `null`, `undefined` hoặc rỗng `''` (ví dụ khi dữ liệu từ AI trả về không có ID).

2. **Sửa hàm `selectedPeriodsForLesson(lessonId, lessonName = '')`**:
   - Khi `lessonId` được cung cấp:
     - Lấy các tiết theo `lessonId`:
       ```javascript
       const byId = all.filter(x => (x.lessonId === lessonId || x.id.startsWith(lessonId + ':')) && selectedIds.has(x.id)).map(x => x.period);
       return byId;
       ```
     - Nếu `lessonId` đã có, trả về `byId` (dù rỗng cũng trả về rỗng). **Tuyệt đối không** fallback xuống kiểm tra `lessonName` khi `lessonId` đã được cung cấp.

3. **Cải tiến `cleanLessonName` và `lessonKeywords`**:
   - Bổ sung cụm regex loại bỏ `"THỰC HÀNH VÀ TRẢI NGHIỆM"`, `"HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM"`.
   - Trong `lessonKeywords`, bổ sung các từ chung không mang nghĩa phân biệt bài học: `'TRAI'`, `'NGHIEM'`, `'THUC'`, `'HANH'`, `'CHUONG'`, `'HOAT'`, `'DONG'`.
   - Trong `lessonsMatch`: Đối với các bài không có số thứ tự bài (không có `lessonOrdinal`), nếu độ dài từ khóa quá ngắn hoặc chỉ trùng các từ chung thì không được coi là khớp.

4. **Sửa logic đồng bộ Phụ lục 3 (`appendixThreeTable` & `syncIntegrationFromAppendixOne`)**:
   - Khi ghép dòng từ Phụ lục 1 sang Phụ lục 3:
     - Ưu tiên ghép 1-1 theo thứ tự bài học trong danh sách (`rowIndex` / `normal`), hoặc nếu ghép theo tên thì phải đánh dấu dòng Phụ lục 1 đã dùng (`usedPl1Indices.add(pl1Index)`), không cho phép nhiều dòng Phụ lục 3 cùng ăn theo một dòng Phụ lục 1.

5. **Bổ sung danh sách bài NLS vào `getConfig` và `appendixPrompt`**:
   - Trong `getConfig()`: Bổ sung `selectedLessons` và `selectedLessonIds` vào object `nls` (tương tự như `ai.selectedLessons`).
   - Trong `appendixPrompt(no, c)`:
     - Khai báo danh sách bài NLS được chọn:
       `const nlsSelectedText = nlsList.length ? nlsList.map(x => `“${x.lesson}”`).join('; ') : '(không có bài nào)';`
     - Bổ sung chỉ thị ràng buộc AI:
       `NLS TUYỆT ĐỐI chỉ được xuất cho đúng các bài sau: ${nlsSelectedText}. CẤM xuất mã NLS cho bất kỳ bài học nào khác ngoài danh sách này.`

6. **Đồng bộ mã nguồn sang file Canvas**:
   - Cập nhật tương ứng sang `backupcode viettailieu/canvas_xaydungphuluc.html`.
   - Tạo/đồng bộ sang `canvas_xaydungphuluc.html` ở thư mục gốc để đảm bảo các bài test `tests/sgk-knowledge-smoke.js` và `tests/xaydungphuluc-math-smoke.js` chạy thông suốt.

---

## 5. Kế hoạch Kiểm thử & Xác minh (Verification Plan)

Coder thực hiện các kiểm tra sau:

1. **Kiểm tra tự động với smoke test**:
   - Bổ sung test case trong `tests/xaydungphuluc-smoke.js`:
     - Thiết lập cấu hình NLS 28 tiết, AI 12 tiết.
     - Khẳng định bảng Phụ lục 1 và Phụ lục 3 tính ra chính xác 28 tiết NLS và 12 tiết AI, không bị dôi thành 30 tiết NLS hay 14 tiết AI.
     - Khẳng định không bị match chéo giữa các bài "Hoạt động thực hành và trải nghiệm" khác nhau.
   - Chạy các test:
     - `node tests/xaydungphuluc-smoke.js`: PASS.
     - `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
     - `node tests/xaydungphuluc-math-smoke.js`: PASS.
     - `node tests/sgk-knowledge-smoke.js`: PASS.
2. **Ghi chép bàn giao**:
   - Ghi lại toàn bộ nội dung đã sửa và kết quả kiểm thử vào `docs/handoff/IMPLEMENT.md`.

