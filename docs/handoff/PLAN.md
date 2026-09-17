# PLAN: Khắc phục lỗi lẫn lộn 2 cột, lặp Header Word, lỗi render begincases & Chuẩn hóa sư phạm giải hệ phương trình

## Hiện trạng & Phân tích nguyên nhân gốc rễ (Qua 4 ảnh phản ánh của người dùng)

> [!IMPORTANT]
> **Điểm mấu chốt được xác nhận:** Nhiều khi AI sinh nội dung Markdown và LaTeX hoàn toàn đúng chuẩn, trên Web Preview (Marked + KaTeX) hiển thị bình thường, nhưng **KHI XUẤT VÀ RENDER SANG WORD (.docx) THÌ CHÍNH BỘ TRÌNH DIỄN WORD (`js/khbd-docx.js`) LÀ NƠI GÂY RA LỖI** làm hỏng bố cục bảng và công thức!

---

### 1. Lẫn lộn nội dung giữa 2 cột (Cột Hoạt động GV-HS và Cột Nội dung) (Ảnh 1 & 2)
- **Hiện tượng**: 
  - Ở bảng mục *d) Tổ chức thực hiện*, Bước 1 và nửa đầu Bước 2 nằm ở Cột trái ("Hoạt động của GV và HS").
  - Nhưng ngay giữa Bước 2, từ đoạn `(Số luống | Số cây/luống | Tổng số cây)...` cùng toàn bộ Bước 3 và Bước 4 lại bị nhảy sang Cột phải ("Nội dung").
  - Cột phải vốn chỉ dành để ghi bảng kiến thức toán học thì nay chứa toàn bộ kịch bản phân vai của GV và HS.
- **Nguyên nhân cốt lõi trong Word Renderer & Xử lý Markdown**:
  - Khi AI sinh văn bản gợi ý giáo viên hướng dẫn học sinh lập bảng nháp, AI đã viết dấu gạch đứng `|` bên trong ô: `(Số luống | Số cây/luống | Tổng số cây)`.
  - Hàm `splitKhbdMarkdownTableRow` gặp ký tự `|` (không nằm trong `$...$`) nên đã tách dòng này thành 3–4 cells thay vì 2 cells.
  - Cả `createDocxTableFromMarkdown` trong `js/khbd-docx.js` (dòng 911–913) và `mergeSplitActivityTables` trong `js/khbd-app.js` (dòng 5870, 5881) đều có cơ chế gộp cell thô sơ:
    `const rawCells = isActivityTwoCol && parsedCells.length > 2 ? [parsedCells[0], parsedCells.slice(1).join(" | ")] : parsedCells;`
    Code mặc định gán `parsedCells[0]` vào Cột 1 và tống **TẤT CẢ** các cell còn lại (`cells.slice(1)`) vào Cột 2!
  - Hậu quả: Toàn bộ phần nội dung sau dấu `|` đầu tiên (gồm nửa sau Bước 2, Bước 3, Bước 4 và các câu thoại `- GV:`, `- HS:`) bị đẩy sạch sang Cột phải ("Nội dung").

---

### 2. Lặp toàn bộ khung tiêu đề bài dạy trên đầu mọi trang Word (Ảnh 2)
- **Hiện tượng**:
  - Trang 2, trang 3 trở đi của file Word xuất ra đều bị lặp lại nguyên khối tiêu đề ở đầu trang:
    `Trường THCS TRẦN PHÚ | Giáo viên: Hoàng Tấn Thiên`
    `CHƯƠNG I: PHƯƠNG TRÌNH VÀ HỆ HAI PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN`
    `TIẾT 3, 4, 5 - BÀI 2: GIẢI HỆ HAI PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN`
    `Thời lượng thực hiện: 03 tiết (135 phút)`
  - Khối này chiếm tới 1/3 trang giấy, chèn ép lên bảng hoạt động đang ngắt trang.
- **Nguyên nhân cốt lõi trong Word Renderer**:
  - Tại dòng 1379 file `js/khbd-docx.js`:
    `section.headers = { default: new Header({ children: headerElements }) };`
  - Code đã gán toàn bộ `headerElements` vào Running Header mặc định của Word. Trong quy chuẩn văn bản giáo án (CV 5512, NĐ 30/2020/NĐ-CP), tiêu đề bài dạy chỉ xuất hiện một lần duy nhất ở trang 1 của phần Thân văn bản (Body), không bao giờ là Running Header lặp lại trên mọi trang.

---

### 3. Lỗi render công thức Word: `begincases` và mất dấu ngoặc nhọn hệ phương trình (Ảnh 3 & Ảnh bổ sung)
- **Hiện tượng thực tế**:
  - Khi biểu diễn biến đổi tương đương hệ phương trình, ví dụ:
    ```
    - Thu gọn hệ phương trình:
    { xy - 2x + 3y - 6 = xy - 9
    { xy + 3x - 2y - 6 = xy + 10
      ⇔ begincases - 2x + 3y = -3; 3x - 2y = 16endcases
    ```
  - **Sự đối lập rõ rệt:**
    + Hệ phương trình đầu tiên đứng độc lập (không có tiền tố) thì Word render được dấu ngoặc nhọn `{` bình thường.
    + Nhưng ngay dòng tiếp theo, khi có dấu tương đương ở đầu dòng (`\Leftrightarrow \begin{cases} ... \end{cases}` hoặc `\Rightarrow \begin{cases} ... \end{cases}`), Word lập tức vỡ vụn thành:
      `⇔ begincases - 2x + 3y = -3; 3x - 2y = 16endcases`
    + Mất hoàn toàn dấu ngoặc nhọn `{` biểu thị hệ phương trình, lộ các từ khóa `begincases` và `endcases` gây mất thẩm mỹ nghiêm trọng.
- **Nguyên nhân cốt lõi trong Word OMML Math Converter (`js/khbd-docx.js`)**:
  - Hàm `createCasesMath` trong `js/khbd-docx.js` chỉ bắt regex khi `\begin{cases}` nằm ở vị trí đầu tiên tuyệt đối của chuỗi:
    `const casesMatch = source.match(/^\\begin\s*\{(cases|aligned)\}([\s\S]*?)\\end\s*\{\1\}\s*$/i);`
  - Khi biểu thức toán có tiền tố như `\Leftrightarrow \begin{cases} ... \end{cases}` (rất phổ biến khi giải toán: `$\Leftrightarrow \begin{cases} ... \end{cases}$`), regex trên không khớp (`casesMatch === null`).
  - Hàm rơi về bộ phân tích `createNativeMath`: bộ này không nhận diện lệnh `\begin`, nên đọc chữ cái `\begin` thành chữ `"begin"`, đọc `{cases}` thành `"c"`, `"a"`, `"s"`, `"e"`, `"s"`, và `\end{cases}` thành `"endcases"`.
  - Trong hàm fallback `latexToUnicodeMath`, dòng 159 thực hiện: `s = s.replace(/[{}]/g, "")`, xóa sạch mọi dấu ngoặc nhọn `{`, khiến hệ phương trình mất luôn dấu ngoặc ôm khi xuất ra Word.

---

### 4. Dùng sai quy chuẩn sư phạm Toán học CT GDPT 2018: Dùng dấu tương đương `\Leftrightarrow` ở cấp THCS & Lời giải nhảy cóc (Ảnh 3 & 4)
- **Quy chuẩn sư phạm môn Toán theo Chương trình GDPT 2018**:
  > [!CAUTION]
  > **QUY ĐỊNH CỐT LÕI CỦA CT GDPT 2018 CẤP THCS (LỚP 6, 7, 8, 9):**
  > Trong SGK hiện hành (Kết nối tri thức, Cánh diều, Chân trời sáng tạo) cấp THCS, **TUYỆT ĐỐI KHÔNG DÙNG DẤU TƯƠNG ĐƯƠNG ($\Leftrightarrow$)**!
  > Khái niệm mệnh đề và ký hiệu tương đương ($\Leftrightarrow$) đã được dời lên chương trình Toán lớp 10 (THPT). Ở cấp THCS, học sinh và giáo viên **bị cấm dùng dấu $\Leftrightarrow$**.
- **Hiện trạng & Sai phạm của AI**:
  - AI bị ảnh hưởng bởi SGK cũ (CT 2006) và dữ liệu toán cấp 3/đại học nên liên tục chèn ký hiệu `\Leftrightarrow` vào đầu hệ phương trình: `\Leftrightarrow \begin{cases} ... \end{cases}`. Điều này vừa **SAI CHUẨN SƯ PHẠM CẤP THCS**, vừa kích hoạt lỗi render `begincases` trong Word!
  - Lời giải bài tập và vận dụng bị nhảy cóc: AI dùng dấu `\Rightarrow` nối tắt từ hệ phương trình thẳng ra nghiệm (`Hệ {...} \Rightarrow x = 666,67; y = 1333,33`), không trình bày các bước giải theo phương pháp thế hoặc phương pháp cộng đại số (kiến thức cốt lõi của Bài 2 Toán 9).
  - Phép biến đổi đại số sai (Ảnh 3: $xy + 2x - 4y - 8 = xy$ nhưng dòng dưới lại viết tương đương $2x - 4y = 40$).
- **Nguyên nhân**:
  - Prompt trong `js/khbd-prompts.js` và `js/khbd-app.js` chưa có chỉ thị nghiêm ngặt về quy chuẩn CT GDPT 2018:
    + CẤM dùng dấu tương đương `\Leftrightarrow` cho môn Toán THCS (lớp 6, 7, 8, 9).
    + BẮT BUỘC trình bày các bước biến đổi bằng câu dẫn sư phạm chuẩn mực ("Thu gọn hệ phương trình, ta được:", "Từ phương trình (1) ta có:", "Thay ... vào (2), ta được:", "hay", "Do đó:") hoặc xuống dòng viết hệ phương trình độc lập `$$\begin{cases} ... \end{cases}$$` không có dấu `\Leftrightarrow` ở đầu.

---

## Phạm vi giải pháp & Kế hoạch triển khai

### Module 1: Sửa triệt để lỗi lẫn lộn 2 cột & chống vỡ bảng Markdown
1. **Cập nhật Prompt cấm dấu `|` nội dung (`js/khbd-prompts.js`)**:
   - Thêm quy định nghiêm ngặt:
     `QUY TẮC CỘT BẢNG TUYỆT ĐỐI: Mỗi hàng bảng Markdown chỉ có đúng 2 cột (| Hoạt động của GV và HS | Nội dung |). TUYỆT ĐỐI CẤM dùng ký tự gạch đứng | bên trong nội dung văn bản dưới mọi hình thức (kể cả trong bảng phân tích, ghi chú hay công thức). Khi liệt kê bắt buộc dùng dấu phẩy (,), dấu gạch chéo (/), hoặc ký hiệu \vert / \|. Vi phạm sẽ làm vỡ bảng.`
2. **Bộ chia cột thông minh theo ngữ nghĩa (Smart Semantic Column Splitter) trong `js/khbd-docx.js` & `js/khbd-app.js`**:
   - Viết hàm `semanticSplitActivityRow(cells)`:
     + Khi một hàng dữ liệu có nhiều hơn 2 cells (do dấu `|` lọt vào bên trong ô):
     + KHÔNG gom mù quáng `parsedCells.slice(1)` vào Cột 2.
     + Thay vào đó, nhận diện ranh giới cột thực sự: Cột 1 là cột chứa các marker kịch bản sư phạm (`Bước 1`, `Bước 2`, `Bước 3`, `Bước 4`, `GV:`, `HS:`, `[Kỹ thuật`, `[Phương pháp`).
     + Bất kỳ cell nào chứa các marker này đều thuộc về Cột 1 (ghép lại bằng khoảng trắng hoặc gạch chéo thay vì dấu `|`).
     + Chỉ chuyển sang Cột 2 khi gặp cell bắt đầu bằng tiêu đề nội dung kiến thức ghi bảng (định nghĩa, công thức, ví dụ mẫu, luyện tập, bài tập, vận dụng không có vai GV/HS).
3. **Chuẩn hóa `mergeSplitActivityTables` trong `js/khbd-app.js`**:
   - Sử dụng cơ chế phân tách thông minh trên để không bao giờ để lọt Bước 3, Bước 4 của GV/HS sang Cột Nội dung.

---

### Module 2: Bỏ lặp tiêu đề bài dạy trên mọi trang Word (`js/khbd-docx.js`)
1. **Đưa khung tiêu đề bài dạy vào phần Body**:
   - Trong `exportFullLessonPlan` (`js/khbd-docx.js` dòng 1378–1385):
   - Đưa `headerElements` vào đầu danh sách phần tử của Body:
     `section.children = [...headerElements, ...bodyElements];`
   - Bỏ gán `headerElements` vào `section.headers.default`.
   - `section.headers` để trống hoặc chỉ chứa header phụ rất nhỏ và mờ nếu cần (hoặc `undefined`).

---

### Module 3: Sửa lỗi render `begincases` và OMML Math trong Word Converter (`js/khbd-docx.js`)
1. **Mở rộng `createCasesMath` hỗ trợ tiền tố toán tử**:
   - Cho phép nhận diện hệ phương trình có tiền tố như `\Leftrightarrow`, `\Rightarrow`, dấu tương đương:
     Hỗ trợ regex: `^([\s\S]*?)\\begin\s*\{(cases|aligned)\}([\s\S]*?)\\end\s*\{\2\}\s*$`
   - Nếu có tiền tố: tạo MathRun/Math symbol cho tiền tố đó trước, sau đó nối tiếp khối delimiter ngoặc nhọn `{` chứa `equationArray`.
2. **Hỗ trợ `\begin{cases}` trực tiếp trong `createNativeMath`**:
   - Khi đọc lệnh `\begin` trong sequence của `createNativeMath`: nếu argument là `cases` hoặc `aligned`, tự động chuyển sang cơ chế delimiter mở `{` và tập hợp các dòng phân cách bởi `\\` thành một `m:eqArr`, không để rơi rớt thành các chữ cái `begincases`...`endcases`.
3. **Bảo vệ ngoặc nhọn trong `latexToUnicodeMath`**:
   - Sửa dòng `s = s.replace(/[{}]/g, "")` thành hàm dọn dẹp có chọn lọc: chỉ xóa các cặp `{}` rỗng hoặc ngoặc bao số mũ/chỉ số dưới, giữ nguyên dấu ngoặc nhọn `{` đứng trước hệ phương trình.

---

### Module 4: Kỷ luật sư phạm Toán học CT GDPT 2018 & Chuẩn hóa phương pháp giải (`js/khbd-prompts.js`, `js/khbd-app.js`)
1. **Bổ sung khối Ràng buộc Sư phạm Toán học CT GDPT 2018 (Math Pedagogical Guard)**:
   - **Quy tắc sử dụng dấu chuẩn CT GDPT 2018**:
     + **CẤP THCS (LỚP 6, 7, 8, 9): TUYỆT ĐỐI CẤM DÙNG DẤU TƯƠNG ĐƯƠNG ($\Leftrightarrow$)**! Khái niệm mệnh đề và ký hiệu tương đương thuộc chương trình lớp 10.
     + BẮT BUỘC dùng lời dẫn sư phạm chuẩn mực:
       * *"Thu gọn hệ phương trình, ta được:"*
       * *"Từ phương trình (1) ta có: $x = ...$"*
       * *"Thay $x = ...$ vào phương trình (2), ta được:"*
       * *"Cộng từng vế hai phương trình, ta được:"*
       * *"Do đó ta có hệ phương trình:"*
       hoặc xuống dòng đặt hệ phương trình trên dòng riêng biệt `$$\begin{cases} ... \end{cases}$$` mà **KHÔNG CÓ** dấu $\Leftrightarrow$ ở đầu.
     + **TUYỆT ĐỐI CẤM** dùng dấu suy ra $\Rightarrow$ để nối tắt từ hệ phương trình sang nghiệm (cấm: `{hệ} => x = ..., y = ...`).
     + Phải có câu kết luận nghiệm chuẩn mực SGK: `"Vậy nghiệm của hệ phương trình là (x; y) = (...; ...)"` hoặc `"Vậy hệ phương trình có nghiệm duy nhất (x; y) = (...; ...)"`.
     + *(Đối với cấp THPT lớp 10–12: Cho phép dùng $\Leftrightarrow$. Bộ chuyển đổi Word OMML vẫn hỗ trợ phòng vệ toàn diện cho cả hai trường hợp).*
   - **Quy tắc bám sát phương pháp giải của bài học (Phương pháp thế & Phương pháp cộng đại số)**:
     + Trong lời giải mẫu (Ví dụ), Luyện tập và Vận dụng:
       BẮT BUỘC phải trình bày từng bước giải tường minh theo đúng phương pháp đang dạy trong bài:
       * **Phương pháp thế**: (1) Từ một phương trình rút 1 ẩn theo ẩn kia $\rightarrow$ (2) Thế vào phương trình còn lại để được phương trình bậc nhất 1 ẩn $\rightarrow$ (3) Giải phương trình 1 ẩn $\rightarrow$ (4) Thế ngược lại tìm ẩn kia $\rightarrow$ (5) Kết luận nghiệm.
       * **Phương pháp cộng đại số**: (1) Nhân hệ số thích hợp (nếu cần) $\rightarrow$ (2) Cộng/trừ từng vế để triệt tiêu 1 ẩn $\rightarrow$ (3) Giải phương trình 1 ẩn $\rightarrow$ (4) Thay vào tìm ẩn còn lại $\rightarrow$ (5) Kết luận nghiệm.
     + CẤM nhảy cóc, CẤM chỉ viết hệ phương trình rồi phán ra đáp số.
   - **Độ chính xác đại số**: Chỉ thị kiểm tra cẩn thận quy tắc chuyển vế đổi dấu và nhân đơn thức với đa thức (tránh lỗi viết sai như ở Ảnh 3).

---

## File tác động
1. `js/khbd-docx.js`:
   - Hàm `createCasesMath` & `createNativeMath`: hỗ trợ an toàn nếu có tiền tố (`\Leftrightarrow`, `\Rightarrow`), không sinh chữ `begincases`/`endcases`.
   - Hàm `latexToUnicodeMath`: không xóa dấu ngoặc nhọn `{` của hệ phương trình.
   - Hàm `createDocxTableFromMarkdown`: áp dụng `semanticSplitActivityRow` chống dồn ô sang Cột 2.
   - Hàm `exportFullLessonPlan`: đưa tiêu đề bài học vào Body, bỏ lặp trên Running Header của mọi trang.
2. `js/khbd-app.js`:
   - Hàm `semanticSplitActivityRow` & `splitKhbdMarkdownTableRow`: chuẩn hóa tách cột theo ngữ nghĩa.
   - Hàm `mergeSplitActivityTables`: chống vỡ bảng khi có dấu `|` nội dung.
   - Hàm `buildPedagogicalPrompt`: bổ sung Math Pedagogical Guard cho môn Toán (cấm $\Leftrightarrow$ ở cấp THCS, bắt buộc giải chi tiết).
3. `js/khbd-prompts.js`:
   - Cấm triệt để dấu `|` bên trong ô kịch bản.
   - Bổ sung quy tắc sư phạm môn Toán chuẩn CT GDPT 2018: cấm dấu $\Leftrightarrow$ ở THCS (lớp 6–9), bắt buộc giải chi tiết theo phương pháp thế / cộng đại số, cấm nhảy cóc, cấm dùng sai dấu `\Rightarrow`.
4. `tests/khbd-table-columns-smoke.js`:
   - Bổ sung test case khi Cột 1 có dấu `|` bên trong (như `(Số luống | Số cây/luống | Tổng số cây)`), bảo đảm Bước 3 và Bước 4 vẫn nằm đúng ở Cột 1.
5. `tests/khbd-docx-math-smoke.js`:
   - Bổ sung test case `$\Leftrightarrow \begin{cases} -3x+8y=-30 \\ 2x-4y=40 \end{cases}$` tạo đúng OMML delimiter `{`, không chứa token `begincases`.

---

## Tiêu chí nghiệm thu (Acceptance Criteria)
1. Khi xuất bảng 2 cột của mục *d) Tổ chức thực hiện*, toàn bộ Bước 1, Bước 2, Bước 3, Bước 4 của GV và HS nằm 100% ở Cột trái ("Hoạt động của GV và HS"); Cột phải ("Nội dung") chỉ chứa kiến thức ghi bảng. Dù văn bản có dấu `|` nội dung cũng không làm nhảy bước sang Cột phải.
2. File Word (.docx) xuất ra chỉ hiển thị khung tiêu đề bài dạy (Tên trường, tên GV, Chương, Bài, Thời lượng) ở đầu trang 1; các trang 2, 3, 4 không bị lặp lại khung tiêu đề này.
3. Công thức hệ phương trình có tiền tố như `$\Leftrightarrow \begin{cases} ... \end{cases}$` hiển thị chuẩn đẹp trong Word với dấu ngoặc nhọn `{`, không xuất hiện chữ `begincases` hay `endcases`.
4. Chuẩn sư phạm môn Toán THCS (lớp 6, 7, 8, 9): Tuyệt đối không dùng dấu tương đương $\Leftrightarrow$; trình bày chi tiết từng bước bằng câu dẫn sư phạm và giải theo phương pháp thế / cộng đại số; không dùng dấu $\Rightarrow$ nối tắt từ hệ sang nghiệm; kết luận nghiệm rõ ràng theo SGK.
5. Toàn bộ smoke test suites chạy `node tests/...` đạt kết quả PASS 100%.
