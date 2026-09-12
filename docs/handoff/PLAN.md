# PLAN: Khắc phục lỗi Gợi ý tích hợp & Thẩm định NLS chưa đạt & Nâng cấp Canvas mở rộng

## PHẦN A: Khắc phục triệt để lỗi gợi ý cả NLS và AI trên bài 1 tiết & Thẩm định NLS chưa đạt (22/140 tiết)

### 1. Hiện trạng & Nguyên nhân gốc rễ (Root Cause)
- **Hiện tượng người dùng phản ánh qua ảnh chụp**:
  1. Trong bảng chọn bài học (Mục 1 / `aiPickerRows`), các **bài 1 tiết** (ví dụ: *Bài 1. Tập hợp*, *Bài 2. Cách ghi số tự nhiên*, *Bài 3. Thứ tự trong tập hợp*, *Bài 4. Phép cộng và phép trừ*) đang bị hệ thống gợi ý **tích chọn cả hai cột**:
     - Cột *Tích hợp NLS*: `[x] Tích hợp NLS` (được tích).
     - Cột *Tích hợp AI*: `[x] Cả bài` / `[x] Tiết 1` (cũng được tích).
  2. Sự mâu thuẫn này dẫn trực tiếp đến lỗi Thẩm định:
     - Giao diện Mục 1 đếm đủ **28 tiết NLS** (do đếm theo checkbox đã tích).
     - Nhưng khi render bảng Phụ lục 1, hàm `selectedIntegration` áp dụng đúng quy tắc sư phạm đã thống nhất:
       `Bài 1 tiết có AI → 0 mã NLS, chỉ có 1 mã AI` (`if (p <= 1) return hasAi ? 0 : 1;`).
     - Vì vậy, 6 bài 1 tiết có AI này bị **xóa mã NLS** trong bảng Phụ lục 1, thực tế chỉ còn **22 tiết NLS** (13 bài).
     - Báo cáo Thẩm định (`calculateComplianceReport`) đếm các dòng thực tế có mã NLS trong bảng Phụ lục 1 thì chỉ thấy **22/140 tiết (mục tiêu 28 tiết)** -> Báo **Chưa đạt**!

- **Nguyên nhân kỹ thuật**:
  1. Thuật toán tự động gợi ý chọn bài NLS (`chooseNlsLessonsForPeriods` / `syncNlsSelectionFromRate`) và AI (`prioritizedAiPeriods` / `syncAiSelectionFromRate`) đang chạy **hoàn toàn độc lập**. Khi người dùng kéo thanh tỉ lệ (hoặc mở trang mẫu), cả hai hàm cùng ưu tiên các bài học đầu tiên (các bài 1 tiết của Chương I) mà không có cơ chế **loại trừ lẫn nhau (mutual exclusion)** đối với bài 1 tiết.
  2. Các hàm tương tác checkbox (`toggleNlsLesson`, `toggleAiLesson`, `toggleAiLessonRow`) chưa có logic ràng buộc loại trừ cho bài 1 tiết: khi người dùng hoặc hệ thống tích chọn AI cho bài 1 tiết thì chưa tự động hủy chọn NLS của bài đó, và ngược lại.

---

### 2. Giải pháp kỹ thuật khắc phục triệt để
Áp dụng trên cả 2 tệp: `canvas_xaydungphuluc.html` và `xaydungphuluc.html`:

1. **Nguyên tắc loại trừ lẫn nhau (Mutual Exclusion) cho bài 1 tiết khi gợi ý tự động**:
   - Khi gợi ý NLS (`chooseNlsLessonsForPeriods` / `syncNlsSelectionFromRate`):
     - Duyệt danh sách bài học ưu tiên, nếu gặp bài 1 tiết mà **đã được chọn tiết AI** (`selectedPeriodsForLesson(lesson.id).length > 0`) -> **Bỏ qua không chọn NLS cho bài đó**, tiếp tục chọn các bài khác (bài từ 2 tiết trở lên, hoặc bài 1 tiết chưa có AI) cho đến khi đạt đủ mục tiêu `target` số tiết NLS (đủ 28 tiết).
   - Khi gợi ý AI (`prioritizedAiPeriods` / `syncAiSelectionFromRate`):
     - Nếu bài 1 tiết đã được chọn NLS -> không tự động chọn AI cho bài đó (ưu tiên bài từ 2 tiết hoặc bài 1 tiết chưa có NLS).

2. **Ràng buộc loại trừ tức thì trên giao diện (Interactive Checkboxes)**:
   - Trong `toggleNlsLesson(lessonId, checked)`:
     - Nếu `checked = true` và bài đó là bài 1 tiết: Tự động bỏ chọn tất cả tiết AI của bài đó trong `aiSelectedLessonIds` (`toggleAiLessonRow(lessonId, false)`).
   - Trong `toggleAiLesson(periodId, checked)` và `toggleAiLessonRow(lessonId, checked)`:
     - Nếu `checked = true` và bài đó là bài 1 tiết: Tự động bỏ chọn NLS của bài đó trong `nlsSelectedLessonIds` (`nlsSelectedLessonIds.delete(lessonId)`).
   - Cập nhật lại thanh trượt tỉ lệ và số lượng hiển thị tức thì.

3. **Kết quả đạt được**:
   - Trên bảng giao diện Mục 1: **Tuyệt đối không có bài 1 tiết nào bị tích cả NLS lẫn AI**.
   - Mục tiêu 28 tiết NLS sẽ được phân bổ chính xác vào 28 tiết thực tế (các bài >= 2 tiết hoặc bài 1 tiết không có AI).
   - Bảng Phụ lục 1 xuất ra đủ đúng 28 tiết có mã NLS.
   - Báo cáo Thẩm định Sư phạm đếm đúng **28/140 tiết (Đạt 100%)**.

---

## PHẦN B: Nâng cấp các công cụ trong "backupcode viettailieu" chạy môi trường Gemini Canvas mở rộng

### 1. Mục tiêu
- **Tối ưu hiển thị mở rộng (Full-width / Expanded Canvas Mode)**: Tự động co giãn phủ rộng toàn màn hình (`w-full max-w-[98%] 2xl:max-w-[1750px] mx-auto`), không bị đóng khung hẹp cố định (`max-w-7xl` ~ 1280px hay `1440px`), tận dụng tối đa không gian khi người dùng nhấn nút mở rộng/toàn màn hình trong Gemini Canvas.
- **Tương thích tuyệt đối Sandbox Iframe của Gemini Canvas**:
  - Chống FOUC / màn hình trắng (Force visible styles & MutationObserver).
  - An toàn CSP: Tránh lỗi chặn Worker (PDF.js worker), tránh chặn popup (`window.confirm`/`alert`).
  - Hộp thoại tương tác DOM (`canvasConfirm`) thay cho `confirm()` vốn bị browser sandbox chặn.
  - Lưu trữ an toàn (`canvasStorage`) có bộ nhớ tạm in-memory khi `localStorage` bị hạn chế quyền truy cập.
  - Banner trạng thái kết nối Gemini Canvas (`canvasHostBanner`).
  - Nút chuyển giao diện "Gọn" (`toggleCompactMode`) để xem được nhiều nội dung hơn trên màn hình Canvas.

### 2. Danh mục tệp tin & Nội dung triển khai
1. `canvas_xaydungphuluc.html` & `xaydungphuluc.html`: Áp dụng bản vá Phần A (chọn bài NLS bù trừ thông minh chống hụt tiết).
2. `backupcode viettailieu/canvas_soankhbd.html`: Mở rộng layout `.app-body`, bổ sung `canvasConfirm` và xử lý an toàn sandbox.
3. `backupcode viettailieu/soanbaigemini.html`: Mở rộng layout `max-w-[98%]`, thêm banner canvas, anti-FOUC, `canvasConfirm`, `canvasStorage`.
4. `backupcode viettailieu/taobaitap.html`: Mở rộng layout 2 khối chính, thêm banner canvas, anti-FOUC.
5. `backupcode viettailieu/taobaocao.html`: Thêm banner canvas, mở rộng layout, anti-FOUC.
6. `backupcode viettailieu/sangkien.html`: Mở rộng layout container chính sang `max-w-[98%]`, thêm banner canvas, anti-FOUC.
7. `backupcode viettailieu/chuyenpdf.html`: Mở rộng `.app-shell` sang `max-w-[98%] 2xl:max-w-[1750px]`, thêm banner canvas, anti-FOUC.
## PHẦN C: Khung mã hoá Sư phạm Tổng quát cho toàn bộ ứng dụng (NLS & AI cho mọi môn học và khối lớp)

### 1. Hiện trạng & Định hướng Kiến trúc Tổng quát
- **Vấn đề cốt lõi người dùng chỉ ra**:
  *"vấn đề là chúng ta phải để cho nó mã hoá thực sự hợp lý ở tất cả các nội dung cần mã hoá chứ không phải 1 hay 2 mã cụ thể, cái chúng ta viết là tổng quát cho ứng dụng"*.
  - Ứng dụng không chỉ dành riêng cho 1 bài Toán cụ thể hay 1 mã riêng lẻ, mà là công cụ tổng quát phục vụ **tất cả các môn học** (Toán, KHTN, Ngữ văn, Lịch sử - Địa lí, Ngoại ngữ, Tin học, GDCD, Công nghệ...) và **tất cả các khối lớp** (6, 7, 8, 9).
  - Lỗi sinh câu mô tả gượng ép, phi lý (như *"AI mô phỏng bánh răng để minh họa BCNN"*) là triệu chứng của việc **thiếu một cơ chế phân loại sư phạm tổng quát** giữa bản chất môn học và mục tiêu của từng Miền năng lực.

---

### 2. Khung quy tắc Sư phạm Tổng quát (Universal Pedagogical Framework)

#### A. Phân định Miền Năng lực AI (QĐ 2422) theo Bản chất Nhóm môn học:
1. **Nhóm môn Công nghệ & Tin học**:
   - Học sinh học trực tiếp về nguyên lý, máy học, lập trình và cấu trúc dữ liệu AI.
   - Được phép sử dụng cả 4 Miền: **Miền A (Hiểu biết AI)**, **Miền B (Ứng dụng)**, **Miền C (Sáng tạo giải pháp)**, **Miền D (Đạo đức & Tác động)**.
2. **Nhóm tất cả các môn học còn lại (Toán, KHTN, Ngữ văn, Lịch sử - Địa lí, Ngoại ngữ, GDCD...)**:
   - Học sinh tiếp cận AI với vai trò là **Trợ lý học tập thông minh (Smart Learning Assistant)** phục vụ môn học đó, KHÔNG học về kỹ thuật/lập trình AI.
   - **Quy tắc phân bổ mã bắt buộc**:
     - **Miền B (Ứng dụng AI - mã `[6-9].B2.x`)**: Dùng trợ lý AI hỗ trợ gợi mở cách tiếp cận, tìm kiếm thông tin, gợi ý các bước giải quyết nhiệm vụ bài học.
     - **Miền D (Đạo đức, Liêm chính & Kiểm chứng - mã `[6-9].D1.x`)**: Đánh giá độ tin cậy của thông tin do AI cung cấp, đối chiếu với SGK, phát hiện sai sót/thiên vị, rèn luyện liêm chính học thuật và tự chịu trách nhiệm về sản phẩm học tập.
     - **Miền C (Sáng tạo cùng AI - mã `[6-9].C...`)**: Dành riêng cho các bài dự án học tập, thực hành trải nghiệm, STEM.
     - **CẤM TUYỆT ĐỐI gán mã Miền A** (`[6-9].A...` - Giải thích con người lập trình AI, máy học, nguyên lý kỹ thuật) vào các bài học của nhóm môn này.

#### B. Phân bổ Năng lực Số (CV 3456 / TT 02/2024) gắn liền Công cụ thực tế của môn học:
- **Nguyên tắc**: Biểu hiện NLS phải nêu đích danh công cụ số thực tế mà học sinh thao tác trong giờ học của môn đó:
  - **Môn Toán**: Máy tính cầm tay (tính toán, kiểm tra nghiệm, phím chức năng), phần mềm GeoGebra/Desmos (vẽ đồ thị, dựng hình động), bảng tính Excel (xử lý dữ liệu thống kê).
  - **Môn KHTN (Lý - Hóa - Sinh)**: Video mô phỏng thí nghiệm ảo, mô hình 3D tương tác cấu tạo phân tử/tế bào, cảm biến số hoặc bảng số liệu đo đạc thực nghiệm.
  - **Môn KHXH (Ngữ văn, Lịch sử - Địa lí, GDCD)**: Bản đồ số (Google Earth/bản đồ tương tác), bảo tàng ảo/tư liệu số lịch sử, phần mềm sơ đồ tư duy (Canva/Mindmap) để tóm tắt và báo cáo sản phẩm.
  - **Môn Ngoại ngữ**: Từ điển số, phần mềm phát âm, công cụ luyện nghe nói tương tác.

#### C. Công thức Sư phạm 3 thành phần chuẩn mực cho câu mô tả (Áp dụng toàn hệ thống):
Mọi câu mô tả NLS và AI (dù do Gemini sinh hay hàm fallback sinh) đều bắt buộc tuân theo cấu trúc 3 thành phần:
```text
[Công cụ số / Trợ lý AI cụ thể] + [Hành động học tập cụ thể gắn với nội dung bài học] + [Kiểm chứng đối chiếu / Trách nhiệm / Sản phẩm của học sinh]
```
- **Ví dụ NLS**:
  - *Toán học*: `[NLS: 5.3.TC1a - Sử dụng máy tính cầm tay để thực hiện các phép tính và kiểm tra kết quả bài [Tên bài].]`
  - *KHTN*: `[NLS: 1.1.TC1a - Khai thác video thí nghiệm mô phỏng để quan sát hiện tượng và tìm hiểu nội dung bài [Tên bài].]`
  - *Ngữ văn / Lịch sử*: `[NLS: 3.1.TC1a - Sử dụng công cụ số (sơ đồ tư duy / bài trình chiếu) để hệ thống hóa kiến thức và trình bày sản phẩm bài [Tên bài].]`
- **Ví dụ AI (Miền B - Ứng dụng)**:
  - `[AI: [Mã].B2.1 - Sử dụng trợ lý AI gợi mở cách tiếp cận, gợi ý các bước thực hiện nhiệm vụ bài [Tên bài]; học sinh tự đối chiếu với SGK để kiểm chứng và hoàn thành bài tập.] (Áp dụng: tiết X, Y).`
- **Ví dụ AI (Miền D - Kiểm chứng & Trách nhiệm)**:
  - `[AI: [Mã].D1.1 - Đánh giá tính chính xác và độ tin cậy của thông tin do AI gợi ý về bài [Tên bài]; đối chiếu với SGK và tự chịu trách nhiệm về kết quả học tập.] (Áp dụng: tiết X, Y).`

---

### 3. Kế hoạch Triển khai Kỹ thuật Tổng quát
Áp dụng trên toàn bộ hệ thống: `js/khbd-standards.js`, `canvas_xaydungphuluc.html`, `xaydungphuluc.html`:

1. **Nâng cấp bộ lọc `isUnnaturalOfficialStandard` trong `js/khbd-standards.js`**:
   - Tự động nhận diện môn học: Nếu `kind === "ai"` và môn học không phải là "Tin học" (`!/tin hoc|cong nghe thong tin|lap trinh/i.test(ctx.subjectName)`), mọi mã thuộc Miền A (`/^\d+\.A/i.test(code)`) đều bị đánh dấu `unnatural = true` (không gán cho bài học).
   - Nhờ đó, thuật toán đề xuất mã AI của mọi môn học sẽ luôn tự động chọn đúng các mã **Miền B (`[g].B2.1`)** và **Miền D (`[g].D1.1`)** cho mọi khối lớp 6, 7, 8, 9.
2. **Nâng cấp hàm Fallback `lessonAppliedAiDescription` và `lessonAppliedNlsDescription`**:
   - Xây dựng ma trận bộ môn tổng quát (Toán học, KHTN, Khoa học xã hội, Ngữ văn, Ngoại ngữ, Tin học...).
   - Tự động sinh mô tả theo đúng công thức 3 thành phần chuẩn mực theo đặc thù môn học và khối lớp, loại bỏ hoàn toàn các câu văn cứng nhắc hoặc gượng ép.
3. **Nâng cấp Chỉ dẫn Sư phạm trong Prompt Gemini (`appendixPrompt`)**:
   - Quy định rõ ràng trong prompt nguyên tắc phân môn: Với các môn học khác ngoài Tin học, mã AI bắt buộc đóng vai trò trợ lý hỗ trợ học tập (Miền B) và đối chiếu kiểm chứng (Miền D).
   - Cấm tuyệt đối Gemini tự chế các ngữ cảnh phi thực tế, gượng ép (như "mô phỏng chuyển động bánh răng", "tìm hiểu lịch sử chatbot"). Mọi mô tả phải bám sát nội dung bài học và năng lực thực hành của học sinh.

---

## 4. Kế hoạch kiểm thử (Verification Plan)

1. **Kiểm thử Thẩm định NLS (Phần A)**:
   - Chạy mô phỏng kiểm thử với cấu hình 140 tiết, 20% NLS (28 tiết), 9% AI (12 tiết).
   - Xác nhận bảng Phụ lục 1 xuất ra đủ 28 tiết có mã NLS, không bị hụt 6 tiết.
   - Xác nhận `calculateComplianceReport` trả về `pass: true` cho tiêu chí Năng lực số.
2. **Kiểm thử Canvas mở rộng (Phần B)**:
   - Tạo và chạy `tests/backupcode-canvas-smoke.js` kiểm tra toàn bộ 6 tệp trong `backupcode viettailieu`: cú pháp hợp lệ, container mở rộng, anti-FOUC và banner canvas.
3. **Hồi quy hệ thống**:
   - `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
   - `node tests/xaydungphuluc-smoke.js`: PASS.
   - `node tests/xaydungphuluc-math-smoke.js`: PASS.
   - `node tests/sgk-knowledge-smoke.js`: PASS.

