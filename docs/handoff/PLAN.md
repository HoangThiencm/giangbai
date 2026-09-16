# PLAN: Xóa Thời gian ở Hồ sơ dạy học, Chuẩn hóa Tiết Luyện tập chung / Ôn tập, và Sửa lỗi rỉ thẻ `<br>- GV:` khi xuất Word

## Hiện trạng

1. **Ý 1 - Hồ sơ dạy học bị gắn nhãn thời gian `(4 phút)` trái quy chuẩn sư phạm**:
   - Khi xuất giáo án ra Word hoặc xem toàn bài, ở mục phụ lục xuất hiện dòng:
     `IV. PHỤ LỤC: HỒ SƠ DẠY HỌC (CÁC PHIẾU HỌC TẬP & CÔNG CỤ ĐÁNH GIÁ)`
     `E. HỒ SƠ DẠY HỌC & PHIẾU HỌC TẬP (PHỤ LỤC) (4 phút)`
   - Nguyên nhân trong code:
     + Trong `js/khbd-app.js` (dòng 6432), khi chuẩn hóa tab `E`, code truyền `fourActivities: actKey !== "E"` (`false`), khiến bộ tính toán ngân sách thời lượng `calculateActivityTimeBudgets` lầm tưởng mục E là *"Hoạt động 5: Hướng dẫn về nhà"* của hệ thống cũ và trích ra 4 phút từ tổng 90 phút (hoặc 2 phút từ 45 phút).
     + Tiếp đó, hàm `normalizeActivityTimeHeadings` (dòng 6390) gắn thêm `(4 phút)` vào tiêu đề của E.
     + Theo Công văn 5512/BGDĐT-GDTrH, Hồ sơ dạy học là **Phụ lục học liệu in ấn đính kèm**, hoàn toàn **không tính thời gian/thời lượng**; toàn bộ 45/90 phút phải được dành trọn vẹn 100% cho các hoạt động dạy học trên lớp.
2. **Ý 2 - Chưa có cơ chế chuyên biệt cho tiết "Luyện tập chung", "Ôn tập"**:
   - Hiện tại, khi gặp bài dạy là tiết "Luyện tập chung", "Ôn tập chương" hay "Bài tập cuối chương", hệ thống vẫn sinh theo mẫu bài dạy lý thuyết thông thường (có cả Hoạt động 2: Hình thành kiến thức mới).
   - Điều này dẫn đến việc AI phải tự "bịa" ra kiến thức mới hoặc lặp lại các bài tập vào mục hình thành kiến thức một cách gượng ép, không đúng thực tế bài học SGK (vốn chỉ gồm các bài tập luyện tập).
   - Giáo viên yêu cầu: Tiết Luyện tập chung / Ôn tập phải có cấu trúc chuẩn mực: **Có Khởi động (Trò chơi ngắn 3–5 phút nhắc lại công thức/quy tắc) → Bỏ Hình thành kiến thức mới → Trọng tâm Luyện tập (chiếm 75–80% thời lượng) → Vận dụng**.
3. **Ý 3 - Xuất Word bị lỗi chèn thẻ thô: `*(Nhận xét của <br>- GV: ....................)*`**:
   - Nguyên nhân kép:
     + **Nguyên nhân 1 (Chèn sai chuỗi):** Hàm `formatKhbdRoleLine` trong `js/khbd-app.js` (dòng 2301) và `canvas_soankhbd.html` (dòng 1421) sử dụng regex `/(?:\*\*)?(GV|HS)\s*:(?:\*\*)?/gi` quá tham lam, tự động bắt gặp chữ `GV:` ở bất kỳ đâu, kể cả trong cụm từ `Nhận xét của GV:` trên mẫu phiếu học tập, rồi chèn chuỗi `<br>- ` vào giữa biến thành `Nhận xét của <br>- **GV:**`. Hàm này lại được gọi bừa bãi lên toàn bộ bài dạy thay vì chỉ áp dụng cho kịch bản phân vai trong bảng 2 cột.
     + **Nguyên nhân 2 (Xuất Word in thẻ HTML thô):** Trong `js/khbd-docx.js`, hàm `parseInlineTextToRuns` đối với các đoạn văn bản bình thường ngoài bảng không xử lý thẻ HTML `<br>`, khiến chuỗi `<br>` bị in nguyên văn thành chữ thô ra file Word `.docx`.

---

## Phạm vi

1. **Xóa bỏ hoàn toàn thời gian ở Hồ sơ dạy học (Mục IV / Phụ lục E)**:
   - Trong `js/khbd-app.js`, bỏ lệnh gán phút cho `headingRe.E` trong `normalizeActivityTimeHeadings`.
   - Bổ sung bộ lọc regex xóa triệt để mọi hậu tố thời lượng như `(X phút)`, `(khoảng X phút)` nếu vô tình xuất hiện ở tiêu đề Phụ lục / Hồ sơ dạy học / Phiếu học tập.
   - Sửa `clipKhbdActivityMarkdown` luôn truyền `fourActivities: true` để toàn bộ thời lượng bài dạy (45p / 90p) được bảo toàn 100% cho các hoạt động trên lớp (A, B, C, D), trả lại số phút bị mất cho các hoạt động học tập.
   - Trong `js/khbd-docx.js` và `js/khbd-app.js`, chuẩn hóa việc xuất phụ lục IV: chỉ giữ tiêu đề chuẩn `IV. PHỤ LỤC: HỒ SƠ DẠY HỌC (CÁC PHIẾU HỌC TẬP & CÔNG CỤ ĐÁNH GIÁ)`, không lặp lại dòng tiêu đề thừa `E. HỒ SƠ DẠY HỌC...` có dính số phút.
2. **Chuẩn hóa cấu trúc tiến trình cho tiết "Luyện tập chung", "Ôn tập"**:
   - Viết hàm nhận diện loại bài `isPracticeOrReviewLesson(topic)` trong `js/khbd-prompts.js` và `js/khbd-app.js`:
     + Nhận diện các từ khóa: `luyện tập chung`, `luyện tập`, `ôn tập`, `bài tập cuối chương`.
   - Tinh chỉnh Prompt và tiến trình dạy học cho loại bài này:
     + **Hoạt động 1 (Khởi động):** Thiết kế trò chơi ngắn (3–5 phút) như Trò chơi ô chữ, Vòng quay may mắn, Đố vui công thức, Khởi động nhanh để vừa tạo hứng thú, vừa tái hiện/nhắc lại các quy tắc, công thức toán học trọng tâm cần dùng trong tiết luyện tập.
     + **Bỏ hoạt động "Hình thành kiến thức mới" (Pha B):** Không sinh hoạt động lý thuyết mới. Toàn bộ thời lượng của Pha B được dồn vào Pha C (Luyện tập). Nếu người dùng bấm tạo ở tab B hoặc tạo 1-click, hệ thống xuất bảng tóm tắt/sơ đồ hệ thống hóa kiến thức ngắn gọn hoặc chuyển tiếp mượt mà sang luyện tập bài tập.
     + **Hoạt động 2 (Luyện tập - Trọng tâm):** Chiếm ~75–80% tổng thời lượng tiết học. Phân dạng bài tập cụ thể bám sát SGK (Dạng 1: Rèn luyện kỹ năng cơ bản; Dạng 2: Vận dụng giải toán / bài toán thực tế); kịch bản phân vai GV - HS đầy đủ 4 bước (Chuyển giao, Thực hiện - có dự kiến lời giải & lỗi sai của HS, Báo cáo đối thoại, Kết luận chốt phương pháp giải).
     + **Hoạt động 3 (Vận dụng):** Bài tập thực tế mở rộng, củng cố và hướng dẫn học sinh tự học ở nhà.
3. **Khắc phục triệt để lỗi rỉ thẻ `<br>- GV:` và in thẻ HTML thô ra Word**:
   - Tinh chỉnh regex trong `formatKhbdRoleLine` (`js/khbd-app.js`, `canvas_soankhbd.html`): Chỉ định dạng khi là đầu lượt lời (đầu dòng, sau `- `, hoặc sau dấu kết thúc câu); **tuyệt đối loại trừ khi phía trước là `Nhận xét của `, `Đánh giá của `, `Ý kiến của `, `Chữ ký của ` hoặc từ `của `**.
   - Không chạy `formatKhbdRoleLineBreaks` lên phần Phụ lục E (Phiếu học tập / Hồ sơ dạy học).
   - Trong `js/khbd-docx.js`:
     + Trước khi chuyển đổi sang Word elements, thay thế toàn bộ `<br\s*\/?>` thành ký tự xuống dòng `\n` hoặc xử lý tạo `TextRun({ break: 1 })`.
     + Đảm bảo không bao giờ xuất hiện chuỗi `<br>` trần trụi trong file Word.
4. **Cập nhật và bổ sung bài kiểm tra tự động**:
   - Cập nhật bài kiểm tra trong `tests/` để xác nhận:
     + Tiêu đề Hồ sơ dạy học không bao giờ chứa `(\d+ phút)`.
     + Cụm từ `*(Nhận xét của GV: ...)*` giữ nguyên vẹn, không bị chèn `<br>- ` hay in thẻ `<br>`.
     + Tiết Luyện tập chung được nhận diện chính xác và phân bổ thời lượng hợp lý.

---

## Ngoài phạm vi

- Không thay đổi cấu trúc bảng 2 cột 1 hàng chuẩn của CV 5512.
- Không can thiệp vào các bài dạy lý thuyết thông thường (vẫn giữ đủ 4 bước A, B, C, D).

---

## File dự kiến tác động

1. `js/khbd-app.js`
2. `js/khbd-docx.js`
3. `js/khbd-prompts.js`
4. `canvas_soankhbd.html`
5. `backupcode viettailieu/canvas_soankhbd.html`
6. `tests/khbd-activity-e-smoke.js`
7. `tests/khbd-time-budgets-smoke.js`
8. `tests/khbd-pedagogy-rate-smoke.js`

---

## Các bước thực hiện chi tiết cho Coder

### Bước 1: Xóa bỏ thời gian ở Hồ sơ dạy học trong `js/khbd-app.js` và `js/khbd-docx.js`
- Trong `js/khbd-app.js`:
  + Tại dòng 6390 (`normalizeActivityTimeHeadings`): Xóa bỏ dòng `if (headingRe.E.test(trimmed)) return replaceHeadingMinutes(line, budgets.E);`. Thay vào đó, nếu dòng trùng khớp với `headingRe.E`, tự động loại bỏ mọi chuỗi dạng `\(\s*\d+\s*phút\s*\)` nếu có.
  + Tại dòng 6432 (`clipKhbdActivityMarkdown`): Đổi `{ fourActivities: actKey !== "E", ... }` thành `{ fourActivities: true, ... }` để `budgets.E` luôn bằng `0` và thời gian được dồn trọn vẹn cho A, B, C, D.
  + Tại hàm xuất toàn bài `getFullLessonPlanMarkdown`: Làm sạch phần đầu của `appendixE`, bỏ tiêu đề con `# E. HỒ SƠ DẠY HỌC...` lặp lại ngay dưới tiêu đề Phụ lục `# IV. PHỤ LỤC: HỒ SƠ DẠY HỌC...`.
- Trong `js/khbd-docx.js`:
  + Kiểm tra trước khi nối `appendixE` vào `markdown`: Loại bỏ dòng tiêu đề lặp lại và xóa triệt để `(\d+ phút)` khỏi phần phụ lục.

### Bước 2: Sửa lỗi chèn `<br>- GV:` và xử lý thẻ `<br>` khi xuất Word
- Trong `js/khbd-app.js` (dòng 2301) và `canvas_soankhbd.html` (dòng 1421):
  + Sửa regex thay thế vai trò:
    ```javascript
    // Không thay thế nếu phía trước là "của", "Nhận xét của", "Ý kiến của", v.v.
    content = content.replace(/(?<!(?:nhận\s*xét|đánh\s*giá|ý\s*kiến|chữ\s*ký)?\s*của\s+)(?:\*\*)?(GV|HS)\s*:(?:\*\*)?/gi, (_, role) => `§BR§§${role.toUpperCase()}§`);
    ```
  + Trong hàm `getFullLessonPlanMarkdown`: Không chạy `formatKhbdRoleLineBreaks` lên `appendixE`.
- Trong `js/khbd-docx.js`:
  + Trong `parseInlineTextToRuns`: Trước khi tách regex, nếu text chứa `<br>`, tách theo `<br\s*\/?>` và sinh `TextRun({ break: 1 })` thay vì để nguyên chuỗi `<br>`.
  + Đảm bảo làm sạch mọi thẻ `<br>` trần trong các đoạn văn bản thường trước khi sinh file Word.

### Bước 3: Bổ sung bộ nhận diện loại bài học trong `js/khbd-prompts.js`
- Định nghĩa hàm nhận diện bài Luyện tập / Ôn tập:
  ```javascript
  function isPracticeOrReviewLesson(topic) {
    return /luyện\s*tập\s*chung|ôn\s*tập|bài\s*tập\s*cuối\s*chương|luyện\s*tập\b/i.test(String(topic || ""));
  }
  ```
- Trong `calculateActivityTimeBudgets`:
  + Khi `isPracticeOrReviewLesson(durationStr, topic)` được bật:
    - `timeA = clamp(3, 5, Math.round(T * 0.1));` (Khởi động trò chơi 3–5 phút).
    - `timeB = 0;` (Không có hình thành kiến thức mới).
    - `timeD = clamp(5, 10, Math.round(T * 0.12));` (Vận dụng 5–10 phút).
    - `timeC = T - timeA - timeD;` (Toàn bộ phần còn lại ~75–80% dành cho Luyện tập).

### Bước 4: Cấu hình Prompt chuyên biệt cho tiết Luyện tập chung / Ôn tập
- Trong `js/khbd-prompts.js`:
  + Bổ sung chỉ dẫn vào `GENERATE_ACTIVITY_A` khi là tiết Luyện tập / Ôn tập:
    "ĐÂY LÀ TIẾT LUYỆN TẬP CHUNG / ÔN TẬP: Tổ chức Khởi động dưới hình thức TRÒ CHƠI HỌC TẬP NGẮN (3–5 phút) như Trò chơi ô chữ, Vòng quay may mắn, Đố vui công thức để kích hoạt không khí và tái hiện/nhắc lại nhanh các quy tắc, công thức then chốt đã học."
  + Trong `GENERATE_ACTIVITY_B` khi là tiết Luyện tập / Ôn tập: Tự động chuyển thành "Hệ thống hóa kiến thức & Phương pháp giải toán" (sơ đồ tư duy / bảng tóm tắt công thức tinh gọn) hoặc hướng dẫn giáo viên chuyển trọng tâm sang Hoạt động Luyện tập C.
  + Trong `GENERATE_ACTIVITY_C`: Mở rộng phạm vi chọn lọc 2–4 bài tập SGK/SBT chia theo các dạng toán rõ ràng để học sinh luyện tập tối đa.

### Bước 5: Kiểm thử và cập nhật test suite
- Cập nhật test `tests/khbd-activity-e-smoke.js`: Khẳng định `assert.doesNotMatch(outputE, /\(\s*\d+\s*phút\s*\)/)` và `assert.doesNotMatch(outputE, /<br>\s*-\s*GV:/)`.
- Cập nhật test `tests/khbd-pedagogy-rate-smoke.js`: Đảm bảo `formatKhbdRoleLineBreaks` không làm hỏng chuỗi `Nhận xét của GV:`.
- Chạy toàn bộ các test liên quan để đảm bảo PASS 100%.

---

## Rủi ro & Giải pháp

- **Rủi ro ảnh hưởng đến kịch bản phân vai trong bảng**:
  -> **Giải pháp**: Chỉ chặn thay thế khi phía trước có từ sở hữu `"của"`. Các mẫu `GV: "..."` và `HS: "..."` thông thường trong kịch bản vẫn ngắt dòng mượt mà.
- **Rủi ro phụ lục E bị rỗng nếu cắt bỏ tiêu đề**:
  -> **Giải pháp**: Chỉ loại bỏ phần tiêu đề trùng lặp `E. HỒ SƠ DẠY HỌC... (4 phút)`, giữ nguyên vẹn toàn bộ nội dung Phiếu học tập số 1, số 2, Rubric đánh giá bên dưới.

---

## Cách kiểm thử

1. Chạy test tĩnh bằng Node.js:
   `node tests/khbd-activity-e-smoke.js`
   `node tests/khbd-time-budgets-smoke.js`
   `node tests/khbd-pedagogy-rate-smoke.js`
2. Kiểm tra xuất Word trên giao diện:
   - Tạo bài dạy có phiếu học tập, xuất file Word (.docx).
   - Kiểm tra dòng nhận xét của giáo viên: Hiển thị chuẩn `*(Nhận xét của GV: ....................)*`, hoàn toàn không có `<br>- ` hay thẻ HTML thô.
   - Kiểm tra mục `IV. PHỤ LỤC`: Tuyệt đối không còn dòng chữ `(4 phút)` hay bất kỳ số phút nào.
3. Kiểm tra bài "Luyện tập chung":
   - Nhập tên bài: "Luyện tập chung (trang 25)", tạo hoạt động A và C: Hoạt động A sinh trò chơi nhắc lại công thức, Hoạt động C chiếm trọn thời lượng với các dạng bài tập chi tiết.

---

## Tiêu chí nghiệm thu

1. Mục Phụ lục / Hồ sơ dạy học khi xuất ra Word (.docx) hoặc Markdown toàn bài **100% không còn gắn thời gian `(X phút)`**.
2. Toàn bộ thời lượng bài dạy (45 phút / 90 phút) được bảo toàn nguyên vẹn cho các hoạt động dạy học trên lớp.
3. Khi soạn tiết "Luyện tập chung" hoặc "Ôn tập":
   - Hoạt động 1 là Trò chơi ngắn tái hiện công thức/kiến thức cũ.
   - Không sinh gượng ép hoạt động "Hình thành kiến thức mới".
   - Hoạt động Luyện tập chiếm đa số thời lượng (~75–80%).
4. Triệt tiêu hoàn toàn lỗi chèn `<br>- GV:` vào `Nhận xét của GV:`; file Word xuất ra không chứa thẻ `<br>` thô.
5. Toàn bộ bài kiểm thử tự động đạt PASS 100%.



