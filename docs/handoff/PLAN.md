# PLAN: Rà Soát Toàn Diện & Khôi Phục Hoàn Toàn Chất Lượng Soạn Giáo Án (Mục B & Toàn Bài) Chuẩn CV 5512

## Bối cảnh & Kết quả Rà soát So sánh với "Hôm trước"

### 1. Tại sao "Hôm trước soạn rất tốt, ok lắm luôn"?
- Trước commit `deecc0d` (tại commit `7bc94fc`):
  + Hàm `clipKhbdActivityMarkdown` và `applyActivityOutput` **hoàn toàn KHÔNG CÓ** các hàm can thiệp thô bạo như `ensureActivityFourPartStructure` và `repairActivityTablesRightColumn`.
  + Trí tuệ nhân tạo (Gemini) được điều phối trực tiếp bởi `PROMPTS.GENERATE_ACTIVITY_B` và `expandActivityBSkeleton`.
  + Từng nhánh con `Hoạt động 2.1`, `Hoạt động 2.2`... sinh ra nguyên bản cực kỳ chuẩn mực:
    * `### Hoạt động 2.1: [Tên đề mục SGK] (... phút)`
    * `#### a) Mục tiêu:` (mục tiêu kiến thức cụ thể của tiểu mục)
    * `#### b) Nội dung:` (nhiệm vụ học sinh nghiên cứu SGK, làm hoạt động khám phá)
    * `#### c) Sản phẩm:` (kết quả câu trả lời, lời giải bài tập ví dụ mẫu)
    * `#### d) Tổ chức thực hiện:`
    * Bảng 2 cột liền mạch: Cột 1 gồm trọn vẹn kịch bản 4 bước (`+ Bước 1: Chuyển giao nhiệm vụ`, `+ Bước 2: Thực hiện nhiệm vụ`, `+ Bước 3: Báo cáo, thảo luận`, `+ Bước 4: Kết luận, nhận định`); Cột 2 là toàn bộ kiến thức ghi bảng chuẩn mực (định nghĩa, công thức LaTeX `$x^2 - 1$`, ví dụ mẫu có đề và lời giải).
  + Khi xuất file Word hoặc xem trước HTML: Các công thức toán học sắc nét, không bị gãy LaTeX, không bị trùng lặp nhãn `- - GV:`, không bị đứt câu hay dồn cục.

### 2. Nguyên nhân phát sinh lỗi khiến "Nó chạy sai tè le, mất mục tiêu, thiếu 4 bước"
Commit `deecc0d` nhằm sửa lỗi nhảy cóc ở Hoạt động 4 (Vận dụng), nhưng đã đưa vào 2 cơ chế gây lỗi nghiêm trọng:

1. **`repairActivityBlockFourParts` trong `js/khbd-app.js`**:
   - Hàm này áp dụng tràn sang cả Mục B (chia tách từng nhánh 2.1, 2.2 rồi chạy repair).
   - **Mất `a) Mục tiêu:`**: Hàm chỉ tìm regex `Mục tiêu:` để đổi thành `#### a) Mục tiêu:`. Nếu AI không sinh sẵn từ khóa này, hàm **hoàn toàn KHÔNG tạo mục `a)`**, dẫn đến Hoạt động 2.1 nhảy cóc thẳng vào `b) Nội dung:`.
   - **Vỡ LaTeX và đứt cụt chữ ở `b)` và `c)`**:
     * Khi thấy thiếu `hasB`, hàm lấy `step1` của bảng, xóa `<br>`, cắt `.slice(0, 400)` nhét vào `b) Nội dung:`. Lời thoại GV/HS của Bước 1 bị lôi lên trên, qua bộ định dạng `formatKhbdRoleLineBreaks` bị chèn thêm gạch đầu dòng biến thành `- - GV: ... - - HS: ...`, công thức LaTeX bị cắt ngang lưng thành `$-5x^2y; $x^3 - \frac{1` gây lỗi cú pháp nghiêm trọng!
     * Khi thấy thiếu `hasC`, hàm lấy Cột 2 (ghi bảng), xóa `<br>`, cắt `.slice(0, 400)` nhét vào `c) Sản phẩm:`. Toàn bộ đề mục, định nghĩa bị dồn thành 1 dòng đơn điệu và đứt cụt chữ ở cuối (`- Bậc của đơn thức (c`).
   - **Phá nát bảng và làm "thiếu 4 bước"**: Bước 1 bị bóc trích đẩy lên trên, bảng `d)` phía dưới lại lặp lại Bước 1; các bước 2, 3, 4 bị che khuất hoặc bị hiểu lầm là khuyết thiếu.
   - **Chạy lặp 2 lần**: Trong `applyActivityOutput` chạy `ensureActivityFourPartStructure` 1 lần, rồi truyền vào `clipKhbdActivityMarkdown` lại chạy thêm 1 lần nữa!

2. **Lỗ hổng trong `ACTIVITY_TABLE_CONTRACT_COMPACT` (`js/khbd-prompts.js`)**:
   - Khi người dùng chọn chế độ Soạn rút gọn (4–6 trang), `ACTIVITY_TABLE_CONTRACT` bị thay thế bằng `ACTIVITY_TABLE_CONTRACT_COMPACT`.
   - Khung compact này **hoàn toàn không nhắc AI** sinh 4 mục `a), b), c), d)`, và cũng không đưa ra tên chuẩn của 4 bước (`+ Bước 1: Chuyển giao nhiệm vụ`, `+ Bước 2: Thực hiện nhiệm vụ`, `+ Bước 3: Báo cáo, thảo luận`, `+ Bước 4: Kết luận, nhận định`). Do đó Gemini xuất bảng ngắn gọn không có tiêu đề mục con, kích hoạt toàn bộ chuỗi lỗi của `repairActivityBlockFourParts` phá nát giáo án.

---

## Giải pháp Triệt để để Đưa Hệ Thống Về Trạng Thái Hoàn Hảo ("Như Hôm Trước")

### Nguyên tắc bất di bất dịch:
1. **Bảo vệ toàn vẹn cú pháp LaTeX & Text**: Tuyệt đối không dùng `slice(0, 400)`, không bóc tách lời thoại Bước 1 nhét vào nội dung, không bóc cột bảng nhét vào sản phẩm.
2. **Cấu trúc chuẩn CV 5512**: Mọi hoạt động (kể cả từng nhánh con 2.1, 2.2... của Hoạt động B) BẮT BUỘC có đủ:
   - `#### a) Mục tiêu:`
   - `#### b) Nội dung:`
   - `#### c) Sản phẩm:`
   - `#### d) Tổ chức thực hiện:` (Bảng 2 cột đủ 4 bước: Bước 1, Bước 2, Bước 3, Bước 4).
3. **Cả 2 chế độ Soạn (Chi tiết & Rút gọn) đều phải giữ khung 4 mục và 4 bước**: Chế độ rút gọn chỉ tinh giản câu từ, không phá vỡ khung pháp lý của Bộ Giáo dục.

---

## Chi tiết Triển khai cho Coder

### 1. File `js/khbd-prompts.js`
- **Sửa `ACTIVITY_TABLE_CONTRACT_COMPACT`**:
  Yêu cầu rõ ràng:
  + Dù là chế độ rút gọn, mỗi hoạt động (hoặc nhánh con 2.1, 2.2... của Mục B) BẮT BUỘC phải có đủ 4 đề mục:
    `#### a) Mục tiêu:`
    `#### b) Nội dung:`
    `#### c) Sản phẩm:`
    `#### d) Tổ chức thực hiện:`
  + Bảng Markdown `d) Tổ chức thực hiện:` BẮT BUỘC có 2 cột (`| Hoạt động của GV và HS | Nội dung |`) với Cột 1 đủ 4 bước chuẩn mực:
    `+ Bước 1: Chuyển giao nhiệm vụ:`
    `+ Bước 2: Thực hiện nhiệm vụ:`
    `+ Bước 3: Báo cáo, thảo luận:`
    `+ Bước 4: Kết luận, nhận định:`
  + Cột 2 BẮT BUỘC có kiến thức chốt bảng (quy tắc, công thức LaTeX, ví dụ mẫu ngắn).
- **Rà soát `GENERATE_ACTIVITY_B` và `expandActivityBSkeleton`**:
  Đảm bảo prompt mẫu luôn có đủ 4 mục `#### a) Mục tiêu:`, `#### b) Nội dung:`, `#### c) Sản phẩm:`, `#### d) Tổ chức thực hiện:` kèm bảng 2 cột đủ 4 bước cho tất cả các nhánh `Hoạt động 2.k`.

### 2. File `js/khbd-app.js`
- **Viết lại hoàn toàn `repairActivityBlockFourParts`**:
  1. Kiểm tra 4 cờ:
     - `hasA`: `/#{0,4}\s*a\)\s*Mục tiêu/i.test(b)`
     - `hasB`: `/#{0,4}\s*b\)\s*Nội dung/i.test(b)`
     - `hasC`: `/#{0,4}\s*c\)\s*Sản phẩm/i.test(b)`
     - `hasD`: `/#{0,4}\s*d\)\s*Tổ chức thực hiện/i.test(b)`
  2. Chuẩn hóa tiêu đề mục tiêu nếu có:
     `b = b.replace(/^(\s*)(?:#{1,4}\s*)?(?:[-*+]\s*)?Mục tiêu\s*:/im, "$1#### a) Mục tiêu:");`
  3. **Khôi phục `a) Mục tiêu:` nếu thiếu**:
     Nếu `!hasA`, tự động chèn vào trước `b)` (hoặc trước `c)`, `d)`, hoặc trước bảng):
     ```markdown
     #### a) Mục tiêu:
     - Học sinh hình thành và nắm vững kiến thức cốt lõi, hiểu rõ bản chất và vận dụng được quy tắc, định nghĩa của bài học/tiểu mục.

     ```
  4. **Khôi phục `b) Nội dung:` nếu thiếu**:
     **XÓA BỎ TRIỆT ĐỂ** việc bóc `step1` và cắt `slice(0, 400)`.
     Nếu `!hasB`, chèn câu sư phạm tĩnh chuẩn mực:
     ```markdown
     #### b) Nội dung:
     - Học sinh nghiên cứu SGK, làm việc cá nhân và thảo luận nhóm thực hiện các nhiệm vụ học tập khám phá kiến thức.

     ```
  5. **Khôi phục `c) Sản phẩm:` nếu thiếu**:
     **XÓA BỎ TRIỆT ĐỂ** việc bóc Cột 2 và cắt `slice(0, 400)`.
     Nếu `!hasC`, chèn câu sư phạm tĩnh chuẩn mực:
     ```markdown
     #### c) Sản phẩm:
     - Kết quả câu trả lời, lời giải chi tiết cho các nhiệm vụ khám phá và kiến thức cốt lõi ghi chép vào vở.

     ```
  6. **Khôi phục `d) Tổ chức thực hiện:` nếu thiếu**:
     Nếu có bảng mà chưa có tiêu đề `d)`, chèn `#### d) Tổ chức thực hiện:\n` ngay trước bảng.
  7. **Bảo tồn nguyên vẹn bảng 2 cột**:
     - Cột 1 giữ nguyên vẹn toàn bộ 4 bước kịch bản (`Bước 1..4`), không bị gọt xén hay gián đoạn.
     - Cột 2 giữ nguyên toàn bộ kiến thức, công thức LaTeX, đề bài và lời giải ví dụ.
- **Xóa bỏ việc gọi trùng lặp**:
  Trong `applyActivityOutput`, chỉ cần gọi `clipKhbdActivityMarkdown` (vốn đã gọi `ensureActivityFourPartStructure`), không gọi thừa bên ngoài.

### 3. File `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`
- Giữ nguyên cơ chế CDN fallback cho `khbd-prompts.js`, `khbd-pedagogy-catalog.js`, `khbd-docx.js` đã chứng minh hiệu quả chống 0-bytes hosting.
- Đồng bộ guard `typeof window.docxGenerator !== "undefined" || typeof window.DocxGenerator !== "undefined"`.

### 4. File kiểm thử `tests/khbd-table-columns-smoke.js`
- Thêm test case khẳng định:
  + Đầu vào Hoạt động B thiếu `a) Mục tiêu:` $\rightarrow$ Kết quả phải tự động khôi phục đủ `#### a) Mục tiêu:`.
  + Đầu vào Hoạt động B thiếu `b)` hoặc `c)` $\rightarrow$ Khôi phục bằng câu văn chuẩn sư phạm, TUYỆT ĐỐI KHÔNG làm gãy LaTeX (`$x^2 - \frac{1`) và không sinh nhãn đúp `- - GV:`.
  + Bảng Cột 1 giữ nguyên đủ cả 4 bước (`Bước 1..4`).
- Chạy toàn bộ test suite để đạt 100% PASS.

---

## File dự kiến tác động
1. `js/khbd-prompts.js`
2. `js/khbd-app.js`
3. `canvas_soankhbd.html`
4. `backupcode viettailieu/canvas_soankhbd.html`
5. `tests/khbd-table-columns-smoke.js`

---

## Các bước Coder triển khai chi tiết

### Bước 1: Cập nhật `ACTIVITY_TABLE_CONTRACT_COMPACT` trong `js/khbd-prompts.js`
- Bổ sung yêu cầu bắt buộc: Xuất đủ 4 mục `#### a) Mục tiêu:`, `#### b) Nội dung:`, `#### c) Sản phẩm:`, `#### d) Tổ chức thực hiện:` và bảng kịch bản 4 bước (`+ Bước 1:`, `+ Bước 2:`, `+ Bước 3:`, `+ Bước 4:`).

### Bước 2: Viết lại `repairActivityBlockFourParts` trong `js/khbd-app.js`
- Bổ sung kiểm tra `hasA` và tự động chèn `#### a) Mục tiêu:`.
- Xóa bỏ việc bóc `step1` và Cột 2 bằng `.slice(0, 400)`.
- Chèn câu sư phạm tĩnh chuẩn mực cho `b)` và `c)` khi thiếu.
- Giữ nguyên vẹn bảng 2 cột 4 bước.

### Bước 3: Đồng bộ 2 file HTML
- Đồng bộ guard nạp `khbd-docx.js` fallback.

### Bước 4: Chạy kiểm thử tự động
- `node tests/canvas-prompts-integrity-smoke.js`
- `node tests/canvas-soankhbd-smoke.js`
- `node tests/khbd-table-columns-smoke.js`
- `node tests/khbd-pedagogy-rate-smoke.js`
- `node tests/khbd-nls-ai-bold-italic-smoke.js`
- Xác nhận 100% tests PASS.
